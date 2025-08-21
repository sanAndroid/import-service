# Wine Vectorizer & Data Ingestion Service (Draft)

## Overview

This project provides a **vectorization pipeline** and a **Java ingestion service** for structured wine data.

- **Vectorizer (Python, gRPC server)**

  - Uses [SentenceTransformers](https://www.sbert.net) (`all-MiniLM-L6-v2`) to generate 384-dimensional embeddings.
  - Accepts text fields such as _winery_, and later also _wine name_, _vintage_, etc.
  - Serves embeddings over gRPC via the `VectorizeService`.

- **Ingestion Service (Java, gRPC client + PostgreSQL)**
  - Consumes data from scrapers (planned: multiple sources).
  - Normalizes it into a **uniform schema**.
  - Stores the records in **PostgreSQL** with an embedding vector column for semantic search and similarity queries.

## Architecture

[ Scrapers ] → [ Java Service ] → [ PostgreSQL (+embedding) ]
| |
| v
| [ Python Vectorizer (gRPC) ]

- **Java Service**: orchestrates data flow, calls vectorizer, persists data.
- **Python Vectorizer**: exposes `GetEmbeddingVector` RPC returning embedding arrays.
- **PostgreSQL**: holds structured wine records with embeddings for semantic queries (e.g. pgvector extension).

## Components

### 1. Proto Definition

Shared `.proto` file defines the gRPC interface:

- `VectorizeRequest` (fields: `name`, `address`, `region`, `country`)
- `VectorizeResponse` (fields: `embedding[]`, `dim`)

### 2. Python Vectorizer

- Implements `VectorizeService` server.
- Loads transformer model once and reuses it.
- Returns 384-dim embeddings as `float[]`.

### 3. Java Ingestion Service

- Implements gRPC client (`VectorizeServiceGrpc`).
- Fetches/sanitizes scraper data.
- Calls vectorizer to get embeddings.
- Persists results in PostgreSQL, prepared for later semantic search.

## Requirements

- **Python 3.10+**
  - `grpcio`, `grpcio-tools`, `sentence-transformers`, `torch`
- **Java 21+**
  - gRPC libs (`grpc-netty-shaded`, `grpc-protobuf`, `grpc-stub`), `protobuf-java`
- **PostgreSQL 15+** with [`pgvector`](https://github.com/pgvector/pgvector) extension

## Development

### Generate gRPC Code

Python:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. vectorize.proto
```

Java (Maven with protobuf-maven-plugin):

```bash
mvn compile
```

## Run Vectorizer

```bash
python server.py
```

## Run JavaService

```bash
mvn spring-boot:run
```

## Roadmap

- **Data Storage**
  - Store full embedding vectors in PostgreSQL using the `pgvector` extension.
- **Scraping**
  - Add a route to scrape available wines directly from winery sources.
  - Implement multiple scrapers to discover additional wineries.
  - Extend scrapers to gather and aggregate detailed information about specific wines.
- **Data Enrichment**
  - Generate descriptive summaries of wines based on the collected data.
- **Search & Retrieval**
  - Add a similarity search API (nearest-neighbor queries on embeddings).
- **DevOps**
  - Establish a CI/CD pipeline for generating and publishing the shared proto artifact.
