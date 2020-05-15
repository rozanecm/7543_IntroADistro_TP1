class info_accesos_entry:
    def __init__(self, posiciones):
        self.posicion_en_dominios_DS = posiciones
        self.indice_posicion_a_acceder = 0

    def posicion_a_acceder(self):
        return_value = self.posicion_en_dominios_DS[self.indice_posicion_a_acceder]
        if self.indice_posicion_a_acceder == len(self.posicion_en_dominios_DS) - 1:
            self.indice_posicion_a_acceder = 0
        else:
            self.indice_posicion_a_acceder += 1
        return return_value
