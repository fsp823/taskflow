import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from taskflow.models import Task, PRIORIDAD_MINIMA, PRIORIDAD_MAXIMA


class TestTaskModel(unittest.TestCase):

    def test_creacion_valida(self):
        tarea = Task(titulo="Estudiar Python", prioridad=3)

        self.assertEqual(tarea.titulo, "Estudiar Python")
        self.assertEqual(tarea.prioridad, 3)
        self.assertEqual(tarea.estado, "pendiente")

        # id y fecha_creacion deben generarse automáticamente
        self.assertIsInstance(tarea.id, str)
        self.assertIsInstance(tarea.fecha_creacion, str)

    def test_titulo_vacio(self):
        with self.assertRaises(ValueError):
            Task(titulo="", prioridad=3)

        with self.assertRaises(ValueError):
            Task(titulo="   ", prioridad=3)

    def test_prioridad_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            Task(titulo="Algo", prioridad=0)

        with self.assertRaises(ValueError):
            Task(titulo="Algo", prioridad=6)

    def test_to_dict(self):
        tarea = Task(titulo="Leer", prioridad=2)
        datos = tarea.to_dict()

        self.assertEqual(datos["titulo"], "Leer")
        self.assertEqual(datos["prioridad"], 2)
        self.assertEqual(datos["estado"], "pendiente")
        self.assertIn("id", datos)
        self.assertIn("fecha_creacion", datos)

    def test_from_dict(self):
        datos = {
            "id": "1234",
            "titulo": "Probar",
            "prioridad": 4,
            "estado": "completada",
            "fecha_creacion": "2024-01-01T10:00:00"
        }

        tarea = Task.from_dict(datos)

        self.assertEqual(tarea.id, "1234")
        self.assertEqual(tarea.titulo, "Probar")
        self.assertEqual(tarea.prioridad, 4)
        self.assertEqual(tarea.estado, "completada")
        self.assertEqual(tarea.fecha_creacion, "2024-01-01T10:00:00")

    def test_from_dict_faltan_campos(self):
        datos_incompletos = {
            "titulo": "Algo",
            "prioridad": 3
        }

        with self.assertRaises(KeyError):
            Task.from_dict(datos_incompletos)


if __name__ == "__main__":
    unittest.main()
