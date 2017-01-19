__author__ = 'Alkesh'
import turtle
import os
import random
import time
import simpleaudio as sa

#wave_obj = sa.WaveObject.from_wave_file(os.system("laser.mp3"))
#play_obj = wave_obj.play()
#play_obj.wait_done()

turtle.title("Infinity")
turtle.bgpic("back2.gif")
turtle.speed(0)
turtle.bgcolor("black")
turtle.setundobuffer(1)                      #It clears unnecessary memory by limiting the number of undo actions
turtle.tracer(0)


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.color(color)
        self.penup()
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        #Boundaries
        if(self.xcor() > 290):
            self.setx(290)
            self.rt(60)

        if(self.xcor() < -290):
            self.setx(-290)
            self.rt(60)

        if(self.ycor() > 290):
            self.sety(290)
            self.rt(60)

        if(self.ycor() < -290):
            self.sety(-290)
            self.rt(60)

    def is_Collision(self, other):
        if(self.xcor() >= other.xcor()-20 and self.xcor() <= other.xcor()+20 and
           self.ycor() >= other.ycor()-20 and self.ycor() <= other.ycor()+20):
            return True

        else:
            return False

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.life = 3

    def turn_left(self):
        self.lt(45)
    def turn_right(self):
        self.rt(45)
    def accelerate(self):
        self.speed += 1
    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.setheading(random.randint(0,360))
        self.speed = 6

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.setheading(random.randint(0,360))
        self.speed = 8

    #Overwriting move() to give allies a bit different movement
    def move(self):
        self.fd(self.speed)

        #Boundaries
        if(self.xcor() > 290):
            self.setx(290)
            self.rt(60)

        if(self.xcor() < -290):
            self.setx(-290)
            self.rt(60)

        if(self.ycor() > 290):
            self.sety(290)
            self.rt(60)

        if(self.ycor() < -290):
            self.sety(-290)
            self.rt(60)

        if(self.ycor() < -290):
            self.sety(-290)
            self.rt(60)


#Missile Sprite
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000,100)

    def fire(self):
        if(self.status == "ready"):
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status = "firing"


    def move(self):
        if(self.status == "ready"):
            self.goto(-1000,100)

        if(self.status == "firing"):
            self.fd(self.speed)

        #Border Collision Check
        if(self.xcor()< -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290):
            #print("Border hit")
            self.goto(-1000,100)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self,spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,100)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if(self.frame > 0):
            self.fd(10)
            self.frame += 1

        if(self.frame >20):
            self.frame = 0
            self.goto(-1000,100)

#Create the Sprites
player = Player("triangle", "white", 0, 0)
#enemy = Enemy("circle", "red", -100, 0 )
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "green", 100, 0)

enemies = []
allies = []
particles = []

for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0 ))

for i in range(6):
    allies.append(Ally("square", "green", 100, 0 ))

for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0 ))

#Key Bindings
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
turtle.onkey(player.decelerate,"Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

#Game Class
class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "Playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()


    def show_status(self):
        self.pen.undo()
        msg = "Score : %s"%(self.score)
        self.pen.penup()
        self.pen.goto(-300,310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

#Game Object
game = Game()
#Draw the game border
game.draw_border()
#Draw the score card
game.show_status()

#Game Loop
while(True):
    turtle.update()
    time.sleep(0.03)
    player.move()
    missile.move()


    for enemy in enemies:
        enemy.move()
        #Player collision with the enemy
        if(player.is_Collision(enemy)):
            x = random.randint(-200,200)
            y = random.randint(-200,200)
            enemy.goto(x,y)
            game.score -= 75
            game.show_status()

        #If the missile hits the enemy
        if(missile.is_Collision(enemy)):
            x = random.randint(-200,200)
            y = random.randint(-200,200)
            enemy.goto(x,y)
            missile.status = "ready"
            game.score += 100
            game.show_status()

            #Explosion System
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for ally in allies:
        ally.move()
        #If the missile hits the ally
        if(missile.is_Collision(ally)):
            x = random.randint(-200,200)
            y = random.randint(-200,200)
            ally.goto(x,y)
            missile.status = "ready"
            #Increase the score
            game.score -= 50
            game.show_status()

    for particle in particles:
        particle.move()


delay = input("Press Enter to finish")