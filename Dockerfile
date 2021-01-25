FROM python:3.8-ubi7
WORKDIR /app 
COPY . .
CMD ["test.py"]
ENTRYPOINT ["python3"]

