import pygame
import sys

"""
Klasa Lina predstavlja i računa igračeve živote

Prvo odredimo varijable i kreiramo Rect za Health Bar.
Onda putem metoda merimo koliko HP igrač gubi/dobija.

Glavna metoda gde se računa HP je metoda 'hp'.
Sa 'update' metodom se pokreće 'hp' metoda. Ovo ne mora da se deli na 2 metode,
ali pomaže u klasama imati te 'pokretače', odnosno 'wrapper-e'
"""


class Lina(pygame.sprite.Sprite):
    def __init__(self, ekran, pozicija):
        super().__init__()
        self.ekran = ekran
        self.pozicija = pozicija
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect(center=(0, 0))
        self.current_health = (pozicija[0] / 4)
        self.target_health = (pozicija[0] / 2)
        self.max_health = (pozicija[0] / 2)
        self.health_bar_length = (pozicija[0] / 3)
        self.health_ratio = self.max_health / self.health_bar_length

    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self, pozicija):
        self.hp(pozicija)

    def hp(self, pozicija):
        self.health_bar_length = (pozicija[0] / 3)
        pygame.draw.rect(self.ekran, (240, 90, 33), (pozicija[0] / 3, pozicija[1] / 1.5, self.target_health / self.health_ratio, 25))
        pygame.draw.rect(self.ekran, (255, 255, 255), (pozicija[0] / 3, pozicija[1] / 1.5, self.health_bar_length, 25), 2)

    def mrtva(self):
        if self.target_health == 0:
            return True


# Klasa Slika poziva i očitava sliku iz direktorijuma 'Slike' u glavnoj datoteci, na ekran.
class Slika(pygame.sprite.Sprite):
    def __init__(self, ime, velicina, pozicija=(0, 0)):
        super().__init__()
        self.image = pygame.image.load(f".\\Slike\\{ime}")
        self.rect = self.image.get_rect()
        self.image.convert_alpha
        self.rect.top, self.rect.left = pozicija
        self.scale_image(velicina)

    def scale_image(self, velicina):
        #color_depth = self.image.get_bitsize()
        #if color_depth != 24 and color_depth != 32:
            # If the image is not in a supported format, convert it to a 24-bit surface
            #self.image = self.image.convert(24)
        self.image = pygame.transform.scale(self.image, (velicina[0], velicina[1]))


class Pozadina(Slika):
    def __init__(self, ime, velicina, pozicija=(0, 0)):
        super().__init__(ime, velicina)
        self.scale_image_smooth(velicina)

    def scale_image_smooth(self, velicina):
        color_depth = self.image.get_bitsize()
        if color_depth != 24 and color_depth != 32:
            # If the image is not in a supported format, convert it to a 24-bit surface
            self.image = self.image.convert(24)
        self.image = pygame.transform.smoothscale(self.image, velicina)


"""
Klasa MisL kreira, kontroliše i animira miša koji dolazi sa leve strane.

Prvo se otvara lista, u koju se ubacuju sve verzije miša sa leva (3 slike).
self.image je index od napravljene liste, počevši od 0(promenljiva self.trenutan_sprajt). Promenljivu posle povećavamo.
Na izabranu poziciju crtamo prvu sliku miša.

Metoda 'update' prvo povećava vrednost na x osi, i tako pomera mise na desno.
Nakon toga putem manipulisanja promenljive trenutni_sprajt, menja izmedju 3 slike, simulirajući animaciju.

Metode zamah_desni i zamah_levi proveravaju gde su miševi, i najbližeg sredini ekrana ubija. 
"""


class MisL(pygame.sprite.Sprite):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__()
        self.animiran = True
        self.boss_alive = boss_alive
        self.velicina = velicina
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Obican_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Obican_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Obican_3.png"))
        self.trenutan_sprajt = 0
        self.image = self.sprajtovi[self.trenutan_sprajt]
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pozicija

    def update(self, x_promena):
        self.trenutan_sprajt += 0.3
        if self.trenutan_sprajt >= len(self.sprajtovi):
            self.trenutan_sprajt = 0
        self.image = self.sprajtovi[int(self.trenutan_sprajt)]
        self.rect.x += x_promena


