class Operateur:
    @staticmethod
    def addition(op1, op2):
        return op1 + op2

    @staticmethod
    def soustraction(op1, op2):
        return op1 - op2

    @staticmethod
    def multiplication(op1, op2):
        return op1 * op2

    @staticmethod
    def division(op1, op2):
        if op2 != 0:
            return op1 / op2
        else:
            raise ZeroDivisionError("Division par zéro n'est pas autorisée.")
