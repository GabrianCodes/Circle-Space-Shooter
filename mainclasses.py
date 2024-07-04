import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
	def __init__(self,group):
		super().__init__(group)
		self.image = pygame.image.load('.\\graphics\\ship.png').convert_alpha()
		self.rect = self.image.get_rect(center = (WINDOW_WITDH/2, WINDOW_HEIGHT/2))
		self.can_shoot = True
		self.shoot_time = None

	def laser_timer(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > 500:
				self.can_shoot = True

	def input_position(self):
		position = pygame.mouse.get_pos()
		self.rect.center = position

	def laser_shoot(self):
		if pygame.mouse.get_pressed()[0] and self.can_shoot:
			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()

			Laser(self.rect.midtop, laser_group)

	def update(self):
		self.laser_timer()
		self.laser_shoot()
		self.input_position()


class Laser(pygame.sprite.Sprite):
	def __init__(self,position,group):
		super().__init__(group)
		self.image = pygame.image.load('.\\graphics\\laser.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = position)
		self.position = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(0,-1)
		self.speed = 600

	def update(self):
		self.position += self.direction * self.speed * dt 
		self.rect.topleft = (round(self.position.x),round(self.position.y))

class Circle(pygame.sprite.Sprite):
	def __init__(self,position,group):

		super().__init__(group)
		self.image = pygame.image.load('.\\graphics\\circle.png').convert_alpha()
		self.rect = self.image.get_rect(center = position)

		self.position = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
		self.speed = randint(300,900)

	def update(self):
		self.position += self.direction * self.speed * dt 
		self.rect.topleft = (round(self.position.x),round(self.position.y))

class Score:
	def __init__(self):
		self.font = pygame.font.Font ('.\\graphics\\subatomic.ttf',50)

	def display(self):
		survival_time = f'Survival Time: {pygame.time.get_ticks() // 1000}'
		text_surface = self.font.render(survival_time, True, (255,0,0))
		text_rectangle = text_surface.get_rect(center = (WINDOW_WITDH/2, WINDOW_HEIGHT -100))
		pygame.draw.rect(display_surface, (255,0,0), text_rectangle.inflate(10,10), width = 5, border_radius = 5)
		display_surface.blit(text_surface, text_rectangle)





pygame.init()
WINDOW_WITDH, WINDOW_HEIGHT = 1920, 1080
display_surface = pygame.display.set_mode((WINDOW_WITDH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Mission")
clock = pygame.time.Clock()

#background
background = pygame.image.load('.\\graphics\\background.png').convert()
background_scale = pygame.transform.scale(background,(WINDOW_WITDH,WINDOW_HEIGHT))


# sprite groups

spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
circle_group = pygame.sprite.Group()

#sprite creation
ship = Ship(spaceship_group)

circle_timer = pygame.event.custom_type()
pygame.time.set_timer(circle_timer, 500)

survival_time = Score()

while True:

	#event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == circle_timer:
			circle_y_position = randint(-150, -50)
			circle_x_position = randint(-100, WINDOW_WITDH + 100)
			Circle((circle_x_position, circle_y_position), group = circle_group)

	dt = clock.tick() / 1000


	#background
	display_surface.blit(background_scale,(0,0))
	spaceship_group.update()
	laser_group.update()
	circle_group.update()
	#graphics
	survival_time.display()

	spaceship_group.draw(display_surface)
	laser_group.draw(display_surface)
	circle_group.draw(display_surface)




	pygame.display.update()