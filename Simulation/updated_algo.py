import time
import math
import itertools


Row     =   10
Column  =   10

Obstacles   =   [[4,8],[6,8], [9,7], [0,6], [3,5], [6,5], [9,5], [0,4], [6,4], [0,3], [3,3], [9,3], [6,2 ],[0,1], [9,1], [0,0], [1,0], [2,0], [7,0], [8,0], [9,0], [7,8], [2,8], [3,8], [5,8], [0,7], [3,6], [6,6], [9,6], [0,5], [3,4], [9,4], [6,3], [0,2], [3,2], [9,2]]
Products    =   [[5,0],[2,4],[3,9],[2,2],[2,6],[8,4],[1,5],[2,7],[5,7],[4,2],[4,4],[5,3],[7,6],[8,6],[6,1]]

route_map   =   []
cost_map    =   []
Visited     =   []


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


def generate_cost_map():
    
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


def get_route(minimum_path):
    route=[]
    
    for item in range(0,len(minimum_path)-1):
        route.append(route_map[item][item+1])
        route[-1].pop(0)
        
    return route


def main():
    generate_cost_map()
    minimum_distance , minimum_path = shortest_path(cost_map)
    print(minimum_distance , minimum_path)
  
    
if __name__=='__main__':
    main()