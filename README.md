# NCU gym monitor

One private repository, one GitHub Actions workflow, one Python collector, one CSV.
Your computer does not need to be on. No AI calls, website synchronization, external scheduler, or manually maintained credentials.

## Where to check
- Read or download [data/records.csv](data/records.csv).
- Open the repository's **Actions** tab and check the latest execution and its timestamp.
- The main branch is the authoritative data. The CSV opens in Excel (UTF-8 BOM).
- A green push/manual execution proves that one collection worked; only an execution marked **schedule** proves the timer triggered.
- If the CSV's latest timestamp stops advancing, inspect Actions. A missing scheduled execution does not necessarily generate a failure notification.
- To stop early: Actions → NCU gym CSV collector → menu → Disable workflow.
- To take one current observation manually: Actions → NCU gym CSV collector → Run workflow.

## Timing
Scheduled for minute **13, 33, 53** of every hour, about 20 minutes apart, away from the hourly peak.
Collection ends **2026-10-12 10:00 Asia/Taipei**, preserving the original one-week study. The first subsequent execution disables the workflow.
GitHub's scheduler is best effort: a run can be delayed or dropped. A schedule configuration is not a guarantee of exact intervals.
There are no waiting jobs running between observations; each run exits after collecting and committing.

## Data correctness
Columns: timestamp, count, status, source.
- timestamp: actual retrieval time in Asia/Taipei, never scheduled time.
- open: a unique exact 重訓室 row with a nonnegative integer; real 0 is valid.
- missing: source unavailable, ambiguous or nonnumeric; count is blank and source explains why.
- closed: inferred outside normal 09:00–20:50 hours; count is blank. Temporary closure announcements are not automatically checked.
- Source: https://pe.ncu.edu.tw/about/66.html and its linked published CSV.
- The official source provides no last-update time. A row captures the published count as seen at retrieval, not a guarantee it was freshly updated.
- Missed executions remain gaps. No fabricated readings or historical backfill with a current number.
- Two previous genuine JSON observations are migrated once, preserving their original timestamps/counts/status/source. The old JSON remains as an archive and is no longer updated.
- Network errors are retried once when safe. Source failure is saved as missing, then the workflow is marked failed. Invalid stored data fails without overwriting it.
- Concurrent collector runs are serialized. Commit push is retried once after a rebase.

## Costs and privacy
The repository stays private. Only GitHub Actions compute is used; its account usage limits still apply.
The CSV is not sent to the previous Site. The ChatGPT hourly sync is paused.
GitHub schedule behavior: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
