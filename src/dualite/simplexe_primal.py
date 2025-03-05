from typing import Final, NewType, Sequence, TypeAlias, TypeVar, MutableSequence


T = TypeVar('T')
Matrix: TypeAlias = Sequence[Sequence[T]]
MutableMatrix: TypeAlias = MutableSequence[MutableSequence[T]]
ConstraintsMatrix = NewType('ConstraintsMatrix', Matrix[float])
ConstantConstraintVector = NewType('ConstantConstraintVector', Sequence[float])
ObjectiveFunctionVector = NewType('ObjectiveFunctionVector', Sequence[float])

def create_empty_matrix(lines: int, columns: int) -> MutableMatrix[float]:
    return [[0.0] * columns for _ in range(lines)]


def create_initial_matrix(A: ConstraintsMatrix, b: ConstantConstraintVector, c: ObjectiveFunctionVector) -> Matrix[float]:
    constraints_count = len(A)
    variables_count = len(A[0]) if constraints_count > 0 else 0

    tableau = create_empty_matrix(constraints_count + 1, variables_count + constraints_count + 1)
    
    for i in range(constraints_count):
         for j in range(variables_count):
             tableau[i][j] = A[i][j]
         tableau[i][variables_count+i] = 1.0
         tableau[i][-1] = b[i]
         
    for j in range(variables_count):
        tableau[-1][j] = -c[j]

    return tableau


def is_optimal_solution_achieved(matrix: Matrix[float]) -> bool:
    LAST_ROW = matrix[-1]

    return all(map(lambda x: x >= 0, LAST_ROW))


def is_problem_unbounded(matrix: Matrix[float], colonne_pivot: int) -> bool:
    return all(map(lambda i: matrix[i][colonne_pivot] <= 0, range(len(matrix))))


def get_pivot_column(matrix: Matrix[float]) -> int:
    return min(range(len(matrix[0])), key=lambda j: matrix[-1][j])


def get_pivot_line(matrix: Matrix[float], colonne_pivot: int) -> int:
    ratios = []
    for i in range(len(matrix)):
        if matrix[i][colonne_pivot] > 0:
            ratios.append(matrix[i][-1] / matrix[i][colonne_pivot])
        else:
            ratios.append(float('inf'))
    return min(range(len(ratios)), key=lambda i: ratios[i])


def simplexe_primal(A, b, c, tableau=None):
    constraints_count = len(A)
    variables_count = len(A[0]) if constraints_count > 0 else 0


    if tableau is None:
        tableau = create_initial_matrix(A, b, c)
    

    print(tableau)

    while True:
        if is_optimal_solution_achieved(tableau):
            break

        colonne_pivot = get_pivot_column(tableau)

        if is_problem_unbounded(tableau, colonne_pivot):
            return None

        ligne_pivot = get_pivot_line(tableau, colonne_pivot)

        pivot = tableau[ligne_pivot][colonne_pivot]
        for j in range(variables_count + constraints_count + 1):
            tableau[ligne_pivot][j] /= pivot

        for i in range(constraints_count + 1):
            if i != ligne_pivot:
                facteur = tableau[i][colonne_pivot]
                for j in range(variables_count + constraints_count + 1):
                    tableau[i][j] -= facteur * tableau[ligne_pivot][j]

    x = [0.0] * variables_count
    for i in range(variables_count):
        colonne = -1
        for k in range(constraints_count):
            is_identity = True
            for l in range(variables_count):
                if abs(tableau[k][l] - (1.0 if l == i else 0.0)) > 1e-6:
                    is_identity = False
                    break
            if is_identity:
                colonne = k
                break
        if colonne != -1:
            x[i] = tableau[colonne][-1]

    z = -tableau[-1][-1]

    return x, z, tableau


class LinearProgram:
    _constraints_matrix: Final[Matrix[float]]
    _constant_constraint_vector: Final[Sequence[float]]
    _objective_function_vector: Final[Sequence[float]]

    def __init__(self, 
                 constraints_matrix: Matrix[float], 
                 constant_constraint_vector: Sequence[float], 
                 objective_function_vector: Sequence[float]) -> None:
        
        self._constraints_matrix = constraints_matrix
        self._constant_constraint_vector = constant_constraint_vector
        self._objective_function_vector = objective_function_vector

    
    def __str__(self) -> str:
        result = ""

        result += "Programme linéaire :\n"
        result += "Maximiser z = "
        for i in range(len(self._objective_function_vector)):
            result += f"{self._objective_function_vector[i]} * x{i+1}"
            if i < len(self._objective_function_vector) - 1:
                result += " + "
        result += "\n"

        result += "Sous les contraintes :\n"
        for i in range(len(self._constraints_matrix)):
            for j in range(len(self._constraints_matrix[0])):
                result += f"{self._constraints_matrix[i][j]} * x{j+1}"
                if j < len(self._constraints_matrix[0]) - 1:
                    result += " + "
            result += f" <= {self._constant_constraint_vector[i]}\n"

        result += "Avec :\n"
        for i in range(len(self._objective_function_vector)):
            result += f"x{i+1} >= 0\n"
        return result
    








if __name__ == '__main__':
    # Exemple d'utilisation
    A = ConstraintsMatrix([[1, 1], [2, 1]])
    b = ConstantConstraintVector([4, 6])
    c = ObjectiveFunctionVector([3, 2])

    lp = LinearProgram(A, b, c)

    print(lp)

    x, z, tableau = simplexe_primal(A, b, c)

    print("Solution optimale :", x)
    print("Valeur optimale de la fonction objectif :", z)
    print("Tableau final du simplexe :")
    for row in tableau:
        print(row)
