FROM python:3.9-slim as base 
FROM base

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y  vim git 

WORKDIR /code

COPY ./requirements0722.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/
RUN python3 superuser.py

EXPOSE 8080

CMD ["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8080"]