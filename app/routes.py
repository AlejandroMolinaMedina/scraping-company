from flask import render_template, request, send_file, redirect, url_for, flash
from app import create_app, db
from app.models import Informe, Comentario, Usuario, TipoUsuario
from utils.analysis_utils import get_first_contentful_paint, get_technology_info_formatted, getHostsThisSite, save_json, create_pdf, save_pdf, generarCodigo, send_verification_email, decrypt_url, encrypt_url
import json
import tldextract
from datetime import datetime, timedelta
import re
from app.forms import FormLogin, FormRegistro, FormVerfificacion
from flask import Flask, session
from flask_session import Session
from flask_mail import Mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from os import remove
import pyshorteners
import requests
import time



app = create_app()
mailapp = Mail(app)
Session(app)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    
    if request.method == 'POST':
        patron_url = re.compile(r'^https?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?$')
        # Obtener la URL del formulario
        urlI = request.form['url']
        if patron_url.match(urlI):

            name = tldextract.extract(urlI).domain
            ob = db.session.query(Informe).filter_by(nombre = name.capitalize()).first()

            if ob:
                name_site = ob.nombre.capitalize()
                jsonInforme= ob.json_name
                url = ob.url
                id_Informe = ob.id_Informe


                data_informe = jsonInforme
                nombre_archivo = 'app/json/' + data_informe

                with open(nombre_archivo, 'r') as archivo:
                    json_data = archivo.read()
                    data = json.loads(json_data)

                    technology_infoJ = data['technology_info']

                    metricsJ = data['metrics']

                    hosting_providerJ = data['hosting_provider']

                    date = data['date']

                    diagnosis = data['diagnosis']

                    enlace_publico = data['urlPublic']

                    print(enlace_publico)


                    #Mandar el enlace público al template
                    return render_template('templateReport.html', hosting_provider=hosting_providerJ, metrics=metricsJ, technology_info=technology_infoJ, date = date, name_site = name_site, url = url, id_Informe = id_Informe, diagnosticos= diagnosis)
            else:

                name = name.capitalize()
                technology_info = get_technology_info_formatted(urlI)
                
                metrics = get_first_contentful_paint(urlI)

                hosting_provider = getHostsThisSite(urlI)

                today = datetime.now()
                date = today.strftime('%d/%m/%Y')

                jsonInforme = name + '.json'
                name_pdf = name + '.pdf'   

                new_report = Informe(nombre = name, url = urlI, date = date, json_name = jsonInforme, pdf_name = name_pdf)
                db.session.add(new_report)
                db.session.commit()
                id_Informe = new_report.id_Informe

                token = encrypt_url(id_Informe, app.secret_key)
                s = pyshorteners.Shortener()
                
                enlace_publico =url_for('VerInformeP', token=token, _external=True, timeout=5)
            
                template_vars = {
                'technology_info': technology_info,
                'metrics': metrics[0],
                "diagnosis": metrics[1],
                'hosting_provider': hosting_provider,
                'date': date,
                'url': urlI,
                'comments': [],
                'urlPublic': enlace_publico}

                          
                save_json(template_vars, jsonInforme)
                
                print(enlace_publico)
                #Mandar enlace público al template
                return render_template('templateReport.html', hosting_provider=hosting_provider, metrics=metrics[0], technology_info=technology_info, date = date, name_site = name, url = urlI, pdf_name = name_pdf, jsonInforme = jsonInforme, id_Informe = id_Informe, diagnosticos=metrics[1], enlace_publico = enlace_publico)
        else:
            error_message = "Ingrese una URL correcta"
            return render_template('formUrl.html', error_message=error_message)
    else:
        return render_template('formUrl.html')

@app.route('/verReportes', methods=['GET', 'POST'])
@login_required

def verReportes():
    error_message = session.pop('error_message', None)
    
    # Configura la página actual y el número de elementos por página
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de informes por página
    
    # Calcula el offset
    offset = (page - 1) * per_page
    
    # Realiza la consulta con offset y limit
    reports_query = Informe.query.order_by(Informe.id_Informe.desc())
    reports = reports_query.offset(offset).limit(per_page).all()
    
    # Obtiene el número total de informes para la paginación
    total_reports = reports_query.count()
    total_pages = (total_reports + per_page - 1) // per_page
    
    # Determina si hay páginas previas y siguientes
    has_prev = page > 1
    has_next = page < total_pages
    prev_num = page - 1
    next_num = page + 1
    
    return render_template('verInformes.html',
                           reports=reports,
                           error_message=error_message,
                           total_pages=total_pages,
                           has_prev=has_prev,
                           has_next=has_next,
                           prev_num=prev_num,
                           next_num=next_num)    
    

