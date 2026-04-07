FROM python:3.11-slim

# 1. Set the working directory inside the container
WORKDIR /app

# 2. Copy requirements from the CURRENT folder (pythonProject/qaGenie)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy everything from the CURRENT folder into /app
# This includes main.py, index.html, and the static folder
COPY . .

# 4. Start the app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]