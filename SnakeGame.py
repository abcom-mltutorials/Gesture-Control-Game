# Copyright @ 2020 ABCOM Information Systems Pvt. Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import random
import pygame
import sys
from pygame.locals import *
from settingsSnakeFun import *

def main():
	global CLOCK, SCREEN, FONT

	pygame.init()
	CLOCK = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((Width_window, height_window))
	FONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Snake Game')

	showStartScreen()
	while True:

		runGame()

		showGameOverScreen()

def runGame():
	#to set a random starting point in the game
	startx = random.randint(5, cell_width - 6)
	starty = random.randint(5, cell_height - 6)
	global worm
	worm = [{'x' : startx, 'y' : starty}, {'x': startx - 1, 'y':starty}, {'x':startx - 2, 'y':starty}]
	direction = UP

	food = getRandomLocation()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()

		#To check Collision with edges
		if worm[HEAD]['x'] == -1 or worm[HEAD]['x'] == cell_width or worm[HEAD]['y'] == -1 or worm[HEAD]['y'] == cell_height:
			return
		#To check Collision with snake's body
		for wormBody in worm[1:]:
			if wormBody['x'] == worm[HEAD]['x'] and wormBody['y'] == worm[HEAD]['y']:
				return
		#Check Collision with food
		if worm[HEAD]['x'] == food['x'] and worm[HEAD]['y'] == food['y']:

			food = getRandomLocation()
		else:
			del worm[-1]

#To move the Snake
		if direction == UP:
			newHead = {'x': worm[HEAD]['x'], 'y': worm[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': worm[HEAD]['x'], 'y': worm[HEAD]['y'] + 1}
		elif direction == RIGHT:
			newHead = {'x': worm[HEAD]['x'] + 1, 'y': worm[HEAD]['y']}
		elif direction == LEFT:
			newHead = {'x': worm[HEAD]['x'] - 1, 'y': worm[HEAD]['y']}
		worm.insert(0, newHead)

#for drawing the game Screen
		SCREEN.fill(BGCOLOR)
		drawGrid()
		drawWorm(worm)
		drawfood(food)
		drawScore((len(worm) - 3) * 10)
		pygame.display.update()
		CLOCK.tick(FPS)
#to calculate the score of the game
def getTotalScore():
	return ((len(worm) - 3) * 10)

def drawPressKeyMsg():
	pressKeyText = FONT.render('Tap to play', True,GREEN)
	pressKeyRect = pressKeyText.get_rect()
	pressKeyRect.center = (Width_window - 200, height_window - 100)
	SCREEN.blit(pressKeyText, pressKeyRect)

def drawSettingsMsg():
	SCREEN.blit(SETTINGSBUTTON, (Width_window - SETTINGSBUTTON.get_width(), height_window - SETTINGSBUTTON.get_height()))

def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key

def showStartScreen():
	titlefont = pygame.font.Font('freesansbold.ttf', 100)
	titleText = titlefont.render('SNAKE GAME', True,RED)
	while True:
		SCREEN.fill(BGCOLOR)
		titleTextRect = titleText.get_rect()
		titleTextRect.center = (Width_window / 2, height_window / 2)
		SCREEN.blit(titleText, titleTextRect)

		drawPressKeyMsg()
		if checkForKeyPress():
			pygame.event.get()
			return
		pygame.display.update()
		CLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

def getRandomLocation():
	return {'x': random.randint(0, cell_width - 1), 'y': random.randint(0, cell_height - 1)}

def showGameOverScreen():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
	gameOverText = gameOverFont.render('Game Over', True, GREEN)
	gameOverRect = gameOverText.get_rect()
	totalscoreFont = pygame.font.Font('freesansbold.ttf', 40)
	totalscoreText = totalscoreFont.render('Total Score: %s' % (getTotalScore()), True, YELLOW)
	totalscoreRect = totalscoreText.get_rect()
	totalscoreRect.midtop = (Width_window /2, 150)
	gameOverRect.midtop = (Width_window /2, 30)
	SCREEN.fill(BGCOLOR)
	SCREEN.blit(gameOverText, gameOverRect)
	SCREEN.blit(totalscoreText, totalscoreRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(1000)
	checkForKeyPress()

	while True:
		if checkForKeyPress():
			pygame.event.get()
			return

def drawScore(score):
	scoreText = FONT.render('Score: %s' % (score), True, GREEN)
	scoreRect = scoreText.get_rect()
	scoreRect.center = (Width_window  - 100, 30)
	SCREEN.blit(scoreText, scoreRect)

def drawWorm(worm):
	x = worm[HEAD]['x'] * size_cell
	y = worm[HEAD]['y'] * size_cell
	wormHeadRect = pygame.Rect(x, y, size_cell, size_cell)
	pygame.draw.rect(SCREEN, DARKGRAY, wormHeadRect)

	for coord in worm[1:]:
		x = coord['x'] * size_cell
		y = coord['y'] * size_cell
		wormSegmentRect = pygame.Rect(x, y, size_cell, size_cell)
		pygame.draw.rect(SCREEN, RED, wormSegmentRect)

def drawfood(coord):
	x = coord['x'] * size_cell
	y = coord['y'] * size_cell
	appleRect = pygame.Rect(x, y, size_cell, size_cell)
	pygame.draw.rect(SCREEN, DARKGREEN, appleRect)

def drawGrid():
	for x in range(0, Width_window, size_cell):
		pygame.draw.line(SCREEN, RED, (x, 0), (x, height_window))
	for y in range(0, height_window, size_cell):
		pygame.draw.line(SCREEN, RED, (0, y), (Width_window, y))

if __name__ == '__main__':
	main()
