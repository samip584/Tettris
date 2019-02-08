import pygame

pygame.font.init()

screen = pygame.display.set_mode((400, 400))
count = 0

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
while True:
		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				sys.exit()
			for font in pygame.font.get_fonts():
				screen.fill((135,206,250))
				largeText = pygame.font.SysFont(font, 20)
				TextSurf, TextRect = text_objects( font.upper(), largeText, (255,69,5))
				TextRect.center = ((200, 30))
				screen.blit(TextSurf, TextRect)
				pygame.display.update()
				asd = input()
	