import pandas as pd
from pathlib import Path

p = Path("data")
p.mkdir(exist_ok=True)
df = pd.read_csv(p / "sample_full.csv")
chunks = [df[i:i+10] for i in range(0, len(df), 10)]
(p / "chunks").mkdir(exist_ok=True)
for i,ch in enumerate(chunks):
    ch.to_csv(p / "chunks" / f"chunk_{i}.csv", index=False)
