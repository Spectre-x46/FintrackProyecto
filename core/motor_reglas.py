import re

class MotorCategorizacion:
    def __init__(self, reglas_usuario):
        self.reglas = reglas_usuario # ej: {"uber": "Transporte"}
        
    def analizar(self, texto_crudo):
        texto = texto_crudo.lower()
        for clave, categoria in self.reglas.items():
            # Busca la palabra clave completa, ignorando mayúsculas/minúsculas
            if re.search(r'\b' + re.escape(clave.lower()) + r'\b', texto):
                return categoria 
        return "Sin Categoría"
