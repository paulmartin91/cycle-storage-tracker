FROM python:3.11-slim

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