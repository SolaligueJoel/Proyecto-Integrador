from flask.wrappers import Response
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker, relationship
from sqlalchemy import func
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


from time import gmtime, strftime
import requests
import matplotlib.pyplot as plt
from werkzeug.utils import send_file

db = SQLAlchemy()

class Localidad(db.Model):
    __tablename__ = "localidad"
    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String)
    price_min = db.Column(db.Integer)
    price_max = db.Column(db.Integer)
    time = db.Column(db.String)
    
    
    def __repr__(self):
        return f"Location:{self.location} price min: {self.price_min} precio max: {self.price_max} time: {self.time}"
    

def create_schema():
    db.drop_all()
    db.create_all()

def insert(location,price_min,price_max,time):
    location = Localidad(location = location, price_min = price_min, price_max = price_max,time=time)
    db.session.add(location)
    db.session.commit()


def fetch(location):
    url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q=Departamentos%20Alquilers%20{}%20&limit=50'.format(location)
    response = requests.get(url)
    data_json = response.json()
    new_data = data_json["results"]
    
    #Filtrando lista en pesos
    new_list = [{"price":x["price"], "condition":x["condition"]} for x in new_data if x.get("currency_id") == "ARS"]

    return new_list



def transform(new_data,min,max):
    #Realizando listas por valor minimo, intermedio y maximo
  
    precio_min = [int(x["price"]) for x in new_data if x.get("price")< min]
    precio_min_max = [int(x["price"]) for x in new_data if x.get("price")>min and x.get("price")< max]
    precio_max = [int(x["price"]) for x in new_data if x.get("price")>max]
    return [len(precio_min),len(precio_min_max),len(precio_max)]
    





def report(limit=0, offset=0):
    # Obtener todas las personas
    #query = db.session.query(Localidad).filter(Localidad.location == location)
    query= db.session.query(Localidad)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Persona podría tener una función
    # para pasar a JSON/diccionario
    for person in query:
        json_result = {'Localidad': person.location,'Price_min': person.price_min, 'Price_max': person.price_max, 'Time':person.time}
        json_result_list.append(json_result)

    return json_result_list

def grafico(data,location): 

    #Pie Plot
    fig = Figure(figsize=(10,5))
    fig.tight_layout()
    ax = fig.add_subplot()
    ax.set_title('Cantidad Alquileres en {}'.format(location),fontsize=27)
    
    label = ['Valor minimo','Valor intermedio','Valor maximo']
    colors = ['#90EE90','#FDD835','#B03A2E']
    label2 = [f'Alq,Dep por debajo del valor minimo: {data[0]}', f'Alq,Dep entre los precios min y max: {data[1]}',f'Alq,Dep que superan el valor maximo: {data[2]}']

    ax.set_xlim(0,10)
    ax.pie(data,labels= label, wedgeprops={'edgecolor':'black'}, autopct='%0.0f%%', colors=colors)
    ax.legend(label2,loc=1,fontsize=8)
    ax.axis('equal')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    encoded_img = base64.encodebytes(output.getvalue())
    plt.close(fig)
    return encoded_img
    #return Response(output.getvalue(),mimetype='image/png')
    
