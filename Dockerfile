# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy entrypoint script into the image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


# Set the entrypoint script to be executed
ENTRYPOINT ["/entrypoint.sh"]


# Install dependencies
COPY requirements.txt /app/
# RUN pip install --upgrade pip && pip install -r requirements.txt
RUN for i in 1 2 3; do pip install --upgrade pip && pip install --default-timeout=100 -r requirements.txt && break || sleep 5; done


# Copy the current directory contents into the container at /app
COPY . /app/

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "agify_project.wsgi:application"]
