# Author: Andrew Higgins
# https://github.com/speckly
# FamousJump, 15 March 2024

import random
from os import path

#modes
game_play = 0
dead = 0
settings = 0
character = 0
platforminit = 0
brokenlist = [50] * 9
movinglist = []

WIDTH = 1000
HEIGHT = 700

#player
player = Actor('mrchew', anchor=('center', 'bottom'))
playerlegs = Actor('playerlegs', anchor=('center', 'bottom'))
playerlegs.pos = 500, 300 #actually show doesnt work
playerlegs._update_pos()

#platform
platformDirection = [0] * 9
platforms = []
for i in range(9):
    platform = Actor('platform1')
    platform.pos = -1000, 0
    platforms.append(platform)
touched = [0] * 9
#buttons
playbutton = Actor('playbutton')
playbutton.pos = 200, 500 #middle
playbutton._update_pos()
characterbutton = Actor('characterbutton')
characterbutton.pos = 800, 500 #right middle
characterbutton._update_pos()
#physics
xdiff = 1 #multiplier of how xvelo changes
xvelo = 0 #velocities
yvelo = 0
holdlength = 0
#screenrefresh
is_refresh = 0
toptile = 0
score = 0
red = 255 #bg colors
green = 0
blue = 0
cycle = [1] + [0] * 5
#score
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



def draw():
    global toptile
    global playerlegs, player
    global red, blue, green
    global cycle
    screen.fill((red, blue, green))
    if cycle[0] == 1:
        green += 1
        if green == 255:
            cycle[0] = 0
            cycle[1] = 1
    elif cycle[1] == 1:
        red -= 1
        if red == 0:
            cycle[1] = 0
            cycle[2] = 1
    elif cycle[2] == 1:
        blue += 1
        if blue == 255:
            cycle[2] = 0
            cycle[3] = 1
    elif cycle[3] == 1:
        green -= 1
        if green == 0:
            cycle[3] = 0
            cycle[4] = 1
    elif cycle[4] == 1:
        red += 1
        if red == 255:
            cycle[4] = 0
            cycle[5] = 1
    elif cycle[5] == 1:
        blue -= 1
        if blue == 0:
            cycle[5] = 0
            cycle[0] = 1
    playbutton.draw()
    for platform in platforms:
        platform.draw()
    characterbutton.draw()
    playerlegs.draw()
    player.draw()
    characters = ["mrchew", "trump", "queen", "osama"]
    player = Actor(characters[character], anchor=('center', 'bottom'))
    screen.draw.text(f"Your score: {score}", (10, 20), color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, shadow=(1,1))
    screen.draw.text(f"Your highscore: {highscore}", (10, 40), color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, shadow=(1,1))

def on_mouse_down(pos):
    global game_play, character
    if playbutton.collidepoint(pos):
        game_play = 1
        gameinit()
    if characterbutton.collidepoint(pos):
        character = (character + 1) % 4

def update():
    # attach head to legs
    player.pos = playerlegs.x, playerlegs.y - 110
    player._update_pos()
    if game_play == 1:
        game()
    elif dead == 1:
        dead_ani()

def mainmenu():
    global game_play, dead, yvelo, xdiff, score
    game_play = dead = yvelo = xdiff = score = 0
    playbutton.pos = 200, 500
    characterbutton.pos = 800, 500
    playerlegs.pos = 500, 300

def gameinit():
    global refresh, platforms
    global game_play
    xspawn = []
    toptile = [random.randint(50, 100)]
    for i, platform in enumerate(platforms):
        xspawn.append(random.randint(50, 960))
        toptile.append(toptile[i] + random.randint(90,100))
        platform.pos = xspawn[i], toptile[i]

    playerlegs.pos = 500, 500
    platforms[-1].x = playerlegs.x # easy transition
    game_play = 1

