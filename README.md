# Sistema de Gestión de Informes y Autenticación

Una solución web integral desarrollada en Python para la gestión eficiente de usuarios, autenticación segura y generación automatizada de informes dinámicos. Diseñado bajo una arquitectura modular y listo para despliegue en la nube mediante contenedores Docker y flujos CI/CD.

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Flask](https://img.shields.io/badge/framework-flask-green.svg)

## Características Principales

- **Gestión de Usuarios:** Sistema completo de registro y autenticación con verificación de identidad mediante correo electrónico.
- **Generación de Reportes:** Motor de creación de informes personalizados con capacidad de exportación a PDF y visualización en tiempo real.
- **Formularios Dinámicos:** Interfaz optimizada para la captura de datos y procesamiento de URLs de análisis.
- **Despliegue DevOps:** Configuración profesional con soporte para despliegue automatizado mediante AWS CodeDeploy y Docker Compose.
- **Arquitectura Escalable:** Separación lógica entre modelos, rutas y vistas, facilitando el mantenimiento y la escalabilidad del sistema.

## Guía de Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose instalados.
- Python 3.10+ (para desarrollo local).

### Ejecución con Docker
1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```
2. Iniciar los servicios:
   ```bash
   docker-compose up --build
   ```
3. Acceder a la aplicación desde `http://localhost:5000`.

### Ejecución Local
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación:
   ```bash
   python run.py
   ```

## Estructura del Proyecto

```text
.
├── app/                # Lógica de la aplicación y plantillas
│   ├── static/         # Assets: CSS, JS, Imágenes
│   └── templates/      # Vistas HTML (Jinja2)
├── scripts/            # Hooks de despliegue (AWS CodeDeploy)
├── utils/              # Funciones auxiliares de procesamiento
├── appspec.yml         # Configuración para AWS CodeDeploy
├── config.py           # Variables de configuración
├── Dockerfile          # Configuración del contenedor
├── docker-compose.yml  # Orquestación de servicios
└── run.py              # Punto de entrada
```

## Soporte y Documentación

Para reportar errores, sugerir mejoras o realizar consultas técnicas, por favor utilice el sistema de *Issues* del repositorio. Asegúrese de incluir pasos detallados para reproducir cualquier comportamiento inesperado.

## Mantenimiento y Contribución

Este proyecto fomenta la colaboración abierta. Antes de enviar cambios:
1. Revise el archivo `CONTRIBUTING.md` para conocer nuestras normas de estilo y flujo de trabajo.
2. Verifique que el código cumpla con los estándares definidos.
3. Envíe sus propuestas a través de un *Pull Request*.

Este software se distribuye bajo los términos definidos en el archivo `LICENSE`.