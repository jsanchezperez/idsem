"""
  Invoice token generator
"""
import string
from ast import literal_eval
import numpy as np
import time
import json
import calendar


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    stime = time.mktime(time.strptime(start, "%d/%m/%Y"))
    etime = time.mktime(time.strptime(end, "%d/%m/%Y"))

    ptime = stime + np.random.random() * (etime - stime)

    return ptime


def random_nif():
    """
    This function will return a random NIF with the correct format.
    """
    nif_letter = literal_eval(open("dictionaries/nif_letter.txt").read())
    nif = np.random.randint(10 ** 7, 10 ** 8)
    let = nif_letter[str(nif % 23)]
    return str(nif) + let


def generate_client_info(data, data_dir):
    """ ... """

    nombres = open(data_dir + "spanish_names.txt", encoding="UTF-8").readlines()
    apellidos = open(data_dir + "spanish_surnames.txt", encoding="UTF-8").readlines()

    poblaciones = open(data_dir + "spanish_villages.txt", encoding="UTF-8").readlines()
    calles = open(data_dir + "spanish_streets.txt", encoding="UTF-8").readlines()

    # 'Name'
    data['B1'] = (np.random.choice(nombres)).replace('\n', '') + ' ' + \
                       (np.random.choice(apellidos)).replace('\n', '') + ' ' + \
                       (np.random.choice(apellidos)).replace('\n', '')

    if np.random.randint(2) == 1:
        data['B1'] = data['B1'].upper()

    # 'NIF'
    data['B2'] = random_nif()

    # 'Address'
    data['B3'] = (np.random.choice(calles)).replace('\n', '')

    # 'Postal Code' 'City' 'Province'
    poblacion = np.random.choice(poblaciones).split(";")
    data['B4'] = poblacion[2].replace('"', '').replace('\n', '')
    data['B5'] = poblacion[1].replace('"', '')
    data['B6'] = poblacion[0].replace('"', '')

    data['A1'] = data['B1']
    data['A2'] = data['B2']
    data['A3'] = data['B3']
    data['A4'] = data['B4']
    data['A5'] = data['B5']
    data['A6'] = data['B6']



def generate_marketer_csv_info(data, data_dir):
    """ ... """

    comercializadoras = [line.replace('\n', '') for line in
                         open(data_dir + "spanish_marketers.csv", encoding="UTF-8").readlines()]

    com = np.random.choice(comercializadoras)

    # "Nombre_Comercializadora"
    data['C1'] = com.split(";")[1]

    # "CIF_Comercializadora"    
    data['C2'] = com.split(";")[8]       

    # "Direccion_Comercializadora"
    data['C3'] = com.split(";")[2]

    # "CP_Comercializadora"
    data['C4'] = com.split(";")[3]

    # "Poblacion_Comercializadora"
    data['C5'] = com.split(";")[4]

    # "Provincia_Comercializadora"
    data['C6'] = com.split(";")[5]

    # "Registro_Mercantil_Comercializadora":
    data['C7'] = data['C6'] + ", tomo " + str(np.random.randint(50000)) + ", folio " + \
        str(np.random.randint(100)) + ", sección " + str(np.random.randint(10)) + \
        ", hoja número M-" + str(np.random.randint(300000)) + ", inscripción " + \
        str(np.random.randint(200))

    # "Domicilio_Social_Comercializadora":
    data['C8'] = data['C3'] + ", " + data['C4'] + " - " + data['C6']

    # "Web_Comercializadora":       
    data['C9'] = com.split(";")[11]

    # "Email_Comercializadora":
    x = data['C9'].rsplit("www.", 1)

    if len(x) > 1:
        email = "atencionalcliente@" + x[1]
    else:
        email = "" 

    data['CA'] = email                

    # "Nombre_Corto_Comercializadora":
    data['CB'] = data['C1']

    # "Telefono_atencion_publico_Comercializadora"
    telephone = com.split(";")[6]        
    data['CC'] = telephone

    # "Telefono_averias_Comercializadora":
    x = np.random.randint(100)
    data['CD'] = telephone[:-3] + str(x).zfill(3)    

    # "Telefono_RECLAMACIONES_Comercializadora":
    x = np.random.randint(100)
    data['CE'] = telephone[:-3] + str(x).zfill(3)     


