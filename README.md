# Python Game (War Zone)

## Proje geliştirilme aşamaları:
###### 1. PyGame kütüphanesinin projeye import edilmesi
###### 2.	Karakterlerin yaratılması
###### 3.	Klavye tuşlarının karakterlere atanması
###### 4.	Sprite animasyon eklenmesi
###### 5.	Mermilerin oluşturulması ve karakterlere atanması
###### 6.	Mermilerin karakterlere verdiği hasarın ayarlanması
###### 7.	Bombaların oluşturulup karakterlere atanması ve karakterlere verdikleri hasarların ayarlanması
###### 8.	Bomba patlama animasyonlarının oluşturulması
###### 9.	Buff kutularının oluşturulması
###### 10.	Buff kutuları ile karakterlerin çarpışmalarının yakalanıp her karakter için buff kontrollerinin yapılması
###### 11.	Haritanın oluşturulması
###### 12.	Harita üzerine itemların yerleştirilmesi
###### 13.	Ses dosyalarının eklenmesi

## Oyun İşleyişi
### Oyun açılış ekranı

<img width="700" height="400" align="center" src="https://user-images.githubusercontent.com/61651202/150359362-b55e6091-d975-4e23-aea6-a82a3ea3ba8b.png">
 
-	Start butonuna tıklandığında oyun başlar. Karakterler alandaki yerlerini alır.
-	Exit Butonu ile oyun kapanır.

### Oyun başladığında karakterler alandaki yerlerini alır
<img width="700" height="400" align="center" src="https://user-images.githubusercontent.com/61651202/150359439-cd68e60d-c3c1-4b9a-b233-26e5120143a0.png">
<img width="700" height="400" align="center" src="https://user-images.githubusercontent.com/61651202/150359558-000825ef-0fa7-4d6f-915f-1081d4dcc181.png">

-	Yukarıda gösterilen görselde görüldüğü gibi karakterlerin can, mermi ve bomba sayıları sağ ve sol üstte gösterilmektedir.
-	Karakterler bomba veya mermi fırlattığında ellerindeki mermi ve bomba sayıları azalır. 
-	Herhangi bir karakterin canı 0’landığında oyun sona erer.
-	Karakterler, karakterlerin mermileri ve karakterlerin bombaları colliderect() fonksiyonu ile kontrol edilir. Bu alan dışına çıkmaları engellenir.

 
### Oyun karakterleri
##	Soldier 

<img width="150" height="200" align="center" src="https://user-images.githubusercontent.com/61651202/150360173-65e6e012-f293-46fd-91bb-6aed40cdedcd.png">
 

-	W,A,S,D tuşları ile hareket eder.
-	Ctrl tuşu ile ateş edip Shift tuşu ile el bombası fırlatır.


##	Robot

<img width="150" height="200" align="center" src="https://user-images.githubusercontent.com/61651202/150360235-edebddb9-fc27-4af0-9d71-41fb1b22332c.png">
 

-	Yön tuşları ile hareket eder.
-	Ctrl tuşu ile ateş edip, Shift tuşu ile bomba fırlatır.

### Karakterlerin hareketleri animasyonlar ile daha güzel görünür hale getirilmiştir.

- Soldier yürüyüş animasyonu
<p align="center">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360375-9dfb5a73-5c70-4e34-bea7-f97a6127f972.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360411-c20d81c2-f06e-4fcf-bfbe-80113dae0010.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360430-07098be5-d385-4e16-80b3-ac8ef734f4ab.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360460-0c22c3b1-83f2-4cf9-9802-ba58f505c961.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360495-28489d8c-708b-4521-b81f-62b94ab1a6b6.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360514-97e76c4e-e4ea-4551-9c8d-e0e1391f0cb5.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360537-5bd1f257-cfaa-491f-ba71-af3180019836.png">
</p>
       
- Soldier zıplama animasyonu
<p align="center">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150360731-dd7a00a4-e555-49b9-b155-ba8aaac54e12.png">
</p>
 
- Soldier ölüm animasyonu
<p align="center">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150361911-d85c0cea-3806-4cb2-9e89-05c519a7c052.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150361950-0c1d66de-21e3-476e-9268-06c5e25ae0fa.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150361984-8df31385-863d-4ae9-8e7b-219cef08fa16.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362011-d29751a1-ce55-48e2-bcc9-5de25c6b96c2.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362026-e7b09733-1cd4-417e-b38d-c23970b311ca.png">
</p>
     
- Robot yürüyüş animasyonu
<p align="center">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362236-9c40ecd4-fefb-42fb-9a19-3271ef0c3515.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362292-3bba9bfb-aacf-4e40-9855-bf8447bb4c64.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362313-8ce33417-710f-4332-aafe-b892d3b64974.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362346-5b67cc41-f5f0-4ce1-b317-e7ebb3e9a2fc.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362375-10caa3d5-a7d3-40f0-b636-8f046e479a89.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362403-9e712a63-083a-46de-87a7-2d526f62f6f1.png">
</p>

