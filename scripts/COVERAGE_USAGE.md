# DroidAgent Coverage Collection 使用說明

## 功能描述
這個腳本支持對 20 個 Android APP 進行自動化測試和覆蓋率收集。

## 支持的應用程序
1. A2dp (a2dp.Vol)
2. ActivityDiary (de.rampro.activitydiary)
3. AnyCut (com.anycut)
4. BatteryDog (net.sf.andbatdog.batterydog)
5. Bierverkostung (de.retujo.bierverkostung)
6. BudgetWatch (protect.budgetwatch)
7. CalorieScope (org.dynamicsoft.caloriescope)
8. CarReport (me.kuehle.carreport)
9. chubbyclick (agrigolo.chubbyclick)
10. Diaguard (com.faltenreich.diaguard)
11. FruitRadar (com.fruitradar)
12. getflow (com.getflow)
13. good-weather (org.asdtm.goodweather)
14. HourlyReminder (com.github.axet.hourlyreminder)
15. mileage (com.evancharlton.mileage)
16. MunchLife (info.bpace.munchlife)
17. omni-note (it.feio.android.omninotes.alpha)
18. OpenMoneyTracker (com.blogspot.e_kanivets.moneytracker)
19. RentalCalc (protect.rentalcalc)
20. tippytipper (net.mandaria.tippytipper)

## 使用方法

### 1. 選擇要測試的應用
編輯 `scripts/dumpCoverage.py` 文件，在開頭的配置部分：

```python
# 取消註解你要測試的APP，一次只能選擇一個
# APP_NAME = "A2dp"
# APP_NAME = "ActivityDiary"
# APP_NAME = "AnyCut"
APP_NAME = "BatteryDog"              # 當前選中的APP
# APP_NAME = "Bierverkostung"
# ...
```

### 2. 運行腳本
```bash
cd scripts
python dumpCoverage.py
```

### 3. 腳本會自動執行以下步驟：
1. 創建對應的輸出目錄 (`E:\droidagent\output\{APP_NAME}\ec`)
2. 啟動 DroidAgent 進行自動化測試
3. 啟動 instrumented 應用 (需要後續添加具體指令)
4. 收集覆蓋率數據 (每30秒一次，共250次)

### 4. 輸出結果
- 覆蓋率文件位置: `E:\droidagent\output\{APP_NAME}\ec\coverage{i}.ec`
- DroidAgent 日誌: `E:\droidagent\output\{APP_NAME}\`

## 待完成的工作
1. 添加每個APP的 instrument 指令到 `start_instrumented_app()` 函數
2. 驗證每個APP的包名是否正確

## 切換APP的快速方法
只需要修改一行代碼即可切換測試的APP：

```python
# 從這個
APP_NAME = "BatteryDog"

# 改成這個
APP_NAME = "tippytipper"
```

腳本會自動：
- 使用正確的包名
- 創建對應的輸出目錄
- 調用正確的 DroidAgent 參數
- 收集對應APP的覆蓋率數據

## 注意事項
- 一次只能測試一個APP
- 確保 Android 模擬器已啟動 (emulator-5554)
- 確保所有APP的APK文件都在 `target_apps/` 目錄下
- 需要為每個APP配置正確的 instrumentation 指令
