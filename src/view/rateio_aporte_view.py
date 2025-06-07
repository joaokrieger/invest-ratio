import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class RateioAporteView(tk.Frame):
    
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack(fill='both', expand=True)

        self.saldo = tk.DoubleVar()
        self.entrada_saida_frame()
        self.percentual_frame()

    def entrada_saida_frame(self):
        group = ttk.LabelFrame(self, text="Entradas / Saídas")
        group.pack(fill='x', padx=10, pady=10)

        self.remuneracao = tk.DoubleVar()
        self.despesa = tk.DoubleVar()

        ttk.Label(group, text="Remuneração mensal:").grid(row=0, column=0, sticky='w')
        ttk.Entry(group, textvariable=self.remuneracao).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(group, text="Despesa mensal:").grid(row=1, column=0, sticky='w')
        ttk.Entry(group, textvariable=self.despesa).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(group, text="Saldo disponível:").grid(row=2, column=0, sticky='w')
        ttk.Entry(group, textvariable=self.saldo, state='readonly').grid(row=2, column=1, padx=5, pady=5)

        self.remuneracao.trace_add('write', self.controller.atualizar_saldo)
        self.despesa.trace_add('write', self.controller.atualizar_saldo)

    def percentual_frame(self):
        group = ttk.LabelFrame(self, text="Percentuais de Investimento")
        group.pack(fill='x', padx=10, pady=10)

        self.percentuais = {}
        self.valores = {}

        categorias = self.controller.get_categorias()

        for i, nome in enumerate(categorias):
            ttk.Label(group, text=nome + " (%):").grid(row=i, column=0, sticky='w')

            var_p = tk.DoubleVar()
            ttk.Entry(group, textvariable=var_p, width=10).grid(row=i, column=1, padx=5, pady=2)

            ttk.Label(group, text="Valor (R$):").grid(row=i, column=2, sticky='w')
            var_v = tk.DoubleVar()
            ttk.Entry(group, textvariable=var_v, state='readonly', width=15).grid(row=i, column=3, padx=5, pady=2)

            self.percentuais[nome] = var_p
            self.valores[nome] = var_v

            var_p.trace_add('write', lambda *_ , n=nome: self.controller.atualizar_valor(n))

        ttk.Label(group, text="Percentual restante (%):").grid(row=len(categorias), column=0, sticky='w')
        self.percentual_restante = tk.DoubleVar()
        ttk.Entry(group, textvariable=self.percentual_restante, state='readonly', width=10).grid(row=len(categorias), column=1)

        group.columnconfigure(3, weight=1)

        ttk.Button(group, text="Gravar Percentuais", command=self.controller.gravar_percentuais)\
            .grid(row=len(categorias)+1, column=3, sticky='e', padx=10,pady=10)

