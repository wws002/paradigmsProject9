import pygame
import time

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

	def update(self):
		#gravity
		self.vvel += 3.14159
		self.y += self.vvel

		#ground
		if self.y > 355:
			self.y = 355

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
########## Model ###########
############################
class Model():
	def __init__(self):
		self.mario = Mario(self)
		self.brick1 = Brick(100, 200)
		self.brick2 = Brick(600, 350)

	def update(self):
		self.mario.update()

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
		self.screen.blit(self.model.brick1.brickPic, (self.model.brick1.x, self.model.brick1.y), self.model.rect)
		self.screen.blit(self.model.brick2.brickPic, (self.model.brick2.x, self.model.brick2.y), self.model.rect)

		#animate mario
		if self.model.mario.facingRight: #if he's facing right, animate right

			#increment mframe
			self.model.mario.mframe+=1
			if self.model.mario.mframe > 4: self.model.mario.mframe = 0

			#if keyRight and mario is on a surface, draw him running
			if self.model.mario.runningRight and (self.model.mario.onTop or self.model.mario.y == 355):
  				self.screen.blit(self.model.mario.marioPics[self.model.mario.mframe], (self.model.mario.x, self.model.mario.y), self.model.rect)

			#else draw him standing still
			else: self.screen.blit(self.model.mario.marioPics[3], (self.model.mario.x, self.model.mario.y), self.model.rect)

		else: #if he's facing left,  animate left

			#increment mframe
			self.model.mario.mframe+=1
			if self.model.mario.mframe < 5 or self.model.mario.mframe > 9: self.model.mario.mframe = 5

			#if keyLeft and mario is on a surface, draw him running
			if self.model.mario.runningLeft and (self.model.mario.onTop or self.model.mario.y == 355):
  				self.screen.blit(self.model.mario.marioPics[self.model.mario.mframe], (self.model.mario.x, self.model.mario.y), self.model.rect)

			#else draw him standing still
			else: self.screen.blit(self.model.mario.marioPics[7], (self.model.mario.x, self.model.mario.y), self.model.rect)

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
		self.model.mario.runningRight = False
		self.model.mario.runningLeft = False

		if keys[K_LEFT]:
			self.model.mario.x -= 10
			self.model.mario.runningLeft = True
			self.model.mario.facingRight = False
		if keys[K_RIGHT]:
			self.model.mario.x += 10
			self.model.mario.runningRight = True
			self.model.mario.facingRight = True
		if keys[K_SPACE] and self.model.mario.y == 355:
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
