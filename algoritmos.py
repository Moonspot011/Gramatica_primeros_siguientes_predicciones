from collections import defaultdict

class Gramatica:
    def __init__(self, archivo):
        self.producciones = defaultdict(list)
        self.no_terminales = set()
        self.terminales = set ()
        self.inicial = None
        self.leer_gramatica(archivo)
        self.primeros = {}
        self.siguientes = {}
        
    def leer_gramatica(self, archivo):
        with open(archivo, 'r') as f:
            for linea in f:
                if '->' in linea:
                    izquierda, derecha = linea.strip().split('->')
                    izquierda = izquierda.strip()
                    produccion = derecha.strip().split()
                    self.producciones[izquierda].append(produccion)
                    self.no_terminales.add(izquierda)
        
        # detectar terminales            
        for noter, reglas in self.producciones.items():
            for regla in reglas:
                for simbolo in regla:
                    if simbolo != "ε" and simbolo not in self.no_terminales:
                        self.terminales.add(simbolo)
                        
    def calcular_primeros(self):
        self.primeros = {noter: set() for noter in self.no_terminales}
        cambio = True
        while cambio:
            cambio = False
            for noter in self.no_terminales:
                for regla in self.producciones[noter]:
                    for simbolo in regla:
                        if simbolo in self.terminales or simbolo == "ε":
                            if simbolo not in self.primeros[noter]:
                                self.primeros[noter].add(simbolo)
                                cambio = True
                            break
                        else:
                            nuevos = self.primeros[simbolo] - {"ε"}
                            # verifica si hay un simbolo nuevo en los primeros
                            if not nuevos.issubset(self.primeros[noter]):
                                self.primeros[noter] |= nuevos
                                cambio = True
                            if "ε" not in self.primeros[simbolo]:
                                break
                    else:
                        if "ε" not in self.primeros[noter]:
                            self.primeros[noter].add("ε")
                            cambio = True
        return self.primeros
    
    def calcular_siguientes(self, inicial = None):
        if inicial is None:
            inicial = self.inicial
        self.siguientes = {noter: set() for noter in self.no_terminales}
        if inicial is None:
            raise ValueError("No se encontró símbolo inicial. Asegura que gram.txt tenga al menos una producción.")
        self.siguientes[inicial].add("$")
        cambio = True
        while cambio:
            cambio = False
            for noter in self.no_terminales:
                for regla in self.producciones[noter]:
                    for i, simbolo in enumerate(regla):
                        if simbolo in self.no_terminales:
                            siguiente = regla[i+1:] if i+1 < len(regla) else []
                            if siguiente:
                                primeros_siguiente = self.primeros_secuencia(siguiente)
                                nuevos = primeros_siguiente - {"ε"}
                                if not nuevos.issubset(self.siguientes[simbolo]):
                                    self.siguientes[simbolo] |= nuevos
                                    cambio = True
                                if "ε" in primeros_siguiente:
                                    if not self.siguientes[noter].issubset(self.siguientes[simbolo]):
                                        self.siguientes[simbolo] |= self.siguientes[noter]
                                        cambio = True
                            else:
                                if not self.siguientes[noter].issubset(self.siguientes[simbolo]):
                                    self.siguientes[simbolo] |= self.siguientes[noter]
                                    cambio = True
        return self.siguientes
    
    def primeros_secuencia(self, secuencia):
        resultado = set()
        for simbolo in secuencia:
            if simbolo == "ε":
                resultado.add("ε")
                return resultado
            elif simbolo in self.terminales:
                resultado.add(simbolo)
                return resultado
            else:  # es un no terminal
                resultado |= self.primeros[simbolo] - {"ε"}
                if "ε" not in self.primeros[simbolo]:
                    return resultado
        resultado.add("ε")
        return resultado
    
    def calcular_prediccion(self):
        predicciones = {}
        for noter in self.no_terminales:
            for regla in self.producciones[noter]:
                primera = self.primeros_secuencia(regla)
                if "ε" in primera:
                    predicciones[(noter, tuple(regla))] = (primera - {"ε"}) | self.siguientes[noter]
                else:
                    predicciones[(noter, tuple(regla))] = primera
        return predicciones
                
if __name__ == "__main__":
    g = Gramatica("gram.txt")
    primeros = g.calcular_primeros()
    siguientes = g.calcular_siguientes(inicial=list(g.no_terminales)[0])
    predicciones = g.calcular_prediccion()
    
    print("Primeros:")
    for noter, primeros in primeros.items():
        print(f"{noter}: {primeros}")
    
    print("\nSiguientes:")
    for noter, siguientes in siguientes.items():
        print(f"{noter}: {siguientes}")
    
    print("\nPredicciones:")
    for(noter, regla), predi in predicciones.items():
        print(f"{noter} -> {' '.join(regla)}: {predi}")
    
                    
                                