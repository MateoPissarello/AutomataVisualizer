import re
from typing import List, Union

# Definimos un tipo para los lenguajes
Language = Union[List[str], List[str], str]


def generate_examples(language: Language, max_length: int = 5) -> List[str]:
    """
    Genera ejemplos de cadenas para un lenguaje dado.
    """
    examples = []

    if isinstance(language, list):
        # Caso 1: Lenguaje finito o definido por extensión
        examples = language[:max_length]
    elif isinstance(language, str):
        # Caso 2: Lenguaje por comprensión
        match = re.match(r"(.*)\^n(.*)\^n\s*:.*n\s*>=\s*1", language)
        if match:
            prefix, suffix = match.groups()
            for n in range(1, max_length + 1):
                examples.append(prefix * n + suffix * n)

    return examples


def pumping_lemma_check(string: str, p: int, language: Language) -> bool:
    """
    Verifica si una cadena cumple con el lema de bombeo.
    """
    n = len(string)
    if n < p:
        return True  # No aplica si la longitud es menor que p

    for i in range(1, p):
        x = string[:i]
        y = string[i : i + p]
        z = string[i + p :]

        if len(y) == 0:
            continue

        # Prueba de bombeo
        for k in range(0, 3):  # Prueba con diferentes repeticiones
            pumped = x + (y * k) + z
            if pumped not in generate_examples(language):
                return False

    return True


def check_language(language: Language, p: int = 5):
    """
    Verifica si un lenguaje es regular utilizando el lema de bombeo.
    """
    examples = generate_examples(language)
    results = []

    for example in examples:
        result = pumping_lemma_check(example, p, language)
        results.append((example, result))

    # Verificar si algún resultado es False
    is_regular = all(result for _, result in results)

    return results, is_regular


# Ejemplo de uso
if __name__ == "__main__":
    finite_language = ["abc", "cde", "acc"]
    extension_language = ["ab", "aabb", "aaabbb"]
    comprehension_language = "0^n1^n : n >= 1"

    # Calcular resultados
    finite_results, finite_is_regular = check_language(finite_language)
    extension_results, extension_is_regular = check_language(extension_language)
    comprehension_results, comprehension_is_regular = check_language(
        comprehension_language
    )

    # Imprimir resultados
    print("Resultados para lenguaje finito:", finite_results)
    print("¿Es regular?:", "Sí" if finite_is_regular else "No")

    print("Resultados para lenguaje por extensión:", extension_results)
    print("¿Es regular?:", "Sí" if extension_is_regular else "No")

    print("Resultados para lenguaje por compresión:", comprehension_results)
    print("¿Es regular?:", "Sí" if comprehension_is_regular else "No")
