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

cars = []
for _ in range(5):
    x = random.randint(-600, -50)
    y = random.choice([460, 500])
    c = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    v = random.randint(2, 5)
    cars.append({"x": x, "y": y, "color": c, "velocidad": v})

rect_x = 300
rect_y = 580
rect_ancho = 30
rect_alto = 20
velocidad_rect = 5

game_over = False  

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

    pg.draw.rect(pantalla, ver, (0, 400, 600, 200))
    pg.draw.rect(pantalla, gra, (0, 450, 600, 100))
    for x in range(0, 600, 60):
        pg.draw.rect(pantalla, ama, (x + 10, 495, 40, 10))
    for x in range(50, 600, 200):
        pg.draw.rect(pantalla, roj, (x, 300, 80, 80))
        pg.draw.polygon(pantalla, caf, [(x, 300), (x + 40, 260), (x + 80, 300)])
        pg.draw.rect(pantalla, bla, (x + 20, 330, 20, 20))

    player_rect = pg.Rect(rect_x, rect_y, rect_ancho, rect_alto)  

    for car in cars:
        car_rect = pg.Rect(car["x"], car["y"], 60, 30) 
        pg.draw.rect(pantalla, car["color"], car_rect)
        pg.draw.circle(pantalla, neg, (car["x"] + 10, car["y"] + 30), 6)
        pg.draw.circle(pantalla, neg, (car["x"] + 50, car["y"] + 30), 6)
        car["x"] += car["velocidad"]
        if car["x"] > 600:
            car["x"] = random.randint(-600, -50)
            car["y"] = random.choice([460, 500])
            car["velocidad"] = random.randint(2, 5)
            car["color"] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        if player_rect.colliderect(car_rect):
            game_over = True 

    pg.draw.rect(pantalla, ama, player_rect) 
    pg.display.flip()

# Pantalla de Game Over
font = pg.font.Font(None, 74)
text = font.render("Game Over", True, roj)
text_rect = text.get_rect([300, 300])
pantalla.blit(text, text_rect)
pg.display.flip()

while True:  
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()