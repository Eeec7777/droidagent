import time
import os
import shutil
import json
import argparse
import subprocess
import shlex

# Fix Windows encoding issues
import sys
import locale

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    # Set console encoding to UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    
    # Set default encoding for file operations
    try:
        import _locale
        _locale._getdefaultlocale = lambda: (None, 'utf-8')
    except:
        pass
    
    # Set environment encoding
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Fix JSON loading for androguard
    import json
    import builtins
    original_open = builtins.open
    def utf8_open(file, mode='r', **kwargs):
        if 'encoding' not in kwargs and 'b' not in mode:
            kwargs['encoding'] = 'utf-8'
        return original_open(file, mode, **kwargs)
    builtins.open = utf8_open
    
    # Fix json.load to handle encoding issues
    original_json_load = json.load
    def safe_json_load(fp, **kwargs):
        try:
            return original_json_load(fp, **kwargs)
        except UnicodeDecodeError:
            # If there's a unicode error, try to read as utf-8
            fp.seek(0)
            content = fp.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            return json.loads(content, **kwargs)
    json.load = safe_json_load


# Disable Google GenAI telemetry to avoid capture() errors
os.environ['GOOGLE_GENAI_DISABLE_TELEMETRY'] = '1'
os.environ['GOOGLE_ANALYTICS_DISABLED'] = '1'
os.environ['GOOGLE_CLOUD_DISABLE_TELEMETRY'] = '1'

from droidbot.device import Device
from droidbot.app import App
from droidbot.input_event import IntentEvent, KeyEvent

from droidagent import TaskBasedAgent

from device_manager import DeviceManager, ExternalAction, recover_activity_stack, is_loading_state
from collections import defaultdict, OrderedDict
from targets import initial_knowledge_map


SCRIPT_DIR = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(SCRIPT_DIR, '..', 'resources/personas')

POST_EVENT_WAIT = 1
MAX_STEP = 8000


def load_profile(profile_id):
    if not os.path.exists(os.path.join(PROFILE_DIR, f'{profile_id}.txt')):
        raise FileNotFoundError(f'Profile {profile_id} does not exist')

    with open(os.path.join(PROFILE_DIR, f'{profile_id}.txt'), 'r') as f:
        profile_content = f.read().strip()
    
    profile = OrderedDict()
    for l in profile_content.split('\n'):
        l = l.strip()
        if l.startswith('-'):
            l = l.removeprefix('-').strip()
            prop = l.split(':')[0].strip()
            val = l.split(':')[1].strip()
            profile[prop] = val
    
    return profile


