#!/usr/bin/python3
# Generate hound config.

import json
import os
import urllib.request
import urllib.parse
from typing import Dict, Any, TextIO


DEFAULT_SETTINGS = {
    "max-concurrent-indexers": 4, 
    "dbpath": "data", 
    "title" : "Hound",
    "health-check-uri" : "/healthz",
}


def dump_file(settings: Dict[str, Any], fileobj: TextIO) -> None:
    json.dump(settings, fileobj, indent=4, sort_keys=True)
    fileobj.write("\n")


def get_githubrepos(username: str, page=None, per_page=100):
    path = f"https://api.github.com/users/{username}/repos"
    kw = {"per_page": 100}
    if page is not None:
        kw["page"] = page
        next_page = page + 1
    else:
        next_page = 2
    query = urllib.parse.urlencode(kw)
    with urllib.request.urlopen("{}?{}".format(path, query)) as resp:
        body = resp.read()
        if isinstance(body, bytes):
            body = body.decode("utf-8")  # type: ignore
        data = json.loads(body)
        if data:
            for repo in data:
                yield repo["name"], repo["html_url"]
            yield from get_githubrepos(username, next_page, per_page=per_page)


def main():
    settings = DEFAULT_SETTINGS.copy()
    settings["repos"] = repos = {}

    def addrepos(iterable):
        for name, url in iterable:
            repos[name] = {"url": url}

    usernames = [
        "balena-io",
        "balena-io-library",
        "balenalabs",
        "product-os",
        "people-os",
        "company-os",
        "balena-io-playground",
    ]
    
    for username in usernames:
        addrepos(get_githubrepos(username))

    with open("config.json", "w") as outfile:
        dump_file(settings, outfile)

if __name__ == "__main__":
    main()
