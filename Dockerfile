FROM alpine:3.18.0

RUN apk update && \
    apk add --no-cache git docker jq docker-cli docker-compose

WORKDIR /app

COPY . /app
RUN chmod +x ./clone.sh ./build.sh
RUN ./clone.sh
CMD ./build.sh
