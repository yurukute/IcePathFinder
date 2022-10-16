from random import sample
import queue


class IceMaze:
    def __init__(self, row=0, col=0, rock_num=0, snow_num=0):
        self.__row = row
        self.__col = col
        self.__map = [[' ']*col for i in range(row)]
        pos = [i for i in range(row*col)]
        rocks = sample(pos, rock_num)
        snows = sample([i for i in pos if i not in rocks], snow_num)
        for i in rocks:
            self.__map[i // col][i % col] = '#'
        for i in snows:
            self.__map[i // col][i % col] = 'x'
        [start, end] = sample([i for i in pos if
                               i not in rocks and
                               i not in snows], 2)
        self.__map[start // col][start % col] = 'S'
        self.__map[end // col][end % col] = 'E'
        self.__start = start

    def read_maze(strmap):
        if strmap[len(strmap)-1] == '\n':
            strmap = strmap[:-1]
        col = max(len(i) for i in strmap.split('\n'))
        row = len(strmap.split('\n'))
        maze = IceMaze(row, col)
        i, j = 0, 0
        for c in strmap:
            if c == 'S':
                maze.__start = i*row + j
            if c != '\n':
                maze.__map[i][j] = c
                j += 1
            else:
                i, j = i+1, 0
        return maze

    def next_tile(self, curr, DIR):
        next = curr
        while(self.__map[curr // self.__col][curr % self.__col] != 'E'):
            if DIR == 'UP' and curr >= self.__col:
                next = curr - self.__col
            elif DIR == 'DOWN' and curr < (self.__row - 1)*self.__col:
                next = curr + self.__col
            elif DIR == 'LEFT' and curr % self.__col != 0:
                next = curr - 1
            elif DIR == 'RIGHT' and (curr+1) % self.__col != 0:
                next = curr + 1
            else:
                break
            tile = self.__map[next // self.__col][next % self.__col]
            if tile == '#':
                return curr
            elif tile == 'x':
                return next
            curr = next
        return next

    def update_result(self, result, parent, curr):
        new_path = []
        while parent[curr] != -1:
            new_path.insert(0, curr)
            curr = parent[curr]
        new_path.insert(0, curr)
        if len(result) == 0 or len(new_path) < len(result):
            return new_path
        return result

    def bfs(self):
        result = []
        mark = [0]*self.__row*(self.__col+1)
        parent = [-1]*self.__row*(self.__col+1)
        Queue = queue.Queue()
        Queue.put(self.__start)
        col = self.__col
        while not Queue.empty():
            curr = Queue.get()
            if(self.__map[curr // col][curr % col] == 'E'):
                result = self.update_result(result, parent, curr)
                continue
            mark[curr] = 1
            for DIR in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                next = self.next_tile(curr, DIR)
                if (next != curr and next != parent[curr] and
                        not mark[next] and parent[next] == -1):
                    parent[next] = curr
                    Queue.put(next)
        return result

    def dfs(self):
        result = []
        mark = [0]*self.__row*(self.__col+1)
        parent = [-1]*self.__row*(self.__col+1)
        Stack = queue.LifoQueue()
        Stack.put(self.__start)
        col = self.__col
        while not Stack.empty():
            curr = Stack.get()
            if(self.__map[curr // col][curr % col] == 'E'):
                result = self.update_result(result, parent, curr)
                continue
            mark[curr] = 1
            for DIR in reversed(['UP', 'DOWN', 'LEFT', 'RIGHT']):
                next = self.next_tile(curr, DIR)
                if (next != curr and next != parent[curr] and
                        not mark[next] and parent[next] == -1):
                    parent[next] = curr
                    Stack.put(next)
        return result

    def print(self):
        for i in range(self.__row):
            for j in range(self.__col):
                print(self.__map[i][j], end='')
            print()

    def get_map(self):
        return self.__map
