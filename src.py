import os
import random
import os.path
from os import path

#modes
game_play = 0
main_menu = 0
settings = 0
character = 0
select = 0
gameinit = 1
pause = 1
platforminit = 0
brokenlist = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
movinglist = []

WIDTH = 1000
HEIGHT = 700
#if __name__ == '__main__':
    #os.system('py -m pgzero penguin.py')
#player
player = Actor('mrchew', anchor=('center', 'bottom'))
player.pos = -1000, 500
player._update_pos()
playerlegs = Actor('playerlegs', anchor=('center', 'bottom'))
playerlegs.pos = 500, 300 #actually show doesnt work
playerlegs._update_pos()
dead = 0

#platform
platformDirection = [0, 0, 0, 0, 0, 0, 0, 0, 0]
updateplatform = 0
platform1 = Actor('platform1')#sorry mr chew apparently blit doesnt want to cooperate
platform2 = Actor('platform1')
platform3 = Actor('platform1')
platform4 = Actor('platform1')
platform5 = Actor('platform1')
platform6 = Actor('platform1')
platform7 = Actor('platform1')
platform8 = Actor('platform1')
platform9 = Actor('platform1')
platform1.pos = -1000, 0
platform2.pos = -1000, 0
platform3.pos = -1000, 0
platform4.pos = -1000, 0
platform5.pos = -1000, 0
platform6.pos = -1000, 0
platform7.pos = -1000, 0
platform8.pos = -1000, 0
platform9.pos = -1000, 0
touched1 = 0
touched2 = 0
touched3 = 0
touched4 = 0
touched5 = 0
touched6 = 0
touched7 = 0
touched8 = 0
touched9 = 0
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
xspawn = []
score = 0
red = 255 #bg colors
green = 0
blue = 0
cycle1 = 1
cycle2 = 0
cycle3 = 0
cycle4 = 0
cycle5 = 0
cycle6 = 0
textdisplay = 0
#score
highscore = 0
if path.exists("score.txt"):
    f = open("score.txt", "r") #normally saved in C:\Users\user_name\mu_code
    highscore = f.read()
else:
    f = open("score.txt", "w")
    f.write("0")
f.close()
if highscore == "":
    f = open("score.txt", "w")
    f.write("0")
    highscore = 0
    f.close()
def draw():
    global toptile
    global playerlegs, player
    global refresh, score
    global red, blue, green
    global cycle1, cycle2, cycle3, cycle4, cycle5, cycle6
    global platforminit, gameinit, textdisplay, character
    screen.fill((red, blue, green))  #background refresh
    if cycle1 == 1:
        green += 1
        if green == 255:
            cycle1 = 0
            cycle2 = 1
    elif cycle2 == 1:
        red -= 1
        if red == 0:
            cycle2 = 0
            cycle3 = 1
    elif cycle3 == 1:
        blue += 1
        if blue == 255:
            cycle3 = 0
            cycle4 = 1
    elif cycle4 == 1:
        green -= 1
        if green == 0:
            cycle4 = 0
            cycle5 = 1
    elif cycle5 == 1:
        red += 1
        if red == 255:
            cycle5 = 0
            cycle6 = 1
    elif cycle6 == 1:
        blue -= 1
        if blue == 0:
            cycle6 = 0
            cycle1 = 1
    playbutton.draw()
    platform1.draw()
    platform2.draw()
    platform3.draw()
    platform4.draw()
    platform5.draw()
    platform6.draw()
    platform7.draw()
    platform8.draw()
    platform9.draw()
    characterbutton.draw()
    playerlegs.draw()
    player.draw()
    if character == 0:
        player = Actor("mrchew", anchor=('center', 'bottom'))
    elif character == 1:
        player = Actor("trump", anchor=('center', 'bottom'))
    elif character == 2:
        player = Actor("queen", anchor=('center', 'bottom'))
    elif character == 3:
        player = Actor("osama", anchor=('center', 'bottom'))
    screen.draw.text("Your score: " + str(score), (10, 20), color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, shadow=(1,1))
    screen.draw.text("Your highscore: " + str(highscore), (10, 40), color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, shadow=(1,1))
def on_mouse_down(pos):
    global game_play, character
    if playbutton.collidepoint(pos):
        game_play = 1
        gameinit()
    if characterbutton.collidepoint(pos):
        character += 1
        if character == 4:
            character = 0
def update():
    global game_play
    player.pos = playerlegs.x, playerlegs.y - 110
    player._update_pos()
    #draw()
    if game_play == 1:
        game()
    elif dead == 1:
        game()
