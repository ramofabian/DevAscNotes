#Base image
FROM --platform=linux/amd64 python:3.11-slim
#Adding a working directtory
WORKDIR /app
#Installing pre-requisites
#Disclamer: We can use ADD instead of COPY but it is not recommended as it can cause issues with caching and file permissions.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#Coping the API script
COPY mySmallApi/ .
#Exposing the port 8000
EXPOSE 8000
#Running reverse proxy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 