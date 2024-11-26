import qrcode

def generar_codigo_qr(link, nombre_archivo='codigo_qr.png'):
    # Crea el objeto de código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Agrega el enlace al QR
    qr.add_data(link)
    qr.make(fit=True)

    # Genera la imagen del QR
    imagen = qr.make_image(fill="black", back_color="white")
    imagen.save(nombre_archivo)
    print(f"Código QR guardado como {nombre_archivo}")

# Ejemplo de uso
generar_codigo_qr("http://127.0.0.1:5000/", "mi_codigo_qr.png")
