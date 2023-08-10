import pygame
from main import sat
from pygame import mixer

"""
Funkcija pritisni proverava vrstu inputa

U zavisnosti od 'type' eventa u main While loopu,
funkcija vraća True.

Parametri:
tip - vrsta inputa u (str) formatu
e - vrsta eventa u main for loopu (ugrađeni pygame eventi)
"""


def pritisni(tip, e):
    if tip == "Klik" and e.type == pygame.MOUSEBUTTONDOWN:
        return True
    if tip == "Quit" and e.type == pygame.QUIT:
        return True
    if tip == "Dugme" and e.type == pygame.KEYDOWN:
        return True


"""
Funkcija key_event proverava koje dugme je pritisnuto

U zavisnosti od 'type' 'key-a' u main While loopu,
funkcija vraca True. Čini preglednije šta se stvarno dešava.

Parametri:
key - dugme u (str) formatu
e - vrsta 'key-a' u 'pritisni' funkciji
"""


def key_event(key, e):
    if key == "Levo" and e.key == pygame.K_LEFT:
        return True
    if key == "Desno" and e.key == pygame.K_RIGHT:
        return True
    if key == "A" and e.key == pygame.K_a:
        return True
    if key == "F" and e.key == pygame.K_f:
        return True
    if key == "UP" and e.key == pygame.K_UP:
        return True
    if key == "Spejs" and e.key == pygame.K_SPACE:
        return True
    if key == "ESC" and e.key == pygame.K_ESCAPE:
        return True


"""
Funkcija skraćuje kod, poyivavši potrebne metode za svaki main while loop.

pygame.displaz.update() - bez ove metode, ne bi se ništa videlo na ekranu
sat.tick(60) - FPS
"""


def naslov(text):
    pygame.display.set_caption(str(text))


"""
Funkcije get_zvuk i get_muziku nalaze i puštaju .wav fajlove

get_zvuk  koristi .Sound iz pygame.mixer,
get_muziku koristi .music 
funkcionišu na sličan način, samo što je .music predviđen za pozadinsku muziku,
dok je .Sound za VFX.

Parametri:
lokacija - kada se poziva funkcija, dovoljno je da se napiše ime fajla
jacina - moze da se promeni ali i nemora
"""


def get_zvuk(lokacija, jacina=1):
    zvuk = mixer.Sound(f".\\Audio\\{str(lokacija)}")
    zvuk.set_volume(float(jacina))
    zvuk.play()


def get_muziku(lokacija, jacina=1):
    pygame.mixer.music.load(f".\\Audio\\{str(lokacija)}")
    pygame.mixer.music.set_volume(float(jacina))
    pygame.mixer.music.play(loops=-1)


"""
Funkcija namesti_font podešava font nekom objektu

Parametri:
text - šta će da piše
velicina - (širina, visina)
font - naziv fonta iz sistema
boja - narandzasta po defaultu
"""


def namesti_font(text, velicina, font="freesansbold.ttf", boja="#F05A21"):
    return pygame.font.SysFont(font, velicina).render(text, True, boja)


"""
Funkcija napravi_rect stvara Surface, ispuni ga bojom, i crta ga na ekran

pygame.Surface - stvara površinu
pygame.draw.rect - ocrtava gde se površina nalazi
drugi .draw.rect - ocrtava "stroke" odnosno okvir
"""


def napravi_rect(sirina, visina, unutrasnja_boja=(50, 50, 50), boja_okvira=(255, 255, 255)):
    povrsina = pygame.Surface((sirina, visina))
    pygame.draw.rect(povrsina, unutrasnja_boja, (0, 0, sirina, visina))
    pygame.draw.rect(povrsina, boja_okvira, (0, 0, sirina, visina), 2)
    return povrsina


"""
Funkcija napravi_bar se odnosi na stamina i cooldown barove, mada može se koristiti i za kreiranje drugih.

Parametri:
cd - Cooldown(odbrojavanje) od pritiska tastera C
stam - Broj iskorišćenih zamaha, stavljenih u listu u main.py
max_cd - Koliki je limit za odbrojavanje, podešen je na 5 sekundi
max_stam - Koliko treba zamaha da se iskoristi da bi se bar napunio
helper - Bool parametar implementiran da bi se ova hard coded funkcija samo jednom pisala a ne dva puta.
"""


def napravi_bar(cd, stam, max_cd, max_stam, helper, velicina):
    sirina = velicina[0] / 10
    visina = velicina[1] / 30
    surface = pygame.Surface((sirina, visina))
    surface.fill((128, 128, 128))
    ispunjena_sirina_cd = int(cd / max_cd * sirina)
    ispunjena_sirina_stam = int(stam / max_stam * sirina)
    cd_boja = (53, 119, 29)
    stam_boja = (166, 13, 25)
    if cd < 5 and helper:
        pygame.draw.rect(surface, (119, 65, 29), (0, 0, ispunjena_sirina_cd, visina))
    elif cd >= 5 and helper:
        pygame.draw.rect(surface, cd_boja, (0, 0, ispunjena_sirina_cd, visina))
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, sirina, visina), 2)

    if stam < 10 and not helper:
        pygame.draw.rect(surface, (50, 50, 50), (0, 0, ispunjena_sirina_stam, visina))
    elif stam >= 10 and not helper:
        pygame.draw.rect(surface, stam_boja, (0, 0, ispunjena_sirina_stam, visina))
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, sirina, visina), 2)

    return surface


