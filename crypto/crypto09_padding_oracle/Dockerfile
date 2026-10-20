FROM python:3.11-alpine
WORKDIR /app
COPY app.py requirements.txt key.bin iv.bin ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8109
CMD ["python", "app.py"]
