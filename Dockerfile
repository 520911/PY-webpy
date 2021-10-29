FROM python:3.8.12
WORKDIR /crud_create
COPY . /crud_create
RUN pip install -r /crud_create/requirements.txt
EXPOSE 8000
CMD ["gunicorn", "stocks_products.wsgi", "0.0.0.0:8000"]