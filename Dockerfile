FROM python:3.8.5-alpine3.12

LABEL maintainers="manofcolombia,crutonjohn"

RUN mkdir /app

WORKDIR /app

ADD bytesized_api.py /app

ADD requirements.txt /app

ADD entrypoint.sh /app

RUN pip install -r requirements.txt

EXPOSE 8888/tcp

ENV API="12345"

ENV URL="https://bytesized-hosting.com/api/v1/accounts.json"

ENTRYPOINT ["sh", "entrypoint.sh"]