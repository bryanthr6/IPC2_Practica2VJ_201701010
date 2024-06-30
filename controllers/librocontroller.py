# Todo el manejo de libros será aquí
# Blueprint nos ayuda a tener distintos controladores dentro de Python para mantener orden en las APIs
from flask import Blueprint, jsonify, request, Response
from models.libro import Libro
from xml.etree import ElementTree as ET
import os

Blueprint_libro = Blueprint('libro', __name__)

libros = []

#ENDPOINT PARA OBTENER TODOS LOS LIBROS
@Blueprint_libro.route('/cargarLibros', methods=['POST'])
def carga_libro():
    try:
        # Obtenemos el archivo XML
        xml_entrada = request.data.decode('utf-8')
        if xml_entrada == '':
            return jsonify({
                'message': 'Error al cargar los libros: El XML está vacío',
                'status': 404
            }), 404

        # QUITARLE LOS SALTOS DE LÍNEA INNECESARIOS AL ARCHIVO XML
        xml_entrada = xml_entrada.replace('\n', '')

        # LEER el XML
        root = ET.fromstring(xml_entrada)
        for libro in root:
            id = libro.attrib['id']
            titulo = ''
            autor = ''
            idioma = ''
            categoria = ''
            editorial = ''
            copias = ''
            for elemento in libro:
                if elemento.tag == 'titulo':
                    titulo = elemento.text
                if elemento.tag == 'autor':
                    autor = elemento.text 
                if elemento.tag == 'idioma':
                    idioma = elemento.text
                if elemento.tag == 'categoria':
                    categoria = elemento.text
                if elemento.tag == 'editorial':
                    editorial = elemento.text
                if elemento.tag == 'copias':
                    copias = elemento.text
            nuevo = Libro(id, titulo, autor, idioma, categoria, editorial, copias)

            # Verificar si el libro ya existe en la lista para evitar duplicados
            if not any(l.id == nuevo.id for l in libros):
                libros.append(nuevo)

            # Agregar el libro al XML que YA EXISTE
            if os.path.exists('database/libros.xml'):
                tree2 = ET.parse('database/libros.xml')
                root2 = tree2.getroot()
                # Verificar si el libro ya existe en el XML para evitar duplicados
                if not any(l.attrib['id'] == nuevo.id for l in root2.findall('libro')):
                    nuevo_libro = ET.SubElement(root2, 'libro', id=nuevo.id)
                    titulo = ET.SubElement(nuevo_libro, 'titulo')
                    titulo.text = nuevo.titulo
                    autor = ET.SubElement(nuevo_libro, 'autor')
                    autor.text = nuevo.autor 
                    idioma = ET.SubElement(nuevo_libro, 'idioma')
                    idioma.text = nuevo.idioma
                    categoria = ET.SubElement(nuevo_libro, 'categoria')
                    categoria.text = nuevo.categoria
                    editorial = ET.SubElement(nuevo_libro, 'editorial')
                    editorial.text = nuevo.editorial
                    copias = ET.SubElement(nuevo_libro, 'copias')
                    copias.text = nuevo.copias
                    ET.indent(root2, space='\t', level=0)
                    tree2.write('database/libros.xml', encoding='utf-8', xml_declaration=True)

        # Si en dado caso no existe el XML lo creamos
        if not os.path.exists('database/libros.xml'):
            with open('database/libros.xml', 'w', encoding='utf-8') as file:
                file.write(xml_entrada)

        return jsonify({
            'message': 'Libros cargados correctamente',
            'status': 200
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'Error al cargar los libros: {str(e)}',
            'status': 404
        }), 404

# Endpoint para obtener todos los libros en formato JSON
@Blueprint_libro.route('/verLibros', methods=['GET'])
def ver_libros():
    try:
        if not libros:
            return jsonify({
                'libros': [],
                'message': 'No hay libros disponibles',
                'status': 404
            }), 404

        libros_json = [libro.to_dict() for libro in libros]

        return jsonify({
            'libros': libros_json,
            'message': 'Lista de libros obtenida correctamente',
            'status': 200
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'Error al obtener la lista de libros: {str(e)}',
            'status': 500
        }), 500

