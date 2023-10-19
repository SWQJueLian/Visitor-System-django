from dataclasses import dataclass
from typing import Union, Any


@dataclass
class Result:
    code: int
    message: Union[str, dict]
    data: Any = None
    extra: Any = None
