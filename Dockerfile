# This is a docker image for web scraping and PDF processing
FROM jupyter/minimal-notebook:python-3.11

# Switch to root to update and install dependencies
USER root

# Install system dependencies including poppler-utils for PDF processing
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-dev \
    poppler-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /project

# Adjust permissions for everything within /project
COPY --chown=$NB_UID:$NB_GID src ./src
COPY --chown=$NB_UID:$NB_GID pyproject.toml .
COPY --chown=$NB_UID:$NB_GID requirements.txt .

# Create data directories with proper permissions
RUN mkdir -p /project/data/scraped_pdfs /project/data/images && \
    chown -R $NB_UID:$NB_GID /project/data

# Switch back to the non-root user before installing Python packages
USER $NB_UID

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install beautifulsoup4 pdf2image

# Default command
CMD ["/bin/bash"]
