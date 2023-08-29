from collections import UserDict
from typing import Hashable, Callable, Any, Dict


class MapDict(UserDict):
    def __init__(self, another_dict: Dict[Hashable, Any], function: Callable[[Any], Any]):
        self.function = function
        super().__init__(another_dict)

    def __getitem__(self, key: Hashable):
        value = self.data.__getitem__(key)
        changed_value = self.function(value)
        return changed_value
