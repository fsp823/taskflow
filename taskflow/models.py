# taskflow/models.py
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Task:
    titulo: str
    prioridad: int
    estado: str = "pendiente"
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.titulo or not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")
        if self.prioridad < 1 or self.prioridad > 5:
            raise ValueError(f"La prioridad debe estar entre 1 y 5, recibido: {self.prioridad}")

    def to_dict(self) -> dict:
        """Convierte la tarea a un diccionario para serialización JSON.

        Returns:
            dict con todos los campos de la tarea.

        Example:
            >>> t = Task(titulo="Estudiar", prioridad=3)
            >>> t.to_dict()
            {'id': '...', 'titulo': 'Estudiar', 'prioridad': 3, 'estado': 'pendiente', 'fecha_creacion': '...'}
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        """Crea una Task desde un diccionario leído de JSON.

        Args:
            d: diccionario con los campos de la tarea.

        Returns:
            Una instancia de Task.

        Raises:
            KeyError: si faltan campos obligatorios en el diccionario.
        """
        return cls(
            id=d["id"],
            titulo=d["titulo"],
            prioridad=d["prioridad"],
            estado=d["estado"],
            fecha_creacion=d["fecha_creacion"],
        )