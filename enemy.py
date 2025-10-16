import pygame

class Enemy():
    default_speed = 2
    def __init__(self, pos):
        self.pos = list(pos)
        self.image = pygame.image.load("assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (64, 32))
        self.speed = Enemy.default_speed
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        
        self.hit = False
        self.death_images = []
        self.death_images.append(pygame.transform.scale(pygame.image.load("assets/enemy_death1.png"), (64, 32)))
        self.death_images.append(pygame.transform.scale(pygame.image.load("assets/enemy_death2.png"), (64, 32)))
        self.death_images.append(pygame.transform.scale(pygame.image.load("assets/enemy_death3.png"), (64, 32)))
        self.death_images.append(pygame.transform.scale(pygame.image.load("assets/enemy_death4.png"), (64, 32)))
        self.death_images.append(pygame.transform.scale(pygame.image.load("assets/enemy_death5.png"), (64, 32)))
        
        
        self.current_death_image = 0
        
        

    def update(self):
        if self.hit == True:
            self.image = self.death_images[self.current_death_image]
            self.current_death_image += 1
            if self.current_death_image >= len(self.death_images):
                self.current_death_image = 0
        else:
            self.pos[0] -= Enemy.default_speed
            self.rect.x = self.pos[0]


    def render(self, surf):
        surf.blit(self.image, self.pos)
       

