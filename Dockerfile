# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup.
CMD panel serve panel_example/main.py --address 0.0.0.0 --port 8080 --allow-websocket-origin="*" --basic-auth credentials.json --cookie-secret rnTUVZbBwexI6AZne3_9pre9xWFfC3s9JWKG3vNbUas=
