import json
from datetime import datetime, timedelta

import requests

# FIXME: uncomment only one of below to select the wanted dose
# DOSE = "Pfizer Dose 1"
# DOSE = "Pfizer Dose 2"
DOSE = "Pfizer Dose 3"
# DOSE = "Moderna Dose 1"
# DOSE = "Moderna Dose 2"
# DOSE = "Moderna Dose 3"

BRAND = DOSE.split()[0]

START_DATE = datetime.now().strftime("%Y-%m-%d")
END_DATE = (datetime.now() + timedelta(30)).strftime("%Y-%m-%d")

if __name__ == '__main__':
    print("Searching for:")
    print(f"\t{DOSE}")
    print(f"\tSTART_DATE={START_DATE}")
    print(f"\tEND_DATE={END_DATE}")
    print()

    url = 'https://gql.medscheck.medmeapp.com/graphql'
    headers = {
        "x-tenantid": "edfbb1a3-aca2-4ee4-bbbb-9237237736c4",
        "Origin": "https://shoppersdrugmart.medmeapp.com"
    }

    stores_url = 'https://www1.shoppersdrugmart.ca/sdmapi/store/GetCovidShotStores?lang=en&covidBrands=&lat=43.7949488&lng=-79.2356212&minLat=40&minLng=-80&maxLat=45&maxLng=-76'
    stores_request = requests.get(stores_url)
    stores_result = json.loads(stores_request.content)

    print(f'Total stores: {len(stores_result)}')
    counter = 1
    for store in stores_result:
        print(f'processing: {counter}')
        counter += 1

        if not store["VaccineBrands"][BRAND]:
            print(f"Brand '{BRAND}' not found, continuing to next store... ")
            continue

        pharmacy_id_payload = {
            "operationName": "getEnterprisePharmacy",
            "variables": {
                "storeNo": format(store['StoreID'], '04d'),
                "enterpriseName": "SDM"
            },
            "query": "query getEnterprisePharmacy($enterpriseName: String, $storeNo: String) {\n  getEnterprisePharmacy(enterpriseName: $enterpriseName, storeNo: $storeNo) {\n    id\n    name\n    timeZone\n    enterprise\n    theme\n    logoLong\n    logoCircle\n    logoLongInverse\n    province\n    storeNo\n    privacyPolicy\n    pharmacyAddress {\n      id\n      unit\n      streetNumber\n      streetName\n      city\n      province\n      postalCode\n      poBox\n      __typename\n    }\n    pharmacyContact {\n      id\n      phone\n      email\n      __typename\n    }\n    __typename\n  }\n}\n"
        }
        pharmacy_id_request = requests.post(url, data=json.dumps(pharmacy_id_payload), headers=headers)
        pharmacy_id_result = json.loads(pharmacy_id_request.content)

        this_pharmacy_id = pharmacy_id_result['data']['getEnterprisePharmacy']['id']
        appointment_payload = {
            "operationName": "publicGetAppointmentTypes",
            "variables": {},
            "query": "query publicGetAppointmentTypes($appointmentTypeId: Int, $method: EAppointmentTypeMethod, $isWaitlist: Boolean) {\n  publicGetAppointmentTypes(appointmentTypeId: $appointmentTypeId, method: $method, isWaitlist: $isWaitlist) {\n    id\n    type\n    category\n    subCategory\n    durations\n    methods\n    intakeForms\n    minimumAge\n    description\n    subDescription\n    isWalkinAllowed\n    isWaitlisted\n    price\n    bookingStartDate\n    bookingEndDate\n    waitlistDescription\n    location\n    isExternalClinic\n    __typename\n  }\n}\n"
        }
        appointment_headers = {
            "x-tenantid": "edfbb1a3-aca2-4ee4-bbbb-9237237736c4",
            "Origin": "https://shoppersdrugmart.medmeapp.com",
            "x-pharmacyid": this_pharmacy_id
        }
        appointment_request = requests.post(url, data=json.dumps(appointment_payload), headers=appointment_headers)
        appointment_result = json.loads(appointment_request.content)
        for appointment in appointment_result['data']['publicGetAppointmentTypes']:
            if DOSE in appointment['type'] and "Pediatric" not in appointment['type']:
                if appointment['isWaitlisted']:
                    print("\tFound vaccine but the store is wait-list only")
                    continue
                vaccine_payload = {
                    "operationName": "publicGetAvailableTimes",
                    "variables": {
                        "pharmacyId": this_pharmacy_id,
                        "appointmentTypeId": appointment['id'],
                        "noOfPeople": 1,
                        "filter": {
                            "startDate": START_DATE,
                            "endDate": END_DATE
                        }
                    },
                    "query": "query publicGetAvailableTimes($pharmacyId: String, $appointmentTypeId: Int!, $noOfPeople: Int!, $filter: AvailabilityFilter!) {\n  publicGetAvailableTimes(pharmacyId: $pharmacyId, appointmentTypeId: $appointmentTypeId, noOfPeople: $noOfPeople, filter: $filter) {\n    startDateTime\n    endDateTime\n    resourceId\n    __typename\n  }\n}\n"
                }

                vaccine_request = requests.post(url, data=json.dumps(vaccine_payload), headers=headers)
                vaccine_result = json.loads(vaccine_request.content)
                try:
                    if (vaccine_result['data']['publicGetAvailableTimes']):
                        print("YEAH!!")
                        print(pharmacy_id_result['data']['getEnterprisePharmacy']['name'])
                        print(vaccine_result['data']['publicGetAvailableTimes'])
                except TypeError:
                    print(vaccine_result)