- Robot zıplama animasyonu
 <p align="center">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362684-18e29dc0-1d66-478c-be35-78c463769a69.png">
</p>

-Robot ölüm animasyonu
<p align="center">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362860-1244174d-f841-4e7c-b963-d81efd543f36.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362922-5de84c58-c65e-46ec-8c3a-8d026e932b60.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150362996-1fe150a9-5b9a-4ad7-881e-36cc5f12de55.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150363048-5cc122ee-32e3-4fc5-80ab-79237b8b36ad.png">
  <img width="75" height="75" src="https://user-images.githubusercontent.com/61651202/150363101-b239a6ef-6cf9-452d-b73e-69ca6097358a.png">
</p>


### Mermi ve bomba hasarları
-	Karakterler mermi hasarı aldıklarında aşağıdaki görselde görüldüğü gibi can değeri 10 azalır.
<img width="700" height="400" src="https://user-images.githubusercontent.com/61651202/150363525-9847c4c6-30ba-4141-ba90-138d1630b311.png">

-	Karakterler bomba hasarı aldıklarında aşağıdaki görselde görüldüğü gibi can değeri 50 azalır.
<img width="700" height="400" src="https://user-images.githubusercontent.com/61651202/150363558-ecddfc32-9f72-45fc-89b9-4e29df4e506b.png">
 
### Buff Kutuları
-	Karakterler canları azaldığında, veya cephaneleri bittiğinde buff kutuları yardımıyla canlarını ve cephanelerini yenileyebilirler.

-> Healt Box

<img width="50" height="50" src="https://user-images.githubusercontent.com/61651202/150364091-62a6bc0b-489a-4165-b038-51ebe81cd9d1.png">
- Karakterin can değerini +25 yükseltir

-> Ammo Box

<img width="50" height="50" src="https://user-images.githubusercontent.com/61651202/150365016-45964a37-0ee9-42d2-bcf2-d2b12047abd2.png">
- Karakterin mermi miktarını +15 yükseltir.

-> Bomb Box

<img width="50" height="50" src="https://user-images.githubusercontent.com/61651202/150365069-f50db1b0-9b6d-43ed-af09-ec1bbe8d0aa1.png">
- Karakterin bomba miktarını 3 yükseltir.

-> Defence Box

<img width="50" height="50" src="https://user-images.githubusercontent.com/61651202/150365105-0bea1d52-409e-4a74-8511-509a43dad1cf.png">
- Karakterlerin can miktarlarını maksimum seviyede doldurur.

### Karakterler ile buff kutularının çarpışma anları

-Eğer karakterin canı azalmış ise Defence kutusu ile canını doldurabilir.

<img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365254-1d989390-2232-4c98-9db8-ac388eea8e8e.png"> <img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365291-222442a0-dd3f-49e6-8bd2-ab5a3f4080ed.png">
    
-Eğer karakterin Bombası bitmiş ise Bomb kutusundan 3 bomba alabilir.

<img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365322-8fe5e88e-073d-4925-8b1e-8b6a29ee950e.png"> <img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365348-0aaa002e-9bd5-40a1-b0c6-451324a4080e.png">
   
-Eğer karakterin mermisi bitmiş ise Ammo kutusundan 15 mermi alabilir.

<img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365382-366e1afa-6c6a-42db-83c3-56165a77f030.png"> <img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365421-ec8c4777-7574-44db-b255-f23aebeea6cb.png">
   
-Eğer karakterin canı azalmış ise Health kutusundan +25 can alabilir

<img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365448-b778eae6-1b88-45f6-8fb7-61a141a509f3.png"> <img width="350" height="300" src="https://user-images.githubusercontent.com/61651202/150365487-16c43e04-6534-443c-8b76-aefe8ecb46cf.png">
 

### Karakterlerden birinin can değeri sıfırlandığında
-	Can değeri sıfırlanan karakterin hareket etmesi engellenir ve karakter ölüm animasyonuna geçiş yapar.
-	Ekrana Restart butonu bastırılır.
 
 <img width="700" height="400" align="center" src="https://user-images.githubusercontent.com/61651202/150365583-a0685f86-bcc4-4498-a88b-5734988acc57.png">
 
-	Restart butonu ile oyun  tekrardan başlatılır.


## FAYDALANMIŞ OLDUĞUM KAYNAKLAR
 - Sprite dökümantasyonu: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite

- Pygame python'a entegre etmek için kullanılan dökümantasyon: https://www.pygame.org/wiki/GettingStarted
