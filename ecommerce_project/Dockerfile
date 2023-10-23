FROM python:3.10-slim-buster as base

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man7 &&\
    apt-get update &&\
    apt-get install --yes --no-install-recommends \
    libpq-dev \
    gcc \
    file \
    make \
    musl-dev \
    libc-dev &&\
    rm -rf /var/lib/apt/* &&\
    apt-get clean

ADD ./requirements.txt /tmp

RUN pip3 install --no-cache-dir --upgrade pip &&\
    pip3 install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 8000

RUN mkdir /code
COPY . /code
WORKDIR /code