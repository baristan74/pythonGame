import pygame,os,button,map
from pygame import mixer

mixer.init()
pygame.init()

SCREEN_WIDTH =1200
SCREEN_HEIGHT=600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('War Zone')

clock = pygame.time.Clock()
FPS =60

#renklerin tanımlanması
LIGHTGREEN = (144, 201, 120)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

# oyun verilerinin tanımlanması
GRAVITY = 0.75
ROWS = 15
COLS= 30
SURFACE_SIZE = SCREEN_HEIGHT // ROWS



# oyuncu hareketlerinin değerlerini tanımlama
soldier_moving_left = False
soldier_moving_right = False
robot_moving_left = False
robot_moving_right = False
soldier_shoot = False
robot_shoot = False
secondGun_robot = False
secondGun_soldier = False
secondGun_soldier_thrown = False
secondGun_robot_thrown = False

start_game = False

#ses dosyalarının yüklenmesi
pygame.mixer.music.load('Assets/audio/clubbedtodeath.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,5000)
robot_shoot_effect=pygame.mixer.Sound('Assets/audio/robot.mp3')
robot_shoot_effect.set_volume(0.5)
soldier_shoot_effect=pygame.mixer.Sound('Assets/audio/soldier.mp3')
soldier_shoot_effect.set_volume(0.5)
bomb_explosion_effect=pygame.mixer.Sound('Assets/audio/bomb.mp3')
bomb_explosion_effect.set_volume(0.5)

#Buttun görünlülerinin yüklenmesi
start_img = pygame.image.load(os.path.join('Assets/start_button.png')).convert_alpha()
exit_img = pygame.image.load(os.path.join('Assets/exit_button.png')).convert_alpha()
restart_img = pygame.image.load(os.path.join('Assets/restart_button.png')).convert_alpha()

#Arka plan görüntüsü ayarı
background_img = pygame.image.load(os.path.join('Assets/background.jpg')).convert_alpha()
background_img_fix = pygame.transform.scale(background_img, (1200, 600)).convert_alpha()

#mermi resimleri yüklenmesi
robot_bullet = pygame.image.load(os.path.join('Assets/icons/robot_bullet.png')).convert_alpha()
soldier_bullet = pygame.image.load(os.path.join('Assets/icons/soldier_bullet.png')).convert_alpha()
grenade_img = pygame.image.load(os.path.join('Assets/icons/grenade.png')).convert_alpha()
grenade_img = pygame.transform.scale(grenade_img, (12, 12)).convert_alpha()
bomb_robot_img = pygame.image.load(os.path.join('Assets/icons/robot_bomb.png')).convert_alpha()
bomb_robot_img = pygame.transform.scale(bomb_robot_img, (15, 15)).convert_alpha()

#buff kutularının tanımlanması
heal_box_img= pygame.image.load(os.path.join('Assets/icons/health.png')).convert_alpha()
heal_box_img = pygame.transform.scale(heal_box_img, (20, 20)).convert_alpha()
defence_box_img= pygame.image.load(os.path.join('Assets/icons/defence.png')).convert_alpha()
defence_box_img = pygame.transform.scale(defence_box_img, (20, 20)).convert_alpha()
ammo_box_img= pygame.image.load(os.path.join('Assets/icons/ammo.png')).convert_alpha()
ammo_box_img = pygame.transform.scale(ammo_box_img, (20, 20)).convert_alpha()
bomb_box_img= pygame.image.load(os.path.join('Assets/icons/bomb.png')).convert_alpha()
bomb_box_img = pygame.transform.scale(bomb_box_img, (20, 20)).convert_alpha()


#python sözlük kullanımı buff box için // javadaki enum gibi
buff_boxes = {
    'Health'   : heal_box_img,
    'Ammo'     : ammo_box_img,
    'Bomb'     : bomb_box_img,
    'Defence'  : defence_box_img
}


font = pygame.font.SysFont('Future', 30)
def draw_text(text, font, text_col, x, y): # ekrana yazmak istediğim yazılar için kullanıyorum
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x,y))

# ekranı karelere bölme fonksiyonu
# def draw_grid():
#     for line in range(0,30):
#         pygame.draw.line(SCREEN, (255, 255, 255), (0, line * SURFACE_SIZE), (SCREEN_WIDTH, line * SURFACE_SIZE))
#         pygame.draw.line(SCREEN, (255, 255, 255), (line * SURFACE_SIZE, 0), (line * SURFACE_SIZE, SCREEN_HEIGHT))


