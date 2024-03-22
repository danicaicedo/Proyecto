class Socio:
    def __init__(self, cedula, nombre, tipo_suscripcion):
        self.cedula = cedula
        self.nombre = nombre
        self.fondos_disponibles = 0
        self.tipo_suscripcion = tipo_suscripcion
        self.facturas_sin_pagar = []
        self.personas_autorizadas = []

    def agregar_fondos(self, monto):
        if self.tipo_suscripcion == 'VIP':
            max_fondos = 5000000
        else:
            max_fondos = 1000000
        self.fondos_disponibles = min(self.fondos_disponibles + monto, max_fondos)

    def generar_factura(self, concepto, valor, nombre_generador):
        if valor <= self.fondos_disponibles:
            self.facturas_sin_pagar.append({'concepto': concepto, 'valor': valor, 'generador': nombre_generador})
            self.fondos_disponibles -= valor
            return True
        else:
            return False

    def pagar_factura(self, indice_factura):
        if 0 <= indice_factura < len(self.facturas_sin_pagar):
            factura = self.facturas_sin_pagar.pop(indice_factura)
            self.fondos_disponibles += factura['valor']
            return True
        else:
            return False

    def agregar_persona_autorizada(self, persona_autorizada):
        if persona_autorizada not in self.personas_autorizadas:
            self.personas_autorizadas.append(persona_autorizada)
            print(f"Persona autorizada '{persona_autorizada}' registrada correctamente para el socio '{self.nombre}'")
        else:
            print(f"La persona autorizada '{persona_autorizada}' ya está registrada para el socio '{self.nombre}'")

    def eliminar_persona_autorizada(self, persona_autorizada):
        if persona_autorizada not in self.personas_autorizadas:
            print(f"La persona autorizada '{persona_autorizada}' no está registrada para el socio '{self.nombre}'")
            return False
        for factura in self.facturas_sin_pagar:
            if factura['generador'] == persona_autorizada:
                print(f"No se puede eliminar la persona autorizada '{persona_autorizada}', tiene facturas pendientes.")
                return False
        self.personas_autorizadas.remove(persona_autorizada)
        print(f"Persona autorizada '{persona_autorizada}' eliminada correctamente para el socio '{self.nombre}'")
        return True


class ClubSocial:
    def __init__(self):
        self.socios = []
        self.socios_vip = 0

    def afiliar_socio(self):
        cedula = input("Ingrese la cédula del socio: ")
        nombre = input("Ingrese el nombre del socio: ")
        tipo_suscripcion = input("Ingrese el tipo de suscripción (VIP o Regular): ").upper()
        if tipo_suscripcion not in ['VIP', 'REGULAR']:
            print("Tipo de suscripción inválido. Debe ser VIP o Regular.")
            return False
        
        if tipo_suscripcion == 'VIP' and self.socios_vip >= 3:
            print("No se pueden afiliar más socios VIP.")
            return False
        
        for socio in self.socios:
            if socio.cedula == cedula:
                print("Ya existe un socio con esta cédula.")
                return False
        
        nuevo_socio = Socio(cedula, nombre, tipo_suscripcion)
        if tipo_suscripcion == 'VIP':
            self.socios_vip += 1
        
        nuevo_socio.agregar_fondos(100000 if tipo_suscripcion == 'VIP' else 50000)
        self.socios.append(nuevo_socio)
        print(f"Socio '{nombre}' afiliado correctamente.")
        return True

    def registrar_persona_autorizada(self):
        cedula_socio = input("Ingrese la cédula del socio al que desea registrar una persona autorizada: ")
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                persona_autorizada = input("Ingrese el nombre de la persona autorizada: ")
                socio.agregar_persona_autorizada(persona_autorizada)
                return True
        print("No se encontró ningún socio con esa cédula.")
        return False

    def pagar_factura(self):
        cedula_socio = input("Ingrese la cédula del socio que va a pagar la factura: ")
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                indice_factura = int(input("Ingrese el índice de la factura a pagar: "))
                if socio.pagar_factura(indice_factura):
                    print("Factura pagada correctamente.")
                    return True
                else:
                    print("Índice de factura inválido o fondos insuficientes.")
                    return False
        print("No se encontró ningún socio con esa cédula.")
        return False

    def registrar_consumo(self):
        cedula_socio = input("Ingrese la cédula del socio que realiza el consumo: ")
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                concepto = input("Ingrese el concepto del consumo: ")
                valor = float(input("Ingrese el valor del consumo: "))
                nombre_generador = input("Ingrese el nombre del generador del consumo: ")
                if socio.generar_factura(concepto, valor, nombre_generador):
                    print("Consumo registrado correctamente.")
                    return True
                else:
                    print("Fondos insuficientes para registrar el consumo.")
                    return False
        print("No se encontró ningún socio con esa cédula.")
        return False

    def aumentar_fondos_socio(self):
        cedula_socio = input("Ingrese la cédula del socio al que desea aumentar los fondos: ")
        for socio in self.socios:
            if socio.cedula == cedula_socio:
                monto = float(input("Ingrese el monto a agregar: "))
                socio.agregar_fondos(monto)
                print("Fondos agregados correctamente.")
                return True
        print("No se encontró ningún socio con esa cédula.")
        return False


class MenuClubSocial:
    def __init__(self):
        self.club = ClubSocial()

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Club Social ---")
            print("1. Afiliar un socio")
            print("2. Registrar una persona autorizada")
            print("3. Pagar una factura")
            print("4. Registrar un consumo")
            print("5. Aumentar fondos de un socio")
            print("6. Salir")

            opcion = input("Ingrese el número de la opción que desea realizar: ")

            if opcion == '1':
                self.club.afiliar_socio()
            elif opcion == '2':
                self.club.registrar_persona_autorizada()
            elif opcion == '3':
                self.club.pagar_factura()
            elif opcion == '4':
                self.club.registrar_consumo()
            elif opcion == '5':
                self.club.aumentar_fondos_socio()
            elif opcion == '6':
                print("Saliendo del programa...")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

# Ejemplo de uso:
menu = MenuClubSocial()
menu.mostrar_menu()

