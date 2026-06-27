from pathlib import Path
from app.rag import ingest_file

def infer_business_id(filename: str):
    parts = filename.split("_")
    for part in parts:
        if part in ["P", "C", "S"]:
            return part
    return "P"


for folder in ["data/clean", "data/poisoned"]:
    for path in Path(folder).glob("*.txt"):
        business_id = infer_business_id(path.name)
        result = ingest_file(business_id, str(path))
        print(result)
