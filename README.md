Proyecto Grupal TaskFlow 

TaskFlow CLI
TaskFlow CLI es un gestor de tareas en consola escrito en Python 3.12+. Su objetivo es ofrecer una herramienta ligera, extensible y fácil de usar para crear, listar y gestionar tareas desde la terminal. El proyecto crece de forma incremental: comienza con una estructura mínima y evoluciona hacia una aplicación completa con modelos de datos, persistencia en JSON, lógica de negocio, colores en la CLI y una batería de tests automatizados.

🚀 Instalación de dependencias
Asegúrate de tener Python 3.12 o superior instalado.

1. Clona el repositorio:

bash
git clone https://github.com/tuusuario/taskflow.git
cd taskflow

2. Instala las dependencias:

bash
pip install -r requirements.txt
Esto instalará:

Typer — para la interfaz de línea de comandos

Rich — para salida con colores y tablas

pytest — para ejecutar los tests


▶️ Ejecución de la aplicación
Puedes ejecutar la CLI directamente con Python:

bash
python -m taskflow.cli hello
Ejemplo:

bash
python -m taskflow.cli hello TaskFlow
Salida esperada:

Código
Hola TaskFlow 👋