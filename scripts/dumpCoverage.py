#!/usr/bin/python
import time
import subprocess
import threading
import os

# Create output directory if it doesn't exist
output_dir = "E:\\droidagent\\output\\tippytipper\\ec"
os.makedirs(output_dir, exist_ok=True)

# Start DroidAgent in a separate thread
def run_droidagent():
    print("Starting DroidAgent...")
    subprocess.call("python run_droidagent.py --app tippytipper --output_dir ../output/tippytipper --is_emulator", shell=True)

# Start instrumented app
def start_instrumented_app():
    print("Starting instrumented app...")
    # Wait for DroidAgent to install the app first
    time.sleep(30)
    
    # Start the instrumented app using am instrument
    print("Launching instrumented tippytipper app...")
    subprocess.call("adb shell am instrument net.mandaria.tippytipper/net.mandaria.tippytipper.activities.test.JacocoInstrumentation", shell=True)

# Start DroidAgent in background
droidagent_thread = threading.Thread(target=run_droidagent)
droidagent_thread.daemon = True
droidagent_thread.start()

# Start instrumented app in background
instrumented_thread = threading.Thread(target=start_instrumented_app)
instrumented_thread.daemon = True
instrumented_thread.start()

# Wait a bit for both to start
time.sleep(40)

print("Starting coverage collection...")
i = 0
while i<250:
    i = i+1
    time.sleep(30)
    print(i)
    subprocess.call("adb -s emulator-5554 shell am broadcast -a generateECFile",shell=True)
    
    # subprocess.call(f"adb -s emulator-5554 exec-out run-as com.naman14.timber cat /data/data/com.naman14.timber/files/coverage.ec > E:\\droidagent\\output\\timber\\ec\\coverage{i}.ec",shell=True)

    #subprocess.call(f"adb -s emulator-5554 exec-out run-as net.stargw.fx cat /data/data/net.stargw.fx/files/coverage.ec > E:\\droidagent\\output\\stargwfx\\ec\\coverage{i}.ec",shell=True)

    #subprocess.call(f"adb -s emulator-5554 exec-out run-as com.blogspot.e_kanivets.moneytracker cat /data/data/com.blogspot.e_kanivets.moneytracker/files/coverage.ec > E:\\droidagent\\output\\moneytracker\\ec\\coverage{i}.ec",shell=True)

    #subprocess.call(f"adb -s emulator-5554 exec-out run-as it.feio.android.omninotes.alpha cat /data/data/it.feio.android.omninotes.alpha/files/coverage.ec > E:\\droidagent\\output\\omninotes\\ec\\coverage{i}.ec",shell=True)

    #subprocess.call(f"adb -s emulator-5554 exec-out run-as a2dp.Vol cat /data/data/a2dp.Vol/files/coverage.ec > E:\\droidagent\\output\\a2dp\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as net.alaindonesia.silectric cat /data/data/net.alaindonesia.silectric/files/coverage.ec > E:\\droidagent\\output\\silectric\\ec\\coverage{i}.ec",shell=True)
    
    # subprocess.call(f"adb -s emulator-5554 exec-out run-as agrigolo.chubbyclick cat /data/data/agrigolo.chubbyclick/files/coverage.ec > E:\\droidagent\\output\\chubbyclick\\ec\\coverage{i}.ec",shell=True)

    # subprocess.call(f"adb -s emulator-5554 exec-out run-as org.asdtm.goodweather cat /data/data/org.asdtm.goodweather/files/coverage.ec > E:\\droidagent\\output\\goodweather\\ec\\coverage{i}.ec",shell=True)

    #subprocess.call(f"adb -s emulator-5554 exec-out run-as protect.budgetwatch cat /data/data/protect.budgetwatch/files/coverage.ec > E:\\droidagent\\output\\budgetwatch\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as me.kuehle.carreport cat /data/data/me.kuehle.carreport/files/coverage.ec > E:\\droidagent\\output\\carreport\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as org.epstudios.epmobile cat /data/data/org.epstudios.epmobile/files/coverage.ec > E:\\droidagent\\output\\epmobile\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as com.github.axet.hourlyreminder cat /data/data/com.github.axet.hourlyreminder/files/coverage.ec > E:\\droidagent\\output\\hourlyreminder\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as info.bpace.munchlife cat /data/data/info.bpace.munchlife/files/coverage.ec > E:\\droidagent\\output\\munchlife\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as protect.rentalcalc cat /data/data/protect.rentalcalc/files/coverage.ec > E:\\droidagent\\output\\rentalcalc\\ec\\coverage{i}.ec",shell=True)
    
    subprocess.call(f"adb -s emulator-5554 exec-out run-as net.mandaria.tippytipper cat /data/data/net.mandaria.tippytipper/files/coverage.ec > E:\\droidagent\\output\\tippytipper\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as de.freewarepoint.whohasmystuff cat /data/data/de.freewarepoint.whohasmystuff/files/coverage.ec > E:\\droidagent\\output\\whohasmystuff\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as org.dynamicsoft.caloriescope cat /data/data/org.dynamicsoft.caloriescope/files/coverage.ec > E:\\droidagent\\output\\caloriescope\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as com.example.trigger cat /data/data/com.example.trigger/files/coverage.ec > E:\\droidagent\\output\\trigger\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as net.sf.andbatdog.batterydog cat /data/data/net.sf.andbatdog.batterydog/files/coverage.ec > E:\\droidagent\\output\\batterydog\\ec\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as de.retujo.bierverkostung cat /data/data/de.retujo.bierverkostung/files/coverage.ec > E:\\droidagent\\output\\bierverkostung\\ec\\coverage{i}.ec",shell=True)
    
    ### human testing ###
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as a2dp.Vol cat /data/data/a2dp.Vol/files/coverage.ec > E:\\droidagent\\output\\a2dp\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as net.alaindonesia.silectric cat /data/data/net.alaindonesia.silectric/files/coverage.ec > E:\\droidagent\\output\\silectric\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as agrigolo.chubbyclick cat /data/data/agrigolo.chubbyclick/files/coverage.ec > E:\\droidagent\\output\\chubbyclick\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as protect.budgetwatch cat /data/data/protect.budgetwatch/files/coverage.ec > E:\\droidagent\\output\\budgetwatch\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as me.kuehle.carreport cat /data/data/me.kuehle.carreport/files/coverage.ec > E:\\droidagent\\output\\carreport\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as org.epstudios.epmobile cat /data/data/org.epstudios.epmobile/files/coverage.ec > E:\\droidagent\\output\\epmobile\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as info.bpace.munchlife cat /data/data/info.bpace.munchlife/files/coverage.ec > E:\\droidagent\\output\\munchlife\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as net.sf.andbatdog.batterydog cat /data/data/net.sf.andbatdog.batterydog/files/coverage.ec > E:\\droidagent\\output\\batterydog\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as org.dynamicsoft.caloriescope cat /data/data/org.dynamicsoft.caloriescope/files/coverage.ec > E:\\droidagent\\output\\caloriescope\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as protect.rentalcalc cat /data/data/protect.rentalcalc/files/coverage.ec > E:\\droidagent\\output\\rentalcalc\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as net.mandaria.tippytipper cat /data/data/net.mandaria.tippytipper/files/coverage.ec > E:\\droidagent\\output\\tippytipper\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as com.github.axet.hourlyreminder cat /data/data/com.github.axet.hourlyreminder/files/coverage.ec > E:\\droidagent\\output\\hourlyreminder\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as com.example.trigger cat /data/data/com.example.trigger/files/coverage.ec > E:\\droidagent\\output\\trigger\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as de.freewarepoint.whohasmystuff cat /data/data/de.freewarepoint.whohasmystuff/files/coverage.ec > E:\\droidagent\\output\\whohasmystuff\\ec\\human\\coverage{i}.ec",shell=True)
    
    #subprocess.call(f"adb -s emulator-5554 exec-out run-as de.retujo.bierverkostung cat /data/data/de.retujo.bierverkostung/files/coverage.ec > E:\\droidagent\\output\\bierverkostung\\ec\\human\\coverage{i}.ec",shell=True)
    