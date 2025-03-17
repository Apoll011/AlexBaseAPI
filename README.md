# Alex Base API

## Overview
The Alex Base API is a high-performance server designed to handle resource-intensive operations for the Alex Home Assistant system. This server functions as the computational backbone for Alex, processing complex requests that would otherwise strain the main system resources.

## Features
- **Distributed Processing**: Offloads heavy computational tasks from the main Alex Home Assistant
- **Containerized Architecture**: Runs in a Docker container for easy deployment and scaling
- **Version Control Integration**: Maintains synchronization with the Alex Home Assistant through the version controller
- **RESTful API**: Provides standardized endpoints for all Alex services
- **Low Latency**: Optimized for quick response times even for complex operations
- **Resource Management**: Efficiently handles CPU and memory-intensive tasks

## Requirements
- Docker Engine (v20.10.0 or later recommended)
- 500MB RAM minimum (1GB recommended)
- 2GB available disk space
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
npm install
# or
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env file with your configuration
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
- Start the Alex Base API server

### API Endpoints
The server exposes the following endpoints:

- `GET /alex/alive` - Check server status

## Integration with Alex
To integrate with the Alex Home Assistant:

1. Add the server URL to your Alex configuration: on the .alex_config file ()

2. Restart your Alex Home Assistant instance

### Logs
Logs are available in the Docker container:
```bash
docker logs alex-server
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
- GitHub: [@Apoll011](https://github.com/Apoll011)
- Related Project: [Alex Home Assistant](https://github.com/Apoll011/Alex)