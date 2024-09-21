from line_drawing import DDA

def clip(screen, elements, clip_method, xmin, ymin, xmax, ymax):
    """
    Executa os algoritmos de recorte conforme o método especificado.
    """
    for elemento in elements:
        if clip_method == "cohen_sutherland":
            cohen_sutherland(screen, xmin, ymin, xmax, ymax, elemento)
        else:
            liang_barsky(screen, xmin, ymin, xmax, ymax, elemento)

def cohen_sutherland(screen, xmin, ymin, xmax, ymax, elemento):

    def calcular_codigo_regiao(x, y):
        codigo = 0

        if x < xmin:  # à esquerda
            codigo |= 1
        if x > xmax:  # à direita
            codigo |= 2
        if y < ymin:  # abaixo
            codigo |= 4
        if y > ymax:  # acima
            codigo |= 8

        return codigo

    aceito = False
    finalizado = False
    ponto_intersecao_x = ponto_intersecao_y = 0

    x1, y1 = elemento["p1"]
    x2, y2 = elemento["p2"]

    while not finalizado:
        codigo1 = calcular_codigo_regiao(x1, y1)
        codigo2 = calcular_codigo_regiao(x2, y2)

        if codigo1 == 0 and codigo2 == 0:
            aceito = True
            finalizado = True
        elif (codigo1 & codigo2) != 0:
            finalizado = True
        else:
            codigo_fora = codigo1 if codigo1 != 0 else codigo2

            if codigo_fora & 1:
                ponto_intersecao_x = xmin
                ponto_intersecao_y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            elif codigo_fora & 2:
                ponto_intersecao_x = xmax
                ponto_intersecao_y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            elif codigo_fora & 4:
                ponto_intersecao_y = ymin
                ponto_intersecao_x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            elif codigo_fora & 8:
                ponto_intersecao_y = ymax
                ponto_intersecao_x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)

            if codigo_fora == codigo1:
                x1, y1 = ponto_intersecao_x, ponto_intersecao_y
                elemento["p1"] = (x1, y1)
            else:
                x2, y2 = ponto_intersecao_x, ponto_intersecao_y
                elemento["p2"] = (x2, y2)

    if aceito:
        DDA(screen, elemento)
    return aceito

def liang_barsky(screen, xmin, ymin, xmax, ymax, elemento):

    def teste_recorte(p, q, u1, u2):
        sucesso = True

        if p < 0:
            r = q / p
            if r > u2:
                sucesso = False
            elif r > u1:
                u1 = r
        elif p > 0:
            r = q / p
            if r < u1:
                sucesso = False
            elif r < u2:
                u2 = r
        elif q < 0:
            sucesso = False

        return sucesso, u1, u2

    x1, y1 = elemento["p1"]
    x2, y2 = elemento["p2"]

    u1, u2 = 0, 1
    delta_x = x2 - x1
    delta_y = y2 - y1

    p = [-delta_x, delta_x, -delta_y, delta_y]
    q = [
        x1 - xmin,
        xmax - x1,
        y1 - ymin,
        ymax - y1,
    ]

    sucesso, u1, u2 = teste_recorte(p[0], q[0], u1, u2)
    sucesso, u1, u2 = teste_recorte(p[1], q[1], u1, u2) and sucesso, u1, u2
    sucesso, u1, u2 = teste_recorte(p[2], q[2], u1, u2) and sucesso, u1, u2
    sucesso, u1, u2 = teste_recorte(p[3], q[3], u1, u2) and sucesso, u1, u2

    if sucesso:
        if u2 < 1:
            x2 = x1 + u2 * delta_x
            y2 = y1 + u2 * delta_y
            elemento["p2"] = (x2, y2)
        if u1 > 0:
            x1 = x1 + u1 * delta_x
            y1 = y1 + u1 * delta_y
            elemento["p1"] = (x1, y1)

        DDA(screen, elemento)
