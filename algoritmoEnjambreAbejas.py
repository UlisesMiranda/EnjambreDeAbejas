import math
import random

# Definimos la función de aptitud (objetivo a minimizar)
def evaluate(solution):
    x, y = solution
    return x**2 + y**2

# Definimos la función que produce nuevas soluciones para las abejas obreras
def produce_worker_solutions(solutions, solution_limites):
  # Produce nuevas soluciones para las abejas obreras
  worker_solutions = []
  worker_limites = []
  
  for i, solution in enumerate(solutions):
    x, y = solution
    limite = solution_limites[i]
    bandera = True
    if limite <= 10:
        r1 = random.uniform(-1, 1)
        # Seleccionamos una solución al azar
        xk, yk = random.choice(solutions)
        
        eleccion = random.randint(0,1)
        if eleccion == 0:
            xj = x + r1*(xk - x)
            if evaluate((xj, solution[1])) < evaluate(solution):
                worker_solutions.append((xj, solution[1]))
                nuevo_limite = 0
                worker_limites.append(nuevo_limite)
                bandera = False
        else:
            yj = y + r1*(yk - y)
            if evaluate((solution[0], yj)) < evaluate(solution):
                worker_solutions.append((solution[0], yj))
                nuevo_limite = 0
                worker_limites.append(nuevo_limite)
                bandera = False
        limite += 1
        solution_limites[i] = limite
    
  return worker_solutions, worker_limites, solution_limites

# Definimos la función que selecciona las mejores soluciones
def select_best_solutions(solutions, solutions_limites):
    evaluations = [evaluate(bee) for bee in solutions]
    
    solutionsAgrup = list(zip(solutions, solutions_limites, evaluations))
    
    # Ordenamos las soluciones por su aptitud y seleccionamos las mejores
    solutionsAgrup.sort(key=lambda x: x[2])
    
    return solutionsAgrup[:10]

# Definimos la función que calcula los valores de probabilidad para cada solución
def calculate_probabilities(solutions):
    # Calculamos los valores de fit de acuerdo a la regla de minimización
    fit_list = []
    for s in solutions:
        f = evaluate(s)
        newFit = 0
        if f >= 0:
            newFit = 1 / (1 + f)
        else:
            newFit = 1 + abs(f)
        fit_list.append(newFit)
            
    # Calculamos el valor de sigma como la suma de todos los valores de fit
    sigma = sum(fit for fit in fit_list)

    probabilities = []
    for fit in fit_list:
        # Calculamos la probabilidad de cada solución utilizando la fórmula p1 = fiti/sigma
        probability = fit / sigma
        probabilities.append(probability)
    return probabilities

# Definimos la función que produce nuevas soluciones para las abejas observadoras
def produce_observer_solutions(solutions, solutions_limites, probabilities):
    # Produce nuevas soluciones para las abejas observadoras
    observer_solutions = []
    observer_limites = []
    solutions_agrupado = list(zip(solutions, solutions_limites, probabilities))
    
    for _ in range(20):
        solution_elegida = random.choices(solutions_agrupado, probabilities)[0]
        sol = solution_elegida[0]
        x, y = solution_elegida[0]
        limite = solution_elegida[1]
        indiceAbeja = solutions_agrupado.index(solution_elegida)
        bandera = True
        
        if random.uniform(0, 1) < solution_elegida[2]:
            if limite <= 10:
                r2 = random.uniform(-1, 1)
                # Seleccionamos una solución utilizando el método de la ruleta
                xk, yk = random.choices(solutions, probabilities)[0]
                
                eleccion = random.randint(0,1)
                if eleccion == 0:
                    xj = x + r2*(x - xk)
                    if evaluate((xj, sol[1])) < evaluate(sol):
                        observer_solutions.append((xj, sol[1]))
                        nuevo_limite = 0
                        observer_limites.append(nuevo_limite)
                        bandera = False
                else:
                    yj = y + r2*(y - yk)    
                    if evaluate((sol[0], yj)) < evaluate(sol):
                        observer_solutions.append((sol[0], yj))
                        nuevo_limite = 0
                        observer_limites.append(nuevo_limite)
                        bandera = False
                limite += 1
                
                solution, limiteSolucion, probability = solutions_agrupado[indiceAbeja]
                solutions_agrupado[indiceAbeja] = solution, limite, probability
        else:
            continue
            
    solutions, solutions_limites, prob = list(zip(*solutions_agrupado))
    return observer_solutions, observer_limites, solutions_limites