def generate_distributor_info(data, data_dir):
    """ ... """
    distribuidoras = [line.replace('\n', '') for line in
                      open(data_dir + "spanish_distributors.csv", \
                          encoding="UTF-8").readlines()]

    dist = np.random.choice(distribuidoras)

    # "Nombre_Distribuidora":
    data['D1'] = dist.split(";")[2].replace('\n', '')   

    # "CIF_Distribuidora":
    data['D2'] = dist.split(";")[0]         

    # "Web_Distribuidora":
    data['D9'] = dist.split(";")[4]   

    # "Telefono_atencion_publico_Distribuidora"
    telephone = dist.split(";")[3]    
    data['DC'] = telephone            

    # "Telefono_averias_Distribuidora":
    x = np.random.randint(100)
    data['DD'] = telephone[:-2] + str(x).zfill(2) 



def generate_agreement_info(data, tmpdata, dates_info):
    """ ... """
    # 'CUPS'
    data['E1'] = 'ES' + str(np.random.randint(10 ** 15, 10 ** 16, dtype=np.int64))
    letters = list(string.ascii_uppercase)
    data['E1'] += ''.join(np.random.choice(letters) for i in range(4))

    # 'PotenciaContratada'
    tmp = np.random.normal(4,1)     
    tmpdata['E3l'] = round(tmp, 3)
    data['E3l'] = ("%.3f" % tmpdata['E3l']).replace('.', ',')
    tmpdata['E3'] = round(tmp, 2) 
    data['E3'] = ("%.2f" % tmpdata['E3']).replace('.', ',')

    # "Numero_Contrato"
    data['E4'] = str(np.random.randint(10 ** 11, 10 ** 12, dtype=np.int64))

    # "Numero_Contador" 
    data['E5'] = str(np.random.randint(10 ** 8, 10 ** 9, dtype=np.int64))

    # 'PeajeAcceso'
    a = np.array([0.5734, 0.3671, 0.0016, 0.0146, 0.0119, 0.0001, 0.0268])
    data['E6'] = np.random.choice(['2.0A', '2.0DHA', '2.0DHS', '2.1A', '2.1DHA', '2.1DHS', '3.0A'], p=a/np.sum(a))         

    E2 = data['E6'][3:]

    # "Nombre_Tarifa"
    data['E2'] = ""
    if E2 == "A":
        data['E2'] = "PVPC sin discriminación horaria"
    elif E2 == "DHA":
        data['E2'] = "PVPC disc. horaria (2 periodos)"
    elif E2 == "DHS":
        data['E2'] = "PVPC disc. horaria (3 periodos)"
    #print("data['E2']:" + data['E2'])

    # "Fecha_Fin_Suministro":  / "FinContrato"
    date_format_long = '%d de %B de %Y'
    date_format_point = '%d.%m.%Y'
    date_format_slash = '%d/%m/%Y'
    new_date = dates_info['fechainicio'] + dates_info['months'] * dates_info['month_time']
    data['E7s'] = time.strftime(date_format_slash, time.localtime(new_date))
    data['E7p'] = time.strftime(date_format_point, time.localtime(new_date))
    data['E7l'] = time.strftime(date_format_long, time.localtime(new_date))
    data['E7'] = data['E7l']

    # 'CNAE'
    data['E8'] = "9820 Viviendas Particulares. Primera Vivienda"

    # 'Referencia_Contrato_Suministro'
    data['E9'] = str(np.random.randint(10 ** 12, 10 ** 13, dtype=np.int64))



