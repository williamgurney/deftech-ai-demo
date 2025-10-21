#!/bin/bash

# DefTech AI Document Assistant - Quick Setup Script

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║           DefTech AI Document Assistant - Setup                     ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your COHERE_API_KEY"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Initialize system
echo ""
echo "Initializing Cohere client and Qdrant database..."
python3 init_demo.py

if [ $? -ne 0 ]; then
    echo "❌ Initialization failed"
    echo "Please check that COHERE_API_KEY is set correctly in .env"
    exit 1
fi

echo "✓ System initialized"
echo ""

# Create sample documents
echo "Creating sample defense documents..."
python3 create_sample_docs.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to create sample documents"
    exit 1
fi

echo "✓ Sample documents created"
echo ""

# Ingest documents
echo "Ingesting documents into vector database..."
python3 ingest_documents.py

if [ $? -ne 0 ]; then
    echo "❌ Document ingestion failed"
    exit 1
fi

echo "✓ Documents ingested"
echo ""

# Setup complete
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║                    Setup Complete! ✓                                 ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Ready to run the demo!"
echo ""
echo "To start the demo, run:"
echo "  python3 demo_queries.py"
echo ""
