FROM python:3.10-slim

WORKDIR /app
COPY detect.py .

RUN pip install pandas scikit-learn

CMD ["python", "detect.py"]

