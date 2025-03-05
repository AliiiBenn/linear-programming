import numpy as np
import matplotlib.pyplot as plt

class FonctionLineaire:
    def __init__(self, coefficients, constante=0):
        """
        Initialise une fonction linéaire.
        
        Args:
            coefficients: liste ou array des coefficients [a, b, ...] pour ax + by + ...
            constante: terme constant c dans ax + by + ... + c
        """
        self.coefficients = np.array(coefficients)
        self.constante = constante
        
    def evaluer(self, points):
        """
        Évalue la fonction pour un point ou ensemble de points donnés.
        
        Args:
            points: array de la forme [x, y, ...] ou [[x1,y1,...], [x2,y2,...], ...]
        """
        points = np.array(points)
        if points.ndim == 1:
            return np.dot(self.coefficients, points) + self.constante
        return np.dot(points, self.coefficients) + self.constante
    
    def __str__(self):
        """Représentation string de la fonction"""
        terms = []
        for i, coef in enumerate(self.coefficients):
            if coef != 0:
                if i == 0:
                    terms.append(f"{coef}x")
                elif i == 1:
                    terms.append(f"{coef}y")
                else:
                    terms.append(f"{coef}x_{i}")
        
        if self.constante != 0:
            terms.append(str(self.constante))
            
        return " + ".join(terms)

def visualiser_fonction_lineaire(f, x_range=(-10, 10), y_range=(-10, 10)):
    """
    Visualise une fonction linéaire en 2D.
    """
    # Créer une grille de points
    x = np.linspace(x_range[0], x_range[1], 100)
    y = np.linspace(y_range[0], y_range[1], 100)
    X, Y = np.meshgrid(x, y)
    
    # Calculer les valeurs de la fonction
    points = np.column_stack((X.ravel(), Y.ravel()))
    Z = f.evaluer(points).reshape(X.shape)
    
    # Créer le graphique
    plt.figure(figsize=(10, 8))
    
    # Tracer les courbes de niveau
    contours = plt.contour(X, Y, Z, levels=20)
    plt.clabel(contours, inline=True, fontsize=8)
    
    # Ajouter les axes et les labels
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Visualisation de f(x,y) = {f}')
    plt.colorbar(label='Valeur de f(x,y)')
    
    plt.show()

# Exemple d'utilisation:
if __name__ == "__main__":
    # Créer la fonction f(x,y) = 2x + 3y + 1
    f = FonctionLineaire([2, 3], 1)
    
    # Évaluer pour un point
    point = [1, 2]
    print(f"f{tuple(point)} = {f.evaluer(point)}")
    
    # Évaluer pour plusieurs points
    points = np.array([[1, 2], [0, 1], [2, 0]])
    print("\nÉvaluation pour plusieurs points:")
    for pt, val in zip(points, f.evaluer(points)):
        print(f"f{tuple(pt)} = {val}")
    
    # Afficher la fonction
    print(f"\nFonction: {f}")

    # Visualiser la fonction
    visualiser_fonction_lineaire(f)