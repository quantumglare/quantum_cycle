FROM python:3.9.1-slim-buster

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/quantumglare"

RUN apt-get update

RUN apt-get install --no-install-recommends -y \
    make

COPY requirements.txt requirements.txt

RUN pip install --disable-pip-version-check --no-cache-dir -U ipython ipdb && \
    pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

WORKDIR /usr/src/quantumglare/
