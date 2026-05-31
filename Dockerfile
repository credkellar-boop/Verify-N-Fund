# Step 1: Use an official lightweight Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set system environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Install system dependencies required for image processing (Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy the dependencies file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the application code into the container
COPY . .

# Step 7: Expose the network port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Step 8: Define the command to run the application when the container starts
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
