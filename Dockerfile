FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
SHELL ["/bin/bash", "-c"]
RUN source config.sh
CMD ["flask", "run", "--host", "0.0.0.0"]