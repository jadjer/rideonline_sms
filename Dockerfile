FROM python

ARG VERSION
ARG BUILD_DATE
ARG GITHUB_SHA

ENV VERSION=$VERSION
ENV BUILD_DATE=$BUILD_DATE
ENV GITHUB_SHA=$GITHUB_SHA

ENV HILINK="http://192.168.1.1"

ENV BASE_PATH="/app"
ENV APP_PATH="$BASE_PATH/app"

RUN pip install --upgrade pip

RUN mkdir -p $BASE_PATH
WORKDIR $BASE_PATH

RUN mkdir -p $APP_PATH
COPY requirements.txt $BASE_PATH
RUN pip install -r $BASE_PATH/requirements.txt
COPY app $APP_PATH

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
