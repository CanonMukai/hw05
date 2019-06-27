

rosen_list = [{"Name":"Yamanote", "Stations":["Shinagawa", "O-saki", "Gotanda"]}]

def make_graph(rosen_list):
    station_links_dict = {}
    for rosen in rosen_list:
        for i in range(len(rosen['Stations'])-1):
            if rosen['Stations'][i] in station_links_dict:
                station_links_dict[rosen['Stations'][i]].append(rosen['Stations'][i+1])
            else:
                station_links_dict[rosen['Stations'][i]] = [rosen['Stations'][i+1]]
    return station_links_dict


make_graph(rosen_list)
    
