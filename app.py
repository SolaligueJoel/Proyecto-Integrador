from flask.helpers import flash, url_for
from werkzeug.utils import redirect
import traceback
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, Response
from flask_login import LoginManager,login_required,login_user,logout_user,current_user
from config import config
import os
import localidad
import pytz
from users import User
import users


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY']='thisisasecretkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db_config = config('db', config_path_name)
server_config = config('server', config_path_name)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"

localidad.db.init_app(app)
users.db.init_app(app)


"""
TAREA

VERIFICAR ERRORES DE PRECIO price max < price min
enviar error del servidor al html
README GITHUB

"""





#-----------------------------INDEX-----------------------------#

@app.route("/")
def index():
    try:
        if os.path.isfile(db_config['database']) == False:
            localidad.create_schema()
            users.create_schema()
        return redirect(url_for('signup'))
    except:
        return jsonify({'trace': traceback.format_exc()})


#-----------------------------LOGIN-----------------------------#

@app.route("/login",methods=['GET','POST']) 
def login():
    if request.method == 'GET':
        try:
            return render_template('login.html')
        except:
            return jsonify({'trace': traceback.format_exc()})
    if request.method == 'POST':
        try:
            user_name = str(request.form.get('user_name'))            
            check_user= users.validar_user(user_name)
            password = request.form.get('password')

      
            if check_user is not None and check_user.check_password(password):
                login_user(check_user)
                flash(f'Hola {user_name}!')
                return render_template('home.html')
            
            elif not check_user:
                flash(' Usuario incorrecto!')
                return render_template('login.html')
            
            elif check_user.check_password(request.form.get('password')) is False:
                flash(' La contraseña no coincide con el usuario')
                return render_template('login.html')
            else:
                flash(' Los datos ingresados no son corretos.')
                return render_template('login.html')
        except:
            return jsonify({'trace': traceback.format_exc()})
        

#-----------------------------SIGNUP-----------------------------#

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        try:
            return render_template('signup.html')        
        except:
            return jsonify({'trace': traceback.format_exc()})
    if request.method == 'POST':
        try:
            time1 = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
            time = time1.strftime('%d/%m/%Y | %H:%M')

            user_name = request.form.get('user_name')
            email = request.form.get('email')
            password = request.form.get('password')
                        
            check_user = users.validar_user(user_name)
            check_email = users.validar_email(email)
            
            if check_user:
                flash(f'El Usuario "{user_name}" ya se encuentra registrado!')
                return render_template('signup.html')
            
            elif check_email:
                flash(f'El email "{email}" ya se encuentra registrado!')
                return render_template('signup.html') 
                           
            new_user = User(user_name,email,password,time)
            users.insert(new_user)
            login_user(new_user)
            flash(f'Hola {user_name}!')

            return render_template('home.html')
    
        except:
            return jsonify({'trace': traceback.format_exc()})
     
     
@login_manager.user_loader
def load_user(user_id):
    return users.user_id(user_id)     


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')
    
          

#--RESET TABLE USER 
@app.route("/resetear")
@login_required
def resetear():
    users.create_schema()
    return ("Base de datos regenerada")

    

#----------------------------- TABLA LOCALIDADES -----------------------------#

@app.route("/home",methods=['GET','POST'])
@login_required
def meli():
    if request.method == 'GET':
        try:
            return render_template('home.html')
        except:
            return jsonify({'trice': traceback.format_exc()})
    if request.method == 'POST':
        try:
            time1 = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
            time = time1.strftime('%d/%m/%Y, %H:%M')
            location = str(request.form.get('location'))
            price_min = str(request.form.get('price_min'))
            price_max = str(request.form.get('price_max'))
            if (location is None or price_min.isdigit() and price_max.isdigit() is False):
                return Response(status=400)
            localidad.insert(location,int(price_min),int(price_max),time)
            
            min = int(price_min)
            max = int(price_max)
            dataset = localidad.fetch(location)
            data = localidad.transform(dataset,min,max)
            encoded_img = localidad.grafico(data,location)
            return render_template('grafico.html',overview_graph=encoded_img)
           
        except:
            return jsonify({'trace': traceback.format_exc()})

#-----------------------------TABLA LOCALIDADES-----------------------------#
@app.route("/localidades")
@login_required
def localidades():
    if request.method == 'GET':
        try:
            data = localidad.report()
            return render_template('tabla.html',data = data)        
        except:
            return jsonify({'trace': traceback.format_exc()})
    if request.method == 'POST':
        try:
            time1 = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
            time = time1.strftime('%d/%m/%Y, %H:%M')
            location = str(request.form.get('location'))
            price_min = str(request.form.get('price_min'))
            price_max = str(request.form.get('price_max'))
            if (location is None or price_min.isdigit() and price_max.isdigit() is False):
                return Response(status=400)
            localidad.insert(location,int(price_min),int(price_max),time)   
        except:
            return jsonify({'trace': traceback.format_exc()}) 
        


#--RESET TABLE LOCALIDADES 
@app.route("/reset")
@login_required
def reset():
    try:
        localidad.create_schema()
        result = "<h3> Base de datos re-generada!</h3>"
        return render_template('tabla.html')
    except:
        return jsonify({'trade': traceback.format_exc()})


if __name__ == '__main__':
    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)
