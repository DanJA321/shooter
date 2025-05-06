#Create your own shooter

from pygame import *
from random import randint


window = display.set_mode((700,500))
display.set_caption('space game')
bg = transform.scale(image.load('galaxy.jpg'),(700,500))

class Game(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image),(size_x,size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
       window.blit(self.image,(self.rect.x,self.rect.y))

bullets = sprite.Group()

sum_bullet = 0
class Player(Game):

   def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < 650:
           self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.y > 50:
           self.rect.x -= self.speed
        if keys[K_SPACE] :
           self.fire()

   def fire(self):
      global sum_bullet

      if sum_bullet < 20 :
         #fire_sound.play()
         bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
         bullets.add(bullet)
      
      else :
         window.blit(text_reload, (300, 450))

      if  sum_bullet > 50 :
           sum_bullet = 0

      sum_bullet += 1


      

lose = 0
class Enemy(Game):
   def update(self):
      self.rect.y += self.speed
      global lose
      if self.rect.y > 500 :
         self.rect.y = -4
         self.rect.x = randint(10, 650)
         self.speed = randint(1, 5)
         lose += 1

class  Bullet(Game):
   def update(self):
      self.rect.y += self.speed
      print('tes')
      if self.rect.y < 0 :
         self.kill()

class Asteroid(Game):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500 :
            self.rect.y = -40
            self.rect.x  = randint(10, 650)
            self.speed = randint(1, 5)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(10, 650), -40, 75, 60, randint(1, 5))
    asteroids.add(asteroid)

hero = Player('rocket.png',400,400,65,65, 10)

monsters = sprite.Group()
sum_enemy = 6
for i in range(sum_enemy):
   monster = Enemy('ufo.png', randint(10,650), 20,65,65, randint(1,5))
   monsters.add(monster)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font2 = font.SysFont(None, 60)
font1 = font.Font(None, 32)
text_win = font2.render('KAMU MENANG', True, (255, 255, 255))
text_fail = font2.render('KAMU KALAH', True, (255, 0, 0))
font3 = font.SysFont(None, 34)
text_reload = font3.render('reload cuy', True, (255, 0, 0))

run = True
game = True
clock = time.Clock() 

while run :

   for e in event.get():
       if e.type == QUIT:
           run = False

   window.blit(bg, (0,0))

   if sprite.collide_rect(hero, monster) or lose >= 5 or sprite.collide_rect(hero, asteroid):
      window.blit(text_fail, (250, 250))
      game = False

   colides = sprite.groupcollide(bullets, monsters, True, True)

   colides = sprite.groupcollide(bullets, asteroids, True, False)

   if len(monsters) == 0:
      window.blit(text_win, (250, 250))

   text_lose = font1.render('dilewatkan :' + str(lose), 1, (255,255,255))
   window.blit(text_lose, (10,10))

   if game:
     asteroids.draw(window)
     asteroids.update()
     monsters.draw(window)
     monsters.update()
     bullets.draw(window)
     bullets.update()

     hero.reset()
     hero.update()
   display.update()
   clock.tick(40)
