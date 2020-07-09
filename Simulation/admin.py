from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

#class layouot_button():
#   def __init__(self):
global Column
global Row
Column=0
Row=0
Products=[]
Position=[]
Obstacles=[]
d=[]

main = Tk()
main.geometry("1900x950")

v = StringVar()
value=StringVar()
pos_value = StringVar() 
Yaxis = StringVar()
Xaxis = StringVar()

flag=False
def call_frame():
    if flag==True:
        frame=Frame(main,relief=GROOVE,width=800,height=850,bd=1,bg="cyan")
        frame.place(x=600,y=200)
        return frame
    else:
        frame=Frame(main,relief=GROOVE,width=700,height=400,bd=1,bg="cyan")
        frame.place(x=600,y=200)
        return frame

selection_position = {
    '0':'U',
    '1':'D',
    '2':'L',
    '3':'R'
}

class layout_button():
    product_name=''
    product_position=''
    obst_position=''
    myframe=call_frame()
    myframe.destroy()
    x=0
    y=0
    def __init__(self,myframe,posx,posy):
        myframe=myframe
        self.x=posx
        self.y=posy
        self.b = Button(myframe,width=8,height=4,bg="white")
        self.b.grid(row=self.x,column=self.y)
        self.b.configure(command=self.highlight)
        #print(self.x,self.y)
    
    def entry(self):
        size = self.product_name.split(' ')
        if len(size)>2:
            pass
        else:
            temp1 = value.get()+selection_position[pos_value.get()]+' '
            temp2 = selection_position[pos_value.get()]
            if self.product_name!='':
                self.product_name = self.product_name+temp1
                self.product_position = self.product_position +" "+'['+str(self.y)+','+str(Column-self.x)+']'+temp2
            else:
                self.product_name = temp1
                self.product_position='['+str(self.y)+','+str(Column-self.x)+']'+temp2
            
        self.b.configure(text=self.product_name,anchor='w')        

    def erase(self):
        self.product_name=''
        self.product_position=''
        self.obst_position=''
        self.b.configure(text=self.product_name,anchor='n')
        
    def obst(self):
        self.product_name=''
        self.product_position=''
        self.obst_position='['+str(self.y)+','+str(Column-self.x)+']'
        self.b.configure(text=self.product_name,anchor='n')
        
    def popup(self):
        global pos_value
        global value
        window = Toplevel()
        window.geometry("400x200+650+450")
        value=StringVar(window)
        product = Label(window, text="Product Name: ")
        position = Label(window, text="Position: ")
        product.grid(row=0, column=0)
        position.grid(row=1,column=0)
        window.grid_columnconfigure(1, minsize=50) 
        window.grid_columnconfigure(2, minsize=50) 
        window.grid_columnconfigure(3, minsize=50) 
        window.grid_columnconfigure(4, minsize=50) 
        window.grid_rowconfigure(1, minsize=50) 
        window.grid_rowconfigure(2, minsize=100) 
        pos_value = StringVar(window,"2") 
        Radiobutton(window,variable=pos_value,text="UP",value=0,indicator=0, bg="yellow",width=5,).grid(row=1,column=1)
        Radiobutton(window,variable=pos_value,text="DOWN",value=1,indicator=0, bg="yellow",width=5).grid(row=1,column=2)
        Radiobutton(window,variable=pos_value,text="LEFT",value=2,indicator=0, bg="yellow",width=5).grid(row=1,column=3)
        Radiobutton(window,variable=pos_value,text="RIGHT",value=3,indicator=0, bg="yellow",width=5).grid(row=1,column=4)
        Entry(window,textvariable=value).grid(row=0,column=1,columnspan=3)
        submit = Button(window, text="Save",width=6, command=self.entry)
        save = Button(window, text="Exit",width=6,command=window.destroy)
        submit.grid(row=2, column=1)
        save.grid(row=2,column=3)

    def highlight(self):
        #print(v.get())
        if v.get()=='0':
            self.b.configure(bg = "red")
            self.obst()
        elif v.get()=='1':
            self.b.configure(bg = "green")
            self.popup()
        else:
            self.b.configure(bg = "white")
            self.erase()
        #print(self.b.cget('bg'))