def mainmenu():
    global game_play, gameinit, platforminit, dead, updateplatform, yvelo, xdiff
    xdiff = 0
    yvelo = 0
    dead = 0
    updateplatform = 0
    game_play = 0
    platforminit = 0
    playbutton.pos = 500, 500
    characterbutton.pos = 800, 500
    playerlegs.pos = 500, 300
def gameinit():
    global refresh
    global game_play
    global toptile
    global xspawn
    global newtoptile
    newtoptile = 0
    xspawn = []
    toptile = [random.randint(50, 100)]
    for x in range(9):
        xspawn.append(random.randint(50, 960))
    for x in range(9):
        newtoptile = toptile[x] + random.randint(90,100)
        toptile.append(newtoptile)
    platform1.pos = xspawn[0], toptile[0]
    platform2.pos = xspawn[1], toptile[1]
    platform3.pos = xspawn[2], toptile[2]
    platform4.pos = xspawn[3], toptile[3]
    platform5.pos = xspawn[4], toptile[4]
    platform6.pos = xspawn[5], toptile[5]
    platform7.pos = xspawn[6], toptile[6]
    platform8.pos = xspawn[7], toptile[7]
    platform9.pos = 500, 600
    playerlegs.pos = 500, 500
    game_play = 1
def game():
    global touched1, touched2, touched3, touched4, touched5, touched6, touched7, touched8, touched9
    global gameinit, gameplay, gameplay, dead, score, game_play, highscore, updateplatform, platformDirection
    global xvelo, yvelo, yscoll, toptile, holdlength, toptile, xdiff
    toggleleft = 0
    toggleright = 0
    playbutton.pos = -1000, 500
    characterbutton.pos = -1000, 500
    if game_play == 1:
        #scoring
        if playerlegs.y < 100:
            if touched1 == 0:
                score += 1
                touched1 = 1
        if playerlegs.y < 200:
            if touched2 == 0:
                score += 1
                touched2 = 1
        if playerlegs.y < 300:
            if touched3 == 0:
                score += 1
                touched3 = 1
        if playerlegs.y < 400:
            if touched4 == 0:
                score += 1
                touched4 = 1
        if playerlegs.y < 500:
            if touched5 == 0:
                score += 1
                touched5 = 1
        if playerlegs.y < 600:
            if touched6 == 0:
                score += 1
                touched6 = 1
        if playerlegs.y < 700:
            if touched7 == 0:
                score += 1
                touched7 = 1
        if playerlegs.y < 800:
            if touched8 == 0:
                score += 1
                touched8 = 1
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
            if (platform9.y - 10 < playerlegs.y < platform9.y) and (platform9.x - 75 < playerlegs.x < platform9.x + 75) == True:
                jump()
                if platform9.image == "platform3":
                    animate(platform9, tween = 'out_elastic', pos=(platform9.x, 1000))
            elif (platform8.y - 10 < playerlegs.y < platform8.y) and (platform8.x - 75 < playerlegs.x < platform8.x + 75) == True:
                jump()
                if platform8.image == "platform3":
                    animate(platform8, tween = 'out_elastic', pos=(platform8.x, 1100))
            elif (platform7.y - 10 < playerlegs.y < platform7.y) and (platform7.x - 75 < playerlegs.x < platform7.x + 75) == True:
                jump()
                if platform7.image == "platform3":
                    animate(platform7, tween = 'out_elastic', pos=(platform7.x, 1200))
            elif (platform6.y - 10 < playerlegs.y < platform6.y) and (platform6.x - 75 < playerlegs.x < platform6.x + 75) == True:
                jump()
                if platform6.image == "platform3":
                    animate(platform6, tween = 'out_elastic', pos=(platform6.x, 1300))
            elif (platform5.y - 10 < playerlegs.y < platform5.y) and (platform5.x - 75 < playerlegs.x < platform5.x + 75) == True:
                jump()
                if platform5.image == "platform3":
                    animate(platform5, tween = 'out_elastic', pos=(platform5.x, 1400))
            elif (platform4.y - 10 < playerlegs.y < platform4.y) and (platform4.x - 75 < playerlegs.x < platform4.x + 75) == True:
                jump()
                if platform4.image == "platform3":
                    animate(platform4, tween = 'out_elastic', pos=(platform4.x, 1500))
            elif (platform3.y - 10 < playerlegs.y < platform3.y) and (platform3.x - 75 < playerlegs.x < platform3.x + 75) == True:
                jump()
                if platform3.image == "platform3":
                    animate(platform3, tween = 'out_elastic', pos=(platform3.x, 1600))
            elif (platform2.y - 10 < playerlegs.y < platform2.y) and (platform2.x - 75 < playerlegs.x < platform2.x + 75) == True:
                jump()
                if platform2.image == "platform2":
                    animate(platform2, tween = 'out_elastic', pos=(platform3.x, 1700))
            elif (platform1.y - 10 < playerlegs.y < platform1.y) and (platform1.x - 75 < playerlegs.x < platform1.x + 75) == True:
                jump()
                if platform1.image == "platform3":
                    animate(platform1, tween = 'out_elastic', pos=(platform1.x, 1800))
        #yboundaries
        if playerlegs.y < 0:
            refresh()
            if xdiff < 13:
                xdiff += 1
        if playerlegs.y > 699:
            game_play = 0 #deadeth
            dead = 1
        #platformproperties-moving
        direction = 0

        if platform1.image == "platform2":
            if platformDirection[0] == 0:
                platform1.x += 5 * (xdiff/5)
                if platform1.x > 980:
                    platformDirection[0] = 1
            elif platformDirection[0] == 1:
                platform1.x -= 5 * (xdiff/5)
                if platform1.x < 20:
                    platformDirection[0] = 0
        if platform2.image == "platform2":
            if platformDirection[1] == 0:
                platform2.x += 5 * (xdiff/5)
                if platform2.x > 980:
                    platformDirection[1] = 1
            elif platformDirection[1] == 1:
                platform2.x -= 5 * (xdiff/5)
                if platform2.x < 20:
                    platformDirection[1] = 0
        if platform3.image == "platform2":
            if platformDirection[2] == 0:
                platform3.x += 5 * (xdiff/5)
                if platform3.x > 980:
                    platformDirection[2] = 1
            elif platformDirection[2] == 1:
                platform3.x -= 5 * (xdiff/5)
                if platform3.x < 20:
                    platformDirection[2] = 0
        if platform4.image == "platform2":
            if platformDirection[3] == 0:
                platform4.x += 5 * (xdiff/5)
                if platform4.x > 980:
                    platformDirection[3] = 1
            elif platformDirection[3] == 1:
                platform4.x -= 5 * (xdiff/5)
                if platform4.x < 20:
                    platformDirection[3] = 0
        if platform5.image == "platform2":
            if platformDirection[4] == 0:
                platform5.x += 5 * (xdiff/5)
                if platform5.x > 980:
                    platformDirection[4] = 1
            elif platformDirection[4] == 1:
                platform5.x -= 5 * (xdiff/5)
                if platform5.x < 20:
                    platformDirection[4] = 0
        if platform6.image == "platform2":
            if platformDirection[5] == 0:
                platform6.x += 5 * (xdiff/5)
                if platform6.x > 980:
                    platformDirection[5] = 1
            elif platformDirection[5] == 1:
                platform6.x -= 5 * (xdiff/5)
                if platform6.x < 20:
                    platformDirection[5] = 0
        if platform7.image == "platform2":
            if platformDirection[6] == 0:
                platform7.x += 5 * (xdiff/5)
                if platform7.x > 980:
                    platformDirection[6] = 1
            elif platformDirection[6] == 1:
                platform7.x -= 5 * (xdiff/5)
                if platform7.x < 20:
                    platformDirection[6] = 0
        if platform8.image == "platform2":
            if platformDirection[7] == 0:
                platform8.x += 5 * (xdiff/5)
                if platform8.x > 980:
                    platformDirection[7] = 1
            elif platformDirection[7] == 1:
                platform8.x -= 5 * (xdiff/5)
                if platform8.x < 20:
                    platformDirection[7] = 0
        if platform9.image == "platform2":
            if platformDirection[8] == 0:
                platform9.x += 5 * (xdiff/5)
                if platform9.x > 980:
                    platformDirection[8] = 1
            elif platformDirection[8] == 1:
                platform9.x -= 5 * (xdiff/5)
                if platform9.x < 20:
                    platformDirection[8] = 0
    if dead == 1:
        yvelo -= 0.2
        playerlegs.y += yvelo
        playerlegs._update_pos()
        if updateplatform == 0:
            animate(platform1, tween = 'accelerate', duration= 3, pos=(platform1.x, -100))
            animate(platform2, tween = 'accelerate', duration= 3, pos=(platform2.x, -90))
            animate(platform3, tween = 'accelerate', duration= 3, pos=(platform3.x, -80))
            animate(platform4, tween = 'accelerate', duration= 3, pos=(platform4.x, -70))
            animate(platform5, tween = 'accelerate', duration= 3, pos=(platform5.x, -60))
            animate(platform6, tween = 'accelerate', duration= 3, pos=(platform6.x, -50))
            animate(platform7, tween = 'accelerate', duration= 3, pos=(platform7.x, -40))
            animate(platform8, tween = 'accelerate', duration= 3, pos=(platform8.x, -30))
            animate(platform9, tween = 'accelerate', duration= 3, pos=(platform9.x, -20))
            updateplatform = 1
        if platform8.y == -30:
            if score > int(highscore):
                highscore = score
                f = open("score.txt", "w")
                f.write(str(score))
                f.close()
            playerlegs.y = -50
            mainmenu()
