import tkinter as tk
from tkinter import messagebox
import math
import numpy as np
import re
from sympy import symbols, sympify, diff, lambdify
from sympy.core.sympify import SympifyError

x = symbols('x')

# === MÉTODO DA BISSEÇÃO ===
def bissecao(func_str, a, b, epsilon, k_max):
    def f(x):
        return eval(func_str, {"x": x, "math": math})

    if f(a) * f(b) >= 0:
        return "Intervalo inválido: f(a) e f(b) devem ter sinais opostos."

    resultado = f"{'Iter':<5} {'a':<10} {'b':<10} {'x':<10} {'f(x)':<12} {'ER%':<10}\n"
    x_anterior = None

    for k in range(1, k_max + 1):
        x = (a + b) / 2
        fx = f(x)

        # Cálculo do erro relativo percentual (como porcentagem)
        if x_anterior is not None:
            erro_rel = abs((x - x_anterior) / x) * 100
            if erro_rel < epsilon:
                # Parar aqui: erro já abaixo do limite, não registra essa iteração
                resultado += f"\n✨ Raiz aproximada encontrada: {x:.6f} com ER% ≈ {erro_rel:.6f}"
                return resultado
            erro_str = f"{erro_rel:.6f}"
        else:
            erro_str = "-----"

        resultado += f"{k:<5} {a:<10.6f} {b:<10.6f} {x:<10.6f} {fx:<12.6f} {erro_str:<10}\n"

        # Atualiza intervalo
        if f(a) * fx < 0:
            b = x
        else:
            a = x

        x_anterior = x

    resultado += f"\n⚠️ Número máximo de iterações atingido. Raiz aproximada: {x:.6f}"
    return resultado
def resolver_bissecao():
    try:
        func = entrada_func.get()
        a = float(entrada_a.get())
        b = float(entrada_b.get())
        epsilon = float(entrada_epsilon.get())
        k = int(entrada_k.get())

        resultado = bissecao(func, a, b, epsilon, k)
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, resultado)
    except Exception as e:
        messagebox.showerror("Erro", f"Algo deu ruim, revisa os dados:\n{str(e)}")
