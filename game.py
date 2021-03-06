import pygame
import time
import random

from pygame.locals import*
from time import sleep

############################
########## Mario ###########
############################
class Mario():
	def __init__(self, model):
		self.model = model
		self.x = 0
		self.y = 0
		self.model.scrollPos = self.x - 350
		self.prev_x = 0
		self.prev_y = 0
		self.w = 60
		self.h = 95
		self.vvel = 0
		self.mframe = 0
		self.facingRight = True
		self.runningRight = False
		self.runningLeft = False
		self.onTop = False
		self.marioPics = []
		self.marioPics.append(pygame.image.load("mario1.png"))
		self.marioPics.append(pygame.image.load("mario2.png"))
		self.marioPics.append(pygame.image.load("mario3.png"))
		self.marioPics.append(pygame.image.load("mario4.png"))
		self.marioPics.append(pygame.image.load("mario5.png"))
		self.marioPics.append(pygame.image.load("mario1left.png"))
		self.marioPics.append(pygame.image.load("mario2left.png"))
		self.marioPics.append(pygame.image.load("mario3left.png"))
		self.marioPics.append(pygame.image.load("mario4left.png"))
		self.marioPics.append(pygame.image.load("mario5left.png"))

	def collision(self, x, y, w, h):
		if self.x + self.w <= x:
			return False
		if self.x >= x + w:
			return False
		if self.y + self.h <= y:
			return False
		if self.y >= y + h:
			return False
		return True

	def leaveBlock(self, x, y, w, h):
		if self.y + self.h > y and self.prev_y + self.h <= y:
			self.vvel = 0
			self.y = y - self.h
			self.onTop = True
		if self.y < y + h and self.prev_y >= y + h:
			self.y = y + h
			self.vvel = 0.1
		if self.x + self.y > x and self.prev_x + self.w <= x:
			self.runningRight = False
			self.model.scrollPos = x - 350 - self.w
			self.x = x - self.w
		if self.x < x + w and self.prev_x >= x + w:
			self.runningLeft = False
			self.model.scrollPos = x - 350 + w
			self.x = x + w

	def notePrevious(self):
		self.prev_x = self.x
		self.prev_y = self.y

	def update(self):
		#gravity
		self.vvel += 3.14159
		self.y += self.vvel

		#ground
		if self.y > 355:
			self.y = 355
			self.vvel = 0

		#run
		if self.runningLeft:
			self.x -= 10
			self.model.scrollPos -= 10
			self.facingRight = False
		if self.runningRight:
			self.x +=10
			self.model.scrollPos += 10
			self.facingRight = True

		#collision detection
		if self.collision(self.model.brick1.x, self.model.brick1.y, self.model.brick1.w, self.model.brick1.h):
			self.leaveBlock(self.model.brick1.x, self.model.brick1.y, self.model.brick1.w, self.model.brick1.h)
		if self.collision(self.model.brick2.x, self.model.brick2.y, self.model.brick2.w, self.model.brick2.h):
			self.leaveBlock(self.model.brick2.x, self.model.brick2.y, self.model.brick2.w, self.model.brick2.h)
		if self.collision(self.model.coinBlock1.x, self.model.coinBlock1.y, self.model.coinBlock1.w, self.model.coinBlock1.h):
			self.leaveBlock(self.model.coinBlock1.x, self.model.coinBlock1.y, self.model.coinBlock1.w, self.model.coinBlock1.h)
		if self.collision(self.model.coinBlock2.x, self.model.coinBlock2.y, self.model.coinBlock2.w, self.model.coinBlock2.h):
			self.leaveBlock(self.model.coinBlock2.x, self.model.coinBlock2.y, self.model.coinBlock2.w, self.model.coinBlock2.h)

############################
########## Brick ###########
############################
class Brick():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = 100
		self.h = 100
		self.brickPic = pygame.image.load("Brick_Block.png")

############################
######## CoinBlock #########
############################
class CoinBlock():
	def __init__(self, model, x, y):
		self.x = x
		self.y = y
		self.w = 90
		self.h = 90
		self.coinCount = 5
		self.model = model
		self.coinBlockPic = pygame.image.load("coinBlock2.png")
		self.emptyCoinBlockPic = pygame.image.load("emptyCoinBlock2.png")

	def update(self):
		if(self.model.mario.y == self.y + self.h and self.model.mario.x + self.model.mario.w > self.x and self.model.mario.x < self.x + self.w):
			if self.coinCount > 0:
				self.vvelocity = -30.0
				self.n = random.randint(1, 50)
				if self.n%2 == 0:
					self.hvelocity = self.n%15
				else:
					self.hvelocity = -(self.n%15)

				self.model.coins.append(Coin(self.hvelocity, self.vvelocity, self.x, self.y, self.model))
				self.coinCount -= 1

