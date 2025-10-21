#!/bin/bash

# DefTech AI Document Assistant - Setup with Virtual Environment

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

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv

    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi

    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

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
    echo "Your API key is already in .env.example, so .env should be ready!"
    echo ""
fi

# Initialize system
echo ""
echo "Initializing Cohere client and Qdrant database..."
python init_demo.py

if [ $? -ne 0 ]; then
    echo "❌ Initialization failed"
    echo "Please check that COHERE_API_KEY is set correctly in .env"
    exit 1
fi

echo "✓ System initialized"
echo ""

# Create sample documents
echo "Creating sample defense documents..."
python create_sample_docs.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to create sample documents"
    exit 1
fi

echo "✓ Sample documents created"
echo ""

# Ingest documents
echo "Ingesting documents into vector database..."
python ingest_documents.py

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
echo "✓ Virtual environment created at: ./venv/"
echo "✓ Dependencies installed"
echo "✓ Sample documents created"
echo "✓ Vector database populated"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "To start the demo (with venv activated):"
echo "  python demo_queries.py"
echo ""
echo "Or run directly:"
echo "  ./run_demo.sh"
echo ""
