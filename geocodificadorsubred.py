# usuraio y clave
username = ""
password = ""

direcciones_str = """DG 18 BIS 16A 70
KR 11C ESTE 1 62
CL 20 SUR 11A 5 ESTE
"""
direcciones = direcciones_str.splitlines()

print(direcciones)  #valida que esten bien.


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time
from bs4 import BeautifulSoup

tiempo_espera = 0.5

# Configura las opciones de Chrome para ejecutar el navegador en modo sin cabeza
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializa el navegador Chrome
driver = webdriver.Chrome(options=chrome_options)

# Inicia sesión en la página
login_url = 'http://sig.saludcapital.gov.co/geocodificardireccion/login.aspx'
driver.get(login_url)

# Supongamos que has ingresado tu nombre de usuario y contraseña en los campos correspondientes
# Asegúrate de inspeccionar los elementos de la página para obtener los identificadores correctos
username_field = driver.find_element("name", "txbUsuario")
password_field = driver.find_element("name", "txbContrasena")

# Ingresa el nombre de usuario y la contraseña
username_field.send_keys(username)
password_field.send_keys(password)

# Haz clic en el botón de inicio de sesión
submit_button = driver.find_element("name", "btnIngresar")
submit_button.click()

# Espera un tiempo para asegurarse de que la página se cargue completamente
time.sleep(tiempo_espera)

# Navega a la página de geocodificación
geocoding_url = 'http://sig.saludcapital.gov.co/geocodificardireccion/geocodificar/geocodificar.aspx'
driver.get(geocoding_url)


###solo para buscar una direccion de a una
##address_field = driver.find_element("name", "txbDireccion")
##address = "DG 18 BIS 16A 70"
##address_field.send_keys(address)

for direccion in direcciones:
  # Ingresa la dirección en el campo correspondiente
  address_field = driver.find_element("name", "txbDireccion")
  address_field.clear()  # Limpia el campo antes de ingresar una nueva dirección
  address_field.send_keys(direccion)

  # Haz clic en el botón "Buscar Dirección"
  search_button = driver.find_element("name", "btnBuscarDireccion")
  search_button.click()

  # Espera un tiempo para que se realice la búsqueda y se obtenga la respuesta
  time.sleep(tiempo_espera)

  # Imprime la respuesta obtenida

  # Obtén el código fuente de la página
  pagina_html = driver.page_source

  # Usa BeautifulSoup para analizar el código HTML
  soup = BeautifulSoup(pagina_html, 'html.parser')

  # Encuentra el elemento  con el id "lblLocalidad"
  input_direccion = soup.find('input', {'name': 'txbDireccion'})
  span_localidad = soup.find('span', id='lblLocalidad')

  print(input_direccion['value'], ";",span_localidad.text)

# Cierra el navegador
driver.quit()