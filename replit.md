# Sistema de Votación Blockchain - IzyVote

## Overview

IzyVote is a secure, anonymous blockchain-based voting system built with Flask. The application enables transparent elections where votes are cryptographically secured and stored in a blockchain, ensuring immutability and verifiability while maintaining voter anonymity. The system is specifically designed for university environments, requiring @uni.pe or @uni.edu.pe email addresses for authentication.

## System Architecture

The application follows a traditional web application architecture with blockchain integration:

**Frontend**: HTML templates with Bootstrap for responsive UI, JavaScript for client-side validation
**Backend**: Flask web framework with SQLAlchemy ORM for database operations
**Database**: PostgreSQL (production) / SQLite (development) for metadata storage
**Blockchain**: Custom Python implementation for vote storage and verification
**Email Service**: SMTP integration for verification codes
**Deployment**: Gunicorn WSGI server on Replit with autoscaling

## Key Components

### 1. Web Application Layer (`app.py`, `main.py`, `routes.py`)
- Flask application factory pattern with database initialization
- Route handlers for voting flow, admin panel, and blockchain visualization
- Session management for admin authentication and voter verification

### 2. Database Models (`models.py`)
- **Election**: Stores election metadata and voting options as JSON
- **VerificationCode**: Links verification codes to specific elections and emails
- **VoterHistory**: Prevents double voting using hashed email addresses

### 3. Blockchain Implementation (`blockchain.py`)
- Custom Block class with SHA-256 hashing and proof-of-work mining
- VotingBlockchain class for chain management and vote processing
- Persistent storage in JSON format for blockchain data

### 4. Email Service (`email_service.py`)
- SMTP-based verification code generation and delivery
- HTML email templates for user communication
- Configurable email provider support

### 5. Frontend Templates (`templates/`)
- Base template with Bootstrap dark theme and responsive design
- Voter flow: email verification → code entry → voting → results
- Admin panel for election management and system monitoring

## Data Flow

1. **Election Creation**: Admin creates election with title, description, and options
2. **Voter Verification**: User enters @uni.pe or @uni.edu.pe email, system sends 6-digit verification code
3. **Vote Submission**: User enters code and selects option, system validates and processes
4. **Blockchain Recording**: Valid votes are added to pending votes, then mined into blocks
5. **Result Display**: Real-time results calculated from blockchain data with charts

## External Dependencies

### Core Dependencies
- **Flask 3.1.1**: Web framework for routing and templating
- **SQLAlchemy 2.0.41**: Database ORM with PostgreSQL support
- **Gunicorn 23.0.0**: Production WSGI server for deployment
- **psycopg2-binary**: PostgreSQL database adapter

### Additional Libraries
- **python-dotenv**: Environment variable management
- **email-validator**: Email format and domain validation
- **Bootstrap 5**: Frontend CSS framework with dark theme
- **Chart.js**: JavaScript charting library for results visualization
- **Font Awesome**: Icon library for UI elements

### External Services
- **Gmail SMTP**: Email delivery service for verification codes
- **Replit PostgreSQL**: Managed database service for production

## Deployment Strategy

The application is configured for deployment on Replit with the following setup:

**Environment**: Python 3.11 with PostgreSQL 16 module
**Process Management**: Gunicorn with automatic binding and port configuration
**Scaling**: Autoscale deployment target for handling variable loads
**Database**: Automatic PostgreSQL provisioning with connection string injection
**Security**: Environment variables for sensitive configuration data

Configuration files:
- `.replit`: Defines runtime environment and deployment settings
- `pyproject.toml`: Python dependencies and project metadata
- `.env`: Environment variables for database, email, and security settings

The deployment uses a two-stage approach:
1. Development: SQLite database with debug mode enabled
2. Production: PostgreSQL with Gunicorn and environment-based configuration

## Changelog

- June 27, 2025. Added support for @uni.edu.pe email domain in addition to @uni.pe
- June 21, 2025. Reset voting processes and blockchain system
- June 21, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.