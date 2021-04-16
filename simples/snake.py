from turtle import  *
from random import  *
from base import vector, square

food = vector(0, 0)
snake = [vector(10, 0)]
speed = 10
aim = vector(0, -speed)

def change(x, y):
    "change snake direction"
    aim.x = x
    aim.y = y

def inside(head):
    return -200 <head.x < 190 and -200 < head.y < 190

def move():
    head = snake[-1] .copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return


    snake.append(head)
    if head == food:
        print('snake point', len(snake))
        food.x = randrange(-15, 15)*10
        food.y = randrange(-15, 15)*10
    else:
        snake.pop(0)
    clear()


    for body in snake:
        square(body.x, body.y, 9, 'green')

    square(food.x, food.y, 9, 'black')
    update()
    ontimer(move, 100)

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(speed,0), 'Right')
onkey(lambda: change(-speed, 0), 'Left')
onkey(lambda: change(0,speed), 'Up')
onkey(lambda: change(0,-speed), 'Down')
move()
done()

