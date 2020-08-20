FROM python:3.8.5-alpine3.12

LABEL maintainers="manofcolombia,crutonjohn"

RUN \
    pip install requests prometheus_client flask && \
    mkdir /app

WORKDIR /app

ADD bytesized_api.py /app

ADD byte/ /app/byte

ADD entrypoint.sh /app

EXPOSE 8888/tcp

ENV API="12345" 

ENTRYPOINT ["sh", "entrypoint.sh"]
