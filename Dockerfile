# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose port 8000 (optional, but good practice)
EXPOSE 8000

# Run the app with uvicorn, binding to 0.0.0.0 so it's accessible outside container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
