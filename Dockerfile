# syntax=docker/dockerfile:1

FROM python:3.14.7-slim-bookworm

ARG USER=bowler

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Prevents Python from buffering stdout and stderr
    PYTHONUNBUFFERED=1 \
    # Ensure the venv binaries are on the `PATH`
    PATH="/opt/api/.venv/bin:$PATH"

# Build dependencies for psycopg2
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
            build-essential \
            gcc \
            libpq-dev \
            python3-dev \
            && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /opt/api/

# Install locked runtime dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Copy the FastAPI project to the container
COPY app/ ./app/

# Run as a non-root user
RUN useradd --create-home ${USER} && chown -R ${USER} /opt/api
USER ${USER}

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI production server
CMD ["fastapi", "run", "app/main.py"]
