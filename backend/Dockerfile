# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download required NLTK data
RUN python -m nltk.downloader punkt stopwords wordnet

# Copy the rest of the app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run your Flask app
CMD ["python", "app.py"]
