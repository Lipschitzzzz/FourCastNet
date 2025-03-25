import cdsapi

dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "divergence",
        "fraction_of_cloud_cover",
        "geopotential",
        "ozone_mass_mixing_ratio",
        "potential_vorticity",
        "relative_humidity",
        "specific_cloud_ice_water_content",
        "specific_cloud_liquid_water_content",
        "specific_humidity",
        "specific_rain_water_content",
        "specific_snow_water_content",
        "temperature",
        "u_component_of_wind",
        "v_component_of_wind",
        "vertical_velocity",
        "vorticity"
    ],
    "year": ["2021"],
    "month": ["10"],
    "day": [
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "time": [
        "00:00", "06:00", "12:00",
        "18:00"
    ],
    "pressure_level": [
        "50", "500", "850",
        "1000"
    ],
    "data_format": "netcdf",
    "download_format": "zip"
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
