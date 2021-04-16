from random import *
from turtle import *
from base import vector

player = vector(0, 0)
aim = vector(2, 0)

def wrap(value):

    if value == 210:
        dot(10, 'red')
    return value




def draw():
    player.move(aim)
    player.x = wrap(player.x)
    player.y = wrap(player.y)
    aim.move(random()-0.3)
    aim.rotate(random()*10)
    clear()
    goto(player.x, player.y)
    dot(10)
    if True:
        ontimer(draw, 100)


setup(420, 420, 370, 0)

tracer(False)
up()
draw()
done()




