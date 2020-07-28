FROM lsiobase/alpine.python3

LABEL maintainers="manofcolombia,crutonjohn"

RUN \
    pip install requests prometheus_client && \
    chown -R abc:abc \
        /config \
        /app

USER abc

WORKDIR /app

ADD bytesized-api.py /app

ADD entrypoint.sh /app

EXPOSE 8888/tcp

ENV API="12345" \
    INTERVAL="600"

ENTRYPOINT ["sh", "entrypoint.sh"]
