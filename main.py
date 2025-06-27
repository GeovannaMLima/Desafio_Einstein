from cromossomo import gerar_individuo,mostrar_fenotipo,mostrar_genotipo
from genetico import fitness,nova_geracao



#parametros
pop_size =250 
Pc = 0.85
Pm = 0.15
qtd_elite = int(pop_size * 0.08)
qtd_imigrantes = 3
max_gen = 1000


populacao = [gerar_individuo() for _ in range(pop_size)]

for geracao in range(max_gen):
    populacao = nova_geracao(populacao, Pc, Pm, qtd_elite, qtd_imigrantes)
    fitnesses = [fitness(ind) for ind in populacao]
    melhor_fit = max(fitnesses)
 
    if geracao % 200 == 0 or melhor_fit == 23:
        print(f"Geração {geracao} - Melhor fitness: {melhor_fit}")
    
    if melhor_fit == 23:
        print(f"Solução ótima encontrada na geração {geracao}")
        break
else:
    print("Não foi encontrada solução ótima dentro do limite de gerações.")


melhor = max(populacao, key=fitness)
print(f"\nSolução encontrada com fitness {fitness(melhor)}:")
mostrar_genotipo(melhor)
mostrar_fenotipo(melhor)
