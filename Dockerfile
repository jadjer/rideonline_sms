FROM python

ARG VERSION

ENV VERSION=${VERSION}
ENV HILINK="http://192.168.1.1"

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY app /app/app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
