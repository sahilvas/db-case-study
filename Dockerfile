# Use an official Python image as the base
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Create logs and output directories
RUN mkdir -p /app/logs /app/output

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the script
CMD ["python", "bin/demo_script_with_async.py"]
