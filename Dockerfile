FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY product.csv .
EXPOSE 8000
# Run the app
CMD ["python", "app.py"]