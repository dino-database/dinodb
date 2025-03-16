# DinoDB

![Docker Pulls](https://img.shields.io/docker/pulls/dinodb/dinodb?label=Downloads&logo=docker)
![Docker Image Size](https://img.shields.io/docker/image-size/dinodb/dinodb/latest?label=Image%20Size)
![Docker Version](https://img.shields.io/docker/v/dinodb/dinodb?label=Latest%20Version)
![Security Scan](https://img.shields.io/badge/Security%20Scan-Passing-green)

DinoDB is a high-performance, lightweight, **Privacy-Focused** database designed to store and retrieve data efficiently. This project aims to provide a fast and reliable solution for handling database operations in a simple and scalable way.

## Features

- Efficient key-value storage.
- Designed for fast insertions, lookups, and deletions.
- Minimalistic API for integration.

## Installation

To install DinoDB, simply clone the repository and install the necessary dependencies.

## Using DinoDB with Docker

You can pull the latest version of DinoDB (v1.1.1) from Docker Hub using the following command:

```bash
docker pull dinodb/dinodb:1.1.1
```

### Prerequisites

- Python 3.7+
- Docker (optional, for containerized version)

### Steps to Install

1. Clone the repository:

   ```bash
   git clone https://github.com/dino-database/dinodb.git
   cd dinodb
   ```

2. Set up the Python environment and install dependencies:

   Using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   Or use Docker (**suggested**):

   ```bash
   docker pull dinodb/dinodb
   ```

## Usage

### Running the Application

To run DinoDB, use the following command:

```bash
python main.py
```

Or if you're using Docker:

```bash
docker run -p {your port}:8000 dinodb
```

This will start the API at `http://127.0.0.1:{your port}`.

### API Endpoints

The following endpoints are available:

- `POST /insert`: Insert a new record into the database.
- `GET /search/{key}`: Search for a record by key.
- `DELETE /delete/{key}`: Delete a record by key.

### Example

**Insert a Record:**

```bash
curl -X 'POST' 'http://127.0.0.1:8000/insert' -H 'Content-Type: application/json' -d '{"key": "my_key", "value": "my_value"}'
```

**Search for a Record:**

```bash
curl -X 'GET' 'http://127.0.0.1:8000/search/my_key'
```

**Delete a Record:**

```bash
curl -X 'DELETE' 'http://127.0.0.1:8000/delete/my_key'
```

## Development

To contribute to DinoDB, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the SSPL License - see the [LICENSE](LICENSE) file for details.
