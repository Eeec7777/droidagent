#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import subprocess
import threading
import os

# ============================================================================
# APP CONFIGURATION - 修改這裡來選擇要測試的APP
# ============================================================================
# 取消註解你要測試的APP，一次只能選擇一個
# ============================================================================

# APP_NAME = "a2dp"                    # Package: a2dp.Vol
APP_NAME = "activitydiary"           # Package: de.rampro.activitydiary
# APP_NAME = "AnyCut"                  # Package: com.example.anycut
# APP_NAME = "BatteryDog"              # Package: net.sf.andbatdog.batterydog
# APP_NAME = "Bierverkostung"          # Package: de.retujo.bierverkostung
# APP_NAME = "BudgetWatch"             # Package: protect.budgetwatch
# APP_NAME = "CalorieScope"            # Package: org.dynamicsoft.caloriescope
# APP_NAME = "CarReport"               # Package: me.kuehle.carreport
# APP_NAME = "chubbyclick"             # Package: agrigolo.chubbyclick
# APP_NAME = "Diaguard"                # Package: com.faltenreich.diaguard.beta
# APP_NAME = "FruitRadar"              # Package: eu.quelltext.mundraub
# APP_NAME = "getflow"                 # Package: org.wentura.getflow
# APP_NAME = "goodweather"            # Package: org.asdtm.goodweather
# APP_NAME = "HourlyReminder"          # Package: com.github.axet.hourlyreminder
# APP_NAME = "mileage"                 # Package: com.evancharlton.mileage
# APP_NAME = "MunchLife"               # Package: info.bpace.munchlife
# APP_NAME = "omninote"               # Package: it.feio.android.omninotes.alpha
# APP_NAME = "OpenMoneyTracker"        # Package: com.blogspot.e_kanivets.moneytracker
# APP_NAME = "RentalCalc"              # Package: protect.rentalcalc
# APP_NAME = "tippytipper"             # Package: net.mandaria.tippytipper

# ============================================================================
# APP PACKAGE MAPPING - 不要修改這裡
# ============================================================================
APP_PACKAGES = {
    "a2dp": "a2dp.Vol",
    "activitydiary": "de.rampro.activitydiary",
    "AnyCut": "com.example.anycut",
    "BatteryDog": "net.sf.andbatdog.batterydog",
    "Bierverkostung": "de.retujo.bierverkostung",
    "BudgetWatch": "protect.budgetwatch",
    "CalorieScope": "org.dynamicsoft.caloriescope",
    "CarReport": "me.kuehle.carreport",
    "chubbyclick": "agrigolo.chubbyclick",
    "Diaguard": "com.faltenreich.diaguard.beta",
    "FruitRadar": "eu.quelltext.mundraub",
    "getflow": "org.wentura.getflow",
    "goodweather": "org.asdtm.goodweather",
    "HourlyReminder": "com.github.axet.hourlyreminder",
    "mileage": "com.evancharlton.mileage",
    "MunchLife": "info.bpace.munchlife",
    "omninote": "it.feio.android.omninotes.alpha",
    "OpenMoneyTracker": "com.blogspot.e_kanivets.moneytracker",
    "RentalCalc": "protect.rentalcalc",
    "tippytipper": "net.mandaria.tippytipper"
}

# ============================================================================
# INSTRUMENTATION COMMANDS - 不要修改這裡
# ============================================================================
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
    "goodweather": "adb shell am instrument org.asdtm.goodweather/.test.JacocoInstrumentation",
    "HourlyReminder": "adb shell am instrument com.github.axet.hourlyreminder/com.github.axet.hourlyreminder.test.JacocoInstrumentation",
    "mileage": "adb shell am instrument com.evancharlton.mileage/com.evancharlton.mileage.test.JacocoInstrumentation",
    "MunchLife": "adb shell am instrument info.bpace.munchlife/info.bpace.munchlife.test.JacocoInstrumentation",
    "omninote": "adb shell am instrument it.feio.android.omninotes.alpha/it.feio.android.omninotes.test.JacocoInstrumentation",
    "OpenMoneyTracker": "adb shell am instrument com.blogspot.e_kanivets.moneytracker/com.blogspot.e_kanivets.moneytracker.test.JacocoInstrumentation",
    "RentalCalc": "adb shell am instrument protect.rentalcalc/protect.rentalcalc.test.JacocoInstrumentation",
    "tippytipper": "adb shell am instrument net.mandaria.tippytipper/net.mandaria.tippytipper.activities.test.JacocoInstrumentation"
}

