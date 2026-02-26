import pygame


pygame.init();
window = pygame.display.set_mode((1024, 980))

while True:
    # Check todos os eventos
    for event in pygame.event.get():
        quitting = event.type == pygame.QUIT
        if quitting:
            pygame.quit()
            quit()
    pass
