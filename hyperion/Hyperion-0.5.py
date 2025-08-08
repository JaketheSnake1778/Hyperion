version = ("v0.5.8/7/25")

# Credit to TEABOY
# Feel free to change / improve anything
import math
import random
import time
import turtle
#import os

astlist = []


windowsizex = 1600
windowsizey = 900

G = 0.7  # gravity constant, actually 6.673e-11, but for arcady-ness needs to be *much* higher

print("Hyperion - By TEABOY")
print(version)


class Game:
    def __init__(self):

        # Creating a window screen
        self.wn = turtle.Screen()
        self.wn.title("Hyperion " + version)
        self.wn.bgcolor(0, 0, 0)
        screenTk = self.wn.getcanvas().winfo_toplevel()
        screenTk.attributes("-fullscreen", True)


        # setting necessary program vars
        self.runtime = 0
        self.lag = []
        self.sum = 0
        self.returntime = 0
        self.paused = False
        self.resetted = False
        self.classesLoaded = False
        self.hasStarted = False

        # initializing non-menu classes
        

        print("Running - Alt + F4 or CTRL-C in terminal to close")

        

    def mainloop(self):

        if not self.hasStarted:
            self.menu = StartMenu()
        
        starttimer = time.time()

        # needed to make the game run
        self.wn.update()


        #New keyboard logic
        self.wn.listen()
        self.wn.onkey(self.inputW, 'w')
        self.wn.onkey(self.inputA, 'a')
        self.wn.onkey(self.inputS, 's')
        self.wn.onkey(self.inputD, 'd')
        self.wn.onkey(self.inputSpace, 'space')
        self.wn.onkey(self.restart, 'r')
        self.wn.onkey(self.pause, 'p')

        # making the objects refresh
        if not game.paused:
            self.ship.onloop()
            self.hud.onloop()
            self.level.onloop()
            self.effect.onloop()

            if self.resetted:
                self.ship.t.clear()
                self.resetted = False

            #Finicky asteroid logic
            for asto in astlist:
                asto.onloop()
                if self.isejected(asto.loc, asto.velocity) or (game.collision(asto.loc[0], asto.loc[1], 0, 0, 15)) or (game.collision(asto.loc[0], asto.loc[1], game.level.moon.position[0], game.level.moon.position[1] + 5, 5)):
                    asto.t.clear()
                    asto.t.hideturtle()
                    astlist.remove(asto)
                    del(asto)
                

            if random.randint(0, 10) == 1 and astlist.__len__() < 5:
                astlist.append(Asteroid(self.level.moon.position[0] * (random.randint(7, 13) / 10), self.level.moon.position[1] * (random.randint(7, 13) / 10), random.random() * 4, random.randint(0, 360)))

            # Quasars started here
            if (random.randint(0, 800) == 1) and self.level.quasaring == False:
                self.level.quasar()

        if not game.paused:
            self.runtime += 1


        # calculate total time it takes to run per frame
        endtimer = time.time()
        self.returntime = endtimer - starttimer
        self.lag.append(self.returntime)
        if len(self.lag) > 50:
            self.lag.pop(0)

        self.sum = 0

        for x in self.lag:
            self.sum = self.sum + x
        self.sum = self.sum / 51

        if self.sum > 0.06:
            self.lagreduce()

    def inputSpace(self):
        if self.classesLoaded:
            self.ship.thrust()
        else:
            self.menu.start()
    
    def inputW(self):
        if self.classesLoaded:
            self.ship.prograde()

    def inputA(self):
        if self.classesLoaded:
            self.ship.turnleft()
    
    def inputS(self):
        if self.classesLoaded:
            self.ship.retrograde()
    
    def inputD(self):
        if self.classesLoaded:
            self.ship.turnright()


    def pause(self):
        if game.paused:
            game.paused = False
            game.hud.warnmessage = ""
            self.menu.clear()
        else:
            game.hud.warnmessage = "PAUSED - SCORE: " + str(self.ship.runtime)
            game.hud.onloop()
            game.paused = True
            self.menu.pauseMenu()

    def isejected(self, loc, velocity):
        if (loc[0] > windowsizex / 2 or loc[0] < -windowsizex / 2) or (loc[1] > windowsizey / 2 or loc[1] < -windowsizey / 2) or (velocity > 20):
            return (True)
        else:
            return (False)

    def collision(self, x1, y1, x2, y2, rad):
        if math.dist((x1, y1), (x2, y2)) <= rad:
            return True
        else:
            return False

    def lagreduce(self):

        print("Reducing lag...")
        self.ship.t.clear()
        self.ship.e.clear()

        self.hud.note.clear()
        self.hud.rotT.clear()
        self.hud.velT.clear()
        self.hud.nameT.clear()

    def restart(self):

        self.resetted = True
        game.ship.reset()

        game.level.reset()
        game.lagreduce()
        self.hud.warnmessage = " "

    def onstart(self):
        self.ship = Ship(0, 25, 10, -90, "white")
        self.hud = HUD()
        self.level = Level()
        self.effect = Effects()

        self.wn.tracer(0)  # Move to after classes are made for intro animation
        self.classesLoaded = True

        

