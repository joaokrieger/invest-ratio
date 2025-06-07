import os
import tkinter as tk

from ttkbootstrap import Window
from src.utils import resource_path
from src.controller.rateio_aporte_controller import RateioAporteController

class App(Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Gestor de Investimentos - JEK")
        self.geometry("600x500")
        self.resizable(False, False)

        icone_path = resource_path("src/image/favicon.png")
        self.iconphoto(False, tk.PhotoImage(file=icone_path))

        RateioAporteController(self)
        