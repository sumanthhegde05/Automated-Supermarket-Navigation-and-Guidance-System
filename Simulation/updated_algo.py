import time
import math
import itertools
start_time = time.time()
Row=10
Column=10

route_map=[]
cost_map=[]
Obstacles=[[4 ,8],[6, 8], [9 ,7], [0 ,6], [3, 5], [6 ,5], [9 ,5], [0 ,4], [6 ,4], [0 ,3], [3, 3], [9 ,3], [6 ,2 ],[0 ,1], [9 ,1], [0, 0], [1 ,0], [2 ,0], [7, 0 ],[8, 0 ],[9 ,0 ],[7 ,8 ],[2,8], [3,8], [5,8], [0,7], [3,6], [6,6], [9,6], [0,5], [3,4], [9,4], [6,3], [0,2], [3,2], [9,2]]
Products = [[5,0],[2,4],[3,9],[2,2],[2,6],[8,4],[1,5],[2,7],[5,7],[4,2],[4,4],[5,3],[7,6],[8,6],[6,1]]
Visited=[]

def is_valid(cell):
    if cell in Obstacles or cell in Visited or cell[0]>=Column or cell[0]<0 or cell[1]>=Row or cell[1]<0 :
        return False
    else:
        return True

def find_neoghbpurs(cell):
    temp=[]
    valid_neighbours=[]
    for offset in range  (-1,2):
        if offset !=0:
            temp.append([])
            temp[-1].append(cell[0]+offset)
            temp[-1].append(cell[1])
    for offset in range  (-1,2):
        if offset !=0:
            temp.append([])
            temp[-1].append(cell[0])
            temp[-1].append(cell[1]+offset)
    for item in temp:
        if is_valid(item):
            valid_neighbours.append(item)
    return valid_neighbours

def algo(start,end):
    Queue=[]
    path=[]
    Queue.append([])
    Queue[-1].append(start)
    while len(Queue)!=0:
        path = Queue.pop(0)
        neighbours = find_neoghbpurs(path[-1])
        Visited.append(path[-1])
        for neighbour in neighbours:
            temp = path.copy() 
            temp.append(neighbour)
            Queue.append(temp)
        if temp[-1]==end:
            break
    return temp

for start in range (0,len(Products)):
    route_map.append([])
    cost_map.append([])
    for end in range (0,len(Products)):
        if start!=end:
            #print('entry',Products[start],Products[end])
            route_map[start].append(algo(Products[start],Products[end]))
            cost_map[start].append(len(route_map[start][end]))
            del Visited[:]
        else:
            route_map[start].append([])
            cost_map[start].append(0)

#print(route_map[0])
#print(cost_map)

def shortest_path(cost_map):
    n = len(cost_map)
    n-=1
    cost_dict = {}
    for k in range(1, n):
        cost_dict[(1 << k, k)] = (cost_map[0][k], 0)

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            for k in subset:
                prev = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((cost_dict[(prev, m)][0] + cost_map[m][k], m))
                cost_dict[(bits, k)] = min(res)
    bits = (2**n - 1) - 1
    res = []
    for k in range(1, n):
        res.append((cost_dict[(bits, k)][0] + cost_map[k][n], k ))
    opt, parent = min(res)
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = cost_dict[(bits, parent)]
        bits = new_bits
    path.append(0)
    ret_path = list(reversed(path))
    ret_path.append(n)
    return opt, ret_path

minimum_distance , minimum_path = shortest_path(cost_map)
#print(minimum_distance , minimum_path)
print("--- %s seconds ---" % (time.time() - start_time))

'''adj = [[0, 8, 16, 6, 10, 8, 10, 11, 8, 4, 6, 4, 9, 10, 3], 
        [8, 0, 9, 3, 3, 13, 3, 4, 13, 7, 9, 9, 10, 13, 13], 
        [16, 9, 0, 11, 7, 11, 7, 17, 17, 13, 11, 13, 10, 9, 16], 
        [6, 3, 11, 0, 5, 11, 5, 6, 15, 5, 7, 7, 12, 13, 15], 
        [10, 3, 7, 5, 0, 11, 13, 2, 13, 9, 7, 9, 8, 13, 13], 
        [8, 13, 11, 11, 11, 0, 13, 10, 7, 9, 11, 9, 4, 3, 6], 
        [10, 14, 7, 5, 3, 13, 0, 4, 14, 9, 9, 11, 10, 14, 14], 
        [11, 4, 6, 6, 2, 10, 4, 0, 13, 8, 6, 8, 7, 13, 13],
        [8, 7, 9, 9, 5, 7, 7, 4, 0, 7, 5, 5, 4, 11, 11],
        [4, 7, 13, 5, 9, 9, 9, 8, 7, 0, 3, 3, 10, 11, 15],
        [6, 9, 11, 7, 7, 11, 9, 6, 5, 3, 0, 13, 8, 13, 13], 
        [4, 9, 13, 7, 9, 9, 11, 8, 5, 14, 3, 0, 8, 14, 14], 
        [9, 10, 10, 12, 8, 4, 10, 7, 4, 10, 8, 8, 0, 13, 13], 
        [10, 11, 9, 13, 9, 3, 11, 8, 5, 11, 9, 9, 14, 0, 8], 
        [3, 8, 16, 6, 10, 6, 10, 11, 8, 4, 6, 4, 7, 8, 0]]'''

route=[]
for item in range(0,len(minimum_path)-1):
    route.append(route_map[item][item+1])
    route[-1].pop(0)
print(route)
