FROM python:3.13-slim

WORKDIR /home/app

COPY requirements.txt /home/app/
COPY to_do.py /home/app/
COPY to_do_app.py /home/app/
COPY openapi.yaml /home/app/

COPY db.py /home/app/
COPY .env /home/app/

COPY ./supabase /home/app/supabase

#install Python3 and pip
# RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip

# install venv and activate
# RUN apt install python3.13-venv -y && python3 -m venv .venv 

# RUN . .venv/bin/activate && 
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "to_do_app.py"]