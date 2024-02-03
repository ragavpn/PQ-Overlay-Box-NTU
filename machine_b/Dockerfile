# machine_b/Dockerfile

FROM python:3.8-slim-buster 

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl

WORKDIR /app
ADD . /app

# Copy the certificates into the container
ADD ../cert /app/cert

CMD ["python", "machine_b.py"]
