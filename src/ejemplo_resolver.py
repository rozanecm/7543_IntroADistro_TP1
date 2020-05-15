import dns.resolver

# Resolve www.yahoo.com
result = dns.resolver.query('www.yahoo.com')
result = dns.resolver.query('yahoo.com')

# Para obtener todo el RR, necesito esto:
for answer in result.response.answer:
    print(answer)

# Para obtener solamente la ip, necesito esto:
for answer in result:
    print(answer)
