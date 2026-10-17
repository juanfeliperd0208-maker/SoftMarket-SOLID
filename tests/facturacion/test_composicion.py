from facturacion.composicion import crear_servicio_facturacion
from facturacion.notificaciones import NotificadorEmail
from facturacion.servicio import ServicioFacturacion


class SMTPFalso:
    enviados = []

    def __init__(self, servidor, puerto):
        self.servidor, self.puerto = servidor, puerto

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self):
        pass

    def login(self, usuario, clave):
        pass

    def send_message(self, mensaje):
        SMTPFalso.enviados.append((self.servidor, self.puerto, mensaje))


def test_la_raiz_de_composicion_lee_la_configuracion_del_entorno(monkeypatch):
    for clave, valor in {
        "SOFTMARKET_SMTP_SERVIDOR": "smtp.ejemplo.com",
        "SOFTMARKET_SMTP_USUARIO": "ventas@softmarket.com",
        "SOFTMARKET_SMTP_CLAVE": "secreta",
        "SOFTMARKET_SMTP_REMITENTE": "ventas@softmarket.com",
    }.items():
        monkeypatch.setenv(clave, valor)

    assert isinstance(crear_servicio_facturacion(), ServicioFacturacion)


def test_notificador_email_envia_por_el_servidor_configurado(monkeypatch):
    SMTPFalso.enviados.clear()
    monkeypatch.setattr("facturacion.notificaciones.smtplib.SMTP", SMTPFalso)
    notificador = NotificadorEmail("smtp.ejemplo.com", 587, "u", "c", "ventas@softmarket.com")

    notificador.notificar("ana@correo.com", "Factura FAC-000001", "TOTAL: 10.00")

    servidor, puerto, correo = SMTPFalso.enviados[0]
    assert (servidor, puerto, correo["To"]) == ("smtp.ejemplo.com", 587, "ana@correo.com")
