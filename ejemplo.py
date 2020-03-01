from mail import mailer


# def mailer(asunto, correos, nombres=None, empresas=None, sexos=None, mas=None, fem=None):

mailer(asunto='Prueba',
	   correos=['example@gmail.com'], 
	   nombres=['Pedro'],
	   empresas= ['Monster Inc.'])