# Start of gravity code
        # Honestly I have no idea how any of this works
    def giveMotion(self, deltaV, motionDirection):

        if self.velocity != 0:

            x_comp = math.sin(math.radians(
                self.motionDirection)) * self.velocity
            y_comp = math.cos(math.radians(
                self.motionDirection)) * self.velocity
            x_comp += math.sin(math.radians(motionDirection)) * deltaV
            y_comp += math.cos(math.radians(motionDirection)) * deltaV
            self.velocity = math.sqrt((x_comp ** 2) + (y_comp ** 2))

            if x_comp > 0 and y_comp > 0:  # calculate degrees depending on the coordinate quadrant
                self.motionDirection = math.degrees(
                    math.asin(abs(x_comp)/self.velocity))  # update motion direction

            elif x_comp > 0 and y_comp < 0:
                self.motionDirection = math.degrees(
                    math.asin(abs(y_comp)/self.velocity)) + 90

            elif x_comp < 0 and y_comp < 0:
                self.motionDirection = math.degrees(
                    math.asin(abs(x_comp)/self.velocity)) + 180

            else:
                self.motionDirection = math.degrees(
                    math.asin(abs(y_comp)/self.velocity)) + 270

        else:
            self.velocity = self.velocity + deltaV  # in m/s
            self.motionDirection = motionDirection  # degrees

    # math for the orbit of the spaceship, no clue how it works
    def gravity(self, shipx, shipy, massofship, velofship):

        self.mass = massofship
        self.velocity = velofship
        motionForce = self.mass * self.velocity  # F = m * v
        x_net = 0
        y_net = 0
        gridScale = 2

        for x in [y for y in Planet.instances if y is not self]:

            distance = math.sqrt(
                ((shipx - x.position[0]) ** 2) + (shipy - x.position[1] - x.uradius) ** 2)
            gravityForce = G*(self.mass * x.umass) / \
                ((distance * gridScale) ** 2)

            x_pos = shipx - x.position[0]
            y_pos = shipy - x.position[1] - x.uradius

            if x_pos <= 0 and y_pos > 0:  # calculate degrees depending on the coordinate quadrant
                gravityDirection = math.degrees(
                    math.asin(abs(y_pos)/distance)) + 90

            elif x_pos > 0 and y_pos >= 0:
                gravityDirection = math.degrees(
                    math.asin(abs(x_pos)/distance)) + 180

            elif x_pos >= 0 and y_pos < 0:
                gravityDirection = math.degrees(
                    math.asin(abs(y_pos)/distance)) + 270

            else:
                gravityDirection = math.degrees(math.asin(abs(x_pos)/distance))

            # x component of vector
            x_gF = gravityForce * math.sin(math.radians(gravityDirection))
            # y component of vector
            y_gF = gravityForce * math.cos(math.radians(gravityDirection))

            x_net += x_gF
            y_net += y_gF

        x_mF = motionForce * math.sin(math.radians(self.motionDirection))
        y_mF = motionForce * math.cos(math.radians(self.motionDirection))
        x_net += x_mF
        y_net += y_mF
        netForce = math.sqrt((x_net**2)+(y_net**2))

        if x_net > 0 and y_net > 0:  # calculate degrees depending on the coordinate quadrant
            self.motionDirection = math.degrees(
                math.asin(abs(x_net)/netForce))  # update motion direction

        elif x_net > 0 and y_net < 0:
            self.motionDirection = math.degrees(
                math.asin(abs(y_net)/netForce)) + 90

        elif x_net < 0 and y_net < 0:
            self.motionDirection = math.degrees(
                math.asin(abs(x_net)/netForce)) + 180

        else:
            self.motionDirection = math.degrees(
                math.asin(abs(y_net)/netForce)) + 270

        self.velocity = netForce/self.mass  # update velocity
        traveled = self.velocity/gridScale  # grid distance traveled per 1 sec
        self.position = (shipx + math.sin(math.radians(self.motionDirection)) * traveled,
                         shipy + math.cos(math.radians(self.motionDirection)) * traveled)  # update pos

        return (self.position)
