"""
This program is based on the original program 'just_drop.py'
by Sean M. Tracey from the book 'Make Games with Python"
"""

import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

pygame.init()
clock = pygame.time.Clock()

title_image = pygame.image.load("assets/title.jpg")
game_over_image = pygame.image.load("assets/game_over.jpg")
player_sprite_sheet = pygame.image.load("assets/wraith_V3.png") # load your sprite sheet
player_sprite_sheet = pygame.transform.scale(player_sprite_sheet, (640, 64)) # rescale sprite sheet


windowWidth = 400
windowHeight = 600

surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Drop!')

leftDown = False
rightDown = False

gameStarted = False
gameEnded = False
gamePlatforms = []
platformSpeed = 3
platformDelay = 2000
lastPlatform = 0
platformsDroppedThrough = -1
dropping = False

gameBeganAt = 0
timer = 0

frameTimer = 0 # used to help get correct sprite image
frameNumber = 0 # used as an index into sprite sheet to get correct sprite
wasMovingToTheLeft = True # boolean used to help when left or right button is not pressed

player = {
  "x" : windowWidth / 2,
  "y" : 0,
  "height" : 64, # original value = 25
  "width" : 32, # original value = 10
  "vy" : 5
}

def setFrameNumber():

  global leftDown, frameNumber
  if frameTimer % 10 == 0: # time to get next sprite frame
    # if moving to right and was moving to right
    if rightDown and not(wasMovingToTheLeft):
      if frameNumber > 4:
        frameNumber = 0
      else:
        frameNumber += 1
    # if moving to right and was moving left
    if rightDown and wasMovingToTheLeft:
      frameNumber = 0
    # if moving to left and was moving to left
    if leftDown and wasMovingToTheLeft:
      if frameNumber > 9:
        frameNumber = 5
      else:
        frameNumber += 1
    # if moving to left and was moving to right
    if leftDown and not(wasMovingToTheLeft):
      frameNumber = 5
    """
    # if not moving and was moving to the right
    if not(leftDown) and not(rightDown) and not(wasMovingToTheLeft):
      if frameNumber > 4:
        frameNumber = 0
      else:
        frameNumber += 1
    # if not moving and was moving to the left
    if not(leftDown) and not(rightDown) and wasMovingToTheLeft:
      if frameNumber > 9:
        frameNumber = 5
      else:
        frameNumber += 1
    """

def drawPlayer():

  hitbox = pygame.draw.rect(surface, (0,0,0), (player["x"], player["y"], player["width"], player["height"])) # defined this rectangle as a hitbox variable
  surface.blit(player_sprite_sheet, hitbox, (16 + 64 * frameNumber, 0, 32, 64))

def movePlayer():
  
  global platformsDroppedThrough, dropping

  leftOfPlayerOnPlatform = True
  rightOfPlayerOnPlatform = True

  if surface.get_at(( int(player["x"]), int(player["y"]) + player["height"])) == (0,0,0,255):
    leftOfPlayerOnPlatform = False
  
  if surface.get_at(( int(player["x"]) + (player["width"] - 22), (int(player["y"]) + 39) + (player["height"] - 39))) == (0,0,0,255): # modified based on original width and height settings
    rightOfPlayerOnPlatform = False

  if leftOfPlayerOnPlatform is False and rightOfPlayerOnPlatform is False and (player["y"] + player["height"]) + player["vy"] < windowHeight:
    player["y"] += player["vy"]

    if dropping is False:
      dropping = True
      platformsDroppedThrough += 1

  else :

    foundPlatformTop = False
    yOffset = 0
    dropping = False

    while foundPlatformTop is False:

      if surface.get_at(( int(player["x"]), ( int(player["y"]) + player["height"]) - yOffset )) == (0,0,0,255):
        player["y"] -= yOffset
        foundPlatformTop = True
      elif (player["y"] + player["height"]) - yOffset > 0:
        yOffset += 1
      else :

        gameOver()
        break

  if leftDown is True:
    if player["x"] > 0 and player["x"] - 5 > 0:
      player["x"] -= 5
    elif player["x"] > 0 and player["x"] - 5 < 0:
      player["x"] = 0

  if rightDown is True:
    if player["x"] + player["width"] < windowWidth and (player["x"] + player["width"]) + 5 < windowWidth:
      player["x"] += 5
    elif player["x"] + player["width"] < windowWidth and (player["x"] + player["width"]) + 5 > windowWidth:
      player["x"] = windowWidth - player["width"]

def createPlatform():

  global lastPlatform, platformDelay

  platformY = windowHeight
  gapPosition = random.randint(0, windowWidth - 40)

  gamePlatforms.append({"pos" : [0, platformY], "gap" : gapPosition})
  lastPlatform = GAME_TIME.get_ticks()

  if platformDelay > 800:
    platformDelay -= 50

def movePlatforms():
  # print("Platforms")

  for idx, platform in enumerate(gamePlatforms):

    platform["pos"][1] -= platformSpeed

    if platform["pos"][1] < -10:
      gamePlatforms.pop(idx)
      

def drawPlatforms():

  for platform in gamePlatforms:

    pygame.draw.rect(surface, (255,255,255), (platform["pos"][0], platform["pos"][1], windowWidth, 10))
    pygame.draw.rect(surface, (0,0,0), (platform["gap"], platform["pos"][1], 40, 10) )


def gameOver():
  global gameStarted, gameEnded

  platformSpeed = 0
  gameStarted = False
  gameEnded = True

def restartGame():

  global gamePlatforms, player, gameBeganAt, platformsDroppedThrough, platformDelay

  gamePlatforms = []
  player["x"] = windowWidth / 2
  player["y"] = 0
  gameBeganAt = GAME_TIME.get_ticks()
  platformsDroppedThrough = -1
  platformDelay = 2000

def quitGame():
  pygame.quit()
  sys.exit()

# 'main' loop
while True:

  surface.fill((0,0,0))

  for event in GAME_EVENTS.get():

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_LEFT:
        leftDown = True
        wasMovingToTheLeft = True
      if event.key == pygame.K_RIGHT:
        rightDown = True
        wasMovingToTheLeft = False
      if event.key == pygame.K_ESCAPE:
        quitGame()

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        leftDown = False
      if event.key == pygame.K_RIGHT:
        rightDown = False

      if event.key == pygame.K_SPACE:
        if gameStarted == False:
          restartGame()
          gameStarted = True

    if event.type == GAME_GLOBALS.QUIT:
      quitGame()

  if gameStarted is True:
    # Play game
    timer = GAME_TIME.get_ticks() - gameBeganAt

    movePlatforms()
    drawPlatforms()
    movePlayer()
    setFrameNumber()
    drawPlayer()

  elif gameEnded is True:
    # Draw game over screen
    surface.blit(game_over_image, (0, 150))
    # show score - number of platforms traversed
    font = pygame.font.Font("assets/ZenDots-Regular.ttf", 32) # load font from asset folder - can get fonts from Google fonts
    score = font.render("High Score: " + str(platformsDroppedThrough), True, (255, 255, 255))
    surface.blit(score, (50, 250))

  else :
    # Welcome Screen
    surface.blit(title_image, (0, 150))

  if GAME_TIME.get_ticks() - lastPlatform > platformDelay:
    createPlatform()

  clock.tick(60)
  frameTimer += 1 # increment frameTimer
  # print(str(platformsDroppedThrough)) # figuring out what this variable does
  pygame.display.update()
