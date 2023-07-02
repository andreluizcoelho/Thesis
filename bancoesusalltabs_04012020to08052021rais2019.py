#!/usr/bin/env python
# coding: utf-8

# # CEP 

# In[1]:


#getting the cep from old bancoesus to merge with this one


# In[2]:


import pandas as pd


# In[3]:


cepintegerbancoesusnodup = pd.read_excel('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cepbancoesus27.02.2021/cepintegerbancoesusnodup.xlsx', sheet_name='Planilha2')


# In[4]:


cepintegerbancoesusnodup.shape


# In[5]:


cepintegerbancoesusnodup.head(3)


# In[150]:


#not worth to merge with the old data to get only 1300 ceps


# In[ ]:


bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[152]:


bancoesusalltabsrais2019.shape


# In[153]:


bancoesusalltabsrais2019.head(3)


# In[154]:


bancoesusalltabsrais2019['cep']


# In[155]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('.','')
bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('-','')
bancoesusalltabsrais2019['cep']


# In[156]:


bancoesusalltabsrais2019.drop_duplicates(subset=['cep'])


# In[157]:


bancoesusalltabsrais2019nodupsCEPS = bancoesusalltabsrais2019.drop_duplicates(subset=['cep']) 


# In[158]:


bancoesusalltabsrais2019nodupsCEPS.shape


# In[159]:


bancoesusalltabsrais2019nodupsCEPS = bancoesusalltabsrais2019nodupsCEPS[['cep']]


# In[160]:


bancoesusalltabsrais2019nodupsCEPS.shape


# In[161]:


bancoesusalltabsrais2019nodupsCEPS


# In[162]:


bancoesusalltabsrais2019nodupsCEPS['cep'].dropna()


# In[163]:


bancoesusalltabsrais2019nodupsCEPS['cep'].isna().sum()


# In[164]:


bancoesusalltabsrais2019nodupsCEPS['cep'] = bancoesusalltabsrais2019nodupsCEPS['cep'].dropna()


# In[165]:


cep=bancoesusalltabsrais2019nodupsCEPS['cep'].tolist()


# In[166]:


cep


# In[ ]:





# In[54]:


#pip install pycep_correios


# In[55]:


#pip install geopy


# In[75]:


import pycep_correios
from geopy.geocoders import Nominatim

endereco = pycep_correios.get_address_from_cep('55780000')

geolocator = Nominatim(user_agent='test_app')
location = geolocator.geocode(endereco['logradouro'] + ', ' + endereco['cidade'] + ' - ' + endereco['bairro'])

print(location.latitude, location.longitude)


# In[53]:


#the code above only works 1 by 1 


# In[57]:


bancoesusalltabsrais2019nodupsCEPS


# In[126]:


bancoesusalltabsrais2019nodupsCEPS.to_csv('ceps.csv', index=False)


# In[ ]:





# In[60]:


#1.Faça a leitura do arquivo .csv utilizando o método open() do Python, e armazene os ceps em uma lista


# In[69]:


import csv    
lista_ceps = []   
with open('ceps.csv') as file:
    next(file)  # Pula o cabeçalho, caso exista
    for row in csv.reader(file):
        lista_ceps.append(row[0])


# In[70]:


#2.Transforme o seu código para conversão de cep em uma função:


# In[71]:


import pycep_correios
from geopy.geocoders import Nominatim

def extrai_lat_long(cep):
    endereco = pycep_correios.get_address_from_cep(cep)

    geolocator = Nominatim(user_agent='test_app')
    location = geolocator.geocode(endereco['logradouro'] + ', ' + endereco['cidade'] + ' - ' + endereco['bairro'])

    return(location.latitude, location.longitude)


# In[72]:


#3. Crie um novo .csv com o CEP, latitude e longitude, usando o mesmo método open(), 
#mas dessa vez com o arquivo de saída, e com o parâmetro 'w' para indicar que a operação é de escrita (write):


# In[88]:


'''with open('ceps_lat_long.csv', 'w') as file:
     cabecalho = ['cep', 'latitude', 'longitude']
     writer = csv.DictWriter(file, fieldnames=cabecalho)

     writer.writeheader() # Escreve o cabeçalho
     for cep in lista_ceps:
         latitude, longitude = extrai_lat_long(cep)
         writer.writerow({'cep': cep, 'latitude': latitude, 'longitude': longitude})
'''


# In[76]:


#this above is not working with many ceps


# In[84]:


#pip install cep-to-coords


# In[99]:


'''from cep_to_coords.convert import cep_to_coords
coordenadas = cep_to_coords('55780000')
print(coordenadas)
'''


# In[96]:


#export CEP_ABERTO_TOKEN='d8e540d0700d405acc0496142c5be3d2'
#meu token=d8e540d0700d405acc0496142c5be3d2


# In[97]:


'''from cep_to_coords.convert import cep_to_coords
from cep_to_coords.strategies import CEPAbertoConverter


coordenadas = cep_to_coords('55780000', factory=CEPAbertoConverter)
print(coordenadas)
'''


# ## From CEP aberto

# In[108]:


#https://cepaberto.com/api_key


# In[109]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=01001000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

response.json()


# In[113]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=55780000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

response.json()


# In[ ]:





# In[ ]:





# ## From viacep

# In[112]:


#http://viacep.com.br/


# In[111]:


import requests

url = "http://viacep.com.br/ws/01001000/json/"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

response.json()


# In[ ]:





# ## from my github post cep to latitude and longitude

# In[121]:


import re
import string
from abc import ABC, abstractmethod

class CEPConverter(ABC):
    @abstractmethod
    def __call__(self, cep):
        pass
class Coordinates(ABC):
    def __init__(self, cep):
        self.cep = cep
        self.clean_cep = self._clean_CEP()
    def _clean_CEP(self):
        # Regex to avoid CEPs with dash ('-')
        regex = re.compile("[%s]" % re.escape(string.punctuation))
        return regex.sub("", self.cep)
    @abstractmethod
    def __call__(self):
        pass


# In[122]:


import json
import requests


URL_GET_ADDRESS_FROM_CEP = "http://www.viacep.com.br/ws/{}/json"


class BaseException(Exception):
    """ base exception"""

    def __init__(self, message=""):
        super(BaseException, self).__init__(message)
        self.message = message

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.message)


def get_address_from_cep(cep):
    """ Source: https://github.com/mstuttgart/pycep-correios/blob/develop/pycep_correios/client.py """
    try:
        response = requests.get(URL_GET_ADDRESS_FROM_CEP.format(cep))

        if response.status_code == 200:
            address = json.loads(response.text)

            if address.get("erro"):
                raise BaseException(message="Other error")

            return {
                "bairro": address.get("bairro", ""),
                "cep": address.get("cep", ""),
                "cidade": address.get("localidade", ""),
                "logradouro": address.get("logradouro", ""),
                "uf": address.get("uf", ""),
                "complemento": address.get("complemento", ""),
            }

        elif response.status_code == 400:
            raise BaseException(message="Invalid CEP: %s" % cep)  # noqa
        else:
            raise BaseException(message="Other error")

    except requests.exceptions.RequestException as e:
        raise BaseException(message=e)


# In[123]:


import os
import requests

#from .viacep import get_address_from_cep
#from .base import CEPConverter, Coordinates


class CorreiosPhotonConverter(CEPConverter):
    def __call__(self, cep):
        return CorreiosPhotonCoordinates(cep)()


class CEPAbertoConverter(CEPConverter):
    def __call__(self, cep):
        return CEPAbertoCoordinates(cep)()


class CorreiosPhotonCoordinates(Coordinates):
    def fetch_address(self):
        try:
            search_result = get_address_from_cep(self.clean_cep)
            address = " ".join(
                [
                    search_result["logradouro"],
                    search_result["bairro"],
                    search_result["cidade"],
                    search_result["uf"],
                    "Brasil",
                ]
            )
            # Treating the case when Correios API return an empty json
            if address == " Brasil":
                address = "-"
        except:
            address = "-"

        return address

    def fetch_coordinates(self, address):
        try:
            if address == "-":
                print("NaN")
                return {"latitude": float("nan"), "longitude": float("nan")}

            r = requests.get(
                "".join(["http://photon.komoot.de/api?q=", address, "&limit=1"])
            )

            result = r.json()
            # list with lon, lat
            coordinates = result["features"][0]["geometry"]["coordinates"]
            return {"latitude": coordinates[1], "longitude": coordinates[0]}
        except IndexError:
            return {"latitude": float("nan"), "longitude": float("nan")}
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def __call__(self):
        address = self.fetch_address()
        coordinates = self.fetch_coordinates(address)
        return coordinates


class CEPAbertoCoordinates(Coordinates):
    def fetch_coordinates(self):
        try:
            url = f"https://www.cepaberto.com/api/v3/cep?cep={self.clean_cep}"
            # Sign up for your free token on: https://cepaberto.com/
            # export CEP_ABERTO_TOKEN='your-token'
            headers = {"Authorization": f'Token token={os.getenv("CEP_ABERTO_TOKEN")}'}
            response = requests.get(url, headers=headers)
            json_response = response.json()
            return {
                "latitude": float(json_response["latitude"]),
                "longitude": float(json_response["longitude"]),
            }
        
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        

    def __call__(self):
        coordinates = self.fetch_coordinates()
        return coordinates


# In[124]:


#from .base import CEPConverter
#from .strategies import CorreiosPhotonConverter


def cep_to_coords(cep: str, factory: CEPConverter = CorreiosPhotonConverter) -> dict:
    coordinates = factory()(cep)
    return coordinates


# In[ ]:





# In[167]:


bancoesusalltabsrais2019nodupsCEPS


# In[168]:


bancoesusalltabsrais2019nodupsCEPS.reset_index(level=0)


# In[169]:


bancoesusalltabsrais2019nodupsCEPS.reset_index(level=0, inplace = True)


# In[170]:


bancoesusalltabsrais2019nodupsCEPS.rename(columns={'index':'id'},inplace = True)


# In[137]:


#the id equals the original index from the original data


# In[171]:


bancoesusalltabsrais2019nodupsCEPS


# In[ ]:


bancoesusalltabsrais2019nodupsCEPS.to_excel('')


# In[139]:


bancoesusalltabsrais2019nodupsCEPS[0:425]


# In[140]:


row0to425 = bancoesusalltabsrais2019nodupsCEPS[0:425]


# In[141]:


row0to425 


# In[142]:


row0to425.update("cep_to_coords('" + row0to425[['cep']].astype(str) + "'),")
print(row0to425 )


# In[143]:


row0to425


# In[144]:


row0to425=row0to425.loc[:,'cep']


# In[145]:


row0to425


# In[146]:


print(' '.join(row0to425))#.tolist()


# In[147]:


coordenadasrow0to425 = cep_to_coords('55780000'), cep_to_coords('55010250'), cep_to_coords('55000000'), cep_to_coords('55004260'), cep_to_coords('50000000'), cep_to_coords('55020220'), cep_to_coords('53715410'), cep_to_coords('54420010'), cep_to_coords('54410010'), cep_to_coords('54400135'), cep_to_coords('51020160'), cep_to_coords('55125000'), cep_to_coords('51020210'), cep_to_coords('54420280'), cep_to_coords('nan'), cep_to_coords('52050138'), cep_to_coords('50740050'), cep_to_coords('53545630'), cep_to_coords('50670260'), cep_to_coords('53431640'), cep_to_coords('51010020'), cep_to_coords('53401080'), cep_to_coords('51021360'), cep_to_coords('50610100'), cep_to_coords('52010290'), cep_to_coords('53416650'), cep_to_coords('53230130'), cep_to_coords('53437000'), cep_to_coords('52050115'), cep_to_coords('54450220'), cep_to_coords('51030010'), cep_to_coords('54320120'), cep_to_coords('54270230'), cep_to_coords('50710140'), cep_to_coords('50721470'), cep_to_coords('0000000000'), cep_to_coords('52150000'), cep_to_coords('53510290'), cep_to_coords('52021040'), cep_to_coords('52121070'), cep_to_coords('50610300'), cep_to_coords('52120390'), cep_to_coords('53230140'), cep_to_coords('51170590'), cep_to_coords('53250640'), cep_to_coords('54590000'), cep_to_coords('54500000'), cep_to_coords('55695000'), cep_to_coords('53150470'), cep_to_coords('56306620'), cep_to_coords('50781600'), cep_to_coords('50610090'), cep_to_coords('48900400'), cep_to_coords('56314485'), cep_to_coords('56300000'), cep_to_coords('50980745'), cep_to_coords('56395000'), cep_to_coords('56330790'), cep_to_coords('52051100'), cep_to_coords('52041115'), cep_to_coords('54410150'), cep_to_coords('50751090'), cep_to_coords('56316568'), cep_to_coords('54310230'), cep_to_coords('50750320'), cep_to_coords('53020240'), cep_to_coords('52041130'), cep_to_coords('50710330'), cep_to_coords('52050500'), cep_to_coords('12228700'), cep_to_coords('55750000'), cep_to_coords('53010010'), cep_to_coords('56308050'), cep_to_coords('56332720'), cep_to_coords('50680000'), cep_to_coords('55820000'), cep_to_coords('00000000'), cep_to_coords('53421081'), cep_to_coords('55680000'), cep_to_coords('52190190'), cep_to_coords('55940000'), cep_to_coords('58320000'), cep_to_coords('52131180'), cep_to_coords('50980260'), cep_to_coords('51010030'), cep_to_coords('55360000'), cep_to_coords('52080020'), cep_to_coords('50741270'), cep_to_coords('52091010'), cep_to_coords('52171340'), cep_to_coords('50680300'), cep_to_coords('52061240'), cep_to_coords('52061250'), cep_to_coords('52221280'), cep_to_coords('52121220'), cep_to_coords('50761550'), cep_to_coords('50760200'), cep_to_coords('50670500'), cep_to_coords('50780640'), cep_to_coords('53080250'), cep_to_coords('55130000'), cep_to_coords('54460312'), cep_to_coords('55460000'), cep_to_coords('50720380'), cep_to_coords('50640470'), cep_to_coords('51020260'), cep_to_coords('50080600'), cep_to_coords('51300350'), cep_to_coords('53421310'), cep_to_coords('52050050'), cep_to_coords('53150410'), cep_to_coords('52211500'), cep_to_coords('50610000'), cep_to_coords('53260020'), cep_to_coords('50760735'), cep_to_coords('54700500'), cep_to_coords('54774300'), cep_to_coords('50060003'), cep_to_coords('54410470'), cep_to_coords('51320020'), cep_to_coords('55825000'), cep_to_coords('53417220'), cep_to_coords('54210342'), cep_to_coords('54210321'), cep_to_coords('50810500'), cep_to_coords('54735730'), cep_to_coords('50080470'), cep_to_coords('53000000'), cep_to_coords('53540240'), cep_to_coords('53420230'), cep_to_coords('53429230'), cep_to_coords('50781000'), cep_to_coords('55670000'), cep_to_coords('54420080'), cep_to_coords('51020041'), cep_to_coords('52070180'), cep_to_coords('52041550'), cep_to_coords('53402645'), cep_to_coords('53439250'), cep_to_coords('50790000'), cep_to_coords('50770120'), cep_to_coords('50820370'), cep_to_coords('51230040'), cep_to_coords('55600000'), cep_to_coords('29722000'), cep_to_coords('51160000'), cep_to_coords('54330212'), cep_to_coords('54450020'), cep_to_coords('50710470'), cep_to_coords('53437040'), cep_to_coords('54080042'), cep_to_coords('54240350'), cep_to_coords('54753786'), cep_to_coords('51020220'), cep_to_coords('52020070'), cep_to_coords('53320165'), cep_to_coords('53437420'), cep_to_coords('54410390'), cep_to_coords('53421090'), cep_to_coords('54430315'), cep_to_coords('53407610'), cep_to_coords('50860070'), cep_to_coords('53150230'), cep_to_coords('50721775'), cep_to_coords('52121030'), cep_to_coords('51110120'), cep_to_coords('51298412'), cep_to_coords('52110130'), cep_to_coords('52050380'), cep_to_coords('52020020'), cep_to_coords('53080790'), cep_to_coords('54800000'), cep_to_coords('01001000'), cep_to_coords('55150000'), cep_to_coords('52020117'), cep_to_coords('51020050'), cep_to_coords('54756120'), cep_to_coords('53130600'), cep_to_coords('50070075'), cep_to_coords('54400420'), cep_to_coords('54440420'), cep_to_coords('54220000'), cep_to_coords('52030175'), cep_to_coords('54120350'), cep_to_coords('55630000'), cep_to_coords('53300210'), cep_to_coords('54440071'), cep_to_coords('51021000'), cep_to_coords('56540000'), cep_to_coords('50640460'), cep_to_coords('53030060'), cep_to_coords('52051350'), cep_to_coords('54270020'), cep_to_coords('53220130'), cep_to_coords('53030260'), cep_to_coords('50721290'), cep_to_coords('52160838'), cep_to_coords('52110100'), cep_to_coords('52110060'), cep_to_coords('52130000'), cep_to_coords('50950005'), cep_to_coords('52191280'), cep_to_coords('50761340'), cep_to_coords('54240010'), cep_to_coords('52220705'), cep_to_coords('52011055'), cep_to_coords('55640000'), cep_to_coords('53530400'), cep_to_coords('53650575'), cep_to_coords('53416560'), cep_to_coords('55602390'), cep_to_coords('52040250'), cep_to_coords('52130900'), cep_to_coords('51230080'), cep_to_coords('54100680'), cep_to_coords('50060470'), cep_to_coords('51190660'), cep_to_coords('52070013'), cep_to_coords('55270000'), cep_to_coords('53530140'), cep_to_coords('52120320'), cep_to_coords('53350144'), cep_to_coords('54000580'), cep_to_coords('53230191'), cep_to_coords('54740660'), cep_to_coords('51200050'), cep_to_coords('50050400'), cep_to_coords('50740270'), cep_to_coords('55800000'), cep_to_coords('54160680'), cep_to_coords('54589170'), cep_to_coords('54120550'), cep_to_coords('56230500'), cep_to_coords('51170135'), cep_to_coords('50980160'), cep_to_coords('53615772'), cep_to_coords('53625772'), cep_to_coords('53600000'), cep_to_coords('52120057'), cep_to_coords('50040380'), cep_to_coords('52041915'), cep_to_coords('54270100'), cep_to_coords('50940000'), cep_to_coords('53110000'), cep_to_coords('53180160'), cep_to_coords('54789510'), cep_to_coords('50750290'), cep_to_coords('21030500'), cep_to_coords('54325280'), cep_to_coords('53121360'), cep_to_coords('53405615'), cep_to_coords('50920650'), cep_to_coords('54120200'), cep_to_coords('51780000'), cep_to_coords('51130020'), cep_to_coords('51130200'), cep_to_coords('53280090'), cep_to_coords('52081372'), cep_to_coords('53210250'), cep_to_coords('52070647'), cep_to_coords('51020250'), cep_to_coords('53437610'), cep_to_coords('53439430'), cep_to_coords('50740000'), cep_to_coords('51111220'), cep_to_coords('52060280'), cep_to_coords('52051240'), cep_to_coords('52191241'), cep_to_coords('53170270'), cep_to_coords('53080670'), cep_to_coords('55292583'), cep_to_coords('55295300'), cep_to_coords('52020220'), cep_to_coords('50610150'), cep_to_coords('54753140'), cep_to_coords('52041055'), cep_to_coords('51021550'), cep_to_coords('54150095'), cep_to_coords('50920735'), cep_to_coords('56912500'), cep_to_coords('56780000'), cep_to_coords('52020140'), cep_to_coords('50800120'), cep_to_coords('51110290'), cep_to_coords('55650000'), cep_to_coords('51150400'), cep_to_coords('50610120'), cep_to_coords('50860180'), cep_to_coords('50760016'), cep_to_coords('50820480'), cep_to_coords('50640280'), cep_to_coords('52030140'), cep_to_coords('50750400'), cep_to_coords('53030080'), cep_to_coords('55614727'), cep_to_coords('54430200'), cep_to_coords('53370450'), cep_to_coords('55515000'), cep_to_coords('53000600'), cep_to_coords('54783010'), cep_to_coords('50860000'), cep_to_coords('50680180'), cep_to_coords('52011040'), cep_to_coords('50090075'), cep_to_coords('50810777'), cep_to_coords('50771040'), cep_to_coords('50030280'), cep_to_coords('50781430'), cep_to_coords('54350000'), cep_to_coords('54786160'), cep_to_coords('54753785'), cep_to_coords('53010430'), cep_to_coords('53370260'), cep_to_coords('53180670'), cep_to_coords('53435610'), cep_to_coords('53140210'), cep_to_coords('52020015'), cep_to_coords('52020010'), cep_to_coords('53050440'), cep_to_coords('55610350'), cep_to_coords('54400020'), cep_to_coords('54330680'), cep_to_coords('52050555'), cep_to_coords('50930380'), cep_to_coords('53330550'), cep_to_coords('52280232'), cep_to_coords('52051280'), cep_to_coords('52060150'), cep_to_coords('53050170'), cep_to_coords('52030010'), cep_to_coords('50870520'), cep_to_coords('50721170'), cep_to_coords('50721175'), cep_to_coords('52040350'), cep_to_coords('53435030'), cep_to_coords('54762620'), cep_to_coords('55815140'), cep_to_coords('53082080'), cep_to_coords('50920135'), cep_to_coords('51020000'), cep_to_coords('50730670'), cep_to_coords('50790150'), cep_to_coords('53130350'), cep_to_coords('51170390'), cep_to_coords('50980645'), cep_to_coords('54762315'), cep_to_coords('50050450'), cep_to_coords('50710100'), cep_to_coords('50711290'), cep_to_coords('50741350'), cep_to_coords('52171011'), cep_to_coords('50731230'), cep_to_coords('54762740'), cep_to_coords('50761620'), cep_to_coords('50810040'), cep_to_coords('54762640'), cep_to_coords('52080250'), cep_to_coords('50780020'), cep_to_coords('52490300'), cep_to_coords('50720680'), cep_to_coords('52110440'), cep_to_coords('52041430'), cep_to_coords('55850000'), cep_to_coords('50810460'), cep_to_coords('55745000'), cep_to_coords('53404030'), cep_to_coords('29815000'), cep_to_coords('53190310'), cep_to_coords('54740570'), cep_to_coords('51020280'), cep_to_coords('53431690'), cep_to_coords('53150360'), cep_to_coords('54759270'), cep_to_coords('51010210'), cep_to_coords('51150130'), cep_to_coords('55296510'), cep_to_coords('55290000'), cep_to_coords('50610320'), cep_to_coords('54330561'), cep_to_coords('52070010'), cep_to_coords('54786770'), cep_to_coords('50800080'), cep_to_coords('53370550'), cep_to_coords('51300130'), cep_to_coords('50970350'), cep_to_coords('52090046'), cep_to_coords('53140015'), cep_to_coords('53150260'), cep_to_coords('54430160'), cep_to_coords('53435550'), cep_to_coords('53437360'), cep_to_coords('55240000'), cep_to_coords('55200000'), cep_to_coords('50731340'), cep_to_coords('54320302'), cep_to_coords('51270170'), cep_to_coords('50810420'), cep_to_coords('53210160'), cep_to_coords('53060380'), cep_to_coords('50710310'), cep_to_coords('53130070'), cep_to_coords('52160835'), cep_to_coords('52211100'), cep_to_coords('50761060'), cep_to_coords('54460640'), cep_to_coords('54340080'), cep_to_coords('52020000'), cep_to_coords('53900000'), cep_to_coords('53080410'), cep_to_coords('53431020'), cep_to_coords('51240350'), cep_to_coords('55602000'), cep_to_coords('51170320'), cep_to_coords('53270645'), cep_to_coords('54330300'), cep_to_coords('53220375'), cep_to_coords('50100280'), cep_to_coords('54330380'), cep_to_coords('54330038'), cep_to_coords('52210330'), cep_to_coords('53403500'), cep_to_coords('91021100'), cep_to_coords('52080040'), cep_to_coords('51030140'), cep_to_coords('50750230')