# End of gravity code

# main planet class, not just for planets, but for moons and other circular gravitational bodies
class Planet:

    instances = []

    def __init__(self, name, x, y, radius, mass, color):

        self.name = name
        self.velocity = 0
        Planet.instances.append(self)

        self.t = turtle.Pen()
        self.t.up()
        self.t.color(color)
        self.t.hideturtle()
        self.t.width(2)
        self.t.fillcolor(color)

        self.uradius = radius
        self.umass = mass
        self.position = [0, 0]
        self.position[0] = x
        self.position[1] = y - radius

        self.refresh = True

        self.onloop()

    def onloop(self):

        self.t.clear()

        self.t.up()
        self.t.goto(self.position)
        self.t.down()

        if self.refresh:
            self.t.begin_fill()
            self.t.circle(self.uradius)
            self.t.end_fill()

# the ship class
class Ship:
    def __init__(self, startx, starty, initvel, initveldir, color):

        self.t = turtle.Pen()
        self.t.color(color)
        # self.t.hideturtle()
        self.t.shape("circle")
        self.t.shapesize(0.2, 0.2, 0.2)

        self.e = turtle.Pen()
        self.e.color(0.2, 0.2, 0.2)
        self.e.hideturtle()
        self.e.width(4)

        self.m = turtle.Pen()
        self.m.color("yellow")
        self.m.hideturtle()

        self.motionDirection = initveldir
        self.loc = [startx, starty]
        self.velocity = 0
        self.mass = 10
        self.rotation = self.motionDirection
        self.deltaV = 49.9
        self.runtime = 0
        self.eraseloc = []
        self.eraseloc.append(self.loc)
        self.dead = False
        self.drainamount = 1
        self.drainrate = 0.25
        self.range = 100
        self.minerate = 0.2
        self.doGravity = True
        self.colorlist = ["red", "brown", "yellow", "orange"]

        Game.giveMotion(self, initvel, initveldir)

        self.t.up()
        self.t.goto(self.loc[0], self.loc[1])
        self.t.down()

    # Keybound functions
    def turnright(self):
        self.rotation = self.rotation + 5

    def turnleft(self):
        self.rotation = self.rotation - 5

    def thrust(self):
        if self.deltaV > 0:
            Game.giveMotion(self, 0.1, self.rotation)
            self.deltaV -= 0.1
        else:
            self.deltV = 0

    def prograde(self):
        self.rotation = self.motionDirection
        self.thrust()

    def retrograde(self):
        self.rotation = self.motionDirection - 180
        self.thrust()

    def reset(self):
        self.motionDirection = -90
        self.loc = [0, 25]
        self.velocity = 10
        self.mass = 10
        self.rotation = self.motionDirection
        self.deltaV = 49.9
        self.runtime = 0
        self.eraseloc = []
        self.eraseloc.append(self.loc)
        self.e.up()
        self.dead = False
        self.drainamount = 1
        self.drainrate = 0.25
        self.range = 100
        self.minerate = 0.2
        self.doGravity = True

        self.t.color("White")
        self.t.shapesize(0.2, 0.2, 0.2)


    def die(self):

        #only do things once
        if not self.dead:
            self.motionDirection = self.motionDirection + (random.randint(1, 120) - 60)
            self.velocity = self.velocity / 2
            self.deltaV = 0
            self.dead = True
            self.t.color("orange")
            self.t.shapesize(0.4, 0.4, 0.4)
            game.hud.warnmessage = "CRITICAL FAILURE ~ FINAL SCORE: " + str(int(self.deathtime))

            game.effect.explosion(self.loc[0], self.loc[1], 1)

        
    def onloop(self):

        self.m.clear()

        if self.doGravity:
            self.loc = Game.gravity(self, self.loc[0], self.loc[1], self.mass, self.velocity)

        if self.dead == False:
            
            self.deathtime = self.runtime

            self.eraseloc.append(self.loc)
        else:
            self.t.shapesize(random.random() / 2, random.random() / 2, random.random() / 2)
            self.t.color(self.colorlist[random.randint(0, 3)])

        self.t.goto(self.loc[0], self.loc[1])

        if (game.collision(game.ship.loc[0], game.ship.loc[1], 0, 0, 15)) or (game.collision(game.ship.loc[0], game.ship.loc[1], game.level.moon.position[0], game.level.moon.position[1] + 5, 5)):
            self.velocity = 0
            self.die()
            self.doGravity = False
        else:
            self.doGravity = True
            

        if (self.deltaV <= 0):
            self.die()

        for asteroid in astlist:
            if game.collision(game.ship.loc[0], game.ship.loc[1], asteroid.position[0], asteroid.position[1], 3):
                self.die()

        if game.collision(game.ship.loc[0], game.ship.loc[1], game.level.moon.position[0], game.level.moon.position[1], self.range) and self.dead == False:
            self.deltaV = self.deltaV + self.minerate
            game.hud.warnmessage = "MINING"
            self.m.up()
            self.m.goto(self.loc)
            self.m.down()
            self.m.goto(game.level.moon.position[0], game.level.moon.position[1] + 2.5)

        elif game.hud.warnmessage == "MINING":
            game.hud.warnmessage = ""

        if (len(self.eraseloc) > 150 or self.dead) and (len(self.eraseloc) > 1):
            self.eraseloc.pop(0)
            self.e.goto(self.eraseloc[0])

        elif len(self.eraseloc) > 0 and self.runtime < 100:
            self.e.goto(self.eraseloc[0])

        if self.runtime == 0:
            self.e.down()
        if self.runtime % 30 == 1 and self.deltaV > 0:
            self.deltaV = self.deltaV - self.drainamount

        if self.runtime % 1000 == 1 and not self.dead:
            self.drainamount = self.drainamount + self.drainrate
            self.minerate = self.minerate - 0.025
            self.range = self.range - 1

        self.runtime += 1

