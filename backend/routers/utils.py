import re


def check_if_language_is_regular(language, p=2):
    if "," in language and "..." not in language:
        return handle_finite_languages(language)
    elif "..." in language:
        return handle_extension_languages(language, p)
    elif "^n" in language:
        return handle_compression_languages(language, p)


def generate_valid_strings(language_pattern):
    locate = language_pattern.find("^")
    base_before = language_pattern[:locate]
    base_after = language_pattern[locate+1:]
    valid_strings = []
    for i in range(1, 6):
        valid_strings.append(base_before*i + base_after*i)
    return valid_strings



# def handle_finite_languages(language):
#     """
#     El lenguaje es finito, así que es regular automáticamente.
#     """
#     print("Lenguaje finito. Es regular automáticamente.")
#     return True


# def handle_extension_languages(language, p):
#     """
#     El lenguaje es por extensión. Evaluar si las cadenas cumplen con el lema de bombeo.
#     """
#     # Limpiar la entrada eliminando '...' y separar las cadenas
#     strings = language.replace("...", "").split(",")

#     # Evaluar el lema de bombeo para cada cadena
#     print("Evaluando lenguaje por extensión:")
#     for s in strings:
#         print(f"Evaluando cadena: {s}")
#         if not check_pumping_lemma(s, p):
#             print(
#                 f"La cadena '{s}' no cumple el lema de bombeo, el lenguaje no es regular."
#             )
#             return False
#     print("Todas las cadenas cumplen con el lema de bombeo, el lenguaje es regular.")
#     return True


# def handle_compression_languages(language, p):
#     """
#     El lenguaje es por compresión. Generar algunas cadenas y evaluarlas con el lema de bombeo.
#     """
#     print(f"Generando cadenas para el lenguaje de compresión: {language}")

#     # Aquí debes generar algunas cadenas a partir del patrón. Ejemplo para 'a^n', generar 'a', 'aa', 'aaa', etc.
#     # Aquí es necesario implementar una forma de generar cadenas según el patrón dado.
#     generated_strings = generate_strings_from_pattern(language)

#     # Evaluar cada cadena generada con el lema de bombeo
#     print("Evaluando lenguaje por compresión:")
#     for s in generated_strings:
#         print(f"Evaluando cadena generada: {s}")
#         if not check_pumping_lemma(s, p):
#             print(
#                 f"La cadena '{s}' no cumple el lema de bombeo, el lenguaje no es regular."
#             )
#             return False
#     print(
#         "Todas las cadenas generadas cumplen con el lema de bombeo, el lenguaje es regular."
#     )
#     return True


# def check_pumping_lemma(w, p):
#     """
#     Verificar si la cadena w cumple con el lema de bombeo.
#     w es la cadena a verificar y p es el número de bombeo.
#     """
#     n = len(w)

#     # Verificar si la longitud de la cadena es mayor o igual a p
#     if n < p:
#         print(
#             f"Cadena '{w}' es demasiado corta para aplicar el lema de bombeo (longitud {n} < {p})."
#         )
#         return True  # Si la cadena es corta, no necesitamos bombear

#     # Intentar dividir la cadena en tres partes: x, y, z
#     for i in range(1, n):  # Buscar un punto en el que dividir la cadena
#         x = w[:i]
#         for j in range(i+1, n):  # Buscar otro punto de corte
#             y = w[i:j]
#             z = w[j:]

#             if len(y) > 0:  # Solo proceder si y no es vacía
#                 print(f"División de '{w}': x = '{x}', y = '{y}', z = '{z}'")
#                 break
#         if len(y) > 0:  # Si encontramos una división válida, salimos del bucle
#             break
#     else:
#         # Si no encontramos una división válida
#         print(f"Cadena '{w}' no se puede dividir adecuadamente (y está vacío).")
#         return False

#     # Aplicar el bombeo y verificar si la cadena resultante sigue en el lenguaje
#     for i in range(1, 4):  # Probar con bombear de 1 a 3 veces
#         pumped_string = x + y * i + z
#         print(f"Bombear {i} veces: {pumped_string}")
#         # Verificar si la cadena bombeada sigue en el lenguaje
#         if not is_in_language(pumped_string):
#             print(f"Cadena '{pumped_string}' NO está en el lenguaje.")
#             return False  # Si alguna cadena bombeada no está en el lenguaje, no es regular

#     return True


# def is_in_language(w):
#     """
#     Verifica si una cadena w pertenece al lenguaje definido por extensión.
#     """
#     # Aquí puedes definir la función que verifica si una cadena pertenece al lenguaje dado.
#     # Para este ejemplo, asumimos que las cadenas con 'a^n' o 'a+b+' son aceptadas.
#     # Por ejemplo, lenguaje de solo a's: 'a+', lenguaje de ab's: 'a+b+'

#     # Usaremos expresiones regulares para ver si la cadena sigue el patrón regular
#     if re.match(r"^a+$", w):  # Solo una o más 'a's
#         return True
#     if re.match(r"^ab+$", w):  # 'a' seguido de una o más 'b's
#         return True

#     return False


# def generate_strings_from_pattern(language):
#     """
#     Genera una lista de cadenas a partir del patrón de compresión dado en el lenguaje.
#     """
#     # Este es un ejemplo simple para 'a^n', se podrían generar cadenas como: 'a', 'aa', 'aaa', etc.
#     # Dependiendo de la forma del patrón, debes adaptar esta función.

#     # Aquí estamos generando algunas cadenas para un lenguaje simple de 'a^n'
#     if "^n" in language:
#         return ["a", "aa", "aaa"]
#     elif "ab^n" in language:
#         return ["ab", "abb", "abbb"]
#     else:
#         return []


if __name__ == "__main__":
    # Generar cadenas válidas para el lenguaje 0^n1^n
    valid_strings_01 = generate_valid_strings("0^1", max_n=5)
    print("Cadenas válidas para el lenguaje 0^n1^n:")
    for s in valid_strings_01:
        print(s)

    # Puedes usar esta misma función para otros lenguajes con la forma a^n b^n, como 'a^n b^n'
    valid_strings_ab = generate_valid_strings("a^b", max_n=5)
    print("\nCadenas válidas para el lenguaje a^n b^n:")
    for s in valid_strings_ab:
        print(s)
