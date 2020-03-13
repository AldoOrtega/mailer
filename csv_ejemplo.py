from mail import csv_mailer, csv_encoder

datos = 'files/datos_prueba.csv'
csv_encoder(datos)
csv_mailer('Ejemplo',
			 mas='Estimado', fem='Estimada', r_body='files/body.html',
			 r_datos=datos)