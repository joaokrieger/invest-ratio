import tkinter as tk
import json
import os
import shutil
from tkinter import messagebox
from src.utils import resource_path
from src.view.rateio_aporte_view import RateioAporteView

class RateioAporteController:
    def __init__(self, root):
        self.view = RateioAporteView(root, self)
        self.view.controller = self

        self.user_data_dir = self.get_diretorio()
        os.makedirs(self.user_data_dir, exist_ok=True)

        self.data_file = os.path.join(self.user_data_dir, "percentuais_investimento.json")
        self.verifica_arquivo_json()
        self.carregar_percentuais()

    def get_diretorio(self):
        home = os.path.expanduser("~")
        appdata = os.getenv('APPDATA')
        return os.path.join(appdata or home, "GestorInvestimentos")

    def verifica_arquivo_json(self):
        if not os.path.exists(self.data_file):
            try:
                source = resource_path("src/data/percentuais_investimento.json")
                shutil.copyfile(source, self.data_file)
            except Exception as e:
                with open(self.data_file, "w") as f:
                    json.dump({}, f)

    def get_categorias(self):
        return [
            "Renda Fixa",
            "Ações",
            "Fundos Multimercados",
            "Fundos Imobiliários (FIIs)",
            "Criptomoedas",
            "Internacional (BDRs e ETFs)"
        ]

    def atualizar_saldo(self, *_):
        try:
            saldo = self.view.remuneracao.get() - self.view.despesa.get()
            self.view.saldo.set(max(saldo, 0.0))
            for nome in self.view.percentuais:
                self.atualizar_valor(nome)
        except tk.TclError:
            pass

    def atualizar_valor(self, nome):
        try:
            total = sum(var.get() for var in self.view.percentuais.values())
            if total > 100:
                messagebox.showwarning("Limite excedido", "A soma dos percentuais não pode passar de 100%.")
                self.view.percentuais[nome].set(0.0)
                return

            percentual = self.view.percentuais[nome].get()
            valor = self.view.saldo.get() * percentual / 100
            self.view.valores[nome].set(round(valor, 2))
            self.atualizar_percentual_restante()
        except tk.TclError:
            pass

    def atualizar_percentual_restante(self):
        try:
            total = sum(var.get() for var in self.view.percentuais.values())
            restante = max(0.0, 100.0 - total)
            self.view.percentual_restante.set(round(restante, 2))
        except tk.TclError:
            pass

    def gravar_percentuais(self):
        dados = {nome: var.get() for nome, var in self.view.percentuais.items()}
        try:
            with open(self.data_file, "w") as f:
                json.dump(dados, f, indent=4)
            messagebox.showinfo("Sucesso", "Percentuais gravados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{e}")

    def carregar_percentuais(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    dados = json.load(f)
                for nome, valor in dados.items():
                    if nome in self.view.percentuais:
                        self.view.percentuais[nome].set(valor)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo:\n{e}")
