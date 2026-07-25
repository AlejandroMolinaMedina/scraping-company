import requests
import json
from jinja2 import Environment
from jinja2 import FileSystemLoader
from pdfkit import from_string
import os
import tldextract
from datetime import datetime
import re
import random
from flask import render_template_string
from flask_mail import Message
import base64
from itsdangerous import URLSafeSerializer
import requests
import dotenv

def get_first_contentful_paint(url):
    #"AIzaSyAL67F5ZAG1eCWeoG5hAOwf2CYO_EfumAE"
    api_key = os.environ.get('PAGESPEED_APIKEY')
    api_url = f"https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=SEO&category=ACCESSIBILITY&category=BEST_PRACTICES&category=PERFORMANCE&strategy=DESKTOP&key={api_key}"
    response = requests.get(api_url)
    data = response.json()
    try:

        print("Datos guardados exitosamente en 'ligthouse.json'.")
        fcp_value = data["lighthouseResult"]["audits"]["first-contentful-paint"].get("displayValue", "N/A").replace("\xa0", " ")
        lcp_value = data["lighthouseResult"]["audits"]["largest-contentful-paint"].get("displayValue", "N/A").replace("\xa0", " ")
        cls_value = data["lighthouseResult"]["audits"]["cumulative-layout-shift"].get("displayValue", "N/A").replace("\xa0", " ")
        si_value = data["lighthouseResult"]["audits"]["speed-index"].get("displayValue", "N/A").replace("\xa0", " ")
        tbt_value = data["lighthouseResult"]["audits"]["total-blocking-time"].get("displayValue", "N/A").replace("\xa0", " ")
        performance = data["lighthouseResult"]["categories"]["performance"].get("score", None)
        accessibility = data["lighthouseResult"]["categories"]["accessibility"].get("score", None)
        best_practices = data["lighthouseResult"]["categories"]["best-practices"].get("score", None)
        seo = data["lighthouseResult"]["categories"]["seo"].get("score", None)
        
        if performance is not None:
            performance = performance * 100
        if accessibility is not None:
            accessibility = accessibility * 100
        if best_practices is not None:
            best_practices = best_practices * 100
        if seo is not None:
            seo = seo * 100

        
        metrics = {'First Content Paint': [fcp_value], 'Largest Contentful Paint': [lcp_value], 'Cumulative Layout Shift': [cls_value], 'Speed Index': [si_value], 'Total Blocking Time': [tbt_value]}
        
        diagnosis = {"Performance": [performance], "Accesibilidad":[accessibility], "Mejores prácticas": [best_practices], "SEO":[seo]}        
        

        result = [metrics, diagnosis]
        return result
    except KeyError:
        print (data)
        return None

def get_technology_info_formatted(url):
    #"wq0ec3q7zwkhhko60d7d83856wy0ssvn1lnrbk7w01s327xtjn85up986vja0s70tjrd2l"
    api_key = os.environ.get('WHO_HOST_ADN_WHATCMS_APIKEY')
    api_url = 'https://whatcms.org/API/Tech'
    params = {'key': api_key, 'url': url}
    response = requests.get(api_url, params=params)
    tech_info_raw = response.text

    try:
        technologysData = []
        hostname_json = json.loads(tech_info_raw)
        print(hostname_json)
        for result in hostname_json["results"]:
            nombre = result["name"]
            if nombre == 'Magento':
                urlM = url + '/magento_version'
                versionM = requests.get(urlM)
                if versionM.status_code == 200:
                    magento_version = versionM.text.strip()
                    if magento_version.startswith("Magento/"):
                        magento_version = magento_version.replace("Magento/", "", 1)
                        version = magento_version
                    else:
                        version = "N/A"
                else:
                    version = "No se encontró la versión"
                    print(versionM.status_code)
            else:
                version = result["version"] if "version" in result else "N/A"
            
            categorias = result["categories"] if "categories" in result else ["N/A"]
            technologysData.append([nombre, version, categorias])

        print(technologysData)
        return technologysData

    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        print("\nRespuesta JSON (en bruto):")
        print("------------------")
        print(tech_info_raw)


def getHostsThisSite(url):
    api_key = os.environ.get('WHO_HOST_ADN_WHATCMS_APIKEY')
    api_url = 'https://www.who-hosts-this.com/API/Host'
    params = {'key': api_key, 'url': url}
    response = requests.get(api_url, params=params)
    tech_info_raw = response.text

    try:
        hostname_json = json.loads(tech_info_raw)
        for result in hostname_json.get("results", []):
            nombre = result.get("isp_name", "N/A")
            return nombre

    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        print("\nRespuesta JSON (en bruto):")
        print("------------------")
        print(tech_info_raw)


