from src.controllers.schema_root import SchemaRoot

if __name__ == "__main__":
    schema_root = SchemaRoot(json_path="test_jsons", dtc_path="test_dataclass")
    schema_root.generate("champions")
