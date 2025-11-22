# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some PyTorch/NetworkX ops)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to cache dependencies)
COPY requirements.txt .

# Install Python dependencies
# We use the --no-cache-dir flag to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Render uses
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
