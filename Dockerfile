# This is a basic docker image for use in the clinic

FROM jupyter/minimal-notebook:python-3.11

# Swith to root to update and install python dev tools
USER root
RUN apt update
RUN apt install -y python3-pip python3-dev

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1) \
    && CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) \
    && wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip /chromedriver/chromedriver* -d /usr/local/bin/ \
    && rm /chromedriver/chromedriver*

# Create working directory
WORKDIR /project

# Adjust permissions for everything within /project before switching back to $NB_UID
COPY --chown=$NB_UID:$NB_GID src ./src
COPY --chown=$NB_UID:$NB_GID pyproject.toml .
COPY --chown=$NB_UID:$NB_GID requirements.txt .

# Switch back to the non-root user before installing Python packages
USER $NB_UID

# Install Python 3 packages
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]