# In[ ]:





# In[ ]:


#it's better to do the CEP'S on a separate jupyter notebook, and then come back to this one


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


pd.set_option('display.max_rows', None)


# In[91]:


bancoesusalltabsrais2019.isna().sum()


# In[ ]:


import missingno as msno


# In[ ]:


msno.bar(bancoesusalltabsrais2019)


# In[ ]:


bancoesusalltabsrais2019.nunique()


# In[ ]:


bancoesusalltabsrais2019.dtypes


# In[ ]:


pd.set_option('display.max_columns', None)


# In[ ]:


pd.set_option('display.max_rows', 10)


# In[ ]:


bancoesusalltabsrais2019.head(3)


# In[ ]:


bancoesusalltabsrais2019.describe()


# In[ ]:


pd.set_option('display.max_rows', None)


# In[92]:


bancoesusalltabsrais2019.isnull().sum().sort_values(ascending=False)


# In[93]:


list(bancoesusalltabsrais2019.isnull().sum().sort_values(ascending=False).index)


# In[ ]:


pd.set_option('display.max_columns', None)


# In[94]:


#dropping columns with more than 100k missing values, except 'condicoes' that are the comorbities that might be related to death


# In[95]:


bancoesusalltabsrais2019.drop(columns=['DATA DE SAÍDA DA HOSPITALIZAÇÃO',
 'TRIMESTRE',
 'DATA DA HOSPITALIZAÇÃO',
 'estrangeiro',
 'OUTRA, QUAL (PROF. SAÚDE)?',
 'OUTRA, QUAL (PROF. SEG)?',
 'OUTRA, QUAL (OCUPAÇÃO)?',
 'LOCAL DA HOSPITALIZAÇÃO',
 'CATEGORIA DA OCUPAÇÃO',
 'CATEGORIA PROF. DE SEG.',
 'CATEGORIA DO PROF. DE SAÚDE',
 'ESFERA DE GESTÃO',
 'etnia',
 'SETOR DO ÓBITO',
 'DATA DA CONFIRMAÇÃO DO ÓBITO',
 'QUAL UNIDADE?',
 'DATA DO ÓBITO',
 'LOCAL DO ÓBITO',
 'OUTRAS MORBIDADES PRÉVIAS (QUAIS)?',
 'resultadoTesteSorologicoTotais',
 'OUTRO LOCAL DE INTERNAMENTO (NA NOTIFICAÇÃO)',
 'OUTRA UNIDADE NOTIFICADORA',
 'GESTANTE',
 'CONTATO PRÓXIMO DE PROF. DE SAÚDE OU DE SEG. PÚBLICA?',
 'OUTRA OCUPAÇÃO',
 'É SERVIÇO PÚBLICO?',
 'DATA DE CONFIRMAÇÂO',
 'ATUALIZAÇÃO (CLASSIF.)',
 'EXAME',
 'UNIDADE COLETORA',
 'TIPO DE MATERIAL COLETADO',
 'LABORATÓRIO',
 'TIPO DE LABORATÓRIO',
 'DATA DO RESULTADO',
 'DATA DE RECEBIMENTO DA AMOSTRA',
 'RESULTADO DO TESTE',
 'STATUS NO GAL',
 'ATUALIZAÇÂO (EVOLUÇÂO)',
 'LOCAL DE INTERNAMENTO (NA NOTIFICAÇÃO)',
 'IDENTIDADE DE GÊNERO',
 'ORIENTAÇÃO SEXUAL',
 'ENDEREÇO COMPLETO',
 'TIPO DA NOTIFICAÇÃO',
 'COLETA DE EXAMES',
 'UNIDADE NOTIFICADORA',
 'INTERNADO',
 'ID',
 'paisOrigem',
 'resultadoTesteSorologicoIgM',
 'resultadoTesteSorologicoIgG',
 'dataTesteSorologico',
 'tipoTesteSorologico',
 'testeSorologico',
 'notificadorCNPJ',
 'telefone',
 'cbo',
 'complemento',
 'cns',
 'nomeMae',
 'outrosSintomas',
 'cnes','_merge'], axis = 1, inplace=True)


# In[ ]:


list(bancoesusalltabsrais2019.isnull().sum().sort_values(ascending=False).index)


# In[ ]:


#bancoesusalltabsrais2019.drop({'DATA DE SAÍDA DA HOSPITALIZAÇÃO',..., '_merge'}, axis = 'columns', inplace = True)


# In[ ]:


bancoesusalltabsrais2019.shape


# In[ ]:


bancoesusalltabsrais2019.isnull().sum().sort_values(ascending=False)


# In[ ]:


bancoesusalltabsrais2019.head(3)


# In[ ]:


bancoesusalltabsrais2019.evolucaoCaso.unique()


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['evolucaoCaso']=='ÓBITO']


# In[ ]:


bancoesusalltabsrais2019['evolucaoCaso'].unique()


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['evolucaoCaso']=='ÓBITO'].shape


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['evolucaoCaso']=='Cura'].shape


# In[ ]:


bancoesusalltabsrais2019['resultadoTeste'].unique()


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['resultadoTeste']=='Positivo'].shape


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['resultadoTeste']=='Negativo'].shape


# In[ ]:


bancoesusalltabsrais2019['Resultado Final'].unique()


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['Resultado Final']=='Positivo'].shape


# In[ ]:


bancoesusalltabsrais2019[bancoesusalltabsrais2019['Resultado Final']=='Negativo'].shape


# In[ ]:


pd.set_option('display.max_rows', 10)


# In[96]:


bancoesusalltabsrais2019.head(3)


# In[ ]:


bancoesusalltabsrais2019['classificacaoFinal'].unique()


# In[97]:


bancoesusrais2019selecionado = bancoesusalltabsrais2019[['condicoes','estado', 'evolucaoCaso', 'dataInicioSintomas', 'cpf', 
                          'nomeCompletoDesnormalizado','dataNascimento','resultadoTeste', 'bairro', 
                          'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao', 'sintomas', 'cep', 'idade', 'racaCor',
                         'profissionalSeguranca','tipoTeste','sexo', 'Resultado Final','Tipo Vínculo','Escolaridade após 2005','Vl Remun Média Nom','Vl Remun Média (SM)',
                          'Tempo Emprego' ,'Qtd Hora Contr','CBO Ocupação 2002','CNAE 2.0 Classe','CNAE 2.0 Subclasse','Qtd Dias Afastamento',
                          'IBGE Subsetor','CEP Estab','Mun Trab']]


# In[98]:


bancoesusrais2019selecionado.head(3)


# In[99]:


bancoesusrais2019selecionado.shape


# In[100]:


pd.Timestamp.min


# In[101]:


pd.Timestamp.max


# In[102]:


bancoesusrais2019selecionado['dataNascimento'] = pd.to_datetime(bancoesusrais2019selecionado['dataNascimento'], errors = 'coerce') #This will force the dates which are outside the bounds to NaT


# In[103]:


bancoesusrais2019selecionado.shape


# In[104]:


bancoesusrais2019selecionado.head(3)


# In[105]:


bancoesusrais2019selecionado['dataNascimento'].isna().sum() 


# In[ ]:


pd.set_option('display.max_columns', None)


# In[106]:


bancoesusrais2019selecionado.head(3)


# In[107]:


bancoesusrais2019selecionado['cep'] = bancoesusrais2019selecionado['cep'].str.replace('.','')
bancoesusrais2019selecionado['cep'] = bancoesusrais2019selecionado['cep'].str.replace('-','')


# In[108]:


bancoesusrais2019selecionado.head(3)


# In[109]:


bancoesusrais2019selecionado.to_excel('bancoesusrais2019selecionado.xlsx', index = False)


# # Banco Esus Rais 2019 selecionado

# In[110]:


import pandas as pd


# In[111]:


bancoesusrais2019selecionado = pd.read_excel('bancoesusrais2019selecionado.xlsx')


# In[112]:


bancoesusrais2019selecionado.head(3)


# In[179]:


pd.set_option('display.max_columns', None)


# In[180]:


bancoesusrais2019selecionado.head(3)


# In[113]:


bancoesusrais2019selecionado.shape


# In[182]:


#cep, intervalo de renda, setor atividades cnae, grouby bairro, groupby municipio, mapas, gráficos etc


# In[115]:


#dropping na before adding the 'condicoes' (comorbity column) had 150k rows, now it has only 13k
#but it's important to keep comorbity, because on this data, everyone who died had a comorbity


# In[114]:


bancoesusrais2019selecionado.dropna().shape


# In[184]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].unique()


# In[119]:


import plotly.express as px


# In[120]:


fig = px.pie(bancoesusrais2019selecionado, names='evolucaoCaso')
fig.show()


# In[187]:


fig = px.pie(bancoesusrais2019selecionado, names='estado')
fig.show()


# In[121]:


bancoesusrais2019selecionado['estado'] = bancoesusrais2019selecionado['estado'].str.upper()


# In[189]:


fig = px.pie(bancoesusrais2019selecionado, names='estado')
fig.show()


# In[190]:


fig = px.pie(bancoesusrais2019selecionado, names='resultadoTeste')
fig.show()


# In[191]:


fig = px.pie(bancoesusrais2019selecionado, names='Resultado Final')
fig.show()


# In[122]:


bancoesusrais2019selecionado['Resultado Final'].unique()


# In[193]:


fig = px.pie(bancoesusrais2019selecionado, names='profissionalSaude')
fig.show()


# In[123]:


bancoesusrais2019selecionado = bancoesusrais2019selecionado[(bancoesusrais2019selecionado['profissionalSaude']=='Sim') | (bancoesusrais2019selecionado['profissionalSaude']=='Não')] 


# In[ ]:





# In[20]:


#bancoesusrais2019selecionado.rename({'profissionalSaude':'Health Professionals'}, axis = 1, inplace = True)


# In[195]:


fig = px.pie(bancoesusrais2019selecionado, names='profissionalSaude')
fig.show()


# In[124]:


bancoesusrais2019selecionado['profissionalSaude'].unique()


# In[125]:


bancoesusrais2019selecionado['Health Professionals'] = bancoesusrais2019selecionado['profissionalSaude']
bancoesusrais2019selecionado['Health Professionals'] = bancoesusrais2019selecionado['Health Professionals'].str.replace('Sim', '1')
bancoesusrais2019selecionado['Health Professionals'] = bancoesusrais2019selecionado['Health Professionals'].str.replace('Não', '0')
bancoesusrais2019selecionado['Health Professionals'] = bancoesusrais2019selecionado['Health Professionals'].astype(int)


# In[126]:


bancoesusrais2019selecionado['Health Professionals'].unique()


# In[127]:


bancoesusrais2019selecionado['Health Professionals'].mean()


# In[200]:


fig = px.pie(bancoesusrais2019selecionado, names='sexo')
fig.show()


# In[128]:


bancoesusrais2019selecionado = bancoesusrais2019selecionado[(bancoesusrais2019selecionado['sexo']=='Masculino') | (bancoesusrais2019selecionado['sexo']=='Feminino')] 


# In[202]:


fig = px.pie(bancoesusrais2019selecionado, names='sexo')
fig.show()


# In[203]:


fig = px.pie(bancoesusrais2019selecionado, names='tipoTeste')
fig.show()


# In[129]:


bancoesusrais2019selecionado = bancoesusrais2019selecionado[(bancoesusrais2019selecionado['tipoTeste']=='RT-PCR') | (bancoesusrais2019selecionado['tipoTeste']=='TESTE RÁPIDO - ANTICORPO') | (bancoesusrais2019selecionado['tipoTeste']=='TESTE RÁPIDO - ANTÍGENO')] 


# In[205]:


fig = px.pie(bancoesusrais2019selecionado, names='tipoTeste')
fig.show()


# [Antígeno e Anticorpo Covid](https://www.fleury.com.br/medico/artigos-cientificos/conheca-as-diferencas-entre-os-testes-diagnosticos-para-covid-19)

# In[206]:


fig = px.pie(bancoesusrais2019selecionado, names='Escolaridade após 2005')
fig.show()


# In[207]:


'''
ANALFABETO 1
ATE 5.A INC 2
5.A CO FUND 3
6. A 9. FUND 4
FUND COMPL 5
MEDIO INCOMP 6
MEDIO COMPL 7
SUP. INCOMP 8
SUP. COMP 9
MESTRADO 10
DOUTORADO 11
'''
'''
Incomplete primary education 1,2,3,4
Complete primary education 5,6
Complete secondary education 7,8
Complete higher education 9,10,11
'''


# In[130]:


import numpy as np


# In[131]:


bins = [1, 5, 7, 9, np.inf]
names = ['1-4','5-6','7-8','9-11']

bancoesusrais2019selecionado['schooling'] = pd.cut(bancoesusrais2019selecionado['Escolaridade após 2005'], bins, labels=names)

print(bancoesusrais2019selecionado.dtypes)


# In[210]:


bancoesusrais2019selecionado.head(3)


# In[132]:


bancoesusrais2019selecionado['schooling'] = bancoesusrais2019selecionado['schooling'].str.replace('1-4','Incomplete primary education')
bancoesusrais2019selecionado['schooling'] = bancoesusrais2019selecionado['schooling'].str.replace('5-6','Complete primary education')
bancoesusrais2019selecionado['schooling'] = bancoesusrais2019selecionado['schooling'].str.replace('7-8','Complete secondary education')
bancoesusrais2019selecionado['schooling'] = bancoesusrais2019selecionado['schooling'].str.replace('9-11','Complete higher education')


# In[212]:


