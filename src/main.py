import pygame
from src.game_objects import Markers, Marker
from src.geometry import SinePattern, MouseBased

pygame.init()
window_dimensions = (1200, 600)
window = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption('PatternModul8')
frames_per_second = 60
clock = pygame.time.Clock()

background = pygame.Surface(window.get_size())
background = background.convert()
background.fill((79, 78, 75))

window.blit(background, (0, 0))
pygame.display.flip()

running = True

markers = Markers(
    pattern=SinePattern(
        amplitude=120,
        duration=4000,
        time=pygame.time,
        dimensions=window_dimensions,
        modulation=MouseBased(
            window_dimensions[0],
            'x',
            pygame.mouse)))
for i in range(32):
    Marker(markers)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    markers.update()

    window.blit(background, (0, 0))
    markers.draw(window)
    pygame.display.flip()
    pygame.event.pump()
    # pygame.display.update()
    clock.tick(frames_per_second)
