from __future__ import annotations
from dataclasses import dataclass
from typing import Generator, TypeVar, Generic, Iterable

_T = TypeVar("_T")


@dataclass
class Node(Generic[_T]):
    value: _T
    left: Node[_T] | None = None
    right: Node[_T] | None = None


class Tree(Generic[_T]):

    def __init__(self, root: Node[_T]) -> None:
        self._root = root

    @classmethod
    def from_iter(cls, it: Iterable[_T]) -> Tree[_T]:
        pass

    def __iter__(self) -> Generator[_T, None, None]:

        def _inorder(node: Node[_T] | None) -> Generator[_T, None, None]:
            if node is not None:
                yield from _inorder(node.left)
                yield node.value
                yield from _inorder(node.right)

        return _inorder(self._root)


a = Node("a", Node("b"), Node("c"))
tree = Tree(a)
print([x for x in tree])
