from datetime import datetime

class info_accesos_entry:
    def __init__(self, posiciones, ttl):
        self.posicion_en_dominios_DS = posiciones
        self.indice_posicion_a_acceder = 0

        self.ttl = ttl
        self.timestamp_of_retrieval = datetime.now()

    def posicion_a_acceder(self):
        return_value = self.posicion_en_dominios_DS[self.indice_posicion_a_acceder]
        if self.indice_posicion_a_acceder == len(self.posicion_en_dominios_DS) - 1:
            self.indice_posicion_a_acceder = 0
        else:
            self.indice_posicion_a_acceder += 1
        return return_value

    def sirve(self):
        print("chequeando si sirve. Pasaron", (datetime.now() - self.timestamp_of_retrieval).total_seconds(), " - TTL:", self.ttl)
        return ((datetime.now() - self.timestamp_of_retrieval).total_seconds()) < self.ttl
    
    def get_posiciones_in_dominios(self):
        return self.posicion_en_dominios_DS