def game():
    global touched, score, game_play, highscore, platformDirection
    global xvelo, yvelo, yscoll, holdlength, xdiff, dead
    toggleleft = 0
    toggleright = 0
    playbutton.pos = -1000, 500
    characterbutton.pos = -1000, 500
    if game_play == 1:
        #scoring
        for i in range(9):
            if playerlegs.y < 100 + 100*i:
                if touched[i] == 0:
                    score += 1
                    touched[i] = 1
        #physics
        yvelo += 0.275
        if yvelo > 0:
            playerlegs.image = "playerlegs"
        playerlegs.y = playerlegs.y + yvelo
        playerlegs._update_pos()
        #pacman mechanic idk
        if playerlegs.x < -20:
            playerlegs.x = 1020
        if playerlegs.x > 1020:
            playerlegs.x = -20
        #kontol
        if keyboard.left:
            toggleright = 0
            if toggleleft == 0:
                holdlength = 0
                toggleleft = 1
            if toggleleft == 1:
                holdlength += 0.1
            xvelo = 10 + holdlength
            playerlegs.x -= xvelo
        elif keyboard.right:
            toggleleft = 0
            if toggleright == 0:
                holdlength = 0
                toggleright = 1
            holdlength += 0.1
            xvelo = 10 + holdlength
            playerlegs.x += xvelo
        #platform contact
        if yvelo > 0:
            for i, platform in enumerate(platforms):
                if (platform.y - 10 < playerlegs.y < platform.y) and (platform.x - 75 < playerlegs.x < platform.x + 75):
                    jump()
                    if platform.image == "platform3":
                        animate(platform, tween = 'out_elastic', pos=(platform.x, 1000 + 100*i)) # Why did i implement this y cor?
        #yboundaries
        if playerlegs.y < 0:
            refresh()
            if xdiff < 13:
                xdiff += 1
        if playerlegs.y > 699:
            game_play = 0 #deadeth
            dead = 1
            for platform in platforms:
            # y cor increases by 10 if something doesnt work then put it back
                animate(platform, tween = 'accelerate', duration=3, pos=(platform.x, -100))
        #platformproperties-moving
        direction = 0
        for i, platform in enumerate(platforms):
            if platform.image == "platform2":
                if platformDirection[i] == 0:
                    platform.x += 5 * (xdiff/5)
                    if platform.x > 980:
                        platformDirection[i] = 1
                else:
                    platform.x -= 5 * (xdiff/5)
                    if platform.x < 20:
                        platformDirection[i] = 0

def dead_ani():
    global yvelo, highscore
    yvelo -= 0.2
    playerlegs.y += yvelo
    playerlegs._update_pos()
    if platforms[8].y == -100:
        if score > highscore:
            highscore = score
            with open("score.txt", "w") as f:
                f.write(str(score))
        playerlegs.y = -50
        mainmenu()
    # else:
    #     for platform in platforms:
    #         # y cor increases by 10 if something doesnt work then put it back
    #         animate(platform, tween = 'accelerate', duration=3, pos=(platform.x, -100))

def refresh():
    global yvelo
    global xdiff
    global touched, brokenlist, movinglist
    playerlegs.y = 698
    yvelo = -9
    xspawn = []
    newxspawn = 500
    toptile = [random.randint(50, 75)]
    for x in range(9):
        # list of x coordinates
        touched[x] = 0
        boundarydistl = 50 - newxspawn
        boundarydistr = 950 - newxspawn
        newxspawn += random.randint(boundarydistl, boundarydistr)
        xspawn.append(newxspawn)
        
        # list of y coordinates
        toptile.append(toptile[x] + random.randint(90,100))
    
    for i, platform in enumerate(platforms):
        platform.pos = xspawn[i], toptile[i]
    platforms[-1].x = playerlegs.x # easy transition

    xtrans = playerlegs.x
    if playerlegs.x < 20:
        xtrans = 30
    if playerlegs.x > 980:
        xtrans = 960
    if xdiff >= 2:
        movinglist = [] #init
        for x in range(9):
            moving = random.randint(0, 15 - xdiff)
            movinglist.append(moving)
    if xdiff >= 3:
        brokenlist = []
        for x in range(9):
            broken = random.randint(0, 25 - xdiff)
            brokenlist.append(broken)
    if xdiff >= 2:
        for i, platform in enumerate(platforms):
            if movinglist[i] == 0:
                platform.image = "platform2"
            elif brokenlist[i] == 0:
                platform.image = "platform3"
            else:
                platform.image = "platform1"

def jump():
    global yvelo, playerlegs
    yvelo = -10
    playerlegs.image = 'playerlegs1'

# if __name__ == '__main__':
#     os.system('py -m pgzero penguin.py')