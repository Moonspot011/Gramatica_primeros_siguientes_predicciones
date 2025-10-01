# Algoritmos de Primeros, Siguientes y Predicciones en Python

Este proyecto implementa en Python los algoritmos clásicos de análisis sintáctico para calcular los conjuntos **Primeros**, **Siguientes** y las **Predicciones** de una gramática libre de contexto.

---

## Archivos principales

- `algoritmos.py` → contiene la implementación de las clases y métodos.
- `gram.txt` → archivo de texto con la gramática a analizar.

---

## Formato del archivo `gram.txt`

Cada producción debe escribirse en **una sola línea**.  
- Ejemplo:
  ```bash
  A -> a B C
  B -> b bas
  B -> big C boss
  C -> ε
  C -> c
## Importante:
- Usa `ε` (la letra épsilon) para indicar la **cadena vacía**.
- No uses `|` en las reglas. Si un no terminal tiene varias producciones, escríbelas en líneas separadas.

---

## 📌 Ejecución

1. Coloca la gramática en `gram.txt`.
2. Ejecuta el programa:
   ```bash
    python3 algoritmos.py


## Ejemplo de salida

- Con el gram.txt de ejemplo:
  ```bash
  A -> a B C
  B -> b bas
  B -> big C boss
  C -> ε
  C -> c

- La ejecución produce
  ```bash
  Primeros:
  A: {'a'}
  B: {'b', 'big'}
  C: {'c', 'ε'}
  
  Siguientes:
  A: {'$'}
  B: {'c', '$'}
  C: {'boss', '$'}
  
  Predicciones:
  B -> b bas: {'b'}
  B -> big C boss: {'big'}
  A -> a B C: {'a'}
  C -> ε: {'boss', '$'}
  C -> c: {'c'}

## Funcionalidad

Primeros: símbolos que pueden aparecer al inicio de cada no terminal.

Siguientes: símbolos que pueden aparecer inmediatamente después de cada no terminal.

Predicciones: conjunto de símbolos de entrada con los que se elige cada producción (útil para parsers LL(1)).

Requisitos

- Python 3.7 o superior.

