# Sistema de Gestión de Informes y Autenticación

Este proyecto es una aplicación web robusta diseñada para la gestión de usuarios, generación de informes dinámicos y procesamiento de datos. Construido sobre un framework web en Python, el sistema integra capacidades de autenticación, verificación por correo electrónico y generación de reportes en formato PDF, optimizado para despliegue en contenedores.

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Flask](https://img.shields.io/badge/framework-flask-green.svg)

## Características Principales

- **Gestión de Usuarios:** Sistema completo de registro, inicio de sesión y verificación de cuentas mediante correo electrónico.
- **Generación de Informes:** Creación de reportes personalizados con soporte para exportación a PDF y visualización web.
- **Formularios Dinámicos:** Interfaz intuitiva para la captura de datos y URLs de análisis.
- **Despliegue DevOps:** Configuración lista para producción mediante Docker y scripts automatizados de ciclo de vida (AWS CodeDeploy ready).
- **Arquitectura Modular:** Separación clara entre la lógica de negocio, modelos de datos y plantillas de presentación.

## Guía de Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose instalados.
- Python 3.x (si se ejecuta fuera de contenedor).

### Instalación y Ejecución con Docker
1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. Levantar los servicios:
   ```bash
   docker-compose up --build
   ```

3. Acceder a la aplicación desde `http://localhost:5000`.

### Ejecución Local
1. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ejecutar la aplicación:
   ```bash
   python run.py
   ```

## Estructura del Proyecto

```text
.
├── app/                # Código fuente principal (lógica, modelos, vistas)
│   ├── static/         # Recursos estáticos (CSS, JS, Imágenes)
│   └── templates/      # Plantillas HTML (Jinja2)
├── scripts/            # Scripts de automatización y despliegue (CI/CD)
├── utils/              # Funciones auxiliares y utilidades de análisis
├── Dockerfile          # Configuración de contenedor
├── docker-compose.yml  # Orquestación de servicios
├── run.py              # Punto de entrada de la aplicación
└── requirements.txt    # Dependencias del proyecto
```

## Servicios y APIs Externas

La aplicación depende de los siguientes servicios externos para realizar sus funciones de análisis:

- **[Google PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started):** Utilizada para obtener métricas de rendimiento, SEO, accesibilidad y mejores prácticas.
- **[WhatCMS API](https://whatcms.org/API):** Utilizada para identificar el CMS y las tecnologías base de los sitios web analizados.
- **[WhoHostsThis API](https://www.who-hosts-this.com/API):** Utilizada para identificar el proveedor de hosting de los sitios web.
- **[Website Technology Lookup API](https://rapidapi.com/santiagomontes7/api/website-technology-lookup-api/) (vía RapidAPI):** Utilizada como alternativa para la detección de tecnologías web.
- **Servicio SMTP (Flask-Mail):** Utilizado para el envío de correos electrónicos transaccionales (verificación de cuentas).

Para el correcto funcionamiento de estas características, asegúrese de configurar las variables de entorno necesarias (claves de API, credenciales de correo) tal como se indica en la configuración del proyecto.

## Soporte y Documentación

Para reportar errores o solicitar nuevas funcionalidades, por favor abra un *Issue* en el repositorio siguiendo las plantillas proporcionadas. Si requiere asistencia técnica adicional, consulte los archivos dentro de la carpeta `docs/` (si están disponibles) o contacte con el equipo de mantenimiento.

## Mantenimiento y Contribución

Este proyecto acepta contribuciones a través de *Pull Requests*. Antes de realizar cambios, por favor:
1. Asegúrese de leer la guía de estilo del código.
2. Verifique que todas las pruebas pasen correctamente.
3. Consulte el archivo `CONTRIBUTING.md` para conocer el flujo de trabajo estándar.

Este software se distribuye bajo los términos definidos en el archivo `LICENSE`.