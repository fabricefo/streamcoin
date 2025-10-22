FROM tiangolo/uvicorn-gunicorn:python3.9

ARG DB_PASSWORD
ENV DB_PASSWORD=$DB_PASSWORD

RUN mkdir /fastapi_app

COPY requirements.txt /fastapi_app

WORKDIR /fastapi_app

RUN pip install -r requirements.txt

COPY . /fastapi_app



EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]