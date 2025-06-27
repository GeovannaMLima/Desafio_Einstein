from random import sample,randint,random,choice
from cromossomo import gerar_individuo, corrigir_cromossomo

#Operações, métodos e função fitness

def fitness(cromossomo):
    score = 0

    casas = []
    for i in range(5):
        casas.append({
            'nacionalidade': cromossomo[i],
            'cor': cromossomo[i+5],
            'bebida': cromossomo[i+10],
            'cigarro': cromossomo[i+15],
            'animal': cromossomo[i+20]
        })
    def vizinhos(i):
        return [j for j in [i-1, i+1] if 0 <= j < 5]

    # Regra 1: O Norueguês vive na primeira casa
    if casas[0]['nacionalidade'] == 0:
        score += 1

    # Regra 2: O Inglês vive na casa Vermelha
    for casa in casas:
        if casa['nacionalidade'] == 1 and casa['cor'] == 0:
            score += 1

    # Regra 3: O Sueco tem Cachorros
    for casa in casas:
        if casa['nacionalidade'] == 2 and casa['animal'] == 0:
            score += 1

    # Regra 4: O Dinamarquês bebe Chá
    for casa in casas:
        if casa['nacionalidade'] == 3 and casa['bebida'] == 0:
            score += 1

    # Regra 5: A casa Verde fica à esquerda da Branca
    for i in range(4):  # só até a casa 4
        if casas[i]['cor'] == 1 and casas[i+1]['cor'] == 2:
            score += 2

    # 6. O homem da casa Verde bebe Café.
    for casa in casas:
        if casa['cor'] == 1 and casa['bebida'] == 1:
            score += 1

    # 7. Quem fuma Pall Mall cria Pássaros.
    for casa in casas:
        if casa['cigarro'] == 0 and casa['animal'] == 1:
            score += 1

    # 8. O homem da casa Amarela fuma Dunhill.
    for casa in casas:
        if casa['cor'] == 3 and casa['cigarro'] == 1:
            score += 1

    # 9. O homem da casa do meio bebe Leite.
    if casas[2]['bebida'] == 2:
        score += 1

    # 10. Quem fuma Blends mora ao lado de quem tem Gatos.
    for i in range(5):
        if casas[i]['cigarro'] == 2:
            for j in vizinhos(i):
                if casas[j]['animal'] == 2:
                    score += 3
                    break

    # 11. Quem cria Cavalos mora ao lado de quem fuma Dunhill.
    for i in range(5):
        if casas[i]['animal'] == 3:
            for j in vizinhos(i):
                if casas[j]['cigarro'] == 1:
                    score += 3
                    break

    # 12. Quem fuma BlueMaster bebe Cerveja.
    for casa in casas:
        if casa['cigarro'] == 3 and casa['bebida'] == 3:
            score += 1

    # 13. O Alemão fuma Prince.
    for casa in casas:
        if casa['nacionalidade'] == 4 and casa['cigarro'] == 4:
            score += 1

    # 14. O Norueguês mora ao lado da casa Azul.
    for i in range(5):
        if casas[i]['nacionalidade'] == 0:
            for j in vizinhos(i):
                if casas[j]['cor'] == 4:
                    score += 2
                    break

    # 15. Quem fuma Blends é vizinho do que bebe Água.
    for i in range(5):
        if casas[i]['cigarro'] == 2:
            for j in vizinhos(i):
                if casas[j]['bebida'] == 4:
                    score += 3
                    break

    return score


def crossover_um_ponto(pai1,pai2):
    ponto = randint(1, len(pai1) - 2)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

def mutacao(cromo, taxa=0.1):
    novo = cromo[:]
    for i in range(0, 25, 5):  # grupos de 5: nat, cor, etc.
        if random() < taxa:
            a = choice(range(i, i+5))
            b = choice([x for x in range(i, i+5) if x != a])
            novo[a], novo[b] = novo[b], novo[a]
    return novo


def aplicar_imigracao(populacao, qtd=2):
    for _ in range(qtd):
        idx = randint(0, len(populacao)-1)
        populacao[idx] = gerar_individuo()

def elitismo(populacao, fitnesses, qtd_elite):
    pares = list(zip(populacao, fitnesses))
    pares.sort(key=lambda x: x[1], reverse=True)
    elite = [ind for ind, fit in pares[:qtd_elite]]
    return elite


def roleta(populacao, fitnesses):
    total = sum(fitnesses)
    if total == 0:
        return choice(populacao)  
    probs = [f / total for f in fitnesses]
    
    # Gerar a roleta acumulada
    roleta_acumulada = []
    soma = 0
    for p in probs:
        soma += p
        roleta_acumulada.append(soma)

    # Sort valor
    r = random()
    
    # Encontrar quem corresponde ao valor sorteado
    for i, limite in enumerate(roleta_acumulada):
        if r <= limite:
            return populacao[i]

def nova_geracao(populacao, taxa_crossover, taxa_mutacao, qtd_elite, qtd_imigrantes):
    nova_pop = []
    fitnesses = [fitness(ind) for ind in populacao]
    
    # Elitismo
    elite = elitismo(populacao, fitnesses, qtd_elite)
    nova_pop.extend(elite)

    # Gerar filhos por crossover
    while len(nova_pop) < len(populacao):
        pai1 = roleta(populacao, fitnesses)
        pai2 = roleta(populacao, fitnesses)

       # pai1, pai2 = choice(populacao), choice(populacao)
        if random() < taxa_crossover:
            filho1, filho2 = crossover_um_ponto(pai1, pai2)
        else:
            filho1, filho2 = pai1[:], pai2[:]
        
        # Mutação
        filho1 = mutacao(filho1, taxa_mutacao)
        filho2 = mutacao(filho2, taxa_mutacao)

        filho1 = corrigir_cromossomo(filho1)
        filho2 = corrigir_cromossomo(filho2)

        nova_pop.extend([filho1, filho2])

    # Corte se excedeu o tamanho
    nova_pop = nova_pop[:len(populacao)]

    # Imigração
    aplicar_imigracao(nova_pop, qtd_imigrantes)


    return nova_pop
    