# School Project: Weather Station Integration with Home Assistant

This Python project connects a weather station to [Home Assistant (HA)](https://www.home-assistant.io/) using the MQTT protocol.

## Features
- Publishes sensor data (e.g., temperature, humidity, air quality) via MQTT.
- Pre-configured Docker Compose setup for Home Assistant and MQTT broker.
- Fully customizable using a `.env` configuration file.

## Tools and Resources
- [MQTT Explorer](https://mqtt-explorer.com/) (Optional, for testing and debugging MQTT messages).


## Prerequisites

### 1. Install Required Software

- **Docker**:
  - Ensure Docker and Docker Compose are installed. ([Get Docker](https://docs.docker.com/get-docker/))

- **Python**:
  - Install Python on your system. ([Download Python](https://www.python.org/downloads/))


### 2. Clone the Repository

Clone the repository to your desired location:
  ```bash
  git clone <repository_url>
  cd <repository_name>
  ```


### 3. Configure the Environment

1. Copy `.env.template` to a new `.env` file:
   ```bash
   cp .env.template .env
   ```

2. Open the `.env` file and update the required values:
    - MQTT broker details (IP, port).
    - Debug and logging options.
    - Sensor data file paths.


### 4. Install Python Dependencies

Install the required Python packages:
  ```bash
  pip install -r requirements.txt
  ```


## Quick Start with Docker Compose

### Steps

1. **Start the Docker Services**:

    - From the folder containing docker-compose.yml, run:
      ```bash
      docker compose up -d
      ```

2. **Access Home Assistant**:

    - Open your web browser and go to:
      ```bash
      http://<IP or localhost>:8123
      ```

    - Log in with the following credentials:
      - Username: `admin`
      - Password: `admin`


## Running the Python Script

1. **Start the Python Script**:
    
    - Once the environment is set up, execute the main Python script:
      ```bash
      python main.py
      ```

2. **Behavior**:

    - The script reads sensor data from files, publishes it to the MQTT broker, and repeats at the specified interval.


---

> Notes
- Use MQTT Explorer to monitor MQTT messages and ensure data is being published correctly.

- Ensure the MQTT broker and Home Assistant are running before starting the Python script.

- Adjust settings in the .env file as needed.