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
def obtener_custom_domains():
    """
    Esta funcion maneja el request GET /api/domains

    :return:        200 lista ordenada alfabeticamente de domains de la materia
    """
    # Create the list of people from our data
    return sorted(domains.values(), key=lambda domain: domain.get('domain'))

def obtener_uno(id_alumno):
    """
    Esta funcion maneja el request GET /api/domains/{id_alumno}

     :id_alumno body:  id del alumno que se quiere obtener
    :return:        200 alumno, 404 alumno no encontrado
    """
    if id_alumno not in domains:
        return abort(404, 'El alumno no fue encontrado')

    return domains.get(id_alumno)

def crear(**kwargs):
    """
    Esta funcion maneja el request POST /api/domains

     :param body:  custdom a crear en la lista de domains
    :return:        201 custdom creado, 400 ip o custom duplicado
    """
    custdom = kwargs.get('body')
    ip = custdom.get('ip')
    domain = custdom.get('domain')
    if not ip or not domain:
        return abort(400, 'Faltan datos para crear un custdom')

    dup = False
    for alumno_existente in domains.values():
        dup = ip == alumno_existente.get('ip') or domain == alumno_existente.get('domain')
        if dup: break

    if dup:
        return abort(400, 'ip o domain ya existentes')

    new_id = max(domains.keys()) + 1
	custdom['custom'] = True
    domains[new_id] = custdom

    return make_response(custdom, 201)

def borrar(id_alumno):
    """
    Esta funcion maneja el request DELETE /api/domains/{id_alumno}

    :id_alumno body:  id del alumno que se quiere borrar
    :return:        200 alumno, 404 alumno no encontrado
    """
    if id_alumno not in domains:
        return abort(404, 'El alumno no fue encontrado')

    del domains[id_alumno]

    return make_response('', 204)
