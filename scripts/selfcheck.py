"""Self-check for the download retry added in src/downloader.py.

Run with:  python scripts/selfcheck.py

No test framework on purpose - this repo has none, and the thing worth
guarding is a handful of branches.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import downloader  # noqa: E402


class FakeResponse:
    def __init__(self, status):
        self.status_code = status
        self.headers = {"content-length": "3"}
        self.url = "https://example.invalid/x"

    def raise_for_status(self):
        if self.status_code >= 400:
            raise HttpError(self.status_code)

    def iter_content(self, chunk_size=8192):
        yield b"abc"


class HttpError(Exception):
    """Stands in for the HTTPError curl_cffi raises from raise_for_status()."""

    def __init__(self, status):
        super().__init__(f"HTTP {status}")
        self.response = FakeResponse(status)


def main() -> None:
    # 4xx means the resource is not there; retrying cannot help.
    assert not downloader._is_transient(HttpError(404)), "404 must not be retried"
    assert not downloader._is_transient(HttpError(403)), "403 must not be retried"
    # 5xx and transport-level problems are worth another go.
    assert downloader._is_transient(HttpError(503)), "503 should be retried"
    assert downloader._is_transient(OSError("connection reset")), "OSError should be retried"
    assert downloader._is_transient(TimeoutError("timed out")), "timeout should be retried"

    # A TLS/DNS blip: this is the failure that actually happened in CI
    # ("certificate subject name 'dotcom.glb' does not match target hostname").
    blip = Exception("curl: (60) SSL: certificate subject name mismatch")
    assert downloader._is_transient(blip), "TLS blip should be retried"

    # The retry loop: succeed on the third attempt without sleeping.
    calls = {"n": 0}

    def fake_get(url, stream=True):
        calls["n"] += 1
        if calls["n"] < 3:
            raise blip
        return FakeResponse(200)

    orig_get, orig_sleep = downloader.session.get, downloader.time.sleep
    downloader.session.get = fake_get
    downloader.time.sleep = lambda _s: None
    try:
        # _download_once writes the body out, so exercise just the wrapper's
        # control flow by letting the third call succeed through the real code.
        out = downloader.download_resource("https://example.invalid/x", "out.bin",
                                           attempts=4)
        assert out.exists(), "expected the retried download to write a file"
    finally:
        downloader.session.get = orig_get
        downloader.time.sleep = orig_sleep
        Path("out.bin").unlink(missing_ok=True)
    assert calls["n"] == 3, f"expected 3 attempts, made {calls['n']}"

    # A permanent 404 must not be retried.
    calls["n"] = 0

    def always_404(url, stream=True):
        calls["n"] += 1
        return FakeResponse(404)

    downloader.session.get = always_404
    downloader.time.sleep = lambda _s: None
    try:
        downloader.download_resource("https://example.invalid/x", "out.bin", attempts=4)
        raise AssertionError("expected a 404 to propagate")
    except HttpError:
        pass
    finally:
        downloader.session.get = orig_get
        downloader.time.sleep = orig_sleep
        Path("out.bin").unlink(missing_ok=True)
    assert calls["n"] == 1, f"404 should be tried once, tried {calls['n']}"

    print("selfcheck OK")


if __name__ == "__main__":
    main()