FROM docker:dind

RUN apk update && \
    apk add --no-cache git jq python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
COPY . .
RUN pip3 install --no-cache -r requirements.txt

RUN chmod +x ./shell/clone.sh ./shell/build.sh ./shell/runfrom.sh ./shell/killall.sh
RUN ./shell/clone.sh

CMD ./shell/build.sh && ./shell/runfrom.sh 2 2 2 2
