import pandas as pd

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
cols = ["sepal_length","sepal_width","petal_length","petal_width","label"]
df = pd.read_csv(url, names=cols)

# Guardar a CSV
df.to_csv("data/sample_full.csv", index=False)
print("CSV listo en data/sample_full.csv")
