import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest 
from taskflow.logic import filter_by_status, sort_by_priority, get_stats
from taskflow.models import Task

class TestLogic(unittest.TestCase):

    def setUp(self):
        self.tasks = [
            Task(titulo="Tarea 1", estado="pendiente", prioridad=3),
            Task(titulo="Tarea 2", estado="completada", prioridad=1),
            Task(titulo="Tarea 3", estado="pendiente", prioridad=5),
            Task(titulo="Tarea 4", estado="completada", prioridad=2)
        ]

    def test_filter_by_status(self):
        pendientes = filter_by_status(self.tasks, "pendiente")
        self.assertEqual(len(pendientes), 2)
        for t in pendientes:
            self.assertEqual(t.estado, "pendiente")

        completadas = filter_by_status(self.tasks, "completada")
        self.assertEqual(len(completadas), 2)
        for t in completadas:
            self.assertEqual(t.estado, "completada")

        vacio = filter_by_status(self.tasks, "otro")
        self.assertEqual(vacio, [])

    def test_sort_by_priority(self):
        asc = sort_by_priority(self.tasks)
        prioridades_asc = [t.prioridad for t in asc]
        self.assertEqual(prioridades_asc, sorted(prioridades_asc))

        desc = sort_by_priority(self.tasks, reverse=True)
        prioridades_desc = [t.prioridad for t in desc]
        self.assertEqual(prioridades_desc, sorted(prioridades_desc, reverse=True))

    def test_get_stats(self):
        stats = get_stats(self.tasks)
        self.assertEqual(stats["total"], 4)
        self.assertEqual(stats["pendientes"], 2)
        self.assertEqual(stats["completadas"], 2)
        self.assertAlmostEqual(stats["prioridad_media"], (3+1+5+2)/4, places=2)

        stats_vacio = get_stats([])
        self.assertEqual(stats_vacio, {
            "total": 0,
            "pendientes": 0,
            "completadas": 0,
            "prioridad_media": 0.0
        })
