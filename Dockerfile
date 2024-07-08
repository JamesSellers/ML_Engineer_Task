# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set the working directory in the container
WORKDIR /model

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock /model/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /model

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask application
CMD ["poetry", "run", "python", "main.py"]