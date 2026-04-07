FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y vsftpd netcat-openbsd nmap curl python3 && rm -rf /var/lib/apt/lists/*
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && dpkg-reconfigure --frontend noninteractive tzdata
RUN useradd -m attacker && echo "attacker:weakpass" | chpasswd
COPY flag.txt /root/flag.txt
COPY vsftpd.conf /etc/vsftpd.conf
RUN chmod 600 /root/flag.txt
EXPOSE 21
CMD ["vsftpd", "/etc/vsftpd.conf"]
