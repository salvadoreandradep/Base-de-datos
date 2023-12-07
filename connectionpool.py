from bs4 import BeautifulSoup
import urllib3
import csv

# Desactivar la verificación del certificado SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Constantes
NUM_ELEMENTS = 10

def scrape_data(url, class_name1, class_name2):
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
    try:
        web = http.request('GET', url)
        web_status = web.status
        if web_status != 200:
            print(f"Error durante la solicitud web. Estado: {web_status}")
            return None, None
    except Exception as e:
        print(f"Error durante la solicitud web: {e}")
        return None, None

    soup = BeautifulSoup(web.data, "html.parser")

    # Obtener los elementos de la primera clase
    pos1_elements = soup.find_all(class_=class_name1)[:NUM_ELEMENTS]
    data_list_pos1 = [element.get_text() for element in pos1_elements]

    # Obtener los elementos de la segunda clase
    pos2_elements = soup.find_all(class_=class_name2)[:NUM_ELEMENTS]
    data_list_pos2 = [element.get_text() for element in pos2_elements]

    return data_list_pos1, data_list_pos2

def save_to_csv(data_list_pos1, data_list_pos2, output_file):
    # Guardar en un archivo CSV con columnas separadas
    with open(output_file, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Escribir los encabezados
        writer.writerow(['Producto', 'Modelo'])
        # Escribir los datos en columnas separadas
        writer.writerows(zip(data_list_pos1, data_list_pos2))

# URL del sitio web
url = 'https://www.omnisport.com/categorias/computadoras'

# Nombres de las clases que se quieren extraer
class_name1 = 'font-gothic'
class_name2 = 'text-main font-bold text-lg md:text-xl'

# Nombre del archivo de salida CSV
output_file = 'datos.csv'

# Llamar a la función para realizar el scraping y guardar en el archivo CSV
data_list_pos1, data_list_pos2 = scrape_data(url, class_name1, class_name2)

if data_list_pos1 is not None and data_list_pos2 is not None:
    save_to_csv(data_list_pos1, data_list_pos2, output_file)
    print(f"Datos guardados exitosamente en {output_file}")
else:
    print("No se pudieron obtener datos para guardar.")

