FROM python

ENV KAFKA_HOST="127.0.0.1"

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
COPY ./main.py /app/main.py

RUN useradd -ms /bin/bash user_app
USER user_app

EXPOSE 9092

CMD ["python", "main.py"]
