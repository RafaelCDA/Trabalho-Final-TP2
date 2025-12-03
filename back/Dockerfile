FROM python:3.12-slim

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y sqlite3 libsqlite3-dev && apt-get clean

WORKDIR /app

RUN mkdir ./data && sqlite3 ./data/database.db

COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
