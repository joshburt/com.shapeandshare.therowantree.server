FROM python:3.9

WORKDIR /
RUN pip install --upgrade pip

COPY dist/*.whl /tmp/wheels/
RUN pip install /tmp/wheels/*.whl

CMD ["python", "-m", "rowantree.content.service.server"]
