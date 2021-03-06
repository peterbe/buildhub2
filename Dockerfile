FROM python:3.6-slim@sha256:6f39e7dfc5158b351cfea004541fc85898452c2e4cbeb2b36f00c286fc957a88

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/

# add a non-privileged user for installing and running the application
# don't use --create-home option to prevent populating with skeleton files
RUN mkdir /app && \
    chown 10001:10001 /app && \
    groupadd --gid 10001 app && \
    useradd --no-create-home --uid 10001 --gid 10001 --home-dir /app app

# install a few essentials and clean apt caches afterwards
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-transport-https build-essential curl git

# Clean up apt
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /app

# Install Python dependencies
COPY requirements.txt /tmp/
WORKDIR /tmp
RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app

# Switch back to home directory
WORKDIR /app

RUN chown -R 10001:10001 /app

USER 10001

# CMD ["/bin/bash", "/app/bin/run.sh", "web"]

ENTRYPOINT ["/bin/bash", "/app/bin/run.sh"]
CMD ["web"]
