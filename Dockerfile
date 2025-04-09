FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir -p /app/backend /app/data
WORKDIR /app/backend


# Install dependencies
COPY requirements.txt /app/backend/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/backend