def abrir_bissecao():
    global metodo_janela
    metodo_janela = tk.Tk()
    metodo_janela.title("✨ Método da Bisseção")
    metodo_janela.configure(bg="#fce4ec")  # Rosa clarinho

    # Centralizar a janela
    centralizar_janela(metodo_janela, 800, 600)

    metodo_janela.grid_columnconfigure(0, weight=1)
    metodo_janela.grid_columnconfigure(1, weight=1)

    fonte_label = ("Segoe UI", 10)
    fonte_titulo = ("Segoe UI", 14, "bold")

    tk.Label(metodo_janela, text="Método da Bisseção 💖", font=fonte_titulo, bg="#fce4ec").grid(row=0, column=0, columnspan=2, pady=10)

    # Instruções
    instrucoes = (
        "✏️ Use 'x' como variável\n"
        "📐 Use ** para potência (ex: x**2)\n"
        "📚 Pode usar funções de math (ex: math.sin(x), math.log10(x), math.e**x)\n"
        "⚠️ f(a) e f(b) devem ter sinais opostos"
    )
    tk.Label(metodo_janela, text=instrucoes, justify="left", bg="#fce4ec", font=("Segoe UI", 9)).grid(row=1, column=0, columnspan=2, pady=5)

    # Entradas
    labels = ["f(x) =", "a =", "b =", "ε =", "k máximo ="]
    entradas = []
    defaults = ["x**3 - 9*x + 3", "0", "1", "0.01", "10"]

    for i, (lbl, default) in enumerate(zip(labels, defaults)):
        tk.Label(metodo_janela, text=lbl, font=fonte_label, bg="#fce4ec").grid(row=i+2, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(metodo_janela, width=30)
        entry.insert(0, default)
        entry.grid(row=i+2, column=1, padx=5, pady=2)
        entradas.append(entry)

    global entrada_func, entrada_a, entrada_b, entrada_epsilon, entrada_k, texto_resultado
    entrada_func, entrada_a, entrada_b, entrada_epsilon, entrada_k = entradas

    # Botões
    tk.Button(metodo_janela, text="🔍 Calcular Raiz", command=resolver_bissecao, bg="#f8bbd0", font=fonte_label).grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(metodo_janela, text="↩️ Voltar", command=lambda: voltar(metodo_janela), bg="#f8bbd0", font=fonte_label).grid(row=8, column=0, columnspan=2)

    # Resultado
    texto_resultado = tk.Text(metodo_janela, height=15, width=60, bg="#fff0f5")
    texto_resultado.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    metodo_janela.mainloop()

# === MÉTODO DA SECANTE ===
def secante(func_str, x0, x1, epsilon, k_max):
    def f(x):
        return eval(func_str, {"x": x, "math": math})

    resultado = f"{'Iter':<5} {'x0':<12} {'x1':<12} {'x2':<12} {'f(x2)':<12} {'ER%':<10}\n"

    for k in range(1, k_max + 1):
        f_x0 = f(x0)
        f_x1 = f(x1)

        if f_x1 - f_x0 == 0:
            return "Divisão por zero na fórmula da secante 🧨"

        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        f_x2 = f(x2)

        # Cálculo do erro relativo percentual
        if k > 1:
            erro_rel = abs((x2 - x1) / x2) * 100
            erro_str = f"{erro_rel:.6f}"

            if erro_rel < epsilon:
                resultado += f"{k:<5} {x0:<12.6f} {x1:<12.6f} {x2:<12.6f} {f_x2:<12.6f} {erro_str:<10}\n"
                resultado += f"\n✨ Raiz aproximada encontrada: {x2:.6f} com ER% ≈ {erro_rel:.6f}"
                return resultado
        else:
            erro_str = "-----"

        resultado += f"{k:<5} {x0:<12.6f} {x1:<12.6f} {x2:<12.6f} {f_x2:<12.6f} {erro_str:<10}\n"

        # Atualiza os valores para a próxima iteração
        x0, x1 = x1, x2

    resultado += f"\n⚠️ Máximo de iterações atingido. Raiz aproximada: {x2:.6f}"
    return resultado
def resolver_secante():
    try:
        func = entrada_func.get()
        x0 = float(entrada_x0.get())
        x1 = float(entrada_x1.get())
        epsilon = float(entrada_epsilon.get())
        k = int(entrada_k.get())

        resultado = secante(func, x0, x1, epsilon, k)
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, resultado)
    except Exception as e:
        messagebox.showerror("Erro", f"Deu ruim... vê isso aqui:\n{str(e)}")
