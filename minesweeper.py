import random
import termcolor #doesn't display properly in command prompt zzzzz
#HEIGHT IS LOOPED FIRST, THAN WIDTH
class Cell:

    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.nearby = 0
ANSWER_LENGTH = 2
class Grid:

    def __init__(self, width = 9, height = 9, mines = 9):
        x = input('Play default? Y/N: ')
        if x == 'Y':
            self.width = width
            self.height = height
            self.mines = mines
        else:
            self.width = int(input('Choose amount of columns in board: '))
            self.height = int(input('Choose amount of rows in board: '))
            self.mines = int(input('Choose amount of mines in board: '))
        self.cells_revealed_goal = (self.width * self.height) - self.mines
        self.contents = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Cell())
            self.contents.append(row)

    def place_mines(self):
        while self.mines > 0:
            x = random.randint(0,self.height-1)
            y = random.randint(0,self.width-1)
            if self.contents[x][y].is_mine == True:
                continue
            else:
                self.contents[x][y].is_mine = True
                self.contents[x][y].nearby = termcolor.colored('*','magenta')
                self.mines -= 1

    def check_nearby(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j].is_mine == True:
                    continue
                else:
                    for x in range(max(0,i-1),min(i+2,self.height)):
                        for y in range(max(0,j-1), min(j+2,self.width)):
                            if self.contents[x][y].is_mine == True:
                                self.contents[i][j].nearby += 1

    def print_board(self):
        print('\n'*40)
        flag = termcolor.colored('⚐','red')
        for i in range(self.height+1): #print da height first
            printed_cell = '|'
            for j in range(self.width+1):
                if i == 0 and j == 0:
                    printed_cell += '.|'
                    continue
                elif i == 0:
                    printed_cell += f'{chr(64+j)}|'
                elif j == 0:
                    printed_cell += f'{chr(64+i)}|'
                elif self.contents[i-1][j-1].is_revealed == True:
                    printed_cell += f'{self.contents[i-1][j-1].nearby}|'
                elif self.contents[i-1][j-1].is_flagged == True:
                    printed_cell += f'{flag}|'
                else:
                    printed_cell += ' |'
            print(printed_cell)

    def turn(self):
        coord_system = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16}
        while True:
            answer = input("Choose a coordinate to reveal (format = row+column (inputing AB will reveal row A, col B)). Put 'f' after your answer to flag/unflag column. ")
            try:
                row = coord_system[answer[0].upper()] - 1
                col = coord_system[answer[1].upper()] - 1
            except KeyError:
                print('Please select a coordinate within the range.')
                continue
            except IndexError:
                print('Please select a coordinate within the range.')
                continue
            if len(answer) != ANSWER_LENGTH and answer[2] != 'f':
                print('Please select a coordinate within the range.')
                continue
            if row >= self.height or col >= self.width:
                print('Please select a coordinate within the range.')
                continue
            if self.contents[row][col].is_flagged == True and len(answer) == 2:
                print("Cannot reveal a flagged cell.")
                continue
            if len(answer) > 2 and answer[2] == 'f' and self.contents[row][col].is_flagged == False:
                self.contents[row][col].is_flagged = True
                break
            elif len(answer) > 2 and answer[2] == 'f' and self.contents[row][col].is_flagged == True:
                self.contents[row][col].is_flagged = False
                break
            else:
                self.contents[row][col].is_revealed = True
                break

    def reveal_empty_adjacents(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j].is_revealed == True and self.contents[i][j].nearby == 0:
                    for x in range(max(0,i-1),min(i+2,self.height)):
                        for y in range(max(0,j-1), min(j+2,self.width)):
                            if self.contents[x][y].is_revealed == False:
                                self.contents[x][y].is_revealed = True
                                if self.contents[x][y].nearby == 0:
                                    self.reveal_empty_adjacents()

    def total_reveal(self):
        for i in range(self.height):
            for j in range(self.width):
                self.contents[i][j].is_revealed = True
        self.print_board()

    def game_end(self):
        for i in range(self.height):
            for j in range(self.width):               
                if self.contents[i][j].is_mine and self.contents[i][j].is_revealed == True:
                    self.total_reveal()
                    print('You lost')
                    return True
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j].is_mine == False and self.contents[i][j].is_revealed == True:
                    count += 1
        if count == self.cells_revealed_goal:
            print('You win!')
            return True
        return False

    def restart_game(self):
        x = input('(Input Y to try again): ')
        return x.upper() == 'Y'

def main():
    while True:
        g = Grid()
        g.place_mines()
        g.check_nearby()
        while g.game_end() == False:
            g.print_board()
            g.turn()
            g.reveal_empty_adjacents()
        if not g.restart_game():
            break

if __name__ == '__main__':
    main()