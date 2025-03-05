
class SimplexDictionary:
    def __init__(self, basic_vars, nonbasic_vars, equations, objective_function):
        """
        Représente un dictionnaire du simplexe.

        Args:
            basic_vars (list): Liste des variables de base (chaînes de caractères).
            nonbasic_vars (list): Liste des variables non basiques (chaînes de caractères).
            equations (dict): Dictionnaire des équations pour les variables de base.
                             Les clés sont les variables de base, et les valeurs sont des chaînes
                             de caractères représentant l'expression en fonction des variables
                             non basiques (par exemple, "2 - 2*x2 - 2*x4 + x6").
            objective_function (str): Chaîne de caractères représentant la fonction objective
                                       en fonction des variables non basiques
                                       (par exemple, "13 - 3*x2 - x4 - x6").
        """
        self.basic_vars = basic_vars
        self.nonbasic_vars = nonbasic_vars
        self.equations = equations
        self.objective_function = objective_function

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du dictionnaire.
        """
        representation = ""
        for var in self.basic_vars:
            representation += f"{var} = {self.equations[var]}\n"
        representation += f"z = {self.objective_function}\n"
        return representation

# Exemple d'utilisation
basic_vars = ["x1", "x3", "x5"]
nonbasic_vars = ["x2", "x4", "x6"]
equations = {
    "x1": "2 - 2*x2 - 2*x4 + x6",
    "x3": "1 + x2 + 3*x4 - 2*x6",
    "x5": "1 + 5*x2 + 2*x4"
}
objective_function = "13 - 3*x2 - x4 - x6"

# Création d'une instance de la classe SimplexDictionary
dictionary = SimplexDictionary(basic_vars, nonbasic_vars, equations, objective_function)

# Affichage du dictionnaire
print(dictionary)