def generate_reading_info(data):
    """ ... """
    lectura_anterior = np.random.randint(0, 100000)

    # 'LecturaAnterior'
    data['I1'] = lectura_anterior
    incremento = int(np.round(np.random.normal(270,200))*data['F6']/30) 
    if incremento<0: incremento = 0

    # 'LecturaActual'
    data['I2'] = lectura_anterior + incremento

    # 'ConsumoActual'
    data['I3'] = incremento



def generate_invoice_info(data, dates_info):
    """ ... """
    date_format_long = '%d de %B de %Y'
    date_format_slash = '%d/%m/%Y'
    date_format_underscore = '%d-%B-%Y'
    date_format_point = '%d.%m.%Y'
    new_date = dates_info['fechainicio'] + dates_info['months'] * dates_info['month_time']
    fecha_emision = time.localtime(new_date + 2 * dates_info['day_time'])
    fecha_inicio = time.localtime(dates_info['fechainicio'])

    # 'Numero_Factura'
    F = np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    if np.random.randint(2) == 1:
        F = F + np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    data['F1'] = F + str(np.random.randint(10 ** 9, 10 ** 10, dtype=np.int64))

    # 'Referencia_Factura'
    data['F2'] = str(np.random.randint(10 ** 11, 10 ** 12, dtype=np.int64)) + "/" \
                 + str(np.random.randint(10 ** 3, 10 ** 4, dtype=np.int64))

    # 'Fecha_Emision'
    data['F3s'] = time.strftime(date_format_slash, fecha_emision)
    data['F3l'] = time.strftime(date_format_long, fecha_emision)
    data['F3p'] = time.strftime(date_format_point, fecha_emision)
    data['F3'] = data['F3l']

    # 'Fecha_Inicio'
    data['F4s'] = time.strftime(date_format_slash, fecha_inicio)
    data['F4u'] = time.strftime(date_format_underscore, fecha_inicio)
    data['F4l'] = time.strftime(date_format_long, fecha_inicio)
    data['F4p'] = time.strftime(date_format_point, fecha_inicio)
    data['F4'] = data['F4l']

    # 'Fecha_Fin'
    data['F5s'] = time.strftime(date_format_slash, time.localtime(new_date))
    data['F5u'] = time.strftime(date_format_underscore, time.localtime(new_date))
    data['F5l'] = time.strftime(date_format_long, time.localtime(new_date))
    data['F5p'] = time.strftime(date_format_point, time.localtime(new_date))
    data['F5'] = data['F5l']

    # 'Dias_Facturados'  'Days'
    data['F6'] = dates_info['days']

    # 'Dias_Ano'
    data['F7'] = 365
    if calendar.isleap(time.localtime(new_date)[0]):
        data['F7'] = 366



def generate_payment_info(data, dates_info, data_dir):
    """ ... """
    date_format_long = '%d de %B de %Y'
    date_format_point = '%d.%m.%Y'
    new_date = dates_info['fechainicio'] + dates_info['months'] * dates_info['month_time']

    # "Forma_Pago"
    data['G1'] = "Domiciliada" # bancaria"

    # "Fecha_Cargo"
    data['G3p'] = time.strftime(date_format_point, time.localtime(new_date \
                 + 5 * dates_info['day_time']))
    data['G3l'] = time.strftime(date_format_long, time.localtime(new_date \
                 + 5 * dates_info['day_time']))
    data['G3'] = data['G3l']

    # "Código_Mandato"
    data['G4'] = 'E' + str(np.random.randint(10 ** 14, 10 ** 15, dtype=np.int64)) + str(np.random.randint(10 ** 10, 10 ** 11, dtype=np.int64))

    # "Versión"
    data['G5'] = str(np.random.randint(10 ** 3, 10 ** 4)).zfill(4)

    bancos = [line.replace('\n', '') for line in
              open(data_dir + "spanish_banks.csv", encoding="UTF-8").readlines()]

    bank = np.random.choice(bancos)

    # 'Entidad'
    data['G6'] = bank.split(";")[7].replace('"', '')
    data['G6'] = data['G6'].replace('\n', '')

    # 'Sucursal'
    data['G7'] = str(np.random.randint(10 ** 2, 10 ** 3)).zfill(4)

    # 'Digito_Control'
    data['G8'] = str(np.random.randint(10 ** 1, 10 ** 2)).zfill(2)

    # 'Cuenta_Corriente'
    data['G9'] = (str(np.random.randint(10 ** 4, 10 ** 5)) + "*****").zfill(10)

    # "IBAN"
    cod_europeo = bank.split(";")[0]
    data['G2'] = cod_europeo + str(np.random.randint(10 ** 1, 10 ** 2)).zfill(2) \
                 + data['G7'] + data['G8'] + data['G9']

    # 'Nombre_banco'
    data['GA'] = bank.split(";")[2].replace('"', '')   



