FROM python:3

WORKDIR /usr/src/app
COPY candleApi.py .

CMD [ "python", "./candleApi.py" ]