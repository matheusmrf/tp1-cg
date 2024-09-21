def draw_pixel(screen, x, y, tags="default"):
    screen.canvas.create_rectangle(x, y, x+1, y+1, tags=tags)

def draw(screen, elemento):
    """
    Executa as funções de desenho conforme o tipo do elemento.
    """
    print(elemento)
    if elemento["type"] == "circ_bresenham":
        circ_bresenham(screen, elemento)
    else:
        DDA(screen, elemento)

def DDA(screen, elemento):

    x1, y1 = elemento["p1"]
    x2, y2 = elemento["p2"]

    delta_x = int(x2 - x1)
    delta_y = int(y2 - y1)

    passos = abs(delta_x) if abs(delta_x) > abs(delta_y) else abs(delta_y)

    incremento_x = delta_x / passos
    incremento_y = delta_y / passos

    x, y = x1, y1

    draw_pixel(screen, x, y)

    for _ in range(passos):
        x += incremento_x
        y += incremento_y
        draw_pixel(screen, x, y)

def circ_bresenham(screen, elemento):

    def plotar_pontos_circulo(screen, xc, yc, x, y):
        draw_pixel(screen, xc + x, yc + y)
        draw_pixel(screen, xc - x, yc + y)
        draw_pixel(screen, xc + x, yc - y)
        draw_pixel(screen, xc - x, yc - y)
        draw_pixel(screen, xc + y, yc + x)
        draw_pixel(screen, xc - y, yc + x)
        draw_pixel(screen, xc + y, yc - x)
        draw_pixel(screen, xc - y, yc - x)

    xc, yc = elemento["p1"]
    raio = elemento["r"]

    x, y = 0, raio
    p = 3 - 2 * raio

    plotar_pontos_circulo(screen, xc, yc, x, y)

    while x < y:
        if p < 0:
            p += 4 * x + 6
        else:
            p += 4 * (x - y) + 10
            y -= 1
        x += 1
        plotar_pontos_circulo(screen, xc, yc, x, y)

def bresenham(screen, elemento):

    x1, y1 = elemento["p1"]
    x2, y2 = elemento["p2"]

    delta_x = int(x2 - x1)
    delta_y = int(y2 - y1)

    if delta_x >= 0:
        passo_x = 1
    else:
        passo_x = -1
        delta_x = -delta_x

    if delta_y >= 0:
        passo_y = 1
    else:
        passo_y = -1
        delta_y = -delta_y

    x, y = x1, y1

    draw_pixel(screen, x, y)

    if delta_y < delta_x:
        p = 2 * delta_y - delta_x
        c1 = 2 * delta_y
        c2 = 2 * (delta_y - delta_x)

        for _ in range(delta_x):
            x += passo_x
            if p < 0:
                p += c1
            else:
                y += passo_y
                p += c2
            draw_pixel(screen, x, y)
    else:
        p = 2 * delta_x - delta_y
        c1 = 2 * delta_x
        c2 = 2 * (delta_x - delta_y)

        for _ in range(delta_y):
            y += passo_y
            if p < 0:
                p += c1
            else:
                x += passo_x
                p += c2
            draw_pixel(screen, x, y)