def abrir_secante():
    global metodo_janela
    metodo_janela = tk.Tk()
    metodo_janela.title("🌈 Método da Secante")
    metodo_janela.configure(bg="#fce4ec")

    # Centralizar a janela
    centralizar_janela(metodo_janela, 800, 600)

    # Tornar as colunas expansíveis para centralização
    metodo_janela.grid_columnconfigure(0, weight=1)
    metodo_janela.grid_columnconfigure(1, weight=1)

    fonte_label = ("Segoe UI", 10)
    fonte_titulo = ("Segoe UI", 14, "bold")

    tk.Label(metodo_janela, text="Método da Secante 🌟", font=fonte_titulo, bg="#fce4ec").grid(row=0, column=0, columnspan=2, pady=10)

    instrucoes = (
        "✏️ Use 'x' como variável\n"
        "📐 Use ** para potência (ex: x**2)\n"
        "📚 Pode usar funções de math (ex: math.sin(x), math.log10(x), math.e**x)\n"
        "⚠️ f(a) e f(b) devem ter sinais opostos"
    )
    tk.Label(metodo_janela, text=instrucoes, justify="left", bg="#fce4ec", font=("Segoe UI", 9)).grid(row=1, column=0, columnspan=2, pady=5)

    labels = ["f(x) =", "x0 =", "x1 =", "ε =", "k máximo ="]
    entradas = []
    defaults = ["x**3 - 9*x + 3", "0", "1", "0.01", "10"]

    for i, (lbl, default) in enumerate(zip(labels, defaults)):
        tk.Label(metodo_janela, text=lbl, font=fonte_label, bg="#fce4ec").grid(row=i+2, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(metodo_janela, width=30)
        entry.insert(0, default)
        entry.grid(row=i+2, column=1, padx=5, pady=2)
        entradas.append(entry)

    global entrada_func, entrada_x0, entrada_x1, entrada_epsilon, entrada_k, texto_resultado
    entrada_func, entrada_x0, entrada_x1, entrada_epsilon, entrada_k = entradas

    tk.Button(metodo_janela, text="🌟 Calcular Raiz", command=resolver_secante, bg="#f8bbd0", font=fonte_label).grid(row=7, column=0, columnspan=2, pady=10)
    tk.Button(metodo_janela, text="↩️ Voltar", command=lambda: voltar(metodo_janela), bg="#f8bbd0", font=fonte_label).grid(row=8, column=0, columnspan=2)

    texto_resultado = tk.Text(metodo_janela, height=15, width=60, bg="#fff0f5")
    texto_resultado.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    metodo_janela.mainloop()

# === MÉTODO DA ELIMINAÇÃO DE GAUSS ===
def parse_equation(equation):
    equation = equation.replace(' ', '').lower()
    if '=' not in equation:
        raise ValueError("Equação inválida, deve conter '='")
    left, right = equation.split('=')
    right_val = float(right)
    terms = re.findall(r'([+-]?\d*\.?\d*)?([a-z])', left)
    coeffs = {}
    for coef, var in terms:
        if coef in ('', '+'): coef = 1.0
        elif coef == '-': coef = -1.0
        else: coef = float(coef)
        coeffs[var] = coeffs.get(var, 0) + coef
    return coeffs, right_val
def extrair_matrizes(equacoes):
    # Coletar todas as variáveis que aparecem em qualquer equação
    todas_vars = sorted({var for coef_dict, _ in equacoes for var in coef_dict.keys()})

    A = []
    B = []
    for coef_dict, resultado in equacoes:
        linha = [coef_dict.get(var, 0.0) for var in todas_vars]
        A.append(linha)
        B.append(resultado)

    return np.array(A, dtype=float), np.array(B, dtype=float), todas_vars
def gauss(A, b, debug_texto=None):
    n = len(A)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])  # Matriz aumentada [A|b]

    for i in range(n):
        # Pivotamento parcial (trocar linha atual com a de maior valor absoluto na coluna)
        max_row = np.argmax(abs(M[i:n, i])) + i
        M[[i, max_row]] = M[[max_row, i]]

        if debug_texto is not None:
            debug_texto.insert(tk.END, f"\n🔄 Trocando linhas {i} e {max_row}\n{M}\n")

        # Verifica se o pivô é muito pequeno (evita divisão por quase zero)
        if abs(M[i, i]) < 1e-10:
            raise ValueError(f"Pivô muito pequeno ou nulo na linha {i}. Sistema pode ser impossível ou ter infinitas soluções.")

        for j in range(i + 1, n):
            fator = M[j, i] / M[i, i]
            M[j, i:] -= fator * M[i, i:]
            if debug_texto is not None:
                debug_texto.insert(tk.END, f"\n➡️ Eliminando linha {j} com fator {fator:.4f}\n{M}\n")

    # Verificar inconsistência: linha toda zero com termo independente diferente de zero
    for i in range(n):
        if np.allclose(M[i, :-1], 0) and not np.isclose(M[i, -1], 0):
            raise ValueError(f"Sistema inconsistente detectado na linha {i} (0 = {M[i, -1]:.4f}).")

    # Substituição reversa
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if abs(M[i, i]) < 1e-10:
            raise ValueError(f"Pivô nulo na linha {i}. Sistema pode ter infinitas soluções.")
        soma = sum(M[i, j] * x[j] for j in range(i + 1, n))
        x[i] = (M[i, -1] - soma) / M[i, i]
        if debug_texto is not None:
            debug_texto.insert(tk.END, f"\n🧮 Resolvendo x{i+1} = {x[i]:.4f}\n")

    return x
