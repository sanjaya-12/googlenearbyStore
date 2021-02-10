import requests
import json
import pandas as pd
import time
import numpy as np
from contextlib import redirect_stdout

APIKEY = "XXXXXXXXXXXXXXXXXXXXXXXX"


def findPlaces(loc=("0","0"),radius=500, pagetoken = 2,LocationNo = 0 , LocationName = "xyz"):
   lat, lng = loc
   type = "restaurant"
   LocationNo = LocationNo
   LocationName = LocationName
   ww_store = str(LocationNo) +"," + LocationName+","
   url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={APIKEY}{pagetoken}".format(lat = lat, lng = lng, radius = radius, type = type,APIKEY = APIKEY, pagetoken = "&pagetoken="+pagetoken if pagetoken else "")
   #print(url)
   response = requests.get(url)
   res = json.loads(response.text)
   # print(res)
   #print("here results ---->>> ", len(res["results"]))

   with open('D:\GoogleAPI\out.csv', 'a+') as f:
         with redirect_stdout(f):
          for result in res["results"]:
           info = str(ww_store) + ",".join(map(str,[result["name"],result["geometry"]["location"]["lat"],result["geometry"]["location"]["lng"],result.get("rating",0),result["place_id"]]))
           print(info)
   pagetoken = res.get("next_page_token",None)

   print("here -->> ", pagetoken)

   return pagetoken

# pagetoken = "CpQFhwIAADQWOcVI1wll-B869Z24El48rXw18gKoab_keD65V18zFEvPjKIfrS79Pc_vXJcZQtOuF0RObQG20ph-GE3ssP3k1fu8zsYbw5g3UPbSjAvQLdXkdD1qAWztXj7hc5Kxc4pYRyGM1_ljVOHg3Py_zSlYscnoNjCvRua2MDQgusCsEquNqGREFdvhjDkbeMhEFYxHucTnIn96OxIJEpamePTHsBooYyPBaa_ejGZ_C99QeDjpSkSKBgEe3aL1uWKlYhsGKh7biQUR5rKsKPodwccLIrW8Gr5tag3NH0sLPExHHvqzlpkj--KIuydTVjPH7u2zHxmPByServ2S5xjXYUBRr-ly3e1xPsVMhZZH9TxfttCIHLscBvpvCswIfaGYdl3bEzsrFISfpp0rpKtlp9gWGY7Tbk2n6s3etCHQEHn2qmM8bsJwkZV81pUWN0j9C9RX-ywOyIKY2yp1w_Iq1mRwOwY4mckbicOoooHiV6JER4xe7Kizw9hbXOnezn_NMk15TLwRoXlfL1s73uwogo-VWE8c-V1HqRpWQSyudRhLwhOEclrICXIdxICOgTgYO1z57xCEerw3QUL_7MPDrlbbh_AlX8I6Jfe8IhQ1Fkqu_njatm6aBTjkp2CSqlvZJpI_Lrv330VcyFEqBkGn7NJew3I9xofSrBaXFa8ABi6DXQm6-yC32OEyf7GHNXINjT1IB0yh6KR6c0qzaqiqOzKcuuai9XqEMQNNKyi6EuhzH5TP9YA56N3JhnXRFhs2aWHZhLlieVI6_uqzpZSgYjUem8aQrMTlmHw0kIYU8I-Ca041C4Zm2gMezwygRrhzsOoAmbmu96nft0KuIWTB3A_xGVKYQ2qjb2KRM7nsglnSEhDoNs8EhvuIm0FQs30YSCp5GhRO3b3Tn5rsLuwiWgu8hwEGhL0S1A"

df = pd.read_csv("D:\GoogleAPI\storeInfo.csv", usecols=[0,1,2,3])
pagetoken = None
for index, row in df.iterrows():
    #print(row['Longitude'],row['Latitude'])
   # pagetoken = findPlaces((row['Latitude'], row['Longitude']),pagetoken=pagetoken)
    while True: 
     pagetoken = findPlaces((row['Latitude'],row['Longitude']),pagetoken=pagetoken,LocationNo = row['LocationNo'] ,LocationName = row['LocationName'])
     time.sleep(5)
     if not pagetoken:
         break 