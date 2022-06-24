import pygame

test_obstacle = pygame.rect.Rect(10,30,30,30)
items = [test_obstacle]

class Player:
  def __init__(self,speed,health,x,y):
    self.speed = speed
    self.health = health
    self.rect = pygame.rect.Rect(x,y,50,50)
    
  def draw(self,screen,items):
    pygame.draw.rect(screen, (0,0,0), self.rect)
    for item in items:
      pygame.draw.rect(screen, (0,255,0), item)
    
  def move(self,items,w,h):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
      if self.rect.top > 75:
        self.rect.y -= self.speed
      else:
        for item in items:
          item.y += self.speed
          
    elif keys[pygame.K_s]:
      if self.rect.bottom < h - 75:
        self.rect.y += self.speed
      else:
        for item in items:
          item.y -= self.speed
      
    if keys[pygame.K_a]:
      if self.rect.left > 75:
        self.rect.x -= self.speed
      else:
        for item in items:
          item.x += self.speed
          
    elif keys[pygame.K_d]:
      if self.rect.right < w - 75:
        self.rect.x += self.speed
      else:
        for item in items:
          item.x -= self.speed
