import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("jc_prodlimp.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_unit REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_conn():
    return sqlite3.connect("jc_prodlimp.db")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JC Prodlimp — Controle de Vendas")
        self.geometry("950x620")
        self.configure(bg="#f0f4f8")
        init_db()
        self._build_ui()
        self.load_pedidos()

    def _build_ui(self):
        header = tk.Frame(self, bg="#1a56a0", height=60)
        header.pack(fill="x")
        tk.Label(header, text="JC Prodlimp — Sistema de Vendas",
                 bg="#1a56a0", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=12)

        body = tk.Frame(self, bg="#f0f4f8")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        form_frame = tk.LabelFrame(body, text=" Novo Pedido ",
                                   bg="#f0f4f8", fg="#1a56a0",
                                   font=("Arial", 11, "bold"), bd=2)
        form_frame.pack(side="left", fill="y", padx=(0,15), ipadx=10, ipady=10)

        campos = [("Cliente:", "entry_cliente"), ("Produto:", "entry_produto"),
                  ("Quantidade:", "entry_qtd"), ("Valor unitario (R$):", "entry_valor")]

        for i, (label, attr) in enumerate(campos):
            tk.Label(form_frame, text=label, bg="#f0f4f8",
                     font=("Arial", 10)).grid(row=i, column=0, sticky="w", pady=6, padx=8)
            entry = tk.Entry(form_frame, width=22, font=("Arial", 10))
            entry.grid(row=i, column=1, pady=6, padx=8)
            setattr(self, attr, entry)

        tk.Label(form_frame, text="Status:", bg="#f0f4f8",
                 font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=6, padx=8)
        self.combo_status = ttk.Combobox(form_frame, width=19,
                                         values=["Pendente","Em andamento","Entregue","Cancelado"],
                                         state="readonly", font=("Arial", 10))
        self.combo_status.set("Pendente")
        self.combo_status.grid(row=4, column=1, pady=6, padx=8)

        btn_frame = tk.Frame(form_frame, bg="#f0f4f8")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=14)

        tk.Button(btn_frame, text="Adicionar", command=self.add_pedido,
                  bg="#1a56a0", fg="white", font=("Arial", 10, "bold"),
                  width=12, cursor="hand2", relief="flat").pack(side="left", padx=4)
        tk.Button(btn_frame, text="Atualizar", command=self.update_pedido,
                  bg="#2e75b6", fg="white", font=("Arial", 10, "bold"),
                  width=12, cursor="hand2", relief="flat").pack(side="left", padx=4)
        tk.Button(btn_frame, text="Excluir", command=self.delete_pedido,
                  bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
                  width=12, cursor="hand2", relief="flat").pack(side="left", padx=4)
        tk.Button(btn_frame, text="Limpar", command=self.clear_form,
                  bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                  width=12, cursor="hand2", relief="flat").pack(side="left", padx=4)

        self.lbl_total = tk.Label(form_frame, text="Total: R$ 0,00",
                                  bg="#f0f4f8", fg="#1a56a0", font=("Arial", 11, "bold"))
        self.lbl_total.grid(row=6, column=0, columnspan=2, pady=6)

        table_frame = tk.LabelFrame(body, text=" Pedidos ", bg="#f0f4f8",
                                    fg="#1a56a0", font=("Arial", 11, "bold"), bd=2)
        table_frame
