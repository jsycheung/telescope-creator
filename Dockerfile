FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# docker build . --tag telescope-creator
# docker run -it -p 5000:5000 --env-file ./.envvar --name telescope-creator telescope-creator