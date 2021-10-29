FROM python:3.8
WORKDIR /crud_create
COPY . /crud_create
RUN pip install -r /crud_create/requirements.txt
CMD python manage.py migrate
CMD python manage.py runserver