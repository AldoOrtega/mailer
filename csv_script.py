from mail import csv_mailer, csv_encoder

datos = 'files/datos_ws.csv'
csv_encoder(datos)
csv_mailer('Invitación Workshop IA UdeC',
			 mas='Estimado', fem='Estimada', r_body='files/body_ws.html',
			 r_datos=datos, r_credenciales='files/credenciales_uds.txt',
			 r_footer='files/footer_uds.html')