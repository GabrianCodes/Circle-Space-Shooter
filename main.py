import pygame, sys
from random import randint, uniform


def laser_update(laser_list, speed = 900):
	for rect in laser_list:
		rect.y -= speed*dt
		if rect.bottom < 0:
			laser_list.remove(rect)


def display_survival_time():
	survival_time = f'Survival Time: {pygame.time.get_ticks() // 1000}'
	text_surface = font.render(survival_time, True, (255,0,0))
	text_rectangle = text_surface.get_rect(center = (WINDOW_WITDH/2, WINDOW_HEIGHT -100))
	pygame.draw.rect(display_surface, (255,0,0), text_rectangle.inflate(10,10), width = 5, border_radius = 5)
	display_surface.blit(text_surface, text_rectangle)

def laser_timer(can_shoot, duration = 600):
	if not can_shoot:
		current_time = pygame.time.get_ticks()
		if current_time - shoot_time > duration:
			can_shoot = True
	return can_shoot

def circle_update(circle_list, speed = 800):
	for circle_tuple in circle_list:
		direction = circle_tuple[1]
		circle_rectangle = circle_tuple[0]
		circle_rectangle.center += direction * speed * dt 

		if circle_rectangle.top > WINDOW_HEIGHT:
			circle_list.remove(circle_tuple)

#game init
pygame.init()
WINDOW_WITDH, WINDOW_HEIGHT = 1920, 1080
display_surface = pygame.display.set_mode((WINDOW_WITDH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Mission")
clock = pygame.time.Clock()


#ship import
ship_surface = pygame.image.load('.\\graphics\\ship.png').convert_alpha()
ship_y_position = 400
ship_rectangle = ship_surface.get_rect(center = (WINDOW_WITDH/2, WINDOW_HEIGHT/2))
#laser import
laser_surface = pygame.image.load('.\\graphics\\laser.png')
laser_list = []
#circle import
circle_surface = pygame.image.load('.\\graphics\\circle.png')
circle_list = []
#laser timer
can_shoot = True
shoot_time = pygame.time.get_ticks()

laser_rectangle = laser_surface.get_rect(midbottom = ship_rectangle.midtop)

#circle Timer

circle_timer = pygame.event.custom_type()
pygame.time.set_timer(circle_timer,500)

#background import
background = pygame.image.load('.\\graphics\\background.png').convert()
background_scale = pygame.transform.scale(background,(WINDOW_WITDH,WINDOW_HEIGHT))

#text
font = pygame.font.Font('.\\graphics\\subatomic.ttf',50)



test_rect = pygame.Rect(100,200,400,500)

laser_sound = pygame.mixer.Sound('.\\sounds\\laser.ogg')
explosion_sound = pygame.mixer.Sound('.\\sounds\\explosion.wav')
background_sound = pygame.mixer.Sound('.\\sounds\\music.wav')

while True:

	#event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
			laser_rectangle = laser_surface.get_rect(midbottom = ship_rectangle.midtop)
			laser_list.append(laser_rectangle)

			can_shoot = False
			shoot_time = pygame.time.get_ticks()
			laser_sound.play()

		if event.type == circle_timer:


			x_position = randint(-100, WINDOW_WITDH + 100)
			y_position = randint (-150, - 100)
			circle_rectangle = circle_surface.get_rect(center = (x_position,y_position))
			direction = pygame.math.Vector2(uniform(-0.5, 0.5),1)
			circle_list.append((circle_rectangle,direction))


	
	


	#framerate limit
	dt = clock.tick(120) / 1000

	#input
	ship_rectangle.center = pygame.mouse.get_pos()
	press = pygame.mouse.get_pressed()
	
	laser_update(laser_list)
	circle_update(circle_list)
	can_shoot = laser_timer(can_shoot, 400)

	for circle_tuple in circle_list:
		circle_rectangle = circle_tuple[0]
		if ship_rectangle.colliderect(circle_rectangle):
			pygame.quit()
			sys.exit()


	for laser_rectangle in laser_list:
		for circle_tuple in circle_list:
			if laser_rectangle.colliderect(circle_tuple[0]):
				circle_list.remove(circle_tuple)
				laser_list.remove(laser_rectangle)
				explosion_sound.play()

	


	#updating the display (drawing)
	display_surface.fill((0,0,0))
	display_surface.blit(background_scale,(0,0))

	display_survival_time()
	

	for rect in laser_list:
		display_surface.blit(laser_surface, rect)

	for circle_tuple in circle_list:
		display_surface.blit(circle_surface, circle_tuple[0])


	display_surface.blit(ship_surface, ship_rectangle)


	
	#final frame
	pygame.display.update()