############################
########## Coin ############
############################
class Coin():
	def __init__(self, hvel, vvel, x, y, model):
		self.x = x
		self.y = y
		self.w = 0
		self.h = 0
		self.hvel = hvel
		self.vvel = vvel
		self.model = model
		self.coinPic = pygame.image.load("coin.png")

	def update(self):
		self.vvel += 3.14159
		self.y += self.vvel
		self.x += self.hvel
		if self.y > 1000:
			self.vvel = 0
			self.hvel = 0
			self.y = 1000

############################
########## Model ###########
############################
class Model():
	def __init__(self):
		self.scrollPos = 0
		self.mario = Mario(self)
		self.brick1 = Brick(100, 200)
		self.brick2 = Brick(600, 350)
		self.coinBlock1 = CoinBlock(self, 900, 200)
		self.coinBlock2 = CoinBlock(self, 1200, 230)
		self.coins = list(())

	def update(self):
		self.mario.update()
		self.coinBlock1.update()
		self.coinBlock2.update()
		for i in range(len(self.coins)):
				self.coins[i].update()

############################
########## View ############
############################
class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.model.rect = self.model.mario.marioPics[0].get_rect()
		self.model.rect = self.model.brick1.brickPic.get_rect()

	def update(self):
		#draw the sky(sunny)
		self.screen.fill([0,200,200])

		#draw the ground
		pygame.draw.rect(self.screen, (0, 128, 0), (0, 450, 800, 600))

		#draw bricks
		self.screen.blit(self.model.brick1.brickPic, (self.model.brick1.x - self.model.scrollPos, self.model.brick1.y), self.model.rect)
		self.screen.blit(self.model.brick2.brickPic, (self.model.brick2.x - self.model.scrollPos, self.model.brick2.y), self.model.rect)

		#draw coin blocks
		if self.model.coinBlock1.coinCount > 0:
			self.screen.blit(self.model.coinBlock1.coinBlockPic, (self.model.coinBlock1.x - self.model.scrollPos, self.model.coinBlock1.y), self.model.rect)
		else:
			self.screen.blit(self.model.coinBlock1.emptyCoinBlockPic, (self.model.coinBlock1.x - self.model.scrollPos, self.model.coinBlock1.y), self.model.rect)
		if self.model.coinBlock2.coinCount > 0:
			self.screen.blit(self.model.coinBlock2.coinBlockPic, (self.model.coinBlock2.x - self.model.scrollPos, self.model.coinBlock2.y), self.model.rect)
		else:
			self.screen.blit(self.model.coinBlock2.emptyCoinBlockPic, (self.model.coinBlock2.x - self.model.scrollPos, self.model.coinBlock2.y), self.model.rect)

		#draw the coins
		for i in range(len(self.model.coins)):
			self.screen.blit(self.model.coins[i].coinPic, (self.model.coins[i].x - self.model.scrollPos, self.model.coins[i].y - 30), self.model.rect)

		#animate mario
		if self.model.mario.facingRight: #if he's facing right, animate right

			#increment mframe
			self.model.mario.mframe+=1
			if self.model.mario.mframe > 4: self.model.mario.mframe = 0

			#if keyRight and mario is on a surface, draw him running
			if self.model.mario.runningRight and (self.model.mario.onTop or self.model.mario.y == 355):
  				self.screen.blit(self.model.mario.marioPics[self.model.mario.mframe], (350, self.model.mario.y), self.model.rect)

			#else draw him standing still
			else: self.screen.blit(self.model.mario.marioPics[3], (350, self.model.mario.y), self.model.rect)

		else: #if he's facing left,  animate left

			#increment mframe
			self.model.mario.mframe+=1
			if self.model.mario.mframe < 5 or self.model.mario.mframe > 9: self.model.mario.mframe = 5

			#if keyLeft and mario is on a surface, draw him running
			if self.model.mario.runningLeft and (self.model.mario.onTop or self.model.mario.y == 355):
  				self.screen.blit(self.model.mario.marioPics[self.model.mario.mframe], (350, self.model.mario.y), self.model.rect)

			#else draw him standing still
			else: self.screen.blit(self.model.mario.marioPics[7], (350, self.model.mario.y), self.model.rect)

		#idk
		pygame.display.flip()

############################
####### Controller #########
############################
class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
		keys = pygame.key.get_pressed()
		self.model.mario.notePrevious()
		self.model.mario.runningRight = False
		self.model.mario.runningLeft = False

		if keys[K_LEFT]:
			self.model.mario.runningLeft = True
		if keys[K_RIGHT]:
			self.model.mario.runningRight = True
		if keys[K_SPACE] and (self.model.mario.y == 355 or self.model.mario.onTop) and self.model.mario.vvel == 0:
			self.model.mario.vvel = -35

############################
########## Main ############
############################
print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")
