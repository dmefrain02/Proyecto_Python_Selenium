import os
from github import Github, Auth
from github.GithubException import GithubException

def autentificacion_GitHub(Token):

    print("-" * 90)
    print("Autenticación usuario de la organización GitHub")
    print("-" * 90)

    if not Token:
        print("ERROR: Token no proporcionado.")
        return None

    try:
        # Limpiar espacios accidentales
        Token = Token.strip()

        print("Autenticando con el token proporcionado...")

        # Configuración de autenticación
        auth = Auth.Token(Token)

        # Crear cliente GitHub
        g = Github(auth=auth)

        # Forzar una petición real a la API
        usuario = g.get_user()
        print(f"Autenticación exitosa: {usuario.login}")

        return g

    except GithubException as error:

        print(f"Error HTTP: {error.status}")
        print(f"Detalle: {error.data}")

        return None

    except Exception as error:

        print(f"Error inesperado: {error}")

        return None


# Obtener variable de entorno
Token = os.getenv("Github_token")

# Ejecutar autenticación
github_client = autentificacion_GitHub(Token)

if github_client:
    print("Conexión establecida correctamente.")
else:
    print("No fue posible establecer conexión con GitHub.")