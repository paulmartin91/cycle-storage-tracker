FROM python:3.11-slim

# Install Playwright system dependencies
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy pyproject.toml and uv.lock (if exists)
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies with uv
RUN uv sync --frozen

# Install Playwright browsers
RUN uv run python -m playwright install --with-deps --only-shell chromium

# Copy application files
COPY bike_notifications/ ./bike_notifications/

# Create logs directory
RUN mkdir -p logs

# Run the script using uv
CMD ["uv", "run", "python", "-m", "bike_notifications.main"]