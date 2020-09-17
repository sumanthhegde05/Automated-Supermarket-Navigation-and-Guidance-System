from collections import deque
import turtle
import random
import socket
import time
import math
#import RPi.GPIO as GPIO
from itertools import permutations 
import socket
import time
from threading import *
import threading
import sys
from PIL import Image, ImageDraw, ImageFont

scale=100
only_obstacles=[]
obstacles=[]
trolleys=[]
start=[]
billing=[]
inc=-1
file = open("buffer.txt","r")
data=[]
for each in file:
    data.append(each.strip('\n'))
temp = data[0].split(' ')
row = int(temp[0])
column = int(temp[1] )
Products = data[1].split(' ')
Position = data[2].split(' ')
Obstacles = data[3].split(' ')
start_string = data[4].split(' ')
billing_string = data[5].split(' ')
trolley = data[6].split(' ')
count=0
for item in start_string:
    if item == '':
        pass
    else:
        start.append(int(item))
for item in billing_string:
    if item == '':
        pass
    else:
        billing.append(int(item))
for item in trolley:
    if item=='':
        pass
    elif count%2==0:
        trolleys.append([])
        trolleys[-1].append(int(item))
    else:
        trolleys[-1].append(int(item))
    count+=1
print('billing',billing)
print('start',start)
print('trolleys',trolleys)

