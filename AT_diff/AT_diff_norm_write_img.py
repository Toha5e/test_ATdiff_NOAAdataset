import netCDF4
import numpy as np
import time
import gdal
import osr

def Writing_Geotiff(arr,lon_list,lat_list,outfilename):
    print('\n = = = WRITING GEOTIFF = = =\n')
    #arr=np.array(out_list,dtype=np.float32)
    out_geotiff=outfilename+'.tiff'
    print(out_geotiff)

    x_pixels=arr.shape[1]# quantity of pixels in axis X
    y_pixels=arr.shape[0]# quantity of pixels in axis Y
    band=1
    driver=gdal.GetDriverByName('GTiff')
    outdata=driver.Create(out_geotiff,x_pixels,y_pixels,band,gdal.GDT_Float32)

    srs=osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    outdata.SetProjection(srs.ExportToWkt())
    
    lon_for_georef_list=lon_list
    lat_for_georef_list=lat_list
    
    pre_x_set_trans=lon_for_georef_list[0]
    weight_pxl=lon_list[1]-lon_list[0]
    x_route=0
    pre_y_set_trans=lat_for_georef_list[0]
    height_pxl=lat_list[1]-lat_list[0]
    y_route=0

    x_set_trans=pre_x_set_trans#-(weight_pxl/2)
    y_set_trans=pre_y_set_trans#-(height_pxl/2)

    outdata.SetGeoTransform([x_set_trans,weight_pxl,x_route,y_set_trans,y_route,height_pxl])
    outdata.GetRasterBand(1).WriteArray(arr)
    outdata.FlushCache()
    print(arr)
    return('GEOTIFF_WROTE')



filename_norm='air.mon.1981-2010.ltm.nc'
filename_mon='air.mon.mean.nc'
ds_norm=netCDF4.Dataset(filename_norm)
ds_mon=netCDF4.Dataset(filename_mon)

ds=ds_norm
lat_arr_norm=ds_norm.variables['lat'][:]
lon_arr_norm=ds_norm.variables['lon'][:]
time_arr_norm=ds_norm.variables['time'][:]
air_arr_norm=ds_norm.variables['air'][:]
#lon_arr=ds.variables['lon'][:]
print(len(time_arr_norm))


ds=ds_mon
lat_arr_mon=ds_mon.variables['lat'][:]
lon_arr_mon=ds_mon.variables['lon'][:]
time_arr_mon=ds_mon.variables['time'][:]
air_arr_mon=ds_mon.variables['air'][:]
#lon_arr=ds.variables['lon'][:]
print(len(time_arr_mon))

base_time=5364662400
corect_time=(time_arr_mon[864]*3600)-base_time
#print(time.ctime(corect_time))

index_list=[864,865,866,867,868,869,870,871,872,873,874,875]

base_time=5364662400
for i in range(0,12,1):
    correct_time=(time_arr_mon[index_list[i]]*3600)-base_time
    tt=time.gmtime(correct_time)
    
    diff_arr=air_arr_mon[index_list[i]]-air_arr_norm[i]
    diff_arr=np.where(diff_arr>30,np.nan,diff_arr)
    
    print(tt[0],tt[1], np.mean(diff_arr))
    outfilename='AT_diff_'+str(tt[0])+str(tt[1]).zfill(2)+'_and_norm_'+filename_norm.split('.')[2]+'_'+str(i+1).zfill(2)
    Writing_Geotiff(diff_arr,lon_arr_mon,lat_arr_mon,outfilename)
    




