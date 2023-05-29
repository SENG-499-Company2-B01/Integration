FROM alpine:3.18.0

RUN apk update && \
    apk add --no-cache git docker

WORKDIR /app

COPY . .