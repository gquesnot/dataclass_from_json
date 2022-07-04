import argparse
import os

import requests

from src.controllers.schema_controller import SchemaController

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("type", type=str,help="chose between raw json or url", choices=["json", "url"])
    args.add_argument(
        "input",
        nargs="+",
        help="url or json file or directory",
    )
    args.add_argument(
        "--generate-only", help="Only generate the dataclass", action="store_true"
    )
    args.add_argument(
        "--load-only", help="Only load the dataclass", action="store_true"
    )
    args.add_argument(
        "--show-data", help="show datas if --with-data", action="store_true"
    )
    args.add_argument(
        "--show-schema", help="show dtc schema", action="store_true"
    )
    args.add_argument(
        "--name", help="name of the dataclass required if url", type=str, default=None
    )

    args.add_argument(
        "--output",
        help="where to write class",
        type=str,
        default="test_dataclass",
    )
    args.add_argument("--verbose", help="verbose mode", action="store_true")
    args = args.parse_args()
    sc = SchemaController(args)
    sc.generate_all()
