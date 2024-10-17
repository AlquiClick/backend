from flask import (
    jsonify,
    render_template,
    redirect,
    request,
    url_for,
    Blueprint
)
from models import(
    Marca,
    Fabricante,
    Modelo,
    Categoria,
    Caracteristica,
    Equipo,
    Stock,
    Proveedor,
    Accesorio,
)
from app import db
from forms import MarcaForm
from services.marca_service import MarcaService
from repositories.marca_repository import MarcaRepository

shop_bp = Blueprint('shop', __name__)

@shop_bp.route("/")
def home():
    return render_template("index.html")

@shop_bp.route("/marcas", methods=['POST', 'GET', 'DELETE', 'PUT'])
def marcas():
    form = MarcaForm()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(nombre=nombre)
        db.session.add(nueva_marca)
        db.session.commit()

    elif request.method == 'DELETE':
        marca_id = request.json.get('id')
        if not marca_id:
            return jsonify({"error": "ID is required"}), 400

        marca = Marca.query.get(marca_id)
        print(marca)
        if marca:
            marca.is_active = 0
            db.session.commit()
            return jsonify({"message": f"La marca se eliminó correctamente"}), 200
        else:
            return jsonify({"error": f"Marca with ID {marca_id} not found"}), 404

    elif request.method == 'PUT':
        marca_id = request.json.get('id')
        nuevo_nombre = request.json.get('nombre')
        if not marca_id or not nuevo_nombre:
            return jsonify({"error": "ID and new name are required"}), 400

        marca = Marca.query.get(marca_id)
        if marca:
            marca.nombre = nuevo_nombre
            db.session.commit()
            return jsonify({"message": f"Marca with ID {marca_id} updated successfully"}), 200
        else:
            return jsonify({"error": f"Marca with ID {marca_id} not found"}), 404

    marcas = Marca.query.filter_by(is_active=1).all()
    return render_template(
        "marcas.html",
        marcas=marcas,
        form=form
    )

@shop_bp.route("/marca_list", methods=['POST', 'GET'])
def marcas_list():   
    formulario = MarcaForm()

    services = MarcaService(MarcaRepository())
    marcas = services.get_all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        services.create(nombre=nombre)
        return redirect(url_for('marcas'))

    return render_template(
        'marca_list.html',
         marcas=marcas,
         formulario=formulario
        )

@shop_bp.route("/fabricantes", methods=['POST', 'GET', 'DELETE', 'PUT'])
def fabricantes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        pais_origen = request.form['pais_origen']
        nuevo_fabricante = Fabricante(
            nombre=nombre, 
            pais_origen=pais_origen
        )
        db.session.add(nuevo_fabricante)
        db.session.commit()

    elif request.method == 'DELETE':
        fabricante_id = request.json.get('id')
        if not fabricante_id:
            return jsonify({"error": "ID is required"}), 400

        fabricante = Fabricante.query.get(fabricante_id)
        if fabricante:
            fabricante.is_active = 0
            db.session.commit()
            return jsonify({"message": f"El fabricante se eliminó correctamente"}), 200
        else:
            return jsonify({"error": f"fabricante with ID {fabricante_id} not found"}), 404

    elif request.method == 'PUT':
        fabricante_id = request.json.get('id')
        nuevo_nombre = request.json.get('nombre')
        nuevo_pais_origen = request.json.get('paisOrigen')
        if not fabricante_id or not nuevo_nombre:
            return jsonify({"error": "ID and new name are required"}), 400

        fabricante = Fabricante.query.get(fabricante_id)
        if fabricante:
            fabricante.nombre = nuevo_nombre
            fabricante.pais_origen = nuevo_pais_origen
            db.session.commit()
            return jsonify({"message": f"fabricante with ID {fabricante_id} updated successfully"}), 200
        else:
            return jsonify({"error": f"fabricante with ID {fabricante_id} not found"}), 404

    fabricantes = Fabricante.query.filter_by(is_active=1).all()
    return render_template("fabricantes.html", fabricantes=fabricantes)

