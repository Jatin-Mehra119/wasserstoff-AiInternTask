# Documentation Index

Welcome to the RAG Chat Application documentation! This directory contains comprehensive guides to help you understand, use, and contribute to the project.

## 📚 Documentation Structure

### Quick Start & Overview
- **[README.md](README.md)** - Project overview, architecture diagram, and quick start guide
- **[Main README](../README.md)** - Comprehensive project documentation with detailed features and usage

### API Reference
- **[API.md](API.md)** - Complete REST API documentation with examples and curl commands

### Development
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer guide for contributing to the project

## 🎯 Getting Started

### For Users
1. Read the [Quick Start](README.md#-quick-start) section
2. Follow the [Installation & Running](README.md#installation--running) instructions
3. Review the [API Reference](API.md) for integration details

### For Developers
1. Start with the [Development Setup](DEVELOPMENT.md#-development-setup)
2. Understand the [Project Structure](DEVELOPMENT.md#-project-structure)
3. Review [Core Components](DEVELOPMENT.md#-core-components)
4. Check the [Contributing Guidelines](DEVELOPMENT.md#-contributing)

## 🏗️ Architecture Quick Reference

The application follows a layered architecture:

- **Client Layer**: Web frontend + Streamlit MVP
- **Backend Layer**: FastAPI with modular routes
- **RAG Engine Layer**: Core document processing and vector search
- **Persistence Layer**: FAISS vector store with metadata
- **External Services**: GROQ API and Sentence Transformers

See the [architecture diagram](README.md#️-architecture-overview) for visual representation.

## 🔗 Quick Links

| Topic | Document | Description |
|-------|----------|-------------|
| **Overview** | [README.md](README.md) | Architecture and quick start |
| **API Endpoints** | [API.md](API.md) | REST API reference |
| **Development** | [DEVELOPMENT.md](DEVELOPMENT.md) | Contributing guidelines |
| **Main README** | [../README.md](../README.md) | Detailed project documentation |
| **Tests** | [../tests/README.md](../tests/README.md) | Testing documentation |

## 🚀 Core Features

- **Multi-format Document Processing**: PDF, text, images, code files
- **Intelligent Chat Interface**: AI-powered responses with citations
- **Vector Search**: FAISS-powered semantic similarity search
- **Persistence**: Save and load processed document collections
- **Modern Web UI**: Responsive design with real-time updates
- **Comprehensive API**: RESTful endpoints with interactive documentation

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI/ML**: GROQ API, Sentence Transformers, LangChain
- **Search**: FAISS vector database
- **Testing**: pytest, requests

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Jatin-Mehra119/wasserstoff-AiInternTask/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Jatin-Mehra119/wasserstoff-AiInternTask/discussions)
- **API Docs**: http://localhost:8000/docs (when server is running)

## 📝 Contributing

We welcome contributions! Please read the [Development Guide](DEVELOPMENT.md#-contributing) for guidelines on:

- Code style and standards
- Testing requirements
- Pull request process
- Adding new features

---

*This documentation is maintained alongside the codebase. For the most up-to-date information, always refer to the latest version in the repository.*
