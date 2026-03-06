#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_ZIP="$SCRIPT_DIR/src/lambda/shared_layer.zip"
SRC_DIR="$SCRIPT_DIR/src"

echo "🔨 Building shared Lambda layer with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker not running. Using existing layer if available..."
    if [ -f "$OUTPUT_ZIP" ]; then
        echo "✅ Using existing layer: $OUTPUT_ZIP"
        exit 0
    else
        echo "❌ Error: No existing layer found and Docker is not running."
        echo "   Please start Docker Desktop or use pre-built layer from Git."
        exit 1
    fi
fi

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

mkdir -p $TEMP_DIR/python

# Copy shared modules
echo "📦 Copying shared modules..."
cp -r $SRC_DIR/infrastructure $TEMP_DIR/python/
cp -r $SRC_DIR/application $TEMP_DIR/python/
cp -r $SRC_DIR/domain $TEMP_DIR/python/

# Install pip dependencies with Docker (Linux binaries)
echo "🐍 Installing Python dependencies (Linux binaries)..."
docker run --rm \
    -v "$TEMP_DIR":/var/task \
    --entrypoint pip \
    public.ecr.aws/lambda/python:3.11 \
    install PyJWT requests google-auth google-auth-oauthlib boto3 -t /var/task/python/ --upgrade --quiet

# Create zip
echo "📦 Creating zip..."
mkdir -p "$(dirname "$OUTPUT_ZIP")"
cd $TEMP_DIR
zip -r $OUTPUT_ZIP python -q

echo "✅ Layer built successfully: $OUTPUT_ZIP"
ls -lh $OUTPUT_ZIP
