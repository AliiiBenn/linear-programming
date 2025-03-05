def introduce_slack_variables(constraints):
    """
    Introduit des slack variables pour convertir les inégalités en égalités.

    Args:
        constraints (list): Une liste de chaînes de caractères représentant les contraintes.
                             Chaque contrainte doit être au format "expression <= valeur" ou "expression >= valeur".

    Returns:
        list: Une liste de chaînes de caractères représentant les contraintes converties en égalités,
              avec les slack variables introduites.
    """
    equalities = []
    slack_variable_count = 1
    
    for constraint in constraints:
        if "<=" in constraint:
            expression, value = constraint.split("<=")
            slack_variable = f"s{slack_variable_count}"
            equalities.append(f"{expression} + {slack_variable} = {value}")
            slack_variable_count += 1
        elif ">=" in constraint:
            expression, value = constraint.split(">=")
            slack_variable = f"s{slack_variable_count}"
            equalities.append(f"{expression} - {slack_variable} = {value}")
            slack_variable_count += 1
        else:
            equalities.append(constraint)  # Si ce n'est pas une inégalité, on la garde telle quelle
            
    return equalities

# Exemple d'utilisation
constraints = [
    "x1 + x2 <= 4",
    "2*x1 + x2 <= 6",
    "x1 >= 0",
    "x2 >= 0"
]

equalities = introduce_slack_variables(constraints)

for equality in equalities:
    print(equality)
