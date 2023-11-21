FROM fedora

ARG VERSION="v0.0.0"
ARG BUILD_DATE
ARG GITHUB_SHA

ENV VERSION=$VERSION
ENV BUILD_DATE=$BUILD_DATE
ENV GITHUB_SHA=$GITHUB_SHA
ENV HILINK="http://192.168.1.1"
ENV APP_PATH=/app

RUN dnf update -y
RUN dnf upgrade -y
RUN dnf install -y python python-pip

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

COPY app $APP_PATH/app
COPY run.py $APP_PATH
COPY requirements.txt $APP_PATH

RUN pip install --upgrade pip
RUN pip install -r $APP_PATH/requirements.txt

EXPOSE 8000
ENTRYPOINT python run.py