@shop_bp.route("/modelos", methods=['POST', 'GET', 'DELETE', 'PUT'])
def modelos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fabricante_id = request.form['fabricante_id']
        nuevo_modelo = Modelo(
            nombre=nombre, 
            fabricante_id=fabricante_id
        )
        db.session.add(nuevo_modelo)
        db.session.commit()

    elif request.method == 'DELETE':
        modelo_id = request.json.get('id')
        if not modelo_id:
            return jsonify({"error": "ID is required"}), 400

        modelo = Modelo.query.get(modelo_id)
        if modelo:
            modelo.is_active = 0
            db.session.commit()
            return jsonify({"message": f"El modelo se eliminó correctamente"}), 200
        else:
            return jsonify({"error": f"modelo with ID {modelo_id} not found"}), 404

    elif request.method == 'PUT':
        modelo_id = request.json.get('id')
        nuevo_nombre = request.json.get('nombre')
        nuevo_fabricante = request.json.get('fabricante_id')
        if not modelo_id or not nuevo_nombre:
            return jsonify({"error": "ID and new name are required"}), 400

        modelo = Modelo.query.get(modelo_id)
        if modelo:
            modelo.nombre = nuevo_nombre
            modelo.fabricante_id = nuevo_fabricante
            db.session.commit()
            return jsonify({"message": f"fabricante with ID {modelo.id} updated successfully"}), 200
        else:
            return jsonify({"error": f"fabricante with ID {modelo.id} not found"}), 404

    modelos = Modelo.query.filter_by(is_active=1).all()
    fabricantes = Fabricante.query.filter_by(is_active=1).all()
    return render_template("modelos.html", modelos=modelos, fabricantes=fabricantes)

@shop_bp.route("/categorias", methods=['POST', 'GET'])
@shop_bp.route("/categorias/<int:id>", methods=['POST'])
def categorias(id=None):
    if request.method == 'POST':
        if id:
            method = request.form.get('_method')
            if method == 'PUT':
                categoria = Categoria.query.get(id)
                if categoria:
                    categoria.nombre = request.form['nombre']
                    db.session.commit()
                    return redirect(url_for('categorias'))
                else:
                    return jsonify({"error": f"Categoria with ID {id} not found"}), 404
            elif method == 'DELETE':
                categoria = Categoria.query.get(id)
                if categoria:
                    categoria.is_active = False
                    db.session.commit()
                    return redirect(url_for('categorias'))
                else:
                    return jsonify({"error": f"Categoria with ID {id} not found"}), 404
        else:
            nombre = request.form['nombre']
            nueva_categoria = Categoria(nombre=nombre)
            db.session.add(nueva_categoria)
            db.session.commit()
            return redirect(url_for('categorias'))

    categorias = Categoria.query.filter_by(is_active=True).all()
    return render_template("categorias.html", categorias=categorias)

@shop_bp.route("/caracteristicas", methods=['POST', 'GET'])
@shop_bp.route("/caracteristicas/<int:id>", methods=['POST'])
def caracteristicas(id=None):
    if request.method == 'POST':
        if id:
            method = request.form.get('_method')
            if method == 'PUT':
                caracteristica = Caracteristica.query.get(id)
                if caracteristica:
                    caracteristica.tipo = request.form['tipo']
                    caracteristica.descripcion = request.form['descripcion']
                    db.session.commit()
                    return redirect(url_for('caracteristicas'))
                else:
                    return jsonify({"error": f"Caracteristica with ID {id} not found"}), 404
            elif method == 'DELETE':
                caracteristica = Caracteristica.query.get(id)
                if caracteristica:
                    caracteristica.is_active = False
                    db.session.commit()
                    return redirect(url_for('caracteristicas'))
                else:
                    return jsonify({"error": f"Caracteristica with ID {id} not found"}), 404
        else:
            tipo = request.form['tipo']
            descripcion = request.form['descripcion']
            nueva_caracteristica = Caracteristica(tipo=tipo, descripcion=descripcion)
            db.session.add(nueva_caracteristica)
            db.session.commit()
            return redirect(url_for('caracteristicas'))

    caracteristicas = Caracteristica.query.filter_by(is_active=True).all()
    return render_template("caracteristicas.html", caracteristicas=caracteristicas)

@shop_bp.route("/proveedores", methods=['POST', 'GET'])
@shop_bp.route("/proveedores/<int:id>", methods=['POST'])
def proveedores(id=None):
    if request.method == 'POST':
        if id:
            method = request.form.get('_method')
            if method == 'PUT':
                proveedor = Proveedor.query.get(id)
                if proveedor:
                    proveedor.nombre = request.form['nombre']
                    proveedor.contacto = request.form['contacto']
                    db.session.commit()
                    return redirect(url_for('proveedores'))
                else    :
                    return jsonify({"error": f"Proveedor with ID {id} not found"}), 404
            elif method == 'DELETE':
                proveedor = Proveedor.query.get(id)
                if proveedor:
                    proveedor.is_active = False
                    db.session.commit()
                    return redirect(url_for('proveedores'))
                else:
                    return jsonify({"error": f"Proveedor with ID {id} not found"}), 404
        else:
            nombre = request.form['nombre']
            contacto = request.form['contacto']
            nuevo_proveedor = Proveedor(
                nombre=nombre,
                contacto=contacto
            )
            db.session.add(nuevo_proveedor)
            db.session.commit()
            return redirect(url_for('proveedores'))

    proveedores = Proveedor.query.filter_by(is_active=True).all()
    return render_template("proveedores.html", proveedores=proveedores)

