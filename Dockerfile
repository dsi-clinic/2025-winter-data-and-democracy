# Base image for Jupyter and Python
FROM jupyter/minimal-notebook:python-3.11

# Switch to root to install system-level tools
USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-dev \
    poppler-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create working directory for project
WORKDIR /project

# Copy scraping code and Dash app code
COPY --chown=$NB_UID:$NB_GID src ./src
COPY --chown=$NB_UID:$NB_GID pyproject.toml .
COPY --chown=$NB_UID:$NB_GID requirements.txt .
COPY --chown=$NB_UID:$NB_GID app.py .
COPY --chown=$NB_UID:$NB_GID main.py .
COPY --chown=$NB_UID:$NB_GID pages ./pages
COPY --chown=$NB_UID:$NB_GID output ./output

# Create necessary data directories
RUN mkdir -p /project/data/scraped_pdfs /project/data/images && \
    chown -R $NB_UID:$NB_GID /project/data

# Switch back to non-root user
USER $NB_UID

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install beautifulsoup4 pdf2image dash dash-bootstrap-components gunicorn

# Expose the port used by Dash
EXPOSE 8050

# Default command: serve the Dash app (change if running Jupyter instead)
CMD ["python", "app.py"]
