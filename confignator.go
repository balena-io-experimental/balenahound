package main

import {
	"fmt"
	"net/url"
}
// import json
// import os
// import urllib.request
// import urllib.parse
// from typing import Dict, Any, TextIO

constant DEFAULT_SETTINGS := map[string]string{
	"max-concurrent-indexers": 4, 
	"dbpath": "data", 
	"title" : "Hound",
	"health-check-uri" : "/healthz",
}

// var usernames = [...]string{"balena-io", "balena-io-library", "balenalabs", "product-os", "people-os", "company-os", "balena-io-playground"}
var usernames = [...]string{"people-os"}

// func dump_file(settings: Dict[str, Any], fileobj: TextIO) -> None:
//     json.dump(settings, fileobj, indent=4, sort_keys=True)
//     fileobj.write("\n")


func get_githubrepos(username string, page=None, per_page=100):
    path := "https://api.github.com/users/{username}/repos"
    kw = map[string]int{"per_page": 100}
    if page is not None:
        kw["page"] = page
        next_page = page + 1
    else:
		next_page = 2
	params := url.Values{}
	params.Add(kw)
	query := params.Encode()	
	with urllib.request.urlopen(path + "?" + query)) as resp:
        body = resp.read()
        if isinstance(body, bytes):
            body = body.decode("utf-8")  # type: ignore
        data = json.loads(body)
        if data:
            for repo in data:
                yield repo["name"], repo["html_url"]
            yield from get_githubrepos(username, next_page, per_page=per_page)


func main() {
	
	settings=make(map[string]string)
	for k,v := range DEFAULT_SETTINGS{
		settings[k] = v
	}
	settings["repos"]= repos = {}

	func addrepos(iterable):
		for name, url in iterable:
			repos[name] = {
				"url": url
			}

	for username in usernames:
		addrepos(get_githubrepos(username))
}
