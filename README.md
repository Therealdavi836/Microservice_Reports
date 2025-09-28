# Microservicio de Reportes - Concesionario de Vehículos

Este es unn servicio de generación de reportes de datos para diferentes microservicios en un ecosistema modular de microservicios de un aplicativo web de un concesionario de vehiculos como parte del proyecto semestral de Ingeniería de Software II.
Provee dos unicas funcionalidades de reportes de datos a traves de la conexión con diferentes microservicios dependiendo del tipo de información que se quiera solicitar para reportar, en este caso la generación del reporte se manejara mediante usuarios unicamente autenticados (Administradores) y con verificación del Token generado por el microservicio de autenticación.

---

## Tabla de Contenido

1. [Propósito y Alcance](#propósito-y-alcance)
2. [Arquitectura y Contexto](#arquitectura-y-contexto)
3. [Funcionalidades](#funcionalidades)
4. [Tipos de Reportes](#tipos-de-reportes)
5. [Integración con Microservicios](#integración-con-microservicios)
6. [Requisitos Técnicos para ejecución](#requisitos-técnicos-para-ejecución)
7. [Instalación](#instalación)
8. [Configuración](#configuración)
9. [Ejecución del Microservicio](#ejecución-del-microservicio)
10. [Autenticación y Autorización](#autenticación-y-autorización)
11. [Pruebas con Postman](#pruebas-con-postman)
12. [Endpoints Disponibles](#endpoints-disponibles)
13. [Estructura del Proyecto](#estructura-del-proyecto)
14. [Contribución](#contribución)

## Propósito y Alcance

El Microservicio de Reportes es un componente crítico del sistema de gestión del concesionario de vehículos que centraliza la generación de informes ejecutivos y operativos. Este servicio recopila, procesa y presenta información de manera estructurada desde múltiples fuentes de datos.

## Arquitectura y Contexto

### Contexto del Concesionario

En el ecosistema del concesionario de vehículos, este microservicio actúa como el centro de remisión de datos del sistema, integrando datos de:

- **Base de datos de usuarios**: Información de clientes, vendedores y soporte tecnico
- **Base de datos de vehículos**: por definir
- **Publicaciones y ventas**: Transacciones, contratos y seguimiento de ventas
- **Auditoría y logs**: Trazabilidad de flujo de funcionamiento del aplicativo y funciones de seguridad

### Integración con la Arquitectura de Microservicios

El servicio se conecta con otros microservicios del ecosistema mediante APIs REST y consume datos en tiempo real para generar reportes actualizados y precisos.

## Funcionalidades

### Principales Características

- **Generación de Reportes**: Creación de informes sobre datos actuales de las diferentes bases de datos
- **Reportes On-Demand**: Generación inmediata de reportes
- **Múltiples Formatos**: Exportación en PDF y Excel para diferentes necesidades

No incluye (aún): Filtros Avanzados, Agregaciones complejas y visualizaciones avanzadas de datos mediante herramientas estadisticas; se dejan en el roadmap para implementaciones futuras.

## Tipos de Reportes

### Reportes de Usuarios

Reporte de los usuarioa actuales que se tiene en la base de datos MySQL del microservicio de autenticación.

### Reportes de Vehículos

Reporte de los vehiculos actuales que dispone el concesionario a traves del microservicio del catalogo de vehiculos

### Reportes de publicaciones y ventas

Reporte de las publicaciones creadas en el sitio web y las ventas obtenidas hasta la fecha.

### Reportes de Auditoría y logs

Reporte de posibles incidentes de seguridad e inicios de sesión registrados en el sistema

## Integración con Microservicios

### Microservicios Existentes

- **Microservicio de Autenticación**: Para validación de tokens y permisos de usuario
- **Microservicio de Usuarios**: Datos de clientes y personal
- **Microservicio de Vehículos**: Información del inventario y catálogo
- **Microservicio de Ventas**: Transacciones y contratos

## Requisitos Técnicos para ejecución

### Dependencias del Sistema

- Python 3.8 o superior
- Base de datos PostgreSQL/MySQL (para metadatos)
- Docker (Implementación futura)

### Librerías Python Principales

- Flask (framework web)
- Pandas (manipulación de datos)
- ReportLab (generación de PDFs)
- OpenPyXL (generación de Excel)
- Requests (para consultar otros microservicios)

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Therealdavi836/Microservice_Reports.git
cd Microservice_Reports
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Configuración

## Ejecución del Microservicio

Antes de ejecutar el microservicio es necesario tener el microservicio de autenticación para tener el token bearer pues es requisito de seguridad, estar autenticado para generar los reportes como usuario administrador (OJO: tener ejecutadas las migraciones de laravel e ir a la base de datos en laragon y ponerse rol de admin para probar) a traves de postman pues thunder client por limitación impide descargar los reportes generales, se debe de incluir el token sea en uno de los header o en el apartado auth o uatorization en bearer, mas adelante encontrara la información de como ejecutarla.

### Verificación del Servicio

El microservicio estará disponible en: `http://localhost:5000` o `http://127.0.0.1:5000`

## Autenticación y Autorización

### Requisitos de Autenticación

**IMPORTANTE**: Este microservicio requiere autenticación mediante tokens JWT emitidos por el Microservicio de Autenticación. Solo usuarios con rol de **administrador** pueden generar reportes.

### Configuración del Usuario Administrador

1. **Registrarse en la base de datos del Microservicio de Autenticación**:

   ```json
   POST http://localhost:8000/api/register
   {
     "name": "admin",
     "email": "admin@concesionario.com",
     "password": "Admin123!",
   }
   ```

    Laravel sanctum por defecto lo va a registrar como cliente, para adecuar el rol a admin con id `1` es necesario ir a la base de datos mediante laragon, dirigirse a la tabla `users` y en `role_id` seleccionar el mencionado anteriormente que sera 1 para este caso.

    - Abrir laragon y ubicarse en la base de datos creada en el microservicio
    ![alt text](image.png)
    - Ubicarse en la tabla usuarios
    ![alt text](image-1.png)
    - Seleccionar `role_id` numero 1
    ![alt text](image-2.png)

2. **Obtener Token de Autenticación mdiante inicio de sesión**:

   ```json
   POST http://localhost:8000/api/login
   {
     "email": "admin",
     "password": "Admin123!"
   }
   ```

3. **Respuesta con Token**:

   ```json
   {
     "access_token": "<TOKEN>",
     "user_name": "nombre_usuario",
     "token_type": "Bearer"
   }
   ```

### Uso del Token Bearer

Todos los endpoints del microservicio de reportes requieren el header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Un ejemplo detallado usando thunderclient
![alt text](image-3.png)

Un ejemplo detallado usando Postman
![alt text](image-5.png)

**NOTA**:añadir en los headers para ambos en headers: `Content-Type` y `application/json`

## Pruebas con Postman

### Configuración Inicial de Postman

1. **Crear Nueva Colección**: "Microservicio Reportes - Concesionario"

2. **Configurar Variables de Entorno**:
   - `base_url`: `http://localhost:5000`
   - `auth_token`: `Bearer tu_token_aqui`

3. **Configurar Autorización Global**:
   - Tipo: Bearer Token
   - Token: `{{auth_token}}`

### Colección de Pruebas Recomendadas

#### 1. Generar Reporte de Usuarios (PDF)

```http
POST http://localhost:5000/report/pdf
Authorization: {{auth_token}}
Content-Type: application/json

{
    "ms_url":"http://localhost:8000/api/users"
}
```

#### 2. Generar Reporte de Usuarios (excel)

```http
POST http://localhost:5000/report/excel
Authorization: {{auth_token}}
Content-Type: application/json

{
    "ms_url":"http://localhost:8000/api/users"
}
```

#### 3. Generar Reporte de Vehículos (Excel)

```http
POST http://localhost:5000/report/excel
Authorization: {{auth_token}}
Content-Type: application/json
{
    "ms_url":
}
```

#### 4. Generar Reporte de Vehículos (PDF)

```http
POST http://localhost:5000/report/pdf
Authorization: {{auth_token}}
Content-Type: application/json
{
    "ms_url":
}
```

#### 5. Generar Reporte de publicaciones y ventas (Excel)

```http
POST http://localhost:5000/report/excel
Authorization: {{auth_token}}
Content-Type: application/json
{
    "ms_url":
}
```

#### 6. Generar Reporte de publicaciones y ventas (PDF)

```http
POST http://localhost:5000/report/pdf
Authorization: {{auth_token}}
Content-Type: application/json
{
    "ms_url":
}
```

#### 7. Generar Reporte de Auditoría (PDF)

```http
POST http://localhost:5000/report/pdf
Authorization: {{auth_token}}
Content-Type: application/json
{
    "ms_url":
}
```

#### 8. Generar Reporte de Auditoría (Excel)

```http
POST http://localhost:5000/report/excel
Authorization: {{auth_token}}
Content-Type: application/json
{
    "ms_url":
}
```

#### 9. Descargar Reporte Generado

![alt text](image-6.png)

### Proceso de Descarga de Reportes

1. **Generar Reporte**: Usar endpoints POST para crear el reporte dependiendo del tipo de información solicitud
2. **Verificar Estado**: Esperar una respuesta 200
3. **Descargar Archivo**: Una vez completado, descargar usando postman guiandose de la imagen de arriba

## Endpoints Disponibles

### Endpoints de Reportes de Usuarios

Por implementar

### Endpoints de Reportes de Vehículos

Por implementar

### Endpoints de Reportes de Publicaciones y Ventas

Por implementar

### Endpoints de Reportes de Auditoría

Por implementar

## Estructura del Proyecto

```text
Microservice_Reports/
├── app.py                          # Archivo principal de la aplicación
├── requirements.txt                # Dependencias de Python
├── README.md                       # Documentación del proyecto
|── .gitignore
├── reports/
│   ├── excel_report.py            # Generación de reportes Excel
└   └── pdf_report.py              # Generación de reportes PDF
```

## Contribución

### Estándares de Desarrollo

1. **Código**: Seguir PEP 8 para Python
2. **Tests**: Pendientes de diseñar las pruebas
3. **Documentación**: Documentar todas las funciones públicas
4. **Commits**: Usar conventional commits

### Proceso de Contribución

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Realizar cambios y tests
4. Commit: `git commit -m "feat: agregar nueva funcionalidad"`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Crear Pull Request

### Licencia

MIT.

### Contacto / Mantenimiento

- Juan David Fajardo Betancourt
- Email: jfajardob@unal.edu.co

---

### Razón

- Proyecto semestral de Ingeniería de Software II, Semestre 2025-2.
- Presentado al docente: Jose Albeiro Montes Gil.
- Documento de planeación:
- Informe de evidencia de ejecución de pruebas unitarias: 
