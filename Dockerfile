# Use a lightweight Python base image
FROM python:3.10-slim-buster

# Install system dependencies for the application
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application's requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Set the default command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
