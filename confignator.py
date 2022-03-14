#!/usr/bin/python3
# Generate hound's config.json file

import json
import urllib.request
import urllib.parse
from typing import Dict, Any

# Settings for Hound https://github.com/hound-search/hound#keeping-repos-updated
DEFAULT_SETTINGS = {
    "ms-between-poll": 30,
    "max-concurrent-indexers": 4,
    "dbpath": "data",
    "title": "Hound",
    "health-check-uri": "/healthz",
}

# Repositories that need to be indexed from organizations
# Add your organization here
organizations = [
    "balena-io",
    "balena-io-library",
    "balenalabs",
    "balena-io-playground",
]

# Fetches all GitHub repo urls from a GitHub org
def fetchThemRepos(org: str, nextPage=None, per_page=100):
    path = f"https://api.github.com/users/{org}/repos"
    kw = {"per_page": per_page}
    if nextPage is not None:
        kw["page"] = nextPage
        nextPage = nextPage + 1
    else:
        nextPage = 1
    query = urllib.parse.urlencode(kw)
    with urllib.request.urlopen("{}?{}".format(path, query)) as resp:
        body = resp.read()
        if isinstance(body, bytes):
            body = body.decode("utf-8")  # type: ignore
        data = json.loads(body)
        if data:
            for repo in data:
                yield repo["name"], repo["html_url"]
            yield from fetchThemRepos(org, nextPage, per_page=per_page)


def main():
    settings = DEFAULT_SETTINGS.copy()
    settings["repos"] = repos = {}

    def addrepos(repositories: Dict[str, Any]) -> None:
        for name, url in repositories:
            repos[name] = {"url": url}

    for org in organizations:
        addrepos(fetchThemRepos(org))

    with open("config.json", "w") as configFile:
        json.dump(settings, configFile, indent=4, sort_keys=True)
        configFile.write("\n")


if __name__ == "__main__":
    main()