bancoesusrais2019selecionado.head(3)


# In[133]:


bancoesusrais2019selecionado['CBO Ocupação 2002'].unique()


# In[214]:


#fig = px.bar(bancoesusrais2019selecionado, x='Escolaridade após 2005')
#fig.show()


# In[215]:


#fig = px.pie(bancoesusrais2019selecionado, names='Vl Remun Média (SM)')
#fig.show()


# In[216]:


#separar grupos de salário mínimo, separar grupos de salário


# In[134]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].unique()


# In[218]:


#https://cidades.ibge.gov.br/brasil/pesquisa/23/22787     
#divisão de salários mínimos do ibge 


# In[135]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].min


# In[136]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].sort_values()


# In[221]:


#sem rendimento (0), até 1/2 salário mínimo, mais de 1/2 a 1 salário mínimo, mais de 1 a 2 salários mínimos 
#mais de 2 a 5 salários mínimos, mais de 5 a 10 salários mínimos, mais de 10 a 20 salários mínimos, mais de 20 salários mínimos


# In[137]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'] = bancoesusrais2019selecionado['Vl Remun Média (SM)'].str.lstrip('0')


# In[223]:


#your_string.strip("0")
#to remove both trailing and leading zeros ? If you're only interested in removing trailing zeros, use .rstrip 
#instead (and .lstrip for only the leading ones).


# In[138]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].head(10)


# In[139]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].sort_values(ascending=False).head(10) #70s disappeared


# In[140]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].loc[[92354]]  


# In[141]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'] = bancoesusrais2019selecionado['Vl Remun Média (SM)'].str.replace(',','.')


# In[142]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].head(10)


# In[143]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].sort_values(ascending=False).head(10)


# In[144]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].loc[[92354]] 


# In[145]:


bancoesusrais2019selecionado['Vl Remun Média (SM)']=bancoesusrais2019selecionado['Vl Remun Média (SM)'].astype(float)


# In[146]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].sort_values(ascending=False).head(10)


# In[147]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].sort_values(ascending=True).head(10)


# In[148]:


bancoesusrais2019selecionado[bancoesusrais2019selecionado['Vl Remun Média (SM)']==0]


# In[149]:


bancoesusrais2019selecionado['Vl Remun Média (SM)'].isna().sum()


# In[150]:


bancoesusrais2019selecionado['Vl Remun Média (SM)']


# In[151]:


(10182/252397)*100


# [numeric data into bins](https://stackoverflow.com/questions/49382207/how-to-map-numeric-data-into-categories-bins-in-pandas-dataframe)

# In[238]:


'''sem rendimento (0)
até 1/2 salário mínimo
mais de 1/2 a 1 salário mínimo 
mais de 1 a 2 salários mínimos 
mais de 2 a 5 salários mínimos 
mais de 5 a 10 salários mínimos 
mais de 10 a 20 salários mínimos
mais de 20 salários mínimos
'''


# In[152]:


import numpy as np


# In[153]:


bins = [0, 0.1, 0.5,1 ,2 , 5, 10, 20, np.inf]
names = ['0', '0.1 - 1/2', '1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+']

bancoesusrais2019selecionado['meanminimumwagerange'] = pd.cut(bancoesusrais2019selecionado['Vl Remun Média (SM)'], bins, labels=names)

print(bancoesusrais2019selecionado.dtypes)


# In[154]:


bancoesusrais2019selecionado['meanminimumwagerange'] 


# In[242]:


pd.set_option('display.max_columns',None)


# In[243]:


bancoesusrais2019selecionado.head(5)


# In[244]:


fig = px.pie(bancoesusrais2019selecionado, names='meanminimumwagerange')
fig.show()


# In[155]:


bancoesusrais2019selecionado[bancoesusrais2019selecionado['meanminimumwagerange']==0]


# In[156]:


bancoesusrais2019selecionado['meanminimumwagerange'] = bancoesusrais2019selecionado['meanminimumwagerange'].str.replace('null','0')


# In[247]:


fig = px.pie(bancoesusrais2019selecionado, names='meanminimumwagerange')
fig.show()


# In[248]:


bancoesusrais2019selecionado.shape


# In[249]:


bancoesusrais2019selecionado.head(3)


# In[157]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].unique()


# In[158]:


bancoesusrais2019selecionado['CNAE 2.0 Subclasse'].unique()


# In[159]:


bancoesusrais2019selecionado['CBO Ocupação 2002'].unique()


# In[160]:


bancoesusrais2019selecionado['IBGE Subsetor'].unique()


# In[161]:


bancoesusrais2019selecionado.head(3)


# In[255]:


fig = px.pie(bancoesusrais2019selecionado, names='IBGE Subsetor')
fig.show()


# In[256]:


'''
Subsetor de Atividade Econômica - CNAE/80 (IBGE)
Ícone. Clique para retornar à página inicial.Página Inicial
Ícone. Clique para imprimir esta página.Imprimir
Ícone. Clique para enviar esta página por e-mail.Enviar
Ícone. Clique para retornar à página anterior.Voltar
Código	Categoria	Descrição
01	EXTR MINERAL	EXTRACAO DE MINERAIS
02	MIN NAO MET	INDUSTRIA DE PRODUTOS MINERAIS NAO METALICOS
03	IND METAL	INDUSTRIA METALURGICA
04	IND MECANICA	INDUSTRIA MECANICA
05	ELET E COMUN	INDUSTRIA DO MATERIAL ELETRICO E DE COMUNICACOES
06	MAT TRANSP	INDUSTRIA DO MATERIAL DE TRANSPORTE
07	MAD E MOBIL	INDUSTRIA DA MADEIRA E DO MOBILIARIO
08	PAPEL E GRAF	INDUSTRIA DO PAPEL, PAPELAO, EDITORIAL E GRAFICA
09	BOR FUN COUR	IND. DA BORRACHA, DO FUMO, DE COUROS, PELES E PROD. SIMIL. E IND. DIV.
10	IND QUIMICA	IND. QUIM., DE PROD. FARM., VETER., DE PERF., SABOES, VELAS E MAT. PLA
11	IND TEXTIL	INDUSTRIA TEXTIL, DO VESTUARIO E ARTEFATOS DE TECIDOS
12	IND CALCADOS	INDUSTRIA DE CALCADOS
13	ALIM E BEB	INDUSTRIA DE PROD. ALIMENTICIOS, DE BEBIDAS E ALCOOL ETILICO.
14	SERV UTIL PUB	SERVICOS INDUSTRIAIS DE UTILIDADE PUBLICA
15	CONSTR CIVIL	CONSTRUCAO CIVIL
16	COM VAREJ	COMERCIO VAREJISTA
17	COM ATACAD	COMERCIO ATACADISTA
18	INST FINANC	INSTITUICOES DE CREDITO, SEGUROS E DE CAPITALIZACAO
19	ADM TEC PROF	COM,ADM.IMOV,VAL.MOB,SERV.TECN-PROF,AUX.ATIV.ECON E ORG.INT E REP. INT
20	TRAN E COMUN	TRANSPORTE E COMUNICACOES
21	ALOJ COMUNIC	SERV.ALOJ, ALIM,REP,MANUT,RES, DOMIC,DIVERS,RADIO DIF,TV,COM ESOC
22	MED ODON VET	SERVICOS MEDICOS, ODONTOLOGICOS E VETERINARIOS
23	ENSINO	ENSINO
24	ADM PUBLICA	ADM. PUBLICA DIRETA E AUTARQUICA
25	AGRICULTURA	AGRIC., SILVICULTURA, CRIACAO DE ANIM., EXTR.VEG., PESCA E AGRICULTURA
26	OUTROS	OUTROS
--	IGNORADO	IGNORADO
'''


# [ibgesubsetor](http://acesso.mte.gov.br/portal-pdet/o-pdet/o-programa/detalhes-municipio-7.htm) site do ibge estava fora do ar

# [classes cnae](https://cnae.ibge.gov.br/classificacoes/por-tema/atividades-economicas)
# [21 seções](https://cnae.ibge.gov.br/?option=com_cnae&view=estrutura&Itemid=6160&chave=&tipo=cnae&versao_classe=7.0.0&versao_subclasse=9.1.0)

# In[257]:


#https://concla.ibge.gov.br/images/concla/documentacao/CNAE20_Introducao.pdf


# In[162]:


bancoesusrais2019selecionado['IBGE Subsetor'].value_counts()


# In[163]:


bancoesusrais2019selecionado['IBGE Subsetor'].value_counts(normalize=True)


# In[260]:


#px.bar(bancoesusrais2019selecionado, x='IBGE Subsetor', y='meanminimumwagerange')


# In[261]:


px.bar(bancoesusrais2019selecionado, x=bancoesusrais2019selecionado.groupby('meanminimumwagerange').size(), y=bancoesusrais2019selecionado.groupby('meanminimumwagerange').size())


# In[164]:


bancoesusrais2019selecionado.groupby('meanminimumwagerange').size()


# In[263]:


bancoesusrais2019selecionado.head(3)


# In[165]:


bancoesusrais2019selecionado.groupby('meanminimumwagerange').size()


# In[166]:


bancoesusrais2019selecionado.groupby('IBGE Subsetor').size()


# In[167]:


bancoesusrais2019selecionado.groupby(['IBGE Subsetor','meanminimumwagerange']).size().unstack(fill_value=0).plot.bar();


# In[168]:


bancoesusrais2019selecionado.groupby(['meanminimumwagerange','IBGE Subsetor']).size().plot.bar();


# In[170]:


import matplotlib.pyplot as plt


# In[172]:


fig, ax = plt.subplots(figsize=(15,7))
bancoesusrais2019selecionado.groupby('IBGE Subsetor').size().plot(ax=ax);


# In[173]:


fig, ax = plt.subplots(figsize=(15,7))
bancoesusrais2019selecionado.groupby('meanminimumwagerange').size().plot(ax=ax);


# In[174]:


fig, ax = plt.subplots(figsize=(15,7))
bancoesusrais2019selecionado.groupby('IBGE Subsetor').size().plot(ax=ax);


# In[175]:


bancoesusrais2019selecionado.groupby(['meanminimumwagerange'])['IBGE Subsetor'].sum().plot();


# In[176]:


bancoesusrais2019selecionado.groupby(['meanminimumwagerange'])['IBGE Subsetor'].sum().plot(kind='barh');


# In[177]:


bancoesusrais2019selecionado.groupby(['meanminimumwagerange','racaCor'])['IBGE Subsetor'].sum().unstack().plot();


# In[178]:


bancoesusrais2019selecionado.columns


# [groupyby plots git](https://scentellegher.github.io/programming/2017/07/15/pandas-groupby-multiple-columns-plot.html)

# [plots with pandas groupby medium](https://python.plainenglish.io/making-plots-with-the-pandas-groupby-ac492941af28)

# [densityplots](https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0)

# In[276]:


'''
bancoesusrais2019selecionado.groupby('IBGE Subsetor')['estado', 'evolucaoCaso', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'cep', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr', 'CBO Ocupação 2002',
       'CNAE 2.0 Classe', 'CNAE 2.0 Subclasse', 'Qtd Dias Afastamento', 'CEP Estab', 'Mun Trab', 'meanminimumwagerange'].max()
'''


# In[179]:


bancoesusrais2019selecionado.describe()


# In[278]:


'''
bancoesusrais2019selecionado.groupby('municipio')['estado', 'evolucaoCaso', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'cep', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr', 'CBO Ocupação 2002',
       'CNAE 2.0 Classe', 'CNAE 2.0 Subclasse', 'Qtd Dias Afastamento','IBGE Subsetor','CEP Estab', 'Mun Trab', 'meanminimumwagerange'].max()
'''


# [age groups](https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html)

# In[279]:


'''
0-4 years old	
5-17 years old	
18-29 years old	
30-39 years old	
40-49 years old	
50-64 years old	
65-74 years old	
75-84 years old	
85+ years old
'''


# In[180]:


bins = [0, 5, 18, 30, 40, 50, 65, 75, 85, np.inf]
names = ['0 - 4','5 - 17', '18 - 29', '30 - 39','40 - 49','50 - 64','65 - 74','75 - 84', '85+']

bancoesusrais2019selecionado['agecohort'] = pd.cut(bancoesusrais2019selecionado['idade'], bins, labels=names)

print(bancoesusrais2019selecionado.dtypes)


# In[281]:


bancoesusrais2019selecionado.head(3)


# In[181]:


fig, ax = plt.subplots(figsize=(15,7))
bancoesusrais2019selecionado.groupby('agecohort').size().plot(ax=ax);


# In[283]:


fig = px.pie(bancoesusrais2019selecionado, names='agecohort')
fig.show()


# In[182]:


bancoesusrais2019selecionado.shape


# In[285]:


bancoesusrais2019selecionado.head(3)


# In[183]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].value_counts().unique()


# In[287]:


bancoesusrais2019selecionado['CNAE 2.0 Subclasse'].value_counts().unique()


# In[184]:


bancoesusrais2019selecionado['CNAE 2.0 Subclasse'].nunique()


# In[185]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].nunique()


# [nunique](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.nunique.html)

# In[186]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].value_counts()


# [valuecounts](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html)

# In[187]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].unique()


# In[188]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].value_counts().nunique()


# [IBGE Subclasse](https://concla.ibge.gov.br/busca-online-cnae.html?classe=84124&tipo=cnae&versao=9&view=classe) 
# 
# [IBGE CNAE 2.0 21 Seções](https://cnae.ibge.gov.br/?view=estrutura)

# In[189]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].nunique()


# In[190]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].unique()


# In[191]:


bancoesusrais2019selecionado.head(3)


# In[296]:


bancoesusrais2019selecionado['CBO Ocupação 2002'].value_counts().unique()


# In[192]:


bancoesusrais2019selecionado['IBGE Subsetor'].unique()


# In[298]:


bancoesusrais2019selecionado.groupby(['CNAE 2.0 Classe']).agg(sum)


# In[193]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].nunique()


# In[194]:


bancoesusrais2019selecionado['CNAE 2.0 Subclasse'].nunique()


# In[196]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].unique()


# In[197]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].nunique()


# [IBGE Subclasse](https://concla.ibge.gov.br/busca-online-cnae.html?classe=84124&tipo=cnae&versao=9&view=classe) 
# 
# [IBGE CNAE 2.0 21 Seções](https://cnae.ibge.gov.br/?view=estrutura)

# In[303]:


'''
Seção	Divisões	Denominação
A	01 .. 03	AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA
B	05 .. 09	INDÚSTRIAS EXTRATIVAS
C	10 .. 33	INDÚSTRIAS DE TRANSFORMAÇÃO
D	35 .. 35	ELETRICIDADE E GÁS
E	36 .. 39	ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO
F	41 .. 43	CONSTRUÇÃO
G	45 .. 47	COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
H	49 .. 53	TRANSPORTE, ARMAZENAGEM E CORREIO
I	55 .. 56	ALOJAMENTO E ALIMENTAÇÃO
J	58 .. 63	INFORMAÇÃO E COMUNICAÇÃO
K	64 .. 66	ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS
L	68 .. 68	ATIVIDADES IMOBILIÁRIAS
M	69 .. 75	ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS
N	77 .. 82	ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES
O	84 .. 84	ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL
P	85 .. 85	EDUCAÇÃO
Q	86 .. 88	SAÚDE HUMANA E SERVIÇOS SOCIAIS
R	90 .. 93	ARTES, CULTURA, ESPORTE E RECREAÇÃO
S	94 .. 96	OUTRAS ATIVIDADES DE SERVIÇOS
T	97 .. 97	SERVIÇOS DOMÉSTICOS
U	99 .. 99	ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS
'''


# In[304]:


#bins = [0, 5, 18, 30, 40, 50, 65, 75, 85, np.inf]
#names = ['0 - 4','5 - 17', '18 - 29', '30 - 39','40 - 49','50 - 64','65 - 74','75 - 84', '85+']

#bancoesusrais2019selecionado['economicsector'] = pd.cut(bancoesusrais2019selecionado['CNAE 2.0 Classe'], bins, labels=names)

#print(bancoesusrais2019selecionado.dtypes)


# In[198]:


bancoesusrais2019selecionado.head(3)


# In[306]:


bancoesusrais2019selecionado.sort_values(by = 'CNAE 2.0 Classe').head(3)


# In[307]:


bancoesusrais2019selecionado.sort_values(by = 'IBGE Subsetor').head(3)


# In[308]:


#pip install pillow


# In[309]:


#from PIL import Image
#myImage = Image.open('25 subsetor ibge.jpg');
#myImage.show();


# In[199]:


from IPython.display import Image
Image(filename='25 subsetor ibge.jpg') 


# [CONCLA CNAE IBGE](https://cnae.ibge.gov.br/?view=classe&tipo=cnae&versao=7&classe=01199)

# In[311]:


bancoesusrais2019selecionado.head(3)


# In[200]:


bancoesusrais2019selecionado['sex'] = bancoesusrais2019selecionado['sexo']
bancoesusrais2019selecionado['sex'] = bancoesusrais2019selecionado['sex'].str.replace('Masculino', '1')
bancoesusrais2019selecionado['sex'] = bancoesusrais2019selecionado['sex'].str.replace('Feminino', '0')
bancoesusrais2019selecionado['sex'].astype(int)


# In[201]:


bancoesusrais2019selecionado['sex'].unique()


# In[315]:


bancoesusrais2019selecionado.head(3)


# In[202]:


bancoesusrais2019selecionado.shape


# In[203]:


bancoesusrais2019selecionado['racaCor'].unique()


# In[204]:


bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Indígena', 'Indigena')
bancoesusrais2019selecionado['racaCor'].unique()


# In[319]:


fig = px.pie(bancoesusrais2019selecionado, names='racaCor')
fig.show()


# In[205]:


'''
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Parda', 'Non-white')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Amarela', 'Non-white')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Preta', 'Non-white')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Ignorado', 'Uninformed race')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Indigena', 'Non-white')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Branca', 'White')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('Non-white', '1')
bancoesusrais2019selecionado['racaCor'] = bancoesusrais2019selecionado['racaCor'].str.replace('White', '0')
#bancoesusrais2019selecionado['racaCor'].astype(int)
bancoesusrais2019selecionado.rename({'racaCor':'race'}, axis=1, inplace = True)
'''
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['racaCor']
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['race'].str.replace('Parda', 'Brown')
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['race'].str.replace('Branca', 'White')
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['race'].str.replace('Amarela', 'Yellow')
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['race'].str.replace('Preta', 'Black')
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['race'].str.replace('Indigena', 'Indigenous')
bancoesusrais2019selecionado['race'] = bancoesusrais2019selecionado['race'].str.replace('Ignorado', 'Ignored')


# In[321]:


#bancoesusrais2019selecionado.rename({'racaCor':'race'}, axis = 1, inplace = True)


# In[206]:


bancoesusrais2019selecionado['race'].unique()


