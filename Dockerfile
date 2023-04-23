FROM jjanzic/docker-python3-opencv

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src .

CMD ["python3", "-m" , "flask", "--app=morphify_service", \
    "run", "--host=0.0.0.0", "--port=5050", "--debug"]

#CMD ["python3", "morphify_cli.py", \
#    "--input-dir=./data/input/input_photos/", \
#    "--stranger-dir=./data/input/stranger_photos/", \
#    "--output-dir=./data/output/"]