"""
Sledeće 4 funkcije nalaze miša najbližeg sredini

Ako je m.rect.x (miševa x osa) između polovine ekrana i jednog od krajeva,
i ako je m.rect.x najveći/najmanji (zavisi koja grupa) u grupi miševa, taj miš je najbliži sredini, 
pa će Lina njega prvog da uhvati.

Parametri:
m - miš koji će biti u grupi miševa
ekran_velicina - varijabla za indeksiranje širine ekrana (x osa)
grupa - grupa miševa, leva, desna ili brza
"""

def levi_zamah_max(m, ekran_velicina, grupa):
    misevi = [i for i in grupa if -(ekran_velicina[0] // 48) < i.rect.x < (ekran_velicina[0] // 2.1)]
    if misevi:
        max_x = max([i.rect.x for i in misevi])
        if m.rect.x == max_x:
            return True
        
def levi_zamah_min(m, ekran_velicina, grupa):
    misevi = [i for i in grupa if -(ekran_velicina[0] // 48) < i.rect.x < (ekran_velicina[0] // 2.1)]
    if misevi:
        max_x = min([i.rect.x for i in misevi])
        if m.rect.x == max_x:
            return True

def desni_zamah_max(m, ekran_velicina, grupa):
    misevi = [i for i in grupa if ((ekran_velicina[0]) // 2.1) < i.rect.x < ekran_velicina[0]]
    if misevi:
        max_x = max([i.rect.x for i in misevi])
        if m.rect.x == max_x:
            return True


def desni_zamah_min(m, ekran_velicina, grupa):
    misevi = [i for i in grupa if ((ekran_velicina[0]) // 2.1) < i.rect.x < ekran_velicina[0]]
    if misevi:
        max_x = min([i.rect.x for i in misevi])
        if m.rect.x == max_x:
            return True

def nacrtaj_slider(position, ekran, ekran_velicina, bar_x, bar_y):
    font = pygame.font.Font(None, 42)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    # Calculate the position of the slider bar
    bar_width = ekran_velicina[0] // 6
    bar_height = 15

    # Calculate the position of the slider button
    button_radius = 10
    button_x = bar_x + int(position * bar_width)
    button_y = bar_y

    

    # Draw the slider bar
    pygame.draw.rect(ekran, WHITE, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(ekran, (240, 90, 33), (bar_x, bar_y, bar_width, bar_height), 1)
    
    # Draw the slider button
    pygame.draw.circle(ekran, (240, 90, 33), (button_x, button_y), button_radius)
    
    # Draw the volume percentage
    if bar_y > ekran_velicina[1] // 6:
        volume_text = font.render(f"{int(position * 100)}%", True, (240, 90, 33))
        text_rect = volume_text.get_rect(center=(ekran_velicina[0] // 1.2, ekran_velicina[1] // 3.6))
        ekran.blit(volume_text, text_rect)
    else:
        volume_text = font.render(f"{int(position * 100)}%", True, (240, 90, 33))
        text_rect = volume_text.get_rect(center=(ekran_velicina[0] // 1.2, ekran_velicina[1] // 7.2))
        ekran.blit(volume_text, text_rect)


def skor_save(skor, mode_helper, haj_skor):
    if skor > haj_skor and mode_helper:
        haj_skor = skor
        with open('Options\\skor.txt', 'w') as file:
            file.write(str(haj_skor))

def music_save(volume, new_volume):
    if volume != new_volume:
        with open('Options\\music.txt', 'w') as file:
            file.write(str(new_volume))

def sound_save(volume2, new_volume2):
    if volume2 != new_volume2:
        with open('Options\\SFX.txt', 'w') as file:
            file.write(str(new_volume2))

def low_res_save(ekran_velicina):
    if ekran_velicina[0] == 1280:
        with open('Options\\resolution.txt', 'w') as file:
            file.write(str(ekran_velicina[0]))

def mid_res_save(ekran_velicina):
    if ekran_velicina[0] == 1600:
        with open('Options\\resolution.txt', 'w') as file:
            file.write(str(ekran_velicina[0]))

def high_res_save(ekran_velicina):
    if ekran_velicina[0] == 1920:
        with open('Options\\resolution.txt', 'w') as file:
            file.write(str(ekran_velicina[0]))

def fullscreen_save(helper):
    if helper:
        with open('Options\\type_resolution.txt', 'w') as file:
            file.write('Fullscreen')

def windowed_save(helper):
    if not helper:
        with open('Options\\type_resolution.txt', 'w') as file:
            file.write('Windowed')

def save_all(skor, mode_helper, volume, new_volume, volume2, new_volume2, ekran_velicina, haj_skor, helper):
    skor_save(skor, mode_helper, haj_skor)
    music_save(volume, new_volume)
    sound_save(volume2, new_volume2)
    low_res_save(ekran_velicina)
    mid_res_save(ekran_velicina)
    high_res_save(ekran_velicina)
    fullscreen_save(helper)
    windowed_save(helper)
    

def get_closest_mouse_to_middle(grupa, ekran_velicina):
    middle_x = ekran_velicina[0] // 2  # Calculate the x-coordinate of the middle of the screen

    # Filter the group to get only the mice that are on the left side of the screen
    mice_on_left = [mouse for mouse in grupa if mouse.rect.x < middle_x]

    # Find the mouse from the filtered group with the x-coordinate closest to the middle
    closest_mouse = min(mice_on_left, key=lambda mouse: abs(mouse.rect.x - middle_x))

    return closest_mouse