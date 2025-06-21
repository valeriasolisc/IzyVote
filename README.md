
# IzyVote - Sistema de Votación Blockchain

[![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-v3.1+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🗳️ Descripción

IzyVote es un sistema de votación seguro y anónimo basado en blockchain, diseñado específicamente para universidades. Utiliza tecnología blockchain para garantizar la transparencia, inmutabilidad y verificabilidad de los votos, mientras mantiene el anonimato de los votantes.

## ✨ Características Principales

- **🔒 Seguridad**: Verificación por email con códigos de 6 dígitos
- **🔗 Blockchain**: Almacenamiento inmutable de votos en blockchain personalizada
- **👤 Anonimato**: Solo se almacenan hashes de emails, no información personal
- **🏫 Enfoque Universitario**: Validación específica para dominios @uni.pe
- **📊 Transparencia**: Visualización completa de la blockchain y resultados
- **⚡ Tiempo Real**: Resultados actualizados automáticamente

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask 3.1.1, SQLAlchemy 2.0.41
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Blockchain**: Implementación personalizada en Python con SHA-256
- **Email**: SMTP con templates HTML
- **Deployment**: Gunicorn en Replit

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- PostgreSQL (para producción)

### Configuración Local

1. **Clona el repositorio**
```bash
git clone https://github.com/tu-usuario/izyvote-blockchain.git
cd izyvote-blockchain
```

2. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

3. **Configura las variables de entorno**
Crea un archivo `.env` con:
```env
SESSION_SECRET=tu-clave-secreta-aqui
EMAIL_USERNAME=tu-email@gmail.com
EMAIL_PASSWORD=tu-password-de-aplicacion
ADMIN_EMAIL=admin@uni.pe
ADMIN_PASSWORD=tu-password-admin
```

4. **Ejecuta la aplicación**
```bash
python main.py
```

## 📋 Uso del Sistema

### Para Votantes

1. **Acceder**: Visita la página principal para ver elecciones activas
2. **Verificar Email**: Ingresa tu email @uni.pe para recibir código de verificación
3. **Votar**: Ingresa el código de 6 dígitos y selecciona tu opción
4. **Confirmar**: Recibe confirmación por email de voto registrado

### Para Administradores

1. **Login**: Accede al panel admin con credenciales configuradas
2. **Crear Elecciones**: Define título, descripción y opciones de voto
3. **Gestionar**: Activa/desactiva elecciones según necesidad
4. **Monitorear**: Visualiza estadísticas de blockchain y participación

## 🔧 Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Flask App     │    │   Blockchain    │
│   (Bootstrap)   │◄──►│   (SQLAlchemy)   │◄──►│   (Custom)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │   PostgreSQL    │
                       │   (Metadata)    │
                       └─────────────────┘
```

### Flujo de Datos

1. **Verificación**: Usuario → Email → Código → Validación
2. **Votación**: Voto → Validación → Blockchain → Minado
3. **Resultados**: Blockchain → Conteo → Visualización

## 🔐 Características de Seguridad

- **Verificación de Dominio**: Solo emails @uni.pe permitidos
- **Prevención de Doble Voto**: Tabla de historial con constraints únicos
- **Códigos Temporales**: Expiración automática en 30 minutos
- **Hash de Emails**: Anonimato garantizado mediante SHA-256
- **Blockchain Inmutable**: Imposible alterar votos una vez minados
- **Validación de Cadena**: Detección automática de alteraciones

## 📊 Estructura de Base de Datos

### Tablas Principales

- **Election**: Metadata de elecciones y opciones
- **VerificationCode**: Códigos temporales de verificación
- **VoterHistory**: Historial de votantes (solo hashes)

### Blockchain

- **Blocks**: Índice, timestamp, votos, hash anterior, nonce
- **Votes**: Election ID, opción, timestamp, vote ID

## 🚀 Deployment en Replit

El proyecto está optimizado para deployment en Replit:

```toml
[deployment]
deploymentTarget = "autoscale"
run = ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Variables de Entorno Requeridas

- `SESSION_SECRET`: Clave secreta para sesiones
- `EMAIL_USERNAME`: Usuario SMTP para envío de emails
- `EMAIL_PASSWORD`: Password de aplicación para Gmail
- `ADMIN_EMAIL`: Email del administrador
- `ADMIN_PASSWORD`: Password del administrador

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

- **Desarrollador**: Tu Nombre
- **Email**: tu-email@uni.pe
- **Universidad**: Universidad Nacional de Ingeniería

## 🎯 Roadmap

- [ ] Implementar notificaciones en tiempo real
- [ ] Añadir autenticación multifactor
- [ ] Soporte para múltiples instituciones
- [ ] API REST completa
- [ ] Aplicación móvil
- [ ] Integración con sistemas universitarios

---

**IzyVote** - Democratizando las elecciones universitarias con tecnología blockchain 🗳️⛓️
