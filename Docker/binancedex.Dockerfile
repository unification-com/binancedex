FROM python:3.7.2-slim-stretch

RUN mkdir /src
RUN mkdir /reports

COPY requirements.txt /src

WORKDIR /src

ENV PYTHONPATH /src

RUN pip install -r requirements.txt

COPY src3/binancedex /src/binancedex
COPY src3/tests /src/tests

RUN echo "/usr/local/bin/python -m binancedex.cli" >> /root/.bash_history && \
    echo "py.test /src/tests" >> /root/.bash_history && \
    echo "alias ll='ls -la'" >> /root/.bashrc
