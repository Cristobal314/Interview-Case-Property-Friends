FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md .env ./
COPY src ./src
COPY config ./config

# Install the package and dependencies
RUN pip install --upgrade pip && \
    pip install -e .

# Create artifacts directory
RUN mkdir -p artifacts

ENTRYPOINT ["property-friends"]
CMD ["--help"]