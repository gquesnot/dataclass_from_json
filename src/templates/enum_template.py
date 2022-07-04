from strenum import StrEnum

class {className}(StrEnum):
{params}

    @staticmethod
    def keys() -> List[str]:
        return list({className}.__members__.values())

    @staticmethod
    def values() -> List['{className}']:
        return list({className}.__members__.keys())


