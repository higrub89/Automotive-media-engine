# syntax=docker/dockerfile:1

# ==========================================
# Stage 1: Builder (Compile dependencies)
# ==========================================
FROM manimcommunity/manim:v0.18.0 AS builder

USER root

# Install build dependencies (if any extra are needed, manim image is quite complete)
# We might need gcc or others if packages require compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Install dependencies to user directory for easy copying
COPY requirements.txt .
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# ==========================================
# Stage 2: Runtime (Production Image)
# ==========================================
FROM manimcommunity/manim:v0.18.0 AS runtime

USER root

# Install runtime-only system dependencies
RUN apt-get update && apt-get install -y \
    redis-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local

# Update PATH to include the user install directory
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# create assets/output folders and set permissions
RUN mkdir -p assets output logs temp && \
    chmod -R 777 assets output logs temp

# Expose API port
EXPOSE 8000

# Healthcheck handled by docker-compose, but good to have default CMD
CMD ["uvicorn", "api.router:app", "--host", "0.0.0.0", "--port", "8000"]
