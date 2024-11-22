# Use a specific version of Python for consistency
FROM python:3.9.12-slim  

# Set the working directory
WORKDIR /app  

# Copy the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of your application code
COPY . .  

# Expose the port the app runs on
EXPOSE 5001  

# Command to run the application
CMD ["python", "app.py"]