def generate():
    global d
    global v
    global value
    global Row
    global Column
    #print(Xaxis.get(),Yaxis.get())
    Row = int(Xaxis.get())
    Column = int(Yaxis.get())
    myframe=call_frame()
    v = StringVar(myframe, "9")     
    Product_button = Radiobutton(myframe,variable=v,text="Product",value=1,indicator=0, bg="yellow").grid(row=0,column=0)
    obstacle_button = Radiobutton(myframe,variable=v, text="Obstacle",value=0,indicator=0,bg="yellow").grid(row=0,column=1)
    remove_button = Radiobutton(myframe,variable=v, text="Deselct",value=9,indicator=0,bg="yellow").grid(row=0,column=2)
    try:
        for i in range(1,Row+1):
            d.append([])
            for j in range(0,Column):
                d[i-1].append(layout_button(myframe,i,j))
    except:
        pass
        #print("Entered")

def save():
    for item in d:
        for obj in item:
          
            if obj.product_name!='':
                temp1=obj.product_name.split(' ')
                temp2=obj.product_position.split(' ')

                if len(temp1)>2:
                    Products.append(temp1[0][:-1])
                    Products.append(temp1[1][:-1])
                else:
                    Products.append(obj.product_name[:-2])
            if obj.product_position!='':
                if len(temp2)>2:
                    Position.append(temp2[0])
                    Position.append(temp2[1])
                else:
                    Position.append(obj.product_position)
            if obj.obst_position!='':
                Obstacles.append(obj.obst_position)
    #print(Products,Position,Obstacles)
    file = open("buffer.txt", "w")
    file.write("")
    file.write(str(Row)+" "+str(Column)+"\n")
    for item in Products:
        file.write(str(item)+" ")
    file.write("\n")
    for item in Position:
        file.write(str(item)+" ")
    file.write("\n")
    for item in Obstacles:
        for co in item:
            if co!='[' and co!=']' and co!=',':
                file.write(str(co)+" ")
                
    file.write("\n")
    main.destroy()    

def check():
    global flag
    global Xaxis
    global Yaxis
    global selectframe
    selectframe.destroy()
    heading.configure(text="Admin Panel")
    flag=True
    Yaxis=StringVar(main,"5")
    Xaxis=StringVar(main,"5")
    #print("Enteres")
    row_label=Label(main,text="Enter number of rows:",fg="black",font=("Helvetica", 15 )).place(x=50,y=200)
    row_input = Entry(main, textvariable=Xaxis ).place(x=300,y=205)
    column_label=Label(main,text="Enter number of columns:",fg="black",font=("Helvetica", 15 )).place(x=50,y=300)
    column_input = Entry(main, textvariable=Yaxis).place(x=300,y=305)
    Enter_button = Button(main, text="Generate", width=10,height=2,bg='grey',command=generate)
    Enter_button.place(x=100,y=400)
    save_button = Button(main, text="Save", width=10,height=2,bg='grey',command=save)
    save_button.place(x=100,y=500)

def Host():
    main.destroy()
    #print("Host_code")

selectframe=Frame()
def select():
    global selectframe
    if username.get()=='Admin' and password.get()=='Admin123':
        verifyframe.destroy()
        selectframe=call_frame()
        host_button = Button(selectframe, text="Host",font=("Hevlectica",15),width=6,height=1,command= Host).place(x=150,y=175)
        layout_edit_button=Button(selectframe, text="Edit Layout",font=("Hevlectica",15),width=10,height=1,command= check).place(x=400,y=175)
        
verifyframe = call_frame()
username=StringVar(verifyframe)
password=StringVar(verifyframe)
heading = Label(main,text="Admin Login",fg="green",font=("Helvetica", 30,"bold"))
heading.place(x=800,y=50)
User_label=Label(verifyframe,text="Enter Username:",fg="black",font=("Helvetica", 15 )).place(x=200,y=100)
User_input = Entry(verifyframe, textvariable=username).place(x=400,y=105)
Pass_label = Label(verifyframe, text="Enter Password:",fg="black",font=("Helvetica", 15 )).place(x=200,y=150)
Pass_input = Entry(verifyframe, textvariable=password, show='*').place(x=400,y=150)
submit_button = Button(verifyframe, text="Verify",font=("Hevlectica",15),width=6,height=1,command= select).place(x=350,y=250)
main.mainloop()



