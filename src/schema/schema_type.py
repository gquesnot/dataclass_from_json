import dataclasses
from dataclasses import field
from typing import Optional, List, Union

from src.enums.type_enum import MyTypeBase, MyTypeDefault, MyTypeWithMapping


@dataclasses.dataclass
class SchemaType:
    primary: Optional[MyTypeBase] = None
    secondary: List[Union[MyTypeBase, "SchemaType"]] = field(default_factory=set)
    nullable: bool = False

    def __post_init__(self):
        self.primary = None
        self.secondary = list()
        self.nullable = False

    def __eq__(self, other):
        if isinstance(other, SchemaType):
            return self.primary == other.primary and self.secondary == other.secondary and self.nullable == other.nullable
        return False

    def getSecondary(self):
        results = []
        for secondary in self.secondary:
            if isinstance(secondary, str):
                element = secondary
            elif isinstance(secondary, MyTypeDefault):
                element = secondary.value
            elif isinstance(secondary, SchemaType):
                if len(secondary.secondary) == 0:
                    print('*** get secondary', self)
                element = secondary.secondary[0]
                if isinstance(element, MyTypeDefault):
                    element = element.value
                if secondary.nullable:
                    element = f"Optional[{element}]"
            else:
                element = secondary
            results.append(element)
        if len(results) == 1:
            return results[0]
        else:
            return f"Union[{', '.join(results)}]"



    def hasClass(self):
        if self.primary is None:
            return False
        if self.primary == MyTypeWithMapping.CLASS or self.primary == MyTypeWithMapping.LIST_ROOT:
            return True
        elif len(self.secondary) > 0:
            for v in self.secondary:
                if isinstance(v, MyTypeDefault):
                    return False
                elif isinstance(v, str):
                    return True
                elif v.primary == MyTypeWithMapping.CLASS:
                    return True
        return False

    def secondaryNullable(self):
        for k in self.secondary:
            if isinstance(k, SchemaType):
                return k.nullable
        return False

    def canAdd(self, child):
        return child.primary is None or child.primary == MyTypeWithMapping.CLASS

    def addSecondary(self, type_:Union[MyTypeDefault, MyTypeWithMapping, str, "SchemaType"]):
        if type_ is None:
            self.nullable = True
        else:
            if type_ not in self.secondary:
                if isinstance(type_, MyTypeDefault) or isinstance(type_, MyTypeWithMapping):
                    self.secondary.append(type_)
                elif isinstance(type_, str):
                    self.secondary = [type_]
                elif type_ not in self.secondary and self.canAdd(type_):
                    if type_.nullable:
                        self.secondary.append(type_)
                    else:
                        self.secondary.extend(type_.secondary)
