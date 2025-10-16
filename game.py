import pygame
import sys
from player import Player
from projectile import Projectile
import random
from enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Python Project")
        self.screen_res = (640, 480)
        self.screen = pygame.display.set_mode(self.screen_res)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/gameFont.ttf", 32)
        self.background = pygame.image.load("assets/background2.jpg").convert()
        self.background = pygame.transform.scale(self.background, ((self.screen_res)))
        self.spawn_time = 180
        self.laser_sound = pygame.mixer.Sound("assets/laserSound.mp3")
        self.explode_sound = pygame.mixer.Sound("assets/explosionSound.mp3")

        self.formations = {
            'single' : [(self.screen_res[0], 240)],
            'double' : [(self.screen_res[0], 200),(self.screen_res[0], 250)],
            'line' : [(self.screen_res[0], 100), (self.screen_res[0], 200), (self.screen_res[0], 300), (self.screen_res[0], 400)],
            'v-shape' : [(self.screen_res[0], 100), (self.screen_res[0] + 50, 200), (self.screen_res[0] + 50 , 300), (self.screen_res[0], 400)],
            'zig-zag' : [(self.screen_res[0], 100), (self.screen_res[0] + 100, 200), (self.screen_res[0], 300), (self.screen_res[0] + 100, 400)]
        }

    def run(self):

        self.player = Player( (50, 200))
        self.movement = [False, False]
        self.projectiles = []
        self.enemies = []
        self.spawn_timer = 0
        self.difficulty_timer = 0
        self.running = True
        self.score = 0
        

        collision_ended = False
        scroll = 0

        while self.running:
            if self.player.lives <= 0: # game over
                game_over = True
                self.running = False
            else:
                current_collision = False
                life_counter = self.font.render("Lives: ", True,(255, 255, 255))
                life_counter_rect = life_counter.get_rect(topleft = (16, 16))
                score_counter = self.font.render("Score: " + str(self.score), True,(255, 255, 255))
                score_counter_rect = score_counter.get_rect(topleft = (400, 16))
                self.screen.fill((0, 0 , 155))                
                self.screen.blit(self.background, (scroll, 0)) 
                self.screen.blit(self.background, (scroll + self.background.get_width() , 0))
                scroll -= 5
                self.spawn_timer += 1
                self.difficulty_timer += 1
                

                if abs(scroll) >= self.background.get_width(): #redrawing screen to emulate endless scroll
                    scroll = 0 

                if self.spawn_timer >= self.spawn_time: # enemy generation
                    formation = random.choice(list(self.formations.keys()))
                    for pos in self.formations[formation]:
                        enemy = Enemy(pos)
                        self.enemies.append(enemy)
                    self.spawn_timer = 0

                
                if self.difficulty_timer >= 30000:
                    Enemy.default_speed += 0.25
                    self.spawn_time -= 5
                    self.difficulty_timer = 0

                
                for enemy in self.enemies[:]: # enemy collision detection against player and player projectiles
                    enemy.render(self.screen)
                    enemy.update()


                    if enemy.rect.colliderect(self.player.rect):
                        current_collision = True
                        if not collision_ended:
                            self.player.lives -= 1
                            self.enemies.remove(enemy)
                            print(self.player.lives)
                        continue  
                    if enemy.pos[0] < -50:
                        self.enemies.remove(enemy)
                        continue
                    
                    for projectile in self.projectiles[:]:
                        if projectile.rect.colliderect(enemy.rect):
                            if enemy in self.enemies and not enemy.hit:
                                self.explode_sound.play()
                                enemy.hit = True
                                self.score += 10
                            if projectile in self.projectiles:
                                self.projectiles.remove(projectile)
                            break

                    if enemy.hit == True and enemy.current_death_image >= len(enemy.death_images) - 1:
                        self.enemies.remove(enemy)
                    
                collision_ended = current_collision # end of enemy collision checks

                self.player.render(self.screen)
                self.screen.blit(life_counter, life_counter_rect) # rendering
                self.player.render_lives(self.screen)
                self.screen.blit(score_counter, score_counter_rect)

                for projectile in self.projectiles:
                    projectile.render(self.screen)

                for projectile in self.projectiles: 
                    if projectile.pos[0] < self.screen_res[0] and projectile.pos[0] > 0:
                        projectile.pos[0] += projectile.speed
                        projectile.rect[0] += projectile.speed

                    else:
                        self.projectiles.pop(self.projectiles.index(projectile))
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.movement[0] = True
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = True
                        if event.key == pygame.K_SPACE:
                            if len(self.projectiles) < 5:
                                self.projectiles.append(Projectile((round(self.player.pos[0] + self.player.rect.width // 2), round(self.player.pos[1] + self.player.rect.height //2)) , 8,4))
                                self.laser_sound.play()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.movement[0] = False
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = False
                
                if self.player.pos[1] + self.player.rect.height > self.screen_res[1]:
                    self.player.pos[1] = self.screen_res[1] - self.player.rect.height
                elif self.player.pos[1] < 0:
                    self.player.pos[1] = 0
                
                self.player.update((0,self.movement[1] - self.movement[0]))
                pygame.display.update()
                self.clock.tick(60)
        if game_over:
            self.game_over()
        

    def game_over(self):
        waiting = True
        while waiting:
            color = (255, 255, 255)
            text = self.font.render("Game Over. Your score was " + str(self.score), True, color)
            text_rect = text.get_rect(center = (self.screen_res[0] // 2, self.screen_res[1] // 2 ))

            restart_text = self.font.render("Press R to Restart", True, color)
            restart_text_rect = restart_text.get_rect(center = (self.screen_res[0] // 2, self.screen_res[1] // 2 + 32) )

            quit_text = self.font.render("Press Q to Quit", True, color)
            quit_text_rect = quit_text.get_rect(center =(self.screen_res[0] // 2, self.screen_res[1] // 2 + 64) )

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_text, restart_text_rect)
            self.screen.blit(quit_text,quit_text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    if event.key == pygame.K_q:
                        sys.exit()
                        
        if not waiting:
            self.run()
                        
            
        
        