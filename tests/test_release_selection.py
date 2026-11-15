"""Checks that 'latest' prefers the newest release, prereleases included,
in both the builder (src/utils.py) and the planner (scripts/check_app_updates.py).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from src import utils
import check_app_updates as planner

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

    planner.run_gh = lambda args, timeout=120: (0, json.dumps(RELEASES), "")
    planner._github_release_cache.clear()
    rel = planner._fetch_github_release_dict("u", "r", "latest")
    assert rel["tag_name"] == "v2.1.0-dev.1", rel

    print("PASS: latest picks newest non-draft release (prerelease preferred)")


if __name__ == "__main__":
    main()
