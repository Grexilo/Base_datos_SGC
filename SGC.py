from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import URL_MAPPINGS
from obspy.core import UTCDateTime, trace
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots, figure, subplot, plot
from mpl_toolkits import mplot3d
from math import log
from shapely.geometry import Point
import geopandas
from obspy import read
from tqdm import tqdm
import smtplib
from email.message import EmailMessage


def consultaSGC(f, TimeRecordBefore, TimeRecordAfter, MinMagnitud, MaxMagnitud, MinDepth, MaxDepth, MinLatitud,
                MaxLatitud, MinLongitud, MaxLongitud):
    # print('cal_ini:{} \t'.format(cal_ini.get_date()), end='')
    # print('cal_end:{}'.format(cal_end.get_date()), end='')
    # print('')
    global listaStrems, data

    timeRecordBefore = 60 * int(TimeRecordBefore)  # en segundos
    timeRecordAfter = 60 * int(TimeRecordAfter)  # en segundos
    minMagnitud = float(MinMagnitud)  # 5.0
    maxMagnitud = float(MaxMagnitud)  # 5.8
    canalBusqueda = 'HH?'
    minDepthBusqueda = float(MinDepth)
    maxDepthBusqueda = float(MaxDepth)

    minLatitudBusqueda = float(MinLatitud)
    maxLatitudBusqueda = float(MaxLatitud)
    minLongitudBusqueda = float(MinLongitud)
    maxLongitudBusqueda = float(MaxLongitud)

    print("\nInformacion ingresada:")
    print("minMagnitud:{}".format(minMagnitud))
    print("maxMagnitud:{}".format(maxMagnitud))
    print("timeRecordBefore:{}".format(timeRecordBefore))
    print("timeRecordAfter:{}".format(timeRecordAfter))
    print("canalBusqueda:{}".format(canalBusqueda))
    print("minDepthBusqueda:{}".format(minDepthBusqueda))
    print("maxDepthBusqueda:{}".format(maxDepthBusqueda))
    print("minLatitudBusqueda:{}".format(minLatitudBusqueda))
    print("maxLatitudBusqueda:{}".format(maxLatitudBusqueda))
    print("minLongitudBusqueda:{}".format(minLongitudBusqueda))
    print("maxLongitudBusqueda:{}\n".format(maxLongitudBusqueda))

    try:
        # Lectura archivo excel
        data = pd.read_excel(f)
        data2 = data.copy()

        if 'HORA_UTC' in data:
            data2["FECHA"] = data["FECHA"] + " " + data["HORA_UTC"]
        else:
            data2["FECHA"] = data["FECHA"]

        data2 = data[
            (data['MAGNITUD'] >= minMagnitud) &
            (data['MAGNITUD'] <= maxMagnitud) &
            (data['PROFUNDIDAD'] >= minDepthBusqueda) &
            (data['PROFUNDIDAD'] <= maxDepthBusqueda) &
            (data['LATITUD'] >= minLatitudBusqueda) &
            (data['LATITUD'] <= maxLatitudBusqueda) &
            (data['LONGITUD'] >= minLongitudBusqueda) &
            (data['LONGITUD'] <= maxLongitudBusqueda)]

        # print(data)
        # print(data2)

        zdata = data2['PROFUNDIDAD'].to_numpy()
        xdata = data2['LONGITUD'].to_numpy()
        magdata = data2['MAGNITUD'].to_numpy()
        ydata = data2['LATITUD'].to_numpy()

        # print(data2['LATITUD'].describe())
        # print(data2['LONGITUD'].describe())
        # print(data2['PROFUNDIDAD'].describe())
        # print(data2['MAGNITUD'].describe())

    except:
        # messagebox.showerror(message="No se encontraron eventos", title="Error")
        return None

    listNetwork = []
    listStation = []
    listLocation = []
    listStartTime = []
    listEndTime = []
    listChannel = []
    listSampling_rate = []
    listDelta = []
    listNpts = []
    listEvenTime = []
    listXEventdata = []
    listZEventdata = []
    listYEventdata = []
    listMagEventdata = []
    listLatitudStation = []
    listLongitudStation = []
    listData = []
    listaStrems = []

    # Filtrar estaciones
    dataEstaciones = pd.read_excel('/media/hdd/Data/SGC/Estaciones/estaciones.xlsx')
    # dataEstaciones = pd.read_excel('E:/tg2_codes/srcDataSGC_GUI_New/Estaciones/estaciones.xlsx')
    if (canalBusqueda == "BH?" or canalBusqueda == "HH?"):
        df_mask = dataEstaciones[
            (dataEstaciones[
                 'Localizador'] == 0) &  # El localizador esta definido en 0 pero podria ser 10 para un acelerometro
            (dataEstaciones['Latitud'] >= minLatitudBusqueda) &
            (dataEstaciones['Latitud'] <= maxLatitudBusqueda) &
            (dataEstaciones['Longitud'] >= minLongitudBusqueda) &
            (dataEstaciones['Longitud'] <= maxLongitudBusqueda) &
            ((dataEstaciones['Canal'] == canalBusqueda[:-1] + "E") |
             (dataEstaciones['Canal'] == canalBusqueda[:-1] + "N") |
             (dataEstaciones['Canal'] == canalBusqueda[:-1] + "Z"))]

    else:
        df_mask = dataEstaciones[
            (dataEstaciones[
                 'Localizador'] == 0) &  # El localizador esta definido en 0 pero podria ser 10 para un acelerometro
            (dataEstaciones['Latitud'] >= minLatitudBusqueda) &
            (dataEstaciones['Latitud'] <= maxLatitudBusqueda) &
            (dataEstaciones['Longitud'] >= minLongitudBusqueda) &
            (dataEstaciones['Longitud'] <= maxLongitudBusqueda) &
            (dataEstaciones['Canal'] == canalBusqueda)]

    # print(df_mask['Estacion'])
    strEstaciones = ""
    setEstaciones = set()

    for strDfEsta in df_mask['Estacion']:
        strEstaciones += strDfEsta + ","
        setEstaciones.add(strDfEsta)

    strEstaciones = strEstaciones[:-1]
    str_val = ','.join(list(map(str, setEstaciones)))
    #print("Estaciones encontradas en la zona seleccionada:")
    #print(str_val)
    #print("found %s event(s):" % len(data2))
    #print(data['FECHA'])
    #print(data2.columns.values.tolist())

    for i in tqdm(data2.index):
        # for i in tqdm(range(2)):

        # print(data2['FECHA'][i])
        strTime = data2['FECHA'][i].replace(" ", "T")
        eventTime = UTCDateTime(strTime)
        startTime = eventTime - timeRecordBefore
        endTime = eventTime + timeRecordAfter

        zdata = data2['PROFUNDIDAD'][i]
        xdata = data2['LONGITUD'][i]
        magdata = data2['MAGNITUD'][i]
        ydata = data2['LATITUD'][i]

        # print (strTime)
        # print (str(startTime)[:-1])
        # print (str(endTime)[:-1])

        # LLamado al URL de la base de datos del SGC
        URL = "http://sismo.sgc.gov.co:8080/fdsnws/dataselect/1/query?starttime=" + str(startTime)[
                                                                                    :-1] + "&endtime=" + str(endTime)[
                                                                                                         :-1] + "&network=CM&sta=" + str_val + "&cha=" + canalBusqueda + "&loc=00&format=miniseed&nodata=404"
        # URL = "http://sismo.sgc.gov.co:8080/fdsnws/dataselect/1/query?starttime="+str(startTime)[:-1]+"&endtime="+str(endTime)[:-1]+"&network=CM&sta=*&cha=HHZ&loc=*&format=miniseed&nodata=404"

        try:
            st = read(URL)
            # print(str_val)
            # print(st.__str__(extended=True))

            for stream in st:
                # print(stream.stats.station)
                listNetwork.append(stream.stats.network)
                listStation.append(stream.stats.station)

                df2 = df_mask[df_mask['Estacion'] == str(stream.stats.station)]

                for lat in df2['Latitud']:
                    latitudStation = lat

                for lon in df2['Longitud']:
                    longitudStation = lon

                listLatitudStation.append(latitudStation)
                listLongitudStation.append(longitudStation)

                listLocation.append(stream.stats.location)

                listChannel.append(stream.stats.channel)
                listStartTime.append(stream.stats.starttime)
                listEndTime.append(stream.stats.endtime)
                listSampling_rate.append(stream.stats.sampling_rate)
                listDelta.append(stream.stats.delta)
                listNpts.append(stream.stats.npts)
                listEvenTime.append(eventTime)
                listZEventdata.append(zdata)
                listXEventdata.append(xdata)
                listYEventdata.append(ydata)
                listMagEventdata.append(magdata)
                listData.append(stream.data)
                listaStrems.append(stream)
                # print(listaStrems)
                # print(listData)
                # print(stream.data)





        except:
            # print(st)
            print("\nRegistro no encontrado\n")

    ########################################

    points_df = pd.DataFrame(list(zip(listNetwork, listStation, listLatitudStation, listLongitudStation,
                                      listLocation, listChannel,
                                      listStartTime, listEndTime,
                                      listSampling_rate, listDelta, listNpts,
                                      listEvenTime, listZEventdata, listXEventdata, listYEventdata, listMagEventdata,
                                      listData)),
                             columns=['Network', 'Station', 'LatStation', 'LongStation', 'Location', 'Channel',
                                      'Starttime', 'Endtime', 'Samplingrate', 'Delta', 'Npts', 'Eventime', 'DepthEvent',
                                      'LongEvent', 'LatEvent', 'MagEvent', 'Data'])

    #print(points_df['LatStation'].describe())
    #print(points_df)
    print("Se finalizo la consulta")
    #path = f.split('.')
    #path = path[0] + '.pkl'
    #points_df.to_pickle(path)
    #print('GUARDADO')
    return points_df
    # print(st[0].stats)

    '''Estaciones en Colombia'''
    # print("Estaciones en Colombia")
    # print (client.get_stations(network="CM"))

