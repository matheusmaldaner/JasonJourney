import pygame
import math
import constants
import random


class Weapon:
    def __init__(self, weapon_image, projectile_image):
        self.projectile_image = projectile_image
        self.original_image = weapon_image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        self.flip = False

    def update(self, player):
        shot_cooldown = 300
        projectile = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # makes weapon point where mouse cursor is
        if x_dist > 0:
            self.flip = False
        if x_dist < 0:
            self.flip = True

        # self.fired prevents player from spamming infinite bullets
        if pygame.mouse.get_pressed()[0] and self.fired is False and \
                (pygame.time.get_ticks() - self.last_shot >= shot_cooldown):  # 0 is left mouse button
            projectile = Projectile(self.projectile_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()

        # resets shooting cooldown
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

        return projectile

    def draw(self, surface):
        # flips image across player vertical axis
        flipped_image = pygame.transform.flip(self.original_image, False, self.flip)

        # fixes the angle the weapon is facing
        self.image = pygame.transform.rotate(flipped_image, self.angle)

        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)),
                                  (self.rect.centery - int(self.image.get_height()/2))))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # gets vertical and horizontal speed based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.PROJECTILE_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.PROJECTILE_SPEED)

    def update(self, screen_scroll, wall_tiles, enemy_list):
        # resets variables
        damage = 0
        damage_pos = None

        # makes projectile move in specific direction
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # checks for collision between arrow and tile walls
        for wall in wall_tiles:
            if wall[1].colliderect(self.rect):
                self.kill()

        # deletes projectile if it goes off screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()  # deletes projectile

        # checks collision between weapon and enemy !!!
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive: # see if weapon hits enemy
                damage = 4 + random.randint(-2, 2)
                damage_pos = enemy.rect
                enemy.health -= damage
                enemy.hit = True
                self.kill()
                break

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), (self.rect.centery - int(self.image.get_height()/2))))


class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.FIREBALL_SPEED)  # -ve because pygame y coordiate increases down the screen

    def update(self, screen_scroll, player):
        # reposition fireball based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # checks if fireball has gone off the screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        # checks collision between self and player
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= 10
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))