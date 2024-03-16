# Author: Andrew Higgins
# https://github.com/speckly
# FamousJump, 15 and 16 March 2024

import random
from os import path

game_play = 0
dead = 0
charIDX = 0

WIDTH = 1000
HEIGHT = 700

#player
player = Actor('mrchew', anchor=('center', 'bottom'))
playerlegs = Actor('playerlegs', anchor=('center', 'bottom'))
playerlegs.pos = 500, 300
playerlegs._update_pos()

platformDirection = [0] * 9
platforms = []
wait = False
for i in range(9):
    platform = Actor('platform1')
    platform.pos = -1000, 0
    platforms.append(platform)
touched = [0] * 9

playbutton = Actor('playbutton')
playbutton.pos = 200, 500 # middle
playbutton._update_pos()
characterbutton = Actor('characterbutton')
characterbutton.pos = 800, 500 # right middle
characterbutton._update_pos()

xdiff = 1 # multiplier of how xvelo changes and moving platform speed
xvelo = 0 # velocities
yvelo = 0
holdlength = 0

score = 0
red = 255 #bg colors
green = 0
blue = 0
cycle = [1] + [0] * 5
highscore = 0

if path.exists("score.txt"):
    with open("score.txt") as f: #normally saved in C:\Users\user_name\mu_code
        highscore = f.read()
    
    if not highscore.isdigit():
        with open("score.txt", "w") as f:
            f.write("0")
            highscore = 0
    else:
        highscore = int(highscore)
else:
    with open("score.txt", "w") as f:
        f.write("0")
        highscore = 0

def game():
    global touched, score, game_play, highscore, platformDirection, xvelo, yvelo, holdlength, dead, xdiff, wait
    if game_play == 1:
        if playerlegs.y > 710: # Termination condition
            game_play = 0
            dead = 1
            for platform in platforms:
                animate(platform, tween = 'accelerate', duration=3, pos=(platform.x, -100))
            return

        yvelo += 0.275
        if yvelo > 0:
            playerlegs.image = "playerlegs"
        playerlegs.y += yvelo
        playerlegs._update_pos()

        if playerlegs.x < -20: # Wrap
            playerlegs.x = 1020
        elif playerlegs.x > 1020:
            playerlegs.x = -20

        if keyboard.left:
            holdlength += 0.05
            xvelo = -10 - holdlength
        elif keyboard.right:
            holdlength += 0.05
            xvelo = 10 + holdlength
        else:
            xvelo = 0
            holdlength = 0
        playerlegs.x += xvelo

        for i, platform in enumerate(platforms):
            if platform.image == "platform2":
                if platformDirection[i] == 0:
                    platform.x += 5 * (xdiff/20)
                    if platform.x > 980:
                        platformDirection[i] = 1
                else:
                    platform.x -= 5 * (xdiff/20)
                    if platform.x < 20:
                        platformDirection[i] = 0  

        # Collision
        if yvelo > 0:
            scale = (0 if 0 < yvelo < 10 else yvelo // 2)
            for i, platform in enumerate(platforms):
                # The yvelo can be too high and therefore overshoot this boundary, require scaling
                
                if platform.y + (10 + scale) > playerlegs.y > platform.y and platform.x - 75 < playerlegs.x < platform.x + 75:
                    yvelo = -10 # Jump
                    playerlegs.image = 'playerlegs1'
                    if not touched[i]:
                        score += 1
                        touched[i] = 1
                    if platform.image == "platform3":
                        animate(platform, tween = 'out_elastic', pos=(-100, 400))
        if playerlegs.y < 350 and not wait:
            wait = True
            if xdiff < 100:
                xdiff += 1
            scroll()
        else:
            wait = False

def refresh():
    global yvelo, xspawn, yspawn

    playerlegs.y = 700
    yvelo = -6
    xspawn = []
    yspawn = [random.randint(680, 690)]

    for i, platform in enumerate(platforms):
        touched[i] = 0
        xspawn.append(random.randint(50, 950))
        yspawn.append(yspawn[i] - random.randint(80, 95))
        platform.image = "platform1"  
        platform.pos = xspawn[i], yspawn[i]
    
    platforms[0].x = playerlegs.x # easy transition
    if xdiff >= 50:
        for platform in platforms:
            if not random.randint(0, 101 - xdiff): # chance of broken
                platform.image = "platform3"
    elif xdiff >= 25:
        for platform in platforms:
            if not random.randint(0, 120 - xdiff): # chance of moving
                platform.image = "platform2"

def scroll():
    global yvelo, xspawn, yspawn

    for i, platform in enumerate(platforms): 
        platform.y += 3
        if platform.y > 710:
            if xdiff >= 50 and not random.randint(0, 101 - xdiff): # chance of broken
                platform.image = "platform3"
            elif xdiff >= 30 and not random.randint(0, 120 - xdiff): # chance of moving
                platform.image = "platform2"
            newx = random.randint(50, 950)
            newy = platforms[-1].y - random.randint(80, 95)
            platform.pos = newx, newy
            platforms.append(platforms.pop(i))

def draw():
    global playerlegs, player, red, blue, green, cycle

    """The index of the color being changed (0 for red, 1 for green, and 2 for blue).
    The direction of the change (-1 for decreasing, 1 for increasing)."""
    
    color_changes = [(1, 1), (0, -1), (2, 1), (1, -1), (0, 1), (2, -1)]
    for i in range(len(cycle)):
        if cycle[i] == 1:
            if color_changes[i][0] == 0:
                red += color_changes[i][1]
                if red == 255 or red == 0:
                    cycle[i] = 0
                    cycle[(i + 1) % len(cycle)] = 1
            elif color_changes[i][0] == 1:
                green += color_changes[i][1]
                if green == 255 or green == 0:
                    cycle[i] = 0
                    cycle[(i + 1) % len(cycle)] = 1
            elif color_changes[i][0] == 2:
                blue += color_changes[i][1]
                if blue == 255 or blue == 0:
                    cycle[i] = 0
                    cycle[(i + 1) % len(cycle)] = 1
    
    screen.fill((red, blue, green))
    for actor in platforms + [playbutton, characterbutton, playerlegs, player]:
        actor.draw()

    characters = ["mrchew", "trump", "queen", "osama"]
    player = Actor(characters[charIDX], anchor=('center', 'bottom'))
    screen.draw.text(f"Your score: {score}", (10, 20), color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, shadow=(1,1))
    screen.draw.text(f"Your highscore: {highscore}", (10, 40), color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, shadow=(1,1))

def on_mouse_down(pos):
    global game_play, charIDX
    if playbutton.collidepoint(pos):
        playbutton.pos = -1000, 500
        characterbutton.pos = -1000, 500
        game_play = 1
        refresh()
    if characterbutton.collidepoint(pos):
        charIDX = (charIDX + 1) % 4

def update():
    global game_play, dead

    player.pos = playerlegs.x, playerlegs.y - 110 # attach head to legs
    player._update_pos()

    if game_play == 1:
        game()
    elif dead == 1:
        global yvelo, highscore, yvelo, xdiff, score
        yvelo -= 0.2
        playerlegs.y += yvelo
        playerlegs._update_pos()
        if platforms[8].y == -100:
            if score > highscore:
                highscore = score
                with open("score.txt", "w") as f:
                    f.write(str(score))
            # Reset
            playerlegs.y = -50
            game_play = dead = yvelo = xdiff = score = 0
            playbutton.pos = 200, 500
            characterbutton.pos = 800, 500
            playerlegs.pos = 500, 300