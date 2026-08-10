from App import App

def main():
    """
    Funcion principal que crea la aplicacion y la pone a correr. Si el usuario
    interrumpe el programa con Ctrl+C se cierra con un mensaje en lugar de
    mostrar un error.
    """
    app = App()
    try:
        app.iniciar()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario. Hasta luego.")

main()
