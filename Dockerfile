FROM jjanzic/docker-python3-opencv

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src .

EXPOSE 80

CMD ["python3", "-m" , "flask", "--app=morphify_flask", \
    "run", "--host=0.0.0.0", "--port=80", "--debug"]