@shop_bp.route("/stock", methods=['POST', 'GET'])
@shop_bp.route("/stock/<int:id>", methods=['POST'])
def stock(id=None):
    if request.method == 'POST':
        if id:
            method = request.form.get('_method')
            if method == 'PUT':
                stock = Stock.query.get(id)
                if stock:
                    stock.equipo_id = request.form['equipo']
                    stock.cantidad_disponible = request.form['cantidad']
                    stock.ubicacion = request.form['ubicacion']
                    db.session.commit()
                    return redirect(url_for('stock'))
                else:
                    return jsonify({"error": f"Stock with ID {id} not found"}), 404
            elif method == 'DELETE':
                stock = Stock.query.get(id)
                if stock:
                    stock.is_active = False
                    db.session.commit()
                    return redirect(url_for('stock'))
                else:
                    return jsonify({"error": f"Stock with ID {id} not found"}), 404
        else:
            equipo = request.form['equipo_id']
            cantidad = request.form['cantidad']
            ubicacion = request.form['ubicacion']

            nuevo_stock = Stock(
                equipo_id=equipo,
                cantidad_disponible=cantidad,
                ubicacion=ubicacion
            )

            db.session.add(nuevo_stock)
            db.session.commit()
            return redirect(url_for('stock'))

    stock_list = db.session.query(Stock, Equipo).join(Equipo, Stock.equipo_id==Equipo.id).all()
    equipos = Equipo.query.filter_by(is_active=True).all()
    return render_template("stock.html", stock_list=stock_list, equipos=equipos)

@shop_bp.route("/accesorios", methods=['POST', 'GET'])
@shop_bp.route("/accesorios/<int:id>", methods=['POST'])
def accesorios(id=None):
    if request.method == 'POST':
        if id:
            method = request.form.get('_method')
            if method == 'PUT':
                accesorio = Accesorio.query.get(id)
                if accesorio:
                    accesorio.tipo = request.form['tipo']
                    db.session.commit()
                    return redirect(url_for('accesorios'))
                else:
                    return jsonify({"error": f"Accesorio with ID {id} not found"}), 404
            elif method == 'DELETE':
                accesorio = Accesorio.query.get(id)
                if accesorio:
                    accesorio.is_active = False
                    db.session.commit()
                    return redirect(url_for('accesorios'))
                else:
                    return jsonify({"error": f"Accesorio with ID {id} not found"}), 404
        else:
            tipo = request.form['tipo']
            nuevo_accesorio = Accesorio(
                tipo=tipo
            )
            db.session.add(nuevo_accesorio)
            db.session.commit()
            return redirect(url_for('accesorios'))

    accesorios = Accesorio.query.filter_by(is_active=True).all()
    return render_template("accesorios.html", accesorios=accesorios)

@shop_bp.route("/equipos", methods=['POST', 'GET', 'DELETE', 'PUT'])
def equipos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        modelo_id = request.form['modelo_id']
        categoria_id = request.form['categoria_id']
        costo = request.form['costo']
        nuevo_equipo = Equipo(
            nombre=nombre,
            modelo_id=modelo_id,
            categoria_id=categoria_id,
            costo=costo
        )
        db.session.add(nuevo_equipo)
        db.session.commit()

    elif request.method == 'DELETE':
        equipo_id = request.json.get('id')
        if not equipo_id:
            return jsonify({"error": "ID is required"}), 400

        equipo = Equipo.query.get(equipo_id)
        if equipo:
            equipo.is_active = False
            db.session.commit()
            return jsonify({"message": f"El equipo se eliminó correctamente"}), 200
        else:
            return jsonify({"error": f"Equipo with ID {equipo_id} not found"}), 404

    elif request.method == 'PUT':
        equipo_id = request.json.get('id')
        nuevo_nombre = request.json.get('nombre')
        nuevo_modelo = request.json.get('modelo_id')
        nueva_categoria = request.json.get('categoria_id')
        nuevo_costo = request.json.get('costo')
        if not equipo_id or not nuevo_nombre:
            return jsonify({"error": "ID and new name are required"}), 400

        equipo = Equipo.query.get(equipo_id)
        if equipo:
            equipo.nombre = nuevo_nombre
            equipo.modelo_id = nuevo_modelo
            equipo.categoria_id = nueva_categoria
            equipo.costo = nuevo_costo
            db.session.commit()
            return jsonify({"message": f"fabricante with ID {equipo.id} updated successfully"}), 200
        else:
            return jsonify({"error": f"fabricante with ID {equipo.id} not found"}), 404

    equipos = Equipo.query.filter_by(is_active=True).all()
    modelos = Modelo.query.filter_by(is_active=True).all()
    categorias = Categoria.query.filter_by(is_active=True).all()
    return render_template(
        "equipos.html",
        equipos=equipos,
        modelos=modelos,
        categorias=categorias    
    )

