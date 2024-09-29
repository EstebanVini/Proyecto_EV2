FROM python:3.11.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/application

# Copiar los archivos necesarios
COPY app ./app
COPY data ./data
COPY requirements.txt .
COPY dev.env

# Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 80
EXPOSE 80

# Comando para ejecutar Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]