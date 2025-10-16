import pygame
class Projectile:
    def __init__(self,  pos, width, height):
        self.pos = list(pos)
        self.width = width
        self.height = height
        self.speed = 8
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    

    def render(self, surf):
        pygame.draw.rect(surf, self.color, pygame.Rect(self.pos[0], self.pos[1], self.width, self.height))
        