# Alex Base API

## Overview
Alex Base API is a high-performance server designed to handle resource-intensive natural language processing operations for the Alex Home Assistant system. This server functions as the computational backbone for Alex, processing complex language understanding requests using the Snips NLU engine.

## Features
- **Natural Language Understanding**: Powered by Snips NLU for intent recognition in multiple languages
- **Dictionary Services**: Word definition lookup with fuzzy matching capabilities
- **User Management**: API endpoints for user creation, search, and management
- **Multi-language Support**: Currently supports English and Portuguese
- **Containerized Architecture**: Runs in a Docker container for easy deployment
- **FastAPI Backend**: Modern, high-performance web framework for Python
- **Low Latency**: Optimized for quick response times even for complex NLP operations

## Requirements
- Docker Engine (v19.03.0 or later recommended)
- 2GB RAM minimum (4GB recommended for training models)
- Network access to Alex Home Assistant instance

## Installation

### Using Docker (Recommended)
Build the Docker image:
```bash
docker build -t alex-server .
```

### Manual Installation
1. Clone the repository
```bash
git clone https://github.com/Apoll011/Alex-Base-API.git
cd Alex-Base-API
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Download language models
```bash
python -m snips_nlu download-language-entities pt_pt
python -m snips_nlu download-language-entities en
```

## Usage

### Docker Deployment
Run the server with the following command:
```bash
docker run -p 1178:1178 -v ./features/version_controller:/app/features/version_controller alex-server
```

This will:
- Map port 1178 on your host to port 1178 in the container
- Mount the local version_controller directory to the container for persistent storage
- Start the Alex Base API server with uvicorn

### Configuration
The server configuration is stored in `config.py`:
- Current version: 2.1.0
- Default host: 0.0.0.0
- Default port: 1178

## NLP Components

### Intent Recognition
The IntentKit class provides:
- Intent recognition for user queries
- Support for English and Portuguese
- Training capabilities for custom intent recognition models
- Persistent model storage

### Dictionary Services
The DictionaryKit class provides:
- Word definition lookup
- Fuzzy matching for misspelled words
- Confidence scoring for approximate matches

### User Management
The UserKit class provides:
- User creation, update, and deletion
- User search by name
- Tag-based user filtering with complex conditions

## Project Structure
```
├── features/
│   ├── dictionary/             # Dictionary data files
│   │   └── language/           # Language-specific dictionaries
│   ├── intent_recognition/     # Intent recognition models
│   │   └── snips/              # Snips NLU models and datasets
│   └── version_controller/     # Versioning information
├── main.py                     # FastAPI application
├── kit.py                      # Core NLP components
├── config.py                   # Server configuration
├── Dockerfile                  # Docker configuration
└── requirements.txt            # Python dependencies
```

## API Endpoints
The server exposes FastAPI endpoints for:
- Intent recognition
- Dictionary lookups
- User management
- System status and version information

## Timezone
The server operates in Atlantic/Cape_Verde timezone (UTC-1).

## Docker Image
- Based on Python 3.8-slim
- Custom patched version of snips_nlu utils
- Pre-loaded with language models for English and Portuguese

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
- GitHub: [@Apoll011](https://github.com/Apoll011)
- Related Project: [Alex Home Assistant](https://github.com/Apoll011/Alex)