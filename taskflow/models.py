# taskflow/models.py
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# ── Constantes ────────────────────────────────────────────────────────────────

PRIORIDAD_MINIMA  = 1
PRIORIDAD_MAXIMA  = 5
ESTADO_INICIAL    = "pendiente"


# ── Modelo de datos ───────────────────────────────────────────────────────────

@dataclass
class Task:
    """Representa una tarea en el gestor TaskFlow.

    Attributes:
        titulo:         texto descriptivo de la tarea. No puede estar vacío.
        prioridad:      nivel de urgencia del 1 (baja) al 5 (crítica).
        estado:         estado actual de la tarea. Por defecto 'pendiente'.
        id:             identificador único generado automáticamente (UUID4).
        fecha_creacion: fecha y hora de creación en formato ISO 8601.
    """

    titulo:         str
    prioridad:      int
    estado:         str = ESTADO_INICIAL
    id:             str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self) -> None:
        """Valida los campos obligatorios al crear la tarea.

        Raises:
            ValueError: si el título está vacío o la prioridad está fuera de rango.
        """
        titulo_vacio    = not self.titulo or not self.titulo.strip()
        prioridad_fuera_de_rango = self.prioridad < PRIORIDAD_MINIMA or self.prioridad > PRIORIDAD_MAXIMA

        if titulo_vacio:
            raise ValueError("El título no puede estar vacío.")

        if prioridad_fuera_de_rango:
            raise ValueError(
                f"La prioridad debe estar entre {PRIORIDAD_MINIMA} y {PRIORIDAD_MAXIMA},"
                f" recibido: {self.prioridad}"
            )

    def to_dict(self) -> dict:
        """Convierte la tarea a diccionario para serialización JSON.

        Returns:
            Diccionario con todos los campos de la tarea.

        Example:
            >>> tarea = Task(titulo="Estudiar", prioridad=3)
            >>> tarea.to_dict()
            {'id': '...', 'titulo': 'Estudiar', 'prioridad': 3, 'estado': 'pendiente', 'fecha_creacion': '...'}
        """
        return {
            "id":             self.id,
            "titulo":         self.titulo,
            "prioridad":      self.prioridad,
            "estado":         self.estado,
            "fecha_creacion": self.fecha_creacion,
        }

    @classmethod
    def from_dict(cls, datos_tarea: dict) -> "Task":
        """Construye una Task desde un diccionario leído de JSON.

        Args:
            datos_tarea: diccionario con los campos de la tarea.

        Returns:
            Nueva instancia de Task con los datos del diccionario.

        Raises:
            KeyError: si faltan campos obligatorios en el diccionario.
        """
        return cls(
            id=            datos_tarea["id"],
            titulo=        datos_tarea["titulo"],
            prioridad=     datos_tarea["prioridad"],
            estado=        datos_tarea["estado"],
            fecha_creacion=datos_tarea["fecha_creacion"],
        )