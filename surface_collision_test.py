
import numpy as np
from scipy.interpolate import interpn
from calculate_point_elevation import calculate_point_elevation


def surface_collision_test(map_boundaries, hub_position, contour_data, surface_point):
    """
        Input:
        map_boundaries : longitude and latitude boundaries for the map
        hub_position : longitude, latitude and turbine hub height (above ground)
        contour_data : elevation map in 2D grid array
        surface_point : longitude, latitude of point to test
        
        Output:
        True / False: If the sound collide with the terrain returns True, else returns False
    
    """


    srtm_res = 1/3600 # SRTM30 resolution (approx 1 arc second)
    
    point_elevation, long_axis, lat_axis = calculate_point_elevation(surface_point[0], surface_point[1], map_boundaries, contour_data)
    surface_position = np.append(surface_point, point_elevation)
    
    direction = surface_position - hub_position # calculate direction vector from turbine to surface
    
    n_steps = np.int(np.ceil(np.abs(direction[0:2]).max()/srtm_res))+1 # number of steps necessary at given resolution
    
    # long_cords = np.linspace(hub_position[0], surface_point[0], n_steps) # coordinates to calculate and check elevation
    # lat_cords = np.linspace(hub_position[1], surface_point[1], n_steps)
    # elev_cords = np.linspace(hub_position[2], surface_position[2], n_steps)
    
    # long_cords = np.linspace(surface_point[0], hub_position[0], n_steps) # coordinates to calculate and check elevation
    # lat_cords = np.linspace(surface_point[1], hub_position[1], n_steps)
    # elev_cords = np.linspace(surface_position[2], hub_position[2], n_steps)
    
    long_cords = np.linspace(surface_point[0], hub_position[0], n_steps) # coordinates to calculate and check elevation
    lat_cords = np.linspace(surface_point[1], hub_position[1], n_steps)
    elev_cords = np.linspace(surface_position[2], hub_position[2], n_steps)
    
    long_cords = long_cords[1:int(n_steps/2)]
    lat_cords = lat_cords[1:int(n_steps/2)]
    elev_cords = elev_cords[1:int(n_steps/2)]
    
    for i, x in enumerate(long_cords):
    
        point = np.array([lat_cords[i],long_cords[i]])
        interp_elevation = interpn((lat_axis, long_axis), contour_data, point)
        if interp_elevation -1 > elev_cords[i]:
            return point_elevation, True
            break
    return point_elevation, False
