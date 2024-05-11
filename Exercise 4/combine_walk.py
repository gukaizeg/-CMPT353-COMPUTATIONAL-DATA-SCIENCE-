import os
import pathlib
import sys
import numpy as np
import pandas as pd
from xml.etree.ElementTree import ElementTree

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation, parse
    xmlns = 'http://www.topografix.com/GPX/1/0'
    
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.10f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.10f' % (pt['lon']))
        time = doc.createElement('time')
        time.appendChild(doc.createTextNode(pt['datetime'].strftime("%Y-%m-%dT%H:%M:%SZ")))

        trkpt.appendChild(time)
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    doc.documentElement.setAttribute('xmlns', xmlns)

    with open(output_filename, 'w') as fh:
        fh.write(doc.toprettyxml(indent='  '))


def get_data(input_gpx):
    tree = ElementTree()
    tree.parse(input_gpx)
    namespace = {'gpx': 'http://www.topografix.com/GPX/1/0'}
    trkpts = tree.findall('.//gpx:trkpt', namespaces=namespace)
    data = {
        'lat': [float(trkpt.get('lat')) for trkpt in trkpts],
        'lon': [float(trkpt.get('lon')) for trkpt in trkpts],
        'datetime': [trkpt.find('gpx:time', namespaces=namespace).text for trkpt in trkpts]
    }
    data['datetime'] = pd.to_datetime(data['datetime'], utc=True)
    start_time = data['datetime'][0]
    data['time'] = (data['datetime'] - start_time).total_seconds()

    return pd.DataFrame(data)




def compute_cross_correlation(df1, df2, column1, column2):
    return np.sum(df1[column1] * df2[column2])

def find_best_offset(accl, phone):
    best_offset = 0
    best_correlation = -np.inf
    for offset in np.linspace(-5.0, 5.0, 101):
        phone_offset = phone.copy()
        phone_offset['timestamp'] += pd.to_timedelta(offset, unit='sec')
        phone_offset['rounded_timestamp'] = phone_offset['timestamp'].dt.round('4S')
        phone_avg = phone_offset.groupby('rounded_timestamp').mean()

        combined = pd.merge_asof(accl, phone_avg.reset_index(), on='rounded_timestamp', direction='nearest')
        correlation = compute_cross_correlation(combined, combined, 'x', 'gFx')
        if correlation > best_correlation:
            best_correlation = correlation
            best_offset = offset
    return best_offset




def main():
    input_directory = pathlib.Path(sys.argv[1])
    output_directory = pathlib.Path(sys.argv[2])
    
    accl = pd.read_json(input_directory / 'accl.ndjson.gz', lines=True, convert_dates=['timestamp'])[['timestamp', 'x']]
    gps = get_data(input_directory / 'gopro.gpx')
    phone = pd.read_csv(input_directory / 'phone.csv.gz')[['time', 'gFx', 'Bx', 'By']]
    
    first_time_accl = accl['timestamp'].min()
    first_time_gps = gps['datetime'].min()
    
    accl['rounded_timestamp'] = accl['timestamp'].dt.round('4S')
    gps['timestamp'] = first_time_gps + pd.to_timedelta(gps['time'], unit='sec')
    gps['rounded_timestamp'] = gps['timestamp'].dt.round('4S')
    phone['timestamp'] = first_time_accl + pd.to_timedelta(phone['time'], unit='sec')
    phone['rounded_timestamp'] = phone['timestamp'].dt.round('4S')
    
    accl_avg = accl.groupby('rounded_timestamp').mean()
    gps_avg = gps.groupby('rounded_timestamp').mean()
    phone_avg = phone.groupby('rounded_timestamp').mean()

    accl_gps = accl_avg.reset_index().merge(gps_avg.reset_index(), on='rounded_timestamp')
    combined = accl_gps.merge(phone_avg.reset_index(), on='rounded_timestamp')

    combined['datetime'] = combined['rounded_timestamp']

    best_offset = find_best_offset(accl, phone)
    phone['timestamp'] += pd.to_timedelta(best_offset, unit='sec')

    print(f'Best time offset: {best_offset:.1f}')
    os.makedirs(output_directory, exist_ok=True)
    output_gpx(combined[['datetime', 'lat', 'lon']], output_directory / 'walk.gpx')
    combined[['datetime', 'Bx', 'By']].to_csv(output_directory / 'walk.csv', index=False)


if __name__ == '__main__':
    main()

