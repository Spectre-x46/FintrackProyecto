import re

class MotorCategorizacion:
    """
    Motor de clasificación automática de transacciones por palabras clave.

    Recibe un diccionario {palabra_clave: nombre_categoria} construido desde
    las ReglaAutomatica del usuario en la BD, y clasifica cualquier texto
    buscando coincidencias de palabras completas (usando Regex).

    Uso:
        motor = MotorCategorizacion({"rappi": "Delivery", "uber": "Transporte"})
        motor.analizar("Pago Rappi comida")  # → "Delivery"
        motor.analizar("Compra sin match")   # → "Sin Categoría"
    """

    def __init__(self, reglas_usuario):
        # reglas_usuario: dict {str: str} construido desde ReglaAutomatica.objects
        self.reglas = reglas_usuario

    def analizar(self, texto_crudo):
        """
        Analiza el texto y devuelve el nombre de la primera categoría coincidente.
        Si no hay ninguna coincidencia, devuelve 'Sin Categoría'.
        La búsqueda es insensible a mayúsculas y busca palabras completas (no subcadenas).
        """
        texto = texto_crudo.lower()
        for clave, categoria in self.reglas.items():
            if re.search(r'\b' + re.escape(clave.lower()) + r'\b', texto):
                return categoria
        return "Sin Categoría"
