from flask import Flask, render_template, request
import pulp

import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tipo_objetivo = request.form['tipo_objetivo']
        num_variables = int(request.form['num_variables'])
        num_restricciones = int(request.form['num_restricciones'])
        return render_template('matrix.html', tipo_objetivo=tipo_objetivo, 
                               num_variables=num_variables, 
                               num_restricciones=num_restricciones)
    # En caso de que no haya un POST, no se pasará num_variables a index.html
    return render_template('index.html')  # Sin num_variables en GET

@app.route('/resolver', methods=['POST'])
def resolver():
    tipo_objetivo = request.form['tipo_objetivo']
    num_variables = int(request.form['num_variables'])  # Aquí se define
    coef_objetivo = list(map(float, request.form.getlist('coef_objetivo')))
    num_restricciones = int(request.form['num_restricciones'])

    variables = [pulp.LpVariable(f"x{i + 1}", lowBound=0, cat="Continuous") for i in range(num_variables)]
    prob = pulp.LpProblem("LP_Problem", pulp.LpMaximize if tipo_objetivo == 'Max' else pulp.LpMinimize)
    prob += pulp.lpSum(coef * var for coef, var in zip(coef_objetivo, variables))

    for i in range(num_restricciones):
        restriccion_coef = list(map(float, request.form.getlist(f'restriccion_coef_{i}')))
        valor_restriccion = float(request.form[f'valor_restriccion_{i}'])
        tipo_restriccion = request.form[f'tipo_restriccion_{i}']

        if tipo_restriccion == "<=":
            prob += pulp.lpSum(coef * var for coef, var in zip(restriccion_coef, variables)) <= valor_restriccion
        elif tipo_restriccion == ">=":
            prob += pulp.lpSum(coef * var for coef, var in zip(restriccion_coef, variables)) >= valor_restriccion
        elif tipo_restriccion == "=":
            prob += pulp.lpSum(coef * var for coef, var in zip(restriccion_coef, variables)) == valor_restriccion

    status = prob.solve()
    resultados = {
        "estado": pulp.LpStatus[status],
        "valor_optimo": pulp.value(prob.objective),
        "solucion_optima": {f"x{i + 1}": variables[i].varValue for i in range(num_variables)}
    }

    # Graficar la solución
    if num_variables == 2:  # Solo graficar si hay 2 variables
        x = np.linspace(0, 10, 200)  # Ajusta el rango según tus necesidades

        # Graficar restricciones
        for i in range(num_restricciones):
            restriccion_coef = list(map(float, request.form.getlist(f'restriccion_coef_{i}')))
            valor_restriccion = float(request.form[f'valor_restriccion_{i}'])
            y = (valor_restriccion - restriccion_coef[0] * x) / restriccion_coef[1]
            plt.plot(x, y, label=f'Restricción {i + 1}')

        # Graficar la función objetivo
        y_obj = (resultados["valor_optimo"] - coef_objetivo[0] * x) / coef_objetivo[1]
        plt.plot(x, y_obj, 'r--', label='Función Objetivo')

        # Graficar el punto óptimo
        x_optimo = resultados["solucion_optima"]["x1"]  # Valor óptimo de x1
        y_optimo = resultados["solucion_optima"]["x2"]  # Valor óptimo de x2
        plt.plot(x_optimo, y_optimo, 'go', label='Óptimo')  # Punto óptimo en verde

        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.title('Solución de Programación Lineal')
        plt.axhline(0, color='black', lw=0.5)
        plt.axvline(0, color='black', lw=0.5)
        plt.grid()
        plt.legend()
        
        # Guardar la gráfica
        plt.savefig('static/solution_plot.png')  # Asegúrate de tener una carpeta 'static'
        plt.close()  # Cerrar la figura para liberar memoria

    # Asegúrate de pasar num_variables a la plantilla
    return render_template('resultados.html', resultados=resultados, num_variables=num_variables)

if __name__ == '__main__':
    app.run(debug=True)