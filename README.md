# Balena-Hound

> Run your personal hound instance on a Raspberry Pi with auto-indexing repositories 

## What is Hound?

[Hound](https://github.com/hound-search/hound) is an extremely fast source code search engine. The core is based on this article (and code) from Russ Cox: [Regular Expression Matching with a Trigram Index](http://swtch.com/~rsc/regexp/regexp4.html). Hound itself is a static [React](http://facebook.github.io/react/) frontend that talks to a [Go](http://golang.org/) backend. The backend keeps an up-to-date index for each repository and answers searches through a minimal API.

Source code for Hound, backend and frontend code is [here](https://github.com/hound-search/hound) along detailed deployment instructions.

## Created a configuration generator

Auto-indexing repositories manually with a [Python script]((https://eklitzke.org/indexing-git-repos-with-hound)) at the moment. Additionally, one can configure the script to run as a cron job in order to look for new repositories and generate latest configuration for Hound.

## Running Hound on your board

1. Deploy hound on [balenaCloud](https://balena.io)

[![](https://www.balena.io/deploy.png)](https://dashboard.balena-cloud.com/deploy)

2. Add a new device to your newly created fleet, let it index the repos (Takes time) and it will be ready with message in the console. 

```
running server at http://localhost:80
``` 

If you are new to balenaCloud, follow the [getting started](https://www.balena.io/docs/learn/getting-started/raspberrypi3/nodejs/) guide.

![](dashboard.png)

By default, Hound will be running on balena's GitHub orgs as a way for you to play around with the instance and test it out. You can easily change this creating a new [config.json](https://github.com/hound-search/hound#quick-start-guide) file using the example [config-example.json](https://github.com/hound-search/hound/blob/main/config-example.json) file.


### Configuring your hound

1. Edit the following dictionaries in the `confignator.py` file as per your needs. Confignator generates config files for all repositories present in the orgs you specify.

```python
DEFAULT_SETTINGS = {
    "max-concurrent-indexers": 4, 
    "dbpath": "data", 
    "title" : "Hound",
    "health-check-uri" : "/healthz",
}


organizations = [
        "balena-io",
        "balena-io-library",
        "balenalabs",
        "balena-io-playground",
]    
```

2. Run `confignator.py`. Confignator fetches a fresh list of repositories from the GitHub API, hence make sure not to run it repeatedly in order to avoid hitting the rate limit.

```
python3 confignator.py
```

This will create a file called `config.,json` in the root directory. Push a new release to your fleet in order for the hound to run on the latest configuration. Additionally, one can configure the script to run as a cron job in order to look for new repositories and generate latest configuration for Hound.

## If you are new to balenaCloud

[Get started!](https://www.balena.io/docs/learn/getting-started/raspberrypi3/nodejs/)
