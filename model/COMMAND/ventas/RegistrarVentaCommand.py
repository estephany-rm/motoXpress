from db.gestor_conexiones import ConexionSQLite3

from model.DAO.VentaDAO import VentaDAO
from model.DAO.MotoDAO import MotoDAO
from model.DAO.FinanciacionDAO import FinanciacionDAO

from model.VO.VentaVO import VentaVO
from model.VO.FinanciacionVO import FinanciacionVO
from typing import Optional


class RegistrarVentaCommand:

    def __init__(self, venta: VentaVO,
                 financiacion: Optional[FinanciacionVO] = None):
        self._venta = venta
        self._financiacion = financiacion

        self._venta_id: Optional[int] = None
        self._moto_estado_anterior: Optional[str] = None

    def execute(self, conn: ConexionSQLite3) -> None:
        moto = MotoDAO.obtener_por_id(conn, self._venta.id_moto)
        self._moto_estado_anterior = moto.estado

        self._venta_id = VentaDAO.insertar(conn, self._venta)
        self._venta.id_venta = self._venta_id

        moto.estado = "vendida"
        MotoDAO.actualizar(conn, moto)

        if self._financiacion is not None:
            self._financiacion.id_venta = self._venta_id
            FinanciacionDAO.insertar(conn, self._financiacion)

    def undo(self, conn: ConexionSQLite3) -> None:
        if self._venta_id is None:
            raise RuntimeError("No se puede deshacer: el comando no ha sido ejecutado.")

        VentaDAO.eliminar(conn, self._venta_id)

        moto = MotoDAO.obtener_por_id(conn, self._venta.id_moto)
        moto.estado = self._moto_estado_anterior
        MotoDAO.actualizar(conn, moto)

        if self._financiacion is not None and self._financiacion.id_financiacion is not None:
            FinanciacionDAO.eliminar(conn, self._financiacion.id_financiacion)
