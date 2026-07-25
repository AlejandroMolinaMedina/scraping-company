# Usa la imagen oficial de Python como base
FROM python:3.8

# Establece el directorio de trabajo
WORKDIR /app

# Actualiza la lista de paquetes y luego instala Vim
RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y wkhtmltopdf && \
    apt-get install -y tree 

# Copia los archivos de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el resto de los archivos
COPY . .

# Agrega el directorio de tu módulo al PYTHONPATH
ENV PYTHONPATH="/app:/app/app/utils"

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "run.py"]

