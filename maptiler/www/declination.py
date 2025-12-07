# -*- coding: utf-8 -*-

"""
WSGI module to return magnetic declination for current time, given lat and lon values
Returns plain text, with string representation of dec (or "0.0" if it fails).
Depends on https://github.com/todd-dembrey/geomag
"""
from oomf import *
#from geomag import WorldMagneticModel

def application(environ, start_response):
    response_headers=[('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type'),
    ('Access-Control-Allow-Origin', '*'),
    ('Content-type', 'text/plain')]

    path = environ['QUERY_STRING']
    p = parse_qs(path)
    for key, val in p.items():  #unlist param dictionary values
        p[key] = val[0]

#    wmm = WorldMagneticModel()
    from pygeomag import GeoMag
    from pygeomag import calculate_decimal_year
    import datetime
    
    geo_mag = GeoMag(coefficients_file="wmm/WMM.COF")


    try:
        #magdec = wmm.calc_mag_field(float(p['lat']), float(p['lon'])).declination #look up magnetic declination for correct map North lines
        magdec = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time= calculate_decimal_year(datetime.datetime.now())).d
    except:
        magdec = 0

    start_response('200 OK', response_headers)
    return [str(magdec).encode('utf-8')]
