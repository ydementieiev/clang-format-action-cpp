# Use a specific version of Ubuntu to ensure consistent behavior
FROM ubuntu:20.04

# Install clang-format and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends clang-format-11 python3 && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the format_validator Python script into the image
COPY format_validator.py /format_validator.py

# Ensure the script is executable
RUN chmod +x /format_validator.py

# Set the format_validator to the Python script
ENTRYPOINT ["python3", "/format_validator.py"]
