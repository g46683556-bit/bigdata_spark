# stream_processor.py
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from pyspark.ml import PipelineModel

# Crear sesión de Spark
spark = SparkSession.builder.appName("stream_processor").getOrCreate()

INPUT_DIR = "input"
OUTPUT_DIR = "output"
MODEL_DIR = "model/logreg_model"

# Cargar el modelo entrenado
model = PipelineModel.load(MODEL_DIR)

# Definir esquema del CSV
schema = StructType([
    StructField("sepal_length", DoubleType(), True),
    StructField("sepal_width", DoubleType(), True),
    StructField("petal_length", DoubleType(), True),
    StructField("petal_width", DoubleType(), True),
    StructField("label", StringType(), True)
])

# Leer el stream con esquema definido
stream_df = (
    spark.readStream
         .option("header", True)
         .schema(schema)   # 🔑 IMPORTANTE
         .csv(INPUT_DIR)
)

# Aplicar el modelo al stream
predictions = model.transform(stream_df)

# Seleccionar columnas de salida
out = predictions.select("prediction", "probability", *[c for c in stream_df.columns])

# Guardar las predicciones en formato JSON
query = (
    out.writeStream
       .format("json")
       .option("path", OUTPUT_DIR)
       .option("checkpointLocation", "checkpoint/")
       .outputMode("append")
       .start()
)

print("👀 Streaming escuchando en carpeta", INPUT_DIR)
query.awaitTermination()
