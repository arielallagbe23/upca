class PolishCalculator:
    def __init__(self):
        # Initialisation de la pile pour stocker les opérandes
        self.stack = []

    def polish_calcul_npi(self, expression):
        # Division de l'expression en tokens (opérandes et opérateurs)
        tokens = expression.split()
        print(f"Tokens: {tokens}")  # Débogage
        for token in tokens:
            # Vérification afin de savoir si le token est un nombre (positif ou négatif) et ajout à la pile
            if token.replace('.', '').isdigit() or (token[0] == '-' and token[1:].replace('.', '').isdigit()):
                self.stack.append(float(token))
            # Si le token est un opérateur, réalisation de l'opération correspondante
            elif token in {'+', '-', '*', '/'}:
                # Vérifie si la pile a au moins deux opérandes pour effectuer l'opération
                if len(self.stack) < 2:
                    raise ValueError("Invalid expression")
                # Récupère les deux derniers opérandes de la pile
                operand2 = self.stack.pop()
                operand1 = self.stack.pop()
                print(f"Operands: {operand1}, {operand2}")  # Débogage
                # Effectue l'opération et ajoute le résultat à la pile
                result = self.perform_operation(operand1, operand2, token)
                print(f"Result after {token}: {result}")  # Débogage
                self.stack.append(result)
            else:
                # Si le token n'est ni un nombre ni un opérateur, lève une exception
                print(f"Invalid token: {token}")
                raise ValueError("Invalid token: {}".format(token))
        #  Vérification si la pile contient exactement un résultat après l'évaluation
        if len(self.stack) == 1:
            final_result = self.stack[0]
            # Vide la pile pour le prochain calcul
            self.stack = []
            return final_result
        else:
            # Vide la pile en cas d'expression invalide
            self.stack = []
            raise ValueError("Invalid expression")

    def perform_operation(self, operand1, operand2, operator):
        # Realisation l'opération en fonction de l'opérateur
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            # Vérification si le dénominateur n'est pas zéro pour éviter une division par zéro
            if operand2 == 0:
                raise ValueError("Division by zero")
            return operand1 / operand2

# Création d'une instance de la classe
polish_calculator_instance = PolishCalculator()

# Utilisation de l'instance pour effectuer le calcul
result1 = polish_calculator_instance.polish_calcul_npi("5 4 + 2 *")
print(result1)

# Utilisation pour un autre calcul successif
result2 = polish_calculator_instance.polish_calcul_npi("3 2 -")
print(result2)
