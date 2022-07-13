FROM python:3.10

WORKDIR /messenger_project
COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY ./server.py ./
EXPOSE 5000
CMD ["python","server.py"]