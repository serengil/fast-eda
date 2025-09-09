FROM python:3.8.12

# logs are coming with some delays to aws
ENV PYTHONUNBUFFERED=1

# create required folder
RUN mkdir -p /app && chown -R 1001:0 /app

# switch to application directory
WORKDIR /app

# install os level dependencies
RUN apt-get update

# install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org \
    --trusted-host=files.pythonhosted.org -r /app/requirements.txt

# otherwise it cannot find gunicorn command
ENV PATH="/home/python/.local/bin:$PATH"

# Install application into container
COPY ./src /app/src

WORKDIR /app/src

# run the service
EXPOSE 5000
CMD ["uvicorn", "app:service", "--host", "0.0.0.0", "--port", "5000", "--workers", "2"]