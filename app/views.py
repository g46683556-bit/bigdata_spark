# import os, shutil, time, json, glob
# from pathlib import Path
# import pandas as pd
# from django.shortcuts import render, redirect
# from django.http import JsonResponse

# INPUT = Path("input")
# CHUNKS = Path("data/chunks")
# OUTPUT = Path("output")
# DATA = Path("data")   # carpeta donde guardas el csv completo
# CHUNK_SIZE = 10       # filas por chunk

# for p in [INPUT, CHUNKS, OUTPUT]:
#     p.mkdir(parents=True, exist_ok=True)

# def dividir_csv():
#     """Divide automáticamente el CSV principal en chunks si no existen"""
#     if list(CHUNKS.glob("*.csv")):
#         return  # ya hay chunks, no hacemos nada

#     # buscar un CSV completo en data/
#     files = list(DATA.glob("*.csv"))
#     if not files:
#         return  # no hay dataset completo todavía

#     df = pd.read_csv(files[0])  # tomar el primero
#     for i in range(0, len(df), CHUNK_SIZE):
#         chunk = df.iloc[i:i+CHUNK_SIZE]
#         chunk_file = CHUNKS / f"chunk_{i//CHUNK_SIZE + 1}.csv"
#         chunk.to_csv(chunk_file, index=False)
#     print(f"✅ CSV {files[0].name} dividido en {len(df)//CHUNK_SIZE+1} chunks.")

# def index(request):
#     # leer resultados más recientes
#     files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
#     resultados = []
#     for f in files[:5]:
#         with open(f) as fh:
#             for line in fh:
#                 try:
#                     resultados.append(json.loads(line))
#                 except:
#                     pass
#     return render(request, "app/index.html", {"resultados": resultados})

# def generar_lote(request):
#     dividir_csv()  # nos aseguramos de que haya chunks

#     files = list(CHUNKS.glob("*.csv"))
#     if not files:
#         return JsonResponse({"error": "No hay CSV en data/ para dividir"})

#     src = files[int(time.time()) % len(files)]
#     dst = INPUT / f"batch_{int(time.time()*1000)}.csv"
#     shutil.copy(src, dst)
#     return redirect("index")

import os, shutil, time, json
from django.contrib import messages
from pathlib import Path
import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Carpetas principales
INPUT = Path("input")
CHUNKS = Path("data/chunks")
OUTPUT = Path("output")
DATA = Path("data")
CHUNK_SIZE = 10  # número de filas por chunk

# Crear carpetas si no existen
for p in [INPUT, CHUNKS, OUTPUT, DATA]:
    p.mkdir(parents=True, exist_ok=True)


# def index(request):
#     """Página principal con resultados"""
#     files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
#     resultados = []
#     for f in files[:10]:  # mostramos los últimos 10
#         with open(f) as fh:
#             for line in fh:
#                 try:
#                     obj = json.loads(line)
#                     # añadimos el nombre del archivo para saber de qué CSV vino
#                     obj["_source"] = f.stem
#                     resultados.append(obj)
#                 except:
#                     pass
#     return render(request, "app/index.html", {"resultados": resultados})
def index(request):
    files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
    resultados = []
    for f in files[:5]:
        with open(f) as fh:
            for line in fh:
                try:
                    data = json.loads(line)
                    # guardamos el nombre del archivo como "origen"
                    data["origen"] = f.stem  
                    resultados.append(data)
                except:
                    pass
    return render(request, "app/index.html", {"resultados": resultados})



# @csrf_exempt
# def upload_csv(request):
#     """Subir un CSV completo y dividirlo en chunks"""
#     if request.method == "POST" and request.FILES.get("file"):
#         file = request.FILES["file"]

#         # Guardar en /data
#         save_path = DATA / file.name
#         with open(save_path, "wb+") as dest:
#             for chunk in file.chunks():
#                 dest.write(chunk)

#         # Dividir en chunks con prefijo del nombre
#         df = pd.read_csv(save_path)
#         tag = Path(file.name).stem
#         for i in range(0, len(df), CHUNK_SIZE):
#             chunk = df.iloc[i:i + CHUNK_SIZE]
#             chunk_file = CHUNKS / f"{tag}_chunk_{i // CHUNK_SIZE + 1}.csv"
#             chunk.to_csv(chunk_file, index=False)

#         print(f"✅ CSV {file.name} dividido en {len(df)//CHUNK_SIZE+1} chunks con tag {tag}")
#         return JsonResponse({"success": f"Archivo {file.name} cargado y dividido"})
#     return JsonResponse({"error": "Debes subir un archivo CSV"})



# PRUEBA UNO
# @csrf_exempt
# def upload_csv(request):
#     """Subir un CSV completo y dividirlo en chunks"""
#     if request.method == "POST" and request.FILES.get("file"):
#         file = request.FILES["file"]

#         # Guardar en /data
#         save_path = DATA / file.name
#         with open(save_path, "wb+") as dest:
#             for chunk in file.chunks():
#                 dest.write(chunk)

#         # Dividir en chunks con prefijo del nombre
#         df = pd.read_csv(save_path)
#         tag = Path(file.name).stem
#         for i in range(0, len(df), CHUNK_SIZE):
#             chunk = df.iloc[i:i + CHUNK_SIZE]
#             chunk_file = CHUNKS / f"{tag}_chunk_{i // CHUNK_SIZE + 1}.csv"
#             chunk.to_csv(chunk_file, index=False)

