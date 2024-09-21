import math
from line_drawing import draw

def translacao(screen, elementos, tx, ty):
    """
    Realiza a translação 2D dos elementos.
    """
    for elemento in elementos:
        nova_p1 = (elemento["p1"][0] + tx, elemento["p1"][1] + ty)
        nova_p2 = (elemento["p2"][0] + tx, elemento["p2"][1] + ty)

        elemento["p1"] = nova_p1
        elemento["p2"] = nova_p2

        draw(screen, elemento)

def escala(screen, elementos, sx, sy):
    """
    Realiza a escala dos elementos.
    """
    for elemento in elementos:
        nova_p1 = (elemento["p1"][0] * sx, elemento["p1"][1] * sy)
        nova_p2 = (elemento["p2"][0] * sx, elemento["p2"][1] * sy)
        novo_raio = elemento["r"] * max(sx, sy)

        elemento["p1"] = nova_p1
        elemento["p2"] = nova_p2
        elemento["r"] = novo_raio

        draw(screen, elemento)

def rotacao(screen, elementos, angulo):
    """
    Realiza a rotação dos elementos.
    """
    radiano = math.radians(angulo)

    cos_theta = math.cos(radiano)
    sin_theta = math.sin(radiano)

    for elemento in elementos:
        x1, y1 = elemento["p1"]
        x2, y2 = elemento["p2"]

        x1_rot = x1 * cos_theta - y1 * sin_theta
        y1_rot = x1 * sin_theta + y1 * cos_theta
        x2_rot = x2 * cos_theta - y2 * sin_theta
        y2_rot = x2 * sin_theta + y2 * cos_theta

        elemento["p1"] = (x1_rot, y1_rot)
        elemento["p2"] = (x2_rot, y2_rot)

        draw(screen, elemento)

def reflexao(screen, elementos, tipo_reflexao):
    """
    Realiza a reflexão dos elementos.
    """
    for elemento in elementos:
        x1, y1 = elemento["p1"]
        x2, y2 = elemento["p2"]

        if tipo_reflexao == "X":
            elemento["p1"] = (x1, -y1)
            elemento["p2"] = (x2, -y2)
        elif tipo_reflexao == "Y":
            elemento["p1"] = (-x1, y1)
            elemento["p2"] = (-x2, y2)
        elif tipo_reflexao == "XY":
            elemento["p1"] = (-x1, -y1)
            elemento["p2"] = (-x2, -y2)

        draw(screen, elemento)
