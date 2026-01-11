import tkinter as tk
from tkinter import ttk
from logic import calcular_estatisticas, limite_habilidades, capacidade_inventario
from pdf_generator import gerar_pdf
from tkinter import messagebox
from tkinter import filedialog

def iniciar():
    app = tk.Tk()
    app.title("Gerador de Ficha RPG")
    app.geometry("750x500")

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

    menu = tk.Frame(app, width=100)
    menu.place(x=0, y=0, relheight=1)
    conteudo = tk.Frame(app)
    conteudo.place(x=120, y=0, relwidth=1, relheight=1)

    frame_caracteristicas = tk.Frame(conteudo)
    frame_saberes = tk.Frame(conteudo)

    def mostrar_caracteristicas():
        frame_saberes.pack_forget()
        frame_caracteristicas.pack(fill="both", expand=False)

    def mostrar_saberes():
        frame_caracteristicas.pack_forget()
        frame_saberes.pack(fill="both", expand=False)

    tk.Button(menu, text="Características", command=mostrar_caracteristicas).pack(fill="x")
    tk.Button(menu, text="Saberes & Posses", command=mostrar_saberes).pack(fill="x")
    gerar_btn = tk.Button(menu, text="Gerar PDF", command=lambda: gerar_final())
    gerar_btn.pack(fill="x")
    gerar_btn.place(x=0, y=455, width=100)

    info = tk.LabelFrame(frame_caracteristicas, text="Informações")
    info.grid(row=0, column=0, columnspan=2, sticky="nw", padx=0, pady=10)

    nome_label = tk.Label(info, text="Nome:")
    nome_entry = tk.Entry(info, textvariable=estado["nome"], width=41)
    arqu_label = tk.Label(info, text="Arquétipo:")
    arqu_entry = tk.Entry(info, textvariable=estado["arquetipo"], width=41)

    nome_label.grid(row=0, column=0, sticky="w", padx=5, pady=4)
    nome_entry.grid(row=0, column=1, sticky="w", padx=5, pady=4)
    arqu_label.grid(row=1, column=0, sticky="w", padx=5, pady=4)
    arqu_entry.grid(row=1, column=1, sticky="w", padx=5, pady=4)

    atributos = tk.LabelFrame(frame_caracteristicas, text="Atributos")
    atributos.grid(row=1, column=0, sticky="w", padx=0, pady=10)

    pontos_rest = tk.Label(atributos, text="Pontos Restantes: 12")
    pontos_rest.grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=6)

    linha = 1
    for a in ["FOR","VIG","AGI","COG","EXP","DET"]:
        tk.Label(atributos, text=a, width=5, anchor="w").grid(row=linha, column=0, sticky="w", padx=5, pady=2)
        tk.Spinbox(atributos, from_=0, to=5, width=7, textvariable=estado[a]).grid(row=linha, column=1, sticky="w", padx=5, pady=2)
        tk.Label(atributos, text="", width=0, anchor="w").grid(row=linha, column=2, sticky="w", padx=1, pady=0)
        linha += 1

    stats_frame = tk.LabelFrame(frame_caracteristicas, text="Estatísticas")
    stats_frame.grid(row=1, column=1, sticky="nw", padx=22, pady=10)

    lbl_saude = tk.Label(stats_frame, text="Pontos de Vida:")
    lbl_saude_val = tk.Label(stats_frame, text="10")
    lbl_dispo = tk.Label(stats_frame, text="Pontos de Disposição:")
    lbl_dispo_val = tk.Label(stats_frame, text="5")
    lbl_init = tk.Label(stats_frame, text="Valor de Iniciativa:")
    lbl_init_val = tk.Label(stats_frame, text="1")
    lbl_pres = tk.Label(stats_frame, text="Valor de Presença: ")
    lbl_pres_val = tk.Label(stats_frame, text="1")

    lbl_saude.grid(row=0, column=0, sticky="w", padx=5, pady=(6,0))
    lbl_saude_val.grid(row=0, column=1, columnspan=2, sticky="n", padx=5, pady=(6,0))
    lbl_dispo.grid(row=1, column=0, sticky="w", padx=5, pady=2)
    lbl_dispo_val.grid(row=1, column=1, columnspan=2, sticky="n", padx=5, pady=2)
    lbl_init.grid(row=2, column=0, sticky="w", padx=5, pady=2)
    lbl_init_val.grid(row=2, column=1, columnspan=2, sticky="n", padx=5, pady=2)
    lbl_pres.grid(row=3, column=0, sticky="w", padx=5, pady=2)
    lbl_pres_val.grid(row=3, column=1, columnspan=2, sticky="n", padx=5, pady=2)
    tk.Label(stats_frame, text="", width=1, anchor="w").grid(row=0, column=3, sticky="w", padx=0, pady=0)

    def atualizar():
        soma = sum(estado[x].get() for x in ["FOR","VIG","AGI","COG","EXP","DET"])
        if soma > 12:
            maior = max(["FOR","VIG","AGI","COG","EXP","DET"], key=lambda x: estado[x].get())
            estado[maior].set(estado[maior].get() - (soma - 12))
            soma = sum(estado[x].get() for x in ["FOR","VIG","AGI","COG","EXP","DET"])
        restante = 12 - soma
        if restante < 10:
            pontos_rest.config(text="Pontos Restantes: " + str(restante) + "  ")
        else:
            pontos_rest.config(text="Pontos Restantes: " + str(restante))
        s = calcular_estatisticas({"VIG":estado["VIG"].get(),"DET":estado["DET"].get(),"AGI":estado["AGI"].get(),"EXP":estado["EXP"].get()})
        lbl_saude.config(text="Pontos de Vida:")
        lbl_saude_val.config(text=str(s["PV"]))
        lbl_dispo.config(text="Pontos de Disposição:")
        lbl_dispo_val.config(text=str(s["PD"]))
        lbl_init.config(text="Valor de Iniciativa:")
        lbl_init_val.config(text=str(s["INI"]))
        lbl_pres.config(text="Valor de Presença:")
        lbl_pres_val.config(text=str(s["PRE"]))
        refresh_saberes()

    for k in ["FOR","VIG","AGI","COG","EXP","DET"]:
        estado[k].trace("w", lambda *args: atualizar())

    def carga_total():
        return sum(x["carga"] for x in estado["inventario"])
    
    def hab_conhecidas():
        return len(estado["habilidades"])

    def refresh_saberes(event=None):
        hab_lista.delete(0, tk.END)
        for h in estado["habilidades"]:
            hab_lista.insert(tk.END, h["nome"])
        inv_lista.delete(0, tk.END)
        for i in estado["inventario"]:
            inv_lista.insert(tk.END, i["nome"])
        inv_info.config(text=str(carga_total())+" / "+str(capacidade_inventario(estado["FOR"].get())))
        hab_limite.config(text=str(hab_conhecidas()) + " / " + str(limite_habilidades(estado["COG"].get())))

    def add_habilidade():
        lim_hab = limite_habilidades(estado["COG"].get())
        if hab_conhecidas() >= lim_hab:
            return
        if not hab_nome.get():
            return
        estado["habilidades"].append({
            "nome": hab_nome.get(),
            "descricao": hab_desc.get("1.0", "end").strip(),
            "custo": hab_custo.get()
        })
        estado["habilidades"].sort(key=lambda x: x["nome"])
        hab_nome.set("")
        hab_desc.delete("1.0", "end")
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
    
    def add_item():
        cap_total = capacidade_inventario(estado["FOR"].get())
        novo = inv_carga.get()
        if carga_total() + novo > cap_total:
            return
        if not inv_nome.get():
            return
        estado["inventario"].append({
            "nome": inv_nome.get(),
            "descricao": inv_desc.get("1.0", "end").strip(),
            "carga": novo
        })
        estado["inventario"].sort(key=lambda x: x["nome"])
        inv_nome.set("")
        inv_desc.delete("1.0", "end")
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

    hab_sec = tk.LabelFrame(frame_saberes, text="Habilidades")
    hab_sec.grid(row=0, column=0, sticky="nw", padx=0, pady=10)

    hab_limite = tk.Label(hab_sec, text="0 / 0")
    hab_limite.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    hab_lista = tk.Listbox(hab_sec, height=8, width=40)
    hab_lista.grid(row=1, column=0, sticky="w", padx=5, pady=5)

    tk.Button(hab_sec, text="Excluir", command=del_habilidade).grid(row=2, column=0, sticky="w", padx=5, pady=5)

    hab_form = tk.LabelFrame(frame_saberes, text="Nova habilidade")
    hab_form.grid(row=0, column=1, sticky="nw", padx=10, pady=10)

    hab_nome = tk.StringVar()
    hab_custo = tk.IntVar(value=0)

    tk.Label(hab_form, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(hab_form, textvariable=hab_nome, width=40).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    tk.Label(hab_form, text="Descrição:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    hab_desc = tk.Text(hab_form, width=30, height=6)
    hab_desc.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    tk.Label(hab_form, text="Custo:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    tk.Spinbox(hab_form, from_=0, to=99, textvariable=hab_custo, width=5).grid(row=2, column=1, sticky="w", padx=5, pady=5)
    tk.Button(hab_form, text="Adicionar", command=add_habilidade).grid(row=3, column=0, sticky="w", padx=5, pady=5)
    


    inv_sec = tk.LabelFrame(frame_saberes, text="Inventário")
    inv_sec.grid(row=1, column=0, sticky="nw", padx=0, pady=5)

    inv_info = tk.Label(inv_sec, text="0 / 0")
    inv_info.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    inv_lista = tk.Listbox(inv_sec, height=8, width=40)
    inv_lista.grid(row=1, column=0, sticky="w", padx=5, pady=5)


    tk.Button(inv_sec, text="Excluir", command=del_item).grid(row=2, column=0, sticky="w", padx=5, pady=5)

    inv_form = tk.LabelFrame(frame_saberes, text="Novo item")
    inv_form.grid(row=1, column=1, sticky="nw", padx=10, pady=5)

    inv_nome = tk.StringVar()
    inv_carga = tk.IntVar(value=1)

    tk.Label(inv_form, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(inv_form, textvariable=inv_nome, width=40).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    tk.Label(inv_form, text="Descrição:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    inv_desc = tk.Text(inv_form, width=30, height=6)
    inv_desc.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    tk.Label(inv_form, text="Carga:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    tk.Spinbox(inv_form, from_=1, to=99, textvariable=inv_carga, width=5).grid(row=2, column=1, sticky="w", padx=5, pady=5)
    tk.Button(inv_form, text="Adicionar", command=add_item).grid(row=3, column=0, sticky="w", padx=5, pady=5)

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
