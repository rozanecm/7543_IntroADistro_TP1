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

# Create a handler for our read (GET) people
def obtener_custom_domains(q = ''):
    """
    Esta funcion maneja el request GET /api/custom_domains/
     :q query:  Dominio a buscar en la lista de domains
    :return:        200 lista ordenada alfabeticamente de domains si q es vacio, 200 los resultados
    """
    # Create the list of people from our data
    if not q:
        return sorted(domains.values(), key=lambda domain: domain.get('domain'))

    dup = False
    for dominio_existente in domains.values():
        dup = q == dominio_existente.get('domain')
        if dup: 
            return make_response(dominio_existente, 200)
    return make_response('', 200)
	
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
        return abort(400, 'Faltan datos para modificar el dominio custom')

    dup = False
    i = 0
    for dominio_existente in domains.values():
        dup = ip == dominio_existente.get('ip') or domain == dominio_existente.get('domain')
        if dup:
            dominio_existente['ip'] = ip
            dominio_existente['domain'] = domain
            return make_response(custdom, 200)
        i = i + 1

    return abort(404, 'Domain not found')

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

    result = dns.resolver.query(domain)
    for answer in result.response.answer:
        print(answer)
