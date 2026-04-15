#Base image
FROM --platform=linux/amd64 python:3.11-slim
#Adding a working directtory
WORKDIR /app

COPY hello_world.py .

CMD [ "python", "hello_world.py" ]