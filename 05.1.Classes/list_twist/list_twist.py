from collections import UserList
import typing as tp


# https://github.com/python/mypy/issues/5264#issuecomment-399407428
if tp.TYPE_CHECKING:
    BaseList = UserList[tp.Optional[tp.Any]]
else:
    BaseList = UserList


class ListTwist(BaseList):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """
    Reversed = ['reversed', 'R']
    First = ['first', 'F']
    Last = ['last', 'L']
    Size = ['size', 'S']

    def __getattr__(self, s: str) -> tp.Any:
        if s in self.Reversed:
            return list(reversed(self.data))
        elif s in self.Size:
            return len(self)
        elif s in self.First:
            return self.data[0]
        elif s in self.Last:
            return self.data[-1]
        else:
            return super().__getattribute__(s)

    def __setattr__(self, x: str, y: tp.Any) -> None:
        if x in self.Size:
            if y < len(self.data):
                del self.data[y:]
            elif y > len(self):
                self.data += [None] * (y - len(self.data))
        elif x in self.First:
            self.data[0] = y
        elif x in self.Last:
            self.data[-1] = y
        else:
            return super().__setattr__(x, y)
