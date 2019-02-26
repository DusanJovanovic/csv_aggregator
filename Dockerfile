# Dockerfile-flask

# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
FROM python:3.6.4-slim-jessie

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP

# Expose the port
EXPOSE 5000

# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# We copy the rest of the codebase into the image
COPY . .

# Finally, we run uWSGI with the ini file we
# created earlier
CMD python -u app.py