#!/usr/bin/env python3
"""
Footboom Universe — Queue Publisher
Reads post_queue.json and publishes the next 'ready' item to Instagram via MCP.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

QUEUE_FILE = Path("/home/ubuntu/footboom_agent/queue/post_queue.json")


def load_queue():
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)


def publish_reel(item):
    payload = {
        "type": "reels",
        "caption": item["caption"],
        "media": [
            {
                "type": "video",
                "media_url": item["video_cdn"],
                "thumbnail_url": item["cover_cdn"]
            }
        ],
        "cover_url": item["cover_cdn"],
        "share_to_feed": True
    }

    cmd = [
        "manus-mcp-cli", "tool", "call", "create_instagram",
        "--server", "instagram",
        "--input", json.dumps(payload)
    ]

    print(f"[{datetime.now(timezone.utc).isoformat()}] Publishing: {item['match']}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode == 0:
        print(f"✅ Published successfully!\n{result.stdout}")
        return True
    else:
        print(f"❌ Publish failed:\n{result.stderr}")
        return False


def main():
    queue = load_queue()
    ready_items = [i for i in queue if i.get("status") == "ready"]

    if not ready_items:
        print("No items ready to publish.")
        return

    item = ready_items[0]
    print(f"Found queued item: {item['match']} (scheduled {item['scheduled_kyiv']})")

    success = publish_reel(item)

    # Update status
    for i in queue:
        if i["id"] == item["id"]:
            i["status"] = "published" if success else "failed"
            i["published_at"] = datetime.now(timezone.utc).isoformat()

    save_queue(queue)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
