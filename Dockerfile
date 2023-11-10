# Use an official Python runtime as a parent image  // change the python value
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pipenv and use it to install dependencies from requirements.txt
RUN pip install pipenv && \
    pipenv --python 3.8 && \
    pipenv install --deploy --ignore-pipfile && \
    pipenv install -r requirements.txt

# Set environment variable to run the application
ENV FLASK_APP=app.py

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]


#docker build -t my-python-app .
#docker run -p 5000:5000 my-python-app
