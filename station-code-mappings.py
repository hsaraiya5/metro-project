import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import yaml

with open("wmataApiKeys.yaml", "r") as stream:
    try:
        keys = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

headers = {
    'api_key': keys['apiKey']
}

lines = ['YL', 'RD', 'SV', 'GR', 'BL', 'OR']
mappings = {}
for line in lines:
    params = urllib.parse.urlencode({
        'LineCode': line
    })

    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jStations?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        line_data = json.loads(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
   
    mappings[line] = line_data

output = json.dumps(mappings, indent = 2)
with open("station_code_mappings.json", "w") as outfile:
    outfile.write(output)

