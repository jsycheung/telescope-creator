FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY . .
ENV POSTGRES_URI="postgresql://postgres:postgres@telescope-database.coap2xbf5pos.us-east-1.rds.amazonaws.com:5432/"
ENV FLASK_APP=app.py
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]