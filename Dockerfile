# multi-stage build
#
# We build dependencies (wheels) in a builder stage and copy them to a separate runtime stage 
# so the final image contains only what is needed to run the application, 
# without build artifacts or unnecessary tools.

# Stage 1: Builder
FROM python:3.12 AS builder
WORKDIR /build

# Copy dependency list into the image
COPY requirements.txt .

# Build Python dependencies into wheel packages
# Wheels are precompiled artifacts that can be reused in the runtime stage
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy prebuilt dependency wheels from the builder stage
COPY --from=builder /wheels /wheels

# Install dependencies from wheels and remove temporary files
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY app ./app

# Start the FastAPI application using Uvicorn server
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