class Level:
    def __init__(self):
        self.earth = Planet("Earth", 0, 0, 15, 6000, "green")
        self.moon = Planet("Moon", 50, 0, 5, 1200, "lightblue")

        self.moonangle = (random.random() * 6.282) - 3.141
        self.moondist = (windowsizey / 2) - 25

        self.q = turtle.Pen()
        self.q.up()
        self.q.hideturtle()
        self.q.color("Yellow")
        
        self.qStart = 0
        self.direction = 0
        self.quasaring = False


    def rotate(self, origin, angle):
        
        angle = math.radians(angle)
        ox, oy = origin

        # x’ = x * cos(θ) – y * sin(θ) y’ = x * sin(θ) + y * cos(θ)
        qx = ox * math.cos(angle) - oy * math.sin(angle)
        qy = ox * math.sin(angle) + oy * math.cos(angle)
        return qx, qy

    def quasar(self):
        
        self.direction = (random.randint(0, 360))
        self.q.goto(0, 0)
        self.q.down()
        self.q.setheading(360 - (self.direction + 270))
        self.q.down()
        self.q.forward(windowsizex)
        self.q.backward(windowsizex * 2)
        self.q.up()

        if game.ship.dead == False:
            game.hud.warnmessage = "WARNING DANGEROUS QUASAR INCOMING"
        self.quasaring = True


        self.qStart = game.runtime

    def quasarE(self):
        self.q.width(50)
        self.q.down()
        self.q.forward(windowsizex * 2)
        
        self.q.width(1)
        self.q.up()


        self.earth.refresh = False

    def quasarD(self):
        self.q.clear()
        if game.ship.dead == False:
            game.hud.warnmessage = ""
        self.quasaring = False
        self.earth.refresh = True
        self.earth.t.color("DarkOrange4")

    def reset(self):
        self.earth.t.color("Green")

    def onloop(self):
        self.earth.onloop()
        self.moon.onloop()

        if self.moonangle <= 2 * math.pi:
            self.moonangle = self.moonangle + 0.001
        else:
            self.moonangle = 0

        rotShipPos = self.rotate(game.ship.loc, self.direction)
        
        self.moon.position[0] = self.planetorbitx(
            self.earth.position[0], self.moonangle, self.moondist)
        self.moon.position[1] = self.planetorbity(
            self.earth.position[1] + self.earth.uradius - self.moon.uradius, self.moonangle, self.moondist)

        if self.qStart > 0 and game.runtime == self.qStart + 90:
            self.quasarE()

        if game.runtime - self.qStart >= 90 and game.runtime - self.qStart < 180 and self.qStart != 0:
            if rotShipPos[0] < 25 and rotShipPos[0] > -25:
                game.ship.die()

        if self.qStart > 0 and game.runtime == self.qStart + 180:
            self.quasarD()

        # math for circular orbit Planet class objects, I.E. moons
    def planetorbitx(self, a, angle, distance):
        x = a + distance * math.cos(angle)
        return (x)

    def planetorbity(self, b, angle, distance):
        y = b + distance * math.sin(angle)
        return (y)
    
    
