import json
from pathlib import Path

from src.services.history import save_post


HISTORY_FILE = Path("data/posts.json")


def migrate():
    if not HISTORY_FILE.exists():
        print("ℹ️ posts.json does not exist.")
        return

    with HISTORY_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        posts = json.load(file)

    if not posts:
        print("ℹ️ No posts found in posts.json.")
        return

    print(f"📦 Found {len(posts)} post(s)")

    for index, post in enumerate(posts, start=1):

        save_post(
            {
                "content": post.get("content"),
                "topic": post.get("topic"),
                "subtopic": post.get("subtopic"),
                "angle": post.get("angle"),
                "linkedin_post_id": post.get(
                    "linkedin_post_id"
                ),
                "quality_score": post.get(
                    "quality_score"
                ),
                "duplicate_score": post.get(
                    "duplicate_score"
                ),
                "status": post.get(
                    "status",
                    "published",
                ),
            }
        )

        print(f"✅ Migrated post {index}")


if __name__ == "__main__":
    migrate()