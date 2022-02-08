<<<<<<< HEAD
FROM ciscotestautomation/pyats:latest
WORKDIR /app
COPY . .

RUN apt-get update 


RUN pip3 install --upgrade pip
RUN pip3 install -r req.txt



=======
FROM ciscotestautomation:pyats:latest

WORKDIR /app

COPY . .

RUN apt-get update
RUN iperf3 -y
RUN sudo apt-get install openssh-server
RUN sudo systemctl enable ssh
RUN sudo systemctl start ssh
RUN pip3 install --upgrade pip
RUN pip3 install -r req.txt

EXPOSE 22

CMD ["bin", "bash", ]
>>>>>>> 9a5de25b2aec95b1cbc382234e76f52c470442c1
