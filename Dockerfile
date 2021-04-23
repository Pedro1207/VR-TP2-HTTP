FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY ./python/ /python/
WORKDIR /python
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
