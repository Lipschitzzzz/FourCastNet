import cdsapi

dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "geopotential", "relative_humidity", "temperature",
        "u_component_of_wind", "v_component_of_wind"
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