#         print(f"✅ CSV {file.name} dividido en {len(df)//CHUNK_SIZE+1} chunks con tag {tag}")

#          # Mostrar mensaje en la interfaz
#         messages.success(request, f"✅ Archivo {file.name} subido y dividido en {total_chunks} chunks.")

#         return redirect("index")   # 👈 aquí redirigimos a la vista principal
#     return JsonResponse({"error": "Debes subir un archivo CSV"})





# PRUEBA DOS
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from pathlib import Path

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

        # Mostrar mensaje en la interfaz
        messages.success(request, f"✅ Archivo {file.name} subido y dividido en {total_chunks} chunks.")
        return redirect("index")

    messages.error(request, "⚠️ Debes subir un archivo CSV válido.")
    return redirect("index")








# @csrf_exempt
# def upload_csv(request):
#     if request.method == "POST" and request.FILES.get("csv_file"):
#         csv_file = request.FILES["csv_file"]
#         filename = DATA / csv_file.name

#         # Guardar archivo subido
#         with open(filename, "wb+") as dest:
#             for chunk in csv_file.chunks():
#                 dest.write(chunk)

#         # Dividir en chunks
#         df = pd.read_csv(filename)
#         for i in range(0, len(df), CHUNK_SIZE):
#             chunk = df.iloc[i:i+CHUNK_SIZE]
#             chunk_file = CHUNKS / f"{filename.stem}_chunk_{i//CHUNK_SIZE + 1}.csv"
#             chunk.to_csv(chunk_file, index=False)

#         print(f"✅ Archivo {csv_file.name} cargado y dividido en chunks.")
#         return redirect("index")   # 👈 aquí redirigimos a la vista principal

#     return JsonResponse({"error": "No se subió ningún CSV"})



def generar_lote(request):
    """Mover un chunk al input para que Spark lo procese"""
    files = list(CHUNKS.glob("*.csv"))
    if not files:
        return JsonResponse({"error": "No hay chunks en data/chunks"})

    src = files[int(time.time()) % len(files)]
    dst = INPUT / f"batch_{int(time.time()*1000)}.csv"
    shutil.copy(src, dst)
    print(f"📥 Lote generado desde {src.name}")
    return redirect("index")



# def graficos(request):
#     # --- cargar resultados de clustering ---
#     cluster_results = []
#     cluster_files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
#     for f in cluster_files[:5]:
#         with open(f) as fh:
#             for line in fh:
#                 try:
#                     row = json.loads(line)
#                     if "cluster" in row:   # si viene de modelo KMeans
#                         cluster_results.append(row)
#                 except:
#                     pass

#     # --- cargar resultados de regresión ---
#     regression_results = []
#     for f in cluster_files[:5]:
#         with open(f) as fh:
#             for line in fh:
#                 try:
#                     row = json.loads(line)
#                     if "prediction" in row and "petal_length" in row: # regresión
#                         regression_results.append(row)
#                 except:
#                     pass

#     return render(request, "app/graficos.html", {
#         "clusters": cluster_results,
#         "regresiones": regression_results
#     })


# import os, io, json
# from pathlib import Path
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.linear_model import LinearRegression
# from django.http import HttpResponse
# from django.shortcuts import render

# OUTPUT = Path("output")

# def graficos(request):
#     # Leer resultados del output
#     files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
#     data = []
#     for f in files[:5]:
#         with open(f) as fh:
#             for line in fh:
#                 try:
#                     data.append(json.loads(line))
#                 except:
#                     pass

#     if not data:
#         return render(request, "app/graficos.html", {"msg": "No hay datos en output aún."})

#     # Convertir a DataFrame
#     df = pd.DataFrame(data)

#     # Usamos solo dos features para graficar
#     X = df[["sepal_length", "sepal_width"]].dropna()

#     # ---- Clustering con KMeans ----
#     kmeans = KMeans(n_clusters=3, random_state=0)
#     clusters = kmeans.fit_predict(X)
#     df["cluster"] = clusters

#     # ---- Regresión lineal (ejemplo: sepal_length -> sepal_width) ----
#     reg = LinearRegression()
#     reg.fit(X[["sepal_length"]], X["sepal_width"])
#     line_x = X["sepal_length"]
#     line_y = reg.predict(line_x.values.reshape(-1, 1))

#     # ---- Graficar ----
#     fig, ax = plt.subplots()
#     scatter = ax.scatter(X["sepal_length"], X["sepal_width"], c=clusters, cmap="viridis")
#     ax.plot(line_x, line_y, color="red", linewidth=2, label="Regresión lineal")
#     ax.set_xlabel("Sepal Length")
#     ax.set_ylabel("Sepal Width")
#     ax.legend()

#     # Guardar en memoria
#     buf = io.BytesIO()
#     plt.savefig(buf, format="png")
#     plt.close(fig)
#     buf.seek(0)

#     return HttpResponse(buf.getvalue(), content_type="image/png")

import os, io, json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # 👈 backend no interactivo, ideal para Django
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from django.shortcuts import render

OUTPUT = Path("output")
STATIC_G = Path("app/static/graficos")  # carpeta para guardar los plots
STATIC_G.mkdir(parents=True, exist_ok=True)

def graficos(request):
    # Leer resultados de output
    files = sorted(OUTPUT.glob("*.json"), key=os.path.getmtime, reverse=True)
    data = []
    for f in files[:5]:   # puedes aumentar el rango si quieres más datos
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
        if len(X) > 2:  # al menos algunos puntos
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

    print(plots)

    return render(request, "app/graficos.html", {"plots": plots})
