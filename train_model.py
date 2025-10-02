# train_model.py
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
import os

spark = SparkSession.builder.appName("train_model").getOrCreate()

DATA_CSV = "data/sample_full.csv"
MODEL_DIR = "model/logreg_model"

df = spark.read.option("header", True).option("inferSchema", True).csv(DATA_CSV)

features = [c for c in df.columns if c != 'label']

label_indexer = StringIndexer(inputCol='label', outputCol='labelIndex')
assembler = VectorAssembler(inputCols=features, outputCol='features')
lr = LogisticRegression(featuresCol='features', labelCol='labelIndex')

pipeline = Pipeline(stages=[label_indexer, assembler, lr])
model = pipeline.fit(df)

if os.path.exists(MODEL_DIR):
    import shutil; shutil.rmtree(MODEL_DIR)
model.write().overwrite().save(MODEL_DIR)

print("✅ Modelo guardado en", MODEL_DIR)
spark.stop()
