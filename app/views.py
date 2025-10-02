import os
import io
import time
import json
import shutil
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")   # backend no interactivo, ideal para Django
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# --- Rutas principales ---
INPUT = Path("input")
CHUNKS = Path("data/chunks")
OUTPUT = Path("output")
DATA = Path("data")
STATIC_G = Path("app/static/graficos")

CHUNK_SIZE = 10  # número de filas por chunk

# Crear carpetas si no existen
for p in [INPUT, CHUNKS, OUTPUT, DATA, STATIC_G]:
    p.mkdir(parents=True, exist_ok=True)


def index(request):
    files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
    resultados = []
    for f in files[:5]:
        with open(f) as fh:
            for line in fh:
                try:
                    data = json.loads(line)
                    data["origen"] = f.stem  # guardamos el nombre del archivo como "origen"
                    resultados.append(data)
                except:
                    pass
    return render(request, "app/index.html", {"resultados": resultados})


@csrf_exempt
def upload_csv(request):
    """Subir un CSV completo y dividirlo en chunks"""
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        # Guardar en /data
        save_path = DATA / file.name
        with open(save_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Dividir en chunks con prefijo del nombre
        df = pd.read_csv(save_path)
        tag = Path(file.name).stem
        for i in range(0, len(df), CHUNK_SIZE):
            chunk = df.iloc[i:i + CHUNK_SIZE]
            chunk_file = CHUNKS / f"{tag}_chunk_{i // CHUNK_SIZE + 1}.csv"
            chunk.to_csv(chunk_file, index=False)

        total_chunks = (len(df) // CHUNK_SIZE) + (1 if len(df) % CHUNK_SIZE else 0)
        print(f"✅ CSV {file.name} dividido en {total_chunks} chunks con tag {tag}")

        messages.success(request, f"✅ Archivo {file.name} subido y dividido en {total_chunks} chunks.")
        return redirect("index")

    messages.error(request, "⚠️ Debes subir un archivo CSV válido.")
    return redirect("index")


# def generar_lote(request):
#     """Mover un chunk al input para que Spark lo procese"""
#     files = list(CHUNKS.glob("*.csv"))
#     if not files:
#         return JsonResponse({"error": "No hay chunks en data/chunks"})

#     src = files[int(time.time()) % len(files)]
#     dst = INPUT / f"batch_{int(time.time()*1000)}.csv"
#     shutil.copy(src, dst)
#     print(f"📥 Lote generado desde {src.name}")
#     return redirect("index")

def generar_lote(request):
    """Mover un chunk al input para que Spark lo procese"""
    files = list(CHUNKS.glob("*.csv"))
    if not files:
        return JsonResponse({"error": "No hay chunks en data/chunks"})

    src = files[int(time.time()) % len(files)]
    dst = INPUT / f"batch_{int(time.time()*1000)}.csv"

    # 🔑 Mover de manera atómica (Spark ve el archivo solo cuando ya está completo)
    os.replace(src, dst)

    print(f"📥 Lote generado: {src.name} -> {dst.name}")
    return redirect("index")


def graficos(request):
    # Leer resultados de output
    files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
    data = []
    for f in files[:5]:
        with open(f) as fh:
            for line in fh:
                try:
                    data.append(json.loads(line))
                except:
                    pass

    if not data:
        return render(request, "app/graficos.html", {"msg": "No hay datos en output aún."})

    # Convertir a DataFrame
    df = pd.DataFrame(data)
    plots = []

    # ---- 1. Matriz de correlación ----
    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    heatmap_path = STATIC_G / "heatmap.png"
    plt.savefig(heatmap_path, bbox_inches="tight")
    plt.close()
    plots.append("graficos/heatmap.png")

    # ---- 2. Clustering con KMeans ----
    if {"sepal_length", "sepal_width"} <= set(df.columns):
        X = df[["sepal_length", "sepal_width"]].dropna()
        if len(X) > 2:
            kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
            clusters = kmeans.labels_

            plt.figure(figsize=(6, 4))
            plt.scatter(X["sepal_length"], X["sepal_width"], c=clusters, cmap="viridis")
            plt.xlabel("Sepal Length")
            plt.ylabel("Sepal Width")
            plt.title("KMeans Clustering")
            kmeans_path = STATIC_G / "kmeans.png"
            plt.savefig(kmeans_path, bbox_inches="tight")
            plt.close()
            plots.append("graficos/kmeans.png")

    return render(request, "app/graficos.html", {"plots": plots})
