FROM ciscotestautomation/pyats:latest
WORKDIR /app
COPY . .

RUN apt-get update 


RUN pip3 install --upgrade pip
RUN pip3 install -r req.txt



