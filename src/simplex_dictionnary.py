import numpy as np





class SimplexDictionary:
    def __init__(self, objective_coeffs, constraints_matrix, constraints_rhs, basic_vars=None, nonbasic_vars=None, artificial_vars=None):
        """
        Initialize a simplex dictionary
        
        Args:
            objective_coeffs: coefficients of objective function
            constraints_matrix: matrix of constraint coefficients
            constraints_rhs: right-hand side values of constraints
            basic_vars: initial basic variables
            nonbasic_vars: initial non-basic variables
            artificial_vars: initial artificial variables
        """
        self.objective_coeffs = objective_coeffs
        self.constraints_matrix = constraints_matrix
        self.constraints_rhs = constraints_rhs
        self.num_constraints = len(constraints_rhs)
        self.num_original_vars = len(objective_coeffs)
        self.artificial_vars = artificial_vars if artificial_vars is not None else []
        
        if basic_vars is None:
            self.basic_vars = [f's{i+1}' for i in range(self.num_constraints)]  # Basic variables (slack variables)
        else:
            self.basic_vars = basic_vars
        if nonbasic_vars is None:
            self.nonbasic_vars = [f'x{i+1}' for i in range(self.num_original_vars)]  # Non-basic variables (original variables)
        else:
            self.nonbasic_vars = nonbasic_vars
        self.equations = {}        # Dictionary equations
        self.objective = {}        # Objective function
        
    def is_feasible(self):
        """Check if dictionary is feasible"""
        # A dictionary is feasible if all basic variables are non-negative
        return all(value >= 0 for value in self.get_basic_values())
    
    def create_initial_dictionary(self):
        """Create initial dictionary with slack variables"""
        # Initialize equations for basic variables
        for i, var in enumerate(self.basic_vars):
            if var in self.artificial_vars:
                # Handle artificial variables
                constraint_index = self.artificial_vars.index(var)
                self.equations[var] = f"{self.constraints_rhs[constraint_index]} "
                for j, coeff in enumerate(self.constraints_matrix[constraint_index]):
                    self.equations[var] += f"- {coeff}*{self.nonbasic_vars[j]} "
                self.equations[var] = self.equations[var].strip()
            else:
                # Handle slack variables
                var_index = self.basic_vars.index(var)
                self.equations[var] = f"{self.constraints_rhs[var_index]} "
                for j, coeff in enumerate(self.constraints_matrix[var_index]):
                    self.equations[var] += f"- {coeff}*{self.nonbasic_vars[j]} "
                self.equations[var] = self.equations[var].strip()

        # Initialize objective function
        self.objective['z'] = "0 "
        for j, coeff in enumerate(self.objective_coeffs):
            if j < len(self.nonbasic_vars):  # Vérifier que nous ne dépassons pas la taille de nonbasic_vars
                self.objective['z'] += f"+ {coeff}*{self.nonbasic_vars[j]} "
        self.objective['z'] = self.objective['z'].strip()

    def get_basic_values(self):
        """
        Calculate and return the current values of the basic variables.
        """
        basic_values = []
        for var in self.basic_vars:
            expr = self.equations[var]
            # Evaluate the expression by setting non-basic variables to 0
            value = float(expr.split()[0])  # The constant term is the value
            basic_values.append(value)
        return basic_values

    def __str__(self):
        """String representation of the dictionary"""
        result = "Current dictionary:\n"
        # Show equations for basic variables
        for var, expr in self.equations.items():
            result += f"{var} = {expr}\n"
        # Show objective function
        result += f"z = {self.objective['z']}\n"
        return result

# Example usage:
def example_feasible_dictionary():
    """
    Example of creating and checking a feasible dictionary
    """
    # Initial dictionary for the example problem
    objective_coeffs=[2, 3]
    constraints_matrix=[[1, 1], [2, 1]]
    constraints_rhs=[4, 6]
    dictionary = SimplexDictionary(
        objective_coeffs=objective_coeffs,
        constraints_matrix=constraints_matrix,
        constraints_rhs=constraints_rhs
    )
    
    # Create initial dictionary (which is feasible)
    dictionary.create_initial_dictionary()
    
    print("Initial feasible dictionary:")
    print(dictionary)
    print(f"Is feasible: {dictionary.is_feasible()}")
    
    return dictionary

# Run example
if __name__ == "__main__":
    example_feasible_dictionary()
