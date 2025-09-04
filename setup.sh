#!/bin/bash

# Hotel Service Request Classifier - Setup Script

echo "🏨 Setting up Intelligent Hotel Service Request Classifier..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your MISTRAL_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Check if API key is set
if [ -f ".env" ]; then
    source .env
    if [ -z "$MISTRAL_API_KEY" ] || [ "$MISTRAL_API_KEY" = "your_mistral_api_key_here" ]; then
        echo "⚠️  Warning: MISTRAL_API_KEY not set in .env file"
        echo "📝 Please edit .env and add your Mistral AI API key before running the application"
    else
        echo "✅ MISTRAL_API_KEY is configured"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Edit .env file with your Mistral AI API key"
echo "3. Run the application: python main.py"
echo "4. Test the system: python test_classifier.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
