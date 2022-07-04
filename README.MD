Dataclass from json
==================

Dataclass from json is a class to generate dataclass from json and write them in a file.

Look at tests to see how to use it

## Installation

```bash
pip install -r requirements.txt
# or 
poetry install
```

## Usage

### Create a dataclass from json

```python
from src.controllers.schema_root import SchemaRoot

if __name__ == "__main__":
    schema_root = SchemaRoot(json_path="test_jsons", dtc_path="test_dataclass")
    schema_root.generate("champions")
```

### Load the dataclass

```python
import json
from test_dataclass.champions import Champions

if __name__ == "__main__":
    with open("test_jsons\\champions.json", "r") as f:
        data = json.load(f)
    champions = Champions.from_dict(data)
```

## Test

```bash
  pytest . --no-header --no-summary -q
```



