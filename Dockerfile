FROM ubuntu:20.04

WORKDIR /tmp/Banking
COPY WebApp .

RUN apt-get update  -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install    -r dependencies/requirements.txt 

ENV DEBUG=True
EXPOSE 5000

CMD [ "bash", "-c", "cd /tmp/Banking && ./start.sh" ]

