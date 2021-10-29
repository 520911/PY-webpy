FROM python:3.8
WORKDIR /products
COPY ./products ./products
EXPOSE 8000
RUN pip install -r ./products/requirements.txt
RUN python3 ./products/manage.py migrate
CMD ["python", "./products/manage.py", "runserver", "0.0.0.0:8000"]