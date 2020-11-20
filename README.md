# UrlStat

Display some statistics on HTTP response times for a list of urls.

## Dependencies

- [httpx](https://www.python-httpx.org/)


## Installation

```shell script
$ poetry install
```

## Usage

```shell script
usage: urlstat.py [-h] [-t TIMEOUT] [-m MAX_CONNECTIONS] [-ka MAX_KEEP_ALIVE] [-r ALLOW_REDIRECTS] urls_path

Fetch url from a file and display response times stats

positional arguments:
  urls_path             Path to the url file (one url per line)

optional arguments:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout
  -m MAX_CONNECTIONS, --max-connections MAX_CONNECTIONS
                        Max concurrent connection
  -ka MAX_KEEP_ALIVE, --max-keep-alive MAX_KEEP_ALIVE
                        Max keep alive connections
  -r ALLOW_REDIRECTS, --allow-redirects ALLOW_REDIRECTS
                        Allow redirects
```

## Example

```shell script
$ ./urlstat.py urls_short.txt
invalid-url UnsupportedProtocol
http://www.google.co.in 200 0.135s
http://www.qq.com 200 0.159s
http://www.wikipedia.org 200 0.177s
http://www.facebook.com 200 0.382s
http://www.yahoo.com 200 0.316s
http://www.amazon.com 200 0.478s
http://www.youtube.com 200 0.642s
http://www.baidu.com 200 1.023s
http://www.twitter.com 200 1.271s
===========================================
Total time: 2.903s
Average response time: 0.509s
Median response time: 0.382s
90th percentile response time: 1.073s
Processed : 9/10
```
