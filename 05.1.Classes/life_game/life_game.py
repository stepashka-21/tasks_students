

class LifeGame(object):
    """
    Class for Game life
    """
    def __init__(self, start_board: list[list[int]]) -> None:
        self._Board = start_board
        self._rows = len(start_board)
        self._columns = len(start_board[0])

    def __get_neighbours(self, i: int, j: int) -> tuple[int, int]:
        fis: int = 0
        shr: int = 0
        if j < self._columns - 1 and self._Board[i][j+1] == 2: fis += 1
        elif j < self._columns - 1 and self._Board[i][j+1] == 3: shr += 1
        if j > 0 and self._Board[i][j-1] == 2: fis += 1
        elif j > 0 and self._Board[i][j-1] == 3: shr += 1
        if j < self._columns - 1 and i < self._rows - 1 and self._Board[i+1][j+1] == 2: fis += 1
        elif j < self._columns - 1 and i < self._rows - 1 and self._Board[i+1][j+1] == 3: shr += 1
        if i < self._rows - 1 and j > 0 and self._Board[i+1][j-1] == 2: fis += 1
        elif i < self._rows - 1 and j > 0 and self._Board[i+1][j-1] == 3: shr += 1
        if i < self._rows - 1 and self._Board[i+1][j] == 2: fis += 1
        elif i < self._rows - 1 and self._Board[i+1][j] == 3: shr += 1
        if i > 0 and j > 0 and self._Board[i-1][j-1] == 2: fis += 1
        elif i > 0 and j > 0 and self._Board[i-1][j-1] == 3: shr += 1
        if i > 0 and j < self._columns - 1 and self._Board[i-1][j+1] == 2: fis += 1
        elif i > 0 and j < self._columns - 1 and self._Board[i-1][j+1] == 3: shr += 1
        if i > 0 and self._Board[i-1][j] == 2: fis += 1
        elif i > 0 and self._Board[i-1][j] == 3: shr += 1
        return fis, shr

    def get_next_generation(self) -> list[list[int]]:
        newocean = [[0 for _ in range(self._columns)] for _ in range(self._rows)]
        for i in range(self._rows):
            for j in range(self._columns):
                if self._Board[i][j] == 1:
                    newocean[i][j] = 1
                elif self._Board[i][j] == 2:
                    count = self.__get_neighbours(i, j)[0]
                    if count == 2 or count == 3:
                        newocean[i][j] = 2
                    else:
                        newocean[i][j] = 0
                elif self._Board[i][j] == 3:
                    count = self.__get_neighbours(i, j)[1]
                    if count == 2 or count == 3:
                        newocean[i][j] = 3
                    else:
                        newocean[i][j] = 0
                else:
                    if self.__get_neighbours(i, j)[0] == 3:
                        newocean[i][j] = 2
                    elif self.__get_neighbours(i, j)[1] == 3:
                        newocean[i][j] = 3
        self._Board = newocean
        return self._Board

