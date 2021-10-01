import xml.etree.ElementTree as ET
import json

ns = {
    'soapenc': "http://schemas.xmlsoap.org/soap/encoding/",
    'soapenv': "http://schemas.xmlsoap.org/soap/envelope/",
    'xsd': "http://www.w3.org/2001/XMLSchema",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'ns': "http://www.opentravel.org/OTA/2003/05/common/",
    'xmlns': "http://www.iata.org/IATA/EDIST/2017.2",
    'ns2': "http://www.iata.org/IATA/EDIST/2017.2/CR129"
}
json_data = {}

seatmap1 = ET.parse('./seatmap1.xml')
root1 = seatmap1.getroot()
seatmap2 = ET.parse('./seatmap2.xml')
root2 = seatmap2.getroot()

Departure_obj = {}
Arrival_obj = {}
Flight_obj = {}

def FlightDetailHandler():
    FlightDataList = root2.findall('.//xmlns:DataLists', ns)
    for child in FlightDataList:
        for Departure in child.find('.//xmlns:Departure', ns):
            splitted_tag = Departure.tag.split('}')
            Departure_obj[splitted_tag[1]] = Departure.text
        for Arrival in child.find('.//xmlns:Arrival', ns):
            splitted_tag = Arrival.tag.split('}')
            Arrival_obj[splitted_tag[1]] = Arrival.text
        for Carrier in child.find('.//xmlns:MarketingCarrier', ns):
            splitted_tag = Carrier.tag.split('}')
            Flight_obj[splitted_tag[1]] = Carrier.text

    json_data['Departure'] = Departure_obj
    json_data['Arrival'] = Arrival_obj
    json_data['Flight'] = Flight_obj

def SeatHandler():
    for rows in root1.findall(".//ns:RowInfo", ns):
        rowNumber = rows.attrib['RowNumber']
        cabinType = rows.attrib['CabinType']

        new_obj = {'RowNumber': rowNumber, 'Cabin Type': cabinType}
        for seatInfo in rows.findall(".//ns:SeatInfo", ns):
            seatNumber = seatInfo.find('.//ns:Summary', ns).get('SeatNumber')
            available = seatInfo.find('.//ns:Summary', ns).get('AvailableInd')

            Fee = seatInfo.find('.//ns:Service', ns)
            if Fee is None:
                Cost = 'Not Available'
            else:
                Cost = f"{Fee.find('.//ns:Fee', ns).get('Amount')} {Fee.find('.//ns:Fee', ns).get('CurrencyCode')}"
            for feature in seatInfo.findall('.//ns:Features', ns):
                type = feature.text
                if type == 'Window' or type == 'Aisle' or type == 'Center':
                    new_obj_detail = {'Seat Number': seatNumber,
                                    'Availabilty': available, 'Cost': Cost, 'Features': type}
                else:
                    new_obj_detail = {'Seat Number': seatNumber,
                                    'Availabilty': available, 'Cost': Cost}
            new_obj[f'{seatNumber} Details'] = new_obj_detail
        json_data[f"{rowNumber}"] = new_obj

FlightDetailHandler()
SeatHandler()


with open('seatmap_parsed.json', 'w') as outfile:
    json.dump(json_data, outfile)