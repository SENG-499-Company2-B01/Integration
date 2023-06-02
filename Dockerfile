FROM docker:dind

RUN apk update && \
    apk add --no-cache git jq

WORKDIR /app
COPY . /app

RUN chmod +x ./clone.sh ./build.sh ./runfrom.sh ./killall.sh
RUN ./clone.sh
RUN ./build.sh

CMD ./runfrom.sh 2 2 2 2
