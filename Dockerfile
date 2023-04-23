FROM jjanzic/docker-python3-opencv

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src .

CMD ["python3", "-m" , "flask", "--app=morphify_service", \
    "run", "--host=0.0.0.0", "--port=5050", "--debug"]