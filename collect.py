import csv, io, json, re, sys, urllib.request, urllib.error
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTi7PeVb_4bE22ioWlIMlYwoaDbOQiq7fdn3VRAmS_5V60_9cmTh3P8e97jfvT5X867teqRsMoGY_Ou/pub?gid=0&single=true&output=csv"
END = datetime.fromisoformat("2026-10-12T10:00:00+08:00")
def now():
    return datetime.now(ZoneInfo("Asia/Taipei")).replace(microsecond=0)
def parse(raw):
    values = [r[1].strip() for r in csv.reader(io.StringIO(raw)) if len(r) >= 2 and r[0] == "重訓室"]
    if len(values) != 1 or not re.fullmatch(r"[0-9]+", values[0]):
        raise ValueError("重訓室欄位缺少唯一非負整數")
    return int(values[0])
def retrieve():
    for attempt in range(2):
        try:
            request = urllib.request.Request(SOURCE, headers={"Cache-Control":"no-cache"})
            with urllib.request.urlopen(request, timeout=25) as response:
                return parse(response.read().decode("utf-8-sig")), None
        except urllib.error.HTTPError as error:
            if not attempt and error.code in (429,500,502,503,504):
                continue
            return None, "官方來源HTTP錯誤 " + str(error.code)
        except (urllib.error.URLError, TimeoutError) as error:
            if not attempt:
                continue
            return None, "官方來源連線失敗：" + type(error).__name__
        except (ValueError, UnicodeError) as error:
            return None, "官方来源無有效人數：" + str(error)
def main():
    if now() >= END:
        print("Collection period ended.")
        return
    count, error = retrieve()
    retrieved = now()
    if retrieved >= END:
        return
    source = "中大官方公布人數／GitHub雲端採樣（實際擷取時間；原站無更新時間）"
    if not time(9,0) <= retrieved.time() <= time(20,50):
        status, count = "closed", None
        source += "；依一般09:00–20:50開放時間推定關閉"
    elif error:
        status, count = "missing", None
        source += "；" + error
    else:
        status = "open"
    record = dict(timestamp=retrieved.isoformat(), count=count, status=status, source=source)
    path = Path("data/records.json")
    records = json.loads(path.read_text()) if path.exists() else []
    if not isinstance(records, list):
        raise ValueError("Invalid stored records")
    if not any(r["timestamp"] == record["timestamp"] for r in records):
        records.append(record)
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False))
if __name__ == "__main__":
    main()
