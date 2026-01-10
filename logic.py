def calcular_estatisticas(attrs):
    vig = attrs["VIG"]
    det = attrs["DET"]
    agi = attrs["AGI"]
    exp = attrs["EXP"]
    return {
        "Saúde": 10 + vig * 6,
        "Disposição": 5 + det * 3,
        "Iniciativa": 5 + (agi - 1) + agi * 2,
        "Presença": 5 + (exp - 1) + exp * 2
    }

def limite_habilidades(cog):
    return 1 + cog

def capacidade_inventario(forca):
    if forca == 0:
        return 2
    return 5 * forca
