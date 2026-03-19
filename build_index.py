import os
import json

DATA_FOLDER = "texts"
INDEX_FILE = "index.json"

index = []

for file in os.listdir(DATA_FOLDER):
    with open(os.path.join(DATA_FOLDER, file), encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if name:
                index.append(name)

# save index
with open(INDEX_FILE, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print("Index created successfully!")
