# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY script.py .

# Set the entry point for the container to the name of your Python script
ENTRYPOINT ["python", "main.py"]



# to build, run:` docker build -t lbp_scraper_lambda . `

# to run: ` docker run -p 4000:5000 lbp_scraper_lambda `

