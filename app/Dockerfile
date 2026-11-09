# Imagen base de Python con version fija
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar las dependencias
COPY requirements.txt .

# Intslar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codigo de la aplicacion
COPY app.py .

# Puero utilizado por Flask
EXPOSE 5000

# Iniciar la aplicacion
CMD ["python", "app.py"]
