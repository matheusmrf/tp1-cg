# Implementação de Algoritmos de Computação Gráfica



## 📖 Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Demonstração](#demonstração)


## Sobre

Este projeto foi desenvolvido como parte do Trabalho Prático da disciplina de **Computação Gráfica**. O objetivo principal foi implementar diversos algoritmos gráficos que envolvem transformações geométricas, rasterização de formas e recorte de linhas. A aplicação possui uma interface gráfica interativa construída com Python e Tkinter, permitindo que os usuários interajam de forma intuitiva através de cliques na área de desenho.

## Funcionalidades

### Transformações Geométricas 2D
- **Translação:** Move objetos no espaço bidimensional conforme vetores fornecidos pelo usuário.
- **Rotação:** Gira objetos em torno de um ponto central com um ângulo especificado.
- **Escala:** Redimensiona objetos aumentando ou diminuindo suas dimensões conforme fatores de escala fornecidos.
- **Reflexões:** Realiza reflexões nos eixos X, Y ou ambos (XY) de acordo com a escolha do usuário.

### Rasterização
- **Retas:**
  - **DDA (Digital Differential Analyzer):** Algoritmo para desenhar linhas de forma eficiente.
  - **Bresenham:** Algoritmo otimizado para desenhar linhas com precisão.
- **Circunferência:**
  - **Bresenham para Circunferências:** Algoritmo para desenhar circunferências de forma precisa.

### Recorte
- **Cohen-Sutherland:** Algoritmo de recorte baseado em regiões codificadas para cortar linhas fora da janela de visualização.
- **Liang-Barsky:** Algoritmo que utiliza a equação paramétrica para recortar linhas de maneira mais eficiente.

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python 3.x
- **Bibliotecas:**
  - `Tkinter` para a interface gráfica
  - `math` para operações matemáticas

## Instalação

### Pré-requisitos

- **Python 3.x** instalado no seu sistema. Você pode baixar o Python [aqui](https://www.python.org/downloads/).

### Passos de Instalação

1. **Clone o Repositório:**

    ```bash
    git clone https://github.com/matheusmrf/tp1-cg.git
    ```

2. **Navegue até o Diretório do Projeto:**

    ```bash
    cd tp1-cg
    ```

3. **Instale as Dependências:**

    Este projeto utiliza apenas bibliotecas padrão do Python, então não há dependências adicionais a serem instaladas.

## Uso

1. **Execute o Programa:**

    ```bash
    python main.py
    ```

2. **Interaja com a Interface:**

    - **Desenhar Formas:**
        - **Retas e Circunferências:** Selecione o algoritmo desejado no menu de rasterização e clique na área de desenho para definir os pontos ou o centro e raio das formas.
   
    - **Aplicar Transformações:**
        - Escolha a transformação no menu de transformações geométricas e insira os parâmetros necessários. As transformações serão aplicadas imediatamente aos objetos selecionados.
   
    - **Recortar Linhas:**
        - Defina a janela de recorte com cliques do mouse e aplique os algoritmos de recorte para visualizar as partes das linhas que permanecem dentro da janela.

3. **Limpar a Tela:**
    - Utilize o botão "Clear" para remover todos os objetos e redefinir as variáveis.

## Demonstração

![Demonstração](assets/demonstracao.gif)

**Descrição:**
- **Desenhando Retas e Circunferências:** Selecionando o algoritmo desejado e clicando para definir os pontos.
- **Aplicando Transformações:** Inserindo valores de translação, rotação, escala ou reflexão para ver os objetos se transformarem dinamicamente.
- **Recortando Linhas:** Definindo a janela de recorte e aplicando os algoritmos para visualizar o recorte das linhas.

## Estrutura do Projeto