# In[323]:


fig = px.pie(bancoesusrais2019selecionado, names='race')
fig.show()


# In[324]:


bancoesusrais2019selecionado.head(3)


# In[325]:


#bancoesusrais2019selecionado['race'] =='Uninformed race'


# In[326]:


#bancoesusrais2019selecionado['Uninformed race'] = bancoesusrais2019selecionado['race'] =='Uninformed race'


# In[327]:


#bancoesusrais2019selecionado['Uninformed race'] = bancoesusrais2019selecionado['Uninformed race'].astype(int)


# In[328]:


#bancoesusrais2019selecionado.loc[bancoesusrais2019selecionado['race'].isin(['1','0'])]


# In[329]:


#bancoesusrais2019selecionado.shape


# In[330]:


#bancoesusrais2019selecionado['Uninformed race'].shape


# In[331]:


#bancoesusrais2019selecionado['race'].unique()


# In[332]:


#bancoesusrais2019selecionado[(bancoesusrais2019selecionado['race'] =='0') | (bancoesusrais2019selecionado['race'] =='1')]


# In[207]:


from IPython.display import Image
Image(filename='25 subsetor ibge.jpg')


# In[334]:


fig = px.pie(bancoesusrais2019selecionado, names='IBGE Subsetor')
fig.show()


# In[335]:


'''
24 Administração Pública - Public Administration
16 Comércio Varejista - Retail trade
19 Adm Técnica Profissional - Professional Technical Administration
21 Aloj Comunicações - Communication Accommodation
22 - Médicos Odontológico Vet. - doctors, dentist and veterinarians economic sector -> Human health activities
23 - Ensino -> Education
20 - Transporte e comunicação -> Transport and Communication
17 - Comércio Atacadista -> Wholesale 
13 - Alimentos e Bebidas -> Food and Drink
15 - Construção Civil -> Construction
Other activities 


16+17 (Essential wholesale(17) and retail trade (16))
'''


# In[208]:


bancoesusrais2019selecionado['IBGE Subsector']  = bancoesusrais2019selecionado['IBGE Subsetor'].astype(str)


# In[209]:


bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('24', 'Public Administration')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('16', 'Retail trade')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('19', 'Professional Technical Administration')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('21', 'Communication Accommodation')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('22', 'Human health activities')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('23', 'Education')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('20', 'Transport and Communication')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('17', 'Wholesale')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('13', 'Food and Drink')
bancoesusrais2019selecionado['IBGE Subsector'] = bancoesusrais2019selecionado['IBGE Subsector'].str.replace('15', 'Construction')


# In[210]:


bancoesusrais2019selecionado['IBGE Subsector'].unique()


# In[211]:


bancoesusrais2019selecionado['IBGE Subsector'].replace({'1': 'Other activities', '14': 'Other activities', '8': 'Other activities',
                                                       '25': 'Other activities', '18':'Other activities', '6':'Other activities',
                                                      '9':'Other activities','3':'Other activities', '5':'Other activities',
                                                      '10':'Other activities','4':'Other activities','7':'Other activities',
                                                      '11':'Other activities','2':'Other activities','12':'Other activities'}, inplace = True)


# In[212]:


bancoesusrais2019selecionado['IBGE Subsector'].unique()


# In[341]:


#bancoesusrais2019selecionado.rename({'IBGE Subsector':'Economic activities'}, axis = 1, inplace = True)


# In[342]:


fig = px.pie(bancoesusrais2019selecionado, names='IBGE Subsector')
fig.show()


# In[343]:


bancoesusrais2019selecionado.head(3)


# In[213]:


bancoesusrais2019selecionado['profissionalSeguranca'].unique()


# In[214]:


bancoesusrais2019selecionado['security professional'] = bancoesusrais2019selecionado['profissionalSeguranca']
bancoesusrais2019selecionado['security professional'] = bancoesusrais2019selecionado['security professional'].str.replace('Não', '0')
bancoesusrais2019selecionado['security professional'] = bancoesusrais2019selecionado['security professional'].str.replace('Sim', '1')


# In[215]:


bancoesusrais2019selecionado['security professional'].unique()


# In[216]:


bancoesusrais2019selecionado['security professional'].isna().sum() 


# In[217]:


bancoesusrais2019selecionado['security professional'].dropna


# In[218]:


bancoesusrais2019selecionado.dropna(subset=['security professional'], inplace = True)


# In[219]:


bancoesusrais2019selecionado['security professional'].unique()


# In[220]:


bancoesusrais2019selecionado['security professional'] = bancoesusrais2019selecionado['security professional'].astype(int)


# In[221]:


bancoesusrais2019selecionado['security professional'].mean()


# In[353]:


#bancoesusrais2019selecionado.rename({'profissionalSeguranca':'Security Professionals'}, axis = 1, inplace = True)


# In[ ]:





# In[354]:


#bancoesusrais2019selecionado.plot(x='Security Professionals', kind='bar')


# In[355]:


fig = px.pie(bancoesusrais2019selecionado, names='security professional')
fig.show()


# In[356]:


bancoesusrais2019selecionado.head(3)


# In[222]:


bancoesusrais2019selecionado.dropna()


# In[210]:


#bancoesusrais2019selecionadodropna = bancoesusrais2019selecionado.dropna()


# In[358]:


'''
fig = px.bar(bancoesusrais2019selecionadodropna, x='agecohort', y='meanminimumwagerange', color='schooling',
             hover_data=['evolucaoCaso', 'race'],
             height=400)
fig.update_layout(
    title={
        'text': 'Minimum Wage by Economic Activities',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center'})
fig.update_xaxes(type='category')
fig.update_yaxes(type='category')
fig.show()
'''


# In[359]:


'''fig = px.histogram(bancoesusrais2019selecionadodropna, x='agecohort', y='meanminimumwagerange', color='schooling',
             hover_data=['evolucaoCaso', 'race'],
             height=400)
fig.update_layout(
    title={
        'text': 'Minimum Wage by Economic Activities',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center'})
fig.update_xaxes(type='category')
fig.update_yaxes(type='category')
fig.show()
'''


# In[213]:


'''
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)'
#'paper_bgcolor': 'rgba(0, 0, 0, 0)'
})
'''


# In[ ]:





# In[ ]:





# In[360]:


'''fig = px.scatter(bancoesusrais2019selecionadodropna, x = 'agecohort', y = 'meanminimumwagerange', color = 'agecohort')
fig.update_layout(
    title={
        'text': 'Minimum Wage by Economic Activities',
        'y':0.95,
        'x':0.3,
        'xanchor': 'center',
        'yanchor': 'top'})
'''        


# In[361]:


bancoesusrais2019selecionado.head(3)


# In[362]:


#bancoesusrais2019selecionado.plot(x ='Vl Remun Média (SM)', y='Escolaridade após 2005', kind = 'bar')
#plt.show()


# In[363]:


'''
# creating the bar plot
import matplotlib.pyplot as plt
plt.bar(bancoesusrais2019selecionadodropna['agecohort'], bancoesusrais2019selecionado['meanminimumwagerange'])
plt.xlabel("Courses offered")
plt.ylabel("No. of students enrolled")
plt.title("Students enrolled in different courses")
plt.show()
'''


# [Bar Plot in Matplotlib](https://www.geeksforgeeks.org/bar-plot-in-matplotlib/)
# 
# [Plots from DataFrame](https://www.shanelynn.ie/bar-plots-in-python-using-pandas-dataframes/)

# In[364]:


bancoesusrais2019selecionado.head(3)


# In[217]:


#bancoesusrais2019selecionado['idade'].plot(kind='bar')


# [Mastering the Bar Plot in Python](https://towardsdatascience.com/mastering-the-bar-plot-in-python-4c987b459053)

# [Seaborn Categorical Plot Data](https://seaborn.pydata.org/tutorial/categorical.html)

# In[223]:


import seaborn as sns 


# In[224]:


sns.catplot(x="agecohort", kind="count", palette="ch:.25", data=bancoesusrais2019selecionado)


# In[369]:


'''
sns.catplot(x="agecohort", y = 'meanminimumwagerange', palette="ch:.25", data=bancoesusrais2019selecionado)
'''


# In[ ]:





# # CNAE CLASS

# In[225]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].index.astype(str).str[:2]


# In[226]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:2]


# In[ ]:





# In[227]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:2]


# In[228]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].index.astype(str).str[:2]


# In[229]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:2]


# In[376]:


#bancoesusrais2019selecionado['CNAE 2.0 Divisões'] = bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:2]


# In[377]:


#bancoesusrais2019selecionado['CNAE 2.0 Division'] = bancoesusrais2019selecionado['CNAE 2.0 Classe'].index.astype(str).str[:2]


# In[230]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:2].unique()


# In[231]:


bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:-3]


# In[232]:


bancoesusrais2019selecionado['CNAE 2.0 Division'] = bancoesusrais2019selecionado['CNAE 2.0 Classe'].astype(str).str[:-3]


# In[233]:


bancoesusrais2019selecionado.head(3)


# In[234]:


bancoesusrais2019selecionado.sort_values(by='CNAE 2.0 Division')


# In[235]:


bancoesusrais2019selecionado[bancoesusrais2019selecionado['CNAE 2.0 Division']=='3']


# In[236]:


bancoesusrais2019selecionado[bancoesusrais2019selecionado['CNAE 2.0 Division']=='4']


# In[237]:


bancoesusrais2019selecionado['CNAE 2.0 Section'] = bancoesusrais2019selecionado['CNAE 2.0 Division']


# In[388]:


bancoesusrais2019selecionado.head(3)


# In[93]:


#replacers = {',':'','.':'','-':'','ltd':'limited'} #etc....
#df1['CompanyA'] = df1['CompanyA'].replace(replacers)


# In[238]:


bancoesusrais2019selecionado['CNAE 2.0 Section'] = bancoesusrais2019selecionado['CNAE 2.0 Section'].astype(int).replace(1,'A').replace(2,'A').replace(3,'A').replace(5,'B').replace(6,'B').replace(7,'B').replace(8,'B').replace(9,'B').replace(10,'C').replace(11,'C').replace(12,'C').replace(13,'C').replace(14,'C').replace(15,'C').replace(16,'C').replace(17,'C').replace(18,'C').replace(19,'C').replace(20,'C').replace(21,'C').replace(21,'C').replace(22,'C').replace(23,'C').replace(24,'C').replace(25,'C').replace(26,'C').replace(27,'C').replace(28,'C').replace(29,'C').replace(30,'C').replace(31,'C').replace(32,'C').replace(33,'C').replace(35,'D').replace(36,'E').replace(37,'E').replace(38,'E').replace(39,'E').replace(41,'F').replace(42,'F').replace(42,'F').replace(43,'F').replace(45,'G').replace(46,'G').replace(47,'G').replace(49,'H').replace(50,'H').replace(51,'H').replace(52,'H').replace(53,'H').replace(55,'I').replace(56,'I').replace(58,'J').replace(59,'J').replace(60,'J').replace(61,'J').replace(62,'J').replace(63,'J').replace(64,'K').replace(65,'K').replace(66,'K').replace(68,'L').replace(69,'M').replace(70,'M').replace(71,'M').replace(72,'M').replace(73,'M').replace(74,'M').replace(75,'M').replace(77,'N').replace(78,'N').replace(79,'N').replace(80,'N').replace(81,'N').replace(82,'N').replace(84,'O').replace(85,'P').replace(86,'Q').replace(87,'Q').replace(88,'Q').replace(90,'R').replace(91,'R').replace(92,'R').replace(93,'R').replace(94,'S').replace(95,'S').replace(96,'S').replace(97,'T').replace(99,'U')


# In[239]:


bancoesusrais2019selecionado.head(3)


# In[240]:


bancoesusrais2019selecionado['CNAE 2.0 Section Name'] = bancoesusrais2019selecionado['CNAE 2.0 Section']


# In[392]:


bancoesusrais2019selecionado.head(3)


# In[241]:


bancoesusrais2019selecionado['CNAE 2.0 Section Name'] = bancoesusrais2019selecionado['CNAE 2.0 Section Name'].str.replace('A', 'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA').replace('B','INDÚSTRIAS EXTRATIVAS').replace('C','INDÚSTRIAS DE TRANSFORMAÇÃO').replace('D','ELETRICIDADE E GÁS').replace('E','ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO').replace('F','CONSTRUÇÃO').replace('G','COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS').replace('H','TRANSPORTE, ARMAZENAGEM E CORREIO').replace('I','ALOJAMENTO E ALIMENTAÇÃO').replace('J','INFORMAÇÃO E COMUNICAÇÃO').replace('K','ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS').replace('L', 'ATIVIDADES IMOBILIÁRIAS').replace('M','ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS').replace('N','ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES').replace('O','ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL').replace('P','EDUCAÇÃO').replace('Q','SAÚDE HUMANA E SERVIÇOS SOCIAIS').replace('R','ARTES, CULTURA, ESPORTE E RECREAÇÃO').replace('S','OUTRAS ATIVIDADES DE SERVIÇOS').replace('T','SERVIÇOS DOMÉSTICOS').replace('U','ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS')


# In[242]:


bancoesusrais2019selecionado['CNAE 2.0 Section Name']


# In[395]:


bancoesusrais2019selecionado.head(3)


# In[243]:


bancoesusrais2019selecionado['CNAE 2.0 Section Name'].unique()


# In[397]:


'''
ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL',
       'COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS',
       'ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES',
       'INDÚSTRIAS EXTRATIVAS', 'TRANSPORTE, ARMAZENAGEM E CORREIO',
       'OUTRAS ATIVIDADES DE SERVIÇOS', 'ELETRICIDADE E GÁS',
       'ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS',
       'SAÚDE HUMANA E SERVIÇOS SOCIAIS', 'CONSTRUÇÃO', 'EDUCAÇÃO',
       'ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS',
       'ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO',
       'INDÚSTRIAS DE TRANSFORMAÇÃO',
       'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
       'ARTES, CULTURA, ESPORTE E RECREAÇÃO', 'INFORMAÇÃO E COMUNICAÇÃO',
       'ALOJAMENTO E ALIMENTAÇÃO', 'ATIVIDADES IMOBILIÁRIAS',
       'SERVIÇOS DOMÉSTICOS'
'''


# In[398]:


'''
A -> AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA 
  -> AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE
    
B -> INDÚSTRIAS EXTRATIVAS
  -> EXTRACTIVE INDUSTRIES
    
C -> INDÚSTRIAS DE TRANSFORMAÇÃO
  -> PROCESSING INDUSTRIES
    
D -> ELETRICIDADE E GÁS
  -> ELECTRICITY AND GAS

E -> ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO
  -> WATER, SEWAGE, WASTE MANAGEMENT AND DECONTAMINATION ACTIVITIES

F -> CONSTRUÇÃO
  -> CONSTRUCTION
    
G -> COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
  -> TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES

H -> TRANSPORTE, ARMAZENAGEM E CORREIO
  -> TRANSPORTATION, STORAGE AND MAIL

I -> ALOJAMENTO E ALIMENTAÇÃO
  -> ACCOMMODATION AND FOOD

J -> INFORMAÇÃO E COMUNICAÇÃO
  -> INFORMATION AND COMMUNICATION

K -> ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS
  -> FINANCIAL, INSURANCE AND RELATED SERVICES ACTIVITIES

L -> ATIVIDADES IMOBILIÁRIAS
  -> REAL ESTATE ACTIVITIES

M -> ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS
  -> PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES

N -> ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES
  -> ADMINISTRATIVE ACTIVITIES AND COMPLEMENTARY SERVICES

O -> ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL
  -> PUBLIC ADMINISTRATION, DEFENSE AND SOCIAL SECURITY

P -> EDUCAÇÃO
  -> EDUCATION 

Q -> SAÚDE HUMANA E SERVIÇOS SOCIAIS
  -> HUMAN HEALTH AND SOCIAL SERVICES

R -> ARTES, CULTURA, ESPORTE E RECREAÇÃO
  -> ARTS, CULTURE, SPORTS AND RECREATION

S -> OUTRAS ATIVIDADES DE SERVIÇOS
  -> OTHER SERVICE ACTIVITIES

T -> SERVIÇOS DOMÉSTICOS
  -> DOMESTIC SERVICES

U -> ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS
  -> INTERNATIONAL BODIES AND OTHER EXTRATERRITORIAL INSTITUTIONS
'''


# In[244]:


replacers = {'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA ':'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE','INDÚSTRIAS EXTRATIVAS':'EXTRACTIVE INDUSTRIES','INDÚSTRIAS DE TRANSFORMAÇÃO':'PROCESSING INDUSTRIES','ELETRICIDADE E GÁS':'ELECTRICITY AND GAS','ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO':'WATER, SEWAGE, WASTE MANAGEMENT AND DECONTAMINATION ACTIVITIES', 'CONSTRUÇÃO':'CONSTRUCTION','COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS':'TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES','TRANSPORTE, ARMAZENAGEM E CORREIO':'TRANSPORTATION, STORAGE AND MAIL','ALOJAMENTO E ALIMENTAÇÃO':'ACCOMMODATION AND FOOD','INFORMAÇÃO E COMUNICAÇÃO':'INFORMATION AND COMMUNICATION','ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS':'FINANCIAL, INSURANCE AND RELATED SERVICES ACTIVITIES','ATIVIDADES IMOBILIÁRIAS':'REAL ESTATE ACTIVITIES','ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS':'PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES','ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES':'ADMINISTRATIVE ACTIVITIES AND COMPLEMENTARY SERVICES','ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL':'PUBLIC ADMINISTRATION, DEFENSE AND SOCIAL SECURITY','EDUCAÇÃO':'EDUCATION','SAÚDE HUMANA E SERVIÇOS SOCIAIS':'HUMAN HEALTH AND SOCIAL SERVICES','ARTES, CULTURA, ESPORTE E RECREAÇÃO':'ARTS, CULTURE, SPORTS AND RECREATION','OUTRAS ATIVIDADES DE SERVIÇOS':'OTHER SERVICE ACTIVITIES','SERVIÇOS DOMÉSTICOS':'DOMESTIC SERVICES','ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS':'INTERNATIONAL BODIES AND OTHER EXTRATERRITORIAL INSTITUTIONS'} 
bancoesusrais2019selecionado['CNAE 2.0 Section Name'] = bancoesusrais2019selecionado['CNAE 2.0 Section Name'].replace(replacers)


# In[400]:


bancoesusrais2019selecionado.head(3)


# [CNAE IBGE CONCLA Divisões](https://cnae.ibge.gov.br/?option=com_cnae&view=estrutura&Itemid=6160&chave=&tipo=cnae&versao_classe=7.0.0&versao_subclasse=9.1.0)

# In[245]:


bancoesusrais2019selecionado.rename({'CNAE 2.0 Classe':'CNAE 2.0 Class', 'CNAE 2.0 Subclasse':'CNAE 2.0 Subclass'},axis=1,inplace=True)


