import requests
from github import Github, Auth
from github.GithubException import GithubException
import os
import csv
import sys
import json

def Auth_GitHub(Token):
    try:
        print("---------------------- Autenticacion usuario de la organización GitHub --------------------------------------")
        auth = Auth.Token(Token)
        g = Github(auth=auth)

        print(f"Autenticando con el token proporcionado...")
        user_auth = g.get_user()
        print(f"Autenticado exitosamente como: {user_auth.login}")
        print("--------------------------------------------------------------------------------------------------------------")
        return g
    except GithubException as e:
        print(f"Error: {e.data.get('message', e)}")
        print("--------------------------------------------------------------------------------------------------------------")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado durante la autenticación o al acceder a la organización: {e}.")
        print("--------------------------------------------------------------------------------------------------------------")
        sys.exit(1)

def Read_CSV(CSV_FILE_PATH):
    try:
        #Se lee el contenido del archivo CSV con los usuarios a los que se les creara el repositorio GitHub a partir de la plantilla
        print("----------------------------- Leyendo Archivo CSV con los estudiantes ---------------------------------------")
        with open(CSV_FILE_PATH,mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            required_columns = {'org_name', 'username', 'template_repo'}

            #Se valida que el archivo CSV contenga las columnas requeridas
            if not required_columns.issubset(reader.fieldnames):
                print(f"Error: El archivo CSV debe contener las columnas 'org_name', 'username' y 'template_repo'.")
                sys.exit(1)
            else:
                print(f"Archivo CSV '{CSV_FILE_PATH}' leído correctamente.")
                rows = list(reader)
                print(f"Cantidades de repositorios leídos: {len(rows)}")  
                print(f"Repositorios a crear:")

                #Recorrer la lista de repositorios leídos del archivo CSV
                for row in rows:
                    print(f"Organización: {row['org_name']}, Usuario: {row['username']}, Repositorio Plantilla: {row['template_repo']}")

                #Creación del archivo json con los repositorios leídos del archivo CSV
                with open("datos.json","w",encoding="utf-8") as archivo:
                    json.dump(rows,archivo,indent=4, ensure_ascii=False)
                print("--------------------------------------------------------------------------------------------------------------")
            return json.dumps(rows)
    except FileNotFoundError:
        print(f"Error: El archivo CSV '{CSV_FILE_PATH}' no se encontró.\n")
        print("--------------------------------------------------------------------------------------------------------------")
        sys.exit(1)

def Close_Conn_GitHub(g):
    try:
        g.close()
        print("Conexión con GitHub cerrada correctamente.")
        print("--------------------------------------------------------------------------------------------------------------")
    except Exception as e:
        print(f"Error al cerrar la conexión con GitHub: {e}")
        print("--------------------------------------------------------------------------------------------------------------")

def Process_Repo_GitHub(g):
    #Recorrido por los registros leídos del archivo CSV
    print("------------------------- Procesamiento repositorios de los estudiantes --------------------------------------")

    registros = Read_JSON("datos.json")
    for registro in registros:
        org_target = registro["org_name"]
        user_target = registro["username"]
        template_repo_name = registro["template_repo"]
        new_repo_name = f"{org_target}-{user_target}"

        print(f"Procesando repositorio: {user_target}")
        """print(f"Usuario    : {user_target}")
        print(f"Organización  : {org_target}")
        print(f"Template      : {template_repo_name}")"""
        print(f"Nuevo repo    : {new_repo_name}")

        try:
            #Accediendo a la organización donde se crearan los repositorios de los estudiantes
            print("------------------------- Accediendo a la organización de los repositorios -----------------------------------")
            org = Login_Organization(org_target, g)

            #Buscando el repositorio plantilla que se utilizará para crear los repositorios de los estudiantes
            print("------------------------- Buscando el repositorio plantilla en la organización -------------------------------")
            template_repo_name = Search_Template_Repo_Name(template_repo_name,g)

            #Validar - Revisar Bloque Codigo
            """try:
                #Se valida si el repositorio, ya existe. Si existe, no se crea y se continua con el proceso.
                print("-------------- Validando si el repositorio del estudiante ya existe en la organización -----------------------")
                existing_repo = org.get_repo(new_repo_name)
                print(f"El repositorio {new_repo_name} ya existe")
                #Validate_to_Exist_Repo_Name(org,new_repo_name)
                #continue
            except GithubException as e:
                if e.status != 404:
                    print(f"El repositorio '{new_repo_name}' no existe. Puede ser creado.")"""

            #Creando el repositorio para cada uno de los estudiantes en el archivo CSV
            print("------------------------------ Creando repositorio del estudiante --------------------------------------------")
            print(f"Creando un nuevo repositorio '{new_repo_name}' desde la plantilla '{template_repo_name}'...")
            description = f"Repositorio creado para las simulaciones realizadas por {user_target}"
            repo = Create_Repo_to_Template(org,new_repo_name,template_repo_name,True,description)

            #Añadir al alumno como colaborador con permisos de escritura
            print("------------------ Asignando permisos de escritura al repositorio del estudiante -----------------------------")
            print(f"Añadiendo a {user_target} como colaborador...")
            AddColaboratorRepo(repo,user_target,"push")

        except GithubException as e:
            message = (
            e.data.get("message",str(e))
            if isinstance(e.data, dict) else str(e))
            print(f"Error: Error GitHub con el usuario {user_target}: {message}")
            Bitacora_Errores(user_target,new_repo_name,message,e)
            continue

        print("Proceso Finalizado")
        print("--------------------------------------------------------------------------------------------------------------")

def Read_JSON(path_json):
    with open(path_json,"r",encoding="UTF-8") as archivo:
        return json.load(archivo)

def Login_Organization(org_target, g):
    org = g.get_organization(org_target)
    print(f"Organización encontrada: {org.login}")
    return org

def Search_Template_Repo_Name(template_repo_name, g):
    template_repo_name = g.get_repo(template_repo_name)
    print(f"Repositorio de plantilla encontrado '{template_repo_name}'")
    return template_repo_name

def Validate_to_Exist_Repo_Name(org, new_repo_name):
    existing_repo = org.get_repo(new_repo_name)
    print(f"El repositorio {new_repo_name} ya existe")
    return existing_repo

def Create_Repo_to_Template(org, name,repo,private, description):
    repo = org.create_repo_from_template(
                     name = name,
                    repo = repo,
                    private = private,
                    description = description,
                )

    #Se imprime el repositorio creado junto con la URL
    print(f"Repositorio creado desde la plantilla: '{name}' con la URL: {repo.html_url}")
    return repo

def AddColaboratorRepo(repo, user_target, permission="push"):
    repo.add_to_collaborators(user_target, permission)
    print(f"Permiso agregado correctamente con el usuario: {user_target}.")

def Bitacora_Errores(user_target, new_repo_name, mensaje, e):
    archivo_errores = "error_create_repo.json"
    datos_errores = []
    if os.path.exists(archivo_errores) and os.path.getsize(archivo_errores) > 0:
        with open ("error_create_repo.json", "r", encoding="UTF-8") as archivo:
            datos_errores = json.load(archivo)

    datos_errores.append({
        "Usuario_Repo": user_target,
        "Repositorio": new_repo_name,
        "Mensaje": f"Error: Error GitHub con el usuario {user_target}: {mensaje}",
        "Detalle GitHub": e.data}
        )
    with open("error_create_repo.json","w",encoding="utf-8") as archivo:
            json.dump(datos_errores,archivo,indent=4, ensure_ascii=False)

class RepositorioGitHubManager:
    Token = os.getenv("Github_token")
    CSV_FILE_PATH = "data.csv"
    Read_CSV(CSV_FILE_PATH)
    g = Auth_GitHub(Token)

    Process_Repo_GitHub(g)
    
    Close_Conn_GitHub(g)