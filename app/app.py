import os
import tkinter as tk

from ttkbootstrap import Window
from app.utils import resource_path
from app.controller.rateio_aporte_controller import RateioAporteController

class App(Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Gestor de Investimentos - JEK")
        self.geometry("600x500")
        self.resizable(False, False)

        icone_path = resource_path("app/image/favicon.png")
        self.iconphoto(False, tk.PhotoImage(file=icone_path))

        RateioAporteController(self)
        