#  MisD, MisBryiL, MisBryiD sve nasleđuju od MisL, samo menjaju slike.
class MisD(MisL):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Obican_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Obican_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Obican_3.png"))


class MisBrziL(MisL):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Brzi_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Brzi_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Brzi_3.png"))


class MisBrziD(MisD):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Brzi_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Brzi_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Brzi_3.png"))

class MisSporiL(MisL):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Spori_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Spori_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Levi_Spori_3.png"))


class MisSporiD(MisD):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Spori_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Spori_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Desni_Spori_3.png"))

class MisBossL(MisL):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Boss_levi_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Boss_levi_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Boss_levi_3.png"))


class MisBossD(MisD):
    def __init__(self, pozicija, velicina, boss_alive):
        super().__init__(pozicija, velicina, boss_alive)
        self.sprajtovi = []
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Boss_desni_1.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Boss_desni_2.png"))
        self.sprajtovi.append(pygame.image.load(f".\\Slike\\Boss_desni_3.png"))


"""
Klasa Dugme kreira text na ekranu, na koji moze da se klikne.

Metoda nacrt_okvira kreira novi text okolo vec postojećeg kako bi se video okvir.

Metoda obnovi je okvir/wrapper sa kojim se slika na ekran i text i okvir.

Metode proveri_input i promeni_boju proveravaju input Miša(na PC). Za poziciju se uzima
pygame.mouse.get_pos() pa ako se poklapa sa pozicijom teksta, onda se menja boja, i nešto dešava posle klika.
"""


class Dugme:
    def __init__(self, pozicija, text_input, velicina, boja, boja_okvira):
        self.pozicija = pozicija
        self.text_input = text_input
        self.boja = boja
        self.velicina = velicina
        self.boja_okvira = boja_okvira
        self.render = pygame.font.SysFont("freesansbold.ttf", self.velicina)
        self.text = self.render.render(self.text_input, True, self.boja)
        self.text_rect = self.text.get_rect(center=pozicija)

    def nacrt_okvira(self, surface, color, ovir_velicina):
        okvir_font = pygame.font.SysFont("freesansbold.ttf", self.velicina)
        okvir_text = okvir_font.render(self.text_input, True, color)
        x, y = self.text_rect.topleft
        for offset_x, offset_y in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            surface.blit(okvir_text, (x + offset_x * ovir_velicina, y + offset_y * ovir_velicina))

    def obnovi(self, ekran):
        self.nacrt_okvira(ekran, self.boja_okvira, 2)
        ekran.blit(self.text, self.text_rect)

    def proveri_input(self, pozicija):
        if pozicija[0] in range(self.text_rect.left, self.text_rect.right) and pozicija[1] in range(self.text_rect.top,
                                                                                                    self.text_rect.bottom):
            return True
        return False

    def promeni_boju(self, pozicija):
        if pozicija[0] in range(self.text_rect.left, self.text_rect.right) and pozicija[1] in range(self.text_rect.top,
                                                                                                    self.text_rect.bottom):
            self.text = self.render.render(self.text_input, True, "#F05A21")
        else:
            self.text = self.render.render(self.text_input, True, "white")


class MuteButton:
    def __init__(self, screen, mute_img_path, screen_width, screen_height, scale_factor=0.1):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_factor = scale_factor
        self.mute_img = pygame.image.load(mute_img_path)
        self.mute_button_rect = None
        self.create()

    def create(self):
        # Scale the mute button image
        mute_img_width = int(self.screen_width * self.scale_factor)
        mute_img_height = int(mute_img_width * 0.8)
        self.mute_img = pygame.transform.scale(self.mute_img, (mute_img_width, mute_img_height))

        # Position the mute button in the top right corner
        self.mute_button_rect = self.mute_img.get_rect()
        self.mute_button_rect.topright = (self.screen_width - 280, 220)

    def draw(self):
        # Draw the mute button
        self.screen.blit(self.mute_img, self.mute_button_rect.topleft)