class Map():
    def __init__(self, data):
        self.surface_list = []
        ground_img = pygame.image.load(os.path.join('Assets/ground.png'))
        ground2_img = pygame.image.load(os.path.join('Assets/ground2.png'))

        row_count = 0
        for row in data: # satır satır geziyor her defada colonu artırıyor bir satır bittiğinde satırı arttırıp tekrar colon geziyor
            col_count = 0
            for surface in row:
                if surface == 1:
                    img = pygame.transform.scale(ground_img,(SURFACE_SIZE, SURFACE_SIZE))
                    img_rect =img.get_rect()
                    img_rect.x = col_count * SURFACE_SIZE
                    img_rect.y = row_count * SURFACE_SIZE
                    surface = (img, img_rect)
                    self.surface_list.append(surface)
                if surface == 2:
                    img = pygame.transform.scale(ground2_img,(SURFACE_SIZE, SURFACE_SIZE))
                    img_rect =img.get_rect()
                    img_rect.x = col_count * SURFACE_SIZE
                    img_rect.y = row_count * SURFACE_SIZE
                    surface = (img, img_rect)
                    self.surface_list.append(surface)
                col_count +=1
            row_count += 1

    def draw(self):
        for surface in self.surface_list:
            #Ekran üzerine fayansları çizdiriyorum
            SCREEN.blit(surface[0], surface[1])

map = Map(map.map_data)


character_width, character_height = 60, 40
class Character(pygame.sprite.Sprite): #Character sınıfı tüm askerler için kullanılacak
    def __init__(self, konumX,konumY,character_type,speed,position,direction,bullet_image,ammo,grenades,grenade_image):
        pygame.sprite.Sprite.__init__(self)
        self.character_type=character_type
        self.bullet_image=bullet_image
        self.grenades_image = grenade_image
        self.alive = True
        self.speed= speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.position = position #başlangıç pozisyonu
        self.direction = direction
        self.velocity_y = 0 # y eksenindeki hız zıplamak için
        self.jump = False # oyuncu en başta hareketsiz olduğu için False olarak başlatıyorum
        self.in_air= True # buradaki düşüncem yere inene kadar karakteri havada sayıyorum
        #animasyom işlemleri
        self.animation_list =[]
        self.index =0
        self.action =0  # (harekeet ettirdiğimi anlamak için tanımladım)koşma animasyonu ile durma animasyonunu ayırmak için ekledim 0 ise duruyor 1 ise koşuyor
        self.update_time = pygame.time.get_ticks()

        #oyuncuların tüm resimlerini for döngüsü içinde hangisi ise yükle
        animation_types = ['Idle','Run','Jump','Death']
        for animation in animation_types:
            temp_list = [] #geçici (temporary) listemi tanımlıyorum
            #hangi klasörde kaç tane dosya var bunu öğrenmek için bir python fonksiyonu kullandım
            num_of_files = len(os.listdir(f'Assets/{self.character_type}/{animation}'))
            for i in range(num_of_files):
                # Asker durumu animasyonları
                CHARACTER = pygame.image.load(os.path.join(f'Assets/{self.character_type}/{animation}/{i}.png')).convert_alpha() #convert_alpha'nın eklenme amacı verimliliği arttırmak
                CHARACTER = pygame.transform.scale(CHARACTER, (character_width, character_height)).convert_alpha()
                temp_list.append(CHARACTER)
            self.animation_list.append(temp_list) # geçici listeyi animasyon listesine ekledim

        self.CHARACTER_IMAGE = self.animation_list[self.action][self.index]
        self.rect = self.CHARACTER_IMAGE.get_rect()
        self.rect.center = (konumX, konumY)
        self.width= self.CHARACTER_IMAGE.get_width()
        self.height =self.CHARACTER_IMAGE.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        # coulddown ayarlama  # couldown'ı 20 iken 1 1 azalt
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -=1


    def move(self,moving_left,moving_right):
        #hareketleri sıfırlama değerleri
        dx=0
        dy=0
        #sağa ve sola hareket değerlerinin atanması
        if moving_left:
            dx = -self.speed #x ekseninde hız değeri azalarak sola gidiyor
            self.position = True # yön değiştirme sola döndüğünde resimde sola dönüyor
            self.direction = -1
            # print("sola hareket")
        if moving_right:
            dx = self.speed #x ekseninde hız değeri artırarak sağa gidiyor
            self.position = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.velocity_y = -11 # zıplama işlemi gerçekleştiğinde y ekseninde yükselmek için -li değer verildi
            self.jump = False
            self.in_air = True
            # print("zıplama kontrolü")

        #Yerçekimi tanımlaması
        self.velocity_y += GRAVITY # y yüksekliği yavaş yavaş azalacak
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y # karkaterin y eksenini zıplama hızına göre değiştiriyorum

        #Yüzey ile çarpışma kontrolü
        for surface in map.surface_list:
            # x yönünde çarpışma kontrolü
            if surface[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # y yönünde çarpışma kontrolü
            if surface[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #fayansların altında olup olmadığının kontrolü  zıplarken
                if self.velocity_y <0:
                    self.velocity_y = 0
                    dy = surface[1].bottom - self.rect.top # yüzeyler arası boşluk ile karakterin kafası arasındaki boşluk
                #yerden yüksekte olup olmadığının kontrolü zıplarken
                elif self.velocity_y >= 0:
                    self.velocity_y = 0
                    self.in_air = False
                    dy = surface[1].top - self.rect.bottom


        #dikdörtgenin pozisyonunu değiştirme
        self.rect.x +=dx
        self.rect.y +=dy

    def shoot(self):
        if self.shoot_cooldown ==0 and self.ammo > 0: # couldown'ı 0 iken 20 yap
            self.shoot_cooldown =20
            # merminin x ve y  eksenindeki konumunu ve yönünü ayarlamak için gereken işlemler
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),self.rect.centery + 3, self.direction,self.bullet_image)
            bullet_group.add(bullet)
            #ateş ettikçe mermi azalacak
            self.ammo -=1

    def update_animation(self):
        # animation yükleme
        ANIMATION_COOLDOWN = 100
        self.SOLDIER_IMAGE = self.animation_list[self.action][self.index]
        #son güncellemeden bu yana yeterli zaman geçip geçmediğini kontrol ediyorum
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        #animasyon bittiyse, sıfırlamayı en başa döndürür yani sonsuz döngü
        if self.index >= len(self.animation_list[self.action]):
            if self.action == 3: # ölüm animasyonu için tekrarlama yapmasını istemiyorum bu sebepten dolayı 3. argüman olduğunda döngüyü durdurucak
                self.index = len(self.animation_list[self.action]) - 1
            else:
                self.index =0


    def update_action(self,new_action): # bunu oluşturmamdaki sebep hareket edip etmediğimi genel bir yerden kontrol etmek için
        #yeni hareketimin önceki hareketimden farklı olup olmadığını kontrol et
        if new_action != self.action:
            self.action = new_action
            #animasyon ayarlarını güncelleme
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        # eğer ölmüşse
        if self.health <= 0:
            self.health =0
            self.speed =0
            self.alive = False
            self.update_action(3)

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.SOLDIER_IMAGE, self.position,False), self.rect) # karakterlerin görüntülerinin ekranda düz durmasını sağlıyorum