@app.route('/VerInforme/<string:id>', methods = ['GET', 'POST'])
@login_required
def VerInforme(id):
    try:
        di = int(id)

        ob = db.session.query(Informe).get(di)
        name_site = ob.nombre
        name_site = name_site.capitalize()
        jsonInforme= ob.json_name
        url = ob.url



        data_informe = jsonInforme
        nombre_archivo = 'app/json/' + data_informe

        #Consultar comentarios en la db
        ob_comn = db.session.query(Comentario).filter_by(id_informe=di).order_by(Comentario.id_Comentario).all()
        comments = []


        for comment in ob_comn:
            comentario = comment.comentario
            comentarioid = comment.id_Comentario
            listcomments = [comentarioid, comentario]    
            comments.append(listcomments)

        with open(nombre_archivo, 'r') as archivo:

            json_data = archivo.read()
            data = json.loads(json_data)

            technology_infoJ = data['technology_info']

            metricsJ = data['metrics']

            hosting_providerJ = data['hosting_provider']

            date = data['date']

            diagnosis = data['diagnosis']

            enlace_publico = data['urlPublic']

        
            print(enlace_publico)

        #Mandar enlace al template
        return render_template('templateReport.html', hosting_provider=hosting_providerJ, metrics=metricsJ, technology_info=technology_infoJ, date = date, name_site = name_site, url = url, id_Informe = di, comments = comments, diagnosticos= diagnosis, enlace_publico = enlace_publico)
    
    except Exception as e:
        print(e)

        if isinstance(e, FileNotFoundError):
            # Manejar la excepción de archivo no encontrado
            error_message = 'El archivo no se encuentra disponible'
        elif isinstance(e, AttributeError):
            # Manejar la excepción de atributo no encontrado en el objeto 'ob'
            error_message = 'El reporte ha sido eliminado'
        else:
            # Manejar cualquier otra excepción no especificada
            error_message = str(e)

        session['error_message'] = error_message
        return redirect(url_for('verReportes'))
    

 
@app.route('/VerInformeP/<token>', methods = ['GET', 'POST'])
def VerInformeP(token):
    id = decrypt_url(token, app.secret_key)
    try:
        di = int(id)

        ob = db.session.query(Informe).get(di)
        name_site = ob.nombre
        name_site = name_site.capitalize()
        jsonInforme= ob.json_name
        url = ob.url



        data_informe = jsonInforme
        nombre_archivo = 'app/json/' + data_informe

        #Consultar comentarios en la db
        ob_comn = db.session.query(Comentario).filter_by(id_informe=di).order_by(Comentario.id_Comentario).all()
        comments = []


        for comment in ob_comn:
            comentario = comment.comentario
            comentarioid = comment.id_Comentario
            listcomments = [comentarioid, comentario]    
            comments.append(listcomments)

        with open(nombre_archivo, 'r') as archivo:

            json_data = archivo.read()
            data = json.loads(json_data)

            technology_infoJ = data['technology_info']

            metricsJ = data['metrics']

            hosting_providerJ = data['hosting_provider']

            date = data['date']

            diagnosis = data['diagnosis']


            return render_template('templateReportPublic.html', hosting_provider=hosting_providerJ, metrics=metricsJ, technology_info=technology_infoJ, date = date, name_site = name_site, url = url, id_Informe = di, comments = comments, diagnosticos= diagnosis)
    except Exception as e:
        print(e)

        if isinstance(e, FileNotFoundError):
            # Manejar la excepción de archivo no encontrado
            error_message = 'El archivo no se encuentra disponible'
        elif isinstance(e, AttributeError):
            # Manejar la excepción de atributo no encontrado en el objeto 'ob'
            error_message = 'El reporte ha sido eliminado'
        else:
            # Manejar cualquier otra excepción no especificada
            error_message = str(e)

        session['error_message'] = error_message
        return redirect(url_for('verReportes'))

        
    
