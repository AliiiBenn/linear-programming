import numpy as np

def lexicographic_method(objective_coeffs, constraints_matrix, constraints_rhs):
    """
    Applique la méthode lexicographique pour éviter les cycles dans l'algorithme du simplexe.

    Args:
        objective_coeffs (list): Coefficients de la fonction objective.
        constraints_matrix (list of lists): Matrice des coefficients des contraintes.
        constraints_rhs (list): Valeurs du côté droit des contraintes.

    Returns:
        tuple: Coefficients de la fonction objective, matrice des contraintes et matrice lexicographique.
    """

    num_constraints = len(constraints_rhs)
    num_original_vars = len(objective_coeffs)

    # Créer la matrice lexicographique
    lexicographic_matrix = np.zeros((num_constraints, num_constraints + num_original_vars + 1))

    # Remplir la première colonne avec les valeurs du côté droit des contraintes
    lexicographic_matrix[:, 0] = constraints_rhs

    # Remplir les colonnes suivantes avec la matrice des contraintes
    lexicographic_matrix[:, 1:num_original_vars + 1] = constraints_matrix

    # Remplir les colonnes restantes avec une matrice identité
    lexicographic_matrix[:, num_original_vars + 1:] = np.eye(num_constraints)

    return objective_coeffs, constraints_matrix, lexicographic_matrix

def find_leaving_variable_lexicographic(ratios, lexicographic_rows):
    """
    Trouve la variable sortante en utilisant la méthode lexicographique.

    Args:
        ratios (list): Liste des ratios (b_i / a_ij) pour chaque variable de base.
        lexicographic_rows (list of lists): Lignes de la matrice lexicographique correspondant aux variables de base.

    Returns:
        int: L'indice de la variable sortante.
    """

    min_ratio = float('inf')
    leaving_index = -1

    for i, ratio in enumerate(ratios):
        if ratio > 0 and ratio < min_ratio:
            min_ratio = ratio
            leaving_index = i
        elif ratio > 0 and ratio == min_ratio:
            # En cas d'égalité des ratios, utiliser la méthode lexicographique
            if np.lexicographical_compare(lexicographic_rows[i], lexicographic_rows[leaving_index]) < 0:
                leaving_index = i

    return leaving_index

if __name__ == '__main__':
    # Exemple d'utilisation
    objective_coeffs = [2, 3]
    constraints_matrix = [[1, 1], [2, 1]]
    constraints_rhs = [4, 6]

    print("Problème initial :")
    print(f"Coefficients de l'objectif : {objective_coeffs}")
    print(f"Matrice des contraintes : {constraints_matrix}")
    print(f"Côté droit des contraintes : {constraints_rhs}")

    objective_coeffs_lex, constraints_matrix_lex, lexicographic_matrix = lexicographic_method(objective_coeffs, constraints_matrix, constraints_rhs)

    print("\nProblème avec la méthode lexicographique :")
    print(f"Coefficients de l'objectif : {objective_coeffs_lex}")
    print(f"Matrice des contraintes : {constraints_matrix_lex}")
    print(f"Matrice lexicographique :\n{lexicographic_matrix}")

    # Exemple d'utilisation de find_leaving_variable_lexicographic
    ratios = [4, 3]  # Ratios hypothétiques
    lexicographic_rows = lexicographic_matrix  # Utiliser la matrice lexicographique complète

    leaving_variable_index = find_leaving_variable_lexicographic(ratios, lexicographic_rows)

    print(f"\nIndice de la variable sortante (méthode lexicographique) : {leaving_variable_index}")
