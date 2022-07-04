
class {className}(StrEnum):
{params}

    @classmethod
    def values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def keys(cls) -> List["{className}"]:
        return list(map(lambda c: c, cls))