#Asteroid class, as of 0.3.7/10/23 they do not do anything but move
class Asteroid:

    def __init__(self, startx, starty, initvel, initveldir):

        radius = random.randint(5, 30) / 100

        self.t = turtle.Pen()
        self.t.color("gray")
        self.t.up()
        self.t.shape("circle")
        self.t.shapesize(radius, radius, radius)

        self.motionDirection = initveldir
        self.loc = [startx, starty]
        self.velocity = 0
        self.mass = random.randint(1, 100)
        self.rotation = self.motionDirection

        Game.giveMotion(self, initvel, initveldir)

        self.t.goto(self.loc[0], self.loc[1])

        self.onloop()

    def onloop(self):

        self.loc = Game.gravity(
            self, self.loc[0], self.loc[1], self.mass, self.velocity)

        self.t.goto(self.loc[0], self.loc[1])

        
class HUD:
    def __init__(self):

        self.rotT = turtle.Pen()
        self.rotT.hideturtle()
        self.rotT.color("white")
        self.rotT.up()
        self.rotT.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 50)
        self.rotT.write("Ship Rotation")
        self.rotT.goto((-windowsizex / 2) + 20, (windowsizey / 2) - 20)
        self.rotT.showturtle()

        self.velT = turtle.Pen()
        self.velT.hideturtle()
        self.velT.color("white")
        self.velT.up()
        self.velT.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 70)
        self.velT.write("V: 0.0")

        self.nameT = turtle.Pen()
        self.nameT.hideturtle()
        self.nameT.up()

        self.deltaT = turtle.Pen()
        self.deltaT.hideturtle()
        self.deltaT.color("white")
        self.deltaT.up()
        self.deltaT.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 90)
        self.deltaT.write("Fuel: 0.0")

        self.note = turtle.Pen()
        self.note.hideturtle()
        self.note.color("red")
        self.note.up()
        self.note.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 110)
        self.note.write("GO!")

        self.warnmessage = ""

        self.runtime = 0

    def writenote(self, message):
        self.note.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 130)
        self.note.color("white")
        self.note.write(message)
        self.note.color("red")
        self.note.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 110)

    def onloop(self):

        self.velT.clear()
        self.rotT.clear()
        self.nameT.clear()
        self.deltaT.clear()
        self.note.clear()

        self.rotT.setheading(-game.ship.rotation + 90)

        if self. warnmessage == "OUT OF BOUNDS":
            self.warnmessage = ""
        if (game.ship.loc[0] >= windowsizex / 2 or game.ship.loc[1] >= windowsizey / 2 or game.ship.loc[0] <= -windowsizex / 2 or game.ship.loc[1] <= -windowsizey / 2):
            self.warnmessage = "OUT OF BOUNDS"

        self.velT.write("V: " + str(round(game.ship.velocity, 2)))
        self.note.write(self.warnmessage)

        self.rotT.goto((-windowsizex / 2) + 10, (windowsizey / 2) - 50)
        self.rotT.write("Ship Rotation")
        self.rotT.goto((-windowsizex / 2) + 20, (windowsizey / 2) - 20)

        self.nameT.color("lightgreen")
        self.nameT.goto(game.ship.loc[0] - 10, game.ship.loc[1] - 18)
        self.nameT.write("Hyperion")
        self.nameT.color("red")

        if game.ship.deltaV < 30 and self.runtime % 30 == 0:
            self.deltaT.color("orange")
        elif self.runtime % 15 == 0:
            self.deltaT.color("white")

        self.deltaT.write("Fuel: " + str(abs(round(game.ship.deltaV, 1))))

        self.runtime += 1

