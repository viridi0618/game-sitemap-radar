from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    status_code: int
    body: bytes
    content_type: str = ""
    error: str | None = None


class Fetcher:
    def __init__(self, user_agent: str, timeout: int = 20):
        self.user_agent = user_agent
        self.timeout = timeout

    def fetch(self, url: str) -> FetchResult:
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return FetchResult(
                    url=url,
                    status_code=response.status,
                    body=response.read(),
                    content_type=response.headers.get("Content-Type", ""),
                )
        except urllib.error.HTTPError as exc:
            return FetchResult(url=url, status_code=exc.code, body=b"", error=str(exc))
        except Exception as exc:  # network failures vary by platform
            return FetchResult(url=url, status_code=0, body=b"", error=str(exc))