# Get package name for selected app
PACKAGE_NAME = APP_PACKAGES[APP_NAME]
print(f"Selected APP: {APP_NAME}")
print(f"Package: {PACKAGE_NAME}")

# Create output directory if it doesn't exist
output_dir = f"E:\\droidagent\\output\\{APP_NAME}\\ec"
os.makedirs(output_dir, exist_ok=True)

# Start DroidAgent in a separate thread
def run_droidagent():
    print(f"Starting DroidAgent for {APP_NAME}...")
    subprocess.call(f"python run_droidagent.py --app {APP_NAME} --output_dir ../output/{APP_NAME} --is_emulator", shell=True)

# Start instrumented app
def start_instrumented_app():
    print(f"Starting instrumented app for {APP_NAME}...")
    # Wait for DroidAgent to install the app first
    time.sleep(30)
    
    # Start the instrumented app using am instrument
    print(f"Launching instrumented {APP_NAME} app...")
    
    # 使用對應的instrumentation command
    if APP_NAME in INSTRUMENTATION_COMMANDS:
        cmd = INSTRUMENTATION_COMMANDS[APP_NAME]
        print(f"Running instrumentation command: {cmd}")
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: Instrumentation command failed: {result.stderr}")
        else:
            print("Instrumentation started successfully")
    else:
        print(f"Warning: No instrumentation command found for {APP_NAME}")
    
    # 等待一段時間讓app完全啟動
    time.sleep(5)

# Start DroidAgent in background
droidagent_thread = threading.Thread(target=run_droidagent)
droidagent_thread.daemon = True
droidagent_thread.start()

# Start instrumented app in background
# instrumented_thread = threading.Thread(target=start_instrumented_app)
# instrumented_thread.daemon = True
# instrumented_thread.start()

# Wait a bit for both to start
time.sleep(40)

print("Starting coverage collection...")
i = 0
while i<250:
    i = i+1
    time.sleep(30)
    print(f"Coverage collection iteration {i} for {APP_NAME}")
    subprocess.call("adb -s emulator-5554 shell am broadcast -a generateECFile",shell=True)
    
    # Dump coverage for selected app
    subprocess.call(f"adb -s emulator-5554 exec-out run-as {PACKAGE_NAME} cat /data/data/{PACKAGE_NAME}/files/coverage.ec > E:\\droidagent\\output\\{APP_NAME}\\ec\\coverage{i}.ec",shell=True)

# ============================================================================
# SUMMARY: 
# 此腳本已更新支援20個Android應用程式的自動化coverage測試
# 
# 功能特色:
# 1. 支援20個APP的自動化測試 (a2dp, activitydiary, AnyCut, BatteryDog, Bierverkostung, BudgetWatch, CalorieScope, CarReport, chubbyclick, Diaguard, FruitRadar, getflow, good-weather, HourlyReminder, mileage, MunchLife, omni-note, OpenMoneyTracker, RentalCalc, tippytipper)
# 2. 自動化package name mapping
# 3. 每個APP都有對應的instrumentation command
# 4. 動態coverage collection，根據選擇的APP自動設定
# 5. 多線程執行DroidAgent和instrumented app
# 
# 使用方法:
# 1. 在APP_NAME區域取消註解你要測試的APP
# 2. 執行腳本: python dumpCoverage.py
# 3. 腳本會自動創建對應的output目錄
# 4. Coverage檔案會自動收集到對應的ec目錄
# ============================================================================
