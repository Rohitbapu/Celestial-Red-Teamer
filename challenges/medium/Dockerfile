FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
RUN apt-get update && apt-get install -y apache2 curl nmap && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN useradd -m attacker
WORKDIR /var/www/html
COPY flag.txt ./
RUN chown -R attacker:attacker /var/www/html
EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
