from bs4 import BeautifulSoup
import urllib3
import csv

# Desactivar la verificación del certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_and_save(url, class_name1, class_name2, output_file):
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
    web = http.request('GET', url)
    soup = BeautifulSoup(web.data, "html.parser")

    # Obtener los elementos de la primera clase
    pos1_elements = soup.find_all(class_=class_name1)[:10]
    data_list_pos1 = [element.get_text() for element in pos1_elements]

    # Obtener los elementos de la segunda clase
    pos2_elements = soup.find_all(class_=class_name2)[:10]
    data_list_pos2 = [element.get_text() for element in pos2_elements]

    # Guardar en un archivo CSV con columnas separadas
    with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Escribir los encabezados
        writer.writerow(['Producto', 'Modelo', ' Precio'])
        # Escribir los datos en columnas separadas
        writer.writerows(zip(data_list_pos1, data_list_pos2))

# URL del sitio web
url = 'https://www.omnisport.com/categorias/computadoras'

# Nombres de las clases que se quieren extraer
class_name1 = 'font-gothic'
class_name2 = 'text-main font-bold text-lg md:text-xl'

# Nombre del archivo de salida CSV
output_file = 'parcial.csv'





# Llamar a la función para realizar el scraping y guardar en el archivo CSV
scrape_and_save(url, class_name1, class_name2, output_file)