def refresh():
    global yvelo
    global xdiff
    global platform1, platform2, platform3, platform4, platform5, platform6, platform7, platform8, platform9
    global touched1, touched2, touched3, touched4, touched5, touched6, touched7, touched8, touched9, brokenlist, movinglist
    playerlegs.y = 698
    yvelo = -9
    broken = 55
    moving = 55
    boundarydistl = 0 #distance from spawn to boundary
    boundarydistr = 0
    xspawn = []
    newxspawn = 500
    toptile = [random.randint(50, 75)]
    touched1 = 0
    touched2 = 0
    touched3 = 0
    touched4 = 0
    touched5 = 0
    touched6 = 0
    touched7 = 0
    touched8 = 0
    touched9 = 0
    for x in range(9): #list of x coordinates
        boundarydistl = 50 - newxspawn
        boundarydistr = 950 - newxspawn
        newxspawn += random.randint(boundarydistl, boundarydistr)
        xspawn.append(newxspawn)
    for x in range(9): #list of y coordinates
        newtoptile = toptile[x] + random.randint(90,100)
        toptile.append(newtoptile)
    platform1.pos = xspawn[0], toptile[0]
    platform2.pos = xspawn[1], toptile[1]
    platform3.pos = xspawn[2], toptile[2]
    platform4.pos = xspawn[3], toptile[3]
    platform5.pos = xspawn[4], toptile[4]
    platform6.pos = xspawn[5], toptile[5]
    platform7.pos = xspawn[6], toptile[6]
    platform8.pos = xspawn[7], toptile[7]
    xtrans = 0
    xtrans = int(playerlegs.x)
    if playerlegs.x < 20:
        xtrans = 30
    if playerlegs.x > 980:
        xtrans = 960
    platform9.pos = random.randint(xtrans - 25, xtrans + 25) , random.randint(670, 680) #fairness in transition
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
        if movinglist[0] == 0:
            platform1.image = "platform2"
        elif brokenlist[0] == 0:
            platform1.image = "platform3"
        else:
            platform1.image = "platform1"
        if movinglist[1] == 0:
            platform2.image = "platform2"
        elif brokenlist[1] == 0:
            platform2.image = "platform3"
        else:
            platform2.image = "platform1"
        if movinglist[2] == 0:
            platform3.image = "platform2"
        elif brokenlist[2] == 0:
            platform3.image = "platform3"
        else:
            platform3.image = "platform1"
        if movinglist[3] == 0:
            platform4.image = "platform2"
        elif brokenlist[3] == 0:
            platform4.image = "platform3"
        else:
            platform4.image = "platform1"
        if movinglist[4] == 0:
            platform5.image = "platform2"
        elif brokenlist[4] == 0:
            platform5.image = "platform3"
        else:
            platform5.image = "platform1"
        if movinglist[5] == 0:
            platform6.image = "platform2"
        elif brokenlist[5] == 0:
            platform6.image = "platform3"
        else:
            platform6.image = "platform1"
        if movinglist[6] == 0:
            platform7.image = "platform2"
        elif brokenlist[6] == 0:
            platform7.image = "platform3"
        else:
            platform7.image = "platform1"
        if movinglist[7] == 0:
            platform8.image = "platform2"
        elif brokenlist[7] == 0:
            platform8.image = "platform3"
        else:
            platform8.image = "platform1"
        if movinglist[8] == 0:
            platform9.image = "platform2"
        elif brokenlist[8] == 0:
            platform9.image = "platform3"
        else:
            platform9.image = "platform1"
def pause():
    global game_play, pause
    game_play = 0
    pause = 1

def jump():
    global xvelo, yvelo, playerlegs, score
    yvelo = -10
    playerlegs.image = 'playerlegs1'
