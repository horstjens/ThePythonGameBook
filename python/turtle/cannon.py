# need easygui installed or in the same directory
# tested with python3
# author: Horst JENS <horstjens@gmail.com>
# license: gpl, see http://www.gnu.org/copyleft/gpl.html

import easygui as e
import math
import random as r
import turtle as t



def castle(l=600):
    t.begin_fill()
    t.fd(l)  
    t.lt(90)
    t.fd(2*l/3)
    t.lt(90)
    t.fd(l/3)
    t.lt(90)
    t.fd(l/3)
    t.rt(90)
    t.fd(l/3)
    t.rt(90)
    t.fd(l/3)
    t.lt(90)
    t.fd(l/3)
    t.lt(90)
    t.fd(2*l/3)
    t.lt(90)
    t.end_fill()
    
def cannon(l=70):
    t.begin_fill()
    t.circle(25) # voller Kreis
    t.circle(25,150)  
    t.fd(l)
    t.lt(90)
    t.fd(l/7*2)
    t.lt(90)
    t.fd(l)
    t.lt(180)
    t.end_fill()
    t.fd(l) # biss weng
    
def paint(castlesize = 100, ground=-200, leftpos=-500):
    t.pensize(5)
    #ground = -200
    #leftpos = -500
    t.pu()
    t.goto(leftpos, ground)
    t.pd()
    #t.fd(-500)
    castle(castlesize)
    t.fd(leftpos * -2)

    #kanone
    t.color("blue","green")
    cannon()
    t.setheading(45)


t.screensize(1600,800)
castlesize = 100
ground=-200
leftpos = -500
#t.left(70)
speed=10
play = True
heading = 45

while play:
    #t.clear()
    t.pu()
    t.home()
    t.clear()
    t.speed(0)
    t.pd()
    paint(castlesize, ground, leftpos)
    #t.home()
    #t.pu()
    #t.goto(leftpos * -1, ground)
    #t.setheading(45)
    #t.fd(50)
    t.pd()
    t.speed(10)
    wind = r.choice((-1,1)) * round(r.random(),4)
    e.msgbox("wind is : {}".format(wind))
    #print("wind is : {}".format(wind))
    #heading = float(input("please enter angle (e.g. 45.0)"))
    #speed = float(input("please enter speed (e.g. 10.0)"))
    heading = float( e.enterbox("please enter angle (e.g. 45.0)", default="45.0"))
    speed = float(e.enterbox("please enter speed (e.g. 10.0)", default = "10.0"))

    t.setheading(180-heading)


    dx = math.cos(t.heading()*math.pi/180)*speed
    dy = math.sin(t.heading()*math.pi/180)*speed
    #for step in range(200):
    y = ground
    while y >= ground:
        x = t.xcor()
        y = t.ycor()
        dy -= 0.1
        x += dx
        y += dy
        t.goto(x,y)
    
    play = e.boolbox("play again?")

t.exitonclick()
