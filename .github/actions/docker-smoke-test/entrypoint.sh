#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="smoke-test-${GITHUB_RUN_ID:-local}-${RANDOM}"

echo "== Docker smoke test =="
echo "Image:    ${IMAGE}"
echo "Port:     ${PORT}"
echo "Endpoint: ${PATHNAME}"
echo "Timeout:  ${TIMEOUT_SECONDS}s"
echo

cleanup() {
  echo "Cleaning up container: ${CONTAINER_NAME}"
  docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Pulling image (if needed)..."
docker pull "${IMAGE}"

echo "Starting container..."
docker run -d --name "${CONTAINER_NAME}" -p "${PORT}:8000" "${IMAGE}" >/dev/null

echo "Waiting for app to become healthy..."
deadline=$((SECONDS + TIMEOUT_SECONDS))

until curl -fsS "http://localhost:${PORT}${PATHNAME}" >/dev/null 2>&1; do
  if (( SECONDS >= deadline )); then
    echo "ERROR: App did not become healthy within ${TIMEOUT_SECONDS}s"
    echo "Container logs:"
    docker logs "${CONTAINER_NAME}" || true
    exit 1
  fi
  sleep 1
done

echo "OK: Health check passed."
curl -fsS "http://localhost:${PORT}${PATHNAME}" || true

