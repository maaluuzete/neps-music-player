import csv
import queue
import ttkbootstrap as tb
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import messagebox

corfundo= "#EAF2F8"
cordestaque= "#A7C7E7"
cortexto= "#34495E"
fontetitulo= ("Segoe UI Semilight", 16)
fontetexto= ("Segoe UI", 11)

def carregarbiblioteca(caminho):
    biblioteca = {}
    try:
        with open(caminho, newline='', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor, None)

            for linha in leitor:
                if len(linha) != 3:
                    print(f"[AVISO] Linha inválida ignorada: {linha}")
                    continue

                titulo, artista, duracao = linha
                biblioteca[titulo] = (artista, int(duracao))

    except FileNotFoundError:
        print("Arquivo songs.csv não encontrado.")

    return biblioteca

class NepsMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("NepsMusic Player")
        self.root.geometry("800x400")
        self.biblioteca = carregarbiblioteca("songs.csv")
        self.tocarseguir = queue.SimpleQueue() 
        self.historico = queue.LifoQueue()
        self.musicas = list(self.biblioteca.keys())
        self.indiceatual = 0
        self.musicaatual = None
        self.pausado = False
        self.criarinterface()

    def criarinterface(self):
        frame = tb.Frame(self.root, padding=15)
        frame.pack(fill=BOTH, expand=True)

        self.labelstatus = tb.Label(
            frame,
            text="Nenhuma música tocando",
            font=fontetitulo,
            foreground=cortexto
        )
        self.labelstatus.pack(pady=10)
        controles = tb.Frame(frame)
        controles.pack(pady=15)
        tb.Button(
            controles,
            text="⏯",
            bootstyle="info-outline",
            width=8,
            command=self.tocarpausar
        ).pack(side=LEFT, padx=6)
        tb.Button(
            controles,
            text="⏭",
            bootstyle="info-outline",
            width=8,
            command=self.proxima
        ).pack(side=LEFT, padx=6)

        tb.Button(
            controles,
            text="⏮",
            bootstyle="info-outline",
            width=8,
            command=self.voltar
        ).pack(side=LEFT, padx=6)

        listas = tb.Frame(frame)
        listas.pack(fill=BOTH, expand=True, pady=10)

        self.listabiblioteca = tk.Listbox(
            listas,
            font=fontetexto,
            bg="#F7FBFF",
            fg=cortexto,
            selectbackground=cordestaque,
            relief=FLAT
        )
        self.listabiblioteca.pack(side=LEFT, fill=BOTH, expand=True, padx=6)
        self.listabiblioteca.bind("<Double-Button-1>", self.adicionarfila)
        self.listafila = tk.Listbox(
            listas,
            font=fontetexto,
            bg="#F7FBFF",
            fg=cortexto,
            selectbackground=cordestaque,
            relief=FLAT
        )
        self.listafila.pack(side=LEFT, fill=BOTH, expand=True, padx=6)

        self.listahistorico = tk.Listbox(
            listas,
            font=fontetexto,
            bg="#F7FBFF",
            fg=cortexto,
            selectbackground=cordestaque,
            relief=FLAT
        )
        self.listahistorico.pack(side=LEFT, fill=BOTH, expand=True, padx=6)
        for musica in self.musicas:
            self.listabiblioteca.insert(END, musica)

    def tocarpausar(self):
        if self.musicaatual is None:
            self.tocarproximamusica()
        else:
            self.pausado = not self.pausado
            estado = "Pausado" if self.pausado else "Tocando"
            self.labelstatus.config(text=f"{estado}: {self.musicaatual}")

    def tocarproximamusica(self):
        if self.musicaatual is not None:
            self.historico.put(self.musicaatual)
            self.listahistorico.insert(END, self.musicaatual)

        if not self.tocarseguir.empty():
            self.musicaatual = self.tocarseguir.get()
            self.listafila.delete(0)
        else:
            if self.indiceatual >= len(self.musicas):
                messagebox.showinfo("Fim", "Não há mais músicas.")
                return

            self.musicaatual = self.musicas[self.indiceatual]
            self.indiceatual +=1

        self.pausado = False
        self.labelstatus.config(text=f"Tocando: {self.musicaatual}")

    def proxima(self):
        self.tocarproximamusica()

    def voltar(self):
        if self.historico.empty():
            messagebox.showinfo("Histórico", "Nenhuma música anterior.")
            return

        self.musicaatual = self.historico.get()
        self.listahistorico.delete(END)
        self.labelstatus.config(text=f"Tocando: {self.musicaatual}")

    def adicionarfila(self, event):
        selecao = self.listabiblioteca.curselection()
        if selecao:
            musica = self.listabiblioteca.get(selecao)
            self.tocarseguir.put(musica)
            self.listafila.insert(END, musica)

if __name__ == "__main__":
    app = tb.Window(themename="flatly")
    NepsMusicPlayer(app)
    app.mainloop()
