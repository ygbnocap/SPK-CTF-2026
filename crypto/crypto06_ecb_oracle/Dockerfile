FROM python:3.11-alpine
WORKDIR /app
COPY app.py requirements.txt flag.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8106
CMD ["python", "app.py"]
