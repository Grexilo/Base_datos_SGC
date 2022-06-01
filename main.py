from SGC import consultaSGC, joint_data, send_mail
import glob
import pandas as pd
from obspy import UTCDateTime

""" Parametros para la descarga del SGC """
TimeRecordBefore = 1
TimeRecordAfter = 10
MinMagnitud = 1
MaxMagnitud = 9
MinDepth = 0
MaxDepth = 200
MinLatitud = 6
MaxLatitud = 7.5
MinLongitud = -74
MaxLongitud = -72

# files = glob.glob('E:/improve_code/*.xlsx')
files = glob.glob('/media/hdd/Data/SGC/Sismicidad/2018/*.xlsx')
print(files)

# pick_path = 'E:/improve_code/Picks_2018_2022.csv'
picks = pd.read_pickle('/media/hdd/Data/SGC/Picks_2018_2022.pkl')

for f in files:
    print(f)
    try:
        consulta = consultaSGC(f, TimeRecordBefore, TimeRecordAfter, MinMagnitud, MaxMagnitud, MinDepth, MaxDepth, MinLatitud,
                    MaxLatitud, MinLongitud, MaxLongitud)
        print(type(consulta))

        data_path = f.split('.')
        data_path = data_path[0] + '.pkl'
        print('data path: ' + data_path)

        picados, no_picados, total_rows = joint_data(consulta, picks, data_path)

        subject = 'Done File'
        info = 'File: {} \n Total datos picados: {} \n Total datos sin picar: {} \n ' \
               'Total filas: {}'.format(f, picados, no_picados, total_rows)

        send_mail(subject, info)

    except:
        #print('\n\nfallo')
        subject = 'Some Error'
        info = 'There was an error in file' + f
        send_mail(subject, info)
