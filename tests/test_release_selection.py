"""Checks that 'latest' prefers the newest release, prereleases included."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import utils

RELEASES = [
    {"tag_name": "v2.0.0", "draft": False, "created_at": "2026-10-01", "assets": []},
    {"tag_name": "v2.1.0-dev.1", "draft": False, "created_at": "2026-10-09", "assets": []},
    {"tag_name": "v3.0.0-draft", "draft": True, "created_at": "2026-10-10", "assets": []},
]


def main() -> None:
    utils.gh_api_request = lambda endpoint: RELEASES
    utils.shutil.which = lambda name: "gh"
    utils.time.sleep = lambda seconds: None

    latest = utils.detect_github_release("u", "r", "latest")
    assert latest["tag_name"] == "v2.1.0-dev.1", latest

    print("PASS: latest picks newest non-draft release (prerelease preferred)")


if __name__ == "__main__":
    main()
