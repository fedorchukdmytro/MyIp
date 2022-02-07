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
