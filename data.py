from __future__ import division
import datetime
import json
import logging
import urllib2

import display

API_ENDPOINT = 'http://bustime.mta.info/api/siri/stop-monitoring.json'
API_KEY = None
with open('api.key', 'r') as key_file:
    API_KEY = key_file.read()


def fmt_query(dictionary):
    return '&'.join(['%s=%s' % (key, str(value))
                     for (key, value) in dictionary.iteritems()])

def make_request(line, stop):
    parameters = {
        'key': API_KEY,
        'version': 2,
        'OperatorRef': 'MTA',
        'MonitoringRef': stop,
        'LineRef': line
    }
    req = urllib2.urlopen(API_ENDPOINT + '?' + fmt_query(parameters))
    return json.loads(req.read())


def parse_data(response_dict):
    raw_response = (response_dict['Siri']['ServiceDelivery']
                    ['StopMonitoringDelivery'])
    if 1 in raw_response:
        logging.warning('odd response')

    raw_response = raw_response[0]
        
    return raw_response['ValidUntil'], raw_response['MonitoredStopVisit']


class Bus(object):
    def __init__(self, bus):
        trip = bus['MonitoredVehicleJourney']
        stop = trip['MonitoredCall']
        self.stops_away = stop['NumberOfStopsAway']
        self.eta = stop.get('ExpectedArrivalTime', '?')
        self.destination = trip['DestinationName'][0]
        self.line = trip['PublishedLineName'][0]
        self.status = None
        self.departure = None
        try:
            self.status = trip['ProgressStatus'][0]
            self.departure = trip['OriginAimedDepartureTime']
        except KeyError:
            pass

    def __str__(self):
        return '%s %d stop%s away; ETA %s' % (self.line,
                                              self.stops_away,
                                              ('' if self.stops_away == 1 else 's'),
                                              self._str_time(self.eta))

    def _str_time(self, iso8601_t):
        try:
            t_index = iso8601_t.index('T')
            time = iso8601_t[t_index+1:t_index+9]
            hh, rest = time.split(':', 1)
            return '%s:%s' % (str(int(hh) % 12 or '12'), rest)
        except IndexError, ValueError:
            logging.warn('Bad time value: %s', iso8601_t)
        return is8601_t


def simplify_parsed_data(json_buses):
    return [Bus(json_bus) for json_bus in json_buses]
