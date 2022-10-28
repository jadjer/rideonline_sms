FROM python

ENV PORT=50051
ENV SMS_API_HOST="http://192.168.1.1"

WORKDIR /app

RUN python -m venv venv

COPY requirements.txt /app/requirements.txt

RUN /app/venv/bin/pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app/main.py
COPY app /app/app
COPY protos /app/protos

EXPOSE $PORT

CMD ["/app/venv/bin/python", "./main.py"]
