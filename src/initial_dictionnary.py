def create_initial_dictionary(objective_coeffs, constraints_matrix, constraints_rhs, basic_vars, nonbasic_vars):
    """
    Crée le dictionnaire initial du simplexe.

    Args:
        objective_coeffs (list): Coefficients de la fonction objective.
        constraints_matrix (list of lists): Matrice des coefficients des contraintes.
        constraints_rhs (list): Valeurs du côté droit des contraintes.
        basic_vars (list): Liste des variables de base initiales.
        nonbasic_vars (list): Liste des variables non basiques initiales.

    Returns:
        dict: Le dictionnaire initial du simplexe.
    """

    num_constraints = len(constraints_rhs)
    num_original_vars = len(objective_coeffs)

    # Créer le dictionnaire
    dictionary = {
        'basic_vars': basic_vars,
        'nonbasic_vars': nonbasic_vars,
        'equations': {},
        'objective': {}
    }

    # Remplir les équations
    for i in range(num_constraints):
        equation = f"{constraints_rhs[i]} "
        for j in range(num_original_vars):
            equation += f"- {constraints_matrix[i][j]}*x{j+1} "
        dictionary['equations'][basic_vars[i]] = equation.strip()

    # Remplir la fonction objective
    objective = "0 "
    for i in range(num_original_vars):
        objective += f"+ {objective_coeffs[i]}*x{i+1} "
    dictionary['objective'] = objective.strip()
    
    return dictionary

# Exemple d'utilisation
objective_coeffs = [2, 3]
constraints_matrix = [[1, 1], [2, 1]]
constraints_rhs = [4, 6]

initial_dictionary = create_initial_dictionary(objective_coeffs, constraints_matrix, constraints_rhs, ['s1', 's2'], ['x1', 'x2'])

# Affichage du dictionnaire initial
print("Dictionnaire initial :")
for key, value in initial_dictionary.items():
    print(f"{key}: {value}")
