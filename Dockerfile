FROM ubi8/s2i-base:rhel8.3
WORKDIR /app 
COPY .
CMD ["test.py"]
ENTRYPOINT ["python3"]

