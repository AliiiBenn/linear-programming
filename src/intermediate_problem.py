def create_auxiliary_problem(constraints_matrix, constraints_rhs):
    """
    Crée le problème auxiliaire à partir de la matrice des contraintes et des valeurs du côté droit des contraintes.

    Args:
        constraints_matrix (list of lists): Matrice des coefficients des contraintes.
        constraints_rhs (list): Valeurs du côté droit des contraintes.

    Returns:
        tuple: La matrice des contraintes et les valeurs du côté droit des contraintes pour le problème auxiliaire.
    """

    num_constraints = len(constraints_rhs)
    num_original_vars = len(constraints_matrix[0]) if num_constraints > 0 else 0

    # Créer la matrice des contraintes pour le problème auxiliaire
    auxiliary_constraints_matrix = []
    for i in range(num_constraints):
        row = constraints_matrix[i] + [1]  # Ajouter une variable artificielle à chaque contrainte
        auxiliary_constraints_matrix.append(row)

    # Créer les valeurs du côté droit des contraintes pour le problème auxiliaire
    auxiliary_constraints_rhs = constraints_rhs[:]  # Copier les valeurs du côté droit

    return auxiliary_constraints_matrix, auxiliary_constraints_rhs

def create_auxiliary_objective(num_artificial_vars):
    """
    Crée les coefficients de la fonction objective pour le problème auxiliaire.

    Args:
        num_artificial_vars (int): Le nombre de variables artificielles.

    Returns:
        list: Les coefficients de la fonction objective pour le problème auxiliaire.
    """

    # La fonction objective est de minimiser la somme des variables artificielles
    auxiliary_objective_coeffs = [-1] * num_artificial_vars

    return auxiliary_objective_coeffs

if __name__ == '__main__':
    # Exemple d'utilisation
    constraints_matrix = [[2, 1], [1, 2]]
    constraints_rhs = [4, 5]

    print("Problème initial :")
    print(f"Matrice des contraintes : {constraints_matrix}")
    print(f"Côté droit des contraintes : {constraints_rhs}")

    auxiliary_constraints_matrix, auxiliary_constraints_rhs = create_auxiliary_problem(constraints_matrix, constraints_rhs)
    num_artificial_vars = len(auxiliary_constraints_matrix)
    auxiliary_objective_coeffs = create_auxiliary_objective(num_artificial_vars)

    print("\nProblème auxiliaire :")
    print(f"Matrice des contraintes : {auxiliary_constraints_matrix}")
    print(f"Côté droit des contraintes : {auxiliary_constraints_rhs}")
    print(f"Coefficients de l'objectif : {auxiliary_objective_coeffs}")
