FROM debian:latest

LABEL maintainer=<joppich@bricknet.de>

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -yq && \
    apt-get install -yq --no-install-recommends \
        python3 python3-pip python3-setuptools && \
    rm -r /var/lib/apt/lists /var/cache/apt/*

ENV LANG C.UTF-8  
ENV LC_ALL C.UTF-8

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN useradd -md /srv/website runner -u 1000 && \
    chown -R runner:runner /srv/website

WORKDIR /srv/website
USER runner

RUN mkdir rsvp
COPY docker-entrypoint.sh .
COPY app/ app
EXPOSE 5000

ENTRYPOINT ["/srv/website/docker-entrypoint.sh"]

CMD ["production"]
