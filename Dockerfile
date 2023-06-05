FROM docker:dind

RUN apk update && \
    apk add --no-cache git jq

WORKDIR /app
COPY . /app

RUN chmod +x ./shell/clone.sh ./shell/build.sh ./shell/runfrom.sh ./shell/killall.sh
RUN ./shell/clone.sh
RUN ./shell/build.sh

CMD ./shell/runfrom.sh 2 2 2 2
