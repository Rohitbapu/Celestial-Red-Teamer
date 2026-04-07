FROM ubuntu:22.04
RUN apt-get update && apt-get install -y netcat-openbsd nmap curl python3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash attacker
WORKDIR /home/attacker
COPY flag.txt /home/attacker/flag.txt
COPY start.sh /start.sh
RUN chmod +x /start.sh && chown -R attacker:attacker /home/attacker
USER attacker
EXPOSE 8080
CMD ["/start.sh"]