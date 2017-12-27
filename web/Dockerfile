FROM alpine

# Initialize
RUN mkdir -p /data/web
WORKDIR /data/web


# Setup
RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev postgresql-client postgresql-dev build-base gettext
RUN apk add --update zlib
RUN apk add --update build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip3 install --upgrade pip
COPY requirements.txt /data/web/
RUN pip3 install -r requirements.txt

# Clean
RUN apk del -r python3-dev postgresql

# Prepare
COPY . /data/web/
RUN mkdir -p mydjango/static/admin
