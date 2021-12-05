import pygame,sys,os

pygame.init()

SCREEN_WIDTH =1200
SCREEN_HEIGHT=700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('War Game')
clock = pygame.time.Clock()

clock = pygame.time.Clock()
FPS =60

RED = (255,0,0)

# yer çekimi tanımlaması
GRAVITY = 0.75

#Arka plan görüntüsü ayarı
background_img = pygame.image.load(os.path.join('Assets', 'background.jpg'))
background_img_fix = pygame.transform.scale(background_img, (1200, 700))

# oyuncu hareketlerinin değerlerini tanımlama
soldier_moving_left = False
soldier_moving_right = False
robot_moving_left = False
robot_moving_right = False
soldier_shoot = False
robot_shoot = False

#mermi resmi yüklenmesi
robot_bullet = pygame.image.load(os.path.join('Assets/icons/robot_bullet.png')).convert_alpha()
soldier_bullet = pygame.image.load(os.path.join('Assets/icons/soldier_bullet.png'))


soldier_width, soldier_height = 60, 40  #
class Soldier(pygame.sprite.Sprite): #Asker sınıfı tüm askerler için kullanılacak
    def __init__(self, konumX,konumY,character_type,speed,position,bullet_image,ammo):
        pygame.sprite.Sprite.__init__(self)
        self.character_type=character_type
        self.bullet_image=bullet_image
        self.alive = True
        self.speed= speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.position = position #başlangıç pozisyonu
        self.direction = 1
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
            temp_list = [] #geçici (temporary) listemi sıfırlıyorum
            #hangi klasörde kaç tane dosya var bunu öğrenmek için bir python fonksiyonu kullandım
            num_of_files = len(os.listdir(f'Assets/{self.character_type}/{animation}'))
            for i in range(num_of_files):
                # Asker durma durumu animasyonu
                SOLDIER = pygame.image.load(os.path.join(f'Assets/{self.character_type}/{animation}/{i}.png')).convert_alpha() #convert_alpha'nın eklenme amacı verimliliği arttırmak
                SOLDIER = pygame.transform.scale(SOLDIER, (soldier_width, soldier_height))
                temp_list.append(SOLDIER)
            self.animation_list.append(temp_list) # geçici listeyi animasyon listesine ekledim

        self.SOLDIER_IMAGE = self.animation_list[self.action][self.index]
        self.rect = self.SOLDIER_IMAGE.get_rect()
        self.rect.center = (konumX, konumY)

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
            self.position = True
            self.direction = -1
        if moving_right:
            dx = self.speed #x ekseninde hız değeri artırarak sağa gidiyor
            self.position = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.velocity_y = -11 # zıplama değeri yukarı çıktıkça azalır
            self.jump = False
            self.in_air = True

        #Yerçekimi tanımlaması
        self.velocity_y += GRAVITY # y yüksekliği yavaş yavaş azalacak
        if self.velocity_y > 10:
            self.velocity_y
        dy += self.velocity_y # karkaterin y eksenini zıplama hızına göre değiştiriyorum

        #Zemin ile çarpışma kontrolü
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #dikdörtgenin pozisyonunu değiştirme
        self.rect.x +=dx
        self.rect.y +=dy

    def shoot(self):
        if self.shoot_cooldown ==0 and self.ammo > 0: # couldown'ı 0 iken 20 yap
            self.shoot_cooldown =20
            # merminin x ve y  eksenindeki konumunu ve yönünü ayarlamak için gereken işlemler
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),self.rect.centery + 3, self.direction,self.bullet_image)
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
        #animasyon bittiyse, sıfırlamayı en başa döndürün yani sonsuz döngü
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

    def draw(self): #self default gelmek zorunda
        screen.blit(pygame.transform.flip(self.SOLDIER_IMAGE, self.position,False), self.rect)


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
        #merminin düşman ile çarpışması
        if pygame.sprite.spritecollide(soldier, bullet_group , False):
            if soldier.alive:
                soldier.health -= 20 # mermi nin soldier'a vereceği hasar
                self.kill()
        if pygame.sprite.spritecollide(robot, bullet_group , False):
            if robot.alive:
                robot.health -= 10 # merminin robot'a vereceği hasar
                self.kill()

# sprite grubu oluşturuldu (üretilen tüm mermi nesneleri bu grupda tutulacak)
bullet_group = pygame.sprite.Group()



soldier=Soldier(200,200,'soldier',5,False,soldier_bullet,20) #200 200 konumunu gösteriyor (sınıfın nesnesi)
robot=Soldier(400,200,'robot',5,True,robot_bullet,20)
# # Robot görünütüsü ayarı

# self.ROBOT = pygame.transform.scale(ROBOT_IMAGE, (warior_width, warior_height))
# self.rect = self.ROBOT.get_rect()
# self.rect.center = (konumX, konumY)

run = True
while run:

    clock.tick(FPS)

    screen.blit(background_img_fix, (0, 0))  # (0,0) resmin konumlanacağı nokta

    pygame.draw.line(screen,RED,(0,300),(SCREEN_WIDTH,300))

    soldier.update()
    soldier.draw()

    bullet_group.update()
    bullet_group.draw(screen)

    if soldier.alive:
        if soldier_shoot:
            soldier.shoot()
        if soldier.in_air:
            soldier.update_action(2)  # eğer 2 ise zıplıyor
        #hareket edildiyse actionu değiştir
        # hareket edildiyse actionu değiştir
        elif soldier_moving_left or soldier_moving_right:
            soldier.update_action(1) # eğer 1 ise koşuyor
        else:
            soldier.update_action(0) # eğer 0 ise duruyor
        soldier.move(soldier_moving_left,soldier_moving_right)

    robot.update()
    robot.draw()

    if robot.alive:
        if robot_shoot:
            robot.shoot()
        if robot.in_air:
            robot.update_action(2)  # eğer 2 ise zıplıyor
        #hareket edildiyse actionu değiştir
        elif robot_moving_left or robot_moving_right:
            robot.update_action(1) # eğer 1 ise koşuyor
        else:
            robot.update_action(0)  # eğer 0 ise duruyor
        robot.move(robot_moving_left,robot_moving_right)



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
            if event.key == pygame.K_w and soldier.alive:
                soldier.jump = True

            if event.key == pygame.K_LEFT:
                robot_moving_left = True
            if event.key == pygame.K_RIGHT:
                robot_moving_right = True
            if event.key == pygame.K_RCTRL:
                robot_shoot = True
            if event.key == pygame.K_UP and robot.alive:
                robot.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # tuşun bırakılma anını yakalama
        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_a:
                soldier_moving_left = False
            if event.key == pygame.K_LEFT:
                robot_moving_left = False
            if event.key == pygame.K_LCTRL:
                soldier_shoot = False
            if event.key == pygame.K_d:
                soldier_moving_right = False
            if event.key == pygame.K_RIGHT:
                robot_moving_right = False
            if event.key == pygame.K_RCTRL:
                robot_shoot = False



    pygame.display.update()

pygame.quit()