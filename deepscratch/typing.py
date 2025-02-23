from typing import TypeVar, Union, List, Tuple, Dict

T = TypeVar("T")  # Generic type variable for leaves
PyTree = Union[T, List["PyTree[T]"], Tuple["PyTree[T]", ...], Dict[str, "PyTree[T]"]]
