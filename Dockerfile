FROM python

ENV RABBITMQ_SERVER="192.168.1.6"
ENV SMS_API_HOST="http://192.168.1.1"
ENV SMS_API_USER=""
ENV SMS_API_PASS=""

WORKDIR /app

RUN python -m venv venv

COPY requirements.txt /app/requirements.txt

RUN /app/venv/bin/pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app/main.py
COPY app /app/app

EXPOSE 5672/tcp
EXPOSE 15672/tcp

CMD ["/app/venv/bin/python", "./main.py"]
