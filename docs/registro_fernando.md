Historial de trabajo realizado
1. Descripción inicial del proyecto
Pedí ayuda para definir TaskFlow CLI, un gestor de tareas en consola escrito en Python 3.12+. El proyecto debía crecer desde una carpeta vacía hasta convertirse en una aplicación completa con:

Modelos de datos

Persistencia en JSON

Lógica de prioridades y filtros

Interfaz de consola con colores

Tests automatizados

También quería una historia de commits que guiara la evolución del proyecto.

2. Diseño del esquema del proyecto
Solicité un esquema de carpetas y módulos. La IA proporcionó una estructura clara con:

models.py

storage.py

logic.py

cli.py

Carpeta tests/

Archivo tasks.json

requirements.txt

Deseché este esquema y proporcioné el esquema incluido en el ejercicio

3. Generación del primer commit del proyecto
Le pedí a la IA que preparara la versión inicial del repositorio, incluyendo:

Estructura mínima

CLI básica con un comando hello

Archivo tasks.json vacío

Tests iniciales con pytest

Dependencias en requirements.txt

La IA entreguó todos los archivos listos para usar.

4. Creación del README
Finalmente, le pedí:

“Hazme un readme con una pequeña descripción del proyecto, cómo instalar las dependencias y cómo ejecutarlo.”

Generó un README.md completo con:

Descripción breve del proyecto

Instalación de dependencias

Ejecución de la CLI

Ejecución de tests

Estructura del proyecto

Revisé los archivos .gitignore y __init__.py y los incluí en la estructura.

Testeé y Validé los archivos main.py y cli.py donde se incluía el funcionamiento del programa.

Incluí la carpeta __pycache__ en el archivo .gitignore para agilizar la carga del programa.

