import dns.resolver

# Resolve www.yahoo.com
# result = dns.resolver.query('www.yahoo.com')
# result = dns.resolver.query('yahoo.com')
urls = ['yahoo.com', 'google.com', 'stackoverflow.com', 'wolframalpha.com', 'lanacion.com', 'infobae.com', 'casarosada.org']

for url in urls:
    print("current url:", url)
    result = dns.resolver.query(url)
    print("obteniendo RRs enteros")
    # Para obtener todo el RR, necesito esto:
    for answer in result.response.answer:
        print(answer)

    print("obteniendo solo IPs")
    # Para obtener solamente la ip, necesito esto:
    for answer in result:
        print(answer)

    print("obteniendo solo TTLs")
    # Para obtener solamente la ip, necesito esto:
    print(result.ttl)
