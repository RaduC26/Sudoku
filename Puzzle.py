from Square import Square
import random

BLOCK_SIZE = 60
BLACK = (0, 0, 0)
example = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

example2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]

row = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def createMatrix():
    matrix = example
    for r in range(9):
        for c in range(9):
            matrix[r][c] = Square(BLOCK_SIZE * c, BLOCK_SIZE * r, example[r][c], BLACK)
    return matrix


# def generateRandomEmptyMatrix():
#     matrix = example2
#     for i in range(9):
#         matrix[i][i] = randrange(9)


class Puzzle:
    def __init__(self):
        self.__matrix = None
        self.__is_solved = False
        self.__status = 'Starting'

    def getMatrix(self):
        return self.__matrix

    def isSolved(self):
        return self.__is_solved

    def getStatus(self):
        return self.__status

    def setMatrix(self, matrix):
        self.__matrix = matrix

    def setIsSolved(self, flag):
        self.__is_solved = flag

    def setStatus(self, status):
        self.__status = status

    def generateRandomEmptyMatrix(self):
        self.__matrix = example2
        random.shuffle(row)
        for i in range(9):
            self.__matrix[0][i] = Square(BLOCK_SIZE * i, 0, row[i], BLACK)
        for r in range(1, 9):
            for c in range(9):
                self.__matrix[r][c] = Square(BLOCK_SIZE * c, BLOCK_SIZE * r, 0, BLACK)
        self.solve()
        counter = 1
        random_list = random.sample(range(1, 81), 25)
        for r in range(9):
            for c in range(9):
                if counter in random_list:
                    pass
                else:
                    self.__matrix[r][c].setNumber(0)
                counter += 1

    def solve(self):
        for r in range(9):
            for c in range(9):
                if self.__matrix[r][c].getNumber() == 0:
                    for n in range(1, 10):
                        if self.checkColumnRow(r, c, n) and self.checkSquare(r, c, n):
                            self.__matrix[r][c].setNumber(n)
                            self.solve()
                            if self.isSolved():
                                pass
                            else:
                                self.__matrix[r][c].setNumber(0)
                    return
        self.checkSolved()

    def checkColumnRow(self, c, r, cell_no):
        for i in range(9):
            if self.__matrix[i][r].getNumber() == cell_no or self.__matrix[c][i].getNumber() == cell_no:
                return False
        return True

    def checkSquare(self, r, c, cell_no):
        row_index = int(r / 3) * 3
        column_index = int(c / 3) * 3
        for i in range(row_index, row_index + 3):
            for j in range(column_index, column_index + 3):
                if self.__matrix[i][j].getNumber() == cell_no:
                    return False
        return True

    def checkSolved(self):
        flag = True
        for r in range(9):
            for c in range(9):
                if self.__matrix[r][c].getNumber() == 0:
                    flag = False
        if flag:
            self.__is_solved = True
        else:
            self.__is_solved = False

    def manualPrintMatrix(self):
        for r in range(9):
            if r % 3 == 0:
                print("----------------------")
            for c in range(9):
                if c % 3 == 0:
                    print("|", end="")
                print(self.__matrix[r][c].getNumber(), end=" ")
            print("|")
        print("----------------------")
