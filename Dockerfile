FROM python

WORKDIR /app

RUN python -m venv venv

COPY requirements.txt /app/requirements.txt

RUN /app/venv/bin/pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app/main.py
COPY app /app/app
COPY .env /app/.env

CMD ["/app/venv/bin/python", "./main.py"]
