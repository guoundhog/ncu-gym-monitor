# 中大重訓室：平日每小時 CSV

查看／下載：[data/weekday_hourly.csv](data/weekday_hourly.csv)

- 台灣時間週一至週五，09:30 到20:30，每小時一次，12個預定時段。
- 實際採樣由 ChatGPT 雲端任務直接讀官方CSV並提交GitHub；電腦可以關機。此方法每次會使用ChatGPT任務，不再是純GitHub Actions。
- GitHub Actions 的不可靠cron與push採樣已停用，只保留手動執行。
- 新雲端排程從2026-10-07 14:30開始。當天14:40另有一次驗收；14:00:18/count41為真正擷取的設定驗證資料，並非14:30排程紀錄。
- CSV欄位：timestamp,count,status,source，UTF-8 BOM，可用Excel開啟。
- timestamp為實際台灣擷取時間，不替換成預定時刻。每個09:30起的60分鐘時段最多一筆。
- 只接受唯一「重訓室」列中的非負整數，真實0有效。失敗則missing/count空白並記原因，絕不以0代替失敗。
- 原官方來源 https://pe.ncu.edu.tw/about/66.html 及其公開CSV無更新timestamp；資料代表擷取時所見數字，未自動查核臨時休館公告。
- 不造假、不用現在的數字補歷史空缺；既有真實資料保留。
- 來源與寫入安全暫時錯誤最多重試一次。寫入後再讀回驗證。
- 成功保持安靜；無法存檔或取得有效數字則通知。
- 14:40驗收若沒有14:30起的新有效紀錄，查因並最多修復一次；無法確定可行修復則暫停採樣、明確告知無法達成穩定每小時要求。
- 舊records.csv與records.json保留歷史，不再更新。Sites同步保持暫停。
- 停止新排程：在ChatGPT Scheduled中暫停「中大平日每小時 CSV」。