def joint_data(consulta_df, info_csv, path):
    """
    Args:
        consulta_df: dataframe from consultasgc
        info_csv: dataframe cargado partiendo del csv por parte del SGC

    Returns:
        traces: regresa el dataframe con toda la informacion
    """

    consulta_df['Eventime'] = consulta_df['Eventime'].apply(lambda x: x.isoformat())

    imp_columns = ['event_time_value', 'pick_time_value', 'waveformID_channelCode', 'waveformID_stationCode',
                   'publicID', 'phase_code', 'pick_time_value', 'time_value_ms']

    new_data = consulta_df.join(info_csv[imp_columns].set_index(['event_time_value', 'waveformID_stationCode', 'waveformID_channelCode']),
                on=['Eventime', 'Station', 'Channel'], lsuffix='sgc', rsuffix='csv')

    picados = new_data[(new_data.phase_code == 'P') | (new_data.phase_code == 'S')].shape[0]
    no_picados = new_data[(new_data.phase_code != 'P') | (new_data.phase_code != 'S')].shape[0]
    total_rows = new_data.shape[0]

    new_data.to_pickle(path)

    return picados, no_picados, total_rows

def make_trace(data):
    """

    Parameters
    ----------
    data : A row from a dataframe - A series from pandas
        Dataframe with all the information

    Returns
    -------
    trace : Return a obspy trace

    """
    tr = trace.Trace(data.Data)
    # Add the correct stats for the trace
    tr.stats.network = data.Network
    tr.stats.location = data.Location
    tr.stats.channel = data.Channel
    tr.stats.station = data.Station
    tr.stats.starttime = UTCDateTime(data.Starttime)
    tr.stats.sampling_rate = data.Samplingrate
    tr.stats.npts = data.Npts
    tr.stats.phase_code = data.phase_code
    tr.stats.phase_time = UTCDateTime(data.pick_time_value)

    return tr

def graph_trace(trace):
    """

    Parameters
    ----------
    trace : Obpsy trace previusly generated

    Returns
    -------
    None.
    The idea is tha this function does the graphic part to check the data

    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(trace.times("matplotlib"), trace.data, "b-")
    ax.xaxis_date()
    fig.autofmt_xdate()
    ax.axvline(trace.stats.phase_time, color='r', linestyle='--', lw=2,
               label='Onda {}'.format(trace.stats.phase_code))
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
    plt.show()

def send_mail(subject, info):
    """
    Args:
        subject: Subject of the mail
        info: The information from the mail

    Returns:
        None - Just send an email
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'mvarbla9825@gmail.com'
    msg['To'] = 'miguel2171521@correo.uis.edu.co,miguelvarbla@gmail.com'

    msg.set_content(info)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('mvarbla9825@gmail.com', 'omxfnnekyyozjqjm')
        smtp.send_message(msg)

    print('Correo enviado')
