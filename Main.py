import pygame
import sys
from time import sleep

from Puzzle import Puzzle

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 123, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 540
BLOCK_SIZE = 60
SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])


def main():
    global SCREEN, puzzle
    pygame.init()
    pygame.display.set_caption('SUDOKU')
    start_ticks = pygame.time.get_ticks()
    running = True
    puzzle = Puzzle()
    selected_cell = (0, 0)
    X = []
    time = 0

    font = pygame.freetype.SysFont(None, 26)
    font.origin = True

    while running:
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if puzzle.getStatus() == 'Playing':
                    setBorderColor(selected_cell, BLACK)
                    selected_cell = square_coord(pygame.mouse.get_pos())
                    setBorderColor(selected_cell, ORANGE)
                else:
                    start_ticks = pygame.time.get_ticks()
                    puzzle.generateRandomEmptyMatrix()
                    puzzle.setStatus('Playing')
                    puzzle.setIsSolved(False)
                    X = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    solveMatrix()
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    enterNumber(0, selected_cell)
                elif 1 <= int(pygame.key.name(event.key)) <= 9:
                    if puzzle.checkSquare(selected_cell[1], selected_cell[0], int(pygame.key.name(event.key))) and \
                            puzzle.checkColumnRow(selected_cell[1], selected_cell[0], int(pygame.key.name(event.key))):
                        setBorderColor(selected_cell, GREEN)
                    else:
                        setBorderColor(selected_cell, RED)
                        X.append('1')
                        if len(X) == 5:
                            puzzle.setStatus('Failed')
                    enterNumber(int(pygame.key.name(event.key)), selected_cell)
                    puzzle.checkSolved()
                    if puzzle.isSolved():
                        time = pygame.time.get_ticks() - start_ticks
                        puzzle.setStatus('Finished')
        if puzzle.getStatus() == 'Playing':
            printMatrix()
            printTimer(font, start_ticks)
            placeX(X)
        else:
            printHomeScreen(time)
        pygame.display.update()


def solveMatrix():
    for r in range(9):
        for c in range(9):
            if puzzle.getMatrix()[r][c].getNumber() == 0:
                for n in range(1, 10):
                    if puzzle.checkColumnRow(r, c, n) and puzzle.checkSquare(r, c, n):
                        SCREEN.fill(WHITE)
                        puzzle.getMatrix()[r][c].setNumber(n)
                        puzzle.getMatrix()[r][c].setBorderColor(GREEN)
                        printMatrix()
                        pygame.display.update()
                        sleep(0.0001)
                        solveMatrix()
                        if puzzle.isSolved():
                            pass
                        else:
                            puzzle.getMatrix()[r][c].setNumber(0)
                return
    puzzle.checkSolved()


def printMatrix():
    border_thickness = 2
    font = pygame.font.SysFont('Ariel', 46)
    for r in range(9):
        for c in range(9):
            # Print Borders
            rect = pygame.Rect(puzzle.getMatrix()[r][c].getPosX(), puzzle.getMatrix()[r][c].getPosY(), BLOCK_SIZE,
                               BLOCK_SIZE)
            if puzzle.getMatrix()[r][c].getBorderColor() == RED or puzzle.getMatrix()[r][c].getBorderColor() == ORANGE:
                border_thickness = 5
            pygame.draw.rect(SCREEN, puzzle.getMatrix()[r][c].getBorderColor(), rect, border_thickness)
            border_thickness = 2

            # Print Numbers
            number = str(puzzle.getMatrix()[r][c].getNumber())
            if int(number) > 0:
                text = font.render(number, True, BLACK)
                rect_width = text.get_rect().width
                rect_height = text.get_rect().height
                SCREEN.blit(text, (
                    BLOCK_SIZE * c + BLOCK_SIZE / 2 - rect_width / 2 + 1,
                    BLOCK_SIZE * r + BLOCK_SIZE / 2 - rect_height / 2 + 4))


def highlightSquare(pos):
    puzzle.getMatrix()[pos[1]][pos[0]].setBorderColor(RED)


def setBorderColor(pos, color):
    puzzle.getMatrix()[pos[1]][pos[0]].setBorderColor(color)


def deHighlightSquare(pos):
    puzzle.getMatrix()[pos[1]][pos[0]].setBorderColor(BLACK)


def enterNumber(number, cell):
    puzzle.getMatrix()[cell[1]][cell[0]].setNumber(number)


def square_coord(pos):
    y = int(pos[0] / BLOCK_SIZE)
    x = int(pos[1] / BLOCK_SIZE)
    return y, x


def printTimer(font, start_ticks):
    seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)
    minutes = int(seconds / 60)
    hours = int(minutes / 60)
    timer_string = "Time: {hours:02}:{minutes:02}:{seconds:02}".format(hours=hours, minutes=minutes % 60,
                                                                       seconds=seconds % 60)
    font.render_to(SCREEN, (340, 582), timer_string, BLACK)


def printHomeScreen(time):
    big_font = pygame.freetype.SysFont(None, 26)
    small_font = pygame.freetype.SysFont(None, 14, italic=True)
    normal_font = pygame.freetype.SysFont(None, 18)
    big_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 138, WINDOW_HEIGHT / 4), 'Welcome to SUDOKU!', BLACK)
    small_font.render_to(SCREEN, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 25), 'by Radu Camarascu', BLACK)
    big_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2), 'Press anywhere to Start!', BLACK)
    pygame.draw.rect(SCREEN, BLACK, (40, 360, 460, 200), 2, 15)
    if puzzle.getStatus() == 'Starting':
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 100),
                              'Instructions: - Select a cell with your mouse', BLACK)
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 87, WINDOW_HEIGHT / 2 + 120),
                              '- Enter a number in the cell', BLACK)
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 87, WINDOW_HEIGHT / 2 + 140),
                              '- You have 5 lives', BLACK)
        small_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 180),
                             'Additionally: Press Space to automatically solve the puzzle', BLACK)
    elif puzzle.getStatus() == 'Finished':
        seconds = int(time / 1000)
        minutes = int(seconds / 60)
        hours = int(minutes / 60)
        timer_string = "{hours:02} Hours,{minutes:02} Minutes and {seconds:02} Seconds".format(hours=hours,
                                                                                               minutes=minutes % 60,
                                                                                               seconds=seconds % 60)
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 100),
                              'Congratulations!', BLACK)
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 150),
                              'You completed the game in: ', BLACK)
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 + 170),
                              '{time}'.format(time=timer_string), BLACK)
    elif puzzle.getStatus() == 'Failed':
        normal_font.render_to(SCREEN, (WINDOW_WIDTH / 2 - 180, WINDOW_HEIGHT / 2 + 130),
                              'You lost all your 5 lives! Maybe try again!', BLACK)


def placeX(x):
    font = pygame.freetype.SysFont(None, 26, bold=True)
    for i in range(len(x)):
        font.render_to(SCREEN, (20 * i + 10, WINDOW_HEIGHT - 35), 'X', RED)


if __name__ == '__main__':
    main()
