FROM python:3.11.3

WORKDIR /app

COPY . .

RUN pip install -e .

COPY .env .env

EXPOSE 8080

CMD ["light-data-api"]
# or "CMD ['python', '-m', 'src']"
