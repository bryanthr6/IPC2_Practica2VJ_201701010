#Método más ordenando o más estructurado para el backend
from flask import Flask
from flask_cors import CORS
from controllers.librocontroller import Blueprint_libro, libros, precarga_libros

app = Flask(__name__)
cors = CORS(app)

#Para PRECARGAR la data
libros = precarga_libros()

print(len(libros))


app.register_blueprint(Blueprint_libro)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    