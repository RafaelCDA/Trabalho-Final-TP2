FROM python:3.12-slim
WORKDIR /app

COPY ./back/requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./back /app

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
