#!/bin/env python3
from typing import List, AsyncGenerator
import argparse
import asyncio
import time
from httpx import AsyncClient, HTTPError, Limits


def get_client(
    timeout: int,
    max_connections: int,
    max_keepalive_connections: int
) -> AsyncClient:
    return AsyncClient(
        timeout=timeout,
        limits=Limits(
            max_keepalive_connections=max_keepalive_connections,
            max_connections=max_connections
        )
    )


async def fetch(
    client: AsyncClient,
    url: str,
    allow_redirects: bool
) -> float:
    try:
        response = await client.get(url, allow_redirects=allow_redirects)
        elapsed = response.elapsed.total_seconds()
        print(url, response.status_code, f"{elapsed:.3f}s")
        return elapsed
    except HTTPError as e:
        print(url, type(e).__name__)


async def read_urls(urls_path: str) -> AsyncGenerator[str, None]:
    with open(urls_path, "r") as f:
        for line in f.readlines():
            url = line.strip()
            if url:
                yield url


def percentile(values: List[float], n: float) -> float:
    """
    Calculate the linear interpolated percentile from an array of values
    :param values: an array of values
    :param n: percentage / 100 : 0 < n < 1
    :return: percentile value
    """
    if len(values) == 1:
        return values[0]
    values = sorted(values)
    float_index = n*(len(values)-1)
    i = int(float_index)
    w = abs(float_index-i)
    return values[i] + w*(values[i+1]-values[i])


def print_stats(times: List[float]) -> None:
    processed = [t for t in times if t is not None]
    if processed:
        print_time_fields(
            ("Average response time", sum(processed)/len(processed)),
            ("Median response time", percentile(processed, 0.5)),
            ("90th percentile response time", percentile(processed, 0.9))
        )
    print(f"Processed : {len(processed)}/{len(times)}")


def print_time_fields(*fields) -> None:
    for name, t in fields:
        print(f"{name}: {t:.3f}s")


async def main(
    urls_path: str,
    timeout: int,
    max_connections: int,
    max_keepalive_connections: int,
    allow_redirects: bool
) -> None:
    client = get_client(
        timeout=timeout,
        max_connections=max_connections,
        max_keepalive_connections=max_keepalive_connections
    )
    start = time.perf_counter()
    times = await asyncio.gather(*[
        asyncio.create_task(fetch(client, url, allow_redirects))
        async for url in read_urls(urls_path)
    ])
    print("===========================================")
    print_time_fields(
        ("Total time", time.perf_counter()-start)
    )
    print_stats(times)
    await client.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch url from a file and display response times stats"
    )
    parser.add_argument(
        "urls_path", help="Path to the url file (one url per line)"
    )

    parser.add_argument(
        "-t", "--timeout", help="Timeout",
        dest="timeout", type=int, default=30
    )

    parser.add_argument(
        "-m", "--max-connections", help="Max concurrent connection",
        dest="max_connections", type=int, default=300
    )

    parser.add_argument(
        "-ka", "--max-keep-alive",
        help="Max keep alive connections",
        dest="max_keep_alive", type=int, default=30
    )

    parser.add_argument(
        "-r", "--allow-redirects",
        help="Allow redirects",
        dest="allow_redirects", type=bool, default=True
    )

    args = parser.parse_args()

    asyncio.run(
        main(
            urls_path=args.urls_path,
            timeout=args.timeout,
            max_connections=args.max_connections,
            max_keepalive_connections=args.max_keep_alive,
            allow_redirects=args.allow_redirects
        )
    )
