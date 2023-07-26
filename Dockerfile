FROM docker:dind

RUN apk update && \
    apk add --no-cache git jq

RUN mkdir -p /root/.ssh/
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
COPY ./ssh /root/.ssh
RUN chmod 600 /root/.ssh/*

WORKDIR /app
COPY . .

RUN chmod +x ./shell/clone.sh ./shell/build.sh ./shell/runfrom.sh ./shell/killall.sh
RUN ./shell/clone.sh

CMD ./shell/build.sh && ./shell/runfrom.sh 2 2 2 2
