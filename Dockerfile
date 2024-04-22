# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy the current directory contents into the container at /app
COPY . /app

# Install only runtime dependencies using poetry
RUN poetry config virtualenvs.create false \
                                     && poetry install --no-dev --no-interaction

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable to run the app in production
ENV PYTHONBUFFERED 1

# Run the app. CMD can be overridden when using docker run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
