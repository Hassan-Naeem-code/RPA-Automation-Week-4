# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set environment variables for steel automation
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STEEL_AUTOMATION_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs reports data

# Install the package in development mode
RUN pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash automation && \
    chown -R automation:automation /app
USER automation

# Expose port (if running web interface in future)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import steel_automation; print('OK')" || exit 1

# Default command
CMD ["python", "main_steel.py", "--help"]
