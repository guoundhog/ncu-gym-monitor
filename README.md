# 中大重訓室：平日每小時 CSV

查看或下載：[data/weekday_hourly.csv](data/weekday_hourly.csv)

- 台灣時間週一到週五：09:30、10:30、11:30、12:30、13:30、14:30、15:30、16:30、17:30、18:30、19:30、20:30。
- GitHub Actions cron：`30 1-12 * * 1-5`（UTC）；共每天 12 個預定時段。
- 20:50 後、09:30 前及週末不寫入。每個小時時段最多一筆。
- 本設定持續執行，直到手動停用；已移除先前 10/12 的自動停止。
- 電腦可以關機。不使用 AI、不更新網站。
- 欄位：timestamp（實際擷取時間，台灣時區）、count（人數）、status（open／missing）、source（來源與錯誤原因）。
- 從官方公開 CSV 讀取唯一的「重訓室」列；只接受非負整數，0 是有效人數。
- 抓取失敗會安全重試一次，仍失敗則寫入 missing、人數留空，提交後標示 Actions 失敗。
- 原站沒有更新時間；資料代表擷取當下看到的官方公布數字，不能保證官方剛更新。未自動查核臨時休館公告。
- GitHub 排程可能延遲或漏執行；timestamp 不會假寫成預定時間，也不會用現在的人數補歷史空缺。
- 每次設定變更的連線檢查不會把非採樣時段的測試數字寫入 CSV。
- Actions 頁面中的 schedule 成功執行才證明排程有啟動。單次 push 成功不代表後續每小時必定執行。
- 如 CSV 停止增加，請看 Actions 最新執行時間、event 和結果；没有啟動的排程未必產生錯誤通知。
- 手動採樣：Actions → NCU weekday hourly CSV → Run workflow（仍受平日開放時段與每時段一筆限制）。
- 停止：Actions → NCU weekday hourly CSV → 選單 → Disable workflow。
- 舊 records.csv / records.json 僅保留歷史，現在不再更新；新的記錄不混入舊測試時段。
- repository 保持私人；帳號的 GitHub Actions 使用額度仍適用。

官方頁：https://pe.ncu.edu.tw/about/66.html
排程限制：https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
