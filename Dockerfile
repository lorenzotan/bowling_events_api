FROM python:3.13.3-slim-bookworm

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
            # curl to download uv
            curl \
            && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN chmod -R 755 /uv-installer.sh && /uv-installer.sh && rm /uv-installer.sh
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
# Ensure the installed binary is on the `PATH`
ENV PATH="/opt/api/.venv/bin:/root/.local/bin/:$PATH"

# Create the app directory
RUN mkdir -p /opt/api/app
 
# Set the working directory inside the container
WORKDIR /opt/api/

# install packages
COPY ./pyproject.toml /opt/api/
RUN uv venv .venv && \
    uv sync
# uv sync --no-dev
 
# Copy the FastAPI project to the container
COPY ./app/* /opt/api/app
 
# Expose the FastAPI port
EXPOSE 8000
 
# Run FastAPI development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
