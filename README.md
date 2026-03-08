# 🐝 Soft Bee Backend

## 📌 Descripción del Proyecto

**The Lost Heaven – Soft Bee Backend** es un backend diseñado para soportar aplicaciones modernas mediante una arquitectura escalable, mantenible y desacoplada.

El proyecto sigue principios de **Clean Architecture**, separación de responsabilidades y uso de **inyección de dependencias**, permitiendo construir APIs robustas y fáciles de mantener.

Este backend actúa como la **capa central del sistema**, encargándose de:

- Procesamiento de lógica de negocio
- Gestión de autenticación y autorización
- Comunicación con la base de datos
- Exposición de APIs para clientes (frontend o servicios externos)
- Configuración y manejo de entornos

La arquitectura modular permite escalar el sistema fácilmente y facilita el trabajo en equipo manteniendo un código limpio y organizado.

---

# 🧭 Visión General del Proyecto

El backend está diseñado para proporcionar una base sólida para el desarrollo de aplicaciones backend siguiendo buenas prácticas de ingeniería de software.

## Objetivos principales

- Crear una API mantenible y escalable
- Aplicar principios de **Clean Architecture**
- Separar correctamente responsabilidades
- Facilitar pruebas unitarias y mantenimiento
- Permitir crecimiento del sistema sin acoplamientos fuertes

---

# 🧩 Arquitectura del Sistema

El proyecto utiliza **Clean Architecture**, un patrón arquitectónico que separa el sistema en diferentes capas independientes.

## Principios utilizados

- **Separación de responsabilidades**
- **Independencia del framework**
- **Independencia de la base de datos**
- **Código orientado a dominio**
- **Alta testabilidad**

Esto permite que las reglas de negocio del sistema permanezcan aisladas de tecnologías externas.

---

# 🏗 Arquitectura General

La arquitectura está organizada en diferentes capas:

### Descripción de capas

 - **Presentation Layer**
    - Controladores de la API
    - Manejo de solicitudes HTTP
    - Validación de datos de entrada

- **Application Layer**
    - Casos de uso del sistema
    - Coordinación de operaciones
    - Orquestación de lógica de negocio

- **Domain Layer**
    - Entidades del sistema
    - Reglas de negocio principales
    - Interfaces de repositorios

- **Infrastructure Layer**
  - Conexión con base de datos
  - Implementaciones de repositorios
  - Integraciones externas

---

# 📁 Estructura del Proyecto

El proyecto está organizado siguiendo una estructura modular.
  ```
    src/
    │
    ├── application
    │ ├── use-cases
    │ └── services
    │
    ├── domain
    │ ├── entities
    │ └── repositories
    │
    ├── infrastructure
    │ ├── database
    │ ├── repositories
    │ └── providers
    │
    ├── interfaces
    │ ├── controllers
    │ └── routes
    │
    ├── config
    │ └── environment
    │
    └── main
    └── server

  ```

### Descripción de carpetas

| Carpeta | Descripción |
|------|------|
| `application` | Contiene los casos de uso del sistema |
| `domain` | Define entidades y lógica de negocio |
| `infrastructure` | Implementaciones técnicas (DB, servicios externos) |
| `interfaces` | Controladores y rutas de la API |
| `config` | Configuración del sistema |
| `main` | Inicialización del servidor |

---

# ⚙️ Inyección de Dependencias

El proyecto utiliza **Dependency Injection (DI)** para desacoplar componentes.

### Ventajas

- Reduce el acoplamiento
- Mejora la testabilidad
- Permite reemplazar implementaciones fácilmente
- Facilita mantenimiento

### Flujo conceptual

 ```
          Controller
              ↓
            UseCase
              ↓
    Repository Interface
              ↓
    Repository Implementation
  ```

El controlador no conoce la implementación concreta del repositorio, solo su interfaz.

---

# ⚙️ Configuración del Entorno

La configuración del sistema se gestiona mediante **variables de entorno**.

- Archivo principal:
 ```
   .env
 ```

**Ejemplo:**

  ```env
    PORT=3000
    
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    DATABASE_USER=admin
    DATABASE_PASSWORD=password
    DATABASE_NAME=softbee
    
    JWT_SECRET=supersecret
    JWT_EXPIRES_IN=1d
  ```
Esto permite cambiar configuraciones sin modificar el código.

---

# 🗄 Configuración de Base de Datos

El backend utiliza una base de datos para almacenar información persistente del sistema.

- Configuraciones principales:
  - Host
  - Puerto
  - Usuario
  - Contraseña
  - Nombre de la base de datos

Las conexiones se gestionan desde el módulo de infraestructura, lo que permite cambiar la base de datos sin afectar la lógica del sistema.

---

# 🔐 Autenticación con JWT

El sistema utiliza JSON Web Tokens (JWT) para manejar autenticación segura.

## Flujo de autenticación

  - El usuario inicia sesión
  - El servidor valida las credenciales
  - Se genera un JWT
  - El cliente envía el token en cada request

**Ejemplo:**
  
  ```
    Authorization: Bearer <token>
  ```

## Ventajas

  - Autenticación sin estado (stateless)
  - Seguridad
  - Escalabilidad
  - Fácil integración con APIs

---

# 🚀 Instalación del Proyecto

## 1️⃣ Clonar el repositorio:

  ```
    git clone https://github.com/SoffiaSanchezz/Soft-Bee-Back-End.git
  ```

## 2️⃣ Instalar dependencias

   ```
    npm install
   ```

## 3️⃣ Configurar variables de entorno
- Crear archivo:

    ```
    .env
   ```
    Basado en:

   ```
    .env.example
   ```
## 4️⃣ Ejecutar el proyecto

  Modo desarrollo:
  
   ```
    npm run dev
  ```

  Modo producción:

   ```
    npm start
   ```

---

# 📡 API

El backend expone endpoints REST para permitir la comunicación con aplicaciones frontend u otros servicios.

Las rutas se organizan por módulos dentro de:

   ```
    interfaces/routes
   ```

---

# 🧪 Buenas Prácticas Implementadas

  -  Clean Architecture
  -  Separación de capas
  -  Inyección de dependencias
  -  Configuración mediante variables de entorno
  -  Autenticación JWT
  -  Código modular y escalable
