# -*- coding: utf-8 -*-

"""
WSGI module to return magnetic declination for current time, given lat and lon values
Returns plain text, with string representation of dec (or "0.0" if it fails).
Depends on PyGeoMag: https://pygeomag.readthedocs.io/en/latest/
"""
from oomf import *

def application(environ, start_response):
    response_headers=[('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type'),
    ('Access-Control-Allow-Origin', '*'),
    ('Content-type', 'text/plain')]

    path = environ['QUERY_STRING']
    p = parse_qs(path)
    for key, val in p.items():  #unlist param dictionary values
        p[key] = val[0]

    from pygeomag import GeoMag
    from pygeomag import calculate_decimal_year
    import datetime
    
    geo_mag = GeoMag(coefficients_file="wmm/WMM.COF")

    try:
        magdec = geo_mag.calculate(glat=float(p['lat']), glon=float(p['lon']), alt=0, time= calculate_decimal_year(datetime.datetime.now())).d #look up magnetic declination for correct map North lines
    except:
        magdec = 0

    start_response('200 OK', response_headers)
    return [str(magdec).encode('utf-8')]
