FROM python:3.8

WORKDIR /usr/src/products

COPY ./products/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate