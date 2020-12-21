import pygame
import pytmx
from math import sqrt, dist
import random

class Trigger(pygame.sprite.Sprite):
    """Çizilmeyecek, collision detection için var"""
    def __init__(self, x, y, w, h, blockers=None):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,w,h)
        self.blockers = blockers # tblr


class Block(pygame.sprite.Sprite):
    def __init__(self, tile, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = tile
        self.rect = tile.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bandit(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0, lightbandit=True):
        pygame.sprite.Sprite.__init__(self)

        self.lightbandit=lightbandit

        if lightbandit:
            self.maxhp = self.hp = 50
        else:
            self.maxhp = self.hp = 100
        
        self.game = game
        self.frame = 0
        self.old_frame = -1
        self.last_time = 0
        self.direction = 'r'
        self.status = 'idle'
        self.imgloop = []
        self.images = self.load_animations()
        self.imgloop = self.images[self.direction][self.status]
        self.image = self.imgloop[0]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.startpos = self.rect.copy()
        self.animationleft = 0
        self.previous_distance = 200
        self.attacktimer = 0#son yapılan ataktan bu yana kaç frame geçmiş, aksi takdirde düşman kilitliyor

    def load_animations(self):
        imgdict = {}
        imgdict['l'], imgdict['r'] = {}, {}
        if self.lightbandit:
            tmxfile = 'lightbandit.tmx'
        else:
            tmxfile = 'heavybandit.tmx'
        tmx = pytmx.load_pygame(tmxfile)

        for x,y,gid in tmx.layers[0]:
            tile = tmx.get_tile_image_by_gid(gid)
            prop = tmx.get_tile_properties_by_gid(gid)
            if tile and prop:
                if prop['type'] not in imgdict['r']:
                    imgdict['l'][prop['type']] = []
                    imgdict['r'][prop['type']] = []
                imgdict['l'][prop['type']].append(tile)
                imgdict['r'][prop['type']].append(pygame.transform.flip(tile,1,0))
        return imgdict

    def update(self, current_time, rate=30):
        last = self.rect.copy()

        if current_time > self.last_time + rate: #zamana göre güncelleme
            self.frame += 1
            self.last_time = current_time

        p = self.game.player.rect
        e = self.rect
        d = dist((p.centerx, p.centery), (e.centerx, e.centery))
        if self.status == 'die':
            self.kill()
        elif self.status=='hurt':
            if self.animationleft<=0:
                self.status = 'combatidle'
        elif d<100:
            if self.previous_distance>=100:
                if self.lightbandit:
                    self.animationleft = random.randint(20,40)
                else:
                    self.animationleft = random.randint(10, 25)
            if p.centerx<e.centerx:
                self.direction = 'l'
            else:
                self.direction = 'r'
            if d<20 and self.attacktimer>=20:
                self.status = 'attack'
                self.attacktimer = 0
                pygame.mixer.Sound.play(game.sounds['sword2'])
            else:
                if self.animationleft >= 0:
                    self.status = 'combatidle'
                else:
                    self.status = 'run'
        else:
            if self.animationleft <= 0:
                self.animationleft = random.randint(50,100)
                self.status =random.choice(['idle', 'run'])
        
        self.animationleft -= 1
        self.attacktimer += 1

        if self.status == 'run':
            if self.direction == 'l':
                self.rect.x -= 2
            else:
                self.rect.x += 2

        self.previous_distance = d

        if pygame.sprite.spritecollideany(self, game.triggers['reverse']):
            bl = pygame.sprite.spritecollide(self, game.triggers['reverse'], False) #Çarpışanlar
            new = self.rect
            for b in bl:
                if last.right<=b.rect.left and new.right > b.rect.left:
                    new.right = b.rect.left
                    self.direction = 'l'
                if last.left >= b.rect.right and new.left < b.rect.right:
                    new.left = b.rect.right
                    self.direction = 'r'

        plcollide = pygame.sprite.spritecollide(self, game.triggers['playerspawn'], False)
        if plcollide:
            for pl in plcollide:
                if pl.status in ['attack1', 'attack2', 'attack3'] and self.status!='hurt':
                    self.animationleft = 50 #player sınıfındakinden çok farklı, nedenini anlamadım
                    self.status = 'hurt'
                    pygame.mixer.Sound.play(game.sounds['hurt2'])
                    self.hp -= random.randint(20,30)
                    if self.hp < 0:
                        self.hp = 0
                        self.status = 'die'
                        pygame.mixer.Sound.play(game.sounds['death2'])


        if self.frame != self.old_frame:
            #self.animation_frame += 1
            self.image = self.imgloop[(self.frame)%len(self.imgloop)]
            self.old_frame = self.frame

        self.imgloop = self.images[self.direction][self.status]


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)

        self.frame = 0
        self.last_time = 0
        self.old_frame = -1
        self.status = 'jump'
        self.last_status = 'jump'
        self.direction = 'r'
        self.imgloop = []
        self.images = self.load_animations()
        self.imgloop = self.images[self.direction][self.status]
        self.image = self.imgloop[0]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.startpos = self.rect.copy()
        self.dy = 0
        self.animation_frame = 0
        self.maxhp = self.hp = 100
        self.attack_timer = 0

    def reset(self):
        self.dy = 0
        self.rect = self.startpos.copy()
        self.status = 'jump'
        self.last_status = 'jump'
        self.direction = 'r'
        self.imgloop = self.images[self.direction][self.status]
        self.maxhp = self.hp = 100

    def load_animations(self):
        imgdict = {}
        imgdict['l'], imgdict['r'] = {}, {}
        tmx = pytmx.load_pygame('hero.tmx')
        for x,y,gid in tmx.layers[0]:
            tile = tmx.get_tile_image_by_gid(gid)
            prop = tmx.get_tile_properties_by_gid(gid)
            if tile and prop:
                if prop['type'] not in imgdict['r']:
                    imgdict['l'][prop['type']] = []
                    imgdict['r'][prop['type']] = []
                imgdict['r'][prop['type']].append(tile)
                imgdict['l'][prop['type']].append(pygame.transform.flip(tile,1,0))

        return imgdict

    def update(self, current_time, rate=30):
        last = self.rect.copy()
        if current_time > self.last_time + rate:
            self.frame += 1
            self.last_time = current_time
        key = pygame.key.get_pressed()

        if self.status == 'die':
            self.kill()

        elif self.status == 'hurt':
            self.animationleft -= 1
            if self.animationleft <= 0:
                self.status = 'idle'
        elif self.status in ['attack1', 'attack2', 'attack3']:
            if self.animation_frame >= len(self.imgloop):
                self.status = self.last_status
        
        elif key[pygame.K_SPACE] and self.status not in ['attack1', 'attack2', 'attack3', 'jump'] and self.attack_timer>=10:
            self.last_status = self.status
            self.status ='attack1'
            self.attack_timer = 0
            self.animation_frame=0
            pygame.mixer.Sound.play(game.sounds['sword1'])

        elif self.status == 'run' and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.status = 'jump'

        elif key[pygame.K_UP] and self.status in ['idle', 'run']:
            self.dy = -10
            self.rect.y += self.dy
            self.status = 'jump'

            
        elif (key[pygame.K_RIGHT] or key[pygame.K_LEFT]) and self.status not in ['attack1', 'attack2', 'attack3']:
            if key[pygame.K_LEFT]:
                self.direction='l'
                self.rect.x -= 2
            else:
                self.direction='r'
                self.rect.x += 2

            if self.status != 'jump':
                self.status = 'run'
            
            r=self.rect
            t=Trigger(r.x, r.y+1, r.w, r.h)
            if not pygame.sprite.spritecollideany(t, game.triggers['platform']):
                self.status="jump" #Eğer altta blok yoksa

        if self.status in ['jump']: #serbest düşüş
            self.dy = min(self.dy + .5, 7) # ivme
            self.rect.y += self.dy

        if pygame.sprite.spritecollideany(self, game.triggers['platform']):
            bl = pygame.sprite.spritecollide(self, game.triggers['platform'], False)#Çarpışanlar
            new = self.rect
            for b in bl:
                if 'l' in b.blockers and last.right<=b.rect.left and new.right > b.rect.left:
                    new.right = b.rect.left
                if 'r' in b.blockers and last.left >= b.rect.right and new.left < b.rect.right:
                    new.left = b.rect.right
                if 't' in b.blockers and last.bottom <= b.rect.top and new.bottom > b.rect.top:
                    self.status = 'idle'
                    new.bottom = b.rect.top
                    self.dy = 0
                if 'b' in b.blockers and last.top >= b.rect.bottom and new.top < b.rect.bottom:
                    new.top = b.rect.bottom
                    self.dy = 0                
            
        encollide = pygame.sprite.spritecollide(self, game.triggers['enemyspawn'], False)
        if encollide:
            for en in encollide:
                if en.status == 'attack' and self.status!='hurt':
                    self.animationleft = 3
                    self.status = 'hurt'
                    pygame.mixer.Sound.play(game.sounds['hurt1'])
                    if en.lightbandit:
                        self.hp -= random.randint(20,30)
                    else:
                        self.hp -= random.randint(40,50)
                    if self.hp < 0:
                        self.hp = 0
                        self.status = 'die'
                        pygame.mixer.Sound.play(game.sounds['death1'])

        self.attack_timer += 1

        if self.frame != self.old_frame:
            self.animation_frame += 1
            self.image = self.imgloop[(self.frame)%len(self.imgloop)]
            self.old_frame = self.frame
        
        self.imgloop = self.images[self.direction][self.status]
        if self.rect.y > 5000:#karakter düşünce
            self.reset()


