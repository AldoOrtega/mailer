from mailer import Mailer
from mailer import Message
from  os.path import isfile

def verificador(var1, var2, nombre):
    if var2 is not None:
        if len(var1) != len(var2):
            raise Exception('El número de {} ({}) no coincide con el número de correos ({})'.format(nombre, len(var2), len(var1)))

def encoder(strg):

    dic = {'&ntilde;': 'ñ',
            '&Ntilde;': 'Ñ',
            '&aacute;': 'á',
            '&eacute;': 'é',
            '&iacute;': 'í',
            '&oacute;': 'ó',
            '&uacute;': 'ú',
            '&Aacute;': 'Á',
            '&Eacute;': 'É',
            '&Iacute;': 'Í',
            '&Oacute;': 'Ó',
            '&Uacute;': 'Ú',
            '&euro;': '€'}

    for key, value in dic.items():
        strg = strg.replace(value, key)

    return strg

def csv_encoder(ruta):
    fin = open(ruta, "rt")
    data = fin.read()
    data = encoder(data)
    fin.close()

    fin = open(ruta, "wt")
    fin.write(data)
    fin.close()

def mailer(asunto, correos, nombres=None, empresas=None, sexos=None, mas=None, fem=None, 
            r_header="files/header.html", r_body="files/body.html", r_footer="files/footer.html",
            r_credenciales = "files/credenciales.txt"):

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
    $Sexo: frase que será reemplazada por el parámetro mas en caso de ser hombre o fem en caso de ser mujer

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

    file = open(r_body, "r")
    body = file.read()
    file.close()

    mensaje = body

    if isfile(r_header):
        file = open(r_header, "r")
        header = file.read()
        file.close()
        mensaje = header + mensaje
    
    if isfile(r_footer):
        file = open(r_footer, "r")
        footer = file.read()
        file.close()
        mensaje = mensaje + footer

    mensaje = encoder(mensaje)

    file = open(r_credenciales, 'r') 
    cred = file.read().splitlines()
    file.close()

    i = 0
    for correo in correos:

        mensaje_aux = mensaje

        if nombres is not None:
            mensaje_aux = mensaje_aux.replace('$Nombre', nombres[i])

        if empresas is not None:
            mensaje_aux = mensaje_aux.replace('$Empresa', empresas[i])

        if sexos is not None:
            if sexos[i]:
                mensaje_aux = mensaje_aux.replace('$Sexo', mas)
            else:
                mensaje_aux = mensaje_aux.replace('$Sexo', fem)

        message = Message(From=cred[0],
                      To=correo)
        message.Subject = asunto
        message.Html = mensaje_aux

        sender = Mailer(cred[1], 
                        use_tls=True,
                        usr=cred[2],
                        pwd=cred[3],
                        port=587)

        sender.send(message)
        print('Correo',i,'enviado')
        i+=1   
    

def csv_mailer(asunto, mas=None, fem=None, r_datos='files/datos.csv',
            r_header="files/header.html", r_body="files/body.html", r_footer="files/footer.html",
            r_credenciales = "files/credenciales.txt", **kwarg):

    import pandas as pd

    datos = pd.read_csv(r_datos, **kwarg)

    correos = datos.Correo

    if 'Nombre' in datos.columns:
        nombres = datos.Nombre
    else:
        nombres = None

    if 'Empresa' in datos.columns:
        empresas = datos.Empresa
    else:
        empresas = None

    if 'Sexo' in datos.columns:
        sexos = datos.Sexo
    else:
        sexos = None

    mailer(asunto, correos, nombres, empresas, sexos, mas, fem, r_header, r_body, r_footer, r_credenciales)