@app.route('/obtenerReporte/<string:id>', methods=['GET', 'POST'])
@login_required
def obtenerReporte(id):
    try:

        id = int(id)  
        ob = db.session.query(Informe).get(id)

        jsonInforme= ob.json_name
        pdf_name = ob.pdf_name
        name = ob.nombre

        data_informe = jsonInforme
        nombre_archivo = 'app/json/' + data_informe



        ob_comn = db.session.query(Comentario).filter_by(id_informe = id).all()
        comments = []

        for comment in ob_comn:
            comentario = comment.comentario    
            comments.append(comentario)

        with open(nombre_archivo, 'r') as archivo:

            json_data = archivo.read()
            data = json.loads(json_data)
            path_file = 'pdfs/' + pdf_name
            data['comments'] = comments
            data['name_site'] = name
            print(data)
            pdf = create_pdf(data)
            save_pdf(pdf, pdf_name)
            return send_file(path_file, as_attachment=True, download_name=pdf_name)
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            # Manejar la excepción de archivo no encontrado
            error_message = 'El archivo no se encuentra disponible'
            db.session.delete(ob)
            db.session.commit()
        elif isinstance(e, AttributeError):
            # Manejar la excepción de atributo no encontrado en el objeto 'ob'
            error_message = 'El reporte ha sido eliminado'
        else:
            # Manejar cualquier otra excepción no especificada
            error_message = str(e)

        session['error_message'] = error_message
        return redirect(url_for('verReportes'))
    finally:
        remove(f'app/pdfs/{pdf_name}')



@app.route('/agregarComentario', methods=['GET', 'POST'])
@login_required
def agregarComentario():
    if request.method == 'POST':
        comment = request.form['comentario']
        id_report = request.form['id']
        new_report = Comentario(comentario = comment, id_informe = id_report)
        db.session.add(new_report)
        db.session.commit()
 
        return redirect(url_for('VerInforme',id = id_report))

@app.route('/editarComentario', methods=['GET', 'POST'])
@login_required
def editarComentario():
    if request.method == 'POST':
        comment = request.form['editComentario']
        id_comentario = request.form['id']

        ob_comn = db.session.query(Comentario).filter_by(id_Comentario = id_comentario).first()

        id_report = ob_comn.id_informe

        ob_comn.comentario = comment
        db.session.commit()

        return redirect(url_for('VerInforme',id = id_report))

@app.route('/eliminarComentario', methods=['GET', 'POST'])
@login_required
def eliminarComentario():
    if request.method == 'POST':
        id_comentario = request.form['id']

        ob_comn = db.session.query(Comentario).filter_by(id_Comentario = id_comentario).first()
        id_report = ob_comn.id_informe

        db.session.delete(ob_comn)
        db.session.commit()

        return redirect(url_for('VerInforme',id = id_report))    

@app.route('/registrarUsuario', methods = ['GET', 'POST'] )
def registrarUsuario():
    form = FormRegistro()
    if form.validate_on_submit():
        mail= form.correo.data
        contraseña = form.contraseña.data

        mailc = db.session.query(Usuario).filter_by(email = mail).order_by(Usuario.email).first()
        if mailc:
            return 'Usuario con registro'
        else:
            #hashear contraseña
            usuario = {'mail': mail, 'contraseña':contraseña, 'flag': 1}
            #redirencionar a verififcar codigo
            session['usuario'] = usuario
            return redirect(url_for('verificarCodigo'))
    else:
        print("El formulario no pasó la validación")
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error en el campo {fieldName}: {err}")
    return render_template('registroUsuarios.html', form = form)




