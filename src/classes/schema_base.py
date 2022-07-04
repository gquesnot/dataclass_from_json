from abc import ABC, abstractmethod
from dataclasses import field
from typing import Optional, List, Union, Any

from src.dataclass.custom_type import CustomType


class SchemaBase(ABC):
    """
    This class is used to be the base class for all type_ of datas
    """

    root: "SchemaRoot"
    parent: Optional[Union["SchemaDict", "SchemaList", "SchemaClass"]] = field(
        default_factory=lambda: None
    )
    name: str = ""
    path: str = ""
    nullable: bool = False
    type: CustomType
    datas: List[Any] = field(default_factory=list)

    def __init__(
            self,
            name: str,
            path: str,
            type_: "CustomType",
            root: "SchemaRoot",
            parent: Optional[Union["SchemaDict", "SchemaList", "SchemaClass"]] = None,
    ):
        """
        This method is used to initialize the class
        """
        self.name = name
        self.parent = parent
        self.root = root
        self.nullable = False
        self.type = type_
        self.path = path
        self.datas = []

    def __str__(self):
        return f"{self.path} :\n{' ' * 4 + 'type: ' + str(self.type)}"

    def add_data(self, data):
        self.datas.append(data)

    def __len__(self):
        return len(self.datas)

    @abstractmethod
    def scan_required(self):
        pass

    @abstractmethod
    def generate_class(self):
        pass

    @abstractmethod
    def scan_for_mappings(self):
        pass
