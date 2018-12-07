import pygame
import time

from pygame.locals import*
from time import sleep



class Mario():
	def __init__(self):
		self.x = 0;
		self.y = 0;

	def update(self):
		self.y = 0;



class Model():
	def __init__(self):
		self.mario = Mario();

	def update(self):
		self.mario.update();



class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.mario1 = pygame.image.load("mario1.png")
		self.model = model
		self.model.rect = self.mario1.get_rect()

	def update(self):
		self.screen.fill([0,200,200])#draw the sky(sunny)
		pygame.draw.rect(self.screen, (0, 128, 0), (0, 450, 800, 600))#draw the ground
		self.screen.blit(self.mario1, self.model.rect)#draw mario
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
		#if keys[K_LEFT]:
		#	self.model.dest_x -= 1
		#if keys[K_RIGHT]:
		#	self.model.dest_x += 1



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
