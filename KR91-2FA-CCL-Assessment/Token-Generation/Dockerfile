# Use a specific version of Python for consistency
FROM python:3.9.12-slim  

# Set the working directory
WORKDIR /app  

# Copy the requirements file first for better caching
COPY requirements.txt .  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of your application code
COPY . .  

# Expose the port the app runs on
EXPOSE 5000  
# Set environment variables (optional, can also be set at runtime)
# ENV SECRET_KEY=your_secret_key

# Command to run the application
CMD ["python", "app.py"]