def create_pdf(template_vars):

    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('app/templates/templateInformePDF.html')

    html_out = template.render(template_vars)

    file_content = from_string(
        html_out,
        False,
        #options='here_a_dict_with_special_page_properties',
        css= "app/static/css/styleReport.css" 
    )

    return file_content



def save_pdf(file_content,pdf_name = 'tu_archivo_pdf.pdf', folder_path='app/pdfs'):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        

        pdf_path = os.path.join(folder_path, pdf_name)

        with open(pdf_path, 'wb+') as file:
            file.write(file_content)

        return file_content
    
    except Exception as error:
        print(f'Error saving file to disc. Error: {error}')
        raise error


def save_json (template_vars, file_name = 'pruebaJson.json', json_path= 'app/json'):
    if not os.path.exists(json_path):
            os.makedirs(json_path)
    with open(os.path.join(json_path, file_name), 'w') as file:
            json.dump(template_vars, file)


    with open(os.path.join(json_path, file_name), 'r') as a:
        jsonDic = json.load(a)
    
    return jsonDic


def get_technology_info_formatted2 (urlp):
    url = "https://website-technology-lookup-api.p.rapidapi.com/get_site_apps"

    search = tldextract.extract(urlp)
    names = search.domain
    tld = search.suffix
    dominio = names + '.' + tld
    
    payload = {'data': '{{"rawhostname":"{}","hostname":"{}","url":" {}/","type":"ajax"}}'.format(dominio, dominio, urlp)}


    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": f"{os.environ.get('X-RAPIDAPI-KEY')}",
	"X-RapidAPI-Host": "website-technology-lookup-api.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    

    dic = response.json()

    dic = dic.get('apps')





    jsonS = json.loads(dic)

    # Obtener las claves (en este caso, solo hay una)
    claves = list(jsonS.keys())

    # Obtener el primer valor del JSON
    primer_valor = claves[0]

    dataClave = jsonS[primer_valor]
    lista_obtener = ['CMS', 'Javascript Frameworks', 'Web Framework', 'Web Server', 'Programming Language']


    listaf = []

    # Declarar un conjunto para almacenar elementos únicos
    # Declarar un conjunto para almacenar elementos únicos
    conjunto_resultados = []

    for i in lista_obtener:
        try:
            data = dataClave[i]  # Corregir aquí para obtener la lista directamente
            lenData = len(data)
            if lenData > 1:
                for j in range(lenData):
                    datas = data[j]  # Acceder a cada elemento de la lista
                    name = datas['name']
                    category = str(datas['category'])

                    # Utilizar una tupla para representar la información única
                    resultado_unico = [name, category, [i]]
                    conjunto_resultados.append(resultado_unico)
            else:
                datas = data[0]  # Acceder al único elemento de la lista
                name = datas['name']
                category = str(datas['category'])

                # Utilizar una tupla para representar la información única
                resultado_unico = [name, category, i]
                conjunto_resultados.append(resultado_unico)

        except Exception as e:
            print(f"Error: {e}")
            pass

    # Convertir el conjunto a lista
    listaf = list(conjunto_resultados)

    return(listaf)

#def bindList (list1, list2)


def validar_correo(correo):
    # Expresión regular para validar el formato del correo
    patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Verificar si cumple con el formato general de un correo electrónico
    if re.match(patron_correo, correo):
        return True
        #if "" in correo or "" in correo:
        #    return True
        #else:
        #    return False
    else:
        print("Formato de correo inválido")
        return False
    

def generarCodigo():
    codigo = random.randint(0000, 9999)
    print(codigo)
    return codigo




def send_email(subject, recipients, html_body, mail):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body  # Asignar el cuerpo HTML al mensaje
    mail.send(msg)

def send_verification_email(email, codigo, mail):
    subject = 'Verificación de Correo Electrónico'

    # Leer el archivo HTML con el diseño
    with open('app/templates/correoVerificaciónEmail.html', 'r') as file:
        template = file.read()


    # Reemplazar el marcador de posición con el código real
    body = render_template_string(template, codigo=codigo)

    # Utilizar la función send_email
    send_email(subject, [email], body, mail)


# Encriptar la URL
def encrypt_url(informe_id, secretKey):
    s = URLSafeSerializer(secretKey)
    return s.dumps(informe_id)

# Desencriptar la URL
def decrypt_url(token, secretKey):
    s = URLSafeSerializer(secretKey)
    try:
        informe_id = s.loads(token)
        return informe_id
    except Exception as e:
        print(f"Error al desencriptar la URL: {e}")
        return None


    
    