file.close()
def design(row,column,scale,Products,Position,Obstacles,start,billing):
    details={}
    for item in range(0,len(Products)):
        if Products[item]=='':
            pass
        else:
            details[Products[item]]=Position[item]
    print(details)
    img = Image.new('RGB', (column*scale,row*scale), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    startx=0
    starty=0
    endx=0
    endy=0
    for i in range(0,row):
        startx=0
        starty=i*scale
        endx=column*scale
        endy=i*scale
        shape = [startx,starty,endx,endy] 
        d.line(shape, fill ="black", width = 2)
        for j in range(0,column):
            startx=j*scale
            starty=0
            endx=j*scale
            endy=row*scale
            shape = [startx,starty,endx,endy] 
            d.line(shape, fill ="black", width = 2)

    for items in Products:
        if items in details:
            value = details[items]
            startx= int(value[1])*scale
            starty= row*scale-(int(value[3])*scale)-scale
            endx= startx+scale
            endy= starty+scale
            shape = [startx,starty,endx,endy] 
            d.rectangle(shape, fill ="orange", outline="black",width=2)

    startx= int(start[0])*scale
    starty= row*scale-(int(start[1])*scale)-scale
    endx= startx+scale
    endy= starty+scale
    shape = [startx,starty,endx,endy] 
    d.rectangle(shape, fill ="green", outline="black",width=2)
    d.text((startx+(scale/4),starty+scale/2),  'Entry' ,fill="Black", font=ImageFont.truetype("arial",14))

    startx= int(billing[0])*scale
    starty= row*scale-(int(billing[1])*scale)-scale
    endx= startx+scale
    endy= starty+scale
    shape = [startx,starty,endx,endy] 
    d.rectangle(shape, fill ="green", outline="black",width=2)
    d.text((startx+(scale/4),starty+scale/2),  'Billing' ,fill="Black", font=ImageFont.truetype("arial",14))
    inc=0
    for item in Obstacles:
        if item=='':
            pass
        elif inc%2==0:
            only_obstacles.append([])
            only_obstacles[-1].append(int(item))
            
        else:
            only_obstacles[-1].append(int(item))
        inc+=1
    print("only",only_obstacles)    
        #[[0,1],[0,2],[0,4],[0,5],[0,6],[0,7],[2,9],[3,9],[4,9],[5,9],[6,9],[8,9],[9,9],[9,8],[9,7],[9,6],[9,5],[9,4],[9,2],[9,1],[3,3],[3,4],[3,6],[6,3],[6,5],[6,6],[5,0],[6,4],[3,2]]
    for obstacle in only_obstacles:
        startx= int(obstacle[0])*scale
        starty= row*scale-int((obstacle[1])*scale)-scale
        endx= startx+scale
        endy= starty+scale
        shape = [startx,starty,endx,endy] 
        d.rectangle(shape, fill ="orange", outline="black",width=2)    

    for item in trolleys:
        startx= int(item[0])*scale
        starty= row*scale-int((item[1])*scale)-scale
        endx= startx+scale
        endy= starty+scale
        shape = [startx,starty,endx,endy] 
        d.rectangle(shape, fill ="#45b6fe", outline="black",width=2)  
        d.text((startx+(scale/4),starty+scale/2),  'Trolley' ,fill="Black", font=ImageFont.truetype("arial",14))
    for items in Products:
        if items in details:
            value = details[items]
            obstacles.append([])
            obstacles[-1].append(int(value[1]))
            obstacles[-1].append(int(value[3]))
            startx= int(value[1])*scale
            starty= row*scale-(int(value[3])*scale)-scale
            endx= startx+scale
            endy= starty+scale
            shape = [startx,starty,endx,endy] 
            if value[5]=='L':
                d.text((startx+5,starty+int(scale/2)-5), items,fill="Black", font=ImageFont.truetype("arial",12,))
                d.text((startx+(scale/2)-5,starty+int(scale/2)-10),  '|' ,fill="Black", font=ImageFont.truetype("arial",22))
            elif value[5]=='R':
                d.text((startx+(scale/2),starty+int(scale/2)-5),  items ,fill="Black", font=ImageFont.truetype("arial",12))
                d.text((startx+(scale/2)-5,starty+int(scale/2)-10),  '|' ,fill="Black", font=ImageFont.truetype("arial",22))
            elif value[5]=='D':
                d.text((startx+(scale/4),starty+int(scale-20)),  items ,fill="Black", font=ImageFont.truetype("arial",14))
            else:
                d.text((startx+(scale/4),starty+10),  items ,fill="Black", font=ImageFont.truetype("arial",14))
    
    img.save('background.png')

design(row,column,scale,Products,Position,Obstacles,start,billing)


path=""



class tcp(Thread): #class of thread
    def run(self): #Automatically called when you thread.start() is mentioned.
        global message 
        global address
        (clientsocket, address) = listensocket.accept()
        #print("New connection made!",address)
        message = clientsocket.recv(1024).decode() #Receives Message    

    def kill(self):
        print("Killed")
        self.killed = True 
p=0
turtle.shape("circle")
s = turtle.Screen()
s.setup(column*scale+50 , row*scale+50 , 0 , 0)
s.bgpic('background.png')
turtle.penup()
turtle.goto(-(((column*scale//2)-scale//2-(start[0]*scale))),-(((row*scale//2)-scale//2)-(start[1]*scale)))

turtle.pendown()
turtle.listen()
dist = 100
def up():
    turtle.setheading(90)
    turtle.forward(dist)
    print("UP")

def down():
    turtle.setheading(270)
    turtle.forward(dist)
    print("Down")
def left():
    turtle.setheading(180)
    turtle.forward(dist)
    print("Left")
def right():
    turtle.setheading(0)
    turtle.forward(dist)
    print("Right")

def action(z):
    print("z",z)
    global v
    global s
    #left
    if z[0] is 1 and z[1] is 0 and s is 2:
        right()
    #down
    elif z[0] is 0 and z[1] is 1 and s is 2:
        up()
    #forward
    elif z[0] is -1 and z[1] is 0 and s is 2:
        left()

    #right
    elif z[0] is 0 and z[1] is -1 and s is 2:
        down()


def isValid(point):
    if int(point[0])>=0 and int(point[0])<column and int(point[1])>=0 and int(point[1])<row:
        return True
    else:
        return False

def calculate(point,visited):
    ret_list=[]
    #print("point=",point)
    for i in range (-1,2):      
        if isValid([int(point[0])+i,int(point[1])]) and [int(point[0])+i,int(point[1])] not in visited and i!=0 and [int(point[0])+i,int(point[1])] not in obstacles:
            ret_list.append([int(point[0])+i,int(point[1])])
    for i in range (-1,2): 
        if isValid([int(point[0]),int(point[1])+i]) and [int(point[0]),int(point[1])+i] not in visited and i!=0 and [int(point[0]),int(point[1])+i] not in obstacles:
            ret_list.append([int(point[0]),int(point[1])+i])
    return ret_list

def run(start,end):
    visited=[]
    paths=[]
    del visited[:]
    del paths[:]
    path=str(start[0])+str(start[1])
    paths.append(path)
    j=0
    #print('start=',start)
    #print('end=',end)
    while True :
        flag=True
        j+=1
        #print("loop",j)
        path=paths.pop(0)
        #print("Path=",path)
        visited.append([])
        visited[-1].append(int(path[-2]))
        visited[-1].append(int(path[-1]))
        start = visited[-1]
        neighbours = calculate(start,visited)
        #print("neighbours=",neighbours)
        #print("visited=",visited)
        for i in range(0,len(neighbours)):
            val=path+str(neighbours[i][0])+str(neighbours[i][1])
            paths.append(val)
            if neighbours[i]==end:
                flag=False
                break
        if flag==False:
            break
    return paths[-1]

rem_goals=[]
Details={}
for item in range(0,len(Products)):
    if Products[item]!='' and Position[item][-1]=='L':
        tempx=int(Position[item][1])
        tempy=int(Position[item][3])
        tempx-=1
        Details[Products[item]]=str(tempx)+","+str(tempy)
    elif Products[item]!='' and Position[item][-1]=='R':
        tempx=int(Position[item][1])
        tempy=int(Position[item][3])
        tempx+=1
        Details[Products[item]]=str(tempx)+","+str(tempy)
    elif Products[item]!='' and Position[item][-1]=='D':
        tempx=int(Position[item][1])
        tempy=int(Position[item][3])
        tempy-=1
        Details[Products[item]]=str(tempx)+","+str(tempy)
    elif Products[item]!='' and Position[item][-1]=='U':
        tempx=int(Position[item][1])
        tempy=int(Position[item][3])
        tempy+=1
        Details[Products[item]]=str(tempx)+","+str(tempy)
Details['billing']=str(billing[0])+","+str(billing[1])
print(Details)
'''Details={
    'Masks':'4,1',
    'Fruits':'1,3',
    'Milk':'0,9',
    'Cream':'3,8',
    'Juice':'7,8',
    'Books':'2,5',
    'Pens':'4,5',
    'Tissue':'5,3',
    'Soaps':'7,3',
    'Sweets':'5,2',
    'Spices':'8,3',
    'Coffee':'7,5',
    'billing':str(column-1)+',0'
}'''
    
def algo(rem_goals,initial_co):

    start_time = time.time()
    perm = permutations(rem_goals)
    perm_set=[]
    for i in list(perm):     
        perm_set.append(list(i))
    for i in range(0,len(perm_set)):
        if billing not in perm_set[i]:
            perm_set[i].append(billing)
    print("perm=",len(perm_set))
    return_path=[]
    count=0
    minn=100
    result=[]
    el=0
    for goals in perm_set:
        start=initial_co
        el+=1
        if el%1000==0:
            print(el)
        #print("res=",len(goals))
        for goal in goals:

            end=goal
            value=run(start,end)
            return_path.append(value)
            count+=len(value)
            start=end
        if count<minn:
            print(count)
            #print(return_path)
            minn=count
            result = return_path[:]
        del return_path[:]
        count=0
    print("--- %s seconds ---" % (time.time() - start_time))
    final_path=[]
   
    for item in range(0,len(result)):
        final_path.append([])
        for each in range (0,len(result[item])):
            if each%2==0:
                final_path[item].append([])
                final_path[item][-1].append(int(result[item][each]))
                final_path[item][-1].append(int(result[item][each+1]))
        final_path[item].pop(0)
    return final_path

list1=[]
list2=[]
list3=[]
list4=[]
back=[]
def Convert(string): #A function to convert recieved string to a list
    li = list(string.split(" ")) 
    return li


def get_goals(message):
    global short_path
    global list1
    global list2
    global list3
    global list4
    
    print(message)

    list1 = Convert(message)

    list2.append(list1[0][1:]) #list1 would be in char format

    #print(list1[0])
    #list2.append(int(list1[0][1])) #Excluding the first character({)

    for i in range(1, len(list1)): #conversion of char to int
        #print(list1[i])
        list2.append(list1[i])
    print(list2)
    j=0
    for i in range (0,int((len(list2)))): #Converting the list of numbers to corresponding co-ordinates
        list3.append([])
        list3[i].append(int(Details[list2[i]][0]))
        list3[i].append(int(Details[list2[i]][2]))
   
    print(list3) #list containing all the co-ordinate of respective goals
    
    for i in range(0,len(list3)):
        if list3[i] in visited_goals:
            continue
        list4.append(list3[i])
    return list4

flag=True
flag3=True
message = ''

flag4 = True
back=[]
short_path=[]
z=[0,0]
current=[0,0]
v=2
s=2
v=2 #v and s are the variables used hold the track of the direction
s=2
listensocket = socket.socket()
Port = 7989
maxConnections = 999
IP = socket.gethostname() #Gets Hostname Of Current Machine
listensocket.bind(('',Port)) #binds to the given port number 
listensocket.listen(maxConnections) #Accepts Incomming Connection
print("Server started at " + IP + " on port " + str(Port))
#Imports Modules

while True:
    for item in only_obstacles:
        obstacles.append(item)
    for item in trolleys:
        obstacles.append(item)
    (clientsocket, address) = listensocket.accept()
    print("New connection made!") 
    message = clientsocket.recv(1024).decode() #Receives Message
    print("Client message : "+message) #Prints Message
    if(message=='9696'):
       clientsocket.send(bytes('1\n','utf-8'))
       print("Authenticated")
       break
    else:
       clientsocket.send(bytes('2\n','utf-8'))
       print("Not authenticated")

visited_goals=[]
entry=True
Running=True
while Running:
    inc=0
    if flag==True:
        t1=tcp()
        t1.start()
        t1.join()
        del(t1)
        #
        initial_co=start
        z=[0,0]
    print(message)
    if message[0] == '{':
        print("Enters")
        if flag == True:
            original = message
            rem_goals=get_goals(message)
            #print("visited=",visited)
            short_path=algo(rem_goals,start)
        else:
            pass
        t2=tcp()
        t2.start()
        x=0
        print(short_path)
        while x<len(short_path):
            #print('x',x)
            #print("Entered")            
            while True:
                turtle.stamp()
                print(threading.enumerate())                
                t2.join()       
                if message == 'next':
                    entry=True       
                    t2=tcp()                
                    t2.start()
                    del back[:]
                    #print(display[inc]+' ->',end=" ")
                    break
                elif message == 'billing':
                    flag3=False
                    break
                elif message == 'abort':
                    print("Mission Aborted")
                    sys.exit(0)
                elif message == 'return' and len(back)!=0:
                    x-=1
                    visited_goals.pop()
                    break
                elif message[0]=='{' and entry==True:
                    
                    original = original+" "+message[1:]
                    print("message",original)

                    break
                
                else:   
                    break

            if flag3==False:
                #print(display[-1]+' ->',end=" ")
                message='{billing'
                del list1[:]
                del list2[:]
                del list3[:]
                del list4[:]
                #print('Billing'+' ->',end=" ")
                #print("visited",visited)
                del rem_goals[:]
                rem_goals=get_goals(message)
                print("bill=",rem_goals)
                #print("visited=",visited)
                short_path=algo(rem_goals,initial_co)
                flag=False
                x=0

            if message[0]=='{' and flag3==True and entry==True:
                entry=False
                del list1[:]
                del list2[:]
                del list3[:]
                del list4[:]
                #print("visited",visited)
                rem_goals=get_goals(original)
                print("After addition",rem_goals)
                short_path = algo(rem_goals,initial_co)
                print("short",short_path)
                flag=False
                x=0
                break
            for y in range (0,len(short_path[x])):
                #print("Entered")    
                if message =='stop':
                    while True:
                        print('Stopped'+' ->',end=" ")
                        t2=tcp()
                        t2.start()
                        #print("before",threading.enumerate())
                        t2.join()
                        #print("after",threading.enumerate())
                        if message=='resume':
                            t2=tcp()                
                            t2.start()
                            print('Resumed'+' ->',end=" ")
                            break
                elif message == 'abort':
                    print('Mission aborted'+' ->',end=" ")
                    sys.exit(0) 
    
                elif message == 'return' and flag4 == True and len(back)!=0:
            
                    #print(display[inc]+' ->',end=" ")
                    flag4 = False
                    back.reverse()
                    back.append(short_path[x-1][-1])
                    initial_co[0]=back[0][0]    
                    initial_co[1]=back[0][1]
                    #print("Reverse path", back)
                    for d in range (0,len(back)):
                        #print("loop:",d)
                        z[0]=back[d][0]-initial_co[0]
                        z[1]=back[d][1]-initial_co[1]
                        initial_co[0]=back[d][0]
                        initial_co[1]=back[d][1]
                        #print("z=",z)
                        #print("initial coordinate=",initial_co)
                        action(z)

                        

                elif message=='next'  or message=='resume' or message=='billing' or message=='{':
                    if t2.is_alive()==False:
                        t2=tcp()
                        t2.start()
                
                    
                if flag4 == False:
                    iinitial_co = back[-1]
                    message=' '  
                    del back[:]       
                    break
                            
                #print("loop:",y)
                z[0]=short_path[x][y][0]-initial_co[0]
                z[1]=short_path[x][y][1]-initial_co[1]
                initial_co[0]=short_path[x][y][0]
                initial_co[1]=short_path[x][y][1]
                back.append(short_path[x][y])
                #print("z=",z)
                #print("initial coordinate=",initial_co)
                action(z)

            #tcpsend()

            if flag4 ==True:         
                visited_goals.append(short_path[x][-1])
                #print (visited)
                x+=1
                if x==len(short_path):
                    Running=False
            elif flag4 ==False:
                t2=tcp()
                t2.start()
                flag4 = True
    


turtle.mainloop()