def generate_segment_info(data, tmpdata, ID):
    """ ... """
    percent_days = round(data['F6'] / data['F7'], 6)

    # 'Eurkw_Potencia_Peaje_Acceso_Tramo'
    tmpdata[ID+'2'] = round(np.random.normal(38.043426, 0.5), 6)
    data[ID+'2'] = ("%.6f" % tmpdata[ID+'2']).replace('.', ',')
    tmpdata[ID+'2d'] = round(tmpdata[ID+'2'] / data['F7'], 6)
    data[ID+'2d'] = ("%.6f" % tmpdata[ID+'2d']).replace('.', ',')

    # 'Importe_Potencia_Peaje_Acceso_Tramo1'
    tmp = tmpdata['E3'] * tmpdata[ID+'2'] * percent_days
    tmpdata[ID+'3'] = round(tmp, 2)
    data[ID+'3'] = ("%.2f" % tmpdata[ID+'3']).replace('.', ',')

    # 'Eurkw_Potencia_Coste_Tramo1' 
    tmpdata[ID+'4'] = round(np.random.normal(3.5, 0.5), 6)
    data[ID+'4'] = ("%.6f" % tmpdata[ID+'4']).replace('.', ',')
    tmpdata[ID+'4d'] = round(tmpdata[ID+'4'] / data['F7'], 6)
    data[ID+'4d'] = ("%.6f" % tmpdata[ID+'4d']).replace('.', ',')

    # "Importe_Potencia_Coste_Tramo1"
    tmp = tmpdata['E3'] * tmpdata[ID+'4'] * percent_days
    tmpdata[ID+'5'] = round(tmp, 2)
    data[ID+'5'] = ("%.2f" % tmpdata[ID+'5']).replace('.', ',')

    # 'Eurkw_Potencia_Tramo1'
    tmp = (tmpdata[ID+'2'] + tmpdata[ID+'4']) / data['F7']
    tmpdata[ID+'6'] = round(tmp, 6)
    data[ID+'6'] = ("%.6f" % tmpdata[ID+'6']).replace('.', ',')

    # 'Eurkwh_Energia_Peaje_Acceso_Tramo1'
    value = 0.0
    if data['E6'] == '2.0A':
      value = np.random.normal(0.1263, 0.01263)
    elif data['E6'] == '2.0DHA':
      value = np.random.normal(0.0992, 0.00992)
    elif data['E6'] == '2.0DHS':
      value = np.random.normal(0.0772, 0.00772)
    elif data['E6'] == '2.1A':
      value = np.random.normal(0.1437, 0.01437)
    elif data['E6'] == '2.1DHA':
      value = np.random.normal(0.0899, 0.00899)
    elif data['E6'] == '2.1DHS':
      value = np.random.normal(0.0894, 0.00894)
    elif data['E6'] == '3.0A':
      value = np.random.normal(0.0633, 0.00633)
    tmpdata[ID+'9'] = round(value, 6)
    data[ID+'9'] = ("%.6f" % tmpdata[ID+'9']).replace('.', ',')

    # 'Importe_Energia_Peaje_Acceso_Tramo1'
    tmp = data['I3'] * tmpdata[ID+'9']
    tmpdata[ID+'A'] = round(tmp, 2)
    data[ID+'A'] = ("%.2f" % tmpdata[ID+'A']).replace('.', ',')

    # "PrecioKwh"
    value = 0.0
    if data['E6'] == '2.0A':
      value = np.random.normal(0.1263, 0.01263)
    elif data['E6'] == '2.0DHA':
      value = np.random.normal(0.0992, 0.00992)
    elif data['E6'] == '2.0DHS':
      value = np.random.normal(0.0772, 0.00772)
    elif data['E6'] == '2.1A':
      value = np.random.normal(0.1437, 0.01437)
    elif data['E6'] == '2.1DHA':
      value = np.random.normal(0.0899, 0.00899)
    elif data['E6'] == '2.1DHS':
      value = np.random.normal(0.0894, 0.00894)
    elif data['E6'] == '3.0A':
      value = np.random.normal(0.0633, 0.00633)
    tmpdata[ID+'B'] = round(value, 6)
    data[ID+'B'] = ("%.6f" % tmpdata[ID+'B']).replace('.', ',')

    # "Importe_Energia_Coste_Tramo1"
    tmp = data['I3'] * tmpdata[ID+'B']
    tmpdata[ID+'C'] = round(tmp, 2)
    data[ID+'C'] = ("%.2f" % tmpdata[ID+'C']).replace('.', ',')

    # 'Eurkwh_Energia_Tramo1'
    tmp = tmpdata[ID+'9'] + tmpdata[ID+'B']
    tmpdata[ID+'D'] = round(tmp, 6)
    data[ID+'D'] = ("%.6f" % tmpdata[ID+'D']).replace('.', ',')



