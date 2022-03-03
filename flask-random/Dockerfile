FROM python:3.7.3-slim
COPY requirements.txt /
RUN pip3 install --upgrade pip && pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]