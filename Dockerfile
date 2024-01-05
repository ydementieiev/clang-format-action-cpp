# Use a specific version of Ubuntu to ensure consistent behavior
FROM ubuntu:20.04

# Install clang-format
RUN apt-get update && \
    apt-get install -y --no-install-recommends clang-format-11 && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the entrypoint script into the image
COPY entrypoint.sh /entrypoint.sh

# Ensure the script is executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint.sh"]
