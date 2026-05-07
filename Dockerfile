FROM ghcr.io/infrasonar/python:3.14.3
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
ENV MAX_CHECK_TIMEOUT=900
CMD ["python", "main.py"]
