# NCU gym monitor

Private official published-count observations for the NCU weight room.

- Official page: https://pe.ncu.edu.tw/about/66.html
- `collect.py` reads the exact 重訓室 row from the official linked published CSV.
- GitHub Actions schedules retrieval at minute 7, 27 and 47 of every hour. Queuing may delay or miss a run. Timestamps are actual retrieval times in Asia/Taipei; missed observations are never fabricated.
- The source gives no last-update timestamp. These are observations of published counts, not guaranteed source refresh times.
- Normal hours 09:00–20:50 daily, subject to official closures. Outside normal hours: closed/null. Unavailable or ambiguous numeric values: missing/null. A real zero is valid.
- Records are appended to `data/records.json`. No Site credential is stored here or in Actions.
- Collection ends 2026-10-12 10:00 Asia/Taipei. The first workflow after that disables itself.
- The linked owner-private Site is https://ncu-gym-traffic.huangkaiyu0522.chatgpt.site , project `appgprj_6ac2fe3ade68819191345d337293e45d`.
- Its existing hourly cloud task retrieves this file through the authorized GitHub connector, obtains a fresh Sites service credential in memory, batches validated records into POST /api/records, and verifies them by dated GET /api/records. Timestamp conflicts are skipped. Only actual captured observations are imported.
- Quiet operation except collection/save failures or final week summary; occupancy averages exclude closed and missing records.