def generate_miscellaneous_invoice_info(data, tmpdata):
    """ ... """

    # 'EurDia_AlquilerEquipos'
    rent = np.array([0.03, 0.15, 0.47, 0.54, 0.72, 0.81, 0.91, 1.11, 1.36, 1.53, 1.71, 2.22, 2.79]) 
    rent = np.random.choice(rent)
    tmpdata['M3'] = round(rent, 6)    
    data['M3'] = ("%.6f" % tmpdata['M3']).replace('.', ',')

    rent=rent*12/data["F7"]
    tmpdata['M3d'] = round(rent, 6)    
    data['M3d'] = ("%.6f" % tmpdata['M3d']).replace('.', ',')

    # 'ImporteAlquilerEquipos'
    tmp = tmpdata['M3d'] * data['F6']
    tmpdata['M4'] = round(tmp, 2)
    data['M4'] = ("%.2f" % tmpdata['M4']).replace('.', ',')

    # 'Meses'
    tmp = data['F6'] / 30 # data['L1']) 
    tmpdata['F8l'] = round(tmp, 6) 
    data['F8l'] = ("%.6f" % tmpdata['F8l']).replace('.', ',')

    tmpdata['F8'] = round(tmp, 2) 
    data['F8'] = ("%.2f" % tmpdata['F8']).replace('.', ',')


