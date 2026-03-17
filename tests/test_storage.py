import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import json
import tempfile
from pathlib import Path

from taskflow.storage import load_tasks, save_tasks
from taskflow.models import Task


class TestStorage(unittest.TestCase):

    def test_load_tasks_archivo_no_existe(self):
        ruta_inexistente = Path("no_existe_12345.json")
        resultado = load_tasks(ruta_inexistente)
        self.assertEqual(resultado, [])

    def test_load_tasks_archivo_vacio(self):
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as tmp:
            ruta = Path(tmp.name)

        # Archivo vacío
        resultado = load_tasks(ruta)
        self.assertEqual(resultado, [])

        ruta.unlink()  # borrar archivo temporal

    def test_load_tasks_json_valido(self):
        tareas = [
            Task(titulo="A", prioridad=3),
            Task(titulo="B", prioridad=5)
        ]

        datos = [t.to_dict() for t in tareas]

        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as tmp:
            json.dump(datos, tmp)
            ruta = Path(tmp.name)

        cargadas = load_tasks(ruta)

        self.assertEqual(len(cargadas), 2)
        self.assertEqual(cargadas[0].titulo, "A")
        self.assertEqual(cargadas[1].prioridad, 5)

        ruta.unlink()

    def test_load_tasks_json_malformado(self):
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as tmp:
            tmp.write("{esto no es json}")
            ruta = Path(tmp.name)

        with self.assertRaises(json.JSONDecodeError):
            load_tasks(ruta)

        ruta.unlink()

    def test_save_tasks_crea_y_guarda(self):
        tareas = [
            Task(titulo="Tarea 1", prioridad=2),
            Task(titulo="Tarea 2", prioridad=4)
        ]

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            ruta = Path(tmp.name)

        save_tasks(tareas, ruta)

        contenido = ruta.read_text(encoding="utf-8")
        datos_json = json.loads(contenido)

        self.assertEqual(len(datos_json), 2)
        self.assertEqual(datos_json[0]["titulo"], "Tarea 1")
        self.assertEqual(datos_json[1]["prioridad"], 4)

        ruta.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
