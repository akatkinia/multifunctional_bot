FROM python:3.9-alpine as build
COPY requirements.txt .
RUN apk update && apk add --no-cache build-base && pip install -r requirements.txt

FROM build
WORKDIR /app
COPY . .
EXPOSE 8443
CMD ["python", "bot.py"]