# In[402]:


bancoesusrais2019selecionado.head(3)


# In[246]:


bancoesusrais2019selecionado.columns


# In[ ]:


#column_names = ["C", "A", "B"]
#df = df.reindex(columns=column_names)


# In[ ]:


#rais2019cnae2 = rais2019cnae2[rais2019cnae2.columns[[2,1,0,3]]]


# In[247]:


bancoesusrais2019selecionado[['estado','condicoes','evolucaoCaso', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'cep', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr', 'CBO Ocupação 2002','Qtd Dias Afastamento',
       'CEP Estab', 'Mun Trab', 'Health Professionals', 'security professional','sex', 'race',
       'schooling', 'meanminimumwagerange', 'agecohort', 
       'IBGE Subsetor','IBGE Subsector','CNAE 2.0 Section','CNAE 2.0 Division','CNAE 2.0 Class',
       'CNAE 2.0 Subclass','CNAE 2.0 Section Name']].head(3)


# In[248]:


bancoesusrais2019selecionado = bancoesusrais2019selecionado[['estado','condicoes','evolucaoCaso', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'cep', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr', 'CBO Ocupação 2002','Qtd Dias Afastamento',
       'CEP Estab', 'Mun Trab', 'Health Professionals', 'security professional','sex', 'race',
       'schooling', 'meanminimumwagerange', 'agecohort', 
       'IBGE Subsetor','IBGE Subsector','CNAE 2.0 Section','CNAE 2.0 Division','CNAE 2.0 Class',
       'CNAE 2.0 Subclass','CNAE 2.0 Section Name']]


# In[249]:


bancoesusrais2019selecionado.head(3)


# In[250]:


bancoesusrais2019selecionado.to_excel('bancoesusrais2019selecionadocnae.xlsx',index=False)


# # CBO Ocupação 2002

# In[251]:


import pandas as pd


# In[252]:


bancoesusrais2019selecionadocnae = pd.read_excel('bancoesusrais2019selecionadocnae.xlsx')


# In[253]:


bancoesusrais2019selecionadocnae.head(3)


# In[254]:


bancoesusrais2019selecionadocnae = bancoesusrais2019selecionadocnae[['estado','condicoes','evolucaoCaso', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'cep', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr','Qtd Dias Afastamento',
       'CEP Estab', 'Mun Trab', 'Health Professionals', 'security professional','sex', 'race',
       'schooling', 'meanminimumwagerange', 'agecohort', 
       'IBGE Subsetor','IBGE Subsector','CNAE 2.0 Section','CNAE 2.0 Division','CNAE 2.0 Class',
       'CNAE 2.0 Subclass','CNAE 2.0 Section Name','CBO Ocupação 2002']]


# In[5]:


bancoesusrais2019selecionadocnae.head(3)


# In[255]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].unique()


# In[256]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].nunique()


# [IBGE CONCLA CBO](https://concla.ibge.gov.br/classificacoes/por-tema/ocupacao/classificacao-brasileira-de-ocupacoes)
# 
# [MTECBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf)
# 
# [CBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf#) 

# In[257]:


bancoesusrais2019selecionadocnae.shape


# In[258]:


list(bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].unique())


# In[259]:


list(bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].replace("''",''))


# In[260]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].dtype


# In[261]:


list(bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str))


# In[262]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'] = bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str)


# In[263]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str).str[:-5]


# In[264]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str).str[:-5].unique()


# In[265]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].isna().sum()


# In[266]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group'] = bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str).str[:-5]


# In[267]:


bancoesusrais2019selecionadocnae.head(3)


# The data dictionary below comes from here [CBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf#)

# In[20]:


'''
CODIGO	TITULO
0	MEMBROS DAS FORÇAS ARMADAS, POLICIAIS E BOMBEIROS MILITARES   
    MEMBERS OF THE ARMED FORCES, POLICE AND MILITARY FIREMEN
    
1	MEMBROS SUPERIORES DO PODER PÚBLICO, DIRIGENTES DE ORGANIZAÇÕES DE INTERESSE PÚBLICO E DE EMPRESAS, GERENTES     
    SENIOR MEMBERS OF THE PUBLIC AUTHORITIES, DIRECTORS OF PUBLIC INTEREST ORGANIZATIONS AND COMPANIES, MANAGERS

2	PROFISSIONAIS DAS CIÊNCIAS E DAS ARTES     
    SCIENCE AND ARTS PROFESSIONALS

3	TÉCNICOS DE NIVEL MÉDIO               
    MEDIUM LEVEL TECHNICIANS

4	TRABALHADORES DE SERVIÇOS ADMINISTRATIVOS  
    ADMINISTRATIVE SERVICE WORKERS

5	TRABALHADORES DOS SERVIÇOS, VENDEDORES DO COMÉRCIO EM LOJAS E MERCADOS  
    SERVICE WORKERS, SELLERS IN STORES AND MARKETS

6	TRABALHADORES AGROPECUÁRIOS, FLORESTAIS E DA PESCA  
    AGRICULTURAL, FORESTRY AND FISHERY WORKERS

7	TRABALHADORES DA PRODUÇÃO DE BENS E SERVIÇOS INDUSTRIAIS  
    WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES

8	TRABALHADORES DA PRODUÇÃO DE BENS E SERVIÇOS INDUSTRIAIS  
     WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES

9	TRABALHADORES EM SERVIÇOS DE REPARAÇÃO E MANUTENÇÃO    
    WORKERS IN REPAIR AND MAINTENANCE SERVICES
'''


# In[ ]:


#7 and 8 have the same meaning in the original data dictionary from the website mentioned on the link


# In[268]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group'].dtype


# In[269]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group'].astype(str)


# In[270]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'] = bancoesusrais2019selecionadocnae['CBO 2002 Broad Group'].astype(str).replace('0','MEMBERS OF THE ARMED FORCES, POLICE AND MILITARY FIREMEN').replace('1','SENIOR MEMBERS OF THE PUBLIC AUTHORITIES, DIRECTORS OF PUBLIC INTEREST ORGANIZATIONS AND COMPANIES, MANAGERS').replace('2','SCIENCE AND ARTS PROFESSIONALS').replace('3','MEDIUM LEVEL TECHNICIANS').replace('4','ADMINISTRATIVE SERVICE WORKERS').replace('5','SERVICE WORKERS, SELLERS IN STORES AND MARKETS').replace('6','AGRICULTURAL, FORESTRY AND FISHERY WORKERS').replace('7','WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES').replace('8','WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES').replace('9','WORKERS IN REPAIR AND MAINTENANCE SERVICES')


# In[271]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'].unique()


# In[272]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'].dropna().unique()


# In[273]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'].replace('','NaN').unique()


# In[274]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'] = bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'].replace('','NaN')


# In[275]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'].unique()


# In[276]:


