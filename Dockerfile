from golang:alpine
MAINTAINER vipul@balena.io
EXPOSE 6080

RUN apk add git

RUN go get github.com/hound-search/hound/cmds/... 

COPY . /hound
WORKDIR /hound

CMD ["houndd"]

    # && wget https://github.com/vipulgupta2048/balena-hound/raw/master/confignator.py 
    # && wget https://github.com/vipulgupta2048/balena-hound/raw/master/job
    
# COPY job /etc/cron.d/job

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/job

# Apply cron job
# RUN crontab /etc/cron.d/job