def main(device, app, persona, debug=False):
    start_time = time.time()
    timeout_duration = 7200  # 2 hours in seconds
    agent = TaskBasedAgent(output_dir, app=app, persona=persona, debug_mode=debug)
    device_manager = DeviceManager(device, app, output_dir=output_dir)
    agent.set_current_gui_state(device_manager.current_state)
    need_state_update = False

    max_loading_wait = 3
    loading_wait_count = 0

    while True:
        # Check for timeout
        if time.time() - start_time > timeout_duration:
            print(f'Timeout reached ({timeout_duration} seconds)')
            device.uninstall_app(app)
            device.disconnect()
            device.tear_down()
            exit(0)
        
        if agent.step_count > MAX_STEP:
            print(f'Maximum number of steps reached ({agent.step_count})')
            device.uninstall_app(app)
            device.disconnect()
            device.tear_down()
            exit(0)

        if agent.step_count % 10 == 0:
            elapsed_time = time.time() - start_time
            remaining_time = timeout_duration - elapsed_time
            print(f'Time left: {round(remaining_time / 60, 2)} min')

        if is_loading_state(device_manager.current_state):
            loading_wait_count += 1

            if loading_wait_count > max_loading_wait:
                print('Loading state persisted for too long. Pressing the back button to go back to the previous state...')
                go_back_event = KeyEvent(name='BACK')
                event_dict = device_manager.send_event_to_device(go_back_event)
                agent.memory.append_to_working_memory(ExternalAction(f'{agent.persona_name} pressed the back button because there was no interactable widgets', [event_dict]), 'ACTION')
                loading_wait_count = 0
                continue
                
            else:
                print('Loading state detected. Waiting for the app to be ready...')
                time.sleep(POST_EVENT_WAIT)
                device_manager.fetch_device_state()
                need_state_update = True
                continue

        if need_state_update:   
            # seems that the loading is done and need to update the state captured right after the action to the recent state
            agent.set_current_gui_state(device_manager.current_state)
            device_manager.add_new_utg_edge()
            need_state_update = False
        
        action = agent.step()
        agent.save_memory_snapshot()
        
        if action is not None:
            event_records = []
            events = action.to_droidbot_event()
            for event in events:
                event_dict = device_manager.send_event_to_device(event, capture_intermediate_state=True, agent=agent)
                event_records.append(event_dict)
            
            action.add_event_records(event_records)

            recover_activity_stack(device_manager, agent)
            agent.set_current_gui_state(device_manager.current_state)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a task-based exploration')
    parser.add_argument('--app', type=str, help='name of the app to be tested', default='AnkiDroid')
    parser.add_argument('--output_dir', type=str, help='path to the output directory', default=None)
    parser.add_argument('--profile_id', type=str, help='name of the persona profile to be used', default='jade')
    parser.add_argument('--is_emulator', action='store_true', help='whether the device is an emulator or not', default=False)
    parser.add_argument('--debug', action='store_true', help='whether to run the agent in the debug mode or not', default=False)
    args = parser.parse_args()
    
    timestamp = time.strftime("%Y%m%d%H%M%S")

    if args.debug:
        output_dir = os.path.join(SCRIPT_DIR, f'../evaluation/data_new/{args.app}/agent_run_debug_{args.profile_id}')
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
    elif args.output_dir is None:
        output_dir = os.path.join(SCRIPT_DIR, f'../evaluation/data_new/{args.app}/agent_run_{args.profile_id}_{timestamp}')
    else:
        output_dir = args.output_dir

    device = Device(device_serial='emulator-5554', output_dir=output_dir, grant_perm=True, is_emulator=args.is_emulator)
    device.set_up()
    device.connect()

    app_path = os.path.join(SCRIPT_DIR, '../target_apps/' + args.app + '.apk')
    app = App(app_path, output_dir=output_dir)
    app_name = app.apk.get_app_name()

    persona = OrderedDict()
    persona.update(load_profile(args.profile_id))
    assert 'name' in persona, f'The persona profile {args.profile_id} does not have a name'
    persona_name = persona['name']

    persona.update({
        'ultimate_goal': 'visit as many pages as possible while trying their core functionalities',
        # 'ultimate_goal': 'check whether the app supports interactions between multiple users', # for QuickChat case study
        'initial_knowledge': initial_knowledge_map(args.app, persona_name, app_name),
    })

    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}/exp_info.json', 'w') as f:
        json.dump({
            'app_name': app_name,
            'app_path': os.path.abspath(app_path),
            'device_serial': device.serial,
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }, f, indent=4)
    
    device.install_app(app)
    
    # Use instrumentation command to start app instead of normal start
    # Get the instrumentation command for the app
    INSTRUMENTATION_COMMANDS = {
        "a2dp": "adb shell am instrument a2dp.Vol/a2dp.Vol.test.JacocoInstrumentation",
        "activitydiary": "adb shell am instrument de.rampro.activitydiary/de.rampro.activitydiary.ui.main.test.JacocoInstrumentation",
        "AnyCut": "adb shell am instrument com.example.anycut/com.example.anycut.test.JacocoInstrumentation",
        "BatteryDog": "adb shell am instrument net.sf.andbatdog.batterydog/net.sf.andbatdog.batterydog.test.JacocoInstrumentation",
        "Bierverkostung": "adb shell am instrument de.retujo.bierverkostung/de.retujo.bierverkostung.test.JacocoInstrumentation",
        "BudgetWatch": "adb shell am instrument protect.budgetwatch/protect.budgetwatch.test.JacocoInstrumentation",
        "CalorieScope": "adb shell am instrument org.dynamicsoft.caloriescope/org.dynamicsoft.caloriescope.activities.test.JacocoInstrumentation",
        "CarReport": "adb shell am instrument me.kuehle.carreport/me.kuehle.carreport.gui.test.JacocoInstrumentation",
        "chubbyclick": "adb shell am instrument agrigolo.chubbyclick/agrigolo.chubbyclick.test.JacocoInstrumentation",
        "Diaguard": "adb shell am instrument com.faltenreich.diaguard.beta/com.faltenreich.diaguard.feature.navigation.test.JacocoInstrumentation",
        "FruitRadar": "adb shell am instrument eu.quelltext.mundraub/eu.quelltext.mundraub.activities.test.JacocoInstrumentation",
        "getflow": "adb shell am instrument org.wentura.getflow/.test.JacocoInstrumentation",
        "good-weather": "adb shell am instrument org.asdtm.goodweather/.test.JacocoInstrumentation",
        "HourlyReminder": "adb shell am instrument com.github.axet.hourlyreminder/com.github.axet.hourlyreminder.test.JacocoInstrumentation",
        "mileage": "adb shell am instrument com.evancharlton.mileage/com.evancharlton.mileage.test.JacocoInstrumentation",
        "MunchLife": "adb shell am instrument info.bpace.munchlife/info.bpace.munchlife.test.JacocoInstrumentation",
        "omni-note": "adb shell am instrument it.feio.android.omninotes.alpha/it.feio.android.omninotes.test.JacocoInstrumentation",
        "OpenMoneyTracker": "adb shell am instrument com.blogspot.e_kanivets.moneytracker/com.blogspot.e_kanivets.moneytracker.test.JacocoInstrumentation",
        "RentalCalc": "adb shell am instrument protect.rentalcalc/protect.rentalcalc.test.JacocoInstrumentation",
        "tippytipper": "adb shell am instrument net.mandaria.tippytipper/net.mandaria.tippytipper.activities.test.JacocoInstrumentation"
    }
    
    # Use instrumentation command if available, otherwise use normal start
    if args.app in INSTRUMENTATION_COMMANDS:
        cmd = INSTRUMENTATION_COMMANDS[args.app]
        print(f"Starting app with instrumentation: {cmd}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: Instrumentation command failed: {result.stderr}")
            print("Falling back to normal app start...")
            device.start_app(app)
        else:
            print("Instrumentation started successfully")
    else:
        print(f"No instrumentation command found for {args.app}, using normal start")
        device.start_app(app)

    print('Waiting 10 secs for the app to be ready...')
    print('Output directory:', os.path.abspath(output_dir))
    time.sleep(10)
    
    try:
        main(device, app, persona, debug=args.debug)
    except (KeyboardInterrupt, TimeoutError) as e:
        print("Ending the exploration due to a user request or timeout.")
        print(e)
        device.uninstall_app(app)
        device.disconnect()
        device.tear_down()
        exit(0)

    except Exception as e:
        print("Ending the exploration due to an unexpected error.")
        print(e)
        device.uninstall_app(app)
        device.disconnect()
        device.tear_down()

        raise e
    
    device.uninstall_app(app)
    device.disconnect()
    device.tear_down()