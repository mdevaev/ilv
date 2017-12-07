class Cell():
    def __init__(self, x, y, live=True):
        self.x, self.y = x, y
        self.live = live
        self.around = 0

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def spawn(self):
        self.live = True
        self.around = 0
        return self

class Grid():
    def __init__(self, width, height, screen):
        self.screen = screen
        self.xMax = width
        self.yMax = height
        self.cells = []
        self.deltas = [(-1, -1), (0, -1), (1, -1), (1, 0),
                      (1, 1), (0, 1), (-1, 1), (-1, 0)]

    def tick(self):
        newCells = self.cells[:]
        ''' create potential new cells '''
        for cell in self.cells:
            for dx, dy in self.deltas:
                newCell = Cell((cell.x+dx)%self.xMax,
                               (cell.y+dy)%self.yMax, live=False)
                if newCell not in newCells:
                    newCells.append(newCell)
                newCells[newCells.index(newCell)].around += 1
        ''' spawn new cells for next grid '''
        self.cells = []
        for cell in newCells:
            if (cell.live and cell.around in [2, 3]
            or not cell.live and cell.around == 3):
                self.cells.append(cell.spawn())

    def show(self):
        (image, draw) = make_image()
        for y in range(self.yMax):
            for x in range(self.xMax):
                draw.point((x, y), (255 if Cell(x, y) in self.cells else 0))
        self.screen.send(image)
#        for y in range(self.yMax):
#            print(''.join(
#                        ('X|' if Cell(x, y) in self.cells else ' |') for x in range(self.xMax)))
#        print()


from ilv import Screen, make_image

screen = Screen("/dev/ttyACM0")
screen.set_enabled()


glider = [Cell(2,0), Cell(2,1), Cell(2,2), Cell(1,2), Cell(0,1)]
g = Grid(95, 23, screen)
g.cells = glider
import time
while True:
    g.show()
    g.tick()
    time.sleep(0.1)
