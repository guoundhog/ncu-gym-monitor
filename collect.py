import csv, io, json, os, re, urllib.request, urllib.error
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

SOURCE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTi7PeVb_4bE22ioWlIMlYwoaDbOQiq7fdn3VRAmS_5V60_9cmTh3P8e97jfvT5X867teqRsMoGY_Ou/pub?gid=0&single=true&output=csv"
DATA = Path("data/weekday_hourly.csv")

def eligible(stamp):
    local = stamp.astimezone(ZoneInfo("Asia/Taipei"))
    return local.weekday() < 5 and time(9,30) <= local.time() <= time(20,50)

def slot(stamp):
    local = stamp.astimezone(ZoneInfo("Asia/Taipei"))
    return local.date(), (local.hour * 60 + local.minute - 570) // 60
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

FIELDS = ["timestamp", "count", "status", "source"]
def observation(retrieved, count, error):
    source = "中大官方公布人數／GitHub雲端採樣（實際擷取時間；原站無更新時間）"
    if not time(9,0) <= retrieved.time() <= time(20,50):
        status, count = "closed", None
        source += "；依一般09:00–20:50開放時間推定關閉；未查核臨時休館公告"
    elif error:
        status, count = "missing", None
        source += "；" + error
    else:
        status = "open"
    return dict(timestamp=retrieved.isoformat(), count=count, status=status, source=source)

def validate(record):
    stamp = datetime.fromisoformat(record["timestamp"])
    if stamp.utcoffset() is None:
        raise ValueError("Timestamp has no timezone")
    if record["status"] not in ("open", "closed", "missing"):
        raise ValueError("Invalid status")
    value = record["count"]
    if record["status"] == "open":
        if type(value) is not int or value < 0:
            raise ValueError("Invalid count")
    elif value is not None:
        raise ValueError("Unavailable count must be null")
    if not isinstance(record["source"], str) or not record["source"]:
        raise ValueError("Missing source")

def save(record, path=DATA):
    validate(record)
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDS:
                raise ValueError("Invalid CSV header")
            records = list(reader)
        for row in records:
            value = row["count"]
            if value and not re.fullmatch(r"[0-9]+", value):
                raise ValueError("Invalid stored count")
            row["count"] = int(value) if value else None
    else:
        records = []
    if not isinstance(records, list):
        raise ValueError("Invalid stored records")
    seen = {}
    for row in records:
        validate(row)
        if row["timestamp"] in seen:
            raise ValueError("Duplicate stored timestamp")
        seen[row["timestamp"]] = row
    for row in records:
        if slot(datetime.fromisoformat(row["timestamp"])) == slot(datetime.fromisoformat(record["timestamp"])):
            print("This hourly slot already has an observation; skipped.")
            return
    if record["timestamp"] in seen:
        if seen[record["timestamp"]] != record:
            raise ValueError("Conflicting timestamp")
    else:
        records.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    os.replace(temporary, path)

def main():
    if not eligible(now()):
        print("Outside weekday 09:30–20:50 sampling window; skipped.")
        return
    count, error = retrieve()
    retrieved = now()
    if not eligible(retrieved):
        print("Retrieval completed outside sampling window; skipped.")
        return
    record = observation(retrieved, count, error)
    save(record)
    print(json.dumps(record, ensure_ascii=False))
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write("status=" + record["status"] + "\n")

if __name__ == "__main__":
    main()
