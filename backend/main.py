#PRIMERO: importamos Flask (de no tenerlo instalar desde 'cmd' con 'pip install Flask, Flask-Cors, Jsonify)
from flask import Flask, request
from flask_cors import CORS
from flask.json import jsonify
from clases.usuario import Usuario
from estructuras.estructura import lista_usuarios

#SEGUNDO: Creamos la API de Flask
app = Flask(__name__)

#TERCERO: Añadimos los cors
cors = CORS(app)

#Creamos un ENDPOINT de bienvenida
@app.route('/')
def index():
    return '<h1> Bienvenido a mi API</h1><br\\><p>Usando backend con Python y Flask</p>'

#ENDPOINT para crear un usuario = CREATE
@app.route('/usuario/crear', methods=['POST'])
def crear_usuario():
    if request.method == 'POST':
        try:
            nombre = request.json['nombre']
            username = request.json['username']
            password = request.json['password']
            nuevo = Usuario(nombre, username, password)
            lista_usuarios.append(nuevo)
            return jsonify({
                'message': 'Usuario creado exitosamente',
                'status': 200
            }), 200
        except KeyError as e:
            return jsonify({
                'message':f'Falta el atributo: {e}',
                'status': 400
            }), 400
        except Exception as e:
            return jsonify({
                'message':f'Error al procesar la solicitud en el servidor: {str(e)}',
                'status': 400
            }), 400
        
#ENDPOINT PARA VER TODOS LOS USUARIOS = READ
@app.route('/usuario/ver', methods=['GET'])
def ver_usuario():
    if request.method == 'GET':
        diccionario_respuesta = {
            'message':'Lista de usuarios:',
            'usuario':[],
            'status':200
        }
        for user in lista_usuarios:
            diccionario_respuesta['usuario'].append({
                'nombre': user.nombre,
                'username': user.username,
                'password': user.password
            })
        return jsonify(diccionario_respuesta), 200

#ENDPOINT para actualizar usuario = UPDATE
@app.route('/usuario/actualizar/<string:username>', methods=['PUT'])
def actualizar_usuario(username):
    if request.method == 'PUT':
        try:
            #Antes del for validemos que si exista
            nombre = request.json['nombre']
            password = request.json['password']
            for user in lista_usuarios:
                if user.username == username:
                    user.nombre = nombre
                    user.password = password
                    return jsonify({
                        'message': 'Usuario actualizado correctamente',
                        'status':200
                    }), 200
            return jsonify({
                'message':'El usuario que agregó no se encuentra en el sistema',
                'status': 400
            }), 400
        except KeyError as e:
            return jsonify({
                'message':f'Falta el atributo: {e}',
                'status': 400
            }), 400
        except Exception as e:
            return jsonify({
                'message':f'Error al procesar la solicitud en el servidor: {str(e)}',
                'status': 400
            }), 400
        
#Actualizar cambios mínimos = PATCH
@app.route('/usuario/actualizar/password/<string:username>', methods=['PATCH'])
def actualizar_contra(username):
    if request.method == 'PATCH':
        try:
            password = request.json['password']
            for user in lista_usuarios:
                if user.username == username:
                    user.password = password
                    return jsonify({
                        'message':'Contraseña actualizada correctamente',
                        'status':200
                    }), 200
            return jsonify({
                'message':'El usuario que agregó no se encuentra en el sistema',
                'status': 400
            }), 400
        
        except KeyError as e:
            return jsonify({
                'message':f'Falta el atributo: {e}',
                'status': 400
            }), 400
        except Exception as e:
            return jsonify({
                'message':f'Error al procesar la solicitud en el servidor: {str(e)}',
                'status': 400
            }), 400

# ENDPOINT Eliminar usuario = DELETE
@app.route('/usuario/eliminar/<string:username>', methods=['DELETE'])
def eliminar_usuario(username):
    if request.method == 'DELETE':
        try:
            for user in lista_usuarios:
                if user.username == username:
                    lista_usuarios.remove(user)
                    return jsonify({
                        'message': 'Usuario eliminado correctamente',
                        'status': 200
                    }), 200
            return jsonify({
                'message': 'El usuario no se encuentra en el sistema',
                'status': 400
            }), 400
        except Exception as e:
            return jsonify({
                'message': f'Error al procesar la solicitud en el servidor: {str(e)}',
                'status': 400
            }), 400

#Vamos a crear un Loggin
@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
            if username == 'AdminIPC2' and password == 'IPC2VJ2024':
                return jsonify({
                    'message': 'Usuario logeado correctamente',
                    'role': 1,
                    'status': 200
                }), 200
            for user in lista_usuarios:
                if user.username == username and user.password == password:
                    return jsonify({
                        'message': 'Usuario logeado correctamente',
                        'role': 2,
                        'status': 200
                    }), 200
                
            return jsonify({
                'message': 'Usuario o Contraseña inválidos',
                'status': 400
            }), 400
        
        except KeyError as e:
            return jsonify({
                'message': f'Falta el atributo: {e}',
                'status': 400
            }), 400
        except Exception as e:
            return jsonify({
                'message': f'Error al procesar la solicitud en el servidor: {str(e)}',
                'status': 400
            }), 400



#MANEJO GENÉRICO DE ERRORES 404 PARA CUANDO LA RUTA NO EXISTE
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'message':'La ruta solicitada no existe',
        'status':404
    }),404

#MANEJO GENÉRICO DE ERRORES 405 PARA CUADNO EL MÉTODO NO ESTÁ PERMITIDO
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        'message':'El método solicitado no está permitido',
        'status': 405
    }), 405

        
#El host puede ser localhost o 0.0.0.0; en este caso como es para pruebas se queda como localhost
#El debug=True es para que cada vez que guarde, automaticamente se hagan los cambios
if __name__ == '__main__':
    app.run(host= 'localhost', port=4000, debug=True)