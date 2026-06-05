# UNO-Q-SPI3-Flask-Bridge

## Overview

This project demonstrates how to use a custom Flask brick in Arduino App Lab on the UNO Q to access the Linux SPI interface and exchange data with the MCU.

---

## Why Flask?

The original SPI3 proof-of-concept used a custom HTTP server.

This version uses Flask, which simplifies the implementation and makes it easier to extend the service with additional REST endpoints.

---

## Architecture

```text
MCU (STM32)
     |
     | SPI3
     |
Linux /dev/spidev0.0
     |
     | spidev
     |
Flask brick
     |
     | HTTP
     |
main.py App Lab application
```

The Flask brick acts as an HTTP gateway between the App Lab Python application and the Linux SPI interface exposed by the UNO Q.

---

## Features

- Custom Flask brick
- Access to /dev/spidev0.0
- SPI transfer between MCU and MPU
- HTTP API between containers
- Docker image rebuild procedure documented

---

## Docker Architecture

App Lab creates two containers:

- spiflask-main-1 : runs main.py
- spiflask-spi3-1 : runs the Flask SPI service

The SPI service container is built from:

uno-q-spi3-flask:latest

---

## Important Discovery

When modifying the Flask brick source code, removing only the container is not sufficient.

Docker recreates the container from the existing image.

The image must also be removed so that App Lab rebuilds it from the updated sources.

---

## Rebuild Procedure

First identify the SPI3 container:

```bash
docker ps -a
```

Then remove the SPI3 container and the custom image:

```bash
docker stop <spi3-container>
docker rm <spi3-container>
docker rmi uno-q-spi3-flask:latest
```

Example used during development:

```bash
docker stop uno-q-spi3-flask-bridge-main-spi3-1
docker rm uno-q-spi3-flask-bridge-main-spi3-1
docker rmi uno-q-spi3-flask:latest
```

Then restart the App Lab application.

---

## Related Project

This project focuses on the Flask-based implementation of the SPI3 App Lab bridge.

For a detailed explanation of the SPI frame format, the MCU firmware and the data exchanged between the MCU and MPU, see:

https://github.com/philippe86220/uno-q-spi3-app-lab-poc

---

## Credits

This work was inspired by:
- The custom Flask brick example shared by @ptillisch
- The SPI3 App Lab proof-of-concept published by @Merlin513
  
The MCU firmware uses the SPIPeripheral library developed by  @facchinm.

The Flask adaptation, Docker image rebuild investigation and project documentation were developed through experimentation and collaborative assistance from OpenAI's ChatGPT.

Additional investigation was performed to understand how App Lab manages Docker images and containers on the UNO Q.
