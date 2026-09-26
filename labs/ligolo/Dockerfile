FROM debian:trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 iproute2 curl openssl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
CMD ["sleep", "600"]