#ENDPOINT PARA OBTENER UN LIBRO POR ID
# Endpoint para obtener un libro por su ID en formato XML
@Blueprint_libro.route('/verLibro/<string:id>', methods=['GET'])
def ver_libro(id):
    try:
        # Buscar el libro por su ID en la lista de libros
        libro_encontrado = next((libro for libro in libros if libro.id == id), None)

        if not libro_encontrado:
            return jsonify({
                'message': 'Libro no encontrado',
                'status': 404
            }), 404

        # Construir el XML utilizando ElementTree
        root = ET.Element('libro')
        root.set('id', libro_encontrado.id)

        titulo = ET.SubElement(root, 'titulo')
        titulo.text = libro_encontrado.titulo

        autor = ET.SubElement(root, 'autor')
        autor.text = libro_encontrado.autor

        idioma = ET.SubElement(root, 'idioma')
        idioma.text = libro_encontrado.idioma

        categoria = ET.SubElement(root, 'categoria')
        categoria.text = libro_encontrado.categoria

        editorial = ET.SubElement(root, 'editorial')
        editorial.text = libro_encontrado.editorial

        copias = ET.SubElement(root, 'copias')
        copias.text = libro_encontrado.copias

        # Crear el objeto Response con el XML generado
        xml_data = ET.tostring(root, encoding='utf-8')
        response = Response(xml_data, mimetype='application/xml')

        return response, 200

    except Exception as e:
        return jsonify({
            'message': f'Error al obtener el libro: {str(e)}',
            'status': 500
        }), 500

#ENDPOINT para obtener libros por categoría en formato JSON
@Blueprint_libro.route('/libros/<string:categoria>', methods=['GET'])
def libros_por_categoria(categoria):
    try:
        # Filtrar libros por la categoría especificada
        libros_filtrados = [libro for libro in libros if libro.categoria.lower() == categoria.lower()]

        if not libros_filtrados:
            return jsonify({
                'libros': [],
                'message': f'No hay libros disponibles en la categoría "{categoria}"',
                'status': 404
            }), 404

        # Convertir los libros filtrados a formato JSON
        libros_json = [libro.to_dict() for libro in libros_filtrados]

        return jsonify({
            'libros': libros_json,
            'message': f'Lista de libros en la categoría "{categoria}" obtenida correctamente',
            'status': 200
        }), 200

    except Exception as e:
        return jsonify({
            'message': f'Error al obtener la lista de libros por categoría: {str(e)}',
            'status': 500
        }), 500

# MÉTODO DE PRECARGAR LIBROS
# Este método lo que retorna es el array de libros, si no hay nada en la base de datos regresa vacío
# En caso de que haya algo se encarga de leer el XML primero y lo escribe en el array de libros
def precarga_libros():
    books = []
    if os.path.exists('database/libros.xml'):
        tree = ET.parse('database/libros.xml')
        root = tree.getroot()
        for libro in root:
            id = libro.attrib['id']
            titulo = ''
            autor = ''
            idioma = ''
            categoria = ''
            editorial = ''
            copias = ''
            for elemento in libro:
                if elemento.tag == 'titulo':
                    titulo = elemento.text
                if elemento.tag == 'autor':
                    autor = elemento.text 
                if elemento.tag == 'idioma':
                    idioma = elemento.text
                if elemento.tag == 'categoria':
                    categoria = elemento.text
                if elemento.tag == 'editorial':
                    editorial = elemento.text
                if elemento.tag == 'copias':
                    copias = elemento.text
            nuevo = Libro(id, titulo, autor, idioma, categoria, editorial, copias)
            books.append(nuevo)
    return books
