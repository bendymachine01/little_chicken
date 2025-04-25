import pygame as pg
import sys
import random

pg.init()
tam = (600, 600)
pantalla = pg.display.set_mode(tam)
pg.display.set_caption("litle_chicken")

fondo = (135, 206, 235)
ver = (34, 139, 34)
gra = (105, 105, 105)
ama = (255, 255, 0)
roj = (220, 20, 60)
bla = (255, 255, 255)
caf = (139, 69, 19)
neg = (0, 0, 0)

reloj = pg.time.Clock()

# Definimos los límites 'y' de ambas autopistas
autopista_superior_y_inicio = 310
autopista_superior_y_fin = 310 + 130 - 30  # Restamos la altura del carro
autopista_inferior_y_inicio = 490
autopista_inferior_y_fin = 490 + 130 - 30  # Restamos la altura del carro

autopista_superior_y = 310  # Guardamos la 'y' de la autopista superior
cars = []
for _ in range(16):  # Aumentamos la cantidad de carros para llenar ambos carriles
    autopista = random.choice(['superior', 'inferior'])
    if autopista == 'superior':
        y = random.randint(autopista_superior_y_inicio, autopista_superior_y_fin)
    else:
        y = random.randint(autopista_inferior_y_inicio, autopista_inferior_y_fin)
    x = random.randint(-600, -50)
    c = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    v = random.randint(2, 5)
    cars.append({"x": x, "y": y, "color": c, "velocidad": v})

rect_x = 300
rect_y = 580
rect_ancho = 30
rect_alto = 20
velocidad_rect = 5
vidas = 3
puntaje = 0  # Inicializamos el puntaje
font = pg.font.Font(None, 36)

game_over = False
crossed_top_highway = False  # Variable para controlar si ya cruzó la autopista superior

while not game_over:
    reloj.tick(30)
    pantalla.fill(fondo)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()

        if e.type == pg.KEYDOWN:
            if e.key == pg.K_LEFT:
                rect_x -= velocidad_rect
            if e.key == pg.K_RIGHT:
                rect_x += velocidad_rect
            if e.key == pg.K_UP:
                rect_y -= velocidad_rect
            if e.key == pg.K_DOWN:
                rect_y += velocidad_rect

    # Dibujamos las dos secciones de "césped" (ahora muy pequeñas)
    pg.draw.rect(pantalla, ver, (0, 260, 600, 50))
    pg.draw.rect(pantalla, ver, (0, 440, 600, 50))
    # Dibujamos las dos autopistas (ahora mucho más altas y juntas)
    pg.draw.rect(pantalla, gra, (0, 310, 600, 130))
    pg.draw.rect(pantalla, gra, (0, 490, 600, 130))
    # Dibujamos las líneas amarillas en ambas autopistas (ajustando la posición 'y')
    for x in range(0, 600, 60):
        pg.draw.rect(pantalla, ama, (x + 10, 375, 40, 10))
        pg.draw.rect(pantalla, ama, (x + 10, 555, 40, 10))
    # Ajustamos la posición de los obstáculos para que no se superpongan con las autopistas más grandes
    for x in range(50, 600, 200):
        pg.draw.rect(pantalla, roj, (x, 150, 80, 80))
        pg.draw.polygon(pantalla, caf, [(x, 150), (x + 40, 110), (x + 80, 150)])
        pg.draw.rect(pantalla, bla, (x + 20, 180, 20, 20))

    player_rect = pg.Rect(rect_x, rect_y, rect_ancho, rect_alto)

    # Comprobamos si el rectángulo ha cruzado la autopista superior y sumamos puntos una sola vez por cruce
    if rect_y < autopista_superior_y - rect_alto and not crossed_top_highway:
        puntaje += 1
        crossed_top_highway = True
    elif rect_y >= autopista_superior_y_inicio:
        crossed_top_highway = False  # Resetear la variable cuando vuelve a la zona inferior

    for car in cars:
        car_rect = pg.Rect(car["x"], car["y"], 60, 30)
        pg.draw.rect(pantalla, car["color"], car_rect)
        pg.draw.circle(pantalla, neg, (car["x"] + 10, car["y"] + 30), 6)
        pg.draw.circle(pantalla, neg, (car["x"] + 50, car["y"] + 30), 6)
        car["x"] += car["velocidad"]
        if car["x"] > 600:
            # Al reaparecer, el carro elige una autopista y un carril aleatorio
            autopista = random.choice(['superior', 'inferior'])
            if autopista == 'superior':
                car["y"] = random.randint(autopista_superior_y_inicio, autopista_superior_y_fin)
            else:
                car["y"] = random.randint(autopista_inferior_y_inicio, autopista_inferior_y_fin)
            car["x"] = random.randint(-600, -50)
            car["velocidad"] = random.randint(2, 5)
            car["color"] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        if player_rect.colliderect(car_rect):
            vidas -= 1
            if vidas == 0:
                game_over = True
            else:
                rect_x = 300
                rect_y = 580
                crossed_top_highway = False # Resetear al colisionar

    pg.draw.rect(pantalla, ama, player_rect)
    vidas_texto = font.render(f"Vidas: {vidas}", True, neg)
    pantalla.blit(vidas_texto, (10, 10))
    puntaje_texto = font.render(f"Puntaje: {puntaje}", True, neg)
    pantalla.blit(puntaje_texto, (10, 50))
    pg.display.flip()

# Pantalla de Game Over
font_go = pg.font.Font(None, 74)
text_go = font_go.render("Game Over", True, roj)
text_rect_go = text_go.get_rect(center=(300, 300))
pantalla.blit(text_go, text_rect_go)
pg.display.flip()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()