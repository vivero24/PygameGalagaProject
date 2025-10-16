import pygame
class Player:
    def __init__(self, pos):
        self.pos = list(pos)
        self.velocity = [0,0]
        self.speed = 3
        self.lives = 3
        self.heart_image = pygame.image.load("assets/heart.png")
        self.animation_images = []
        self.animation_images.append(pygame.image.load("assets/ship1.png"))
        self.animation_images.append(pygame.image.load("assets/ship2.png"))
        self.animation_images.append(pygame.image.load("assets/ship3.png"))
        self.animation_images.append(pygame.image.load("assets/ship4.png"))
        self.current_image = 0
        self.image = self.animation_images[self.current_image]
        self.rect = self.image.get_rect()

    def update(self, movement = (0,0)):
        self.current_image += 1
        if self.current_image  >= len(self.animation_images):
            self.current_image = 0
        self.image = self.animation_images[self.current_image]

        frame_movement = (movement[0] + self.velocity[0], self.speed * (movement[1] + self.velocity[1]))
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def render(self, surf):
        surf.blit(self.animation_images[self.current_image], self.pos)
    
    def render_lives(self, surf):
        x = 132
        for i in range(self.lives):
            surf.blit(self.heart_image, (x, 24))
            x += 32


