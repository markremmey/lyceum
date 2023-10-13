# Use an official Python runtime as a base image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pwd

# Make port 80 available to the world outside this container
EXPOSE 80 443

WORKDIR /app/backend

# Run gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:80", "wsgi:app"]