def resolver_gauss():
    try:
        equacoes = [parse_equation(entry.get()) for entry in entradas_equacoes]
        A, b, vars = extrair_matrizes(equacoes)
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "Sistema interpretado:\n")
        texto_resultado.insert(tk.END, f"Matriz A:\n{A}\n\nVetor B:\n{b}\n\n")
        gauss(A, b, texto_resultado)  # ⬅️ só chama, sem atribuir
    except Exception as e:
        messagebox.showerror("Erro", str(e))
def gerar_campos():
    try:
        n = int(entrada_n.get())
        for widget in frame_equacoes.winfo_children():
            widget.destroy()
        global entradas_equacoes
        entradas_equacoes = []
        for i in range(n):
            label = tk.Label(frame_equacoes, text=f"Equação {i+1}:", bg="#fce4ec")
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(frame_equacoes, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entradas_equacoes.append(entry)
        btn_resolver.grid(row=n+4, column=0, columnspan=2, pady=10)
        btn_voltar.grid(row=n+4, column=1, columnspan=2, pady=5)
        texto_resultado.grid(row=n+5, column=0, columnspan=2, pady=10)
    except ValueError:
        messagebox.showerror("Erro", "Digite um número inteiro válido.")
def abrir_gauss():
    global metodo_janela, entrada_n, entradas_equacoes, btn_resolver, btn_voltar, texto_resultado, frame_equacoes
    metodo_janela = tk.Tk()
    metodo_janela.title("🔢 Eliminação de Gauss")
    metodo_janela.configure(bg="#fce4ec")
    centralizar_janela(metodo_janela, 800, 600)
    metodo_janela.grid_columnconfigure(0, weight=1)
    metodo_janela.grid_columnconfigure(1, weight=1)
    fonte_titulo = ("Segoe UI", 14, "bold")
    fonte_label = ("Segoe UI", 10)

    # Título
    tk.Label(metodo_janela, text="🔢 Resolver Sistema Linear por Eliminação de Gauss", font=fonte_titulo, bg="#fce4ec").grid(row=0, column=0, columnspan=2, pady=10)

    # Instruções (logo após o título)
    instrucoes = (
        "📐 Use letras diferentes para representar x1, x2,..., xn\n"
        "✏️ Digite apenas equações lineares, como: 2x + 3y - z = 5\n"
        "⚠️ Equações devem ter '='"
    )
    tk.Label(
        metodo_janela, text=instrucoes, justify="left", bg="#fce4ec",
        font=("Segoe UI", 9), wraplength=700
    ).grid(row=1, column=0, columnspan=2, pady=5)

    # Entrada número de equações
    tk.Label(metodo_janela, text="Digite o número de equações:", font=fonte_label, bg="#fce4ec").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_n = tk.Entry(metodo_janela, width=10)
    entrada_n.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Botão Gerar Entradas
    btn_gerar = tk.Button(metodo_janela, text="Gerar Entradas", command=gerar_campos, bg="#f8bbd0", font=fonte_label)
    btn_gerar.grid(row=3, column=0, columnspan=2, pady=10)

    # Botão Voltar – sempre visível
    btn_voltar = tk.Button(metodo_janela, text="↩️ Voltar", command=lambda: voltar(metodo_janela), bg="#f8bbd0", font=fonte_label)
    btn_voltar.grid(row=4, column=0, columnspan=2, pady=5)

    # Frame para inserir as equações (será preenchido depois)
    frame_equacoes = tk.Frame(metodo_janela, bg="#fce4ec")
    frame_equacoes.grid(row=5, column=0, columnspan=2)

    # Botão Resolver (aparece depois)
    btn_resolver = tk.Button(metodo_janela, text="Resolver", command=resolver_gauss, bg="#f8bbd0", font=fonte_label)

    # Caixa de texto para mostrar resultado (aparece depois)
    texto_resultado = tk.Text(metodo_janela, height=15, width=60, bg="#fff0f5")

# === MÉTODO DE NEWTON_RAPHSON ===
def abrir_newton():
    global metodo_janela
    metodo_janela = tk.Tk()
    metodo_janela.title("🌀 Método de Newton-Raphson")
    metodo_janela.configure(bg="#fce4ec")

    centralizar_janela(metodo_janela, 800, 600)

    metodo_janela.grid_columnconfigure(0, weight=1)
    metodo_janela.grid_columnconfigure(1, weight=1)

    fonte_label = ("Segoe UI", 10)
    fonte_titulo = ("Segoe UI", 14, "bold")

    tk.Label(metodo_janela, text="Método de Newton-Raphson 🌀", font=fonte_titulo, bg="#fce4ec").grid(row=0, column=0, columnspan=2, pady=10)

    instrucoes = (
    "✏️ Use 'x' como variável\n"
    "📐 Use '**' para potência (exemplo: x**2)\n"
    "📚 Use funções comuns do SymPy: sin(x), cos(x), exp(x), log(x), sqrt(x), etc.\n"
    "🔁 A derivada será calculada automaticamente pelo método"
    )

    tk.Label(metodo_janela, text=instrucoes, justify="left", bg="#fce4ec", font=("Segoe UI", 9)).grid(row=1, column=0, columnspan=2, pady=5)

    labels = ["f(x) =", "x0 =", "ε =", "k máximo ="]
    entradas = []
    defaults = ["x**3 - x - 2", "1.5", "0.0001", "20"]

    for i, (lbl, default) in enumerate(zip(labels, defaults)):
        tk.Label(metodo_janela, text=lbl, font=fonte_label, bg="#fce4ec").grid(row=i+2, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(metodo_janela, width=30)
        entry.insert(0, default)
        entry.grid(row=i+2, column=1, padx=5, pady=2)
        entradas.append(entry)

    global entrada_fx, entrada_x0, entrada_eps, entrada_k, texto_resultado
    entrada_fx, entrada_x0, entrada_eps, entrada_k = entradas

    tk.Button(metodo_janela, text="🚀 Calcular Raiz", command=resolver_newton, bg="#f8bbd0", font=fonte_label).grid(row=6, column=0, columnspan=2, pady=10)
    tk.Button(metodo_janela, text="↩️ Voltar", command=lambda: [metodo_janela.destroy(), criar_tela_selecao()], bg="#f8bbd0", font=fonte_label).grid(row=7, column=0, columnspan=2)

    texto_resultado = tk.Text(metodo_janela, height=15, width=60, bg="#fff0f5")
    texto_resultado.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    metodo_janela.mainloop()
def resolver_newton():
    try:
        fx_expr = sympify(entrada_fx.get())
        x0 = float(entrada_x0.get())
        tol = float(entrada_eps.get())
        k_max = int(entrada_k.get())

        f = lambdify(x, fx_expr, 'math')
        dfx_expr = diff(fx_expr, x)
        df = lambdify(x, dfx_expr, 'math')

        resultado = "Iter  x0         f(x0)       f'(x0)      x1         Erro\n"
        resultado += "-" * 60 + "\n"

        for i in range(1, k_max + 1):
            fx0 = f(x0)
            dfx0 = df(x0)

            if dfx0 == 0:
                raise ZeroDivisionError("Derivada zero")

            x1 = x0 - fx0 / dfx0
            erro = abs(x1 - x0)

            resultado += f"{i:<5} {x0:<10.6f} {fx0:<11.6f} {dfx0:<11.6f} {x1:<10.6f} {erro:.6f}\n"

            if erro < tol:
                resultado += f"\n✨ Raiz aproximada encontrada: {x1:.6f}"
                break

            x0 = x1
        else:
            resultado += "\n⚠️ O método não convergiu no número máximo de iterações."

        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, resultado)

    except (SympifyError, ValueError):
        messagebox.showerror("Erro", "Verifique a função ou os valores inseridos.")
    except ZeroDivisionError:
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "❌ Erro: derivada igual a zero. O método falhou.")

