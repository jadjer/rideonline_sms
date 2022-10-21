FROM python

ARG RABBITMQ_SERVER
ARG SMS_API_HOST
ARG SMS_API_USER
ARG SMS_API_PASS

WORKDIR /app

RUN python -m venv venv

COPY requirements.txt /app/requirements.txt

RUN /app/venv/bin/pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app/main.py
COPY app /app/app

RUN echo RABBITMQ_SERVER=$RABBITMQ_SERVER >> .env

RUN echo SMS_API_HOST=SMS_API_HOST >> .env
RUN echo SMS_API_USER=SMS_API_USER >> .env
RUN echo SMS_API_PASS=SMS_API_PASS >> .env

CMD ["/app/venv/bin/python", "./main.py"]
