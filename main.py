import argparse

from src.controllers.level_controller import LevelController

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "names",
        nargs="+",
        help="Names of the classes to generate / name of the json file without "
             ".json, separated by spaces",
    )
    args.add_argument(
        "--generate-only", help="Only generate the dataclass", action="store_true"
    )
    args.add_argument(
        "--load-only", help="Only load the dataclass", action="store_true"
    )
    args.add_argument(
        "--with-data", help="load the dataclass with data", action="store_true"
    )
    args.add_argument(
        "--show-data", help="show datas if --with-data", action="store_true"
    )
    args.add_argument(
        "--json_path", help="path to json directory", type=str, default="jsons"
    )
    args.add_argument(
        "--dtc_path",
        help="path to the directory where you want to store the dataclasses",
        type=str,
        default="dataclass",
    )
    args.add_argument("--verbose", help="verbose mode", action="store_true")
    args = args.parse_args()
    controller = LevelController(
        json_path=args.json_path, dtc_path=args.dtc_path, verbose=args.verbose
    )
    if not args.load_only:
        controller.generate(args.names)
    if not args.generate_only:
        controller.load(args.names)
        datas = controller.getClass(args.names, withDatas=args.with_data)
        if args.show_data and args.with_data or not args.with_data:
            print(datas)
