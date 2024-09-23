import tkinter as tk
from tkinter import simpledialog, messagebox

from line_drawing import DDA, bresenham, circ_bresenham, draw_pixel
from transformations import translacao, escala, rotacao, reflexao
from clipping import clip

class Tela:

    def __init__(self):
        self.largura = 1280
        self.altura = 720

        self.xmin = self.ymin = self.xmax = self.ymax = 0
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.clique_total = 0
        self.clique_par = self.clique_total % 2

        # Lista de dicionários representando objetos desenhados
        self.objetos = []  # {id, type, p1, p2, r}

        self.janela = tk.Tk()
        self.menu = tk.Menu(self.janela)
        self.canvas = tk.Canvas()

        self.janela.title("Desenhador Gráfico")
        self.janela.geometry(f"{self.largura}x{self.altura}")

        # Frames principais
        self.main_frame = tk.Frame(self.janela)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def executar(self):
        self.configurar_canvas()
        self.configurar_labels()
        self.configurar_botoes()
        self.configurar_menu_transformacoes()
        self.configurar_menu_rasterizacao()
        self.configurar_menu_recorte()
        self.janela.mainloop()

    # CONFIGURAÇÕES

    def configurar_canvas(self):
        """
        Cria um canvas com scrollbars.
        """
        largura_cv, altura_cv = 800, 600

        self.canvas = tk.Canvas(self.canvas_frame, width=largura_cv,
                                height=altura_cv, bg="light grey")
        self.canvas.bind('<Button-1>', self.on_click_canvas)
        self.canvas.bind('<Button-3>', self.on_click_canvas)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_v = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL,
                                   command=self.canvas.yview)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_h = tk.Scrollbar(self.janela, orient=tk.HORIZONTAL,
                                   command=self.canvas.xview)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.config(scrollregion=(-800, -600, 800, 600),
                           yscrollcommand=scrollbar_v.set,
                           xscrollcommand=scrollbar_h.set)

    def configurar_labels(self):
        """
        Cria labels para exibir coordenadas dos pontos e da janela de recorte.
        """
        estilo_fonte = ("Arial", 12)

        self.label_p1 = tk.Label(self.left_frame,
                                 text=f"P1: ({self.x1}, {self.y1})",
                                 font=estilo_fonte)
        self.label_p1.pack(pady=5)

        self.label_p2 = tk.Label(self.left_frame,
                                 text=f"P2: ({self.x2}, {self.y2})",
                                 font=estilo_fonte)
        self.label_p2.pack(pady=5)

        self.label_xmin = tk.Label(self.left_frame,
                                   text=f"Xmin, Ymin: ({self.xmin}, {self.ymin})",
                                   font=estilo_fonte)
        self.label_xmin.pack(pady=5)

        self.label_xmax = tk.Label(self.left_frame,
                                   text=f"Xmax, Ymax: ({self.xmax}, {self.ymax})",
                                   font=estilo_fonte)
        self.label_xmax.pack(pady=5)

    def configurar_menu_transformacoes(self):
        """
        Cria o menu de transformações geométricas 2D.
        """
        menu_transf = tk.Menu(self.menu, tearoff=0)
        menu_transf.add_command(label="Translação",
                                command=self.on_translacao)
        menu_transf.add_command(label="Rotação",
                                command=self.on_rotacao)
        menu_transf.add_command(label="Escala",
                                command=self.on_escala)
        menu_transf.add_command(label="Reflexões",
                                command=self.on_reflexao)

        self.menu.add_cascade(label="Transformações 2D", menu=menu_transf)
        self.janela.config(menu=self.menu)

    def configurar_menu_rasterizacao(self):
        """
        Cria o menu de algoritmos de rasterização.
        """
        menu_raster = tk.Menu(self.menu, tearoff=0)
        menu_raster.add_command(label="DDA",
                                command=self.on_dda)
        menu_raster.add_command(label="Bresenham",
                                command=self.on_bresenham)
        menu_raster.add_command(label="Circunferência - Bresenham",
                                command=self.on_circ_bresenham)

        self.menu.add_cascade(label="Rasterização", menu=menu_raster)
        self.janela.config(menu=self.menu)

    def configurar_menu_recorte(self):
        """
        Cria o menu de algoritmos de recorte.
        """
        menu_recorte = tk.Menu(self.menu, tearoff=0)
        menu_recorte.add_command(label="Cohen-Sutherland",
                                 command=self.on_cohen_sutherland)
        menu_recorte.add_command(label="Liang-Barsky",
                                 command=self.on_liang_barsky)

        self.menu.add_cascade(label="Recorte", menu=menu_recorte)
        self.janela.config(menu=self.menu)

    def configurar_botoes(self):
        """
        Cria botão para limpar o canvas.
        """
        botao_limpar = tk.Button(self.left_frame,
                                 text="Limpar",
                                 font=("Arial", 12),
                                 command=self.on_limpar)
        botao_limpar.pack(pady=20)

    # MANIPULADORES DE EVENTOS

    def on_translacao(self):
        """
        Executa a transformação de translação.
        """
        tx, ty = self._entrada_vetor("Translação - Distância X, Y:")
        if tx is not None and ty is not None:
            self.canvas.delete("all")
            translacao(self, self.objetos, tx, ty)

    def on_rotacao(self):
        """
        Executa a transformação de rotação.
        """
        theta = self._entrada_inteiro("Rotação - Ângulo (°):")
        if theta is not None:
            self.canvas.delete("all")
            rotacao(self, self.objetos, theta)

    def on_escala(self):
        """
        Executa a transformação de escala.
        """
        sx, sy = self._entrada_vetor("Escala - Fatores X, Y:")
        if sx is not None and sy is not None:
            self.canvas.delete("all")
            escala(self, self.objetos, sx, sy)

    def on_reflexao(self):
        """
        Executa a transformação de reflexão.
        """
        tipo_reflexao = self._entrada_menu("Reflexão - X, Y, XY:")
        if tipo_reflexao in ["X", "Y", "XY"]:
            self.canvas.delete("all")
            reflexao(self, self.objetos, tipo_reflexao)
        else:
            self._alerta("Escolha válida: X, Y ou XY.")

    def on_dda(self):
        """
        Executa o algoritmo DDA para desenho de linha.
        """
        if self.x1 != 0 and self.x2 != 0:
            item = self._adicionar_objeto("dda",
                                          (self.x1, self.y1),
                                          (self.x2, self.y2))
            DDA(self, item)
        else:
            self._alerta("Selecione dois pontos no Canvas.")

    def on_bresenham(self):
        """
        Executa o algoritmo de Bresenham para desenho de linha.
        """
        if self.x1 != 0 and self.x2 != 0:
            item = self._adicionar_objeto("bresenham",
                                          (self.x1, self.y1),
                                          (self.x2, self.y2))
            bresenham(self, item)
        else:
            self._alerta("Selecione dois pontos no Canvas.")

    def on_circ_bresenham(self):
        """
        Executa o algoritmo de Bresenham para desenho de circunferência.
        """
        if self.clique_total == 0:
            self._alerta("Selecione um ponto no Canvas.")
            return

        raio = self._entrada_inteiro("Circunferência - Raio:")
        if raio is not None:
            ponto = (self.x1, self.y1) if self.clique_par else (self.x2, self.y2)
            item = self._adicionar_objeto("circ_bresenham", ponto, (0, 0), raio)
            circ_bresenham(self, item)

    def on_cohen_sutherland(self):
        """
        Executa o algoritmo de recorte Cohen-Sutherland.
        """
        self._reset_contagem_clique()

        if self.xmin != 0:
            self.canvas.delete("default")
            clip(self, self.objetos, "cohen_sutherland",
                 self.xmin, self.ymin, self.xmax, self.ymax)
        else:
            self._alerta("Defina a janela de recorte com o botão direito.")

    def on_liang_barsky(self):
        """
        Executa o algoritmo de recorte Liang-Barsky.
        """
        self._reset_contagem_clique()

        if self.xmin != 0:
            self.canvas.delete("default")
            clip(self, self.objetos, "liang_barsky",
                 self.xmin, self.ymin, self.xmax, self.ymax)
        else:
            self._alerta("Defina a janela de recorte com o botão direito.")

    def on_click_canvas(self, evento):
        """
        Manipulador de cliques no Canvas.
        """
        self.clique_total += 1
        self.clique_par = self.clique_total % 2

        botao = evento.num

        x = self.canvas.canvasx(evento.x)
        y = self.canvas.canvasy(evento.y)

        tag = f"rect{self.clique_par}"

        if self.clique_par:
            # Primeiro ponto
            self.canvas.delete(tag)
            self.x1, self.y1 = x, y
        else:
            # Segundo ponto
            self.canvas.delete(tag)
            self.x2, self.y2 = x, y

            if botao == 3:  # Clique direito
                self._atualizar_janela_recorte()

        draw_pixel(self, x, y, tags=tag)
        self._atualizar_labels()

    def on_limpar(self):
        """
        Limpa o Canvas e reseta as variáveis.
        """
        self._reset_pontos()
        self._reset_janela_recorte()
        self._reset_contagem_clique()
        self._atualizar_labels()
        self.objetos.clear()
        self.canvas.delete("all")

    # MÉTODOS AUXILIARES

    def _reset_pontos(self):
        """
        Reseta os pontos p1 e p2.
        """
        self.x1 = self.y1 = self.x2 = self.y2 = 0

    def _reset_janela_recorte(self):
        """
        Reseta os limites da janela de recorte.
        """
        self.xmin = self.ymin = self.xmax = self.ymax = 0

    def _reset_contagem_clique(self):
        """
        Reseta a contagem de cliques.
        """
        self.clique_total = 0
        self.clique_par = self.clique_total % 2

    def _entrada_menu(self, mensagem="Valor:"):
        return simpledialog.askstring("Entrada", mensagem)

    def _entrada_inteiro(self, mensagem="Valor:"):
        return simpledialog.askinteger("Entrada", mensagem)

    def _entrada_vetor(self, mensagem="Valores:"):
        entrada = simpledialog.askstring("Entrada", mensagem)
        if not entrada:
            self._alerta("Entrada vazia.")
            return None, None

        valores = entrada.split(',')

        if len(valores) == 2:
            try:
                val_x = float(valores[0].strip())
                val_y = float(valores[1].strip())
                return val_x, val_y
            except ValueError:
                self._alerta("Valores inválidos. Use números separados por vírgula.")
        else:
            self._alerta("Formato inválido. Use X,Y.")
        return None, None

    def _alerta(self, mensagem="Atenção!"):
        messagebox.showwarning("Aviso", mensagem)

    def _atualizar_labels(self):
        self.label_p1.config(text=f"P1: ({self.x1}, {self.y1})")
        self.label_p2.config(text=f"P2: ({self.x2}, {self.y2})")
        self.label_xmin.config(text=f"Xmin, Ymin: ({self.xmin}, {self.ymin})")
        self.label_xmax.config(text=f"Xmax, Ymax: ({self.xmax}, {self.ymax})")

    def _atualizar_janela_recorte(self):
        """
        Atualiza e desenha a janela de recorte.
        """
        if self.clique_total > 2:
            self.canvas.delete("clip")

        self.xmin = min(self.x1, self.x2)
        self.ymin = min(self.y1, self.y2)
        self.xmax = max(self.x1, self.x2)
        self.ymax = max(self.y1, self.y2)

        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,
                                     outline="red", tags="clip")
        self._reset_pontos()

    def _adicionar_objeto(self, tipo, p1, p2, raio=0):
        """
        Adiciona um novo objeto à lista de objetos desenhados.
        """
        id_objeto = len(self.objetos) + 1

        objeto = {
            "id": id_objeto,
            "type": tipo,
            "p1": p1,
            "p2": p2,  # (0,0) se não for circunferência
            "r": raio     # 0 se não for circunferência
        }

        self.objetos.append(objeto)
        return objeto

if __name__ == "__main__":
    tela = Tela()
    tela.executar()
