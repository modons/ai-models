import sys
import cdsapi

"""
download all data needed for panguweather from CDS in grib format. 

Usage: python download_panguweather.py YYYYMMDD [path]
- where path is the directory where the GRIB files should be saved. Defaults to pwd
- the output files take the form YYYYMMDD_sfc.grib and YYYYMMDD_pl.grib, which can be inported at runtime using _my_ file option (not the standard one on the main branch, which uses a single file)
"""

def download_cds_grib_panguweather_pl(c,variables, pressure_levels, year, month, day, output_file):

    request = {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': variables,
        'pressure_level': pressure_levels,
        'year': year,
        'month': month,
        'day': day,
        'time': '00:00'
    }

    print('retrieving pressure-level GRIB data from CDS for date:',year,month,day)
    print('writing the output here:',output_file)
    c.retrieve('reanalysis-era5-pressure-levels', request, output_file)
    
    return

def download_cds_grib_panguweather_sfc(c,variables, year, month, day, output_file):

    request = {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': variables,
        'year': year,
        'month': month,
        'day': day,
        'time': '00:00',
        'levtype': 'sfc'
    }

    print('retrieving surface GRIB data from CDS for date:',year,month,day)
    print('writing the output here:',output_file)
    c.retrieve('reanalysis-era5-single-levels', request, output_file)

    return

# Specify the variables, pressure levels, date, and output file path
sfc_variables = ["mean_sea_level_pressure", "10m_u_component_of_wind", "10m_v_component_of_wind", "2m_temperature"]
pl_variables = ["geopotential", 'specific_humidity', 'temperature', 'u_component_of_wind', 'v_component_of_wind']
pressure_levels = ['1000', '925', '850', '700', '600', '500', '400', '300', '250', '200', '150', '100', '50']

if __name__ == "__main__":
    # Access the command-line arguments
    args = sys.argv[1:]

    if len(args) < 1 or len(args)>2:
        print("Usage: python download_panguweather.py YYYYMMDD [path]")
        exit()

    # parse the date string
    year = args[0][:4]
    month = args[0][4:6]
    day = args[0][6:8]

    output_file_sfc = args[0][:8]+'_sfc.grib'
    output_file_pl = args[0][:8]+'_pl.grib'
    if len(args) == 2:
        output_file_sfc = args[1]+'/'+output_file_sfc
        output_file_pl = args[1]+'/'+output_file_pl

    # start the cds client and pass to the download functions
    c = cdsapi.Client()

    download_cds_grib_panguweather_sfc(c,sfc_variables, year, month, day, output_file_sfc)
    download_cds_grib_panguweather_pl(c,pl_variables, pressure_levels, year, month, day, output_file_pl)
