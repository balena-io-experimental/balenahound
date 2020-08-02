from balenalib/armv7hf-golang:latest-run
MAINTAINER vipul@balena.io

RUN go get github.com/hound-search/hound/cmds/...

install_packages python3 cron

ENTRYPOINT ["python3", "confignator.py"]

EXPOSE 6080

CMD ['hound']
