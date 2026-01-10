import tkinter as tk
from tkinter import ttk
from logic import calcular_estatisticas, limite_habilidades, capacidade_inventario
from pdf_generator import gerar_pdf
from tkinter import messagebox
from tkinter import filedialog

def iniciar():
    app = tk.Tk()
    app.title("Gerador de Ficha RPG")
    app.geometry("880x630")

    estado = {
        "nome": tk.StringVar(),
        "arquetipo": tk.StringVar(),
        "FOR": tk.IntVar(value=0),
        "VIG": tk.IntVar(value=0),
        "AGI": tk.IntVar(value=0),
        "COG": tk.IntVar(value=0),
        "EXP": tk.IntVar(value=0),
        "DET": tk.IntVar(value=0),
        "habilidades": [],
        "inventario": []
    }

    menu = tk.Frame(app, width=150)
    menu.place(x=0, y=0, relheight=1)
    conteudo = tk.Frame(app)
    conteudo.place(x=150, y=0, relwidth=1, relheight=1)

    frame_caracteristicas = tk.Frame(conteudo)
    frame_saberes = tk.Frame(conteudo)

    def mostrar_caracteristicas():
        frame_saberes.pack_forget()
        frame_caracteristicas.pack(fill="both", expand=True)

    def mostrar_saberes():
        frame_caracteristicas.pack_forget()
        frame_saberes.pack(fill="both", expand=True)

    tk.Button(menu, text="Características", command=mostrar_caracteristicas).pack(fill="x")
    tk.Button(menu, text="Saberes & Posses", command=mostrar_saberes).pack(fill="x")

    nome_label = tk.Label(frame_caracteristicas, text="Nome")
    nome_entry = tk.Entry(frame_caracteristicas, textvariable=estado["nome"])
    arqu_label = tk.Label(frame_caracteristicas, text="Arquétipo")
    arqu_entry = tk.Entry(frame_caracteristicas, textvariable=estado["arquetipo"])
    nome_label.pack(anchor="w", padx=10, pady=2)
    nome_entry.pack(fill="x", padx=10)
    arqu_label.pack(anchor="w", padx=10, pady=2)
    arqu_entry.pack(fill="x", padx=10)

    atributos = tk.Frame(frame_caracteristicas)
    atributos.pack(fill="x", pady=10)
    linha = 0
    for a in ["FOR","VIG","AGI","COG","EXP","DET"]:
        tk.Label(atributos, text=a, width=15, anchor="w").grid(row=linha, column=0, sticky="w", padx=10, pady=2)
        tk.Spinbox(atributos, from_=0, to=5, width=5, textvariable=estado[a]).grid(row=linha, column=1, sticky="w", pady=2)
        linha += 1


    stats_frame = tk.Frame(frame_caracteristicas)
    stats_frame.pack(pady=10, fill="x")
    lbl_saude = tk.Label(stats_frame, text="Saúde: 0")
    lbl_dispo = tk.Label(stats_frame, text="Disposição: 0")
    lbl_init = tk.Label(stats_frame, text="Iniciativa: 0")
    lbl_pres = tk.Label(stats_frame, text="Presença: 0")
    lbl_saude.pack(anchor="w", padx=10)
    lbl_dispo.pack(anchor="w", padx=10)
    lbl_init.pack(anchor="w", padx=10)
    lbl_pres.pack(anchor="w", padx=10)

    pontos_rest = tk.Label(frame_caracteristicas, text="Pontos restantes: 12")
    pontos_rest.pack(anchor="w", padx=10, pady=4)

    def atualizar():
        soma = sum(estado[x].get() for x in ["FOR","VIG","AGI","COG","EXP","DET"])
        if soma > 12:
            maior = max(["FOR","VIG","AGI","COG","EXP","DET"], key=lambda x: estado[x].get())
            estado[maior].set(estado[maior].get() - (soma - 12))
            soma = sum(estado[x].get() for x in ["FOR","VIG","AGI","COG","EXP","DET"])
        restante = 12 - soma
        pontos_rest.config(text="Pontos restantes: " + str(restante))
        s = calcular_estatisticas({"VIG":estado["VIG"].get(),"DET":estado["DET"].get(),"AGI":estado["AGI"].get(),"EXP":estado["EXP"].get()})
        lbl_saude.config(text="Saúde: " + str(s["Saúde"]))
        lbl_dispo.config(text="Disposição: " + str(s["Disposição"]))
        lbl_init.config(text="Iniciativa: " + str(s["Iniciativa"]))
        lbl_pres.config(text="Presença: " + str(s["Presença"]))
        refresh_saberes()

    for k in ["FOR","VIG","AGI","COG","EXP","DET"]:
        estado[k].trace("w", lambda *args: atualizar())

    hab_sec = tk.LabelFrame(frame_saberes, text="Habilidades")
    hab_sec.pack(fill="both", expand=False, padx=10, pady=10)

    hab_nome = tk.StringVar()
    hab_desc = tk.StringVar()
    hab_custo = tk.IntVar(value=0)

    tk.Label(hab_sec, text="Nome").pack(anchor="w")
    tk.Entry(hab_sec, textvariable=hab_nome).pack(fill="x")
    tk.Label(hab_sec, text="Descrição").pack(anchor="w")
    tk.Entry(hab_sec, textvariable=hab_desc).pack(fill="x")
    tk.Label(hab_sec, text="Custo").pack(anchor="w")
    tk.Spinbox(hab_sec, from_=0, to=99, textvariable=hab_custo, width=5).pack(anchor="w")

    hab_lista = tk.Listbox(hab_sec, height=6)
    hab_lista.pack(fill="x", pady=5)

    def add_habilidade():
        max_hab = limite_habilidades(estado["COG"].get())
        if len(estado["habilidades"]) >= max_hab:
            return
        if not hab_nome.get():
            return
        estado["habilidades"].append({
            "nome": hab_nome.get(),
            "descricao": hab_desc.get(),
            "custo": hab_custo.get()
        })
        estado["habilidades"].sort(key=lambda x: x["nome"])
        hab_nome.set("")
        hab_desc.set("")
        hab_custo.set(0)
        refresh_saberes()

    def del_habilidade():
        sel = hab_lista.curselection()
        if not sel:
            return
        idx = sel[0]
        alvo = hab_lista.get(idx)
        for h in estado["habilidades"]:
            if h["nome"] == alvo:
                estado["habilidades"].remove(h)
                break
        refresh_saberes()

    tk.Button(hab_sec, text="Adicionar", command=add_habilidade).pack(side="left", padx=5)
    tk.Button(hab_sec, text="Excluir", command=del_habilidade).pack(side="left")

    inv_sec = tk.LabelFrame(frame_saberes, text="Inventário")
    inv_sec.pack(fill="both", expand=True, padx=10, pady=10)

    inv_nome = tk.StringVar()
    inv_desc = tk.StringVar()
    inv_carga = tk.IntVar(value=1)

    tk.Label(inv_sec, text="Nome").pack(anchor="w")
    tk.Entry(inv_sec, textvariable=inv_nome).pack(fill="x")
    tk.Label(inv_sec, text="Descrição").pack(anchor="w")
    tk.Entry(inv_sec, textvariable=inv_desc).pack(fill="x")
    tk.Label(inv_sec, text="Carga").pack(anchor="w")
    tk.Spinbox(inv_sec, from_=1, to=99, textvariable=inv_carga, width=5).pack(anchor="w")

    inv_lista = tk.Listbox(inv_sec, height=6)
    inv_lista.pack(fill="x", pady=5)

    inv_info = tk.Label(inv_sec, text="0 / 0")
    inv_info.pack(anchor="w")

    def carga_total():
        return sum(x["carga"] for x in estado["inventario"])

    def add_item():
        cap = capacidade_inventario(estado["FOR"].get())
        novo = inv_carga.get()
        if carga_total() + novo > cap:
            return
        if not inv_nome.get():
            return
        estado["inventario"].append({
            "nome": inv_nome.get(),
            "descricao": inv_desc.get(),
            "carga": novo
        })
        estado["inventario"].sort(key=lambda x: x["nome"])
        inv_nome.set("")
        inv_desc.set("")
        inv_carga.set(1)
        refresh_saberes()

    def del_item():
        sel = inv_lista.curselection()
        if not sel:
            return
        idx = sel[0]
        alvo = inv_lista.get(idx)
        for i in estado["inventario"]:
            if i["nome"] == alvo:
                estado["inventario"].remove(i)
                break
        refresh_saberes()

    tk.Button(inv_sec, text="Adicionar", command=add_item).pack(side="left", padx=5)
    tk.Button(inv_sec, text="Excluir", command=del_item).pack(side="left", padx=5)

    def refresh_saberes(event=None):
        hab_lista.delete(0, tk.END)
        for h in estado["habilidades"]:
            hab_lista.insert(tk.END, h["nome"])
        inv_lista.delete(0, tk.END)
        for i in estado["inventario"]:
            inv_lista.insert(tk.END, i["nome"])
        cap = capacidade_inventario(estado["FOR"].get())
        inv_info.config(text=str(carga_total())+" / "+str(cap))

    gerar_btn = tk.Button(app, text="Gerar PDF", command=lambda: gerar_final())
    gerar_btn.place(x=10, y=590, width=120)

    def gerar_final():
        if not estado["nome"].get() or not estado["arquetipo"].get():
            return
        soma = sum(estado[x].get() for x in ["FOR","VIG","AGI","COG","EXP","DET"])
        if soma != 12:
            return
        stats = calcular_estatisticas({"VIG":estado["VIG"].get(),"DET":estado["DET"].get(),"AGI":estado["AGI"].get(),"EXP":estado["EXP"].get()})
        dados = {
            "nome": estado["nome"].get(),
            "arquetipo": estado["arquetipo"].get(),
            "atributos": {x:estado[x].get() for x in ["FOR","VIG","AGI","COG","EXP","DET"]},
            "stats": stats,
            "habilidades": estado["habilidades"],
            "inventario": estado["inventario"]
        }
        destino = filedialog.asksaveasfilename(defaultextension=".pdf")
        if destino:
            gerar_pdf(dados, destino)

    mostrar_caracteristicas()
    app.mainloop()
