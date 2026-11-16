import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta


def load_schedule(file_path="schedule.json"):
    """予定データを読み込む"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_by_date(events, target_date):
    """指定日の予定だけを抽出する"""
    result = []

    for event in events:
        start_dt = datetime.fromisoformat(event["start"])

        if start_dt.date().isoformat() == target_date:
            result.append(event)

    result.sort(key=lambda x: x["start"])
    return result


def format_event(event):
    """予定1件を表示用文字列にする"""
    start_dt = datetime.fromisoformat(event["start"])
    end_dt = datetime.fromisoformat(event["end"])

    start_time = start_dt.strftime("%H:%M")
    end_time = end_dt.strftime("%H:%M")

    location = event.get("location")

    if not location:
        location = "（場所なし）"

    return f"{start_time}-{end_time} {event['title']} @{location}"


def main():
    schedule_file = Path("schedule.json")

    if not schedule_file.exists():
        print("schedule.json が見つかりません。予定を表示できません。")
        return

    if len(sys.argv) >= 2:
        target_date = sys.argv[1]
    else:
        jst = timezone(timedelta(hours=9))
        target_date = datetime.now(jst).date().isoformat()

    try:
        events = load_schedule(schedule_file)
    except Exception as e:
        print(f"schedule.json の読み込みに失敗しました: {e}")
        return

    daily_events = filter_by_date(events, target_date)

    print(f"{target_date} の予定 {len(daily_events)} 件")

    for event in daily_events:
        print(format_event(event))


if __name__ == "__main__":
    main()