class Effects:
    def __init__(self):
        self.e = turtle.Pen()
        self.e.shape("circle")
        self.e.up()
        self.e.hideturtle()

        self.e2 = turtle.Pen()
        self.e2.shape("circle")
        self.e2.up()
        self.e2.hideturtle()

        self.elocX = 0
        self.elocY = 0
        self.eint = 0
        self.etime = 0
        self.runtime = 0

        self.exploding = False


    def explosion(self, x, y, intensity):
        self.exploding = True
        self.elocX = x
        self.elocY = y
        self.eint = intensity

        self.etime = self.runtime
        
    def sparks(self, x, y, intensity):
        pass

    def onloop(self):
        self.runtime += 1
        if self.exploding:
            if self.etime == game.runtime:
                self.e.showturtle()
                self.e2.showturtle()
                self.e.color("red")
                self.e2.color("yellow")
                self.e.goto(self.elocX, self.elocY)
                self.e2.goto(self.elocX, self.elocY)
                self.e.shapesize(1 * self.eint, 1 * self.eint, 1 * self.eint)
                self.e2.shapesize(0.5 * self.eint, 0.5 * self.eint, 0.5 * self.eint)

            if self.runtime >= self.etime + 3:
                self.eint += 0.1
                self.e.shapesize(1 * self.eint, 1 * self.eint, 1 * self.eint)
                self.e2.shapesize(0.5 * self.eint, 0.5 * self.eint, 0.5 * self.eint)

            if self.runtime >= self.etime + 6:
                self.eint -= 0.1
                self.e.shapesize(1 * self.eint, 1 * self.eint, 1 * self.eint)
                self.e2.shapesize(0.5 * self.eint, 0.5 * self.eint, 0.5 * self.eint)

            if self.runtime >= self.etime + 9:
                self.e.hideturtle()
                self.e2.hideturtle()
                self.eint = 0
                self.exploding = False

class StartMenu:
    def __init__(self):
        self.selected = 0
        self.hasStarted = False
        game.paused = True
        game.hasStarted = True

        self.t = turtle.Pen()
        self.t.color("red")
        self.t.up()
        self.t.hideturtle()
        self.t.left(90)
        self.t.forward(windowsizey / 5)
        self.t.write("H Y P E R I O N", align="center", font=("Arial", int(windowsizex / 12), "bold", "italic"))   

        self.t.backward(windowsizey / 5)
        self.t.write("PRESS SPACE TO START", align="center", font=("Arial", int(windowsizex / 75), "bold"))   

        self.t.backward(windowsizey / 3.5)
        self.t.write("CONTROLS\nW - THRUST PROGRADE\nS - THRUST RETROGRADE\nA/D - ROTATE\nSPACE - THRUST\nP - PAUSE\nR - RESTART\nALT+F4 - QUIT", 
                    align="center", font=("Arial", int(windowsizex / 85), "bold", "italic"))   
        
        self.t.backward(windowsizey / 7)
        self.t.right(90)
        self.t.forward(windowsizex / 3)
        self.t.left(90)
        self.t.write(version, align="center", font=("Arial", int(windowsizex / 75), "bold"))   



    def start(self):
        self.t.clear()
        game.onstart()
        self.unpause()

    def unpause(self):
        self.t.clear()
        game.paused = False
    
    def pauseMenu(self):
        self.t.goto(0, 0)
        self.t.forward(windowsizey / 5)
        self.t.write("H Y P E R I O N", align="center", font=("Arial", int(windowsizex / 15), "bold", "italic"))   

        self.t.backward(windowsizey / 5)
        self.t.write("PRESS P TO UNPAUSE", align="center", font=("Arial", int(windowsizex / 75), "bold"))   

        self.t.backward(windowsizey / 3.5)
        self.t.write("CONTROLS\nW - THRUST PROGRADE\nS - THRUST RETROGRADE\nA/D - ROTATE\nSPACE - THRUST\nP - PAUSE\nALT+F4 - QUIT", 
                    align="center", font=("Arial", int(windowsizex / 85), "bold", "italic"))

        self.t.backward(windowsizey / 7)
        self.t.right(90)
        self.t.forward(windowsizex / 3)
        self.t.left(90)
        self.t.write(version, align="center", font=("Arial", int(windowsizex / 75), "bold"))   


    def clear(self):
        self.t.clear()   
        
            



# mainloop to keep the game running
global game
game = Game()
waitT = 0
while True:
    game.mainloop()
    if 1/30 - game.returntime > 0:
        waitT = 1/30 - game.returntime
    else:
        waitT = 0
    time.sleep(waitT)  # sets framerate, usually 1/60