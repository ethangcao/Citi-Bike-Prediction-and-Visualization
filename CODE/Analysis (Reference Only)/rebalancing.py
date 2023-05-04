import pandas as pd
import numpy as np

for h_day in [0,1]:
    data = pd.read_csv("LSTM.csv")
    data0 = data[data['half_day']==h_day]
    data0 = pd.pivot_table(data0, values='value', index=['station'], columns=['type'], aggfunc=np.sum).reset_index()
    data0['variance'] =10 + (data0['dropoff']-data0['pickup']).astype(int)
    from_stations = data0[data0['variance']>=0]
    from_stations = from_stations[from_stations['variance']>from_stations['pickup']]
    from_stations['allow'] = (from_stations['variance']-from_stations['pickup']).astype(int)
    from_stations = from_stations[from_stations['allow']>0]
    to_stations = data0[data0['variance']<0].sort_values(by='variance')
    
    heatmap = pd.read_csv("heatmap.csv")
    location = heatmap[['station', 'latitude', 'longitude']].drop_duplicates()
    location_copy = location.copy()
    
    def distance(latitude0, longitude0, latitude1, longitude1):
        return (latitude1-latitude0)**2+((longitude1-longitude0)**2)
    
    station_dict = {}
    for index0, row0 in location.iterrows():
        d_list = []
        print('\r {}/1603'.format(index0+1), end = '')
        for index1, row1 in location_copy.iterrows():
            d_list.append([row1['station'], distance(row0['latitude'], row0['longitude'], row1['latitude'], row1['longitude'])])
        distance_df = pd.DataFrame(d_list, columns = ['station', 'distance']).sort_values(by='distance')
        station_dict[row0['station']] = distance_df[distance_df['distance']>0]
        
    status_dict = {}
    for index, row in from_stations.iterrows():
        status_dict[row['station']] = row['allow']
        
    move = []
    for to_index, to_row in to_stations.iterrows():
        need = -to_row['variance']
        to_st = to_row['station']
        distance_lookup = station_dict[to_st]
        i = 0
        while need>0:
            from_st = distance_lookup.iloc[i,0]
            if from_st in status_dict.keys():
                supply = status_dict[from_st]
                if need >= supply:
                    need -= supply
                    status_dict.pop(from_st)
                else:
                    supply = need
                    need = 0
                    status_dict[from_st] -= supply
                move.append([from_st, to_st, supply])
            i+=1
    
    move_df = pd.DataFrame(move, columns = ['from', 'to', 'quantity'])
    move_df.to_csv('rebalancing{}.csv'.format(h_day), index=False)