class BuffBox(pygame.sprite.Sprite):
    def __init__(self,box_type,x,y,):
        pygame.sprite.Sprite.__init__(self)
        self.box_type = box_type
        self.image = buff_boxes[self.box_type]
        self.rect= self.image.get_rect()
        #fayans üzerinde konumu
        self.rect.midtop = (x + SURFACE_SIZE // 2, y + (SURFACE_SIZE - self.image.get_height()))

    def update(self):
        #karakter ile kutuların çarpışma kontrolü
        if pygame.sprite.collide_rect(self, soldier): # kutu ile soldierın çarpışma anını yakalama
            #hangi kutu türü ile çarpışıldığını yakalama
            if self.box_type == 'Health':
                soldier.health +=25
                if soldier.health > soldier.max_health:
                    soldier.health = soldier.max_health
            elif self.box_type == 'Ammo':
                soldier.ammo += 15
            elif self.box_type == 'Bomb':
                soldier.grenades +=3
            elif self.box_type == 'Defence':
                soldier.health = soldier.max_health
            self.kill() # çarpışmadan sonra kutuyu kaldır
        if pygame.sprite.collide_rect(self, robot): # kutu ile robotun çarpışma anını yakalama
            #hangi kutu türü ile çarpışıldığını yakalama
            if self.box_type == 'Health':
                robot.health +=25
                if robot.health > robot.max_health:
                    robot.health = robot.max_health
            elif self.box_type == 'Ammo':
                robot.ammo += 15
            elif self.box_type == 'Bomb':
                robot.grenades +=3
            elif self.box_type == 'Defence':
                robot.health = robot.max_health
            self.kill() # çarpışmadan sonra kutuyu kaldır



class HealthBar():
    def __init__(self,x,y,health,max_health):
        self.x = x
        self.y =y
        self.health = health
        self.max_health = max_health
    def draw(self,health):
        self.health = health
        oran = self.health / self.max_health # oran sağlık oranını hesaplamak için oluşturdum eğer 50 canım varsa 50 / 100 yani 0.5 yapar bunu ana çerçeve boyu ile çarptığımda gerçek sağlığı verir
        pygame.draw.rect(SCREEN, BLACK, (self.x - 2, self.y - 2,154,24))
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(SCREEN, GREEN, (self.x,self.y, 150 * oran,20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image= image
        self.rect = self.image.get_rect() #imagein boyutunda olucak
        self.rect.center = (x,y)
        self.direction = direction #yön bazı mermiler sağa bazı mermiler sola gidecek bu karakterin hangi tarafa baktığına bağlı olacak
    def update(self):
        #mermi hareketleri
        self.rect.x += (self.direction * self.speed)
        # mermilerin ekrandan çıkıp çıkmadığının kontrolü
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill() #ekrandan çıkan mermileri sil
        #herhangi bir zemin ile merminin çarpışma kontrolü
        for surface in map.surface_list:
            if surface[1].colliderect(self.rect):
                self.kill()
        #merminin düşman ile çarpışması
        if pygame.sprite.spritecollide(soldier, bullet_group , False):
            if soldier.alive:
                soldier.health -= 10 # mermi nin soldier'a vereceği hasar
                self.kill()
        if pygame.sprite.spritecollide(robot, bullet_group , False):
            if robot.alive:
                robot.health -= 10 # merminin robot'a vereceği hasar
                self.kill() # görüntüyü yok ediyorum

class SecondGun(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,image):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.velocity_y = -9  # yukarı hızlanma - çünkü y ekseninde yukarı gidiyor
        self.speed = 7
        self.image= image
        self.rect = self.image.get_rect() #imagein boyutunda olucak
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction #yön bazı mermiler sağa bazı mermiler sola gidecek bu karakterin hangi tarafa baktığına bağlı olacak

    def update(self):
        self.velocity_y += GRAVITY # hızını yer çekimi ile toplayıp yer çekimini sağlıyorum
        dx = self.direction * self.speed
        dy = self.velocity_y

        # surface ile çarpışma kontrolü
        for surface in map.surface_list:
            # bombanın yere düştüğünde yok olma kontrolü
            if surface[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1  # duvara çarptığında geri sekmesini sağlıyorum
                dx = self.direction * self.speed

             # y yönünde çarpışma kontrolü
            if surface[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0 #eğer y ekseninde bir yere değerse direkt aşağı düşmesini istiyorum
                # yerin altında olup olmadığının kontrolü yukarı atılırken
                if self.velocity_y < 0:
                     self.velocity_y = 0
                     dy = surface[1].bottom - self.rect.top  # yüzeyler arası boşlukile karakterin kafası arasındaki boşluk
                # yerden yüksekte olup olmadığının kontrolü zıplarken
                elif self.velocity_y >= 0:
                     self.velocity_y = 0
                     dy = surface[1].top - self.rect.bottom

        # bombanın yerdeğişimi
        self.rect.x += dx
        self.rect.y += dy

        #bombanın geri sayım sayacı
        self.timer -=1
        #bombanın sayacı 0 lanmış ise bomba patlar
        if self.timer <=0:
            self.kill()
            bomb_explosion_effect.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.5) #explosion ve secondGun aralarındaki bağlantıyı kuruyorum
            explosion_group.add(explosion)
            # bombaların hasar vermesi  #abs fonksiyonu mutlak değerini aldırıyor
            if abs(self.rect.centerx - soldier.rect.centerx) < SURFACE_SIZE * 2 and \
                    abs(self.rect.centery - soldier.rect.centery) < SURFACE_SIZE * 2: #bombanın bulunduğu konum ile askeri bulunduğu konum arasındaki fark 2 karodan küçük ise hasar alıcak
                soldier.health -= 50
            if abs(self.rect.centerx - robot.rect.centerx) < SURFACE_SIZE * 2 and \
                    abs(self.rect.centery - robot.rect.centery) < SURFACE_SIZE * 2: #bombanın bulunduğu konum ile askeri bulunduğu konum arasındaki fark 2 karodan küçük ise hasar alıcak
                robot.health -= 50

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(0,6):
            img = pygame.image.load(os.path.join(f'Assets/icons/explosion/{num}.png')).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale),int(img.get_height() *scale)))
            self.images.append(img)
        self.index = 0
        self.image= self.images[self.index]
        self.rect = self.image.get_rect() #imagein boyutunda olucak
        self.rect.center = (x,y)
        self.counter= 0

    def update(self):
        explosion_speed = 4
        # patlama animasyonunun gerçekleştirilmesi
        self.counter +=1
        if self.counter >= explosion_speed: # eğer sayaç patlama hızını aştıysa sayacı sıfırlayıp image dizisinin indexini değiştiriz ki animasyon değişsin
            self.counter = 0
            self.index += 1
            #animasyon tamamlandığında patlama animasyonunu ortadan kaldırma işlemi
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
def restart_game():
    start_game = False
    pygame.mixer.music.play()
    soldier.alive = True
    robot.alive = True
    soldier.speed = 5
    robot.speed = 5
    soldier.update_action(0)
    robot.update_action(0)
    soldier.health = 100
    robot.health = 100
    soldier.ammo = 20
    robot.ammo = 20
    soldier.grenades = 5
    robot.grenades = 5
    soldier.rect.centerx = 90
    soldier.rect.centery = 200
    robot.rect.centerx = 1110
    robot.rect.centery = 200

    create_buff_boxes()

    bullet_group.update()
    secondGun_group.update()
    explosion_group.update()
    buff_boxes_group.update()
    bullet_group.draw(SCREEN)
    secondGun_group.draw(SCREEN)
    explosion_group.draw(SCREEN)
    buff_boxes_group.draw(SCREEN)

# sprite grubu oluşturuldu (üretilen tüm mermi nesneleri bu grupta tutulacak)
bullet_group = pygame.sprite.Group()

secondGun_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

buff_boxes_group = pygame.sprite.Group()

# geçici buff box oluşturma
def create_buff_boxes():
    buff_box = BuffBox('Health', 560,160)
    buff_boxes_group.add(buff_box)
    buff_box = BuffBox('Ammo', 480,160)
    buff_boxes_group.add(buff_box)
    buff_box = BuffBox('Bomb', 640,160)
    buff_boxes_group.add(buff_box)
    buff_box = BuffBox('Defence', 720,160)
    buff_boxes_group.add(buff_box)

create_buff_boxes()

#butonların oluşturulması
start_button = button.Button(SCREEN_WIDTH//2-130,SCREEN_HEIGHT //2 - 150,start_img,1)
exit_button = button.Button(SCREEN_WIDTH//2-130,SCREEN_HEIGHT //2 ,exit_img,1)
restart_button = button.Button(SCREEN_WIDTH//2-130,SCREEN_HEIGHT //2 - 100 ,restart_img,1)


soldier=Character(90,200,'soldier',5,False,1,soldier_bullet,20,5,grenade_img)
robot=Character(1110,200,'robot',5,True,-1,robot_bullet,20,5,bomb_robot_img)
soldier_health_bar = HealthBar(100,33,soldier.health,soldier.health)
robot_health_bar = HealthBar(905,33,robot.health,robot.health)

run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        #menu oluşturma
        SCREEN.fill(LIGHTGREEN)
        #add buttons
        if start_button.draw(SCREEN): # Button classından gelen action üzerinden true gelmişse
            start_game = True
        if exit_button.draw(SCREEN):
            run = False
    else:
        SCREEN.blit(background_img_fix, (0, 0))  # (0,0) resmin konumlanacağı nokta

        # draw_grid()
        map.draw()

        #soldier verileri ekranda gösterme
        draw_text('HEALTH: ',font,WHITE, 10,35)
        soldier_health_bar.draw(soldier.health)
        draw_text('AMMO: ', font, WHITE, 10, 60)
        for x in range(soldier.ammo):
            SCREEN.blit(soldier_bullet, (85 + (x * 10), 63))
        draw_text('GRENADES: ', font, WHITE, 10, 85)
        for x in range(soldier.grenades):
            SCREEN.blit(grenade_img, (130 + (x *11),88))


        # robot verileri ekranda gösterme
        draw_text('HEALTH: ', font, WHITE, 815, 35)
        robot_health_bar.draw(robot.health)
        draw_text('AMMO: ', font, WHITE, 815, 60)
        for x in range(robot.ammo):
            SCREEN.blit(robot_bullet, (885 + (x * 10), 63))
        draw_text('BOMB: ', font, WHITE, 815, 85)
        for x in range(robot.grenades):
            SCREEN.blit(bomb_robot_img, (935 + (x * 14), 85))

        bullet_group.update()
        secondGun_group.update()
        explosion_group.update()
        buff_boxes_group.update()

        bullet_group.draw(SCREEN)
        secondGun_group.draw(SCREEN)
        explosion_group.draw(SCREEN)
        buff_boxes_group.draw(SCREEN)

        soldier.update()
        soldier.draw()

        if soldier.alive:
            if soldier_shoot:
                soldier.shoot()
                # bomba fırlatma
            elif secondGun_soldier and secondGun_soldier_thrown == False and soldier.grenades > 0:
                secondGun_soldier = SecondGun(soldier.rect.centerx + (0.5 * soldier.rect.size[0] * soldier.direction), \
                                            soldier.rect.top, soldier.direction,grenade_img)
                secondGun_group.add(secondGun_soldier)
                #bomba azaltma
                soldier.grenades -= 1
                secondGun_soldier_thrown = True
            if soldier.in_air:
                soldier.update_action(2)  # eğer 2 ise zıplıyor
            #hareket edildiyse actionu değiştir
            # hareket edildiyse actionu değiştir
            elif soldier_moving_left or soldier_moving_right:
                soldier.update_action(1) # eğer 1 ise koşuyor
            else:
                soldier.update_action(0) # eğer 0 ise duruyor
            soldier.move(soldier_moving_left,soldier_moving_right)
        else:
            pygame.mixer.music.stop()
            if restart_button.draw(SCREEN):
                restart_game()


        robot.update()
        robot.draw()

        if robot.alive:
            if robot_shoot:
                robot.shoot()
            #bomba fırlatma
            elif secondGun_robot and secondGun_robot_thrown == False and robot.grenades > 0: # secondGun tanımlamamdaki sebep yeni bir bomba fırlatmadan önce zaten bir bomba fırlatılmış mı kontrolü ve explosion sayısı 0 dan büyükse fırlat kontrolü
                secondGun_robot = SecondGun(robot.rect.centerx+(0.5 * robot.rect.size[0] * robot.direction), robot.rect.top,robot.direction ,bomb_robot_img)
                secondGun_group.add(secondGun_robot)
                # bomba azaltma
                robot.grenades -= 1
                secondGun_robot_thrown = True
            if robot.in_air:
                robot.update_action(2)  # eğer 2 ise zıplıyor
            #hareket edildiyse actionu değiştir
            elif robot_moving_left or robot_moving_right:
                robot.update_action(1) # eğer 1 ise koşuyor
            else:
                robot.update_action(0)  # eğer 0 ise duruyor
            robot.move(robot_moving_left,robot_moving_right)
        else:
            pygame.mixer.music.stop()
            if restart_button.draw(SCREEN):
                restart_game() # oyun verilerini updateledik



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #klavye hareketleri
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_a:
                soldier_moving_left = True
            if event.key == pygame.K_d:
                soldier_moving_right = True
            if event.key == pygame.K_LCTRL:
                soldier_shoot = True
                soldier_shoot_effect.play()
            if event.key == pygame.K_LSHIFT:
                secondGun_soldier = True
            if event.key == pygame.K_w and soldier.alive:
                soldier.jump = True

            if event.key == pygame.K_LEFT:
                robot_moving_left = True
            if event.key == pygame.K_RIGHT:
                robot_moving_right = True
            if event.key == pygame.K_RCTRL:
                robot_shoot = True
                robot_shoot_effect.play()
            if event.key == pygame.K_RSHIFT:
                secondGun_robot = True
            if event.key == pygame.K_UP and robot.alive:
                robot.jump = True

            if event.key == pygame.K_ESCAPE:
                run = False

        # tuşun bırakılma anını yakalama
        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_a:
                soldier_moving_left = False
            if event.key == pygame.K_d:
                soldier_moving_right = False
            if event.key == pygame.K_LCTRL:
                soldier_shoot = False
            if event.key == pygame.K_LSHIFT:
                secondGun_soldier = False
                secondGun_soldier_thrown = False

            if event.key == pygame.K_LEFT:
                robot_moving_left = False
            if event.key == pygame.K_RIGHT:
                robot_moving_right = False
            if event.key == pygame.K_RCTRL:
                robot_shoot = False
            if event.key == pygame.K_RSHIFT:
                secondGun_robot = False
                secondGun_robot_thrown =False # bekleme süresi yerine tuştan el çekildiğinde tekrar fırlatabilmesi için fırlatma özelliğini false'a çektim

    pygame.display.update()

pygame.quit()