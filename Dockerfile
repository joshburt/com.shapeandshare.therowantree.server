FROM python:3.9

RUN pip install --upgrade pip

ADD dist/rowantree.server*.whl /tmp/install/
ADD requirements.txt /tmp/install/

RUN pip install -r /tmp/install/requirements.txt
RUN pip install /tmp/install/*.whl

ADD rowantree.config /

ENTRYPOINT ["python", "-m", "rowantree.server.server"]
