from clientes.notificaciones import NotificadorConsola, NotificadorEmail


class SMTPFalso:
    """Sustituye a smtplib.SMTP para probar sin conectarse a un servidor real."""

    instancias: list["SMTPFalso"] = []

    def __init__(self, servidor, puerto):
        self.servidor, self.puerto = servidor, puerto
        self.tls = False
        self.credenciales = None
        self.mensajes = []
        SMTPFalso.instancias.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def starttls(self):
        self.tls = True

    def login(self, usuario, clave):
        self.credenciales = (usuario, clave)

    def send_message(self, mensaje):
        self.mensajes.append(mensaje)


def test_notificador_email_usa_tls_credenciales_y_arma_el_mensaje(monkeypatch):
    SMTPFalso.instancias.clear()
    monkeypatch.setattr("clientes.notificaciones.smtplib.SMTP", SMTPFalso)
    notificador = NotificadorEmail("smtp.ejemplo.com", 587, "ventas@softmarket.com", "secreta")

    notificador.enviar("ana@correo.com", "Bienvenida", "Hola Ana")

    smtp = SMTPFalso.instancias[0]
    assert (smtp.servidor, smtp.puerto, smtp.tls) == ("smtp.ejemplo.com", 587, True)
    assert smtp.credenciales == ("ventas@softmarket.com", "secreta")
    correo = smtp.mensajes[0]
    assert correo["To"] == "ana@correo.com"
    assert correo["Subject"] == "Bienvenida"
    assert correo.get_content().strip() == "Hola Ana"


def test_notificador_consola_muestra_el_mensaje(capsys):
    NotificadorConsola().enviar("ana@correo.com", "Bienvenida", "Hola Ana")

    assert capsys.readouterr().out == "Para: ana@correo.com | Bienvenida\nHola Ana\n"
