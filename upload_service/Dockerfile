FROM alpine

RUN apk add --update \
        python3 \
        py-pip \
    && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install flask --no-cache-dir && \
    pip3 install gunicorn --no-cache-dir

WORKDIR /service

COPY . /service
RUN pip3 install -r ./requirements.txt

CMD ["gunicorn","--bind","0.0.0.0:8080","service:app"]