@app.route('/verificarCodigo', methods = ['GET', 'POST'])
def verificarCodigo():
    form = FormVerfificacion()
    usuario = session.get('usuario')
   
    if usuario['flag']:
        flag = usuario['flag']
        print ('Existe la flag')
        if flag == 1:
            if form.is_submitted():
                codigo = form.codigo.data
                codigoSend = session.get('codigo')
                mail = usuario['mail']
                contrasenia = generate_password_hash(usuario['contraseña'])  # Encriptar la contraseña
                mailc = db.session.query(Usuario).filter_by(email = mail).order_by(Usuario.email).first()
                if mailc:
                    return 'Usuario con registro'
                else:
                    if int(codigo) == int(codigoSend):
                        tipo_usuario_obj = db.session.query(TipoUsuario).filter_by(id_TipoUsuario=2).order_by(TipoUsuario.id_TipoUsuario).first()
                        new_user = Usuario(email = mail,codigoSecreto = generate_password_hash(str(codigo)), contrasenia = contrasenia, tipoUsuario = tipo_usuario_obj)  # Encriptar el código
                        db.session.add(new_user)
                        db.session.commit()
                        duration = timedelta(seconds=180)
                        ob_codi = db.session.query(Usuario).filter_by(email=mail).first()
                        login_user(ob_codi, remember=True, duration=duration)
                        return redirect(url_for('index'))
                    else:
                        flash('El código no coincide. Por favor, inténtalo de nuevo.')
                        session['codigo'] = codigoSend   # Encriptar el código
                        session['usuario'] = usuario
                        return render_template('verificarCodigo.html', form = form)
            else:
                print("El formulario no pasó la validación")
                usuario = session.get('usuario')
                mail = usuario['mail']
                codigoSend = generarCodigo()
                send_verification_email(mail, codigoSend, mailapp)
                session['codigo'] = codigoSend   # Encriptar el código
                session['usuario'] = usuario
                return render_template('verificarCodigo.html', form = form)
        if flag == 2:
            if form.is_submitted():
                codigo = form.codigo.data
                codigoSend = session.get('codigo')
                usuario = session.get('usuario')
                mail = usuario['mail']
                print(codigo)
                print(type(codigo))
                if int(codigo) == int(codigoSend):
                    ob_codi = db.session.query(Usuario).filter_by(email=mail).first()
                    ob_codi.codigoSecreto = generate_password_hash(str(codigo))
                    db.session.commit()
                    # Iniciar sesión del usuario
                    duration = timedelta(seconds=180)
                    login_user(ob_codi, remember=True, duration=duration)
                    return redirect(url_for('index'))
                else:
                    flash('El código no coincide. Por favor, inténtalo de nuevo.')
                    session['codigo'] = codigoSend   # Encriptar el código
                    session['usuario'] = usuario
                    return render_template('verificarCodigo.html', form = form)
            else:
                print("El formulario no pasó la validación")
                usuario = session.get('usuario')
                mail = usuario['mail']
                codigoSend = generarCodigo()
                send_verification_email(mail, codigoSend, mailapp)
                session['codigo'] = codigoSend   # Encriptar el código
                session['usuario'] = usuario
                return render_template('verificarCodigo.html', form = form)
    else:
        return 'Error'
    


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = FormLogin()
    if form.is_submitted():
        correo = form.correo.data
        contraseña = form.contraseña.data
        mailc = db.session.query(Usuario).filter_by(email = correo).order_by(Usuario.email).first()
        if mailc and check_password_hash(mailc.contrasenia, contraseña):  # Comprobar la contraseña encriptada
            usuario = {'mail': correo, 'flag': 2}
            session['usuario'] = usuario
            return redirect(url_for('verificarCodigo'))
        else:
            flash('La contraseña o el usuario son incorrecto')
    return render_template('login.html', form = form)





@app.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))  # Puedes redirigir a cualquier ruta después del cierre de sesión


@app.before_request
def before_request():
    # Verificar si el usuario está autenticado y configurar el tiempo de inactividad
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    elif 'last_seen' in session and (datetime.utcnow() - session['last_seen']).seconds > 1800:
        logout_user()
        session.clear()
        return redirect(url_for('login'))
    

@app.route('/eliminarInforme', methods=['GET', 'POST'])
@login_required
def eliminarInforme():
    try:

        if request.method == 'POST':
            id = request.form['id']

            print(id)

            ob_comn = db.session.query(Informe).filter_by(id_Informe = id).first()

            data_informe = ob_comn.json_name
            nombre_archivo = 'app/json/' + data_informe
            db.session.delete(ob_comn)
            db.session.commit()
            remove(nombre_archivo)


            return redirect(url_for('verReportes')) 
    except Exception as e:
        print (e)
        return redirect(url_for('verReportes'))

@app.route('/test_connection')
def test_connection():
    try:
        response = requests.get('http://tinyurl.com', timeout=10)
        return f"Status Code: {response.status_code}", 200
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}", 500


    
    
    
    
    

        

        







    
