import pygame
import sys
from pygame.locals import *
from tkinter import *
pygame.init()
size=display_width,display_height=1280,720
#colour
black=0,0,0
white=255,255,255
red_brown=168+55,25,15
green=36, 124, 45
dark_red_brown=168, 25, 15
blue=77, 57, 206
#font
myfont = pygame.font.SysFont("monospace", 15)
#variable
node_pos={} ##(city_name=rectangle_pos)
city_name={} ##(city_name=object)
line_pos=[] ##(cites,status)
i=0
counts=1
class HashableRect(pygame.Rect):
    def __hash__(self):
        return hash(tuple(self))

class node(object):
    def __init__(self,name,p):
        self.neighbour={}#object=distance
        self.city_name=name
        self.position=p
        self.create_node(p)        
        node_pos[self.city_name]=self.position
    def create_node(self,p,colour=red_brown,width=3):
        self.rect_ui=pygame.draw.rect(screen, colour,( (self.position),(50,25)),width)
        self.text=CenteredText(self.city_name,p[0],p[1],50,25)
        pygame.display.flip()
    def __str__(self):
        return self.city_name
    def show_neighbour(self):
        for i in self.neighbour:
            print(i)
    def draw_line(self,p,distance):
        self.neighbour_position=p
        self.connection=pygame.draw.line(screen, black,self.position,self.neighbour_position,3)
        self.distance_font=pygame.font.SysFont("monospace", 15)
        self.distance_text=self.distance_font.render(distance,True,black)
        screen.blit(self.distance_text,((self.position[0]+self.neighbour_position[0])/2,(self.position[1]+self.neighbour_position[1])/2))
        line_pos.append((self.connection,self.distance_text))
        pygame.display.flip()
    def rectangle_ui(self):
        return self.rect_ui
    def get_position(self):
        return self.position
    def get_name(self):
        return self.city_name
    def add_neighbour(self,other,distance):
        self.neighbour[other]=distance
    def get_neighbour(self):
        neighbour=[]
        for n in self.neighbour:
            neighbour.append(n.get_name())
        return neighbour
class Search_Agent(node):
    def __init__(self):
        self.explored=[]
        self.viewed=[]
        self.path=[]
    def find_path(self,start,goal):
        if start in city_name and goal in city_name:
            state=start
            if goal==state:
                self.path.append(state)
                return self.path[:]
            for neighbour in city_name[state].get_neighbour():
                if neighbour not in self.explored and neighbour not in self.viewed:
                    self.viewed.append(state)
                    self.path.append(state)
                    return self.find_path(neighbour,goal)
            self.explored.append(state)
            if state in self.path:
                self.path.remove(state)
            self.viewed=[]
        else:
            return "no route found"

class CenteredText(object):
    def __init__(self, text,x,y,w,h,text_size=10,color=(0,0,0)):
        self.x, self.y, self.w, self.h = x,y,w,h
        pygame.font.init()
        font = pygame.font.SysFont("monospace",text_size,bold=1)
        width, height = font.size(text)
        xoffset = (self.w-width) // 2
        yoffset = (self.h-height) // 2
        self.coords = self.x+xoffset, self.y+yoffset
        self.txt = font.render(text, True, color)
        self.draw(screen)
    def draw(self, screen):
        screen.blit(self.txt, self.coords)

class input_box(object):
    def __init__(self,text="city"):
        self.data=None  
        self.title=text
        self.create_ui_for_city_name()      
        self.master.mainloop()
    def create_ui_for_city_name(self):
        self.master = Tk()
        Label(self.master, text=self.title).grid(row=0)
        self.e1 = Entry(self.master)
        self.e1.grid(row=0, column=1)
        Button(self.master, text='Quit', command=self.master.destroy).grid(row=3, column=0, sticky=W, pady=4)
        Button(self.master, text='enter', command=self.get_input_from_user).grid(row=3, column=1, sticky=W, pady=4)
    def get_input_from_user(self):
        self.data=self.e1.get()
        self.master.destroy()
    def getter(self):
        return self.data

