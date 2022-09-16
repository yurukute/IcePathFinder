from random import sample
import queue


class IceMaze:
    def __init__(self, row=0, col=0, rock_num=0, snow_num=0):
        self.__row = row
        self.__col = col
        self.__map = [' ']*row*(col+1)
        endrow = [i for i in range(col, row*(col+1), (col+1))]
        for i in endrow:
            self.__map[i] = '\n'
        pos = [i for i in range(row*(col+1)) if i not in endrow]
        rocks = sample(pos, rock_num)
        snows = sample([i for i in pos if i not in rocks], snow_num)
        for i in rocks:
            self.__map[i] = '#'
        for i in snows:
            self.__map[i] = 'x'
        [start, end] = sample([i for i in pos if
                               i not in rocks and
                               i not in snows], 2)
        self.__map[start] = 'S'
        self.__map[end] = 'E'
        self.__start = start

    def read_maze(strmap):
        col = strmap.find('\n')
        row = (len(strmap)+1)//(col+1)
        maze = IceMaze(col, row)
        maze.__map = strmap
        maze.start = strmap.find('S')
        return maze

    def next_tile(self, curr, DIR):
        next = curr
        while(self.__map[curr] != 'E'):
            if DIR == 'UP' and curr > self.__col:
                next = curr - (self.__col+1)
            elif DIR == 'DOWN' and curr < len(self.__map) - self.__col:
                next = curr + (self.__col+1)
            elif DIR == 'LEFT' and curr % (self.__col+1) != 0:
                next = curr - 1
            elif DIR == 'RIGHT' and (curr+2) % (self.__col+1) != 0:
                next = curr + 1
            else:
                break
            if self.__map[next] == '#':
                return curr
            if self.__map[next] == 'x':
                return next
            curr = next
        return next

    def update_result(self, result, parent, curr):
        new_path = []
        while parent[curr] != -1:
            if (parent[curr] - curr) % (self.__col+1) == 0:
                new_path.append('u' if parent[curr] > curr else 'd')
            else:
                new_path.append('l' if parent[curr] > curr else 'r')
            curr = parent[curr]
        new_path.reverse()
        if len(result) == 0 or len(new_path) < len(result):
            return new_path
        else:
            return result

    def ice_path_finder(self):
        result = []
        mark = [0]*self.__row*(self.__col+1)
        parent = [-1]*self.__row*(self.__col+1)
        Queue = queue.Queue()
        Queue.put(self.start)
        while not Queue.empty():
            curr = Queue.get()
            mark[curr] = 1
            if(self.__map[curr] == 'E'):
                result = self.update_result(result, parent, curr)
                return result
            for DIR in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                next = self.next_tile(curr, DIR)
                if (next != curr and next != parent[curr] and
                        not mark[next] and parent[next] == -1):
                    parent[next] = curr
                    Queue.put(next)

    def print(self):
        for i in range(self.__row):
            for j in range(self.__col):
                print(self.__map[i*(self.__col+1)+j], end='')
            print()

    def get_info(self):
        return [self.__row, self.__col, self.__map]

    def get_col(self):
        return self.__col
