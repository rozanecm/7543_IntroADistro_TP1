from .info_accesos_entry import info_accesos_entry
import dns.resolver
from flask import abort, make_response, jsonify

# Data to serve with our API
domains = {
    1: {
        'domain': 'localhost',
        'ip': '127.0.0.1',
        'custom': 'true',
    },
	2: {
        'domain': 'www.fi.uba.ar',
        'ip': '157.92.49.38',
        'custom': 'false',
    },
}

def guardar_dominio(domain, ip, custom=False):
    """
    Guarda dominio con su ip correspondiente en registro local de domains.
    Devuelve clave asignada en diccionario 'domains'.
    """
    new_domain = {}
    new_domain['domain'] = domain
    new_domain['ip'] = ip

    new_domain['custom'] = str(custom).lower()

    new_id = max(domains.keys()) + 1
    domains[new_id] = new_domain 
    return new_id

# El siguiente dict tiene como clave un dominio y como valor un objeto
# info_accesos_entry, que devuelve la posicion a acceder del diccionario
# 'domains' definido en la linea 6. De esta forma queda totalmente
# implementado el Round Robin solicitado de forma interna en la clase que
# maneja que registro de los guardados hay que devolver.

info_accesos = {}
def agregar_info_accesos(domain, posiciones, ttl=float('Inf')):
    info_accesos[domain] = info_accesos_entry(posiciones, ttl)

def esta_local(domain):
    if domain in info_accesos:
        if not info_accesos[domain].sirve():
            limpiar_dominios(info_accesos[domain].get_posiciones_in_dominios())
            del info_accesos[domain]
            return False
        else:
            return True
    return False

def limpiar_dominios(posiciones):
    for posicion in posiciones:
        del domains[posicion]

agregar_info_accesos('localhost', [1])
agregar_info_accesos('www.fi.uba.ar', [2])

# Create a handler for our read (GET) people
def obtener_custom_domains(q = ''):
    """
    Esta funcion maneja el request GET /api/custom_domains/
     :q query:  Dominio a buscar en la lista de domains
    :return:        200 lista ordenada alfabeticamente de domains si q es vacio, 200 los resultados
    """
    # Create the list custom domains
    custom_domains_list = []
    for item in domains.values():
        if item['custom'] == 'true':
            custom_domains_list.append(item)
    
    if not q:
        custom_domains = {}
        custom_domains['items'] = custom_domains_list
        return custom_domains

    dup = False
    custom_domains = {}
    filtered_custom_domains = []
    for dominio_existente in custom_domains_list:
        dup = q == dominio_existente.get('domain')
        if dup: 
            filtered_custom_domains.append(dominio_existente)
    custom_domains['items'] = filtered_custom_domains
    return make_response(custom_domains, 200)
	
def crear(**kwargs):
    """
    Esta funcion maneja el request POST /api/custom_domains/

     :domain body:  Dominio a crear en la lista de domains
    :return:        201 dominio creado, 400 faltan datos para crear el dominio, 401 dominio o ip existentes
    """
    custdom = kwargs.get('body')
    ip = custdom.get('ip')
    domain = custdom.get('domain')
    if not ip or not domain:
        return make_response(jsonify({"error":'custom domain already exists'}),400)

    dup = False
    for dominio_existente in domains.values():
        dup = ip == dominio_existente.get('ip') or domain == dominio_existente.get('domain')
        if dup: break

    if dup:
        return make_response(jsonify({"error":'custom domain already exists'}),400)

    new_id = max(domains.keys()) + 1
    custdom['custom'] = 'true'
    domains[new_id] = custdom

    return make_response(custdom, 201)
	
def modificar(**kwargs):
    """
    Esta funcion maneja el request PUT /api/custom_domains/

     :domain body:  Nombre de dominio a modificar en la lista de domains
    :return:        200 dominio modificado, 400 faltan datos para modificar el dominio, 404 domain not found
    """
    custdom = kwargs.get('body')
    ip = custdom.get('ip')
    domain = custdom.get('domain')
    if not ip or not domain:
        return make_response(jsonify({'error':'payload is invalid'}), 400)

    dup = False
    for dominio_existente in domains.values():
        dup = domain == dominio_existente.get('domain')
        if dup:
            dominio_existente['ip'] = ip
            dominio_existente['domain'] = domain
            dominio_existente['custom'] = 'true'
            return make_response(dominio_existente, 200)

    return make_response(jsonify({'error':'domain not found'}), 404)

def borrar(domain):
    """
    Esta funcion maneja el request DELETE /api/custom_domains/{domain}

    :domain path:  nombre del dominio que se quiere borrar
    :return:        200 dominio, 404 domain not found
    """
    if not domain:
        return abort(400, 'Faltan datos para buscar el dominio')

    dup = False
    i = 1
    for dominio_existente in domains.values():
        dup = domain == dominio_existente.get('domain')
        if dup: 
            del domains[i]
            return make_response(dominio_existente, 200)
        i = i + 1
    return abort(404, 'domain not found')

def obtener_dominio(domain):
    """
    Esta funcion maneja el request GET /api/domains/<domain>

    :domain path:  nombre del dominio que se quiere obtener 
    :return:        200 dominio, 404 domain not found
    """
    print("recibi requesta para " + domain)
    try:
        if not esta_local(domain):
            print("no encontrado localmente. Resolviendo consulta hacia afuera")
            result = dns.resolver.query(domain)
            ttl = result.ttl
            posiciones = []
            for ip in result:
                posiciones.append(guardar_dominio(domain, str(ip)))
            print("info posiciones a agregar " + str(posiciones))
            agregar_info_accesos(domain, posiciones, ttl)
            print(domains)
        return (domains[info_accesos[domain].posicion_a_acceder()])
    except dns.resolver.NXDOMAIN:
        return make_response(jsonify({'error':'Not Found'}), 404)
