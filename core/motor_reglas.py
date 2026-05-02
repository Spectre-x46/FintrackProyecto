class MotorCategorizacion:
    def __init__(self, reglas_usuario):
        self.reglas = reglas_usuario # ej: {"uber": "Transporte"}
    def analizar(self, texto_crudo):
        texto = texto_crudo.lower()
        for clave, categoria in self.reglas.items():
            if clave in texto:
                return categoria 
        return "Sin Categoría"
