# Use the official Python image from the Docker Hub with Python 3.10
FROM python:3.10.14-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies and Chrome
RUN apk update && apk upgrade && \
    apk add --no-cache \
    bash \
    build-base \
    curl \
    chromium \
    chromium-chromedriver \
    py3-pip \
    && rm -rf /var/cache/apk/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_DRIVER=/usr/bin/chromedriver

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set the default command to run the Python script
CMD ["python", "main.py"]
