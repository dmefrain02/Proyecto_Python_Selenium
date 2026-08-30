import requests
from github import Github, Auth
from github.GithubException import GithubException
import os
import csv
import sys

CSV_FILE_PATH = "data.csv"
# El token debe existir como variable de entorno
Token = os.getenv("Github_token")

#Se valida que exista la variable de entorno creada con el token de GitHub
if not Token:
    print(f"Error: La variable de entorno 'Github_token' no se encuentra definida. Asegurate de haber configurado la variable de entorno correctamente.\n")
    sys.exit(1)

try: 
    #Se realiza autenticacion con el usuario GitHub
    auth = Auth.Token(Token)
    g = Github(auth=auth)

    print(f"Autenticando con el token proporcionado...")
    user_auth = g.get_user()
    print(f"Autenticado exitosamente como: {user_auth.login}\n")
except GithubException as e:
    print(f"Error: {e.data.get('message', e)}\n") 
    sys.exit(1)    
except Exception as e:
    print(f"Error inesperado durante la autenticación o al acceder a la organización: {e}.\n")
    sys.exit(1)

try:
    #Se lee el contenido del archivo CSV con los usuarios a los que se les creara el repositorio GitHub a partir de la plantilla
    with open(CSV_FILE_PATH,mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        required_columns = {'org_name', 'username', 'template_repo'}

        if not required_columns.issubset(reader.fieldnames):
            print(f"Error: El archivo CSV debe contener las columnas 'org_name', 'username' y 'template_repo.'.")
            sys.exit(1)
        else:
            print(f"Archivo CSV '{CSV_FILE_PATH}' leído correctamente.")
            rows = list(reader)
            print(f"Estudiantes encontrados en el CSV: {len(rows)}")  
            print(f"Contenido del CSV:")
            
            for row in rows:
                print(f"Organización: {row['org_name']}, Usuario: {row['username']}, Repositorio Plantilla: {row['template_repo']}\n")
except FileNotFoundError:
    print(f"Error: El archivo CSV '{CSV_FILE_PATH}' no se encontró.\n")
    sys.exit(1)

#Recorrido por los registros leídos del archivo CSV
for row in rows:
    org_target = row["org_name"].strip()
    user_target = row["username"].strip()
    template_repo_name = row["template_repo"].strip()
    new_repo_name = f"{org_target}-{user_target}"

    print(f"Procesando repositorio de estudiante: {user_target}\n")
    print(f"Usuario       : {user_target}")
    print(f"Organización  : {org_target}")
    print(f"Template      : {template_repo_name}")
    print(f"Nuevo repo    : {new_repo_name}")

    try:
        #Accediendo a la organización donde se crearan los repositorios de los estudiantes
        print("Accediendo a la organización...")
        org = g.get_organization(org_target)
        print(f"Organización encontrada: {org.login}")

        #Buscando el repositorio plantilla que se utilizará para crear los repositorios de los estudiantes
        print(f"Buscando repositorio plantilla '{template_repo_name}'...")
        template_repo_name = g.get_repo(template_repo_name)
        print(f"Repositorio de plantilla encontrado '{template_repo_name}'.\n")

        try:
            #Se valida si el repositorio, ya existe. Si existe, no se crea y se continua con el proceso.
            existing_repo = org.get_repo(new_repo_name)
            print(f"El repositorio {new_repo_name} ya existe")
            continue
        except GithubException as e:
            if e.status != 404:
                raise

        #Creando el repositorio para cada uno de los estudiantes en el archivo CSV
        print(f"Creando un nuevo repositorio '{new_repo_name}' desde la plantilla '{template_repo_name}'...")
        repo = org.create_repo_from_template(
            name = new_repo_name,
            repo = template_repo_name,
            private = True,
            description = f"Repositorio creado para simulaciones realizadas por {user_target}",
        )

        #Se imprime el repositorio creado junto con la URL
        print(f"Repositorio plantilla '{new_repo_name}' creado con éxito con la URL: {repo.html_url}\n")

        #Añadir al alumno como colaborador con permisos de escritura
        print(f"Añadiendo a {user_target} como colaborador...")
        repo.add_to_collaborators(user_target, permission="push")
        print(f"Permiso agregado correctamente con el usuario: {user_target}.\n")
    except GithubException as e:
        message = (
        e.data.get("message",str(e))
        if isinstance(e.data, dict) else str(e))

        print(f"Error: Error GitHub con el usuario {user_target}: {message}\n")
        sys.exit(1)
    except Exception as e:
        print(f"Error procesando a {user_target}:{e}\n")
        sys.exit(1)

print("Proceso Finalizado")
g.close()