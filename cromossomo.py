from random import sample

cromossomo =[
    1,0,4,3,2, #nacionalidade
    0,1,2,3,4, #cores
    2,0,3,1,4, #bebidas
    1,0,3,4,2, #cigarro+
    2,3,1,0,4 #animais
]

#dicionario fenotipo
nacionalidades=["Norueguês", "Inglês", "Sueco", "Dinamarquês", "Alemão"]
cores = ["Vermelha", "Verde", "Branca", "Amarela", "Azul"]
bebidas = ["Chá", "Café", "Leite", "Cerveja", "Água"]
cigarros = ["Pall Mall", "Dunhill", "Blends", "BlueMaster", "Prince"]
animais = ["Cachorros", "Pássaros", "Gatos", "Cavalos", "Peixe"]


def gerar_individuo():
   
    return (
        sample(range(5), 5) +   # nacionalidade
        sample(range(5), 5) +   # cor
        sample(range(5), 5) +   # bebida
        sample(range(5), 5) +   # cigarro
        sample(range(5), 5)     # animal
    )

def corrigir_cromossomo(cromo):
    novo = []
    for i in range(0, 25, 5):
        grupo = cromo[i:i+5]
        faltando = list(set(range(5)) - set(grupo))
        vistos = set()
        corrigido = []
        for g in grupo:
            if g not in vistos:
                corrigido.append(g)
                vistos.add(g)
            else:
                corrigido.append(faltando.pop())
        novo.extend(corrigido)
    return novo

def mostrar_fenotipo(cromossomo):
    nat = cromossomo[0:5]
    cor = cromossomo[5:10]
    beb = cromossomo[10:15]
    cig = cromossomo[15:20]
    ani = cromossomo[20:25]

    print("\n---- Fenótipo do Cromossomo ----")
    for i in range(5):
        print(f"Casa {i+1}: {cores[cor[i]]}, {nacionalidades[nat[i]]}, {bebidas[beb[i]]}, {cigarros[cig[i]]}, {animais[ani[i]]}")

def mostrar_genotipo(cromo):
    print("\n---- Genótipo ----")
    nomes = ["Nacionalidade", "Cor", "Bebida", "Cigarro", "Animal"]
    for i in range(0, 25, 5):
        grupo = cromo[i:i+5]
        print(f"{nomes[i//5]}: {grupo}")
        