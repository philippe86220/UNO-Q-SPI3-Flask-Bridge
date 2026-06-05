FROM debian:bookworm-slim

RUN apt update && \
    apt install -y python3 python3-spidev python3-flask && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /spi3

COPY . /spi3

CMD ["python3", "/spi3/spi_service.py"]Switch the .txt extension to something like .py or .ino to see syntax highlighting.
