FROM lsiobase/alpine.python3

LABEL maintainers="manofcolombia,crutonjohn"

RUN \
    pip install requests prometheus_client flask && \
    chown -R abc:abc \
        /config \
        /app

USER abc

WORKDIR /app

ADD bytesized_api.py /app

ADD byte/ /app/byte

ADD entrypoint.sh /app

EXPOSE 8888/tcp

ENV API="12345" 

ENTRYPOINT ["sh", "entrypoint.sh"]
