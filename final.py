from abc import ABC, abstractmethod
import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN
import numpy as np

white_queen = pg.image.load('assets/white queen.png')
white_bishop = pg.image.load('assets/white bishop.png')
white_rook = pg.image.load('assets/white rook.png')
white_king = pg.image.load('assets/white king.png')
white_knight = pg.image.load('assets/white knight.png')
white_pawn = pg.image.load('assets/white pawn.png')
black_queen = pg.image.load('assets/black queen.png')
black_bishop = pg.image.load('assets/black bishop.png')
black_rook = pg.image.load('assets/black rook.png')
black_king = pg.image.load('assets/black king.png')
black_knight = pg.image.load('assets/black knight.png')
black_pawn = pg.image.load('assets/black pawn.png')

starting_board =[['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                 ['#', '#', '#', '#', '#', '#', '#', '#'],
                 ['#', '#', '#', '#', '#', '#', '#', '#'],
                 ['#', '#', '#', '#', '#', '#', '#', '#'],
                 ['#', '#', '#', '#', '#', '#', '#', '#'],
                 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                 ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
                 ]

window_width = 800
window_height = 800
window = pg.display.set_mode((window_width, window_height))

class Piece(ABC):

    def __init__(self, color, position):
        self.color = color
        self.position = position

    def setpos(self, x, y):
        self.position = (x, y)

    @abstractmethod
    def find(self):
        pass

def wait_for_click():
    while True:
        for event in pg.event.get():
            try:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    return
            except KeyboardInterrupt:
                return

def get_pose(board, size_squares):
    wait_for_click()
    x, y = pg.mouse.get_pos()
    return int(np.floor(x / size_squares)), int(np.floor(y / size_squares))

def create_board(board):
    out = []
    pieces = {
        '#': None,
        'R': Rook,
        'N': Knight,
        'B': Bishop,
        'Q': Queen,
        'K': King,
        'P': Pawn
        }
    y = 0
    for column in board:
        x = 0
        row = []
        for square in column:
            if piece := pieces[square]:
                row.append(piece('black' if y<=2 else 'white', (x, y)))
            else:
                row.append(None)
            x += 1
        y += 1
        out.append(row)
    return out

def Turn(color, board):
    x1, y1 = get_pose(board, 100)
    if board[y1][x1]:
        P = board[y1][x1]
        available = P.find(board)
        print_board(board, window, available)
    x2, y2 = get_pose(board, 100)
    if type(board[y1][x1])==King and x2==x1+2 and y2==y1 and (x2, y2) in available:
        board[y1][x1+1] = board[y1][x1 + 3]
        board[y1][x1+3] = None
    if type(board[y1][x1])==King and x2==x1-2 and y2==y1 and (x2, y2) in available:
        board[y1][x1-1] = board[y1][x1-4]
        board[y1][x1-4] = None
    if (x1, y1)==(x2, y2):
        print_board(board, window)
        return False
    try:
        if color==board[y1][x1].color and (x2, y2) in available:
            current = board.copy()
            current[y2][x2] = current[y1][x1]
            current[y1][x1] = None
            P.setpos(x2, y2)
            print_board(current, window)
            return True
    except AttributeError:
        pass
    return False

def print_board(arr, window, available=None):
    dark_blue = (70, 70, 210)
    light_blue = (130, 130, 210)
    green = (100, 210, 100)
    red = (210, 100, 100)
    for x in range(1,9):
        for y in range(1,9):
            if (x%2==0 and y%2==0) or (x%2!=0 and y%2!=0):
                color = light_blue
                pg.draw.rect(window, color, [100*(x-1), 100*(y-1), 100, 100])
            else:
                color = dark_blue
                pg.draw.rect(window, color, [100*(x-1), 100*(y-1), 100, 100])
            try:
                if (x-1,y-1) in available:
                    pg.draw.rect(window, red if arr[y-1][x-1] else green, [100*(x-1), 100*(y-1), 100, 100])
            except TypeError:
                pass
            if arr[y-1][x-1] and arr[y-1][x-1].color=='white':
                if type(arr[y-1][x-1])==King:
                    window.blit(white_king, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Queen:
                    window.blit(white_queen, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Bishop:
                    window.blit(white_bishop, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Rook:
                    window.blit(white_rook, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Knight:
                    window.blit(white_knight, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Pawn:
                    window.blit(white_pawn, (100*(x-1), 100*(y-1)))

            elif arr[y-1][x-1] and arr[y-1][x-1].color=='black':
                if type(arr[y-1][x-1])==King:
                    window.blit(black_king, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Queen:
                    window.blit(black_queen, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Bishop:
                    window.blit(black_bishop, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Rook:
                    window.blit(black_rook, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Knight:
                    window.blit(black_knight, (100*(x-1), 100*(y-1)))
                elif type(arr[y-1][x-1])==Pawn:
                    window.blit(black_pawn, (100*(x-1), 100*(y-1)))
    pg.display.update()

class Queen(Piece):
    def find(self, board):
        available = []
        x, y = self.position
        for iy in range(y+1, 8):
            if not board[iy][x] or board[iy][x].color != self.color:
                pos = (x, iy)
                available.append(pos)
                if board[iy][x]:
                    break
            else:
                break

        for iy in range(y-1, -1, -1):
            if not board[iy][x] or board[iy][x].color != self.color:
                pos = (x, iy)
                available.append(pos)
                if board[iy][x]:
                    break
            else:
                break

        for ix in range(x+1, 8):
            if not board[y][ix] or board[y][ix].color != self.color:
                pos = (ix, y)
                available.append(pos)
                if board[y][ix]:
                    break
            else:
                break

        for ix in range(x-1, -1, -1):
            if not board[y][ix] or board[y][ix].color != self.color:
                pos = (ix, y)
                available.append(pos)
                if board[y][ix]:
                    break
            else:
                break

        for i in range(1, 8-y):
            ix = x+i
            iy = y+i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break

        for i in range(1, 8-y):
            ix = x-i
            iy = y+i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break

        for i in range(1, y+1):
            ix = x+i
            iy = y-i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break

        for i in range(1, y+1):
            ix = x-i
            iy = y-i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break
        return available

class Bishop(Piece):
    def find(self, board):
        available = []
        x, y = self.position
        for i in range(1, 8-y):
            ix = x+i
            iy = y+i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break

        for i in range(1, 8-y):
            ix = x-i
            iy = y+i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break

        for i in range(1, y+1):
            ix = x+i
            iy = y-i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break

        for i in range(1, y+1):
            ix = x-i
            iy = y-i
            if ix>=0 and iy>=0:
                try:
                    if not board[iy][ix] or board[iy][ix].color != self.color:
                        pos = (ix, iy)
                        available.append(pos)
                        if board[iy][ix]:
                            break
                    else:
                        break
                except IndexError:
                    break
            else:
                break
        return available

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.moved = False

    def setpos(self, x, y):
        super().setpos(x, y)
        self.moved = True

    def find(self, board):
        available = []
        x, y = self.position
        for iy in range(y+1, 8):
            if not board[iy][x] or board[iy][x].color != self.color:
                pos = (x, iy)
                available.append(pos)
                if board[iy][x]:
                    break
            else:
                break

        for iy in range(y-1, -1, -1):
            if not board[iy][x] or board[iy][x].color != self.color:
                pos = (x, iy)
                available.append(pos)
                if board[iy][x]:
                    break
            else:
                break

        for ix in range(x+1, 8):
            if not board[y][ix] or board[y][ix].color != self.color:
                pos = (ix, y)
                available.append(pos)
                if board[y][ix]:
                    break
            else:
                break

        for ix in range(x-1, -1, -1):
            if not board[y][ix] or board[y][ix].color != self.color:
                pos = (ix, y)
                available.append(pos)
                if board[y][ix]:
                    break
            else:
                break
        return available

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.sprint = True

    def setpos(self, x, y):
        super().setpos(x, y)
        self.sprint = False

    def find(self, board):
        available = []
        x, y = self.position
        if self.color == "white":
            if not board[y-1][x]:
                pos = (x, y-1)
                available. append(pos)
            try:
                if board[y-1][x-1].color and (board[y-1][x-1].color != self.color):
                    pos = (x-1, y-1)
                    available.append(pos)
            except (AttributeError, IndexError):
                pass
            try:
                if board[y-1][x+1].color and (board[y-1][x+1].color != self.color):
                    pos = (x+1, y-1)
                    available.append(pos)
            except (AttributeError, IndexError):
                pass
            try:
                if self.sprint and not board[y-2][x] and not board[y-1][x]:
                    pos = (x, y-2)
                    available.append(pos)
            except IndexError:
                pass

        elif self.color == "black":
            if not board[y+1][x]:
                pos = (x, y+1)
                available. append(pos)
            try:
                if board[y+1][x-1].color and (board[y+1][x-1].color != self.color):
                    pos = (x-1, y+1)
                    available.append(pos)
            except (AttributeError, IndexError):
                pass
            try:
                if board[y+1][x+1].color and (board[y+1][x+1].color != self.color):
                    pos = (x+1, y+1)
                    available.append(pos)
            except (AttributeError, IndexError):
                pass
            try:
                if self.sprint and not board[y+2][x] and not board[y+1][x]:
                    pos = (x, y+2)
                    available.append(pos)
            except IndexError:
                pass
        return available

class Knight(Piece):
    def find(self, board):
        available = []
        x, y = self.position
        try:
            if not board[y + 2][x + 1] or board[y + 2][x + 1].color != self.color:
                pos = (x + 1, y + 2)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y + 2][x - 1] or board[y + 2][x - 1].color != self.color:
                pos = (x - 1, y + 2)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y + 1][x + 2] or board[y + 1][x + 2].color != self.color:
                pos = (x + 2, y + 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 1][x + 2] or board[y - 1][x + 2].color != self.color:
                pos = (x + 2, y - 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y + 1][x - 2] or board[y + 1][x - 2].color != self.color:
                pos = (x - 2, y + 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 1][x - 2] or board[y - 1][x - 2].color != self.color:
                pos = (x - 2, y - 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 2][x - 1] or board[y - 2][x - 1].color != self.color:
                pos = (x - 1, y - 2)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 2][x + 1] or board[y - 2][x + 1].color != self.color:
                pos = (x + 1, y - 2)
                available.append(pos)
        except IndexError:
            pass
        return available

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.moved = False

    def setpos(self, x, y):
        super().setpos(x, y)
        self.moved = True

    def find(self, board):
        available = []
        x, y = self.position
        try:
            if not board[y + 1][x + 1] or board[y + 1][x + 1].color != self.color:
                pos = (x + 1, y + 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y][x + 1] or board[y][x + 1].color != self.color:
                pos = (x + 1, y)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 1][x + 1] or board[y - 1][x + 1].color != self.color:
                pos = (x + 1, y - 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 1][x] or board[y - 1][x].color != self.color:
                pos = (x, y - 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y - 1][x - 1] or board[y - 1][x - 1].color != self.color:
                pos = (x - 1, y - 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y][x - 1] or board[y][x - 1].color != self.color:
                pos = (x - 1, y)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y + 1][x - 1] or board[y + 1][x - 1].color != self.color:
                pos = (x - 1, y + 1)
                available.append(pos)
        except IndexError:
            pass

        try:
            if not board[y + 1][x] or board[y + 1][x].color != self.color:
                pos = (x, y + 1)
                available.append(pos)
        except IndexError:
            pass

        if not board[y][x].moved and not board[y][x+3].moved:
            if type(board[y][x+3])==Rook and not board[y][x+2] and not board[y][x+1] and type(board[y][x])==King and board[y][x+3].color==board[y][x].color:
                pos = (x+2, y)
                available.append(pos)

        if not board[y][x].moved and not board[y][x-4].moved:
            if type(board[y][x-4])==Rook and not board[y][x-3] and not board[y][x-2] and not board[y][x-1] and type(board[y][x])==King and board[y][x-4].color==board[y][x].color:
                pos = (x-2, y)
                available.append(pos)
        return available

out = create_board(starting_board)
print_board(out, window)
turn_white = True
while True:
    if Turn('white' if turn_white else 'black', out):
        turn_white = not turn_white