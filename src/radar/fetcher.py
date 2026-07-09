from __future__ import annotations

from dataclasses import dataclass

import httpx


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
        self.client = httpx.Client(
            headers={"User-Agent": self.user_agent},
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
        )

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "Fetcher":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()

    def fetch(self, url: str) -> FetchResult:
        try:
            response = self.client.get(url)
            return FetchResult(
                url=str(response.url),
                status_code=response.status_code,
                body=response.content,
                content_type=response.headers.get("Content-Type", ""),
            )
        except Exception as exc:  # network failures vary by platform
            return FetchResult(url=url, status_code=0, body=b"", error=str(exc))