# === Creditos ===
def abrir_creditos():
    def centralizar_janela(janela, largura=800, altura=600):
        janela.update_idletasks()
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    metodo_janela = tk.Tk()
    metodo_janela.title("🌟 Créditos")
    metodo_janela.configure(bg="#fce4ec")
    centralizar_janela(metodo_janela, 800, 600)

    metodo_janela.grid_rowconfigure(0, weight=1)
    metodo_janela.grid_columnconfigure(0, weight=1)

    canvas = tk.Canvas(metodo_janela, bg="#fce4ec", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    frame_scroll = tk.Frame(canvas, bg="#fce4ec")
    window_id = canvas.create_window((0, 0), window=frame_scroll, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        # Atualiza a largura do frame_scroll para a largura do canvas, garantindo centralização
        canvas.itemconfig(window_id, width=event.width)

    frame_scroll.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    def _on_mousewheel(event):
        delta = int(-1 * (event.delta / 120))
        canvas.yview_scroll(delta, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    fonte_titulo = ("Segoe UI", 14, "bold")
    fonte_label = ("Segoe UI", 10)

    tk.Label(frame_scroll, text="🌟 Créditos", font=fonte_titulo, bg="#fce4ec").pack(pady=10)

    Texto = (
        "Instituição: IBMEC | Unidade: Barra | Periodo:2025.1\n"
        "Diciplina: Modelagem Computaciona | Turma: 8002\n"
        "Profa. Danielle Gonçalves Teixeira\n\n"

        "Alunos:\n\n"
        "Alex Euzebio | Matrícula: 202301134358\n"     
    
    )
    # Agora com justify="center" e pack com fill para centralizar horizontalmente
    tk.Label(frame_scroll, text=Texto, justify="center", bg="#fce4ec", font=("Segoe UI", 15)).pack(padx=10, pady=10)

    tk.Button(frame_scroll, text="↩️ Voltar", command=lambda: voltar(metodo_janela), bg="#f8bbd0", font=fonte_label).pack(pady=15)
    

    metodo_janela.mainloop()

# === Funções de utilidade ===
def centralizar_janela(janela, largura=800, altura=600):
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
def voltar(janela):
    janela.destroy()
    criar_tela_selecao()

# === TELA DE SELEÇÃO INICIAL ===
def criar_tela_selecao():
    global tela_inicial
    tela_inicial = tk.Tk()
    tela_inicial.title("🌸 Seletor de Métodos Numéricos")
    tela_inicial.configure(bg="#fce4ec")

    centralizar_janela(tela_inicial, 800, 600)

    tk.Label(tela_inicial, text="🌟 Escolha o método numérico:", font=("Segoe UI", 14, "bold"), bg="#fce4ec").pack(pady=20)

    tk.Button(tela_inicial, text="💎 Bisseção", width=25, height=2, command=lambda: [tela_inicial.destroy(), abrir_bissecao()],
              bg="#f8bbd0", font=("Segoe UI", 11)).pack(pady=10)

    tk.Button(tela_inicial, text="🌈 Secante", width=25, height=2, command=lambda: [tela_inicial.destroy(), abrir_secante()],
              bg="#f8bbd0", font=("Segoe UI", 11)).pack(pady=10)

    tk.Button(tela_inicial, text="🔢 Eliminação de Gauss", width=25, height=2, command=lambda: [tela_inicial.destroy(), abrir_gauss()],
              bg="#f8bbd0", font=("Segoe UI", 11)).pack(pady=10)
    
    tk.Button(tela_inicial, text="🌀 Newton-Raphson", width=25, height=2, command=lambda: [tela_inicial.destroy(), abrir_newton()],
              bg="#f8bbd0", font=("Segoe UI", 11)).pack(pady=10)

    tk.Button(tela_inicial, text="Creditos", width=25, height=2, command=lambda: [tela_inicial.destroy(), abrir_creditos()],
              bg="#f8bbd0", font=("Segoe UI", 11)).pack(pady=10)

    tela_inicial.mainloop()

# === INICIAR O APP ===
criar_tela_selecao()