class Square:
    def __init__(self, pos_x, pos_y, number, borderColor):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__number = number
        self.__borderColor = borderColor

    def getPosX(self):
        return self.__pos_x

    def getPosY(self):
        return self.__pos_y

    def getNumber(self):
        return self.__number

    def getBorderColor(self):
        return self.__borderColor

    def setNumber(self, number):
        self.__number = number

    def setBorderColor(self, color):
        self.__borderColor = color
