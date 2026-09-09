FROM python:3.11-slim

WORKDIR /app

# Prevent Python from creating .pyc files
# and keep logs immediately visible.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first.
# This improves Docker layer caching.
COPY pyproject.toml uv.lock README.md ./

# Install dependencies into the system environment.
RUN uv sync --frozen --no-dev

# Copy application source.
COPY src ./src

# Create data directory.
RUN mkdir -p /app/data

# Start the LangGraph agent.
CMD ["uv", "run", "python", "-m", "src.main"]