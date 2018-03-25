FROM python:2.7

WORKDIR /app

COPY ./app /app

RUN pip install -r requirements.txt \
    && useradd -M -U -u 1000 trt_server_srv \
    && chown -R trt_server_srv /app

ENTRYPOINT ["python", "./server.py"]
