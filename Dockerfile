# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app

COPY data_analysis.py .
COPY All_Diets.csv .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --prefer-binary pandas matplotlib seaborn

CMD ["python", "data_analysis.py"]
