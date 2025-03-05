import numpy as np

def perturbation_method(objective_coeffs, constraints_matrix, constraints_rhs):
    """
    Applique la méthode de perturbation pour éviter les cycles dans l'algorithme du simplexe.

    Args:
        objective_coeffs (list): Coefficients de la fonction objective.
        constraints_matrix (list of lists): Matrice des coefficients des contraintes.
        constraints_rhs (list): Valeurs du côté droit des contraintes.

    Returns:
        tuple: Coefficients de la fonction objective, matrice des contraintes et valeurs du côté droit des contraintes perturbées.
    """

    num_constraints = len(constraints_rhs)
    num_original_vars = len(objective_coeffs)

    # Perturber les valeurs du côté droit des contraintes
    epsilon = np.random.rand(num_constraints)  # Générer des perturbations aléatoires
    constraints_rhs_perturbed = [constraints_rhs[i] + epsilon[i] for i in range(num_constraints)]

    return objective_coeffs, constraints_matrix, constraints_rhs_perturbed

if __name__ == '__main__':
    # Exemple d'utilisation
    objective_coeffs = [2, 3]
    constraints_matrix = [[1, 1], [2, 1]]
    constraints_rhs = [4, 6]

    print("Problème initial :")
    print(f"Coefficients de l'objectif : {objective_coeffs}")
    print(f"Matrice des contraintes : {constraints_matrix}")
    print(f"Côté droit des contraintes : {constraints_rhs}")

    objective_coeffs_perturbed, constraints_matrix_perturbed, constraints_rhs_perturbed = perturbation_method(objective_coeffs, constraints_matrix, constraints_rhs)

    print("\nProblème perturbé :")
    print(f"Coefficients de l'objectif : {objective_coeffs_perturbed}")
    print(f"Matrice des contraintes : {constraints_matrix_perturbed}")
    print(f"Côté droit des contraintes perturbées : {constraints_rhs_perturbed}")
