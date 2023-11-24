FROM python:3.11-slim
WORKDIR /app
COPY src/ .
RUN pip install -r requirements.txt
EXPOSE 8443
CMD ["python", "bot.py"]
