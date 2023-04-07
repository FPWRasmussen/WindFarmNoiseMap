import numpy as np
import pyproj
from pyproj import Geod
from absorption import absorption
from surface_collision_test import surface_collision_test

# data = np.loadtxt("map_cord.txt")
# terrain = 0 # 0 = land, 1 = water
# map_boundaries = np.array([[12.6154, 55.6583],[12.6703, 55.6893]])

def calculate_noise(data, terrain, map_boundaries, contour_data):
    turbine_cord = data[:,0:2] # 
    hub_height = data[:,2]
    hub_noise = data[:,3]
    longitude_limit =  map_boundaries[:,0]
    latitude_limit = map_boundaries[:,1]

    
    h = 67 # hub height [m]
    L_w = 102.4 # turbine noise [dB]
    alpha = absorption() # Atmospheric absorption [dB/m]
    
    longitude_list = np.linspace(longitude_limit[0], longitude_limit[1], 300) # grid in longitude direction
    latitude_list = np.linspace(latitude_limit[0], latitude_limit[1], 300) # grid in  latitude direction 

    
    L_g = 1.5 # terrain correction (1.5 for land, 3 for water)
    
    # wind turbine coordinates
    noise_grid_total = np.zeros([len(longitude_list),len(latitude_list)])
    
    for n in np.arange(0,len(data)):
        noise_grid = np.zeros([len(longitude_list),len(latitude_list)])
        h = hub_height[n] # hub height [m]
        L_w = hub_noise[n] # turbine noise [dB]
        wt_longitude, wt_latitude = turbine_cord[n]
        for j, longitude in enumerate(longitude_list):
            print(f"Completion: {round(100*(j/len(longitude_list)/len(data)+n/len(data)),1)}%")
            for i, latitude in enumerate(latitude_list):
                surface_point = np.array([longitude, latitude])
                hub_position = np.array([wt_longitude, wt_latitude, h])
                point_elevation, state = surface_collision_test(map_boundaries, hub_position, contour_data, surface_point)
                if state == True:
                    noise_grid[i,j] = 0
                else:
                    angle1,angle2,dist = Geod(ellps='WGS84').inv(longitude, latitude, wt_longitude ,wt_latitude)
                    noise_grid[i,j] = L_w - 10 * np.log10(4*np.pi*((h-point_elevation)**2 + dist**2))-alpha*np.sqrt((h-point_elevation)**2 + dist**2) + L_g# noise turbine[dB]
                noise_grid_total[i,j] = 10*np.log10(10**(noise_grid_total[i,j]/10) + 10**(noise_grid[i,j]/10))
                

    return noise_grid_total, longitude_list, latitude_list