class Game:
    def __init__(self, width=1024, height=640):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Platform Game")
        self.game_map = pytmx.load_pygame('pl2.tmx')
        self.bg = pygame.image.load('bg.png') # Background image
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        
        self.layers = {}
        for layer in self.game_map.layers:
            self.layers[layer.name] = layer
            if layer.name == 'blocker':
                self.blocks = self.get_tiles(layer)
            elif layer.name == 'trigger':
                self.triggers, self.player = self.get_triggers(layer)

        pygame.mixer.music.load('zapacwatchthesky.ogg')
        pygame.mixer.music.set_volume(0.5)
        self.sounds = self.load_sounds()

        pygame.mixer.music.play(loops=-1)
        
    def load_sounds(self):
        soundlist = [('sword1','sword1.ogg'),
                     ('sword2','sword2.ogg'),
                     ('hurt1', 'hurt1.ogg'),
                     ('hurt2', 'hurt2.ogg'),
                     ('death1', 'death1.ogg'),
                     ('death2', 'death2.ogg')
        ]
        sounds = {}
        for sound, filename in soundlist:
            sounds[sound] = pygame.mixer.Sound(filename)
        return sounds

    def get_triggers(self, layer):
        triggers = {
            'platform': pygame.sprite.Group(),
            'enemyspawn': pygame.sprite.Group(),
            'playerspawn': pygame.sprite.Group(),
            'reverse': pygame.sprite.Group(),
        }
        for o in layer:
            if o.type:
                typ = o.type
            else:
                typ = o.properties['type']

            if typ == 'platform':
                triggers[typ].add(Trigger(o.x, o.y, o.width, o.height, o.properties['blockers']))
            elif typ == 'reverse':
                triggers[typ].add(Trigger(o.x, o.y, o.width, o.height))
            elif typ == 'enemyspawn':
                enemy = Bandit(self, o.x, o.y, lightbandit=random.choice([True, False]))
                triggers['enemyspawn'].add(enemy)
            elif typ == 'playerspawn':
                player = Player(self, o.x, o.y)
                triggers['playerspawn'].add(player)
        return triggers, player

    def get_tiles(self, layer):
        tiles = pygame.sprite.Group()
        for x,y,gid, in layer:
            tile = self.game_map.get_tile_image_by_gid(gid)
            if tile is not None:
                tiles.add(Block(tile, x*self.game_map.tilewidth, y*self.game_map.tileheight))
        return tiles

    def draw_health_bars(self):
        for s in self.triggers['enemyspawn'].sprites()+[self.player]:
            p = s.rect
            pygame.draw.rect(self.screen, (0,0,0), (p.x, p.y-3, p.w, 5))
            pygame.draw.rect(self.screen, (0,255,0), (p.x+1, p.y-2, (p.w-2)*(s.hp/s.maxhp), 3))

    def game_loop(self):
        exit = False
        while not exit:
            ticks = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit = True
            self.screen.blit(self.bg,(0,0))
            self.blocks.draw(self.screen)
            self.triggers['playerspawn'].update(ticks, 150)
            self.triggers['playerspawn'].draw(self.screen) #biraz çirkin oldu, aslında player sprite grubu
            self.triggers['enemyspawn'].update(ticks, 150)
            self.triggers['enemyspawn'].draw(self.screen)
            self.draw_health_bars()
            
            pygame.display.update()
            self.clock.tick(150)


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.game_loop()