# Big Data con PySpark

Proyecto que utiliza **PySpark** para procesar datos y entrenar un modelo, integrado con **Django** para la carga y visualización de archivos CSV.

---

## Requisitos

1. **Instalar Java JDK 17**  
   Descargar desde:  
   [Descargar JDK 17 (Adoptium)](https://adoptium.net/es/download?link=https%3A%2F%2Fgithub.com%2Fadoptium%2Ftemurin17-binaries%2Freleases%2Fdownload%2Fjdk-17.0.16%252B8%2FOpenJDK17U-jdk_x64_windows_hotspot_17.0.16_8.msi&vendor=Adoptium)  
   Agregar la variable de entorno `JAVA_HOME` y añadir `%JAVA_HOME%\bin` al PATH.

2. **Configurar Hadoop**  
   - Descomprimir `bin.zip`.  
   - Crear la carpeta `C:\hadoop`.  
   - Copiar dentro la carpeta `bin` descomprimida.

3. **Instalar dependencias de Python**  
   ```bash
   pip install -r requirements.txt


## Mandar CSV a /data
Pasar un archivo sample_full.csv a la carpeta /data

## Ejecutar el train_model.py
Para ejecutar el archivo train_model.py es necesario tener el archivo sample_full.csv en la carpeta /data, ya que con eso se va a entrenar y crear el modelo Spark ML

# Crear carpetas
Crear las carpetas input y output en la raiz del proyecto

## Ejecutar el stream_processor.py
Ahora con el modelo Spark ML recien se puede ejecutar stream_processor.py

## Ejecutar django
El archivo stream_processor.py va estar a la escucha, así que en otra terminal ejecutar django con 'python manage.py runserver'.
Ojo, no hay que cancelar la terminal en la que esta corriendo 'stream_processor.py'

# Pruebas
En la pagina que se genero, hacer la prueba subiendo un CSV y poniendo en generar lote


-------------------------------------------------------------------------



# 📂 Preparación del proyecto

Copiar el archivo sample_full.csv dentro de la carpeta data/.

Crear las carpetas input/ y output/ en la raíz del proyecto.

Estructura esperada:

project_root/
├── app/
|   ├── static/
|   |   └── graficos/
|   ├── templates/
|   |   └── app/
|   |       ├── graficos.html
|   |       └── index.html
|   ├── urls.py
|   └── views.py
│
├── data/
│   └── sample_full.csv
├── input/
├── output/
├── train_model.py
├── stream_processor.py
└── manage.py

⚙️ Ejecución
1. Entrenar el modelo

Ejecuta el siguiente comando:

python train_model.py


Este script entrena el modelo Spark ML utilizando el archivo data/sample_full.csv.

2. Iniciar el procesamiento en streaming

Con el modelo entrenado, ejecuta:

python stream_processor.py


Mantén esta terminal abierta, ya que este script escucha continuamente los nuevos datos en streaming.

3. Iniciar el servidor Django

En una nueva terminal, ejecuta:

python manage.py runserver


⚠️ No cierres la terminal donde corre stream_processor.py.

🧪 Pruebas

Accede a la página web generada por Django (por defecto: http://localhost:8000
).

Sube un archivo CSV.

Haz clic en "Generar lote" para procesar el archivo con el modelo entrenado.

🧰 Tecnologías utilizadas

Python 3.10+

PySpark

Django

Hadoop

Spark MLlib




