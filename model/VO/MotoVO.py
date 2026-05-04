from dataclasses import dataclass, field
from typing import Optional, List, Callable

from model.VO.CategoriaVO import CategoriaVO


@dataclass
class MotoVO:
    id_moto: int
    vin: str = field(default=None)
    marca: str = field(default=None)
    modelo: str = field(default=None)
    anio: int = field(default=None)
    precio: float = field(default=None)
    color: str = field(default=None)
    estado: str = field(default='disponible')

    # relacion de agregacion
    categorias: List[CategoriaVO] = field(default_factory=list)

    # Lazy opcional
    _categorias_loader: Optional[Callable[[], List[CategoriaVO]]] = field(default=None, repr=False)

    def cargar_categorias(self):
        if not self.categorias and self._categorias_loader:
            self.categorias = self._categorias_loader()

    @property
    def esta_disponible(self) -> bool:
        return self.estado == 'disponible'

    def marcar_como_vendida(self):
        if not self.esta_disponible:
            raise ValueError("La moto ya está vendida")
        self.estado = 'vendida'