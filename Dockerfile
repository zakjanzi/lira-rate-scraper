# Define the base image to use
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app
CMD [ "python", "app.py" ]


# to build, run:` docker build -t lira_scraper . `

# to run: ` docker run -p 4000:5000 lira_scraper `
