import pulp

# Crear el problema de programación lineal
prob = pulp.LpProblem("LP_Problema_Optimizacion", pulp.LpMaximize)

# Definir las variables de decisión
x1 = pulp.LpVariable('x1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('x2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('x3', lowBound=0, cat='Continuous')

# Definir la función objetivo
prob += 4.1 * x1 + 1.57 * x2 + 0.67 * x3, "Función Objetivo"

# Definir las restricciones
prob += 10 * x1 + 5 * x2 + 10 * x3 <= 100, "Coco Rallado"
prob += 5 * x1 <= 100, "Chocolate"
prob += 5 * x2 + 10 * x3 <= 70, "Chocolate Blanco"
prob += 20 * x2 <= 53, "Fresa"
prob += x1 + x2 + x3 <= 30, "Unidades de Chocolates"
prob += 5 * x1 + 5 * x2 + 5 * x3 <= 240, "Tiempo de Refrigeración"

# Resolver el problema de programación lineal
status = prob.solve()

# Imprimir la solución
print(f"Valor de la función objetivo: {pulp.value(prob.objective)}")
print("Solución óptima:")
for var in [x1, x2, x3]:
    print(f"{var.name} = {var.varValue}")