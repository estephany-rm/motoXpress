from db.gestor_conexiones import connection_factory   

from model.COMMAND.UndoRedoManager import UndoRedoManager

from service.VentaService import VentaService
from service.MotoService import MotoService
from service.ClienteService import ClienteService
from service.EmpleadoService import EmpleadoService
from service.CategoriaService import CategoriaService

from controller.MotoXpressController import MotoXpressController

# Factory del sistema (construye el árbol de dependencias)
def build_controller() -> MotoXpressController:
    """
    Factory principal.

    Instancia todos los componentes en el orden correcto e inyecta
    dependencias según su capa:
      DB ← DAO ← Service ← Controller
    El UndoRedoManager se crea aquí y se comparte con VentaService.
    """
    undo_redo = UndoRedoManager()

    venta_service    = VentaService(undo_redo)
    moto_service     = MotoService()
    cliente_service  = ClienteService()
    empleado_service = EmpleadoService()
    categoria_service = CategoriaService()

    return MotoXpressController(
        venta_service=venta_service,
        moto_service=moto_service,
        cliente_service=cliente_service,
        empleado_service=empleado_service,
        categoria_service=categoria_service,
    )


# Punto de entrada
def main():
    controller = build_controller()
    # iniciar UI (PyQt5)
    # app = QApplication(sys.argv)
    # ventana = MainWindow(controller)
    # ventana.show()
    # sys.exit(app.exec_())
    print("MotoXpress iniciado correctamente.")
    print("Controller listo:", controller)


if __name__ == "__main__":
    main()
