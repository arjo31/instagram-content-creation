# Use the official Python image from the Docker Hub
FROM python:3.11.4-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install the Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the source code into the container
COPY . /app

# Expose the ports for Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8000

# Command to run both FastAPI and Streamlit
CMD ["sh", "-c", "python3 src/server/fast_server.py & streamlit run app.py"]