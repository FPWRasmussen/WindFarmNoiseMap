import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.io.img_tiles import GoogleTiles
from cartopy.io.shapereader import BasicReader
from calc_extent import calc_extent
from calculate_noise import calculate_noise
import elevation
import rasterio
import pathlib
from calculate_point_elevation import calculate_point_elevation


cwd = pathlib.Path().absolute() # current working directory
data = np.loadtxt("map_cord_test.txt")
turbine_cord = data[:,0:2]
extent = calc_extent(data, 1000)
map_boundaries = np.array([extent[0:2],extent[2:4]]).T
#### ELEVATION MAP
fp = cwd.joinpath("MAP.tif") # TIF file path
elevation.clip(bounds=map_boundaries.flatten(), output= fp)
img = rasterio.open(fp)
band_of_interest = 1 # Which band are you interested.  1 if there is only one band
contour_data = np.flip(img.read(band_of_interest), axis=0)

hub_elevation = np.zeros(len(turbine_cord[:,0]))
for i, x in enumerate(hub_elevation):
    hub_elevation[i], long_axis, lat_axis = calculate_point_elevation(turbine_cord[i,0], turbine_cord[i,1], map_boundaries, contour_data)
data[:,2] = data[:,2] + hub_elevation

noise_grid_total,longitude_list, latitude_list, = calculate_noise(data, 0, map_boundaries, contour_data)


#%%

plt.figure(figsize=[11,8])
imagery = GoogleTiles(style = "satellite")
ax = plt.axes(projection=imagery.crs)


reader = BasicReader("./shapefiles/houses.shp")
ax.add_geometries(reader.geometries(), crs=ccrs.PlateCarree(), color = "red")

reader1 = BasicReader("./shapefiles/Cities.shp")
ax.add_geometries(reader1.geometries(), crs=ccrs.PlateCarree(), color = "green")


ax.set_extent(extent)

ax.add_image(imagery, 16) # 16

xs, ys = turbine_cord.T
plt.plot(xs, ys, "x", transform=ccrs.PlateCarree(), color='blue', markersize=12, label = "Wind Turbines")
plt.plot(0, 0, "-", transform=ccrs.PlateCarree(), color='red', markersize=12, label = "Houses") # proxy_artist
plt.plot(0, 0, "-", transform=ccrs.PlateCarree(), color='green', markersize=12, label = "Cities") # proxy_artist

plt.contourf(longitude_list,latitude_list, noise_grid_total,5, alpha=.5,  transform=ccrs.PlateCarree())
plt.colorbar(label=r"noise [dB]") 

# levels = [33,38,44,49,54],
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
plt.legend()
plt.title("Noise map")
# plt.tight_layout(pad=1)
# plt.show()
plt.savefig("Noise_map.png")
#%%

plt.figure(figsize=[11,8])
ax = plt.axes(projection=imagery.crs)
ax.set_extent(extent)
ax.add_image(imagery, 16) # 16
plt.contourf(long_axis,lat_axis, contour_data,5, alpha=.5,transform=ccrs.PlateCarree())
plt.colorbar(label=r"Elevation [m]") 

plt.plot(xs, ys, "x", transform=ccrs.PlateCarree(), color='blue', markersize=12, label = "Wind Turbines")
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
plt.legend()
plt.title("Elevation map")
# plt.tight_layout()
# plt.show()
plt.savefig("elevation_map.png")