bancoesusrais2019selecionadocnae[bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'] != 'NaN']


# In[277]:


bancoesusrais2019selecionadocnae = bancoesusrais2019selecionadocnae[bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'] != 'NaN']


# In[278]:


bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'].unique()


# In[57]:


#bancoesusrais2019selecionadocnae[bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name']=='NaN']


# In[279]:


bancoesusrais2019selecionadocnae.head(3)


# In[280]:


bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str).str[:-4].unique()


# In[281]:


bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup'] = bancoesusrais2019selecionadocnae['CBO Ocupação 2002'].astype(str).str[:-4]


# In[282]:


bancoesusrais2019selecionadocnae.head(3)


# The data dictionary below comes from here [CBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf#)

# In[36]:


'''
CODIGO	TITULO
CODE -> TITLE

1	MEMBROS DAS FORÇAS ARMADAS         
    MEMBERS OF THE ARMED FORCES

2	POLICIAIS MILITARES          
    MILITARY POLICE

3	BOMBEIROS MILITARES   
    MILITARY FIREMEN

11	MEMBROS SUPERIORES E DIRIGENTES DO PODER PÚBLICO 
    SUPERIOR MEMBERS AND OFFICERS OF THE PUBLIC AUTHORITY


12	DIRIGENTES DE EMPRESAS E ORGANIZAÇÕES (EXCETO DE INTERESSE PÚBLICO)  
    DIRECTORS OF COMPANIES AND ORGANIZATIONS (EXCEPT PUBLIC INTEREST)


13	DIRETORES E GERENTES EM EMPRESA DE SERVIÇOS DE SAÚDE, DA EDUCAÇÃO, OU DE SERVIÇOS CULTURAIS, SOCIAIS OU PESSOAIS  
    DIRECTORS AND MANAGERS IN A HEALTH, EDUCATION, OR CULTURAL, SOCIAL OR PERSONAL SERVICES COMPANY

14	GERENTES    
    MANAGERS

20	PESQUISADORES E PROFISSIONAIS POLICIENTÍFICOS
    POLYSCIENTIFIC RESEARCHERS AND PROFESSIONALS

21	PROFISSIONAIS DAS CIÊNCIAS EXATAS, FÍSICAS E DA ENGENHARIA    
    PROFESSIONALS IN EXACT, PHYSICAL AND ENGINEERING SCIENCES

22	PROFISSIONAIS DAS CIÊNCIAS BIOLÓGICAS, DA SAÚDE E AFINS   
    PROFESSIONALS IN BIOLOGICAL, HEALTH AND RELATED SCIENCES

23	PROFISSIONAIS DO ENSINO      
    TEACHING PROFESSIONALS

24	PROFISSIONAIS DAS CIÊNCIAS JURÍDICAS      
    PROFESSIONALS OF LEGAL SCIENCES

25	PROFISSIONAIS DAS CIÊNCIAS SOCIAIS E HUMANAS  
    PROFESSIONALS OF SOCIAL AND HUMAN SCIENCES

26	COMUNICADORES, ARTISTAS E RELIGIOSOS  
    COMMUNICATORS, ARTISTS AND RELIGIOUS

27	PROFISSIONAIS EM GASTRONOMIA
    PROFESSIONALS IN GASTRONOMY

30	TÉCNICOS POLIVALENTES    
    POLYVALENT TECHNICIAN 

31	TÉCNICOS DE NÍVEL MÉDIO DAS CIÊNCIAS FÍSICAS, QUÍMICAS, ENGENHARIA E AFINS  
    MIDDLE LEVEL TECHNICIANS IN PHYSICAL, CHEMICAL, ENGINEERING AND RELATED SCIENCES

32	TÉCNICOS DE NÍVEL MÉDIO DAS CIÊNCIAS BIOLÓGICAS, BIOQUÍMICAS, DA SAÚDE E AFINS 
    MIDDLE LEVEL TECHNICIANS IN BIOLOGICAL, BIOCHEMICAL, HEALTH AND RELATED SCIENCES

33	PROFESSORES LEIGOS E DE NÍVEL MÉDIO    
    LAY TEACHERS AND MIDDLE LEVEL

34	TÉCNICOS DE NÍVEL MÉDIO EM SERVIÇOS DE TRANSPORTES   
    MEDIUM-LEVEL TECHNICIANS IN TRANSPORTATION SERVICES

35	TÉCNICOS DE NIVEL MÉDIO NAS CIÊNCIAS ADMINISTRATIVAS  
    MEDIUM-LEVEL TECHNICIANS IN ADMINISTRATIVE SCIENCES

37	TÉCNICOS EM NIVEL MÉDIO DOS SERVIÇOS CULTURAIS, DAS COMUNICAÇÕES E DOS DESPORTOS  
    MEDIUM LEVEL TECHNICIANS IN CULTURAL SERVICES, COMMUNICATIONS AND SPORTS

39	OUTROS TÉCNICOS DE NÍVEL MÉDIO
    OTHER MIDDLE LEVEL TECHNICIANS

41	ESCRITURÁRIOS    
    CLERK

42	TRABALHADORES DE ATENDIMENTO AO PÚBLICO   
    PUBLIC SERVICE WORKERS

51	TRABALHADORES DOS SERVIÇOS  
    SERVICE WORKERS

52	VENDEDORES E PRESTADORES DE SERVIÇOS DO COMÉRCIO  
    SELLERS AND SERVICE PROVIDERS

61	PRODUTORES NA EXPLORAÇÃO AGROPECUÁRIA 
    PRODUCERS IN CATTLE RANCHING EXPLORATION

62	TRABALHADORES NA EXPLORAÇÃO AGROPECUÁRIA   
    WORKERS IN CATTLE RANCHING EXPLORATION

63	PESCADORES E EXTRATIVISTAS FLORESTAIS    
    FISHERMEN AND FORESTRY EXTRACTORS

64	TRABALHADORES DA MECANIZAÇÃO AGROPECUÁRIA E FLORESTAL 
    CATTLE RANCHING AND FORESTRY MECHANIZATION WORKERS

71	TRABALHADORES DA INDÚSTRIA EXTRATIVA E DA CONSTRUÇÃO CIVIL 
    WORKERS IN THE EXTRACTIVE INDUSTRY AND CIVIL CONSTRUCTION

72	TRABALHADORES DA TRANSFORMAÇÃO DE METAIS E DE COMPÓSITOS  
    METAL AND COMPOSITE TRANSFORMATION WORKERS

73	TRABALHADORES DA FABRICAÇÃO E INSTALAÇÃO ELETROELETRÔNICA  
    WORKERS IN ELECTRO-ELECTRONIC MANUFACTURING AND INSTALLATION

74	MONTADORES DE APARELHOS E INSTRUMENTOS DE PRECISÃO E MUSICAIS   
    ASSEMBLERS OF PRECISION AND MUSICAL APPARATUS AND INSTRUMENTS

75	JOALHEIROS, VIDREIROS, CERAMISTAS E AFINS    
    JEWELERS, GLASSMEN, CERAMISTS AND RELATED

76	TRABALHADORES NAS INDÚSTRIAS TÊXTIL, DO CURTIMENTO, DO VESTÚARIO E DAS ARTES GRÁFICAS   
    WORKERS IN THE TEXTILE, TANNING, CLOTHING AND GRAPHIC ARTS INDUSTRIES

77	TRABALHADORES DAS INDÚSTRIAS DE MADEIRA E DO MOBILIÁRIO 
    WORKERS IN THE WOOD AND FURNITURE INDUSTRIES

78	TRABALHADORES DE FUNÇÕES TRANSVERSAIS 
    CROSS FUNCTIONAL WORKERS

79	TRABALHADORES DO ARTESANATO
    HANDICRAFT WORKERS

81	TRABALHADORES EM INDÚSTRIAS DE PROCESSOS CONTÍNUOS E OUTRAS INDÚSTRIAS      
    WORKERS IN CONTINUOUS PROCESSES AND OTHER INDUSTRIES

82	TRABALHADORES DE INSTALAÇÕES SIDERÚRGICAS E DE MATERIAIS DE CONSTRUÇÃO 
    WORKERS IN STEEL FACILITIES AND CONSTRUCTION MATERIALS

83	TRABALHADORES DE INSTALAÇÕES E MÁQUINAS DE FABRICAÇÃO DE CELULOSE E PAPEL  
    WORKERS IN PULP AND PAPER MANUFACTURING FACILITIES AND MACHINES

84	TRABALHADORES DA FABRICAÇÃO DE ALIMENTOS, BEBIDAS E FUMO     
    FOOD, BEVERAGE AND SMOKE MANUFACTURING WORKERS

86	OPERADORES DE PRODUÇÃO, CAPTAÇÃO, TRATAMENTO E DISTRIBUIÇÃO (ENERGIA, ÁGUA E UTILIDADES)
    OPERATORS OF PRODUCTION, CAPTURE, TREATMENT AND DISTRIBUTION (ENERGY, WATER AND UTILITIES)

87	OPERADORES DE OUTRAS INSTALAÇÕES INDUSTRIAIS       
    OPERATORS OF OTHER INDUSTRIAL FACILITIES

91	TRABALHADORES EM SERVIÇOS DE REPARAÇÃO E MANUTENÇÃO MECÂNICA   
    WORKERS IN MECHANICAL REPAIR AND MAINTENANCE SERVICES

95	POLIMANTENEDORES                                    
    MAINTAINER

99	OUTROS TRABALHADORES DA CONSERVAÇÃO, MANUTENÇÃO E REPARAÇÃO      
    OTHER CONSERVATION, MAINTENANCE AND REPAIR WORKERS

'''


# In[283]:


bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup'].unique()


# In[284]:


bancoesusrais2019selecionadocnae[bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup']=='00']


# In[39]:


#'00' should not be in the Main SubGroup.'0' is from the Broad Group Name that turns into 1,2 or 3 in the Main SubGroup, and not '00'
#so it needs to be dropped


# In[285]:


bancoesusrais2019selecionadocnae[bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup']!='00']


# In[286]:


bancoesusrais2019selecionadocnae = bancoesusrais2019selecionadocnae[bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup']!='00']


# In[287]:


bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup'].unique()


# In[288]:


bancoesusrais2019selecionadocnae.head(3)


# In[289]:


replacers = {'01':'MEMBERS OF THE ARMED FORCES','02':'MILITARY POLICE',
             '03':'MILITARY FIREMEN','11':'SUPERIOR MEMBERS AND OFFICERS OF THE PUBLIC AUTHORITY',
             '12':'DIRECTORS OF COMPANIES AND ORGANIZATIONS (EXCEPT PUBLIC INTEREST)', 
             '13':'DIRECTORS AND MANAGERS IN A HEALTH, EDUCATION, OR CULTURAL, SOCIAL OR PERSONAL SERVICES COMPANY',
             '14':'MANAGERS','20':'POLYSCIENTIFIC RESEARCHERS AND PROFESSIONALS',
             '21':'PROFESSIONALS IN EXACT, PHYSICAL AND ENGINEERING SCIENCES', 
             '22':'PROFESSIONALS IN BIOLOGICAL, HEALTH AND RELATED SCIENCES',
             '23':'TEACHING PROFESSIONALS', 
             '24':'PROFESSIONALS OF LEGAL SCIENCES','25':'PROFESSIONALS OF SOCIAL AND HUMAN SCIENCES',
             '26':'COMMUNICATORS, ARTISTS AND RELIGIOUS','27':'PROFESSIONALS IN GASTRONOMY',
             '30':'EDUCATION','POLYVALENT TECHNICIAN':'HUMAN HEALTH AND SOCIAL SERVICES',
             '31':'MIDDLE LEVEL TECHNICIANS IN PHYSICAL, CHEMICAL, ENGINEERING AND RELATED SCIENCES',
             '32':'MIDDLE LEVEL TECHNICIANS IN BIOLOGICAL, BIOCHEMICAL, HEALTH AND RELATED SCIENCES',
             '33':'LAY TEACHERS AND MIDDLE LEVEL',
             '34':'MEDIUM-LEVEL TECHNICIANS IN TRANSPORTATION SERVICES',
            '35':'MEDIUM-LEVEL TECHNICIANS IN ADMINISTRATIVE SCIENCES',
            '37':'MEDIUM LEVEL TECHNICIANS IN CULTURAL SERVICES, COMMUNICATIONS AND SPORTS',
            '39': 'OTHER MIDDLE LEVEL TECHNICIANS',
            '41':'CLERK','42':'PUBLIC SERVICE WORKERS','51':'SERVICE WORKERS',
            '52':'SELLERS AND SERVICE PROVIDERS', '61':'PRODUCERS IN CATTLE RANCHING EXPLORATION',
            '62':'WORKERS IN CATTLE RANCHING EXPLORATION','63':'FISHERMEN AND FORESTRY EXTRACTORS',
            '64':'CATTLE RANCHING AND FORESTRY MECHANIZATION WORKERS','71':'WORKERS IN THE EXTRACTIVE INDUSTRY AND CIVIL CONSTRUCTION',
            '72':'METAL AND COMPOSITE TRANSFORMATION WORKERS','73':'WORKERS IN ELECTRO-ELECTRONIC MANUFACTURING AND INSTALLATION',
            '74':'ASSEMBLERS OF PRECISION AND MUSICAL APPARATUS AND INSTRUMENTS','75':'JEWELERS, GLASSMEN, CERAMISTS AND RELATED',
            '76':'WORKERS IN THE TEXTILE, TANNING, CLOTHING AND GRAPHIC ARTS INDUSTRIES','77':'WORKERS IN THE WOOD AND FURNITURE INDUSTRIES',
            '78':'CROSS FUNCTIONAL WORKERS','79':'HANDICRAFT WORKERS','81':'WORKERS IN CONTINUOUS PROCESSES AND OTHER INDUSTRIES',
            '82':'WORKERS IN STEEL FACILITIES AND CONSTRUCTION MATERIALS','83':'WORKERS IN PULP AND PAPER MANUFACTURING FACILITIES AND MACHINES',
            '84':'FOOD, BEVERAGE AND SMOKE MANUFACTURING WORKERS','86':'OPERATORS OF PRODUCTION, CAPTURE, TREATMENT AND DISTRIBUTION (ENERGY, WATER AND UTILITIES)',
            '87':'OPERATORS OF OTHER INDUSTRIAL FACILITIES','91':'WORKERS IN MECHANICAL REPAIR AND MAINTENANCE SERVICES',
            '95':'MAINTAINER','99':'OTHER CONSERVATION, MAINTENANCE AND REPAIR WORKERS'} 
bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup Name'] = bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup'].replace(replacers)


# In[290]:


bancoesusrais2019selecionadocnae['CBO 2002 Main SubGroup Name'].unique()


# In[46]:


bancoesusrais2019selecionadocnae.head(3)


# In[291]:


bancoesusrais2019selecionadocnae.rename({'CBO Ocupação 2002':'CBO Occupation 2002'}, axis = 1, inplace = True)


# In[292]:


bancoesusrais2019selecionadocnae.head(3)


# In[293]:


bancoesusrais2019selecionadocnae.to_excel('bancoesusrais2019selecionadocnaecbo.xlsx', index=False)


# # Descriptive Info

# In[1]:


import pandas as pd


# In[2]:


bancoesusrais2019selecionadocnaecbo = pd.read_excel('bancoesusrais2019selecionadocnaecbo.xlsx')


# In[3]:


bancoesusrais2019selecionadocnaecbo.shape


# In[4]:


bancoesusrais2019selecionadocnaecbo.dropna()


# In[5]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[107]:


pd.set_option('display.max_columns',None)


# In[108]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[6]:


bancoesusrais2019selecionadocnaecbo.describe()


# In[7]:


list(bancoesusrais2019selecionadocnaecbo['idade'].sort_values(ascending=False))


# In[8]:


bancoesusrais2019selecionadocnaecbo[bancoesusrais2019selecionadocnaecbo['idade']<=112]


# In[9]:


bancoesusrais2019selecionadocnaecbo = bancoesusrais2019selecionadocnaecbo[bancoesusrais2019selecionadocnaecbo['idade']<=112]


# In[10]:


bancoesusrais2019selecionadocnaecbo.describe()


# In[11]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[12]:


import plotly.express as px 


# In[13]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='sex')
fig.update_layout(
    title={
        'text':'Sex',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[19]:


bancoesusrais2019selecionadocnaecbo['agecohort'].value_counts()


# In[20]:


bancoesusrais2019selecionadocnaecbo['agecohort'].value_counts(normalize=True)


# In[14]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='agecohort')
fig.update_layout(
    title={
        'text':'Agecohort',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[15]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='race')
fig.update_layout(
    title={
        'text':'Race',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[119]:


#bancoesusrais2019selecionadocnaecbo.dropna()


# In[120]:


'''
fig = px.bar(bancoesusrais2019selecionadocnaecbo.dropna(), x = 'race', y = 'agecohort', color = 'race')
fig.update_layout(
    title={
        'text': 'People Fully Vaccinated (per 100) by Country',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})
'''


# In[21]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='agecohort',color='agecohort',
                   title='Agecohort',
                   labels={'agecohort':'Agecohort', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Agecohort',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Agecohort')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[23]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['agecohort'].dropna(), x='agecohort',color='agecohort',
                   title='Agecohort',
                   labels={'agecohort':'Agecohort', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Agecohort',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Agecohort')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[24]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='race',color='race',
                   title='Race',
                   labels={'race':'Race', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Race',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Race')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[26]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['race'].dropna(), x='race',color='race',
                   title='Race',
                   labels={'race':'Race', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Race',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Race')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[27]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='Health Professionals')
fig.update_layout(
    title={
        'text':'Health Professionals',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[28]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='security professional')
fig.update_layout(
    title={
        'text':'Security Professionals',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[29]:


bancoesusrais2019selecionadocnaecbo.columns


# In[30]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['evolucaoCaso'].dropna(), x='evolucaoCaso',color='evolucaoCaso',
                   title='Municipalities',
                   labels={'evolucaoCaso':'Evolução Caso', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Evolução Caso',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Race')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[31]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='evolucaoCaso')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# #diferença entre curados e recuperados
# curados -> repórter -> não transmitem mais o vírus 
#         médica -> o paciente que passou por todos os sintomas e produziu anticorpos, está imune, está curado, não transmite mais a doença
# recuperados -> repórter -> normalmente não apresentam mais sintomas após 14 dias
#             médica -> ainda está hospitalizado ou em domicílio, diminuindo os sintomas, mas ainda pode transmitir 
# igm -anticorpo de fase aguda
# igg -anticorpo mais duradouro, fase crônica
# [Curado vs Recuperado](https://www.youtube.com/watch?v=HCNr8V1VPaI)
# 
# Curado (healed)-> não transmite mais o vírus, está imune com anticorpos
# 
# 
# Recuperado (recovered)-> ainda pode transmitir o vírus, apesar de já terem passados pelos sintomas, e não apresentá-los mais

# In[32]:


bancoesusrais2019selecionadocnaecbo.rename({'evolucaoCaso':'disease evolution'}, axis = 1, inplace =True)


# In[33]:


bancoesusrais2019selecionadocnaecbo['disease evolution'] = bancoesusrais2019selecionadocnaecbo['disease evolution'].replace(
{'Cura':'healed',
'Em tratamento domiciliar': 'in home treatment', 
'RECUPERADO':'recovered',
'INTERNADO LEITO DE ISOLAMENTO':'hospitalized isolation bed',
'ÓBITO':'death',
'ISOLAMENTO DOMICILIAR':'home isolation',
'INTERNADO UTI':'hospitalized ICU'})


# In[34]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].unique()


# In[35]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].dropna().unique()


# In[36]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].value_counts(normalize=True)


# In[37]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[38]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].isna().sum()


# In[39]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[40]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo.dropna(), names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[41]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo['disease evolution'].dropna(), names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[36]:


#if dropping nan from the whole data to do the graph, more observations will be lost
#to do the graph, there's only the need to dropna() on the column that you're doing the histogram graph
#although dropping na only from the specific column to do the graph instead of dropping na from all the data
#the graphs will have different counts and different frequency, so each column graph will be disproportional
#because some columns will have more na and other columns will have less na's


# In[42]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo['disease evolution'].dropna(), names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[43]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['disease evolution'].dropna(), x='disease evolution',color='disease evolution',
                   title='Disease Evolution',
                   labels={'disease evolution':'Disease Evolution', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Disease Evolution',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Race')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[44]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='disease evolution',color='disease evolution',
                   title='Disease Evolution',
                   labels={'disease evolution':'Disease Evolution', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Disease Evolution',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Disease Evolution')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[45]:


bancoesusrais2019selecionadocnaecbo.columns


# In[46]:


bancoesusrais2019selecionadocnaecbo.sintomas.unique()


# In[47]:


list(bancoesusrais2019selecionadocnaecbo.sintomas.unique())


# In[48]:


#tem que organizar de alguma forma os sintomas


# In[49]:


bancoesusrais2019selecionadocnaecbo.sintomas


# In[50]:


#organizar string, replace, alphabetical order etc


# In[51]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='Resultado Final')
fig.update_layout(
    title={
        'text':'Final Result',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[52]:


bancoesusrais2019selecionadocnaecbo['Resultado Final'].rename({'Null':'null'}, axis = 1, inplace = True)


# In[53]:


bancoesusrais2019selecionadocnaecbo['Resultado Final'].unique()


# In[54]:


bancoesusrais2019selecionadocnaecbo = bancoesusrais2019selecionadocnaecbo[bancoesusrais2019selecionadocnaecbo['Resultado Final']!='Inconclusivo ou indeterminado']


# In[55]:


bancoesusrais2019selecionadocnaecbo['Resultado Final'].unique()


# In[56]:


#bancoesusrais2019selecionadocnaecbo = bancoesusrais2019selecionadocnaecbo.dropna(subset=['Resultado Final'])

#dropping nan from Resultado Final altered disease evolution, it revomed almost all categories, it's better not to drop nan
#in Resultado final and save in it into the main data, otherwise, I dropped na when doing the graph, it's better


# In[57]:


bancoesusrais2019selecionadocnaecbo['Resultado Final'].unique()


# In[58]:


bancoesusrais2019selecionadocnaecbo['Resultado Final'].replace({'Positivo':'positive', 'Negativo':'negative'}, inplace = True)


# In[59]:


bancoesusrais2019selecionadocnaecbo['Resultado Final'].unique()


# In[60]:


bancoesusrais2019selecionadocnaecbo.rename({'Resultado Final':'final result'}, axis = 1, inplace = True)


# In[61]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='final result')
fig.update_layout(
    title={
        'text':'Final Result',
        'y':0.95,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[62]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo.dropna(), names='final result')
fig.update_layout(
    title={
        'text':'Final Result',
        'y':0.95,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[65]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo['final result'].dropna(), names='final result')
fig.update_layout(
    title={
        'text':'Final Result',
        'y':0.95,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[66]:


#there's still na in the column bancoesusrais2019selecionadocnaecbo['final result']
#na's were dropped .dropna() to make the pie chart above


# In[67]:


bancoesusrais2019selecionadocnaecbo.columns


# In[68]:


bancoesusrais2019selecionadocnaecbo.tipoTeste.unique()


# [Rapid Antibody Test](https://diagnostics.roche.com/global/en/article-listing/how-sars-cov-2-rapid-antibody-tests-work.html)
# 
# 
# [Rapid antigen test](https://www.nsw.gov.au/covid-19/health-and-wellbeing/rapid-antigen-testing)
# 
# 
# [RCT-PCR](https://www.cdc.gov/coronavirus/2019-ncov/lab/virus-requests.html)

# In[69]:


bancoesusrais2019selecionadocnaecbo.rename({'tipoTeste':'test type'}, axis = 1, inplace = True)


# In[70]:


bancoesusrais2019selecionadocnaecbo['test type'].replace({'TESTE RÁPIDO - ANTICORPO':'rapid antibody test', 'TESTE RÁPIDO - ANTÍGENO':'rapid antigen test'}, inplace = True)


# In[71]:


bancoesusrais2019selecionadocnaecbo['test type'].unique()


# In[72]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='test type',color='test type',
                   title='Test Type',
                   labels={'test type':'Test Type', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[73]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['test type'].dropna(), x='test type',color='test type',
                   title='Test Type',
                   labels={'test type':'Test Type', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[216]:


#the 2 Test type graphs above are a good example of the tredeoff of dropping nan in the specific column (less observations will be lost)
#and dropping na in the whole data
#the problem is that if doing all graphs with dropping na only in the specific column, each graph will have different count and frequency
#when compared to the other graphs
#making the distortion of all graphs having different counts, so what should be done, dropping na in the whole data to do the graph
#or dropping na only in the specific column to do the graph? (obs:not dropping na is not an option, because the graph 
#won't be done)


# In[74]:


bancoesusrais2019selecionadocnaecbo['test type'].unique()


# In[75]:


bancoesusrais2019selecionadocnaecbo['test type'].value_counts()


# In[76]:


bancoesusrais2019selecionadocnaecbo['test type'].dropna().value_counts()


# In[77]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='Escolaridade após 2005')
fig.update_layout(
    title={
        'text':'School Years',
        'y':0.95,
        'x':0.50,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[78]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='schooling')
fig.update_layout(
    title={
        'text':'School Years',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[80]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='schooling',color='schooling',
                   title='Schooling',
                   labels={'test type':'Schooling', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Schooling',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[82]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['schooling'].dropna(), x='schooling',color='schooling',
                   title='Schooling',
                   labels={'test type':'Schooling', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Schooling',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[83]:


bancoesusrais2019selecionadocnaecbo.columns


# In[92]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='meanminimumwagerange',color='meanminimumwagerange',
                   title='Minimum Wage',
                   labels={'meanminimumwagerange':'Minimum Wage', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Minimum Wage',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[87]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['meanminimumwagerange'].dropna(), x='meanminimumwagerange',color='meanminimumwagerange',
                   title='Minimum Wage',
                   labels={'meanminimumwagerange':'Minimum Wage', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Minimum Wage',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[91]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='IBGE Subsector',color='IBGE Subsector',
                   title='IBGE Subsector',
                   labels={'IBGE Subsector':'IBGE Subsector', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'IBGE Subsector',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[90]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['IBGE Subsector'].dropna(), x='IBGE Subsector',color='IBGE Subsector',
                   title='IBGE Subsector',
                   labels={'IBGE Subsector':'IBGE Subsector', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'IBGE Subsector',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[93]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[94]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='CNAE 2.0 Section Name',color='CNAE 2.0 Section Name',
                   title='CNAE 2.0 Section Name',
                   labels={'CNAE 2.0 Section Name':'CNAE 2.0 Section Name', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'CNAE 2.0 Section Name',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[95]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['CNAE 2.0 Section Name'].dropna(), x='CNAE 2.0 Section Name',color='CNAE 2.0 Section Name',
                   title='CNAE 2.0 Section Name',
                   labels={'CNAE 2.0 Section Name':'CNAE 2.0 Section Name', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'CNAE 2.0 Section Name',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[96]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='CNAE 2.0 Section Name')
fig.update_layout(
    title={
        'text':'CNAE 2.0 Section Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[97]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo.dropna(), x='CBO 2002 Broad Group Name',color='CBO 2002 Broad Group Name',
                   title='CBO 2002 Broad Group Name',
                   labels={'CBO 2002 Broad Group Name':'CBO 2002 Broad Group Name', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'CBO 2002 Broad Group Name',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[98]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['CBO 2002 Broad Group Name'].dropna(), x='CBO 2002 Broad Group Name',color='CBO 2002 Broad Group Name',
                   title='CBO 2002 Broad Group Name',
                   labels={'CBO 2002 Broad Group Name':'CBO 2002 Broad Group Name', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'CBO 2002 Broad Group Name',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[99]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='CBO 2002 Broad Group Name')
fig.update_layout(
    title={
        'text':'CBO 2002 Broad Group Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})#, showlegend=False)
fig.show()


# In[100]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='CBO 2002 Broad Group Name')
fig.update_layout(
    title={
        'text':'CBO 2002 Broad Group Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show()


# In[101]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='CBO 2002 Main SubGroup Name')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[102]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='CBO 2002 Main SubGroup Name')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show()


# In[103]:


bancoesusrais2019selecionadocnaecbo['CBO 2002 Main SubGroup Name'].value_counts(normalize=True)


# In[104]:


bancoesusrais2019selecionadocnaecbo['CBO 2002 Main SubGroup Name'].value_counts()


# In[105]:


bancoesusrais2019selecionadocnaecbo.sort_values(by='CBO 2002 Main SubGroup Name')


# In[106]:


bancoesusrais2019selecionadocnaecbo1 = bancoesusrais2019selecionadocnaecbo


# In[107]:


bancoesusrais2019selecionadocnaecbo['CBO 2002 Main SubGroup Name'].value_counts()<2000


# In[108]:


bancoesusrais2019selecionadocnaecbo['CBO 2002 Main SubGroup Name'][0:15]


# In[109]:


'''
bancoesusrais2019selecionadocnaecbo1.loc[bancoesusrais2019selecionadocnaecbo['CBO 2002 Main SubGroup Name']<2000, 'CBO 2002 Main SubGroup Name' ='OTHERS'
fig = px.pie(bancoesusrais2019selecionadocnaecbo1, names='CBO 2002 Main SubGroup Name', title='CBO 2002 Main SubGroup Name')
fig.update_layout(
    title={
        'text': 'CBO 2002 Main SubGroup Name',
        'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
'''


# In[110]:


bancoesusrais2019selecionadocnaecbo1['CBO 2002 Main SubGroup Name'].value_counts()<2000


# In[111]:


replacers = {'PROFESSIONALS IN EXACT, PHYSICAL AND ENGINEERING SCIENCES':'OTHERS',                                         
'WORKERS IN CATTLE RANCHING EXPLORATION':'OTHERS',                                                              
'METAL AND COMPOSITE TRANSFORMATION WORKERS':'OTHERS',                                                           
'WORKERS IN MECHANICAL REPAIR AND MAINTENANCE SERVICES':'OTHERS',                                                
'FOOD, BEVERAGE AND SMOKE MANUFACTURING WORKERS':'OTHERS',                                                       
'COMMUNICATORS, ARTISTS AND RELIGIOUS':'OTHERS',                                                                 
'DIRECTORS OF COMPANIES AND ORGANIZATIONS (EXCEPT PUBLIC INTEREST)':'OTHERS',                                   
'PROFESSIONALS OF LEGAL SCIENCES':'OTHERS',                                                                     
'MEDIUM LEVEL TECHNICIANS IN CULTURAL SERVICES, COMMUNICATIONS AND SPORTS':'OTHERS',                             
'WORKERS IN ELECTRO-ELECTRONIC MANUFACTURING AND INSTALLATION':'OTHERS',                                         
'DIRECTORS AND MANAGERS IN A HEALTH, EDUCATION, OR CULTURAL, SOCIAL OR PERSONAL SERVICES COMPANY':'OTHERS',      
'OPERATORS OF PRODUCTION, CAPTURE, TREATMENT AND DISTRIBUTION (ENERGY, WATER AND UTILITIES)':'OTHERS',           
'OTHER MIDDLE LEVEL TECHNICIANS':'OTHERS',                                                                       
'OTHER CONSERVATION, MAINTENANCE AND REPAIR WORKERS':'OTHERS',                                                   
'MEDIUM-LEVEL TECHNICIANS IN TRANSPORTATION SERVICES':'OTHERS',                                                  
'MAINTAINER':'OTHERS',                                                                                           
'WORKERS IN CONTINUOUS PROCESSES AND OTHER INDUSTRIES':'OTHERS',                                                 
'WORKERS IN THE WOOD AND FURNITURE INDUSTRIES':'OTHERS',                                                         
'WORKERS IN STEEL FACILITIES AND CONSTRUCTION MATERIALS':'OTHERS',                                               
'EDUCATION':'OTHERS',                                                                                            
'POLYSCIENTIFIC RESEARCHERS AND PROFESSIONALS':'OTHERS',                                                         
'CATTLE RANCHING AND FORESTRY MECHANIZATION WORKERS':'OTHERS',                                                  
'PROFESSIONALS IN GASTRONOMY':'OTHERS',                                                                          
'JEWELERS, GLASSMEN, CERAMISTS AND RELATED':'OTHERS',                                                            
'WORKERS IN PULP AND PAPER MANUFACTURING FACILITIES AND MACHINES':'OTHERS',                                     
'MILITARY POLICE':'OTHERS',                                                                                     
'ASSEMBLERS OF PRECISION AND MUSICAL APPARATUS AND INSTRUMENTS':'OTHERS',                                       
'FISHERMEN AND FORESTRY EXTRACTORS':'OTHERS',                                                                    
'MEMBERS OF THE ARMED FORCES':'OTHERS',                                                                          
'PRODUCERS IN CATTLE RANCHING EXPLORATION':'OTHERS',                                                             
'MILITARY FIREMEN':'OTHERS',                                                                                    
'HANDICRAFT WORKERS':'OTHERS'}      
bancoesusrais2019selecionadocnaecbo1['CBO 2002 Main SubGroup Name'] = bancoesusrais2019selecionadocnaecbo1['CBO 2002 Main SubGroup Name'].replace(replacers)  


# In[112]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo1, names='CBO 2002 Main SubGroup Name')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[113]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo1, names='CBO 2002 Main SubGroup Name')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.95,
        'x':0.50,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show()


# In[ ]:





# In[114]:


#less than 1% name others for example in CBO 2002 Main SubGroup Name
#organize graph broad group name
#organize the symptoms
#groupby minimum wage, bairros, municipalites, agecohort, etc
#to make tables, maps, etc
#make correlations, make models to run regressions, fixed effects, causality inference, spatial econometrics


# In[115]:


bancoesusrais2019selecionadocnaecbo['sintomas'].unique()


# In[116]:


list(bancoesusrais2019selecionadocnaecbo['sintomas'].unique())


# In[117]:


'''
coriza -> coryza
vomito -> vomiting
diarréia -> diarrhea
mialgia -> myalgia 
dor de cabeça -> headache 
dor de garganta -> sore throat
saturação < 95% -> saturation < 95%
dispneia -> dyspnea 
febre -> fever 
tosse -> cough

Distúrbios Olfativos -> olfactory dysfunction
Distúrbios Gustativos -> taste dysfunction
outros -> other
assintomático -> asymptomatic

what symptoms are mild and what symptoms are severe?
how will I organize the column


Epidemiological and clinical characteristics of the first 557 successive
patients with COVID-19 in Pernambuco state, Northeast Brazil

Jurandy Júnior Ferraz de Magalhães et al.

"We then compared the viral load of
severe cases (patients that were admitted to ICU and the ones that have
died) with mild cases at different days since symptoms onset (Fig. 4B).
There was no statistically significant difference in viral load at the time
of diagnosis of patients with mild or severe COVID-19 up to 14 days of
symptoms onset. However, patients with severe disease diagnosed after
14 days of symptoms onset had higher viral load than patients with mild
disease (p = 0.0218)"


https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html
https://www.webmd.com/lung/covid-19-symptoms#1

see the notes from meeting if michele said what is a severe and mild symptom
talk to emile to see how she separated these symptoms and how she handled the data

Dispneia é o termo médico usado para o que chamamos comumente de falta de ar ou de dificuldade de respirar. 
Quando um paciente tem dispneia, sua respiração torna-se irregular ou dificultosa, 
sendo que ele pode respirar de forma acelerada.

Mialgia é o termo médico para dor muscular. 

hospital ward -> enfermaria (caso precise para outra coluna)
'''


# In[118]:


bancoesusrais2019selecionadocnaecbo.columns


# In[119]:


#get back 'condicoes' column, it has less than 10% of the data not missing, so does cbo, but there's another column for cbo


# In[121]:


fig = px.histogram(bancoesusrais2019selecionadocnaecbo['disease evolution'].dropna(), x='disease evolution',color='disease evolution',
                   title='Disease evolution',
                   labels={'disease evolution':'Disease evolution', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Disease evolution',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[127]:


fig = px.pie(bancoesusrais2019selecionadocnaecbo, names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[128]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].unique()


# In[129]:


bancoesusrais2019selecionadocnaecbo.to_excel('bancoesusrais2019selecionadocnaecbo.xlsx', index = False)


# In[218]:


#this file was opened in the heading "Descriptive info", and it was overwritten above
#if wanting to go back, open it again in "Descriptive info"


# # Symptoms 

# In[ ]:


#organize the symptoms
#groupby minimum wage, bairros, municipalites, agecohort, etc
#to make tables, maps, etc
#make correlations, make models to run regressions, fixed effects, causality inference, spatial econometrics


# In[130]:


import pandas as pd


# In[131]:


bancoesusrais2019selecionadocnaecbo = pd.read_excel('bancoesusrais2019selecionadocnaecbo.xlsx')


# In[132]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[133]:


pd.set_option('display.max_columns', None)


# In[134]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[135]:


bancoesusrais2019selecionadocnaecbo.shape


# In[136]:


bancoesusrais2019selecionadocnaecbo['sintomas']


# In[137]:


bancoesusrais2019selecionadocnaecbo['sintomas'].unique()


# In[138]:


list(bancoesusrais2019selecionadocnaecbo['sintomas'].unique())


# In[139]:


'''
Coriza -> coryza
Vômito -> vomiting
Diarreia -> diarrhea
Mialgia -> myalgia 
Dor de Cabeça -> headache
Cefaleia - > headache
Dor de Garganta -> sore throat
Saturação O2 < 95% -> saturation < 95%
Dispneia -> dyspnea 
Febre -> fever 
Tosse -> cough

Coriza / Congestão Nasal -> Coryza / nasal congestion
Cansaço/fadiga -> tiredness/fatigue
Desconforto respiratório / aperto torácico -> respiratory distress / chest tightness


Alteração/perda de olfato e/ou paladar - change/loss of smell and/or taste

Distúrbios Olfativos -> olfactory dysfunction
Distúrbios Gustativos -> taste dysfunction
outros -> other
assintomático -> asymptomatic

there are other wordsattached to each other example VômitoFebre, DiarreiaTosse, and many others

what symptoms are mild and what symptoms are severe? there's no critiria
how will I organize the column? word count


Epidemiological and clinical characteristics of the first 557 successive
patients with COVID-19 in Pernambuco state, Northeast Brazil

Jurandy Júnior Ferraz de Magalhães et al.

"We then compared the viral load of
severe cases (patients that were admitted to ICU and the ones that have
died) with mild cases at different days since symptoms onset (Fig. 4B).
There was no statistically significant difference in viral load at the time
of diagnosis of patients with mild or severe COVID-19 up to 14 days of
symptoms onset. However, patients with severe disease diagnosed after
14 days of symptoms onset had higher viral load than patients with mild
disease (p = 0.0218)"


https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html
https://www.webmd.com/lung/covid-19-symptoms#1

see the notes from meeting if michele said what is a severe and mild symptom
talk to emile to see how she separated these symptoms and how she handled the data

Dispneia é o termo médico usado para o que chamamos comumente de falta de ar ou de dificuldade de respirar. 
Quando um paciente tem dispneia, sua respiração torna-se irregular ou dificultosa, 
sendo que ele pode respirar de forma acelerada.

Mialgia é o termo médico para dor muscular. 

Cefaleia é o termo médico utilizado para designar aquilo que conhecemos como “dor de cabeça"


hospital ward -> enfermaria (caso precise para outra coluna)
'''


# In[140]:


bancoesusrais2019selecionadocnaecbo['sintomas'].astype(str).unique().sum()


# In[141]:


bancoesusrais2019selecionadocnaecbo['sintomas'].dtype


# [Counting Word Frequencies](https://programminghistorian.org/en/lessons/counting-frequencies)
# 
# [Count words on dataframe column](https://stackoverflow.com/questions/65351256/counting-repeated-word-in-dataframe-pandas)

# In[142]:


bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts()


# The explode() function is used to transform each element of a list-like to a row, replicating the index values. Exploded lists to rows of the subset columns; index will be duplicated for these rows. Raises: ValueError - if columns of the frame are not unique. Download the above Notebook from here.[W3 resource](https://www.w3resource.com/pandas/dataframe/dataframe-explode.php#:~:text=The%20explode()%20function%20is,row%2C%20replicating%20the%20index%20values.&text=Exploded%20lists%20to%20rows%20of,the%20frame%20are%20not%20unique.&text=Download%20the%20above%20Notebook%20from%20here.)

# In[143]:


symps = bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts()
symps.plot.bar()


# In[ ]:





# In[ ]:





# In[144]:


bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts()>20000


# In[ ]:





# In[145]:


bancoesusrais2019selecionadocnaecbo['sintomas'].str.get_dummies(', ').sum()


# In[ ]:





# In[146]:


replacers = {'Tosse':'cough','Outros':'others','Dor de garganta':'sore throat','Febre':'fever','Dor de Cabeça':'headache', 
             'Assintomático':'asymptomatic','Coriza':'coryza','Distúrbios Gustativos':'taste dysfunction',
             'Distúrbios Olfativos':'olfactory dysfunction','Dispneia':'dyspneia',
             'Saturação O2 < 95':'others',
             'Desconforto respiratório / aperto torácico':'others',                                                              
             'Cefaleia':'others',                                                           
             'Mialgia':'others',                                                
             'Cansaço/fadiga':'others',                                                       
             'Diarreia':'others',                                                                 
             'Alteração/perda de olfato e/ou paladar ':'others',                                   
             'Coriza / Congestão Nasal ':'others',                                                                     
             'Vômito':'others',                             
             'Náusea':'others',                                         
             'Tiragem Intercostal':'others',      
             'Distúrbios Gustativos,Distúrbios Olfativos':'others',           
             'Cianose':'others',                                                                       
             'Febre,Tosse,Distúrbios Gustativos,Distúrbios Olfativos ':'others',                                                   
             'Febre,Tosse  ':'others',                                                  
             'Erupções cutâneas':'others',                                                                                           
             'Edema mãos/pés':'others',                                                 
             'Febre,Dor de Garganta':'others',                                                         
             'Tosse,Distúrbios Gustativos,Distúrbios Olfativos':'OTHERS',  
             'Batimento Asa de Nariz':'others',                                           
             'Dor de Cabeça,Distúrbios Gustativos,Distúrbios Olfativos':'others',
             'Tosse,Distúrbios Olfativos':'others',
             'Tosse,Dispneia,Distúrbios Gustativos,Distúrbios Olfativos':'others',
             'Febre,Tosse,Dispneia':'others',
             'Febre,Distúrbios Olfativos':'others',
             'Dispneia,Distúrbios Gustativos,Distúrbios Olfativos':'others',
             'Tosse,Dor de Garganta,Dor de Cabeça,Coriza':'others',
             'Febre,Tosse,Dor de Garganta':'others',
             'Febre,Dor de Garganta,Dor de Cabeça':'others'}                    
bancoesusrais2019selecionadocnaecbo['symptoms'] = bancoesusrais2019selecionadocnaecbo['sintomas'].astype(str).replace(replacers) 


# In[147]:


bancoesusrais2019selecionadocnaecbo['symptoms'].unique()


# In[148]:


list(bancoesusrais2019selecionadocnaecbo['symptoms'].unique())


# In[149]:


bancoesusrais2019selecionadocnaecbo['symptoms'].str.split(', ').explode().value_counts()


# In[150]:


bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts()


# In[151]:


bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts(normalize=True)


# In[152]:


bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts(normalize=True)*100


# In[153]:


list(bancoesusrais2019selecionadocnaecbo['sintomas'].str.split(', ').explode().value_counts())


# In[154]:


870+644+351+314+313+211+207+188+79+59+12+12+9+8+8+6+4+4+4+3+2+2+2+1+1+1+1+1+1+1


# In[155]:


#others 3319, outros 80656
#other = 3319+80656


# In[156]:


3319+80656


# In[157]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[158]:


#this string replace does not work, because many words are inside one string, it has to be one word inside the string


# In[159]:


bancoesusrais2019selecionadocnaecbo['symptoms'].str.split(', ').explode().value_counts().sum()


# In[160]:


'''
Tosse                                                        88438
Outros                                                       80656 (+3319 others=83975)
Dor de Garganta                                              70184
Febre                                                        68908
Dor de Cabeça                                                67378
Assintomático                                                44624
Coriza                                                       42644
Distúrbios Gustativos                                        24817
Distúrbios Olfativos                                         24467
Dispneia                                                     24263
'''


# Different ways to create a dataframe [geeksforgeeks](https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/)

# In[47]:


data = [['cough', 88438], ['others', 83975], ['sore throat', 70184], ['fever',68908], ['headache', 67378], ['asymptomatic',44624], ['coryza',42644],['taste dysfunction',24817],['olfactory dysfunction',24467],['dyspnea',24263]]
df = pd.DataFrame(data, columns = ['symptoms', 'count'])
df


# In[162]:


import plotly.express as px


# In[48]:


fig = px.bar(df, x = 'symptoms', y = 'count', color = 'symptoms')
fig.update_layout(
    title={
        'text': 'Symptoms',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})


# In[49]:


fig = px.bar(df, x = 'symptoms', y = 'count', color = 'symptoms')
fig.update_layout(
    title={
        'text': 'Symptoms',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
#fig.show()


# In[51]:


fig = px.pie(df, names = 'symptoms')
fig.update_layout(
    title={
        'text': 'Symptoms',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})


# In[168]:


#no need to rerun symptoms later, only to do the graph, which the dataframe is near the end of the heading 'Symptoms'
#because the symptoms column was not altered in the original data


# In[165]:


bancoesusrais2019selecionadocnaecbo['symptoms']


# In[166]:


del bancoesusrais2019selecionadocnaecbo['symptoms']


# In[167]:


bancoesusrais2019selecionadocnaecbo.head(3)


# [Group dataframe and get sum AND count](https://stackoverflow.com/questions/38174155/group-dataframe-and-get-sum-and-count)

# # Comorbidities

# In[1]:


import pandas as pd


# In[2]:


bancoesusrais2019selecionadocnaecbo = pd.read_excel('bancoesusrais2019selecionadocnaecbo.xlsx')


# In[3]:


bancoesusrais2019selecionadocnaecbo.shape


# In[4]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].unique()


# In[5]:


bancoesusrais2019selecionadocnaecbo[bancoesusrais2019selecionadocnaecbo['disease evolution']=='death']


# In[6]:


bancoesusrais2019selecionadocnaecbo['disease evolution']


# In[7]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].value_counts(normalize=True)


# In[8]:


bancoesusrais2019selecionadocnaecbo['disease evolution'].value_counts()


# In[87]:


#go back to the beginning of the code the get the deleted comorbity column


# In[9]:


bancoesusrais2019selecionadocnaecbo['condicoes']


# In[10]:


bancoesusrais2019selecionadocnaecbo['condicoes'].isna().sum()


# In[11]:


bancoesusrais2019selecionadocnaecbo['condicoes'].notnull().sum()


# In[12]:


bancoesusrais2019selecionadocnaecbo['condicoes'].notna().sum()


# In[13]:


bancoesusrais2019selecionadocnaecbo.rename({'condicoes':'comorbidity'}, axis=1,inplace=True)


# In[14]:


bancoesusrais2019selecionadocnaecbo['comorbidity']


# In[15]:


bancoesusrais2019selecionadocnaecbo['comorbidity'].unique()


# In[20]:


bancoesusrais2019selecionadocnaecbo['comorbidity'].str.split(', ').explode().value_counts()


# In[19]:


bancoesusrais2019selecionadocnaecbo['comorbidity'].str.split(', ').explode().value_counts().plot.bar()


# In[21]:


#como = bancoesusrais2019selecionadocnaecbo['comorbidity'].str.split(', ').explode().value_counts()
#como.plotbar()


# In[17]:


bancoesusrais2019selecionadocnaecbo['comorbidity'].str.split(', ').explode().value_counts(normalize=True)*100


# In[188]:


#make commordity graph
#make graph with comorbities and death, see how they're related


# In[ ]:


'''
Doenças cardíacas crônicas                                                9235
Diabetes                                                                  5904
Doenças respiratórias crônicas descompensadas                             3029
Obesidade                                                                  934
Gestante                                                                   899
Imunossupressão                                                            896
Doenças Cardíacas ou Vasculares                                            421
Doenças renais crônicas em estágio avançado (graus 3                       323
4 ou 5)                                                                    323
Portador de doenças cromossômicas ou estado de fragilidade imunológica     297
Sobrepeso/Obesidade                                                        129
Doenças Respiratórias Crônicas                                              67
Puérpera (até 45 dias do parto)                                             55
Doenças Renais Cronicas                                                     30
Doença Hepática Crônica                                                     12
Gestante de alto risco                                                       3
Portador de Doenças Cromossômicas                                            2
'''


# In[52]:


data = [['chronic heart disease', 9235], ['diabetes',5904], ['decompensated chronic respiratory diseases',3029],
        ['obesity',934],['pregnant', 899],['immunosuppression',896],['heart or vascular diseases',421], 
        ['chronic kidney disease at an advanced stage (grades 3, 4 or 5)',323],
        ['carrier of chromosomal diseases or state of immunological frailty',297],
        ['overweight/obesity',129],['others',169]]
df = pd.DataFrame(data, columns = ['comorbidity','count'])
df


# In[24]:


67+55+30+12+3+2


# In[28]:


import plotly.express as px


# In[53]:


fig = px.bar(df, x = 'comorbidity', y = 'count', color = 'comorbidity')
fig.update_layout(
    title={
        'text': 'Comorbidity',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})


# In[58]:


fig = px.bar(df, x = 'comorbidity', y = 'count', color = 'comorbidity')
fig.update_layout(
    title={
        'text': 'Comorbidity',
        'y':0.95,
        'x':0.35,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')#, showlegend=False)
fig.update_yaxes(title='count',range=[0, 9000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
#fig.show()


# In[55]:


fig = px.pie(df, names='comorbidity')
fig.update_layout(
    title={
        'text': 'Comorbidity',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})


# In[44]:


#what? why are the % all the same?


# In[56]:


fig = px.pie(df, names='count')
fig.update_layout(
    title={
        'text':'Comorbidity',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[59]:


#comorbidity and death


# In[60]:


bancoesusrais2019selecionadocnaecbo.columns


# In[61]:


bancoesusrais2019selecionadocnaecbo['comorbidity']


# In[63]:


bancoesusrais2019selecionadocnaecbo[bancoesusrais2019selecionadocnaecbo['disease evolution']=='death']


# In[74]:


dfcomorbiditydeath = bancoesusrais2019selecionadocnaecbo[bancoesusrais2019selecionadocnaecbo['disease evolution']=='death']


# In[76]:


dfcomorbiditydeath.shape


# In[83]:


dfcomorbiditydeath['comorbidity'].dropna().shape


# In[86]:


dfcomorbiditydeath['comorbidity'].dropna()


# In[87]:


dfcomorbiditydeath['comorbidity'] = dfcomorbiditydeath['comorbidity'].dropna()


# In[88]:


dfcomorbiditydeath.shape


# In[89]:


dfcomorbiditydeath['comorbidity'].shape


# In[90]:


dfcomorbiditydeath.dropna(subset=['comorbidity'])


# In[91]:


dfcomorbiditydeath = dfcomorbiditydeath.dropna(subset=['comorbidity'])


# In[92]:


dfcomorbiditydeath.shape


# In[ ]:





# In[94]:


fig = px.bar(dfcomorbiditydeath, x = 'comorbidity', y = 'disease evolution', color = 'disease evolution')
fig.update_layout(
    title={
        'text': 'Death and Comorbidity',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})


# In[ ]:


bancoesusrais2019selecionadocnaecbo['comorbidity'].str.split(', ').explode().value_counts(normalize=True)*100


# In[97]:


dfcomorbiditydeath['comorbidity'].str.split(', ').explode().value_counts()


# In[99]:


dfcomorbiditydeath['comorbidity'].isnull().sum()


# In[ ]:


#219 died, some had nan for comorbidity, dropping nan it drops to 137 rows, all have comorbidity


# In[2]:


import pandas as pd


# In[3]:


import plotly.express as px


# In[4]:


data = [['heart or vascular diseases',94],['diabetes',71],['overweight/obesity',35], ['chronic kidney disease',14],
        ['chronic respiratory diseases', 10],['chronic liver disease',7],['immunosuppression',4]]
df = pd.DataFrame(data, columns = ['comorbidity','death count'])
df


# In[6]:


fig = px.bar(df, x='comorbidity', y='death count', color = 'comorbidity')
fig.update_layout(
    title={
        'text': 'Death Frequency by Comorbidity',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'},paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')#, showlegend=False)
#fig.update_yaxes(title='count',range=[0, 9000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
#fig.show())


# In[ ]:





# In[ ]:





# # Municipalities

# In[2]:


import pandas as pd


# In[3]:


bancoesusrais2019selecionadocnaecbo = pd.read_excel('bancoesusrais2019selecionadocnaecbo.xlsx')


# In[4]:


bancoesusrais2019selecionadocnaecbo['municipio'].value_counts(normalize=True)


# In[5]:


bancoesusrais2019selecionadocnaecbo['municipio'].value_counts()


# In[6]:


bancoesusrais2019selecionadocnaecbo['municipio'].unique()


# In[15]:


bancoesusrais2019selecionadocnaecbo['municipio'].str.title().unique()


# In[21]:


#pip install unidecode


# In[22]:


#import unidecode


# In[ ]:


bancoesusrais2019selecionadocnaecbo['municipio'].str.title()


# In[23]:


bancoesusrais2019selecionadocnaecbo['municipio'] = bancoesusrais2019selecionadocnaecbo['municipio'].str.title()


# In[29]:


bancoesusrais2019selecionadocnaecbo['municipio'].dtype


# In[28]:


bancoesusrais2019selecionadocnaecbo['municipio'].astype(str).replace('á','a').replace('ã','a').replace('â','a').replace('ê','e').replace('é','e').replace('í','i').replace('ô','o').replace('ó','o').replace('ú','u').replace('ç','c')


# In[32]:


bancoesusrais2019selecionadocnaecbo['municipio'].astype(str)


# In[34]:


bancoesusrais2019selecionadocnaecbo['municipio'] = bancoesusrais2019selecionadocnaecbo['municipio'].astype(str)


# In[35]:


bancoesusrais2019selecionadocnaecbo['municipio'] = bancoesusrais2019selecionadocnaecbo['municipio'].astype(str).replace('á','a').replace('ã','a').replace('â','a').replace('ê','e').replace('é','e').replace('í','i').replace('ô','o').replace('ó','o').replace('ú','u').replace('ç','c')


# In[36]:


bancoesusrais2019selecionadocnaecbo['municipio'].unique()


# In[37]:


#bancoesusrais2019selecionadocnaecbo['municipio'] = bancoesusrais2019selecionadocnaecbo['municipio'].replace(
#{'á':'healed',
#'Em tratamento domiciliar': 'in home treatment', 
#'RECUPERADO':'recovered',
#'INTERNADO LEITO DE ISOLAMENTO':'hospitalized isolation bed',
#'ÓBITO':'death',
#'ISOLAMENTO DOMICILIAR':'home isolation',
#'INTERNADO UTI':'hospitalized ICU'})


# In[38]:


#bancoesusrais2019selecionadocnae['CBO 2002 Broad Group Name'] = bancoesusrais2019selecionadocnae['CBO 2002 Broad Group'].astype(str).replace('0','MEMBERS OF THE ARMED FORCES, POLICE AND MILITARY FIREMEN').replace('1','SENIOR MEMBERS OF THE PUBLIC AUTHORITIES, DIRECTORS OF PUBLIC INTEREST ORGANIZATIONS AND COMPANIES, MANAGERS').replace('2','SCIENCE AND ARTS PROFESSIONALS').replace('3','MEDIUM LEVEL TECHNICIANS').replace('4','ADMINISTRATIVE SERVICE WORKERS').replace('5','SERVICE WORKERS, SELLERS IN STORES AND MARKETS').replace('6','AGRICULTURAL, FORESTRY AND FISHERY WORKERS').replace('7','WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES').replace('8','WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES').replace('9','WORKERS IN REPAIR AND MAINTENANCE SERVICES')


# In[40]:


bancoesusrais2019selecionadocnaecbo['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').unique()


# In[41]:


bancoesusrais2019selecionadocnaecbo['municipio'] = bancoesusrais2019selecionadocnaecbo['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[42]:


bancoesusrais2019selecionadocnaecbo['municipio']


# In[43]:


bancoesusrais2019selecionadocnaecbo['municipio'].value_counts()


# In[44]:


import plotly.express as px


# In[46]:


px.pie(bancoesusrais2019selecionadocnaecbo, names='municipio')


# In[49]:


pd.set_option('display.max_rows', None)


# In[50]:


bancoesusrais2019selecionadocnaecbo['municipio'].value_counts()


# In[51]:


#map


# In[52]:


import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.basemap import Basemap


# In[53]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cruzamento/PE_Municipios_2020/PE_Municipios_2020.shp')


# In[54]:


gdf.head(3)


# In[77]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.title()


# In[56]:


gdf['NM_MUN']=gdf['NM_MUN'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[58]:


gdf.plot()


# In[78]:


gdf['NM_MUN']


# In[79]:


bancoesusrais2019selecionadocnaecbogdfmerge = gdf.merge(bancoesusrais2019selecionadocnaecbo, left_on='NM_MUN', right_on='municipio', how='inner', indicator=True)


# In[80]:


bancoesusrais2019selecionadocnaecbogdfmerge.shape


# In[81]:


bancoesusrais2019selecionadocnaecbogdfmerge.head(3)


# In[82]:


bancoesusrais2019selecionadocnaecbogdfmerge['municipio'].head(3)


# In[83]:


bancoesusrais2019selecionadocnaecbogdfmerge['final result'].unique()


# In[85]:


bancoesusrais2019selecionadocnaecbogdfmerge['final result'].isnull().sum()


# In[86]:


bancoesusrais2019selecionadocnaecbogdfmerge['final result'].isna().sum()


# In[87]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'] = bancoesusrais2019selecionadocnaecbogdfmerge['final result']


# In[90]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'] = bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].str.replace('negative','0').replace('positive','1')


# In[92]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].unique()


# In[93]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].value_counts()


# In[94]:


bancoesusrais2019selecionadocnaecbogdfmerge.head(3)


# In[98]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].replace('Null','0').unique()


# In[100]:


#substituting null for 0s to get only the positive cases with the sum of 1's
#remember that null is different than 0, 0 means that a person did the covid test and it came negative
#null means there's missing information and it came null from the database system from SESPE, nan means the cell is empty


# In[101]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'] = bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].replace('Null','0')


# In[102]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].unique()


# In[103]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].isna().sum()


# In[106]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].dropna()


# In[109]:


bancoesusrais2019selecionadocnaecbogdfmerge.dropna(subset=['finalresultdummy'], inplace = True)


# In[111]:


bancoesusrais2019selecionadocnaecbogdfmerge.shape


# In[113]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].astype(int)


# In[114]:


bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'] = bancoesusrais2019selecionadocnaecbogdfmerge['finalresultdummy'].astype(int)


# In[122]:


bancoesusrais2019selecionadocnaecbogdfmerge.groupby(by='NM_MUN').sum()


# In[123]:


bancoesusrais2019selecionadocnaecbogdfmergesum = bancoesusrais2019selecionadocnaecbogdfmerge.groupby(by='NM_MUN').sum()


# In[125]:


bancoesusrais2019selecionadocnaecbogdfmergesum


# In[126]:


pd.set_option('display.max_rows', None)


# In[127]:


bancoesusrais2019selecionadocnaecbogdfmergesum


# In[128]:


bancoesusrais2019selecionadocnaecbogdfmergesum.reset_index(level=0, inplace = True)


# In[129]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcases = bancoesusrais2019selecionadocnaecbogdfmergesum.loc[:,['NM_MUN','Health Professionals','security professional','sex','finalresultdummy']]


# In[130]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcases.shape


# In[131]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcases.head(3)


# In[132]:


gdf


# In[133]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge = gdf.merge(bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcases, on='NM_MUN', how='inner', indicator=True)


# In[134]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.shape


# In[135]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.head(4)


# In[136]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[138]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.drop(['_merge'], axis = 1, inplace = True)


# In[139]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.head(3)


# In[140]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.plot()


# In[142]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.plot(cmap='gist_gray', column='NM_MUN', figsize=(10,10),legend=True);


# In[143]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.to_file('bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.shp')


# In[144]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge = gpd.read_file('bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.shp')


# In[145]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.head(3)


# In[153]:


pd.set_option('display.max_rows', None)


# In[154]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge


# In[155]:


#dropping Fernando de Noronha because it's messing up the map, 
#Fernando de Noronha has 25 covid positive cases by the way


# In[161]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.drop(bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.loc[bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge['NM_MUN']=='Fernando De Noronha'].index, inplace = True)


# In[162]:


bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.shape


# In[201]:


f, ax = plt.subplots(1, figsize=(15, 15))
bancoesusrais2019selecionadocnaecbogdfmergecovidtotalcasesmerge.plot(ax=ax, column='finalresul', legend=True, scheme = 'Quantiles', legend_kwds={'fmt':'{:.0f}'}, 
         cmap='binary', edgecolor='k')#, linewidth = 0.1)
ax.set_axis_off()
ax.set_title('Covid Cases PE March 2020 until May 8th 2021 N=56517', fontsize = 15)
plt.axis('equal')
plt.subplots_adjust(left=0.105, bottom=0.68, right=0.92, top=0.9, wspace=0.02, hspace=0.01) #default (left=0.125 [the left side of the subplots of the figure], bottom=0.1 [the bottom of the subplots of the figure], right=0.9 [the right side of the subplots of the figure], top=0.9[the top of the subplots of the figure], wspace=0.2[the amount of width reserved for blank space between subplots], hspace=0.2[the amount of height reserved for white space between subplots])
#plt.xlim(-41.5, -34.5)
#plt.ylim(-10,-4.5)
plt.show()


# In[202]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[204]:


bancoesusrais2019selecionadocnaecbo.shape


# In[205]:


bancoesusrais2019selecionadocnaecbo['municipio'].unique()


# In[207]:


bancoesusrais2019selecionadocnaecbo.to_excel('bancoesusrais2019selecionadocnaecbo.xlsx',index=False)


# In[ ]:





# # Bairros

# In[1]:


import pandas as pd


# In[2]:


bancoesusrais2019selecionadocnaecbo = pd.read_excel('bancoesusrais2019selecionadocnaecbo.xlsx')


# In[3]:


bancoesusrais2019selecionadocnaecbo.shape


# In[4]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[7]:


list(bancoesusrais2019selecionadocnaecbo['bairro'].unique())


# In[8]:


import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.basemap import Basemap


# In[11]:


gdf = gpd.read_file('CemRmRec.shp')


# In[12]:


gdf.shape


# In[13]:


gdf.head(3)


# In[15]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RM_Recife/RM_Recife/Shapes_RM Recife/RM_Recife_UDH.shp')


# In[16]:


gdf.shape


# In[17]:


gdf.head(3)


# In[19]:


gdf.plot();


# In[20]:


pd.set_option('display.max_rows',None)


# In[21]:


gdf


# In[22]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RM_Recife/RM_Recife/Shapes_RM Recife/Municípios_RM_Recife.shp')


# In[23]:


gdf.shape


# In[24]:


gdf.head(3)


# In[26]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RM_Recife/RM_Recife/Shapes_RM Recife/Limite_RM_Recife.shp')


# In[28]:


gdf.shape


# In[29]:


gdf.head(3)


# ## Os bairros de Recife

# In[30]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RM_Recife/RM_Recife/Shapes_RM Recife/RM_Recife_UDH.shp')


# In[31]:


gdf.shape


# In[32]:


gdf.head(3)


# In[35]:


gdf = gdf[gdf['NM_MUNICIP']=='RECIFE']


# In[36]:


gdf.shape


# In[37]:


gdf


# In[39]:


gdf.plot();


# # O geojson será usado

# In[40]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[41]:


bairrosgeojson


# In[42]:


bairrosgeojson.plot();


# In[43]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[47]:


bancoesusrais2019selecionadocnaecbo['bairro'] = bancoesusrais2019selecionadocnaecbo['bairro'].str.title()


# In[48]:


bancoesusrais2019selecionadocnaecbo['bairro']=bancoesusrais2019selecionadocnaecbo['bairro'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[45]:


bairrosgeojson['bairro_nome_ca'] = bairrosgeojson['bairro_nome_ca'].str.title()


# In[46]:


bairrosgeojson


# In[50]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge = bairrosgeojson.merge(bancoesusrais2019selecionadocnaecbo, left_on='bairro_nome_ca', right_on='bairro',how='inner',indicator=True)


# In[51]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge.shape


# In[52]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge.head(3)


# In[53]:


pd.set_option('display.max_columns',None)


# In[54]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge.head(3)


# In[55]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy']=bancoesusrais2019selecionadocnaecbobairrorecifemerge['final result']


# In[56]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy'].unique()


# In[58]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy'] = bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy'].str.replace('negative','0').replace('positive','1').replace('Null','0')


# In[60]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy'].value_counts()


# In[66]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy'] = bancoesusrais2019selecionadocnaecbobairrorecifemerge['finalresultdummy'].astype(int)


# In[67]:


bancoesusrais2019selecionadocnaecbobairrorecifemerge.groupby(by='bairro').sum()


# In[68]:


bairroscovidsum = bancoesusrais2019selecionadocnaecbobairrorecifemerge.groupby(by='bairro').sum()


# In[70]:


bairroscovidsum.reset_index(level=0,inplace=True)


# In[71]:


bairroscovidsum.loc[:,['bairro','Health Professionals','security professional','sex','finalresultdummy']]


# In[72]:


bairroscovidsumsomecols = bairroscovidsum.loc[:,['bairro','Health Professionals','security professional','sex','finalresultdummy']]


# In[73]:


bairroscovidsumsomecols


# In[74]:


bairrosgeojson


# In[75]:


bairromergesumcovidshape=bairrosgeojson.merge(bairroscovidsumsomecols, left_on='bairro_nome_ca',right_on='bairro',how='inner',indicator=True)


# In[76]:


bairromergesumcovidshape.shape


# In[77]:


bairromergesumcovidshape.head(3)


# In[78]:


bairromergesumcovidshape.plot();


# In[79]:


bairromergesumcovidshape.plot(cmap='gist_gray', column='bairro', figsize=(10,10),legend=True);


# In[82]:


bairromergesumcovidshape['finalresultdummy'].sum()


# In[102]:


f, ax = plt.subplots(1, figsize=(20, 20))
bairromergesumcovidshape.plot(ax=ax, column='finalresultdummy', legend=True, scheme = 'Quantiles', legend_kwds={'fmt':'{:.0f}'}, 
         cmap='binary', edgecolor='k')#, linewidth = 0.1)
ax.set_axis_off()
ax.set_title('Covid Cases Recife March 2020 until May 8th 2021 N=18270', fontsize = 15)
plt.axis('equal')
plt.subplots_adjust(left=0.100, bottom=0.66, right=0.6, top=0.9, wspace=0.02, hspace=0.01) #default (left=0.125 [the left side of the subplots of the figure], bottom=0.1 [the bottom of the subplots of the figure], right=0.9 [the right side of the subplots of the figure], top=0.9[the top of the subplots of the figure], wspace=0.2[the amount of width reserved for blank space between subplots], hspace=0.2[the amount of height reserved for white space between subplots])
#plt.xlim(-41.5, -34.5)
#plt.ylim(-10,-4.5)
plt.show()


# In[91]:


bairromergesumcovidshape.drop(['_merge'],axis=1,inplace=True)


# In[92]:


bairromergesumcovidshape.to_file('bairromergesumcovidshape.shp')


# ## CEP 

# In[1]:


import pandas as pd


# In[ ]:


bancoesus27022021latlong = pd.read_excel('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cepbancoesus27.02.2021/bancoesus27022021latlong.xlsx')


# In[3]:


bancoesus27022021latlong.shape


# In[ ]:




