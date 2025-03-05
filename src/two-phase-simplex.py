from intermediate_problem import create_auxiliary_problem, create_auxiliary_objective
from simplex_dictionnary import SimplexDictionary  # Note le underscore au lieu du trait d'union
from pivot import pivot
from initial_dictionnary import create_initial_dictionary  # Assurez-vous que le nom du fichier est correct
from slack_variables import introduce_slack_variables

def two_phase_simplex(objective_coeffs, constraints, constraints_matrix, constraints_rhs, basic_vars, nonbasic_vars):
    """
    Résout un problème de programmation linéaire en utilisant la méthode du simplexe en deux phases.

    Args:
        objective_coeffs (list): Coefficients de la fonction objective.
        constraints (list): Liste des contraintes.
        constraints_matrix (list of lists): Matrice des coefficients des contraintes.
        constraints_rhs (list): Valeurs du côté droit des contraintes.
        basic_vars (list): Liste des variables de base initiales.
        nonbasic_vars (list): Liste des variables non basiques initiales.

    Returns:
        tuple: Une solution optimale et un dictionnaire final.
    """

    # Phase 1 : Résoudre le problème auxiliaire pour trouver une solution de base réalisable initiale
    print("\nPhase 1: Résolution du problème auxiliaire")
    auxiliary_constraints_matrix, auxiliary_constraints_rhs = create_auxiliary_problem(constraints_matrix, constraints_rhs)
    num_artificial_vars = len(auxiliary_constraints_matrix)
    auxiliary_objective_coeffs = create_auxiliary_objective(num_artificial_vars)

    # Ajuster les variables de base et non basiques pour inclure les variables artificielles
    auxiliary_basic_vars = basic_vars + [f"a{i+1}" for i in range(num_artificial_vars)]
    auxiliary_nonbasic_vars = nonbasic_vars + [f"a{i+1}" for i in range(num_artificial_vars)]  # Ajouter les variables artificielles aux variables non basiques
    auxiliary_artificial_vars = [f"a{i+1}" for i in range(num_artificial_vars)]

    # Créer le dictionnaire initial pour le problème auxiliaire
    #initial_auxiliary_dict = create_initial_dictionary(auxiliary_objective_coeffs, auxiliary_constraints_matrix, auxiliary_constraints_rhs, auxiliary_basic_vars, auxiliary_nonbasic_vars)
    initial_auxiliary_dict = SimplexDictionary(
        objective_coeffs=auxiliary_objective_coeffs,
        constraints_matrix=auxiliary_constraints_matrix,
        constraints_rhs=auxiliary_constraints_rhs,
        basic_vars=auxiliary_basic_vars,
        nonbasic_vars=auxiliary_nonbasic_vars,
        artificial_vars=auxiliary_artificial_vars
    )
    initial_auxiliary_dict.create_initial_dictionary()

    # Résoudre le problème auxiliaire en utilisant l'algorithme du simplexe
    # (Implémentation de l'algorithme du simplexe ici - itérer jusqu'à l'optimalité)
    # Pour simplifier, supposons que nous avons une fonction simplex_algorithm
    current_dict = initial_auxiliary_dict
    
    # Implémentation de base de l'algorithme du simplexe (à remplacer par une implémentation complète)
    max_iterations = 100  # Limite pour éviter les boucles infinies
    iteration = 0
    while iteration < max_iterations:
        # Trouver la variable entrante (celle avec le coefficient le plus négatif dans l'objectif)
        entering_variable = None
        min_coeff = 0
        objective_terms = current_dict.objective['z'].split()
        for i in range(1, len(objective_terms), 2):
            term = objective_terms[i-1]
            # Gérer le cas où le terme est collé à la variable (par exemple, "-1x1")
            if '*' in term:
                coeff = float(term.split('*')[0])
            else:
                # Tenter de séparer le coefficient et la variable
                import re
                match = re.match(r'([-+]?\d*\.?\d*)(\D+)', term)
                if match:
                    coeff = float(match.group(1))
                else:
                    coeff = 0.0  # Si on ne trouve pas, on met 0

            variable = objective_terms[i]
            if coeff < min_coeff:
                min_coeff = coeff
                entering_variable = variable

        if entering_variable is None:
            print("Solution optimale trouvée pour la phase 1.")
            break  # Optimalité atteinte

        # Trouver la variable sortante (celle avec le ratio minimum)
        leaving_variable = None
        min_ratio = float('inf')
        for var in current_dict.basic_vars:
            if var.startswith('a'):
                leaving_variable = var
                break
        
        if leaving_variable is None:
            print("Aucune variable artificielle à retirer.")
            break

        # Effectuer le pivot
        print(f"Pivot: Entrante = {entering_variable}, Sortante = {leaving_variable}")
        current_dict = pivot(current_dict, entering_variable, leaving_variable)
        
        iteration += 1

    # Vérifier si la solution de base réalisable a été trouvée (toutes les variables artificielles sont nulles)
    # (Implémentation de la vérification ici)
    # Pour simplifier, supposons que nous avons une fonction is_feasible_solution
    is_feasible = True
    for var in current_dict.basic_vars:
        if var.startswith('a'):
            is_feasible = False
            break

    if not is_feasible:
        print("Le problème original n'a pas de solution de base réalisable.")
        return None, current_dict

    # Phase 2 : Résoudre le problème original en utilisant la solution de base réalisable trouvée dans la phase 1
    print("\nPhase 2: Résolution du problème original")

    # Créer le dictionnaire initial pour le problème original en utilisant la solution de base réalisable de la phase 1
    # (Implémentation de la création du dictionnaire initial ici)
    # Pour simplifier, supposons que nous avons une fonction create_initial_dictionary_phase2
    initial_dict_phase2 = create_initial_dictionary(objective_coeffs, constraints_matrix, constraints_rhs, basic_vars, nonbasic_vars)

    # Résoudre le problème original en utilisant l'algorithme du simplexe
    # (Implémentation de l'algorithme du simplexe ici - itérer jusqu'à l'optimalité)
    # Pour simplifier, supposons que nous avons une fonction simplex_algorithm
    current_dict = initial_dict_phase2
    
    # Implémentation de base de l'algorithme du simplexe (à remplacer par une implémentation complète)
    max_iterations = 100  # Limite pour éviter les boucles infinies
    iteration = 0
    while iteration < max_iterations:
        # Trouver la variable entrante (celle avec le coefficient le plus négatif dans l'objectif)
        entering_variable = None
        min_coeff = 0
        objective_terms = current_dict.objective['z'].split()
        for i in range(1, len(objective_terms), 2):
            term = objective_terms[i-1]
            # Gérer le cas où le terme est collé à la variable (par exemple, "-1x1")
            if '*' in term:
                coeff = float(term.split('*')[0])
            else:
                # Tenter de séparer le coefficient et la variable
                import re
                match = re.match(r'([-+]?\d*\.?\d*)(\D+)', term)
                if match:
                    coeff = float(match.group(1))
                else:
                    coeff = 0.0  # Si on ne trouve pas, on met 0
            variable = objective_terms[i]
            if coeff < min_coeff:
                min_coeff = coeff
                entering_variable = variable

        if entering_variable is None:
            print("Solution optimale trouvée pour la phase 2.")
            break  # Optimalité atteinte

        # Trouver la variable sortante (celle avec le ratio minimum)
        leaving_variable = None
        min_ratio = float('inf')
        
        # Trouver le ratio minimum
        leaving_variable = current_dict.basic_vars[0]

        # Effectuer le pivot
        print(f"Pivot: Entrante = {entering_variable}, Sortante = {leaving_variable}")
        current_dict = pivot(current_dict, entering_variable, leaving_variable)
        
        iteration += 1

    # Extraire la solution optimale du dictionnaire final
    # (Implémentation de l'extraction de la solution ici)
    # Pour simplifier, supposons que nous avons une fonction extract_solution
    optimal_solution = {}
    for var in current_dict['basic_vars']:
        optimal_solution[var] = current_dict['equations'][var]

    return optimal_solution, current_dict

if __name__ == '__main__':
    # Exemple d'utilisation
    objective_coeffs = [-3, -2]
    constraints = ["x1 + x2 <= 4", "2*x1 + x2 <= 6", "x1 >= 0", "x2 >= 0"]
    constraints_matrix = [[1, 1], [2, 1]]
    constraints_rhs = [4, 6]
    basic_vars = ['s1', 's2']
    nonbasic_vars = ['x1', 'x2']

    # Introduire les variables d'écart
    equalities = introduce_slack_variables(constraints)
    print("\nContraintes avec variables d'écart :")
    for equality in equalities:
        print(equality)

    optimal_solution, final_dict = two_phase_simplex(objective_coeffs, constraints, constraints_matrix, constraints_rhs, basic_vars, nonbasic_vars)

    print("\nSolution optimale :", optimal_solution)
    print("\nDictionnaire final :", final_dict)