# Definimos la función que produce nuevas soluciones aleatorias para las abejas exploradoras
def produce_explorer_solutions():
    # Generamos una nueva solución aleatoria en el intervalo (-5, 5) para x y y
    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)
    return (x, y), 0, 0


def ABC():
    # Inicializamos la población de soluciones
    uj = 5
    lj = -5
    solutions = [(lj + random.uniform(0, 1)*(uj - lj), lj + random.uniform(0, 1)*(uj - lj)) for _ in range(20)]
    solutions_limites = [0 for _ in range(len(solutions))]
    evaluations = [evaluate(bee) for bee in solutions]
    
    solutions_agrup = list(zip(solutions, solutions_limites, evaluations))

    # Inicializamos la mejor solución encontrada hasta el momento
    best_solution = min(solutions_agrup, key=lambda x: x[2])

    # Inicializamos el contador de ciclos a 1
    cycle = 1

    # Repetimos los siguientes pasos hasta que el contador de ciclos sea igual a 50
    while cycle <= 50:
        # Guardamos las mejores soluciones por iteracion
        file.write(f"\n{cycle}. Soluciones: \n{solutions}")

        # Produce nuevas soluciones para las abejas obreras
        worker_solutions, worker_limites, solutions_limites = produce_worker_solutions(solutions, solutions_limites)

        # Seleccionamos las mejores soluciones
        solutions, solutions_limites, evaluations = list(zip(*select_best_solutions(worker_solutions + solutions, worker_limites + solutions_limites)))
        
        # Calculamos los valores de probabilidad para cada solución
        probabilities = calculate_probabilities(solutions)

        # Produce nuevas soluciones para las abejas observadoras
        observer_solutions, observer_limites, solutions_limites = produce_observer_solutions(
            solutions, solutions_limites, probabilities)
        
        solutions = list(solutions)
        solutions_limites = list(solutions_limites)
        
        # Seleccionamos las mejores soluciones
        solutions_agrup = select_best_solutions(observer_solutions + solutions,  observer_limites + solutions_limites)
        
        
        solutions, solutions_limites, evaluations = list(zip(*solutions_agrup))
        solutions = list(solutions)
        solutions_limites = list(solutions_limites)

        # Actualizamos la mejor solución encontrada hasta el momento
        solutions_agrup = list(solutions_agrup)
        solutions_agrup.append(best_solution)
        best_solution = min(solutions_agrup, key=lambda x: x[2])

        # Contamos cuántas soluciones han sido abandonadas por las abejas exploradoras
        abandoned_count = 20 - len(solutions_agrup)

        # Reemplazamos las soluciones abandonadas con nuevas soluciones aleatorias
        solutions_agrup += [produce_explorer_solutions() for _ in range(abandoned_count)]
        
        solutions, solutions_limites, evaluations = zip(*solutions_agrup)
        solutions = list(solutions)
        solutions_limites = list(solutions_limites)

        # Incrementamos el contador de ciclos
        cycle += 1

    # Devolvemos la mejor solución encontrada
    return best_solution


# Creamos nuestro archivo de resultados
file = open("resultados.txt", 'w')

# Ejecutamos el algoritmo y mostramos la mejor solución encontrada
best_solution = ABC()
file.write(f"\nLa mejor solución es: {best_solution}")

file.close()
