FROM python:3.8.9-buster

ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt

WORKDIR /
RUN git clone https://github.com/facebookresearch/fastText.git && \
    cd fastText && \
    pip install . && \
    rm -rf /fastText
