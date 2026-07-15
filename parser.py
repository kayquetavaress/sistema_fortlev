import re

# =========================
# ✅ BASE DE MATERIAIS
# =========================

MATERIAIS = {

    # ==================================
    # COMPOSTOS PVC
    # ==================================

    "4000000416": {
        "descricao": "COMPOSTO PÓ PVC BRANCO TUBO ESGOTO",
        "tipo": "COMPOSTO",
        "familia": "PVC",
        "formulacoes": [
            "E04B104",
            "E04B111",
            "E04B113"
        ]
    },

    "4000000417": {
        "descricao": "COMPOSTO PÓ PVC MARROM TUBO SOLDÁVEL",
        "tipo": "COMPOSTO",
        "familia": "PVC",
        "formulacoes": [
            "E02M051",
            "E02M029"
        ]
    },

    # ==================================
    # REFUGOS
    # ==================================

    "4000000507": {
        "descricao": "REFUGO DE POLIETILENO",
        "tipo": "REFUGO",
        "familia": "POLIETILENO",
        "formulacoes": []
    }

}

# =========================
# ✅ BUSCAR MATERIAL PELO CÓDIGO
# =========================

def buscar_material(codigo):

    if codigo in MATERIAIS:
        return MATERIAIS[codigo]["descricao"]

    return "MATERIAL NÃO CADASTRADO"

def buscar_tipo(codigo):

    if codigo in MATERIAIS:
        return MATERIAIS[codigo]["tipo"]

    return ""


def buscar_familia(codigo):

    if codigo in MATERIAIS:
        return MATERIAIS[codigo]["familia"]

    return 
# =========================
# ✅ VALIDAR FORMULAÇÃO
# =========================

def validar_formulacao(codigo, formulacao):

    if codigo not in MATERIAIS:
        return False

    return formulacao in MATERIAIS[codigo]["formulacoes"]


# =========================
# ✅ EXTRAÇÃO DE DADOS
# =========================

def extrair_dados(texto):

    texto = texto.upper()

    linhas = [l.strip() for l in texto.split("\n") if l.strip()]

    # =========================
    # ✅ CÓDIGO
    # =========================

    codigo = None

    for linha in linhas:

        match = re.search(r'\b\d{8,}\b', linha)

        if match:
            codigo = match.group()
            break

    # =========================
    # ✅ MATERIAL PELO CÓDIGO
    # =========================

    material = buscar_material(codigo)

    # =========================
    # ✅ FORMULAÇÃO
    # =========================

    formulacao = None

    texto_sem_espaco = texto.replace(" ", "").replace("\n", "")

    match = re.search(r'E\d{2}[A-Z0-9]\d{3}', texto_sem_espaco)

    if match:

        formulacao = match.group()

        # Correção OCR
        formulacao = formulacao.replace("8", "B", 1)

    # =========================
    # ✅ VALIDAÇÃO
    # =========================

    formulacao_valida = validar_formulacao(
        codigo,
        formulacao
    )

    # =========================
    # ✅ PESO
    # =========================

    peso = None

    for linha in linhas:

        if "PESO" in linha:

            match = re.search(
                r'(\d{3,4})\d{2}',
                linha
            )

            if match:

                peso = float(
                    f"{match.group(1)}.{match.group(2)}"
                )

                break

    # fallback
    if peso is None:

        numeros = re.findall(r'\d+', texto)

        for i in range(len(numeros)-1):

            inteiro = numeros[i]
            decimal = numeros[i+1]

            if len(inteiro) >= 3 and len(decimal) == 2:

                valor = float(
                    f"{inteiro}.{decimal}"
                )

                if 800 <= valor <= 2000:
                    peso = valor
                    break

    # =========================
    # ✅ RETORNO
    # =========================

    return {
    "codigo": codigo,
    "material": material,
    "tipo": buscar_tipo(codigo),
    "familia": buscar_familia(codigo),
    "formulacao": formulacao,
    "formulacao_valida": formulacao_valida,
    "peso": peso
}