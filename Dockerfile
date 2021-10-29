FROM python:3.8
WORKDIR /crud_create
COPY . /crud_create
RUN pip install -r /crud_create/requirements.txt
CMD python manage.py migrate
CMD gunicorn --bind 0.0.0.0:8000 stocks_products.wsgi