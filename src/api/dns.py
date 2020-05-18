import dns.resolver
from flask import abort, make_response

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
        return abort(400, 'Faltan datos para crear el dominio custom')

    dup = False
    for dominio_existente in domains.values():
        dup = ip == dominio_existente.get('ip') or domain == dominio_existente.get('domain')
        if dup: break

    if dup:
        return abort(401, 'ip o domain ya existentes')

    new_id = max(domains.keys()) + 1
    custdom['custom'] = True
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