def generate_invoice_summary_info(data, tmpdata):
    """ ... """
    # 'Importe_Potencia_Contratada'
    tmp = tmpdata['K3'] + tmpdata['K5']
    tmpdata['J1'] = round(tmp,2)
    data['J1'] = ("%.2f" % tmpdata['J1']).replace('.', ',')

    # 'Importe_Energia_Consumida'
    tmp = tmpdata['KA'] + tmpdata['KC']
    tmpdata['J2'] = round(tmp,2)
    data['J2'] = ("%.2f" % tmpdata['J2']).replace('.', ',')

    # "ImporteSubTotal_Potencia_Energia"
    tmp = tmpdata['J1'] + tmpdata['J2']
    tmpdata['J3'] = round(tmp,2)
    data['J3'] = ("%.2f" % tmpdata['J3']).replace('.', ',')

    # 'TipoInteresImpuestoElectricidad'
    tmpdata['N1'] = 0.051127        
    data['N1'] = str(tmpdata['N1']*100).replace('.', ',')

    # 'ImporteImpuestoElectricidad'
    tmp = tmpdata['N1'] * tmpdata['J3']
    tmpdata['N2'] = round(tmp, 2)
    data['N2'] = ("%.2f" % tmpdata['N2']).replace('.', ',')

    # "Importe_Total_Impuestos_Electrico_Alquiler"
    tmp = tmpdata['M4'] + tmpdata['N2']
    tmpdata['N3'] = round(tmp, 2)
    data['N3'] = ("%.2f" % tmpdata['N3']).replace('.', ',')

    # 'Importe_SinImpuestos'
    tmp = tmpdata['J3'] + tmpdata['N3']
    tmpdata['J4'] = round(tmp,2)
    data['J4'] = ("%.2f" % tmpdata['J4']).replace('.', ',')

    # 'ImpuestoNormal'
    taxes=[6.5, 7, 10, 21]
    tmpdata['N4'] = np.random.choice(taxes)
    if tmpdata['N4']>6.5: tmpdata['N4']=round(tmpdata['N4'])
    data['N4'] = str(tmpdata['N4']).replace('.', ',')

    # 'ImporteImpuestoNormal'
    tmp = tmpdata['M4'] * tmpdata['N4'] / 100
    tmpdata['N5'] = round(tmp, 2)
    data['N5'] = ("%.2f" % tmpdata['N5']).replace('.', ',')

    # 'ImpuestoReducido'
    taxes=[1, 2, 3, 5, 6.5, 7, 10, 15, 21]
    tmpdata['N6'] = np.random.choice(taxes)
    if tmpdata['N6']!=6.5: tmpdata['N6']=round(tmpdata['N6'])
    data['N6'] = str(tmpdata['N6']).replace('.', ',')

    # 'Importe_Potencia_Coste_ImpElectricidad':
    tmp = tmpdata['K3'] + tmpdata['K5'] 
    tmp += tmpdata['KA'] + tmpdata['KC'] 
    tmp += tmpdata['N2']
    tmpdata['N7'] = round(tmp, 2)
    data['N7'] = ("%.2f" % tmpdata['N7']).replace('.', ',')

    # 'ImporteImpuestoReducido'
    tmp = tmpdata['N7'] * tmpdata['N6'] / 100.0
    tmpdata['N8'] = round(tmp, 2)
    data['N8'] = ("%.2f" % tmpdata['N8']).replace('.', ',')

    # 'Importe_Total'
    tmp = tmpdata['J4'] + tmpdata['N8'] + tmpdata['N5']
    tmpdata['J5'] = round(tmp,2)
    data['J5'] = ("%.2f" % tmpdata['J5']).replace('.', ',')


def label_randomizer():
    """ ... """
    data_directory = "dictionaries/"

    dates_info = {}

    dates_info['fechainicio'] = random_date("01/01/1990", "31/12/2021")
    dates_info['month_time'] = 2592000
    dates_info['day_time'] = 86400
    dates_info['months'] = np.random.randint(1, 3)
    dates_info['days'] = 30 * dates_info['months']

    result = {}
    tmpresult = {}

    generate_client_info(result, data_directory)
    generate_marketer_csv_info(result, data_directory)
    generate_distributor_info(result, data_directory)
    generate_agreement_info(result, tmpresult, dates_info)

    generate_invoice_info(result, dates_info)
    generate_miscellaneous_invoice_info(result, tmpresult)    
    generate_reading_info(result)

    generate_payment_info(result, dates_info, data_directory)
    generate_segment_info(result, tmpresult, 'K')
    
    generate_invoice_summary_info(result, tmpresult)

    return result



def gen_json(json_fn):
    """ ... """
    result = label_randomizer()

    with open(json_fn, 'w', encoding="utf-8") as json_file:
        json.dump(result, json_file, sort_keys=True, indent=2, ensure_ascii=False)
