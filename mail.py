from mailer import Mailer
from mailer import Message
from  os.path import isfile

def verificador(var1, var2, nombre):
    if var2 is not None:
        if len(var1) != len(var2):
            raise Exception('El número de ' + nombre + ' no coincide con el número de correos')

def mailer(asunto, correos, nombres=None, empresas=None, sexos=None, mas=None, fem=None):

    """
    Función que permite enviar una plantilla de correo a múltiples destinatarios 
    personalizando algunos campos.
    
    asunto: asunto del correo
    correos: lista con las direcciones de correo de los destinatarios
    nombres: lista con los nombres de los destinatarios
    empresa: lista con las empresas a las que pertenecen los destinatarios
    sexo: lista indicando el sexo de los destinatarios, True: masculino, False: femenino
    mas: saludo para los hombres (string)
    fem: saludo para las mujeres (string)

    Escribir el correo en el archivo files/body.html, usando como placeholder los siguientes valores:
    $Nombre: será reemplazado por el nombre del destinatario
    $Empresa: será remplazado por la empresa a la que el destinatario pertenece
    $Masculino: frase exclusiva para hombres
    $Femenino: frase exclusiva para mujeres

    los archivos header.html y footer.html son opcionales para adjuntar cabeceras y piés de página.

    Para las credenciales del servidor crear el archivo credenciales.txt en la carpeta files ingresando los siguientes datos:
    Primera línea: correo del remitente (sender)
    Segunda línea: servidor (ej: smtp.ejemplo.com)
    Tercera línea: nombre de usuario
    Cuarta línea: contraseña
    """

    verificador(correos, nombres, 'nombres')
    verificador(correos, empresas, 'empresas')
    verificador(correos, sexos, 'sexos')

    file = open("files/body.html","r")
    body = file.read()
    file.close()

    mensaje = body

    if isfile('files/header.html'):
        file = open("files/header.html","r")
        header = file.read()
        file.close()
        mensaje = header + mensaje
    
    if isfile('files/footer.html'):
        file = open("files/footer.html","r")
        footer = file.read()
        file.close()
        mensaje = mensaje + footer

    file = open('files/credenciales.txt', 'r') 
    cred = file.read().splitlines()
    file.close()

    i = 0
    for correo in correos:

        if nombres is not None:
            mensaje = mensaje.replace('$Nombre', nombres[i])

        if empresas is not None:
            mensaje = mensaje.replace('$Empresa', empresas[i])

        if sexos is not None:
            if sexos[i]:
                mensaje = mensaje.replace('$Masculino', mas)
            else:
                mensaje = mensaje.replace('$Femenino', fem)

        message = Message(From=cred[0],
                      To=correo)
        message.Subject = asunto
        message.Html = mensaje

        sender = Mailer(cred[1], 
                        use_tls=True,
                        usr=cred[2],
                        pwd=cred[3],
                        port=587)

        sender.send(message)
        i+=1   
    



