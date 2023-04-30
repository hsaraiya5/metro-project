class WMATAException(Exception):
    "base exception for the app"

class WMATARequestError(WMATAException):
    code = 501
    description = "There was an error making a call to a WMATA endpoint"
    pass

class InvalidStationName(WMATAException):
    code = "401"
    description = "Station name input is invalid"