class searh_input(object):
    def __init__(self):
        self.search_cities=[]
        self.create_ui_for_searching()
        self.master.mainloop()
    def create_ui_for_searching(self):
        self.master=Tk()
        Label(self.master, text="start").grid(row=0)
        Label(self.master, text="end").grid(row=1)
        self.e1 = Entry(self.master)
        self.e2 = Entry(self.master)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        Button(self.master, text='Quit', command=self.master.destroy).grid(row=3, column=0, sticky=W, pady=4)
        Button(self.master, text='enter', command=self.get_search_input_from_user).grid(row=3, column=1, sticky=W, pady=4)        
    def get_search_input_from_user(self):
        self.search_cities.append(self.e1.get())
        self.search_cities.append(self.e2.get())
        self.master.destroy()  
    def get_search_cities(self):
        return self.search_cities

def get_input(text="city"):
    i=input_box(text)
    return i.getter()
def get_input_for_search():
    i=searh_input()
    return i.get_search_cities()
def make_screen():
    screen.fill(white)
    search=pygame.draw.rect(screen,blue,(1237, 156,100,50))
    search_text = CenteredText("search",1237, 156,100,50,20)
    clear=pygame.draw.rect(screen,black,(1237,156+100,100,50))
    clear_text=CenteredText("Clear",1237, 156+100,100,50,20,white)
    pygame.display.flip()
def update():
    global node_pos,city_name
    global line_pos
    make_screen()
    for p in line_pos:
        pygame.draw.line(screen, black, p[0],p[1])
    for city,p in node_pos.items():
        pygame.draw.rect(screen, red_brown,( (p),(50,25)), 3)
        text = CenteredText(city,p[0],p[1],50,25)
    pygame.display.flip()

screen=pygame.display.set_mode((0,0),RESIZABLE)
make_screen()
EXIT=True
search_key_pressed=False
adding=False
distance=None
path=[]
while EXIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXIT=False
        if event.type==pygame.KEYDOWN:
            if event.key == ord("l"):
                for k,c_name in city_name.items():
                    if c_name.rectangle_ui().collidepoint(pygame.mouse.get_pos()):
                        break   
        if event.type==pygame.KEYUP:
            if event.key==ord("l"):
                for k,n_name in city_name.items():
                    if n_name.rectangle_ui().collidepoint(pygame.mouse.get_pos()):
                        distance=get_input("distance")
                        if distance:
                            c_name.draw_line(n_name.get_position(),distance) 
                            node.add_neighbour(c_name,n_name,distance)
                            node.add_neighbour(n_name,c_name,distance)
                            distance=None
        if event.type ==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if not search_key_pressed:
                    for k,c in city_name.items():
                        if c.rectangle_ui().collidepoint(pygame.mouse.get_pos()):
                            adding=True 
                            break                   
        if event.type == pygame.MOUSEBUTTONUP:  
            if event.button==1:
                if search.collidepoint(pygame.mouse.get_pos()):
                    search_key_pressed=True
                    search_city_list=get_input_for_search()
                    if len(search_city_list)==2:
                        agent=Search_Agent()
                        path=agent.find_path(search_city_list[0],search_city_list[1])
                        if path:
                            for p in path:
                                city_name[p].create_node(node_pos[p],green,9)
                            search_key_pressed=False
                elif adding:
                    n=get_input()
                    if n:
                        city_name[n]=node(n,pygame.mouse.get_pos())
                        distance=get_input("distance")
                        if distance:
                            c.draw_line(city_name[n].get_position(),distance)
                            node.add_neighbour(c,city_name[n],distance)
                            node.add_neighbour(city_name[n],c,distance)
                            distance=None
                            adding=False
                            n=None
                else:
                    n=get_input()
                    if n:
                        city_name[n]=node(n,pygame.mouse.get_pos())
                        n=None


    #update()

if not path:
    print("nnone")
else:
    for p in path:
        print("-->",p,end=" ")    
pygame.quit()
quit()
