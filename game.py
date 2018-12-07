import pygame
import time

from pygame.locals import*
from time import sleep



class Mario():
	def __init__(self, model):
		self.model = model
		self.x = 0
		self.y = 0
		self.vvel = 0
		self.mario1 = pygame.image.load("mario1.png")


	def update(self):
		self.vvel += 3.14159
		self.y += self.vvel

		if self.y > 355:
			self.y = 355



class Model():
	def __init__(self):
		self.mario = Mario(self)

	def update(self):
		self.mario.update()



class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.model.rect = self.model.mario.mario1.get_rect()

	def update(self):
		self.screen.fill([0,200,200])#draw the sky(sunny)
		pygame.draw.rect(self.screen, (0, 128, 0), (0, 450, 800, 600))#draw the ground
		self.screen.blit(self.model.mario.mario1, (self.model.mario.x, self.model.mario.y), self.model.rect)#draw mario
		pygame.display.flip()



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
		if keys[K_LEFT]:
			self.model.mario.x -= 10
		if keys[K_RIGHT]:
			self.model.mario.x += 10
		if keys[K_SPACE] and self.model.mario.y == 355:
			self.model.mario.vvel = -30



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
