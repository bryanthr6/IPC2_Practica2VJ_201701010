# Definición de la clase Libro
class Libro:
    def __init__(self, id, titulo, autor, idioma, categoria, editorial, copias):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.idioma = idioma
        self.categoria = categoria
        self.editorial = editorial
        self.copias = copias

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'idioma': self.idioma,
            'categoria': self.categoria,
            'editorial': self.editorial,
            'copias': self.copias
        }
