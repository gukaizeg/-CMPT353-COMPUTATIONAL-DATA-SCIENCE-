import sys
import numpy as np
import pandas as pd
from xml.dom.minidom import Document
from pykalman import KalmanFilter
from xml.etree.ElementTree import ElementTree

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
    return pd.DataFrame(data)

def distance(points):
    lat_shifted = points['lat'].shift(1)
    lon_shifted = points['lon'].shift(1)
    dlat = np.radians(points['lat'] - lat_shifted)
    dlon = np.radians(points['lon'] - lon_shifted)
    a = np.sin(dlat/2) ** 2 + np.cos(np.radians(lat_shifted)) * np.cos(np.radians(points['lat'])) * np.sin(dlon/2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return 6371000 * c.sum()

def smooth(points):
    initial_state_mean = [points.iloc[0]['lat'], points.iloc[0]['lon'], 0, 0]
    initial_state_covariance = np.eye(4) * 10
    transition_matrix = np.array([[1, 0, 5e-7, 34e-7],
                                  [0, 1, -49e-7, 9e-7],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])
    observation_matrix = np.eye(4)
    observation_covariance = np.eye(4) * 1
    kf = KalmanFilter(transition_matrices=transition_matrix,
                      observation_matrices=observation_matrix,
                      initial_state_mean=initial_state_mean,
                      initial_state_covariance=initial_state_covariance,
                      observation_covariance=observation_covariance)
    smoothed_states, _ = kf.smooth(points[['lat', 'lon', 'Bx', 'By']].values)
    smoothed_points = pd.DataFrame(smoothed_states[:, :2], columns=['lat', 'lon'])
    smoothed_points['datetime'] = points.index
    return smoothed_points



def output_gpx(points, output_filename):
    def append_trkpt(pt, trkseg):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.7f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.7f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = Document()
    gpx = doc.createElement('gpx')
    gpx.setAttribute('xmlns', 'http://www.topografix.com/GPX/1/0')
    doc.appendChild(gpx)

    trk = doc.createElement('trk')
    gpx.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg)

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def main():
    input_gpx = sys.argv[1]
    input_csv = sys.argv[2]

    points = get_data(input_gpx).set_index('datetime')
    sensor_data = pd.read_csv(input_csv, parse_dates=['datetime']).set_index('datetime')
    points['Bx'] = sensor_data['Bx']
    points['By'] = sensor_data['By']

    dist = distance(points)
    print(f'Unfiltered distance: {dist:.2f}')

    smoothed_points = smooth(points)
    smoothed_dist = distance(smoothed_points)
    print(f'Filtered distance: {smoothed_dist:.2f}')

    output_gpx(smoothed_points, 'out.gpx')

if __name__ == '__main__':
    main()
