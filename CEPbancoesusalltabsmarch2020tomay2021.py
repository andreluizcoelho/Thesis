#!/usr/bin/env python
# coding: utf-8

# ## From CEP's getting latitude and longitude 
# for the merged data bancoesusalltabsmarch2020tomay2021 

# # bancoesusalltabsrais2019nodupsCEPS[0:425]

# In[1]:


import pandas as pd


# In[2]:


bancoesusalltabsrais2019nodupsCEPS = pd.read_csv('bancoesusalltabsrais2019nodupsCEPS.csv')


# In[3]:


bancoesusalltabsrais2019nodupsCEPS.shape


# In[4]:


bancoesusalltabsrais2019nodupsCEPS.head(3)


# In[5]:


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


# In[6]:


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


# In[7]:


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
                "".join(["http://photon.komoot.io/api?q=", address, "&limit=1"])
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


# In[8]:


#from .base import CEPConverter
#from .strategies import CorreiosPhotonConverter


def cep_to_coords(cep: str, factory: CEPConverter = CorreiosPhotonConverter) -> dict:
    coordinates = factory()(cep)
    return coordinates


# In[9]:


bancoesusalltabsrais2019nodupsCEPS


# In[94]:


#bancoesusalltabsrais2019nodupsCEPS.reset_index(level=0)


# In[95]:


#bancoesusalltabsrais2019nodupsCEPS.reset_index(level=0, inplace = True)


# In[96]:


#bancoesusalltabsrais2019nodupsCEPS.rename(columns={'index':'id'},inplace = True)


# In[97]:


#bancoesusalltabsrais2019nodupsCEPS


# In[10]:


bancoesusalltabsrais2019nodupsCEPS[0:425]


# In[11]:


row0to425 = bancoesusalltabsrais2019nodupsCEPS[0:425]


# In[12]:


row0to425


# In[13]:


row0to425.update("cep_to_coords('" + row0to425[['cep']].astype(str) + "'),")
print(row0to425)


# In[14]:


row0to425


# In[15]:


row0to425=row0to425.loc[:,'cep']


# In[16]:


row0to425


# In[17]:


print(' '.join(row0to425))#.tolist()


# In[18]:


coordenadasrow0to425 = cep_to_coords('55780000'), cep_to_coords('55010250'), cep_to_coords('55000000'), cep_to_coords('55004260'), cep_to_coords('50000000'), cep_to_coords('55020220'), cep_to_coords('53715410'), cep_to_coords('54420010'), cep_to_coords('54410010'), cep_to_coords('54400135'), cep_to_coords('51020160'), cep_to_coords('55125000'), cep_to_coords('51020210'), cep_to_coords('54420280'), cep_to_coords('nan'), cep_to_coords('52050138'), cep_to_coords('50740050'), cep_to_coords('53545630'), cep_to_coords('50670260'), cep_to_coords('53431640'), cep_to_coords('51010020'), cep_to_coords('53401080'), cep_to_coords('51021360'), cep_to_coords('50610100'), cep_to_coords('52010290'), cep_to_coords('53416650'), cep_to_coords('53230130'), cep_to_coords('53437000'), cep_to_coords('52050115'), cep_to_coords('54450220'), cep_to_coords('51030010'), cep_to_coords('54320120'), cep_to_coords('54270230'), cep_to_coords('50710140'), cep_to_coords('50721470'), cep_to_coords('0000000000'), cep_to_coords('52150000'), cep_to_coords('53510290'), cep_to_coords('52021040'), cep_to_coords('52121070'), cep_to_coords('50610300'), cep_to_coords('52120390'), cep_to_coords('53230140'), cep_to_coords('51170590'), cep_to_coords('53250640'), cep_to_coords('54590000'), cep_to_coords('54500000'), cep_to_coords('55695000'), cep_to_coords('53150470'), cep_to_coords('56306620'), cep_to_coords('50781600'), cep_to_coords('50610090'), cep_to_coords('48900400'), cep_to_coords('56314485'), cep_to_coords('56300000'), cep_to_coords('50980745'), cep_to_coords('56395000'), cep_to_coords('56330790'), cep_to_coords('52051100'), cep_to_coords('52041115'), cep_to_coords('54410150'), cep_to_coords('50751090'), cep_to_coords('56316568'), cep_to_coords('54310230'), cep_to_coords('50750320'), cep_to_coords('53020240'), cep_to_coords('52041130'), cep_to_coords('50710330'), cep_to_coords('52050500'), cep_to_coords('12228700'), cep_to_coords('55750000'), cep_to_coords('53010010'), cep_to_coords('56308050'), cep_to_coords('56332720'), cep_to_coords('50680000'), cep_to_coords('55820000'), cep_to_coords('00000000'), cep_to_coords('53421081'), cep_to_coords('55680000'), cep_to_coords('52190190'), cep_to_coords('55940000'), cep_to_coords('58320000'), cep_to_coords('52131180'), cep_to_coords('50980260'), cep_to_coords('51010030'), cep_to_coords('55360000'), cep_to_coords('52080020'), cep_to_coords('50741270'), cep_to_coords('52091010'), cep_to_coords('52171340'), cep_to_coords('50680300'), cep_to_coords('52061240'), cep_to_coords('52061250'), cep_to_coords('52221280'), cep_to_coords('52121220'), cep_to_coords('50761550'), cep_to_coords('50760200'), cep_to_coords('50670500'), cep_to_coords('50780640'), cep_to_coords('53080250'), cep_to_coords('55130000'), cep_to_coords('54460312'), cep_to_coords('55460000'), cep_to_coords('50720380'), cep_to_coords('50640470'), cep_to_coords('51020260'), cep_to_coords('50080600'), cep_to_coords('51300350'), cep_to_coords('53421310'), cep_to_coords('52050050'), cep_to_coords('53150410'), cep_to_coords('52211500'), cep_to_coords('50610000'), cep_to_coords('53260020'), cep_to_coords('50760735'), cep_to_coords('54700500'), cep_to_coords('54774300'), cep_to_coords('50060003'), cep_to_coords('54410470'), cep_to_coords('51320020'), cep_to_coords('55825000'), cep_to_coords('53417220'), cep_to_coords('54210342'), cep_to_coords('54210321'), cep_to_coords('50810500'), cep_to_coords('54735730'), cep_to_coords('50080470'), cep_to_coords('53000000'), cep_to_coords('53540240'), cep_to_coords('53420230'), cep_to_coords('53429230'), cep_to_coords('50781000'), cep_to_coords('55670000'), cep_to_coords('54420080'), cep_to_coords('51020041'), cep_to_coords('52070180'), cep_to_coords('52041550'), cep_to_coords('53402645'), cep_to_coords('53439250'), cep_to_coords('50790000'), cep_to_coords('50770120'), cep_to_coords('50820370'), cep_to_coords('51230040'), cep_to_coords('55600000'), cep_to_coords('29722000'), cep_to_coords('51160000'), cep_to_coords('54330212'), cep_to_coords('54450020'), cep_to_coords('50710470'), cep_to_coords('53437040'), cep_to_coords('54080042'), cep_to_coords('54240350'), cep_to_coords('54753786'), cep_to_coords('51020220'), cep_to_coords('52020070'), cep_to_coords('53320165'), cep_to_coords('53437420'), cep_to_coords('54410390'), cep_to_coords('53421090'), cep_to_coords('54430315'), cep_to_coords('53407610'), cep_to_coords('50860070'), cep_to_coords('53150230'), cep_to_coords('50721775'), cep_to_coords('52121030'), cep_to_coords('51110120'), cep_to_coords('51298412'), cep_to_coords('52110130'), cep_to_coords('52050380'), cep_to_coords('52020020'), cep_to_coords('53080790'), cep_to_coords('54800000'), cep_to_coords('01001000'), cep_to_coords('55150000'), cep_to_coords('52020117'), cep_to_coords('51020050'), cep_to_coords('54756120'), cep_to_coords('53130600'), cep_to_coords('50070075'), cep_to_coords('54400420'), cep_to_coords('54440420'), cep_to_coords('54220000'), cep_to_coords('52030175'), cep_to_coords('54120350'), cep_to_coords('55630000'), cep_to_coords('53300210'), cep_to_coords('54440071'), cep_to_coords('51021000'), cep_to_coords('56540000'), cep_to_coords('50640460'), cep_to_coords('53030060'), cep_to_coords('52051350'), cep_to_coords('54270020'), cep_to_coords('53220130'), cep_to_coords('53030260'), cep_to_coords('50721290'), cep_to_coords('52160838'), cep_to_coords('52110100'), cep_to_coords('52110060'), cep_to_coords('52130000'), cep_to_coords('50950005'), cep_to_coords('52191280'), cep_to_coords('50761340'), cep_to_coords('54240010'), cep_to_coords('52220705'), cep_to_coords('52011055'), cep_to_coords('55640000'), cep_to_coords('53530400'), cep_to_coords('53650575'), cep_to_coords('53416560'), cep_to_coords('55602390'), cep_to_coords('52040250'), cep_to_coords('52130900'), cep_to_coords('51230080'), cep_to_coords('54100680'), cep_to_coords('50060470'), cep_to_coords('51190660'), cep_to_coords('52070013'), cep_to_coords('55270000'), cep_to_coords('53530140'), cep_to_coords('52120320'), cep_to_coords('53350144'), cep_to_coords('54000580'), cep_to_coords('53230191'), cep_to_coords('54740660'), cep_to_coords('51200050'), cep_to_coords('50050400'), cep_to_coords('50740270'), cep_to_coords('55800000'), cep_to_coords('54160680'), cep_to_coords('54589170'), cep_to_coords('54120550'), cep_to_coords('56230500'), cep_to_coords('51170135'), cep_to_coords('50980160'), cep_to_coords('53615772'), cep_to_coords('53625772'), cep_to_coords('53600000'), cep_to_coords('52120057'), cep_to_coords('50040380'), cep_to_coords('52041915'), cep_to_coords('54270100'), cep_to_coords('50940000'), cep_to_coords('53110000'), cep_to_coords('53180160'), cep_to_coords('54789510'), cep_to_coords('50750290'), cep_to_coords('21030500'), cep_to_coords('54325280'), cep_to_coords('53121360'), cep_to_coords('53405615'), cep_to_coords('50920650'), cep_to_coords('54120200'), cep_to_coords('51780000'), cep_to_coords('51130020'), cep_to_coords('51130200'), cep_to_coords('53280090'), cep_to_coords('52081372'), cep_to_coords('53210250'), cep_to_coords('52070647'), cep_to_coords('51020250'), cep_to_coords('53437610'), cep_to_coords('53439430'), cep_to_coords('50740000'), cep_to_coords('51111220'), cep_to_coords('52060280'), cep_to_coords('52051240'), cep_to_coords('52191241'), cep_to_coords('53170270'), cep_to_coords('53080670'), cep_to_coords('55292583'), cep_to_coords('55295300'), cep_to_coords('52020220'), cep_to_coords('50610150'), cep_to_coords('54753140'), cep_to_coords('52041055'), cep_to_coords('51021550'), cep_to_coords('54150095'), cep_to_coords('50920735'), cep_to_coords('56912500'), cep_to_coords('56780000'), cep_to_coords('52020140'), cep_to_coords('50800120'), cep_to_coords('51110290'), cep_to_coords('55650000'), cep_to_coords('51150400'), cep_to_coords('50610120'), cep_to_coords('50860180'), cep_to_coords('50760016'), cep_to_coords('50820480'), cep_to_coords('50640280'), cep_to_coords('52030140'), cep_to_coords('50750400'), cep_to_coords('53030080'), cep_to_coords('55614727'), cep_to_coords('54430200'), cep_to_coords('53370450'), cep_to_coords('55515000'), cep_to_coords('53000600'), cep_to_coords('54783010'), cep_to_coords('50860000'), cep_to_coords('50680180'), cep_to_coords('52011040'), cep_to_coords('50090075'), cep_to_coords('50810777'), cep_to_coords('50771040'), cep_to_coords('50030280'), cep_to_coords('50781430'), cep_to_coords('54350000'), cep_to_coords('54786160'), cep_to_coords('54753785'), cep_to_coords('53010430'), cep_to_coords('53370260'), cep_to_coords('53180670'), cep_to_coords('53435610'), cep_to_coords('53140210'), cep_to_coords('52020015'), cep_to_coords('52020010'), cep_to_coords('53050440'), cep_to_coords('55610350'), cep_to_coords('54400020'), cep_to_coords('54330680'), cep_to_coords('52050555'), cep_to_coords('50930380'), cep_to_coords('53330550'), cep_to_coords('52280232'), cep_to_coords('52051280'), cep_to_coords('52060150'), cep_to_coords('53050170'), cep_to_coords('52030010'), cep_to_coords('50870520'), cep_to_coords('50721170'), cep_to_coords('50721175'), cep_to_coords('52040350'), cep_to_coords('53435030'), cep_to_coords('54762620'), cep_to_coords('55815140'), cep_to_coords('53082080'), cep_to_coords('50920135'), cep_to_coords('51020000'), cep_to_coords('50730670'), cep_to_coords('50790150'), cep_to_coords('53130350'), cep_to_coords('51170390'), cep_to_coords('50980645'), cep_to_coords('54762315'), cep_to_coords('50050450'), cep_to_coords('50710100'), cep_to_coords('50711290'), cep_to_coords('50741350'), cep_to_coords('52171011'), cep_to_coords('50731230'), cep_to_coords('54762740'), cep_to_coords('50761620'), cep_to_coords('50810040'), cep_to_coords('54762640'), cep_to_coords('52080250'), cep_to_coords('50780020'), cep_to_coords('52490300'), cep_to_coords('50720680'), cep_to_coords('52110440'), cep_to_coords('52041430'), cep_to_coords('55850000'), cep_to_coords('50810460'), cep_to_coords('55745000'), cep_to_coords('53404030'), cep_to_coords('29815000'), cep_to_coords('53190310'), cep_to_coords('54740570'), cep_to_coords('51020280'), cep_to_coords('53431690'), cep_to_coords('53150360'), cep_to_coords('54759270'), cep_to_coords('51010210'), cep_to_coords('51150130'), cep_to_coords('55296510'), cep_to_coords('55290000'), cep_to_coords('50610320'), cep_to_coords('54330561'), cep_to_coords('52070010'), cep_to_coords('54786770'), cep_to_coords('50800080'), cep_to_coords('53370550'), cep_to_coords('51300130'), cep_to_coords('50970350'), cep_to_coords('52090046'), cep_to_coords('53140015'), cep_to_coords('53150260'), cep_to_coords('54430160'), cep_to_coords('53435550'), cep_to_coords('53437360'), cep_to_coords('55240000'), cep_to_coords('55200000'), cep_to_coords('50731340'), cep_to_coords('54320302'), cep_to_coords('51270170'), cep_to_coords('50810420'), cep_to_coords('53210160'), cep_to_coords('53060380'), cep_to_coords('50710310'), cep_to_coords('53130070'), cep_to_coords('52160835'), cep_to_coords('52211100'), cep_to_coords('50761060'), cep_to_coords('54460640'), cep_to_coords('54340080'), cep_to_coords('52020000'), cep_to_coords('53900000'), cep_to_coords('53080410'), cep_to_coords('53431020'), cep_to_coords('51240350'), cep_to_coords('55602000'), cep_to_coords('51170320'), cep_to_coords('53270645'), cep_to_coords('54330300'), cep_to_coords('53220375'), cep_to_coords('50100280'), cep_to_coords('54330380'), cep_to_coords('54330038'), cep_to_coords('52210330'), cep_to_coords('53403500'), cep_to_coords('91021100'), cep_to_coords('52080040'), cep_to_coords('51030140'), cep_to_coords('50750230')


# In[19]:


print(coordenadasrow0to425)


# In[20]:


row0to425


# In[21]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in row0to425.tolist():
    result.append(''.join(pattern.findall(item)))


# In[22]:


print(result)


# In[23]:


dfrow0to425 = pd.DataFrame(coordenadasrow0to425, result)


# In[24]:


dfrow0to425 


# In[25]:


dfrow0to425.reset_index(level=0, inplace=True) #make the index a column


# In[26]:


dfrow0to425 


# In[27]:


dfrow0to425  = dfrow0to425.rename(columns={'index':'cep'}) #change a column's name


# In[28]:


dfrow0to425


# In[36]:


bancoesusalltabsrais2019nodupsCEPS[['id']][0:425]


# In[37]:


dfrow0to425['id']=bancoesusalltabsrais2019nodupsCEPS[['id']][0:425]


# In[38]:


dfrow0to425


# In[41]:


dfrow0to425


# In[44]:


dfrow0to425[dfrow0to425.columns[[3,0,1,2]]]


# In[45]:


dfrow0to425 = dfrow0to425[dfrow0to425.columns[[3,0,1,2]]]


# In[46]:


dfrow0to425


# In[48]:


dfrow0to425.to_excel('dfrow0to425latlong.xlsx')


# In[ ]:





# # bancoesusalltabsrais2019nodupsCEPS[425:5426]

# In[49]:


bancoesusalltabsrais2019nodupsCEPS[0:425]


# In[53]:


bancoesusalltabsrais2019nodupsCEPS[425:5426]


# In[54]:


row425to5425 = bancoesusalltabsrais2019nodupsCEPS[425:5426]


# In[55]:


row425to5425


# In[56]:


row425to5425.update("cep_to_coords('" + row425to5425[['cep']].astype(str) + "'),")
print(row425to5425)


# In[57]:


row425to5425


# In[58]:


row425to5425=row425to5425.loc[:,'cep']


# In[59]:


row425to5425


# In[60]:


print(' '.join(row425to5425))#.tolist()


# In[61]:


coordenadasrow425to5425 = cep_to_coords('53010200'), cep_to_coords('53407300'), cep_to_coords('50670380'), cep_to_coords('50761070'), cep_to_coords('55720000'), cep_to_coords('54735075'), cep_to_coords('53427420'), cep_to_coords('4406 a 48'), cep_to_coords('54440000'), cep_to_coords('53030050'), cep_to_coords('55810000'), cep_to_coords('54220290'), cep_to_coords('50730640'), cep_to_coords('50761410'), cep_to_coords('52210420'), cep_to_coords('53425030'), cep_to_coords('53425010'), cep_to_coords('54440350'), cep_to_coords('53416100'), cep_to_coords('51280020'), cep_to_coords('52131300'), cep_to_coords('52171170'), cep_to_coords('53437460'), cep_to_coords('53437440'), cep_to_coords('52221260'), cep_to_coords('53415370'), cep_to_coords('53441625'), cep_to_coords('54767620'), cep_to_coords('52070480'), cep_to_coords('52030060'), cep_to_coords('54705160'), cep_to_coords('55555555'), cep_to_coords('55560000'), cep_to_coords('54789000'), cep_to_coords('53409290'), cep_to_coords('52070080'), cep_to_coords('52030170'), cep_to_coords('52280280'), cep_to_coords('54280243'), cep_to_coords('53060450'), cep_to_coords('50610220'), cep_to_coords('51180000'), cep_to_coords('51270281'), cep_to_coords('53270710'), cep_to_coords('50725720'), cep_to_coords('50740170'), cep_to_coords('50070570'), cep_to_coords('52221370'), cep_to_coords('51020011'), cep_to_coords('54315240'), cep_to_coords('54150561'), cep_to_coords('54240250'), cep_to_coords('54150040'), cep_to_coords('54220730'), cep_to_coords('54756653'), cep_to_coords('53240450'), cep_to_coords('51250102'), cep_to_coords('51250020'), cep_to_coords('53433090'), cep_to_coords('53530458'), cep_to_coords('54780040'), cep_to_coords('52070100'), cep_to_coords('50630260'), cep_to_coords('54720225'), cep_to_coords('53250140'), cep_to_coords('52040310'), cep_to_coords('50960120'), cep_to_coords('50930050'), cep_to_coords('53421420'), cep_to_coords('50741530'), cep_to_coords('52060110'), cep_to_coords('53130540'), cep_to_coords('52071280'), cep_to_coords('51340560'), cep_to_coords('53402793'), cep_to_coords('53080340'), cep_to_coords('54270150'), cep_to_coords('55370000'), cep_to_coords('53370351'), cep_to_coords('54910545'), cep_to_coords('5000000000'), cep_to_coords('50910545'), cep_to_coords('50791475'), cep_to_coords('53030010'), cep_to_coords('50720635'), cep_to_coords('50090750'), cep_to_coords('99999999'), cep_to_coords('52150210'), cep_to_coords('53404400'), cep_to_coords('52090370'), cep_to_coords('52051120'), cep_to_coords('50751440'), cep_to_coords('50980360'), cep_to_coords('50820030'), cep_to_coords('53240030'), cep_to_coords('54771570'), cep_to_coords('50080450'), cep_to_coords('50761360'), cep_to_coords('52070270'), cep_to_coords('51111040'), cep_to_coords('51110040'), cep_to_coords('52190100'), cep_to_coords('50730210'), cep_to_coords('52040050'), cep_to_coords('50780470'), cep_to_coords('53180052'), cep_to_coords('54771060'), cep_to_coords('52070530'), cep_to_coords('51320470'), cep_to_coords('50721080'), cep_to_coords('52011090'), cep_to_coords('50920310'), cep_to_coords('52061540'), cep_to_coords('53140150'), cep_to_coords('50800180'), cep_to_coords('53080680'), cep_to_coords('53429470'), cep_to_coords('53130250'), cep_to_coords('53585200'), cep_to_coords('52050052'), cep_to_coords('53290010'), cep_to_coords('52170200'), cep_to_coords('51030820'), cep_to_coords('52080290'), cep_to_coords('53170621'), cep_to_coords('53150210'), cep_to_coords('54330351'), cep_to_coords('51020231'), cep_to_coords('54762484'), cep_to_coords('50980060'), cep_to_coords('52130050'), cep_to_coords('50761540'), cep_to_coords('51345560'), cep_to_coords('50710435'), cep_to_coords('52091200'), cep_to_coords('54759540'), cep_to_coords('52091300'), cep_to_coords('52041010'), cep_to_coords('52041045'), cep_to_coords('53090070'), cep_to_coords('54210390'), cep_to_coords('51260130'), cep_to_coords('75101080'), cep_to_coords('52210040'), cep_to_coords('54735110'), cep_to_coords('51350190'), cep_to_coords('50360250'), cep_to_coords('50630250'), cep_to_coords('50660110'), cep_to_coords('53090435'), cep_to_coords('55435000'), cep_to_coords('56640000'), cep_to_coords('55340000'), cep_to_coords('54400000'), cep_to_coords('54410435'), cep_to_coords('53635120'), cep_to_coords('50060080'), cep_to_coords('51320050'), cep_to_coords('54120400'), cep_to_coords('52110000'), cep_to_coords('56343000'), cep_to_coords('51010010'), cep_to_coords('54240200'), cep_to_coords('54777510'), cep_to_coords('54320030'), cep_to_coords('53421521'), cep_to_coords('53370490'), cep_to_coords('53125750'), cep_to_coords('53421351'), cep_to_coords('52020170'), cep_to_coords('54090438'), cep_to_coords('51010110'), cep_to_coords('53402220'), cep_to_coords('54440120'), cep_to_coords('53423340'), cep_to_coords('51021350'), cep_to_coords('51470190'), cep_to_coords('56900000'), cep_to_coords('51021190'), cep_to_coords('51160070'), cep_to_coords('50760360'), cep_to_coords('53020230'), cep_to_coords('53240440'), cep_to_coords('54070220'), cep_to_coords('54230040'), cep_to_coords('50670020'), cep_to_coords('50570020'), cep_to_coords('53150120'), cep_to_coords('53416070'), cep_to_coords('54753280'), cep_to_coords('54071250'), cep_to_coords('53370560'), cep_to_coords('50100240'), cep_to_coords('53270685'), cep_to_coords('53150170'), cep_to_coords('52131000'), cep_to_coords('50780035'), cep_to_coords('53435540'), cep_to_coords('53435455'), cep_to_coords('50070345'), cep_to_coords('56215000'), cep_to_coords('56330370'), cep_to_coords('54160546'), cep_to_coords('50731060'), cep_to_coords('55170000'), cep_to_coords('54410280'), cep_to_coords('50791280'), cep_to_coords('52121071'), cep_to_coords('51021130'), cep_to_coords('52280081'), cep_to_coords('50740430'), cep_to_coords('53441340'), cep_to_coords('51021010'), cep_to_coords('51021310'), cep_to_coords('50940920'), cep_to_coords('50791236'), cep_to_coords('50710240'), cep_to_coords('50761160'), cep_to_coords('52061080'), cep_to_coords('53427600'), cep_to_coords('50761520'), cep_to_coords('53230530'), cep_to_coords('50070355'), cep_to_coords('50070040'), cep_to_coords('51030060'), cep_to_coords('51240040'), cep_to_coords('52110050'), cep_to_coords('52280514'), cep_to_coords('52111370'), cep_to_coords('50070120'), cep_to_coords('50740535'), cep_to_coords('53280000'), cep_to_coords('54771645'), cep_to_coords('52031180'), cep_to_coords('55620000'), cep_to_coords('55016270'), cep_to_coords('55495000'), cep_to_coords('55008000'), cep_to_coords('54762430'), cep_to_coords('51011220'), cep_to_coords('53441080'), cep_to_coords('53565180'), cep_to_coords('51260010'), cep_to_coords('52050370'), cep_to_coords('54430314'), cep_to_coords('55614630'), cep_to_coords('57976848'), cep_to_coords('50640040'), cep_to_coords('52120300'), cep_to_coords('54410471'), cep_to_coords('53370510'), cep_to_coords('54250531'), cep_to_coords('55860000'), cep_to_coords('52040320'), cep_to_coords('53090340'), cep_to_coords('53690840'), cep_to_coords('53690000'), cep_to_coords('52051000'), cep_to_coords('52060040'), cep_to_coords('53413020'), cep_to_coords('53370255'), cep_to_coords('53070270'), cep_to_coords('56170000'), cep_to_coords('56000000'), cep_to_coords('56190000'), cep_to_coords('52080365'), cep_to_coords('53120000'), cep_to_coords('50810020'), cep_to_coords('50731330'), cep_to_coords('50770765'), cep_to_coords('54756080'), cep_to_coords('52071381'), cep_to_coords('52081030'), cep_to_coords('53270210'), cep_to_coords('54759640'), cep_to_coords('54768210'), cep_to_coords('52051395'), cep_to_coords('50711340'), cep_to_coords('51130040'), cep_to_coords('55870000'), cep_to_coords('55590000'), cep_to_coords('54730671'), cep_to_coords('54730380'), cep_to_coords('52070648'), cep_to_coords('62060030'), cep_to_coords('50640180'), cep_to_coords('52060035'), cep_to_coords('53435640'), cep_to_coords('53270570'), cep_to_coords('50960280'), cep_to_coords('52170000'), cep_to_coords('52120260'), cep_to_coords('50040090'), cep_to_coords('50670390'), cep_to_coords('53139226'), cep_to_coords('50720400'), cep_to_coords('50630400'), cep_to_coords('54715350'), cep_to_coords('52020095'), cep_to_coords('50110788'), cep_to_coords('54460260'), cep_to_coords('53300080'), cep_to_coords('50731140'), cep_to_coords('53700000'), cep_to_coords('55550000'), cep_to_coords('55030270'), cep_to_coords('54768340'), cep_to_coords('50761585'), cep_to_coords('50751370'), cep_to_coords('52070000'), cep_to_coords('52040150'), cep_to_coords('54768180'), cep_to_coords('53402710'), cep_to_coords('53290070'), cep_to_coords('51190120'), cep_to_coords('53110270'), cep_to_coords('54730010'), cep_to_coords('54410290'), cep_to_coords('53431420'), cep_to_coords('52081120'), cep_to_coords('52111474'), cep_to_coords('51260590'), cep_to_coords('50741120'), cep_to_coords('54120551'), cep_to_coords('50761090'), cep_to_coords('50710500'), cep_to_coords('53200000'), cep_to_coords('51240125'), cep_to_coords('52171055'), cep_to_coords('52291130'), cep_to_coords('52070370'), cep_to_coords('54730810'), cep_to_coords('54580980'), cep_to_coords('53402320'), cep_to_coords('50670370'), cep_to_coords('51020035'), cep_to_coords('55012680'), cep_to_coords('52041080'), cep_to_coords('50610450'), cep_to_coords('51030580'), cep_to_coords('54500995'), cep_to_coords('51330330'), cep_to_coords('52031070'), cep_to_coords('51010100'), cep_to_coords('51020001'), cep_to_coords('52011230'), cep_to_coords('53330570'), cep_to_coords('53140050'), cep_to_coords('54070050'), cep_to_coords('52160470'), cep_to_coords('50110752'), cep_to_coords('50780185'), cep_to_coords('50920490'), cep_to_coords('50760520'), cep_to_coords('50790460'), cep_to_coords('51300240'), cep_to_coords('52021180'), cep_to_coords('52030260'), cep_to_coords('52160010'), cep_to_coords('52291291'), cep_to_coords('52050020'), cep_to_coords('51021150'), cep_to_coords('52070493'), cep_to_coords('52010040'), cep_to_coords('53403322'), cep_to_coords('54753490'), cep_to_coords('50720001'), cep_to_coords('51160290'), cep_to_coords('51350330'), cep_to_coords('50791480'), cep_to_coords('50129309'), cep_to_coords('54580740'), cep_to_coords('53370720'), cep_to_coords('52071250'), cep_to_coords('51010060'), cep_to_coords('54460200'), cep_to_coords('51150020'), cep_to_coords('51350310'), cep_to_coords('51240210'), cep_to_coords('51030180'), cep_to_coords('53220122'), cep_to_coords('55500000'), cep_to_coords('54510907'), cep_to_coords('52040040'), cep_to_coords('50731400'), cep_to_coords('50711020'), cep_to_coords('51130525'), cep_to_coords('54368170'), cep_to_coords('54360008'), cep_to_coords('54530012'), cep_to_coords('52070240'), cep_to_coords('51210020'), cep_to_coords('50650320'), cep_to_coords('50710730'), cep_to_coords('52041040'), cep_to_coords('51280415'), cep_to_coords('51130000'), cep_to_coords('46277595'), cep_to_coords('51021510'), cep_to_coords('53130280'), cep_to_coords('51260230'), cep_to_coords('54100425'), cep_to_coords('54090430'), cep_to_coords('56800000'), cep_to_coords('50900190'), cep_to_coords('54530390'), cep_to_coords('54515030'), cep_to_coords('54750000'), cep_to_coords('54745440'), cep_to_coords('53370390'), cep_to_coords('52011060'), cep_to_coords('54410100'), cep_to_coords('54762380'), cep_to_coords('54768450'), cep_to_coords('54759060'), cep_to_coords('54771540'), cep_to_coords('50930670'), cep_to_coords('54440290'), cep_to_coords('50781340'), cep_to_coords('54762470'), cep_to_coords('56328100'), cep_to_coords('50690290'), cep_to_coords('55260000'), cep_to_coords('50920120'), cep_to_coords('53280185'), cep_to_coords('55642114'), cep_to_coords('54230222'), cep_to_coords('52061380'), cep_to_coords('50630700'), cep_to_coords('51350630'), cep_to_coords('53431080'), cep_to_coords('53150005'), cep_to_coords('53439400'), cep_to_coords('51021240'), cep_to_coords('50830720'), cep_to_coords('53625213'), cep_to_coords('52041160'), cep_to_coords('50860260'), cep_to_coords('55610000'), cep_to_coords('50710050'), cep_to_coords('50710030'), cep_to_coords('52050060'), cep_to_coords('50610110'), cep_to_coords('54300370'), cep_to_coords('54705211'), cep_to_coords('50720595'), cep_to_coords('51230260'), cep_to_coords('50761040'), cep_to_coords('50050440'), cep_to_coords('50100170'), cep_to_coords('50710215'), cep_to_coords('54250182'), cep_to_coords('51130030'), cep_to_coords('53409640'), cep_to_coords('53401150'), cep_to_coords('50721650'), cep_to_coords('52120520'), cep_to_coords('54753150'), cep_to_coords('51310570'), cep_to_coords('53320560'), cep_to_coords('51335270'), cep_to_coords('52280510'), cep_to_coords('51030350'), cep_to_coords('50070390'), cep_to_coords('53439171'), cep_to_coords('50720360'), cep_to_coords('51350530'), cep_to_coords('53060050'), cep_to_coords('50761320'), cep_to_coords('53220220'), cep_to_coords('56280000'), cep_to_coords('54280120'), cep_to_coords('51021380'), cep_to_coords('53050320'), cep_to_coords('53240150'), cep_to_coords('52110145'), cep_to_coords('54090110'), cep_to_coords('54210020'), cep_to_coords('53070040'), cep_to_coords('55890000'), cep_to_coords('50711105'), cep_to_coords('51130250'), cep_to_coords('54515170'), cep_to_coords('52120180'), cep_to_coords('52120355'), cep_to_coords('55886000'), cep_to_coords('50761390'), cep_to_coords('54430030'), cep_to_coords('54280075'), cep_to_coords('54140040'), cep_to_coords('54430140'), cep_to_coords('52191100'), cep_to_coords('55810190'), cep_to_coords('55028030'), cep_to_coords('53130500'), cep_to_coords('53640648'), cep_to_coords('52010150'), cep_to_coords('50760225'), cep_to_coords('52120200'), cep_to_coords('53437100'), cep_to_coords('53409700'), cep_to_coords('50630300'), cep_to_coords('50670130'), cep_to_coords('50790380'), cep_to_coords('52111090'), cep_to_coords('54240130'), cep_to_coords('53439310'), cep_to_coords('52160130'), cep_to_coords('51020512'), cep_to_coords('50040020'), cep_to_coords('53415040'), cep_to_coords('54320050'), cep_to_coords('53416010'), cep_to_coords('51160300'), cep_to_coords('50690520'), cep_to_coords('55038220'), cep_to_coords('54520295'), cep_to_coords('53240240'), cep_to_coords('53330150'), cep_to_coords('53090097'), cep_to_coords('50730450'), cep_to_coords('53140130'), cep_to_coords('50720110'), cep_to_coords('50730600'), cep_to_coords('50791510'), cep_to_coords('52160455'), cep_to_coords('53050070'), cep_to_coords('53401260'), cep_to_coords('53433790'), cep_to_coords('53439360'), cep_to_coords('54000750'), cep_to_coords('54705281'), cep_to_coords('53439205'), cep_to_coords('54753320'), cep_to_coords('52160836'), cep_to_coords('50731040'), cep_to_coords('50050902'), cep_to_coords('53110500'), cep_to_coords('54299899'), cep_to_coords('51330410'), cep_to_coords('52660290'), cep_to_coords('52211005'), cep_to_coords('51010760'), cep_to_coords('51021480'), cep_to_coords('53370060'), cep_to_coords('52031060'), cep_to_coords('54325410'), cep_to_coords('52280043'), cep_to_coords('52081515'), cep_to_coords('54320000'), cep_to_coords('52021240'), cep_to_coords('50731290'), cep_to_coords('54535200'), cep_to_coords('54220470'), cep_to_coords('54777320'), cep_to_coords('54280642'), cep_to_coords('54280638'), cep_to_coords('54280129'), cep_to_coords('52011210'), cep_to_coords('52130210'), cep_to_coords('53030040'), cep_to_coords('54000010'), cep_to_coords('54090470'), cep_to_coords('56328210'), cep_to_coords('53403370'), cep_to_coords('50721440'), cep_to_coords('50970010'), cep_to_coords('52110270'), cep_to_coords('51020090'), cep_to_coords('53170635'), cep_to_coords('54515558'), cep_to_coords('52120030'), cep_to_coords('50630650'), cep_to_coords('50710510'), cep_to_coords('53110140'), cep_to_coords('55641000'), cep_to_coords('53130230'), cep_to_coords('53370470'), cep_to_coords('50670060'), cep_to_coords('53407560'), cep_to_coords('54000000'), cep_to_coords('50740010'), cep_to_coords('51021370'), cep_to_coords('54440615'), cep_to_coords('50750260'), cep_to_coords('54000800'), cep_to_coords('54220140'), cep_to_coords('50720705'), cep_to_coords('55014300'), cep_to_coords('54580648'), cep_to_coords('54580645'), cep_to_coords('51021070'), cep_to_coords('52050150'), cep_to_coords('53203019'), cep_to_coords('53230190'), cep_to_coords('50721260'), cep_to_coords('50730240'), cep_to_coords('52080010'), cep_to_coords('54725170'), cep_to_coords('53230670'), cep_to_coords('51030030'), cep_to_coords('53350670'), cep_to_coords('52221170'), cep_to_coords('52051380'), cep_to_coords('52071390'), cep_to_coords('50920121'), cep_to_coords('52040080'), cep_to_coords('53140080'), cep_to_coords('50680070'), cep_to_coords('54580430'), cep_to_coords('51020140'), cep_to_coords('52111410'), cep_to_coords('52041000'), cep_to_coords('54756310'), cep_to_coords('52230000'), cep_to_coords('54330203'), cep_to_coords('53405170'), cep_to_coords('54250120'), cep_to_coords('56314430'), cep_to_coords('56302000'), cep_to_coords('56328150'), cep_to_coords('56306385'), cep_to_coords('54210030'), cep_to_coords('52211003'), cep_to_coords('55297575'), cep_to_coords('54090240'), cep_to_coords('50900065'), cep_to_coords('51280200'), cep_to_coords('52050387'), cep_to_coords('54052380'), cep_to_coords('54505904'), cep_to_coords('54735000'), cep_to_coords('52210120'), cep_to_coords('51250480'), cep_to_coords('52061160'), cep_to_coords('50720555'), cep_to_coords('50731110'), cep_to_coords('52111000'), cep_to_coords('55015080'), cep_to_coords('50940370'), cep_to_coords('55555000'), cep_to_coords('55540000'), cep_to_coords('53441510'), cep_to_coords('54410021'), cep_to_coords('53060170'), cep_to_coords('54310420'), cep_to_coords('56200000'), cep_to_coords('54720210'), cep_to_coords('54170430'), cep_to_coords('54280080'), cep_to_coords('50720550'), cep_to_coords('51130330'), cep_to_coords('53270430'), cep_to_coords('50761580'), cep_to_coords('52111140'), cep_to_coords('51011140'), cep_to_coords('53421020'), cep_to_coords('53422180'), cep_to_coords('50730160'), cep_to_coords('51003010'), cep_to_coords('54270120'), cep_to_coords('53435310'), cep_to_coords('52221295'), cep_to_coords('52221330'), cep_to_coords('53210840'), cep_to_coords('53402580'), cep_to_coords('52111540'), cep_to_coords('51240730'), cep_to_coords('50640680'), cep_to_coords('52030160'), cep_to_coords('52041345'), cep_to_coords('50070450'), cep_to_coords('52110002'), cep_to_coords('52040370'), cep_to_coords('52110459'), cep_to_coords('51020190'), cep_to_coords('53431400'), cep_to_coords('52121100'), cep_to_coords('50980370'), cep_to_coords('50710485'), cep_to_coords('51340230'), cep_to_coords('50710265'), cep_to_coords('50610060'), cep_to_coords('51011610'), cep_to_coords('50010000'), cep_to_coords('54230240'), cep_to_coords('53530488'), cep_to_coords('54720661'), cep_to_coords('53640220'), cep_to_coords('53298280'), cep_to_coords('53370192'), cep_to_coords('54210192'), cep_to_coords('54580165'), cep_to_coords('54220190'), cep_to_coords('51270080'), cep_to_coords('52120010'), cep_to_coords('52004030'), cep_to_coords('52051200'), cep_to_coords('51870080'), cep_to_coords('55450000'), cep_to_coords('50050180'), cep_to_coords('54771680'), cep_to_coords('53220190'), cep_to_coords('54100051'), cep_to_coords('54792992'), cep_to_coords('50771380'), cep_to_coords('50730180'), cep_to_coords('54753190'), cep_to_coords('53160190'), cep_to_coords('53441030'), cep_to_coords('53330040'), cep_to_coords('54762020'), cep_to_coords('54170010'), cep_to_coords('51030065'), cep_to_coords('50900340'), cep_to_coords('54460000'), cep_to_coords('51350180'), cep_to_coords('53240480'), cep_to_coords('52011170'), cep_to_coords('53120090'), cep_to_coords('51020290'), cep_to_coords('51290160'), cep_to_coords('50865090'), cep_to_coords('53437430'), cep_to_coords('54720244'), cep_to_coords('53070290'), cep_to_coords('53320580'), cep_to_coords('53435780'), cep_to_coords('52070060'), cep_to_coords('51021330'), cep_to_coords('53437480'), cep_to_coords('53425070'), cep_to_coords('52070525'), cep_to_coords('53444090'), cep_to_coords('52081280'), cep_to_coords('50710450'), cep_to_coords('51230240'), cep_to_coords('50970280'), cep_to_coords('52050420'), cep_to_coords('54450010'), cep_to_coords('50316078'), cep_to_coords('53060260'), cep_to_coords('53403610'), cep_to_coords('54762732'), cep_to_coords('54490460'), cep_to_coords('52051260'), cep_to_coords('53407040'), cep_to_coords('53407331'), cep_to_coords('52061410'), cep_to_coords('50860241'), cep_to_coords('51350520'), cep_to_coords('54430250'), cep_to_coords('54230639'), cep_to_coords('54230120'), cep_to_coords('53439100'), cep_to_coords('53530408'), cep_to_coords('53435110'), cep_to_coords('50620150'), cep_to_coords('53422000'), cep_to_coords('54230012'), cep_to_coords('52041335'), cep_to_coords('55510000'), cep_to_coords('53260110'), cep_to_coords('53400000'), cep_to_coords('53110380'), cep_to_coords('54530060'), cep_to_coords('55330000'), cep_to_coords('56326180'), cep_to_coords('56310710'), cep_to_coords('54580330'), cep_to_coords('53350460'), cep_to_coords('54765050'), cep_to_coords('53150700'), cep_to_coords('50680030'), cep_to_coords('54150191'), cep_to_coords('51340140'), cep_to_coords('53427000'), cep_to_coords('56506570'), cep_to_coords('56508195'), cep_to_coords('53040055'), cep_to_coords('51350095'), cep_to_coords('52070492'), cep_to_coords('56503380'), cep_to_coords('54774615'), cep_to_coords('56508460'), cep_to_coords('56506485'), cep_to_coords('56506480'), cep_to_coords('54220020'), cep_to_coords('56470000'), cep_to_coords('56509600'), cep_to_coords('55740000'), cep_to_coords('52140300'), cep_to_coords('50791111'), cep_to_coords('53437400'), cep_to_coords('54100581'), cep_to_coords('54320200'), cep_to_coords('53030250'), cep_to_coords('56500000'), cep_to_coords('56503620'), cep_to_coords('56512180'), cep_to_coords('56503270'), cep_to_coords('53439300'), cep_to_coords('56504105'), cep_to_coords('56505150'), cep_to_coords('56505030'), cep_to_coords('53990000'), cep_to_coords('53439791'), cep_to_coords('55614700'), cep_to_coords('52081540'), cep_to_coords('53300290'), cep_to_coords('56519360'), cep_to_coords('56600000'), cep_to_coords('53130270'), cep_to_coords('52170380'), cep_to_coords('56250000'), cep_to_coords('51011110'), cep_to_coords('50670010'), cep_to_coords('52040253'), cep_to_coords('51270240'), cep_to_coords('54580745'), cep_to_coords('53220620'), cep_to_coords('56505010'), cep_to_coords('55814970'), cep_to_coords('50110400'), cep_to_coords('51150330'), cep_to_coords('54140033'), cep_to_coords('53437790'), cep_to_coords('55814030'), cep_to_coords('53170285'), cep_to_coords('53170000'), cep_to_coords('53230090'), cep_to_coords('54490114'), cep_to_coords('50940620'), cep_to_coords('50810070'), cep_to_coords('51010370'), cep_to_coords('53280085'), cep_to_coords('52210020'), cep_to_coords('54325002'), cep_to_coords('53370828'), cep_to_coords('53403245'), cep_to_coords('53370580'), cep_to_coords('53439630'), cep_to_coords('50741200'), cep_to_coords('51010050'), cep_to_coords('51160210'), cep_to_coords('52020060'), cep_to_coords('53625813'), cep_to_coords('55608240'), cep_to_coords('52091151'), cep_to_coords('53402010'), cep_to_coords('54280715'), cep_to_coords('51240470'), cep_to_coords('54270000'), cep_to_coords('54580435'), cep_to_coords('53110110'), cep_to_coords('53441204'), cep_to_coords('53437250'), cep_to_coords('50640340'), cep_to_coords('53431470'), cep_to_coords('50660320'), cep_to_coords('52041015'), cep_to_coords('53421171'), cep_to_coords('53442000'), cep_to_coords('51010560'), cep_to_coords('53070050'), cep_to_coords('51230030'), cep_to_coords('53421180'), cep_to_coords('50760500'), cep_to_coords('50740080'), cep_to_coords('53360290'), cep_to_coords('53441220'), cep_to_coords('51030160'), cep_to_coords('51270530'), cep_to_coords('50820010'), cep_to_coords('54433025'), cep_to_coords('53300190'), cep_to_coords('53230410'), cep_to_coords('53417715'), cep_to_coords('54070030'), cep_to_coords('52110020'), cep_to_coords('50710010'), cep_to_coords('53409370'), cep_to_coords('53050270'), cep_to_coords('53130410'), cep_to_coords('54730321'), cep_to_coords('53431090'), cep_to_coords('54270090'), cep_to_coords('53402520'), cep_to_coords('54420200'), cep_to_coords('50960300'), cep_to_coords('53070100'), cep_to_coords('50920400'), cep_to_coords('52111590'), cep_to_coords('51230560'), cep_to_coords('52230360'), cep_to_coords('54735450'), cep_to_coords('53441490'), cep_to_coords('53439150'), cep_to_coords('53437130'), cep_to_coords('50711110'), cep_to_coords('50721110'), cep_to_coords('50865100'), cep_to_coords('52221175'), cep_to_coords('52221070'), cep_to_coords('51000000'), cep_to_coords('53080800'), cep_to_coords('54460015'), cep_to_coords('51130310'), cep_to_coords('50830470'), cep_to_coords('51160220'), cep_to_coords('50760009'), cep_to_coords('51250470'), cep_to_coords('52011160'), cep_to_coords('50741370'), cep_to_coords('50875140'), cep_to_coords('52041180'), cep_to_coords('52050042'), cep_to_coords('52050320'), cep_to_coords('54589205'), cep_to_coords('54266004'), cep_to_coords('53427290'), cep_to_coords('58860000'), cep_to_coords('51130290'), cep_to_coords('51021230'), cep_to_coords('53437060'), cep_to_coords('53330580'), cep_to_coords('53160640'), cep_to_coords('53140230'), cep_to_coords('52031140'), cep_to_coords('52070230'), cep_to_coords('53407440'), cep_to_coords('53270530'), cep_to_coords('52040010'), cep_to_coords('52051270'), cep_to_coords('51020010'), cep_to_coords('51030310'), cep_to_coords('52291210'), cep_to_coords('53415130'), cep_to_coords('53435580'), cep_to_coords('53437820'), cep_to_coords('50761260'), cep_to_coords('54735130'), cep_to_coords('54749000'), cep_to_coords('53080780'), cep_to_coords('50710190'), cep_to_coords('52060105'), cep_to_coords('53422630'), cep_to_coords('54320111'), cep_to_coords('53431185'), cep_to_coords('54762310'), cep_to_coords('50080410'), cep_to_coords('54450250'), cep_to_coords('54530000'), cep_to_coords('55024790'), cep_to_coords('54280005'), cep_to_coords('54735480'), cep_to_coords('52111070'), cep_to_coords('55900000'), cep_to_coords('53370140'), cep_to_coords('54756055'), cep_to_coords('53140190'), cep_to_coords('55292380'), cep_to_coords('54520260'), cep_to_coords('54589335'), cep_to_coords('54510320'), cep_to_coords('53610284'), cep_to_coords('50050540'), cep_to_coords('54762605'), cep_to_coords('52221380'), cep_to_coords('53280020'), cep_to_coords('52021220'), cep_to_coords('52140620'), cep_to_coords('51021060'), cep_to_coords('53421815'), cep_to_coords('52061070'), cep_to_coords('52060430'), cep_to_coords('52040020'), cep_to_coords('50830450'), cep_to_coords('55036510'), cep_to_coords('54230710'), cep_to_coords('53070220'), cep_to_coords('52120310'), cep_to_coords('54260590'), cep_to_coords('54771010'), cep_to_coords('53080700'), cep_to_coords('52090410'), cep_to_coords('55155000'), cep_to_coords('50680210'), cep_to_coords('50920090'), cep_to_coords('52111081'), cep_to_coords('54410640'), cep_to_coords('52071050'), cep_to_coords('54430060'), cep_to_coords('51170270'), cep_to_coords('50710115'), cep_to_coords('51250170'), cep_to_coords('50720090'), cep_to_coords('53520095'), cep_to_coords('50741150'), cep_to_coords('53413640'), cep_to_coords('53417430'), cep_to_coords('53403000'), cep_to_coords('52130221'), cep_to_coords('54400015'), cep_to_coords('54100715'), cep_to_coords('50730010'), cep_to_coords('52190313'), cep_to_coords('52050505'), cep_to_coords('50791690'), cep_to_coords('53417320'), cep_to_coords('54330600'), cep_to_coords('50070290'), cep_to_coords('54240605'), cep_to_coords('50970300'), cep_to_coords('53433220'), cep_to_coords('53370780'), cep_to_coords('53060500'), cep_to_coords('53260200'), cep_to_coords('50610360'), cep_to_coords('52120020'), cep_to_coords('52120240'), cep_to_coords('50830170'), cep_to_coords('50761680'), cep_to_coords('50710465'), cep_to_coords('53000200'), cep_to_coords('55400000'), cep_to_coords('50610400'), cep_to_coords('52191230'), cep_to_coords('56912170'), cep_to_coords('50800220'), cep_to_coords('50761470'), cep_to_coords('55190000'), cep_to_coords('53070420'), cep_to_coords('54440280'), cep_to_coords('54440260'), cep_to_coords('54410310'), cep_to_coords('53417470'), cep_to_coords('53060110'), cep_to_coords('53220140'), cep_to_coords('54230032'), cep_to_coords('50731225'), cep_to_coords('52031210'), cep_to_coords('55819640'), cep_to_coords('53570120'), cep_to_coords('54270320'), cep_to_coords('52071000'), cep_to_coords('51020180'), cep_to_coords('51113000'), cep_to_coords('53409711'), cep_to_coords('53050150'), cep_to_coords('50731025'), cep_to_coords('53423210'), cep_to_coords('52070500'), cep_to_coords('50960060'), cep_to_coords('54740000'), cep_to_coords('51020021'), cep_to_coords('52240620'), cep_to_coords('50610410'), cep_to_coords('52081000'), cep_to_coords('53433010'), cep_to_coords('54240020'), cep_to_coords('51220000'), cep_to_coords('50741020'), cep_to_coords('52080360'), cep_to_coords('50630200'), cep_to_coords('56912120'), cep_to_coords('56912140'), cep_to_coords('54513605'), cep_to_coords('54460040'), cep_to_coords('53431820'), cep_to_coords('54000500'), cep_to_coords('52051345'), cep_to_coords('51020240'), cep_to_coords('50720000'), cep_to_coords('52070460'), cep_to_coords('55825100'), cep_to_coords('54705365'), cep_to_coords('53433020'), cep_to_coords('52010065'), cep_to_coords('52120193'), cep_to_coords('50770660'), cep_to_coords('55409000'), cep_to_coords('51335496'), cep_to_coords('52061512'), cep_to_coords('51320430'), cep_to_coords('51170140'), cep_to_coords('51170410'), cep_to_coords('50740370'), cep_to_coords('50710440'), cep_to_coords('51240740'), cep_to_coords('53270305'), cep_to_coords('53260630'), cep_to_coords('55430000'), cep_to_coords('50760195'), cep_to_coords('50730130'), cep_to_coords('50690230'), cep_to_coords('53530221'), cep_to_coords('53437470'), cep_to_coords('53120420'), cep_to_coords('50820050'), cep_to_coords('52020212'), cep_to_coords('52020030'), cep_to_coords('50650300'), cep_to_coords('53050030'), cep_to_coords('53401410'), cep_to_coords('52021050'), cep_to_coords('52280500'), cep_to_coords('52071640'), cep_to_coords('50670490'), cep_to_coords('54400140'), cep_to_coords('54409500'), cep_to_coords('51011150'), cep_to_coords('50731470'), cep_to_coords('52061200'), cep_to_coords('50870140'), cep_to_coords('55018210'), cep_to_coords('54460090'), cep_to_coords('52190450'), cep_to_coords('53130340'), cep_to_coords('52191170'), cep_to_coords('54730040'), cep_to_coords('53421030'), cep_to_coords('52120370'), cep_to_coords('50650110'), cep_to_coords('50650030'), cep_to_coords('52121380'), cep_to_coords('53050182'), cep_to_coords('54335160'), cep_to_coords('52121370'), cep_to_coords('53130210'), cep_to_coords('52490010'), cep_to_coords('52120450'), cep_to_coords('52071183'), cep_to_coords('50791467'), cep_to_coords('52211320'), cep_to_coords('54765335'), cep_to_coords('53620520'), cep_to_coords('55592000'), cep_to_coords('51030340'), cep_to_coords('51350290'), cep_to_coords('51011240'), cep_to_coords('52140420'), cep_to_coords('53620095'), cep_to_coords('53150030'), cep_to_coords('50680540'), cep_to_coords('53050260'), cep_to_coords('52130110'), cep_to_coords('52130510'), cep_to_coords('51190460'), cep_to_coords('54505610'), cep_to_coords('50740030'), cep_to_coords('50610140'), cep_to_coords('53433690'), cep_to_coords('50741400'), cep_to_coords('54765115'), cep_to_coords('54120190'), cep_to_coords('50110060'), cep_to_coords('53110460'), cep_to_coords('53160800'), cep_to_coords('53415310'), cep_to_coords('53140120'), cep_to_coords('50800110'), cep_to_coords('52130215'), cep_to_coords('53625105'), cep_to_coords('53350220'), cep_to_coords('52221050'), cep_to_coords('52160240'), cep_to_coords('51020060'), cep_to_coords('56318070'), cep_to_coords('53530474'), cep_to_coords('52280106'), cep_to_coords('50712170'), cep_to_coords('00001111'), cep_to_coords('50751550'), cep_to_coords('54768796'), cep_to_coords('52221300'), cep_to_coords('51030215'), cep_to_coords('51011060'), cep_to_coords('54325720'), cep_to_coords('51270300'), cep_to_coords('53150500'), cep_to_coords('51180030'), cep_to_coords('56309150'), cep_to_coords('50640410'), cep_to_coords('53409280'), cep_to_coords('53530468'), cep_to_coords('54730080'), cep_to_coords('53439170'), cep_to_coords('50741000'), cep_to_coords('52131063'), cep_to_coords('53270275'), cep_to_coords('53010450'), cep_to_coords('55008020'), cep_to_coords('55024810'), cep_to_coords('53130080'), cep_to_coords('51010018'), cep_to_coords('53270160'), cep_to_coords(': 50630170'), cep_to_coords('56870000'), cep_to_coords('53433570'), cep_to_coords('50630170'), cep_to_coords('51111030'), cep_to_coords('52060165'), cep_to_coords('52081170'), cep_to_coords('56321625'), cep_to_coords('51130570'), cep_to_coords('53110450'), cep_to_coords('50100350'), cep_to_coords('53300300'), cep_to_coords('50741380'), cep_to_coords('50741390'), cep_to_coords('54270080'), cep_to_coords('54705475'), cep_to_coords('54100540'), cep_to_coords('51170570'), cep_to_coords('50920360'), cep_to_coords('54100434'), cep_to_coords('54505000'), cep_to_coords('54519160'), cep_to_coords('54240210'), cep_to_coords('52060290'), cep_to_coords('53442160'), cep_to_coords('50030150'), cep_to_coords('50761740'), cep_to_coords('51021520'), cep_to_coords('52291165'), cep_to_coords('52041170'), cep_to_coords('53405817'), cep_to_coords('53290170'), cep_to_coords('51028170'), cep_to_coords('50780510'), cep_to_coords('53444480'), cep_to_coords('53435480'), cep_to_coords('54753680'), cep_to_coords('50800310'), cep_to_coords('50789000'), cep_to_coords('50780300'), cep_to_coords('56828000'), cep_to_coords('56950000'), cep_to_coords('52020025'), cep_to_coords('52280140'), cep_to_coords('53437320'), cep_to_coords('53050040'), cep_to_coords('50830545'), cep_to_coords('50870415'), cep_to_coords('50960090'), cep_to_coords('55046640'), cep_to_coords('54360020'), cep_to_coords('50711112'), cep_to_coords('51310000'), cep_to_coords('53443160'), cep_to_coords('55480000'), cep_to_coords('53250280'), cep_to_coords('52041017'), cep_to_coords('52111310'), cep_to_coords('54470050'), cep_to_coords('54325190'), cep_to_coords('54505090'), cep_to_coords('53210180'), cep_to_coords('50900121'), cep_to_coords('50780010'), cep_to_coords('51011025'), cep_to_coords('53350200'), cep_to_coords('54753400'), cep_to_coords('50750180'), cep_to_coords('54360103'), cep_to_coords('50761625'), cep_to_coords('55473970'), cep_to_coords('55470000'), cep_to_coords('50050000'), cep_to_coords('52210001'), cep_to_coords('56308150'), cep_to_coords('53433700'), cep_to_coords('50630060'), cep_to_coords('50721490'), cep_to_coords('54368060'), cep_to_coords('54360060'), cep_to_coords('53110027'), cep_to_coords('52041090'), cep_to_coords('52070040'), cep_to_coords('54240140'), cep_to_coords('52010210'), cep_to_coords('52211600'), cep_to_coords('55604200'), cep_to_coords('50740120'), cep_to_coords('54490174'), cep_to_coords('50761600'), cep_to_coords('50720180'), cep_to_coords('50711280'), cep_to_coords('50791040'), cep_to_coords('54771000'), cep_to_coords('52280680'), cep_to_coords('55180000'), cep_to_coords('53442120'), cep_to_coords('53080220'), cep_to_coords('50790200'), cep_to_coords('53635610'), cep_to_coords('53441320'), cep_to_coords('50610180'), cep_to_coords('53417270'), cep_to_coords('50791030'), cep_to_coords('53530470'), cep_to_coords('52111130'), cep_to_coords('53435340'), cep_to_coords('43535340'), cep_to_coords('54315310'), cep_to_coords('54170370'), cep_to_coords('54120052'), cep_to_coords('50870280'), cep_to_coords('55298165'), cep_to_coords('53413136'), cep_to_coords('50610340'), cep_to_coords('53620280'), cep_to_coords('52131320'), cep_to_coords('53441070'), cep_to_coords('53421805'), cep_to_coords('52021110'), cep_to_coords('54786010'), cep_to_coords('54737120'), cep_to_coords('50761020'), cep_to_coords('50980427'), cep_to_coords('51320490'), cep_to_coords('51030300'), cep_to_coords('51111210'), cep_to_coords('52291640'), cep_to_coords('53405310'), cep_to_coords('51111011'), cep_to_coords('52070381'), cep_to_coords('50711300'), cep_to_coords('52111520'), cep_to_coords('51000330'), cep_to_coords('52050240'), cep_to_coords('55815206'), cep_to_coords('54530170'), cep_to_coords('53540130'), cep_to_coords('53530482'), cep_to_coords('54360153'), cep_to_coords('53402165'), cep_to_coords('52041065'), cep_to_coords('51345051'), cep_to_coords('50720160'), cep_to_coords('53400990'), cep_to_coords('52490120'), cep_to_coords('50820190'), cep_to_coords('50630190'), cep_to_coords('50920200'), cep_to_coords('52280110'), cep_to_coords('52091192'), cep_to_coords('54490011'), cep_to_coords('54445011'), cep_to_coords('55530000'), cep_to_coords('53413610'), cep_to_coords('53090350'), cep_to_coords('53080350'), cep_to_coords('50920700'), cep_to_coords('54420220'), cep_to_coords('50791130'), cep_to_coords('52211590'), cep_to_coords('54720020'), cep_to_coords('54720195'), cep_to_coords('54330560'), cep_to_coords('53220500'), cep_to_coords('53360320'), cep_to_coords('54715706'), cep_to_coords('50731050'), cep_to_coords('54315320'), cep_to_coords('52211040'), cep_to_coords('52051130'), cep_to_coords('50751110'), cep_to_coords('51260520'), cep_to_coords('53260300'), cep_to_coords('52121170'), cep_to_coords('52021395'), cep_to_coords('50740180'), cep_to_coords('52090860'), cep_to_coords('51021220'), cep_to_coords('53370269'), cep_to_coords('53437390'), cep_to_coords('53090500'), cep_to_coords('53140060'), cep_to_coords('50771450'), cep_to_coords('50980061'), cep_to_coords('55158800'), cep_to_coords('50730250'), cep_to_coords('52050070'), cep_to_coords('52221160'), cep_to_coords('54270170'), cep_to_coords('54280470'), cep_to_coords('50721520'), cep_to_coords('53360470'), cep_to_coords('52071140'), cep_to_coords('51280000'), cep_to_coords('52050340'), cep_to_coords('50761062'), cep_to_coords('50650170'), cep_to_coords('52020214'), cep_to_coords('50070460'), cep_to_coords('52080281'), cep_to_coords('50791300'), cep_to_coords('53421341'), cep_to_coords('53435600'), cep_to_coords('53210380'), cep_to_coords('53230290'), cep_to_coords('53240290'), cep_to_coords('53180080'), cep_to_coords('53040140'), cep_to_coords('52040190'), cep_to_coords('51330140'), cep_to_coords('52160796'), cep_to_coords('52111650'), cep_to_coords('50110360'), cep_to_coords('52211110'), cep_to_coords('50640130'), cep_to_coords('52051281'), cep_to_coords('52061180'), cep_to_coords('52221005'), cep_to_coords('50791465'), cep_to_coords('53080390'), cep_to_coords('53409570'), cep_to_coords('53402660'), cep_to_coords('54340795'), cep_to_coords('53425750'), cep_to_coords('53050077'), cep_to_coords('50610430'), cep_to_coords('50090700'), cep_to_coords('52211550'), cep_to_coords('50710001'), cep_to_coords('55602970'), cep_to_coords('50870550'), cep_to_coords('52051310'), cep_to_coords('50910151'), cep_to_coords('50710430'), cep_to_coords('54320100'), cep_to_coords('54310275'), cep_to_coords('55612195'), cep_to_coords('54400390'), cep_to_coords('54759090'), cep_to_coords('53260010'), cep_to_coords('51180100'), cep_to_coords('51150100'), cep_to_coords('51030330'), cep_to_coords('51021090'), cep_to_coords('52130301'), cep_to_coords('51325280'), cep_to_coords('51027400'), cep_to_coords('53605700'), cep_to_coords('52030020'), cep_to_coords('53441580'), cep_to_coords('51350380'), cep_to_coords('50800250'), cep_to_coords('52140160'), cep_to_coords('53140160'), cep_to_coords('54140160'), cep_to_coords('54240270'), cep_to_coords('53401200'), cep_to_coords('53429060'), cep_to_coords('53350180'), cep_to_coords('52051340'), cep_to_coords('50910535'), cep_to_coords('50920600'), cep_to_coords('53110290'), cep_to_coords('54080061'), cep_to_coords('51230000'), cep_to_coords('52110580'), cep_to_coords('52110460'), cep_to_coords('50920370'), cep_to_coords('50930010'), cep_to_coords('52030172'), cep_to_coords('52081520'), cep_to_coords('52050005'), cep_to_coords('53110295'), cep_to_coords('52091530'), cep_to_coords('53240220'), cep_to_coords('55292780'), cep_to_coords('50680200'), cep_to_coords('52165030'), cep_to_coords('51010080'), cep_to_coords('51010140'), cep_to_coords('54250000'), cep_to_coords('54330610'), cep_to_coords('51021110'), cep_to_coords('55295355'), cep_to_coords('55293120'), cep_to_coords('56400000'), cep_to_coords('53300070'), cep_to_coords('51190740'), cep_to_coords('51290030'), cep_to_coords('54160575'), cep_to_coords('50760220'), cep_to_coords('50720575'), cep_to_coords('53415140'), cep_to_coords('50050120'), cep_to_coords('56330015'), cep_to_coords('52131090'), cep_to_coords('51170300'), cep_to_coords('53150311'), cep_to_coords('50060630'), cep_to_coords('54768160'), cep_to_coords('55920000'), cep_to_coords('54240415'), cep_to_coords('50900100'), cep_to_coords('50740400'), cep_to_coords('51260040'), cep_to_coords('50670230'), cep_to_coords('52090262'), cep_to_coords('53530000'), cep_to_coords('50830260'), cep_to_coords('54520320'), cep_to_coords('54470260'), cep_to_coords('53405313'), cep_to_coords('53409650'), cep_to_coords('54400450'), cep_to_coords('51190670'), cep_to_coords('52211250'), cep_to_coords('52280025'), cep_to_coords('53421450'), cep_to_coords('50720585'), cep_to_coords('52280205'), cep_to_coords('50761050'), cep_to_coords('50761530'), cep_to_coords('50770490'), cep_to_coords('50879470'), cep_to_coords('51010070'), cep_to_coords('54774403'), cep_to_coords('50620460'), cep_to_coords('52040360'), cep_to_coords('53620692'), cep_to_coords('52160030'), cep_to_coords('56509420'), cep_to_coords('55818620'), cep_to_coords('55813420'), cep_to_coords('56510120'), cep_to_coords('54768650'), cep_to_coords('53525310'), cep_to_coords('50080320'), cep_to_coords('53370160'), cep_to_coords('52171111'), cep_to_coords('55602030'), cep_to_coords('54330520'), cep_to_coords('54440110'), cep_to_coords('54400110'), cep_to_coords('52091210'), cep_to_coords('52130347'), cep_to_coords('50850410'), cep_to_coords('53610320'), cep_to_coords('53442010'), cep_to_coords('55565000'), cep_to_coords('54210545'), cep_to_coords('54735490'), cep_to_coords('55040000'), cep_to_coords('53040000'), cep_to_coords('52070200'), cep_to_coords('50741430'), cep_to_coords('52210320'), cep_to_coords('53640620'), cep_to_coords('50751375'), cep_to_coords('52280325'), cep_to_coords('50940040'), cep_to_coords('52490008'), cep_to_coords('53610017'), cep_to_coords('53417450'), cep_to_coords('53230710'), cep_to_coords('53210460'), cep_to_coords('53580135'), cep_to_coords('54460350'), cep_to_coords('54753330'), cep_to_coords('53080470'), cep_to_coords('52130220'), cep_to_coords('50771555'), cep_to_coords('52061055'), cep_to_coords('52061165'), cep_to_coords('54320010'), cep_to_coords('52061275'), cep_to_coords('53280130'), cep_to_coords('50721180'), cep_to_coords('54768415'), cep_to_coords('50920020'), cep_to_coords('56328160'), cep_to_coords('50980380'), cep_to_coords('42130140'), cep_to_coords('51030000'), cep_to_coords('52280100'), cep_to_coords('55010480'), cep_to_coords('53409500'), cep_to_coords('53260160'), cep_to_coords('53401585'), cep_to_coords('53260640'), cep_to_coords('54315010'), cep_to_coords('53429550'), cep_to_coords('52061450'), cep_to_coords('50730000'), cep_to_coords('50060010'), cep_to_coords('50070070'), cep_to_coords('51300000'), cep_to_coords('50771620'), cep_to_coords('52291230'), cep_to_coords('50721250'), cep_to_coords('55612520'), cep_to_coords('51345000'), cep_to_coords('70459000'), cep_to_coords('51240735'), cep_to_coords('52051110'), cep_to_coords('52041325'), cep_to_coords('51011400'), cep_to_coords('51030560'), cep_to_coords('51170120'), cep_to_coords('50790425'), cep_to_coords('52061400'), cep_to_coords('51010230'), cep_to_coords('54280220'), cep_to_coords('53130555'), cep_to_coords('53431010'), cep_to_coords('53040110'), cep_to_coords('53090360'), cep_to_coords('53140290'), cep_to_coords('52120720'), cep_to_coords('51250110'), cep_to_coords('52071430'), cep_to_coords('50761675'), cep_to_coords('51300060'), cep_to_coords('50050215'), cep_to_coords('51020480'), cep_to_coords('50640200'), cep_to_coords('53370220'), cep_to_coords('54580554'), cep_to_coords('52031151'), cep_to_coords('53415260'), cep_to_coords('50791232'), cep_to_coords('50791230'), cep_to_coords('52060180'), cep_to_coords('55400090'), cep_to_coords('51190140'), cep_to_coords('52160180'), cep_to_coords('54715340'), cep_to_coords('50100260'), cep_to_coords('54330580'), cep_to_coords('50040180'), cep_to_coords('50761250'), cep_to_coords('52131541'), cep_to_coords('51170145'), cep_to_coords('52160236'), cep_to_coords('50720750'), cep_to_coords('53240444'), cep_to_coords('53407260'), cep_to_coords('53431040'), cep_to_coords('54290595'), cep_to_coords('50690450'), cep_to_coords('52061170'), cep_to_coords('50690540'), cep_to_coords('50620481'), cep_to_coords('53433460'), cep_to_coords('55614735'), cep_to_coords('51150040'), cep_to_coords('51230010'), cep_to_coords('52051450'), cep_to_coords('50040560'), cep_to_coords('24121965'), cep_to_coords('52221010'), cep_to_coords('54589555'), cep_to_coords('54340518'), cep_to_coords('51345030'), cep_to_coords('50960150'), cep_to_coords('52131270'), cep_to_coords('50790290'), cep_to_coords('54160454'), cep_to_coords('55630370'), cep_to_coords('53330170'), cep_to_coords('55298690'), cep_to_coords('50030230'), cep_to_coords('55006100'), cep_to_coords('50040010'), cep_to_coords('53417000'), cep_to_coords('50731030'), cep_to_coords('53060180'), cep_to_coords('53350854'), cep_to_coords('53640194'), cep_to_coords('53625285'), cep_to_coords('53610351'), cep_to_coords('53610970'), cep_to_coords('51260110'), cep_to_coords('54250520'), cep_to_coords('54325160'), cep_to_coords('51240030'), cep_to_coords('54320130'), cep_to_coords('51250025'), cep_to_coords('50770000'), cep_to_coords('52091153'), cep_to_coords('54753090'), cep_to_coords('53170780'), cep_to_coords('54270110'), cep_to_coords('52211012'), cep_to_coords('54320060'), cep_to_coords('51320160'), cep_to_coords('54470250'), cep_to_coords('52090320'), cep_to_coords('54270060'), cep_to_coords('50790108'), cep_to_coords('51630060'), cep_to_coords('53290100'), cep_to_coords('53140240'), cep_to_coords('50791110'), cep_to_coords('50060001'), cep_to_coords('50900460'), cep_to_coords('55950000'), cep_to_coords('53210260'), cep_to_coords('53240140'), cep_to_coords('56509500'), cep_to_coords('50791381'), cep_to_coords('50050245'), cep_to_coords('54517270'), cep_to_coords('50610440'), cep_to_coords('55612480'), cep_to_coords('54735200'), cep_to_coords('53630735'), cep_to_coords('53520200'), cep_to_coords('53525560'), cep_to_coords('54780080'), cep_to_coords('52070490'), cep_to_coords('50751000'), cep_to_coords('53444501'), cep_to_coords('55700000'), cep_to_coords('54210466'), cep_to_coords('54440130'), cep_to_coords('54280061'), cep_to_coords('53460390'), cep_to_coords('55602280'), cep_to_coords('50720720'), cep_to_coords('50910420'), cep_to_coords('50690735'), cep_to_coords('56509180'), cep_to_coords('56512530'), cep_to_coords('56512790'), cep_to_coords('53424080'), cep_to_coords('53630705'), cep_to_coords('50870380'), cep_to_coords('53439460'), cep_to_coords('52015300'), cep_to_coords('53090045'), cep_to_coords('54774390'), cep_to_coords('51011000'), cep_to_coords('55034190'), cep_to_coords('53441290'), cep_to_coords('51310280'), cep_to_coords('50050510'), cep_to_coords('51150570'), cep_to_coords('53560105'), cep_to_coords('53403780'), cep_to_coords('53230630'), cep_to_coords('56328390'), cep_to_coords('53635565'), cep_to_coords('53431145'), cep_to_coords('54765400'), cep_to_coords('50810000'), cep_to_coords('50710380'), cep_to_coords('51020230'), cep_to_coords('53635110'), cep_to_coords('53130260'), cep_to_coords('51170280'), cep_to_coords('51170100'), cep_to_coords('55140000'), cep_to_coords('52120420'), cep_to_coords('50060110'), cep_to_coords('51020030'), cep_to_coords('50820240'), cep_to_coords('53220261'), cep_to_coords('52120210'), cep_to_coords('52140060'), cep_to_coords('51190110'), cep_to_coords('52050660'), cep_to_coords('52050100'), cep_to_coords('53220330'), cep_to_coords('54270334'), cep_to_coords('52191180'), cep_to_coords('50740130'), cep_to_coords('50470130'), cep_to_coords('52280367'), cep_to_coords('50900490'), cep_to_coords('52111460'), cep_to_coords('51250545'), cep_to_coords('53266040'), cep_to_coords('54783170'), cep_to_coords('54230690'), cep_to_coords('54768220'), cep_to_coords('54765090'), cep_to_coords('51290320'), cep_to_coords('53130470'), cep_to_coords('52120303'), cep_to_coords('52041270'), cep_to_coords('50771405'), cep_to_coords('52021355'), cep_to_coords('51190410'), cep_to_coords('52211020'), cep_to_coords('52111330'), cep_to_coords('54310180'), cep_to_coords('50610170'), cep_to_coords('50781760'), cep_to_coords('53423590'), cep_to_coords('54325760'), cep_to_coords('52120080'), cep_to_coords('50040280'), cep_to_coords('54345590'), cep_to_coords('54400090'), cep_to_coords('52051160'), cep_to_coords('50771480'), cep_to_coords('50630210'), cep_to_coords('54404010'), cep_to_coords('53290370'), cep_to_coords('53330420'), cep_to_coords('54753340'), cep_to_coords('54330205'), cep_to_coords('54768150'), cep_to_coords('50630010'), cep_to_coords('52280230'), cep_to_coords('52041020'), cep_to_coords('53080730'), cep_to_coords('51020270'), cep_to_coords('50761370'), cep_to_coords('51020070'), cep_to_coords('50730040'), cep_to_coords('50731636'), cep_to_coords('51230070'), cep_to_coords('52051360'), cep_to_coords('54756000'), cep_to_coords('53370090'), cep_to_coords('55022180'), cep_to_coords('55022200'), cep_to_coords('53230560'), cep_to_coords('51130320'), cep_to_coords('51270420'), cep_to_coords('50750165'), cep_to_coords('51190130'), cep_to_coords('54280244'), cep_to_coords('53270250'), cep_to_coords('50740450'), cep_to_coords('52080050'), cep_to_coords('50690120'), cep_to_coords('53439200'), cep_to_coords('54410500'), cep_to_coords('52041042'), cep_to_coords('54220353'), cep_to_coords('52050130'), cep_to_coords('52280401'), cep_to_coords('54410130'), cep_to_coords('55038010'), cep_to_coords('55018040'), cep_to_coords('55299390'), cep_to_coords('53060475'), cep_to_coords('53050220'), cep_to_coords('53050130'), cep_to_coords('50670150'), cep_to_coords('50721480'), cep_to_coords('55120000'), cep_to_coords('55034460'), cep_to_coords('55012640'), cep_to_coords('55036120'), cep_to_coords('53625015'), cep_to_coords('50100250'), cep_to_coords('55032555'), cep_to_coords('54535230'), cep_to_coords('54520615'), cep_to_coords('52060140'), cep_to_coords('54530105'), cep_to_coords('54330213'), cep_to_coords('50610030'), cep_to_coords('54410170'), cep_to_coords('50680680'), cep_to_coords('53420100'), cep_to_coords('53130590'), cep_to_coords('53040010'), cep_to_coords('54430090'), cep_to_coords('50070080'), cep_to_coords('52280102'), cep_to_coords('50850314'), cep_to_coords('50720730'), cep_to_coords('55880000'), cep_to_coords('50830510'), cep_to_coords('56512050'), cep_to_coords('50730020'), cep_to_coords('54470030'), cep_to_coords('53402560'), cep_to_coords('53370410'), cep_to_coords('55813435'), cep_to_coords('53370166'), cep_to_coords('50850080'), cep_to_coords('52050110'), cep_to_coords('51230368'), cep_to_coords('51010610'), cep_to_coords('53407460'), cep_to_coords('53407220'), cep_to_coords('53300270'), cep_to_coords('52011020'), cep_to_coords('53625290'), cep_to_coords('53439390'), cep_to_coords('53260210'), cep_to_coords('53150192'), cep_to_coords('51230090'), cep_to_coords('54350300'), cep_to_coords('55655000'), cep_to_coords('53090530'), cep_to_coords('51030380'), cep_to_coords('51030080'), cep_to_coords('50741110'), cep_to_coords('54720072'), cep_to_coords('52020195'), cep_to_coords('50780090'), cep_to_coords('55038281'), cep_to_coords('54430010'), cep_to_coords('52070420'), cep_to_coords('52011240'), cep_to_coords('50610545'), cep_to_coords('50731370'), cep_to_coords('53550661'), cep_to_coords('54330572'), cep_to_coords('53110550'), cep_to_coords('53110520'), cep_to_coords('53370100'), cep_to_coords('51021490'), cep_to_coords('50640440'), cep_to_coords('50740210'), cep_to_coords('53540120'), cep_to_coords('53320190'), cep_to_coords('50980010'), cep_to_coords('50751530'), cep_to_coords('53300220'), cep_to_coords('54280390'), cep_to_coords('53270025'), cep_to_coords('52120095'), cep_to_coords('52110380'), cep_to_coords('51021040'), cep_to_coords('55030265'), cep_to_coords('53210040'), cep_to_coords('53270320'), cep_to_coords('53441100'), cep_to_coords('53530715'), cep_to_coords('54315057'), cep_to_coords('50870760'), cep_to_coords('51130010'), cep_to_coords('50820410'), cep_to_coords('52130150'), cep_to_coords('52130095'), cep_to_coords('52090310'), cep_to_coords('51270070'), cep_to_coords('50620100'), cep_to_coords('52110490'), cep_to_coords('50050010'), cep_to_coords('50761690'), cep_to_coords('51030620'), cep_to_coords('55665000'), cep_to_coords('54170000'), cep_to_coords('53060820'), cep_to_coords('54440030'), cep_to_coords('53180020'), cep_to_coords('54325090'), cep_to_coords('53565381'), cep_to_coords('54220240'), cep_to_coords('53444150'), cep_to_coords('53444200'), cep_to_coords('54777500'), cep_to_coords('53280110'), cep_to_coords('52120040'), cep_to_coords('52190170'), cep_to_coords('50920660'), cep_to_coords('50910480'), cep_to_coords('54240150'), cep_to_coords('55490000'), cep_to_coords('55602650'), cep_to_coords('55606210'), cep_to_coords('50770500'), cep_to_coords('54320650'), cep_to_coords('51230360'), cep_to_coords('50910250'), cep_to_coords('50920680'), cep_to_coords('52091023'), cep_to_coords('52131532'), cep_to_coords('50731280'), cep_to_coords('51330270'), cep_to_coords('10503235'), cep_to_coords('54735133'), cep_to_coords('52060590'), cep_to_coords('53441310'), cep_to_coords('53421360'), cep_to_coords('54753440'), cep_to_coords('53580310'), cep_to_coords('54780310'), cep_to_coords('55022030'), cep_to_coords('55012312'), cep_to_coords('53421201'), cep_to_coords('53230460'), cep_to_coords('50680080'), cep_to_coords('53530450'), cep_to_coords('53530160'), cep_to_coords('50610510'), cep_to_coords('52110230'), cep_to_coords('50800090'), cep_to_coords('51330300'), cep_to_coords('50720270'), cep_to_coords('54420006'), cep_to_coords('53444490'), cep_to_coords('54762145'), cep_to_coords('53230280'), cep_to_coords('53350320'), cep_to_coords('53370420'), cep_to_coords('52071210'), cep_to_coords('51310090'), cep_to_coords('52040340'), cep_to_coords('54762125'), cep_to_coords('54762115'), cep_to_coords('54705400'), cep_to_coords('53270017'), cep_to_coords('51110180'), cep_to_coords('54325485'), cep_to_coords('52090475'), cep_to_coords('51011080'), cep_to_coords('51190420'), cep_to_coords('52031100'), cep_to_coords('50630600'), cep_to_coords('51130300'), cep_to_coords('51111010'), cep_to_coords('54320182'), cep_to_coords('54220180'), cep_to_coords('25030090'), cep_to_coords('50070170'), cep_to_coords('51350010'), cep_to_coords('53090110'), cep_to_coords('54100120'), cep_to_coords('53270307'), cep_to_coords('53403630'), cep_to_coords('53030200'), cep_to_coords('53415120'), cep_to_coords('51130220'), cep_to_coords('54406200'), cep_to_coords('50790340'), cep_to_coords('53200660'), cep_to_coords('52211150'), cep_to_coords('54440351'), cep_to_coords('51030660'), cep_to_coords('51160900'), cep_to_coords('52111160'), cep_to_coords('53240540'), cep_to_coords('53320440'), cep_to_coords('52050140'), cep_to_coords('53429560'), cep_to_coords('54460010'), cep_to_coords('53170624'), cep_to_coords('53560970'), cep_to_coords('53620840'), cep_to_coords('53610076'), cep_to_coords('53429080'), cep_to_coords('53080320'), cep_to_coords('53540400'), cep_to_coords('55030040'), cep_to_coords('51350610'), cep_to_coords('53461564'), cep_to_coords('56580000'), cep_to_coords('52031040'), cep_to_coords('54270171'), cep_to_coords('54270425'), cep_to_coords('50070000'), cep_to_coords('53090220'), cep_to_coords('50680290'), cep_to_coords('54430350'), cep_to_coords('52110220'), cep_to_coords('54310310'), cep_to_coords('50770300'), cep_to_coords('53230020'), cep_to_coords('53170375'), cep_to_coords('52121140'), cep_to_coords('50820420'), cep_to_coords('55608640'), cep_to_coords('50850020'), cep_to_coords('50770390'), cep_to_coords('54100450'), cep_to_coords('53437090'), cep_to_coords('54762300'), cep_to_coords('52010250'), cep_to_coords('54260220'), cep_to_coords('53431370'), cep_to_coords('54270200'), cep_to_coords('54737100'), cep_to_coords('53040480'), cep_to_coords('54120480'), cep_to_coords('53120281'), cep_to_coords('53410000'), cep_to_coords('53050080'), cep_to_coords('52120105'), cep_to_coords('50721100'), cep_to_coords('52770120'), cep_to_coords('55398000'), cep_to_coords('55578000'), cep_to_coords('53230260'), cep_to_coords('53570130'), cep_to_coords('53060791'), cep_to_coords('54740630'), cep_to_coords('53160650'), cep_to_coords('50740040'), cep_to_coords('53431060'), cep_to_coords('54753350'), cep_to_coords('50080240'), cep_to_coords('52131410'), cep_to_coords('53431300'), cep_to_coords('53444190'), cep_to_coords('50820250'), cep_to_coords('50760290'), cep_to_coords('54762022'), cep_to_coords('51320310'), cep_to_coords('91882915'), cep_to_coords('52051290'), cep_to_coords('50830550'), cep_to_coords('52390040'), cep_to_coords('51010378'), cep_to_coords('54330170'), cep_to_coords('50000060'), cep_to_coords('50060000'), cep_to_coords('50000740'), cep_to_coords('52211530'), cep_to_coords('50010090'), cep_to_coords('52125050'), cep_to_coords('52191098'), cep_to_coords('50721510'), cep_to_coords('50741450'), cep_to_coords('50100070'), cep_to_coords('53070070'), cep_to_coords('53370180'), cep_to_coords('53290200'), cep_to_coords('53417460'), cep_to_coords('53439420'), cep_to_coords('53433490'), cep_to_coords('50710180'), cep_to_coords('54720250'), cep_to_coords('50021020'), cep_to_coords('54270050'), cep_to_coords('53580351'), cep_to_coords('54300000'), cep_to_coords('56550000'), cep_to_coords('51280590'), cep_to_coords('50830410'), cep_to_coords('51270650'), cep_to_coords('50731420'), cep_to_coords('53220360'), cep_to_coords('53140170'), cep_to_coords('53020630'), cep_to_coords('52011110'), cep_to_coords('50670340'), cep_to_coords('31310180'), cep_to_coords('52041541'), cep_to_coords('50870235'), cep_to_coords('50875230'), cep_to_coords('51275175'), cep_to_coords('51320250'), cep_to_coords('50650040'), cep_to_coords('52061360'), cep_to_coords('54444029'), cep_to_coords('54490126'), cep_to_coords('53220300'), cep_to_coords('54220716'), cep_to_coords('53250550'), cep_to_coords('52060030'), cep_to_coords('52031080'), cep_to_coords('50980495'), cep_to_coords('51011100'), cep_to_coords('54753630'), cep_to_coords('53410130'), cep_to_coords('05010820'), cep_to_coords('54140181'), cep_to_coords('54120360'), cep_to_coords('50760550'), cep_to_coords('52081550'), cep_to_coords('51190000'), cep_to_coords('54390071'), cep_to_coords('51490071'), cep_to_coords('54490675'), cep_to_coords('53320220'), cep_to_coords('53280060'), cep_to_coords('54410460'), cep_to_coords('53190001'), cep_to_coords('50721365'), cep_to_coords('50820120'), cep_to_coords('51170400'), cep_to_coords('54470757'), cep_to_coords('54470575'), cep_to_coords('54768215'), cep_to_coords('54774310'), cep_to_coords('56306050'), cep_to_coords('52140221'), cep_to_coords('50920640'), cep_to_coords('54400400'), cep_to_coords('54280744'), cep_to_coords('54753220'), cep_to_coords('50741010'), cep_to_coords('52211540'), cep_to_coords('54090393'), cep_to_coords('53080200'), cep_to_coords('51350000'), cep_to_coords('53530270'), cep_to_coords('53130400'), cep_to_coords('53160050'), cep_to_coords('51011290'), cep_to_coords('55299387'), cep_to_coords('53130010'), cep_to_coords('53250355'), cep_to_coords('53210010'), cep_to_coords('53370500'), cep_to_coords('52210415'), cep_to_coords('52210190'), cep_to_coords('52150105'), cep_to_coords('53270090'), cep_to_coords('52070491'), cep_to_coords('54580170'), cep_to_coords('54768000'), cep_to_coords('54756230'), cep_to_coords('54150540'), cep_to_coords('54230175'), cep_to_coords('50761710'), cep_to_coords('54310090'), cep_to_coords('54735030'), cep_to_coords('51180045'), cep_to_coords('50780231'), cep_to_coords('53620630'), cep_to_coords('54170050'), cep_to_coords('50920500'), cep_to_coords('54580300'), cep_to_coords('50850360'), cep_to_coords('54525260'), cep_to_coords('51240290'), cep_to_coords('52131140'), cep_to_coords('54500001'), cep_to_coords('51190575'), cep_to_coords('50820300'), cep_to_coords('51110080'), cep_to_coords('52040300'), cep_to_coords('50070350'), cep_to_coords('52051300'), cep_to_coords('53610071'), cep_to_coords('53330360'), cep_to_coords('52090755'), cep_to_coords('51020390'), cep_to_coords('53610270'), cep_to_coords('54410270'), cep_to_coords('50670126'), cep_to_coords('53409610'), cep_to_coords('50910260'), cep_to_coords('50980765'), cep_to_coords('52061141'), cep_to_coords('53441200'), cep_to_coords('55813530'), cep_to_coords('55813380'), cep_to_coords('50610160'), cep_to_coords('51350040'), cep_to_coords('53580400'), cep_to_coords('54515630'), cep_to_coords('54430170'), cep_to_coords('53250270'), cep_to_coords('50050070'), cep_to_coords('50630770'), cep_to_coords('53290120'), cep_to_coords('53140030'), cep_to_coords('52070501'), cep_to_coords('50761010'), cep_to_coords('52190515'), cep_to_coords('51170500'), cep_to_coords('52071110'), cep_to_coords('53401635'), cep_to_coords('55611437'), cep_to_coords('53013003'), cep_to_coords('53130030'), cep_to_coords('53120360'), cep_to_coords('54786230'), cep_to_coords('54535160'), cep_to_coords('53435000'), cep_to_coords('54705180'), cep_to_coords('54505080'), cep_to_coords('55027210'), cep_to_coords('53020580'), cep_to_coords('54430331'), cep_to_coords('55570000'), cep_to_coords('50721040'), cep_to_coords('56480000'), cep_to_coords('54470210'), cep_to_coords('54330675'), cep_to_coords('50940600'), cep_to_coords('55525000'), cep_to_coords('54505470'), cep_to_coords('54510450'), cep_to_coords('54759360'), cep_to_coords('54753310'), cep_to_coords('50761280'), cep_to_coords('51283080'), cep_to_coords('53409140'), cep_to_coords('52000013'), cep_to_coords('52020213'), cep_to_coords('42803853'), cep_to_coords('51010040'), cep_to_coords('53435210'), cep_to_coords('54420310'), cep_to_coords('54400100'), cep_to_coords('54400080'), cep_to_coords('52011180'), cep_to_coords('50930000'), cep_to_coords('53409335'), cep_to_coords('54420030'), cep_to_coords('51130090'), cep_to_coords('54360160'), cep_to_coords('30100020'), cep_to_coords('54580415'), cep_to_coords('52291021'), cep_to_coords('50020080'), cep_to_coords('52131170'), cep_to_coords('54325670'), cep_to_coords('54290541'), cep_to_coords('54420490'), cep_to_coords('54530470'), cep_to_coords('50731480'), cep_to_coords('51030110'), cep_to_coords('50452526'), cep_to_coords('51260090'), cep_to_coords('55535000'), cep_to_coords('50020240'), cep_to_coords('50110500'), cep_to_coords('56509540'), cep_to_coords('55150260'), cep_to_coords('50100180'), cep_to_coords('53422580'), cep_to_coords('54310200'), cep_to_coords('51270270'), cep_to_coords('52211300'), cep_to_coords('53409150'), cep_to_coords('50900110'), cep_to_coords('53437848'), cep_to_coords('53240670'), cep_to_coords('52050040'), cep_to_coords('55819740'), cep_to_coords('54140380'), cep_to_coords('53422130'), cep_to_coords('53300280'), cep_to_coords('53370050'), cep_to_coords('50720280'), cep_to_coords('50110065'), cep_to_coords('53370440'), cep_to_coords('54431600'), cep_to_coords('53421300'), cep_to_coords('51030700'), cep_to_coords('53210150'), cep_to_coords('55614077'), cep_to_coords('51280420'), cep_to_coords('52140000'), cep_to_coords('54510360'), cep_to_coords('53407670'), cep_to_coords('53435140'), cep_to_coords('50100020'), cep_to_coords('50720130'), cep_to_coords('54325500'), cep_to_coords('54759646'), cep_to_coords('54100090'), cep_to_coords('53320310'), cep_to_coords('50920690'), cep_to_coords('54535080'), cep_to_coords('53439380'), cep_to_coords('52061460'), cep_to_coords('50920350'), cep_to_coords('53360490'), cep_to_coords('54260240'), cep_to_coords('54720190'), cep_to_coords('55770000'), cep_to_coords('53409780'), cep_to_coords('54120272'), cep_to_coords('51350250'), cep_to_coords('52060451'), cep_to_coords('52060450'), cep_to_coords('52190130'), cep_to_coords('53010070'), cep_to_coords('52051175'), cep_to_coords('55012700'), cep_to_coords('50710375'), cep_to_coords('65658000'), cep_to_coords('50091051'), cep_to_coords('50670570'), cep_to_coords('54090330'), cep_to_coords('53020380'), cep_to_coords('50960030'), cep_to_coords('52210100'), cep_to_coords('53270000'), cep_to_coords('52120490'), cep_to_coords('53050452'), cep_to_coords('52021020'), cep_to_coords('55814060'), cep_to_coords('56912430'), cep_to_coords('53422210'), cep_to_coords('52030280'), cep_to_coords('50761450'), cep_to_coords('50731300'), cep_to_coords('51350300'), cep_to_coords('54080260'), cep_to_coords('54470280'), cep_to_coords('55608251'), cep_to_coords('54230202'), cep_to_coords('55405000'), cep_to_coords('56306010'), cep_to_coords('54350220'), cep_to_coords('53417310'), cep_to_coords('55715000'), cep_to_coords('52110570'), cep_to_coords('51030390'), cep_to_coords('54116059'), cep_to_coords('51111190'), cep_to_coords('52120600'), cep_to_coords('56512520'), cep_to_coords('50790010'), cep_to_coords('50711120'), cep_to_coords('51100060'), cep_to_coords('50620520'), cep_to_coords('55018990'), cep_to_coords('53402390'), cep_to_coords('51110160'), cep_to_coords('50771765'), cep_to_coords('54470000'), cep_to_coords('54120130'), cep_to_coords('53620450'), cep_to_coords('51330430'), cep_to_coords('50690745'), cep_to_coords('51270620'), cep_to_coords('54160449'), cep_to_coords('54270070'), cep_to_coords('53419650'), cep_to_coords('54070120'), cep_to_coords('52111430'), cep_to_coords('50875132'), cep_to_coords('54495180'), cep_to_coords('52120250'), cep_to_coords('51021170'), cep_to_coords('50720139'), cep_to_coords('52010902'), cep_to_coords('50630640'), cep_to_coords('55809560'), cep_to_coords('50920280'), cep_to_coords('50920670'), cep_to_coords('53170125'), cep_to_coords('53620721'), cep_to_coords('53403120'), cep_to_coords('50761085'), cep_to_coords('54450190'), cep_to_coords('54100415'), cep_to_coords('50740705'), cep_to_coords('54410160'), cep_to_coords('54720794'), cep_to_coords('54735390'), cep_to_coords('52114300'), cep_to_coords('53170015'), cep_to_coords('52190292'), cep_to_coords('52140340'), cep_to_coords('50751555'), cep_to_coords('55027110'), cep_to_coords('53160740'), cep_to_coords('54240630'), cep_to_coords('53570111'), cep_to_coords('53403285'), cep_to_coords('50930240'), cep_to_coords('54350010'), cep_to_coords('54705378'), cep_to_coords('53610350'), cep_to_coords('53360300'), cep_to_coords('54580380'), cep_to_coords('54580000'), cep_to_coords('50070410'), cep_to_coords('51220030'), cep_to_coords('50731531'), cep_to_coords('51230110'), cep_to_coords('54735340'), cep_to_coords('54280360'), cep_to_coords('50010020'), cep_to_coords('51340250'), cep_to_coords('51150590'), cep_to_coords('54275010'), cep_to_coords('54737040'), cep_to_coords('53050000'), cep_to_coords('54360066'), cep_to_coords('54080050'), cep_to_coords('52071405'), cep_to_coords('52030252'), cep_to_coords('50720690'), cep_to_coords('50980560'), cep_to_coords('50640071'), cep_to_coords('56509490'), cep_to_coords('50060440'), cep_to_coords('54768230'), cep_to_coords('55520000'), cep_to_coords('50980625'), cep_to_coords('52221180'), cep_to_coords('55420000'), cep_to_coords('51190720'), cep_to_coords('51030830'), cep_to_coords('50790075'), cep_to_coords('53403141'), cep_to_coords('53160780'), cep_to_coords('53190000'), cep_to_coords('53170765'), cep_to_coords('55151680'), cep_to_coords('53437740'), cep_to_coords('52150153'), cep_to_coords('54768755'), cep_to_coords('52130120'), cep_to_coords('52060425'), cep_to_coords('53160110'), cep_to_coords('52100000'), cep_to_coords('53140280'), cep_to_coords('50910390'), cep_to_coords('50060004'), cep_to_coords('50790020'), cep_to_coords('52041305'), cep_to_coords('52041110'), cep_to_coords('53370370'), cep_to_coords('53416630'), cep_to_coords('50721530'), cep_to_coords('54705030'), cep_to_coords('52191115'), cep_to_coords('52041030'), cep_to_coords('50940230'), cep_to_coords('50230940'), cep_to_coords('52041640'), cep_to_coords('50791495'), cep_to_coords('52080110'), cep_to_coords('53240230'), cep_to_coords('52280501'), cep_to_coords('52051040'), cep_to_coords('50741080'), cep_to_coords('54230011'), cep_to_coords('52031195'), cep_to_coords('53170150'), cep_to_coords('51011040'), cep_to_coords('51335340'), cep_to_coords('53200320'), cep_to_coords('54120005'), cep_to_coords('53370330'), cep_to_coords('55813425'), cep_to_coords('54535130'), cep_to_coords('54783660'), cep_to_coords('51170260'), cep_to_coords('50761110'), cep_to_coords('52000000'), cep_to_coords('50660280'), cep_to_coords('53439690'), cep_to_coords('52210070'), cep_to_coords('52111320'), cep_to_coords('50820610'), cep_to_coords('52050345'), cep_to_coords('52211480'), cep_to_coords('52140050'), cep_to_coords('53050090'), cep_to_coords('54210380'), cep_to_coords('53220680'), cep_to_coords('52140610'), cep_to_coords('54768759'), cep_to_coords('52071570'), cep_to_coords('52061060'), cep_to_coords('51330250'), cep_to_coords('50630380'), cep_to_coords('53330710'), cep_to_coords('50830150'), cep_to_coords('50040200'), cep_to_coords('52091078'), cep_to_coords('53403220'), cep_to_coords('52121080'), cep_to_coords('52140450'), cep_to_coords('52081451'), cep_to_coords('53439340'), cep_to_coords('51220010'), cep_to_coords('52040480'), cep_to_coords('56614316'), cep_to_coords('56302300'), cep_to_coords('50110270'), cep_to_coords('56506970'), cep_to_coords('50711200'), cep_to_coords('52041300'), cep_to_coords('55365000'), cep_to_coords('56302972'), cep_to_coords('55158110'), cep_to_coords('56912150'), cep_to_coords('52020090'), cep_to_coords('52071160'), cep_to_coords('52120050'), cep_to_coords('52070130'), cep_to_coords('50710170'), cep_to_coords('50781550'), cep_to_coords('52081653'), cep_to_coords('52081522'), cep_to_coords('52040110'), cep_to_coords('53570715'), cep_to_coords('50110080'), cep_to_coords('50870000'), cep_to_coords('54420170'), cep_to_coords('53320541'), cep_to_coords('50740660'), cep_to_coords('50030250'), cep_to_coords('54150420'), cep_to_coords('52130135'), cep_to_coords('51310440'), cep_to_coords('51310390'), cep_to_coords('54150430'), cep_to_coords('53620718'), cep_to_coords('53610440'), cep_to_coords('54330645'), cep_to_coords('53444300'), cep_to_coords('54090260'), cep_to_coords('54170722'), cep_to_coords('50761570'), cep_to_coords('54490220'), cep_to_coords('55173568'), cep_to_coords('55014090'), cep_to_coords('52211050'), cep_to_coords('50900080'), cep_to_coords('53170660'), cep_to_coords('54250040'), cep_to_coords('54753788'), cep_to_coords('53401450'), cep_to_coords('53407750'), cep_to_coords('52210160'), cep_to_coords('52041150'), cep_to_coords('51011651'), cep_to_coords('53439220'), cep_to_coords('53280040'), cep_to_coords('53320410'), cep_to_coords('53413180'), cep_to_coords('50060180'), cep_to_coords('52071120'), cep_to_coords('54420100'), cep_to_coords('53370412'), cep_to_coords('52131190'), cep_to_coords('54759130'), cep_to_coords('57955000'), cep_to_coords('53405192'), cep_to_coords('52191585'), cep_to_coords('55292500'), cep_to_coords('52090565'), cep_to_coords('50970200'), cep_to_coords('50711090'), cep_to_coords('50760600'), cep_to_coords('56505330'), cep_to_coords('53350110'), cep_to_coords('53441330'), cep_to_coords('53421810'), cep_to_coords('50800040'), cep_to_coords('53110610'), cep_to_coords('53444060'), cep_to_coords('50670330'), cep_to_coords('52191445'), cep_to_coords('50780180'), cep_to_coords('53403390'), cep_to_coords('53433280'), cep_to_coords('51345830'), cep_to_coords('52050480'), cep_to_coords('50940270'), cep_to_coords('54720840'), cep_to_coords('53421451'), cep_to_coords('51240260'), cep_to_coords('53520172'), cep_to_coords('53421210'), cep_to_coords('52051060'), cep_to_coords('55297785'), cep_to_coords('54510350'), cep_to_coords('53407230'), cep_to_coords('51230120'), cep_to_coords('53060535'), cep_to_coords('52165000'), cep_to_coords('54733190'), cep_to_coords('53421290'), cep_to_coords('53444120'), cep_to_coords('53070030'), cep_to_coords('54250310'), cep_to_coords('5632811000'), cep_to_coords('55537000'), cep_to_coords('50960230'), cep_to_coords('50670350'), cep_to_coords('52040180'), cep_to_coords('53610285'), cep_to_coords('53530710'), cep_to_coords('51320460'), cep_to_coords('55315000'), cep_to_coords('50800320'), cep_to_coords('52010170'), cep_to_coords('55024000'), cep_to_coords('50680100'), cep_to_coords('51240062'), cep_to_coords('56850000'), cep_to_coords('54740610'), cep_to_coords('53120012'), cep_to_coords('54720305'), cep_to_coords('50110530'), cep_to_coords('50920110'), cep_to_coords('50740380'), cep_to_coords('52211200'), cep_to_coords('53441055'), cep_to_coords('54090101'), cep_to_coords('52110627'), cep_to_coords('52111040'), cep_to_coords('53433240'), cep_to_coords('52081530'), cep_to_coords('50640530'), cep_to_coords('53130290'), cep_to_coords('50020545'), cep_to_coords('51345435'), cep_to_coords('53030150'), cep_to_coords('53050410'), cep_to_coords('54440165'), cep_to_coords('50731160'), cep_to_coords('53220200'), cep_to_coords('51170240'), cep_to_coords('53290190'), cep_to_coords('55297815'), cep_to_coords('55292540'), cep_to_coords('51320210'), cep_to_coords('52081528'), cep_to_coords('50710090'), cep_to_coords('50760150'), cep_to_coords('55642104'), cep_to_coords('53401040'), cep_to_coords('53625400'), cep_to_coords('54100000'), cep_to_coords('54290000'), cep_to_coords('54210000'), cep_to_coords('53530462'), cep_to_coords('53444220'), cep_to_coords('51170440'), cep_to_coords('50720590'), cep_to_coords('50730215'), cep_to_coords('54792200'), cep_to_coords('50750390'), cep_to_coords('50790450'), cep_to_coords('54350020'), cep_to_coords('50680280'), cep_to_coords('55297350'), cep_to_coords('50630070'), cep_to_coords('50070605'), cep_to_coords('51345740'), cep_to_coords('53413100'), cep_to_coords('53090010'), cep_to_coords('54759480'), cep_to_coords('54777700'), cep_to_coords('52110120'), cep_to_coords('51020100'), cep_to_coords('50660390'), cep_to_coords('50650020'), cep_to_coords('53080260'), cep_to_coords('53425580'), cep_to_coords('51130180'), cep_to_coords('50920520'), cep_to_coords('55641735'), cep_to_coords('53530430'), cep_to_coords('53415050'), cep_to_coords('50760750'), cep_to_coords('50000180'), cep_to_coords('51280040'), cep_to_coords('54120082'), cep_to_coords('52070070'), cep_to_coords('54170160'), cep_to_coords('51240280'), cep_to_coords('50770400'), cep_to_coords('51030360'), cep_to_coords('50810240'), cep_to_coords('51030690'), cep_to_coords('54522170'), cep_to_coords('53040150'), cep_to_coords('52081080'), cep_to_coords('55295000'), cep_to_coords('53350210'), cep_to_coords('53409620'), cep_to_coords('55296230'), cep_to_coords('53030100'), cep_to_coords('53240210'), cep_to_coords('53320185'), cep_to_coords('53435530'), cep_to_coords('52010000'), cep_to_coords('50090590'), cep_to_coords('50780040'), cep_to_coords('50070280'), cep_to_coords('52121050'), cep_to_coords('50761150'), cep_to_coords('52050215'), cep_to_coords('13560241'), cep_to_coords('53150300'), cep_to_coords('54720001'), cep_to_coords('54759385'), cep_to_coords('50100300'), cep_to_coords('51111000'), cep_to_coords('54753100'), cep_to_coords('53370040'), cep_to_coords('50080440'), cep_to_coords('51030260'), cep_to_coords('54230432'), cep_to_coords('53370340'), cep_to_coords('53240270'), cep_to_coords('53540050'), cep_to_coords('50060140'), cep_to_coords('53230110'), cep_to_coords('50830000'), cep_to_coords('53350020'), cep_to_coords('53130020'), cep_to_coords('52110005'), cep_to_coords('50820000'), cep_to_coords('54230077'), cep_to_coords('51240220'), cep_to_coords('50011000'), cep_to_coords('50920210'), cep_to_coords('54700000'), cep_to_coords('52070245'), cep_to_coords('52070235'), cep_to_coords('51010220'), cep_to_coords('50100290'), cep_to_coords('56500999'), cep_to_coords('56503420'), cep_to_coords('56515040'), cep_to_coords('56515030'), cep_to_coords('53220120'), cep_to_coords('53560470'), cep_to_coords('52031490'), cep_to_coords('55296200'), cep_to_coords('52040450'), cep_to_coords('52280612'), cep_to_coords('55865000'), cep_to_coords('50721690'), cep_to_coords('53130550'), cep_to_coords('54090090'), cep_to_coords('50761480'), cep_to_coords('52121375'), cep_to_coords('51270690'), cep_to_coords('50670050'), cep_to_coords('54525350'), cep_to_coords('53435230'), cep_to_coords('53330190'), cep_to_coords('51250200'), cep_to_coords('50610971'), cep_to_coords('51320380'), cep_to_coords('54759560'), cep_to_coords('56503410'), cep_to_coords('56502165'), cep_to_coords('54320460'), cep_to_coords('55840000'), cep_to_coords('54320080'), cep_to_coords('54430770'), cep_to_coords('52091230'), cep_to_coords('52091231'), cep_to_coords('51180010'), cep_to_coords('53270571'), cep_to_coords('52150003'), cep_to_coords('51020020'), cep_to_coords('51300160'), cep_to_coords('52140150'), cep_to_coords('55002000'), cep_to_coords('55002970'), cep_to_coords('54120636'), cep_to_coords('53120080'), cep_to_coords('54280200'), cep_to_coords('54505240'), cep_to_coords('53423255'), cep_to_coords('51240200'), cep_to_coords('52030090'), cep_to_coords('53160185'), cep_to_coords('52070583'), cep_to_coords('50791010'), cep_to_coords('50780220'), cep_to_coords('54280533'), cep_to_coords('52160811'), cep_to_coords('52131020'), cep_to_coords('55026060'), cep_to_coords('53530786'), cep_to_coords('53443100'), cep_to_coords('54768190'), cep_to_coords('53190040'), cep_to_coords('53330460'), cep_to_coords('52061010'), cep_to_coords('54280000'), cep_to_coords('55012000'), cep_to_coords('55602100'), cep_to_coords('55026260'), cep_to_coords('50100230'), cep_to_coords('52090622'), cep_to_coords('51130170'), cep_to_coords('51310010'), cep_to_coords('55024650'), cep_to_coords('55008230'), cep_to_coords('53635585'), cep_to_coords('50761415'), cep_to_coords('53437120'), cep_to_coords('50710000'), cep_to_coords('53441020'), cep_to_coords('50720390'), cep_to_coords('53050120'), cep_to_coords('54230070'), cep_to_coords('50630580'), cep_to_coords('55835000'), cep_to_coords('51250340'), cep_to_coords('53421080'), cep_to_coords('51340520'), cep_to_coords('53444410'), cep_to_coords('52160270'), cep_to_coords('50751625'), cep_to_coords('52111622'), cep_to_coords('54410220'), cep_to_coords('54410745'), cep_to_coords('51011340'), cep_to_coords('52160420'), cep_to_coords('53160420'), cep_to_coords('54110000'), cep_to_coords('55580000'), cep_to_coords('55030170'), cep_to_coords('54771792'), cep_to_coords('53010370'), cep_to_coords('50980650'), cep_to_coords('51240480'), cep_to_coords('54240120'), cep_to_coords('52091026'), cep_to_coords('52131591'), cep_to_coords('55042050'), cep_to_coords('58437830'), cep_to_coords('51011420'), cep_to_coords('50680660'), cep_to_coords('50900300'), cep_to_coords('50870030'), cep_to_coords('52111530'), cep_to_coords('52111414'), cep_to_coords('55294290'), cep_to_coords('55297230'), cep_to_coords('54410420'), cep_to_coords('53230251'), cep_to_coords('53370193'), cep_to_coords('53030026'), cep_to_coords('53350120'), cep_to_coords('52490150'), cep_to_coords('52110455'), cep_to_coords('52171050'), cep_to_coords('56903510'), cep_to_coords('52125250'), cep_to_coords('2000000000'), cep_to_coords('50080000'), cep_to_coords('53031100'), cep_to_coords('55295335'), cep_to_coords('54756110'), cep_to_coords('50090160'), cep_to_coords('51011330'), cep_to_coords('51030450'), cep_to_coords('55590990'), cep_to_coords('55595000'), cep_to_coords('56260000'), cep_to_coords('54515090'), cep_to_coords('56903970'), cep_to_coords('54789140'), cep_to_coords('50820600'), cep_to_coords('50721760'), cep_to_coords('54768050'), cep_to_coords('50650120'), cep_to_coords('51330190'), cep_to_coords('54515010'), cep_to_coords('55038270'), cep_to_coords('52060461'), cep_to_coords('54450170'), cep_to_coords('54320330'), cep_to_coords('51350150'), cep_to_coords('53407530'), cep_to_coords('53429380'), cep_to_coords('52120100'), cep_to_coords('52071170'), cep_to_coords('52121420'), cep_to_coords('55293140'), cep_to_coords('50860010'), cep_to_coords('54460250'), cep_to_coords('53070620'), cep_to_coords('50810060'), cep_to_coords('55675000'), cep_to_coords('53220540'), cep_to_coords('53409680'), cep_to_coords('51260260'), cep_to_coords('50620040'), cep_to_coords('50740110'), cep_to_coords('52090380'), cep_to_coords('54410335'), cep_to_coords('53090250'), cep_to_coords('54240030'), cep_to_coords('50740525'), cep_to_coords('52280310'), cep_to_coords('79649954'), cep_to_coords('53530478'), cep_to_coords('52091160'), cep_to_coords('55845000'), cep_to_coords('52210000'), cep_to_coords('50865180'), cep_to_coords('50770610'), cep_to_coords('55757000'), cep_to_coords('56502313'), cep_to_coords('56512540'), cep_to_coords('56519990'), cep_to_coords('52131010'), cep_to_coords('51340360'), cep_to_coords('52090290'), cep_to_coords('56507100'), cep_to_coords('56515700'), cep_to_coords('52130170'), cep_to_coords('52090003'), cep_to_coords('55660000'), cep_to_coords('53415480'), cep_to_coords('53437450'), cep_to_coords('54270630'), cep_to_coords('54762845'), cep_to_coords('54753976'), cep_to_coords('52130470'), cep_to_coords('51020120'), cep_to_coords('52120125'), cep_to_coords('50720310'), cep_to_coords('50900390'), cep_to_coords('54260070'), cep_to_coords('53220530'), cep_to_coords('50865041'), cep_to_coords('51160100'), cep_to_coords('56720000'), cep_to_coords('54420090'), cep_to_coords('54325064'), cep_to_coords('50070580'), cep_to_coords('50080500'), cep_to_coords('50070030'), cep_to_coords('50110090'), cep_to_coords('51160420'), cep_to_coords('51021140'), cep_to_coords('25021220'), cep_to_coords('53437710'), cep_to_coords('53437260'), cep_to_coords('53417681'), cep_to_coords('54780070'), cep_to_coords('54368230'), cep_to_coords('54310050'), cep_to_coords('52110040'), cep_to_coords('50740020'), cep_to_coords('50710165'), cep_to_coords('51010090'), cep_to_coords('51230150'), cep_to_coords('50720741'), cep_to_coords('53530130'), cep_to_coords('53423610'), cep_to_coords('54250240'), cep_to_coords('53370530'), cep_to_coords('53350540'), cep_to_coords('55608470'), cep_to_coords('54753792'), cep_to_coords('52221350'), cep_to_coords('51110210'), cep_to_coords('52160140'), cep_to_coords('50970100'), cep_to_coords('52120090'), cep_to_coords('55014315'), cep_to_coords('53409600'), cep_to_coords('54120000'), cep_to_coords('54150622'), cep_to_coords('53320590'), cep_to_coords('54310260'), cep_to_coords('50865050'), cep_to_coords('53040125'), cep_to_coords('50760770'), cep_to_coords('52211130'), cep_to_coords('52191470'), cep_to_coords('52050310'), cep_to_coords('50070590'), cep_to_coords('50060210'), cep_to_coords('50980705'), cep_to_coords('50060490'), cep_to_coords('55022340'), cep_to_coords('54260130'), cep_to_coords('53441040'), cep_to_coords('53130390'), cep_to_coords('55038080'), cep_to_coords('50741090'), cep_to_coords('54460020'), cep_to_coords('53407210'), cep_to_coords('55608610'), cep_to_coords('53330740'), cep_to_coords('51280400'), cep_to_coords('50980494'), cep_to_coords('54300230'), cep_to_coords('53 415 370'), cep_to_coords('52211191'), cep_to_coords('54768645'), cep_to_coords('55032330'), cep_to_coords('51021300'), cep_to_coords('54220300'), cep_to_coords('50060580'), cep_to_coords('53437290'), cep_to_coords('53434729'), cep_to_coords('50790120'), cep_to_coords('52111360'), cep_to_coords('53220382'), cep_to_coords('55350000'), cep_to_coords('50050240'), cep_to_coords('55294200'), cep_to_coords('52091000'), cep_to_coords('52090300'), cep_to_coords('54705210'), cep_to_coords('53060105'), cep_to_coords('53110600'), cep_to_coords('53330305'), cep_to_coords('53180050'), cep_to_coords('56915899'), cep_to_coords('56903330'), cep_to_coords('569000000'), cep_to_coords('06900000'), cep_to_coords('58600000'), cep_to_coords('52280581'), cep_to_coords('54140260'), cep_to_coords('52280440'), cep_to_coords('52120041'), cep_to_coords('53637550'), cep_to_coords('53120390'), cep_to_coords('53610756'), cep_to_coords('53610272'), cep_to_coords('54230132'), cep_to_coords('54325115'), cep_to_coords('54400310'), cep_to_coords('54335090'), cep_to_coords('54515135'), cep_to_coords('54040240'), cep_to_coords('55604610'), cep_to_coords('54440410'), cep_to_coords('53630840'), cep_to_coords('52060060'), cep_to_coords('50710025'), cep_to_coords('51111090'), cep_to_coords('54120060'), cep_to_coords('52390000'), cep_to_coords('52130315'), cep_to_coords('52120313'), cep_to_coords('53080490'), cep_to_coords('50750070'), cep_to_coords('53437050'), cep_to_coords('52131155'), cep_to_coords('52140180'), cep_to_coords('53290310'), cep_to_coords('53010110'), cep_to_coords('55008450'), cep_to_coords('53110530'), cep_to_coords('53409390'), cep_to_coords('54771410'), cep_to_coords('53320120'), cep_to_coords('50790410'), cep_to_coords('53170045'), cep_to_coords('54762780'), cep_to_coords('53060520'), cep_to_coords('50920330'), cep_to_coords('55640253'), cep_to_coords('54250371'), cep_to_coords('53300060'), cep_to_coords('53220490'), cep_to_coords('52070012'), cep_to_coords('52221120'), cep_to_coords('50730460'), cep_to_coords('53080140'), cep_to_coords('53040180'), cep_to_coords('54325600'), cep_to_coords('56915030'), cep_to_coords('55294936'), cep_to_coords('54220030'), cep_to_coords('54160230'), cep_to_coords('54330310'), cep_to_coords('54530072'), cep_to_coords('53370298'), cep_to_coords('52210061'), cep_to_coords('52280061'), cep_to_coords('54350744'), cep_to_coords('54450080'), cep_to_coords('52280020'), cep_to_coords('54774605'), cep_to_coords('53428805'), cep_to_coords('54450015'), cep_to_coords('53130440'), cep_to_coords('50750120'), cep_to_coords('54230062'), cep_to_coords('52160365'), cep_to_coords('53610345'), cep_to_coords('54450070'), cep_to_coords('54325000'), cep_to_coords('54300040'), cep_to_coords('53437070'), cep_to_coords('50640430'), cep_to_coords('52130330'), cep_to_coords('52060111'), cep_to_coords('51340440'), cep_to_coords('50780390'), cep_to_coords('50980410'), cep_to_coords('55008250'), cep_to_coords('55614230'), cep_to_coords('54710010'), cep_to_coords('51335250'), cep_to_coords('54430290'), cep_to_coords('50920115'), cep_to_coords('50751615'), cep_to_coords('54280011'), cep_to_coords('52040431'), cep_to_coords('59111090'), cep_to_coords('50110160'), cep_to_coords('54705183'), cep_to_coords('50791120'), cep_to_coords('54315360'), cep_to_coords('52280505'), cep_to_coords('54420240'), cep_to_coords('50720382'), cep_to_coords('53370150'), cep_to_coords('54100480'), cep_to_coords('54580735'), cep_to_coords('51110380'), cep_to_coords('52070570'), cep_to_coords('51011070'), cep_to_coords('55614050'), cep_to_coords('55608676'), cep_to_coords('53565580'), cep_to_coords('53240520'), cep_to_coords('50761310'), cep_to_coords('52291081'), cep_to_coords('56130000'), cep_to_coords('51021500'), cep_to_coords('54510000'), cep_to_coords('52291570'), cep_to_coords('52061050'), cep_to_coords('54440010'), cep_to_coords('54400410'), cep_to_coords('52191400'), cep_to_coords('54515390'), cep_to_coords('54517500'), cep_to_coords('53401775'), cep_to_coords('53180000'), cep_to_coords('52011260'), cep_to_coords('52280290'), cep_to_coords('53605040'), cep_to_coords('52171260'), cep_to_coords('55295610'), cep_to_coords('55296610'), cep_to_coords('51010000'), cep_to_coords('51300161'), cep_to_coords('52071185'), cep_to_coords('50751490'), cep_to_coords('51300110'), cep_to_coords('50020480'), cep_to_coords('52140401'), cep_to_coords('52041370'), cep_to_coords('50620650'), cep_to_coords('53437490'), cep_to_coords('54350095'), cep_to_coords('54589340'), cep_to_coords('51011272'), cep_to_coords('54160435'), cep_to_coords('52091505'), cep_to_coords('51330310'), cep_to_coords('52070440'), cep_to_coords('55641420'), cep_to_coords('50070150'), cep_to_coords('50980210'), cep_to_coords('50761590'), cep_to_coords('54325795'), cep_to_coords('55643632'), cep_to_coords('54120046'), cep_to_coords('54460310'), cep_to_coords('54470310'), cep_to_coords('54535420'), cep_to_coords('53220121'), cep_to_coords('54150094'), cep_to_coords('50761640'), cep_to_coords('52011200'), cep_to_coords('55814160'), cep_to_coords('53370110'), cep_to_coords('50500903'), cep_to_coords('52280235'), cep_to_coords('50690685'), cep_to_coords('53250230'), cep_to_coords('54768290'), cep_to_coords('53330250'), cep_to_coords('53130000'), cep_to_coords('51230020'), cep_to_coords('53370267'), cep_to_coords('53270185'), cep_to_coords('55612320'), cep_to_coords('53640306'), cep_to_coords('53419230'), cep_to_coords('53110470'), cep_to_coords('54330000'), cep_to_coords('54530121'), cep_to_coords('54130121'), cep_to_coords('58735000'), cep_to_coords('50780350'), cep_to_coords('55602550'), cep_to_coords('50810320'), cep_to_coords('52120590'), cep_to_coords('50800290'), cep_to_coords('54762745'), cep_to_coords('50721560'), cep_to_coords('50771420'), cep_to_coords('52081020'), cep_to_coords('52490070'), cep_to_coords('50690690'), cep_to_coords('50761130'), cep_to_coords('53370670'), cep_to_coords('54756040'), cep_to_coords('55602681'), cep_to_coords('53429000'), cep_to_coords('53429050'), cep_to_coords('54429050'), cep_to_coords('50870390'), cep_to_coords('52041515'), cep_to_coords('50790310'), cep_to_coords('52211520'), cep_to_coords('53220450'), cep_to_coords('54515260'), cep_to_coords('55296000'), cep_to_coords('55410000'), cep_to_coords('55730000'), cep_to_coords('54296548'), cep_to_coords('54420710'), cep_to_coords('50771570'), cep_to_coords('51300040'), cep_to_coords('53050273'), cep_to_coords('52080000'), cep_to_coords('53290030'), cep_to_coords('54365130'), cep_to_coords('56840000'), cep_to_coords('52080096'), cep_to_coords('50920470'), cep_to_coords('54762660'), cep_to_coords('54762370'), cep_to_coords('54768783'), cep_to_coords('51020903'), cep_to_coords('54210430'), cep_to_coords('54515400'), cep_to_coords('55811000'), cep_to_coords('54505115'), cep_to_coords('54245140'), cep_to_coords('54100130'), cep_to_coords('54280010'), cep_to_coords('16020365'), cep_to_coords('51030020'), cep_to_coords('48730000'), cep_to_coords('50720448'), cep_to_coords('54580001'), cep_to_coords('50670310'), cep_to_coords('53407160'), cep_to_coords('56903440'), cep_to_coords('50910030'), cep_to_coords('54400300'), cep_to_coords('52020210'), cep_to_coords('52030120'), cep_to_coords('50760004'), cep_to_coords('54230050'), cep_to_coords('54505520'), cep_to_coords('55280000'), cep_to_coords('50780030'), cep_to_coords('52021030'), cep_to_coords('52011080'), cep_to_coords('54420001'), cep_to_coords('53403420'), cep_to_coords('51190250'), cep_to_coords('54160220'), cep_to_coords('54505100'), cep_to_coords('51010130'), cep_to_coords('54535070'), cep_to_coords('50050420'), cep_to_coords('50710150'), cep_to_coords('52070584'), cep_to_coords('50640050'), cep_to_coords('55292446'), cep_to_coords('50720145'), cep_to_coords('53240110'), cep_to_coords('50721230'), cep_to_coords('52080094'), cep_to_coords('52020150'), cep_to_coords('50860015'), cep_to_coords('55640040'), cep_to_coords('56509140'), cep_to_coords('55030450'), cep_to_coords('53625490'), cep_to_coords('53370141'), cep_to_coords('53405380'), cep_to_coords('52080330'), cep_to_coords('52010075'), cep_to_coords('53130530'), cep_to_coords('50791150'), cep_to_coords('50781290'), cep_to_coords('51150230'), cep_to_coords('54440300'), cep_to_coords('52050041'), cep_to_coords('52050000'), cep_to_coords('54515150'), cep_to_coords('51111100'), cep_to_coords('53402150'), cep_to_coords('50900410'), cep_to_coords('53417620'), cep_to_coords('53585130'), cep_to_coords('54160470'), cep_to_coords('54290102'), cep_to_coords('50050230'), cep_to_coords('53421036'), cep_to_coords('50070595'), cep_to_coords('54024420'), cep_to_coords('50650400'), cep_to_coords('52081369'), cep_to_coords('50721050'), cep_to_coords('50720050'), cep_to_coords('55293320'), cep_to_coords('55296020'), cep_to_coords('50710270'), cep_to_coords('54715840'), cep_to_coords('54420180'), cep_to_coords('51021530'), cep_to_coords('50761000'), cep_to_coords('52081083'), cep_to_coords('55642150'), cep_to_coords('51112957'), cep_to_coords('54340185'), cep_to_coords('54576821'), cep_to_coords('55155010'), cep_to_coords('51010420'), cep_to_coords('54490090'), cep_to_coords('50920900'), cep_to_coords('55295480'), cep_to_coords('55290660'), cep_to_coords('54330200'), cep_to_coords('54450050'), cep_to_coords('51240010'), cep_to_coords('50920451'), cep_to_coords('50020455'), cep_to_coords('55032150'), cep_to_coords('54580305'), cep_to_coords('54250081'), cep_to_coords('54774490'), cep_to_coords('54210290'), cep_to_coords('53070110'), cep_to_coords('50960560'), cep_to_coords('50711250'), cep_to_coords('56320330'), cep_to_coords('53401090'), cep_to_coords('54768060'), cep_to_coords('51346000'), cep_to_coords('53020080'), cep_to_coords('52041340'), cep_to_coords('51011490'), cep_to_coords('51340730'), cep_to_coords('54433480'), cep_to_coords('53433480'), cep_to_coords('55818525'), cep_to_coords('51280075'), cep_to_coords('50960260'), cep_to_coords('51111250'), cep_to_coords('53020090'), cep_to_coords('52111230'), cep_to_coords('51280510'), cep_to_coords('50740271'), cep_to_coords('53640605'), cep_to_coords('53417031'), cep_to_coords('53471031'), cep_to_coords('53250440'), cep_to_coords('53290285'), cep_to_coords('50050903'), cep_to_coords('52081203'), cep_to_coords('52040330'), cep_to_coords('51011010'), cep_to_coords('55612271'), cep_to_coords('50720605'), cep_to_coords('51130120'), cep_to_coords('52140220'), cep_to_coords('55008510'), cep_to_coords('53550750'), cep_to_coords('53080580'), cep_to_coords('54135301'), cep_to_coords('55813451'), cep_to_coords('54580500'), cep_to_coords('52050180'), cep_to_coords('55028220'), cep_to_coords('55018000'), cep_to_coords('51011310'), cep_to_coords('50860040'), cep_to_coords('52071191'), cep_to_coords('52080644'), cep_to_coords('53409228'), cep_to_coords('52070020'), cep_to_coords('56313353'), cep_to_coords('54320175'), cep_to_coords('50980550'), cep_to_coords('54410359'), cep_to_coords('54490071'), cep_to_coords('54440475'), cep_to_coords('53500000'), cep_to_coords('53425640'), cep_to_coords('53300020'), cep_to_coords('50080730'), cep_to_coords('53270020'), cep_to_coords('52121200'), cep_to_coords('51230220'), cep_to_coords('52165050'), cep_to_coords('53060080'), cep_to_coords('53441610'), cep_to_coords('54230182'), cep_to_coords('52090505'), cep_to_coords('50760720'), cep_to_coords('53070380'), cep_to_coords('50080550'), cep_to_coords('50050030'), cep_to_coords('50960250'), cep_to_coords('50080110'), cep_to_coords('54400200'), cep_to_coords('50810900'), cep_to_coords('52050160'), cep_to_coords('55930000'), cep_to_coords('51021280'), cep_to_coords('50090150'), cep_to_coords('50080480'), cep_to_coords('50771030'), cep_to_coords('53150009'), cep_to_coords('56360000'), cep_to_coords('51190050'), cep_to_coords('55297800'), cep_to_coords('50110815'), cep_to_coords('50020040'), cep_to_coords('54440480'), cep_to_coords('53330020'), cep_to_coords('54315400'), cep_to_coords('53402070'), cep_to_coords('54430282'), cep_to_coords('53441190'), cep_to_coords('53050110'), cep_to_coords('54120260'), cep_to_coords('54230210'), cep_to_coords('50741410'), cep_to_coords('51290310'), cep_to_coords('54440070'), cep_to_coords('54160000'), cep_to_coords('54340000'), cep_to_coords('54420350'), cep_to_coords('54260160'), cep_to_coords('54210543'), cep_to_coords('51030120'), cep_to_coords('54330620'), cep_to_coords('51290470'), cep_to_coords('52120570'), cep_to_coords('54315361'), cep_to_coords('54410680'), cep_to_coords('50060500'), cep_to_coords('51320000'), cep_to_coords('52171295'), cep_to_coords('51030370'), cep_to_coords('54410450'), cep_to_coords('50820630'), cep_to_coords('55612660'), cep_to_coords('53444310'), cep_to_coords('55195605'), cep_to_coords('51220080'), cep_to_coords('54150400'), cep_to_coords('54210544'), cep_to_coords('55006190'), cep_to_coords('55014285'), cep_to_coords('50050290'), cep_to_coords('53530090'), cep_to_coords('53530092'), cep_to_coords('52121580'), cep_to_coords('54280310'), cep_to_coords('54768130'), cep_to_coords('50060070'), cep_to_coords('52081470'), cep_to_coords('52280733'), cep_to_coords('53370170'), cep_to_coords('50771830'), cep_to_coords('54730970'), cep_to_coords('51130100'), cep_to_coords('52060100'), cep_to_coords('50764640'), cep_to_coords('50790260'), cep_to_coords('54210520'), cep_to_coords('52111621'), cep_to_coords('50721430'), cep_to_coords('56820000'), cep_to_coords('56460000'), cep_to_coords('51320130'), cep_to_coords('54420000'), cep_to_coords('52150013'), cep_to_coords('55604250'), cep_to_coords('56520000'), cep_to_coords('55608690'), cep_to_coords('12030730'), cep_to_coords('39444074'), cep_to_coords('53160150'), cep_to_coords('55103001'), cep_to_coords('52060190'), cep_to_coords('50090350'), cep_to_coords('54400370'), cep_to_coords('52030520'), cep_to_coords('53435380'), cep_to_coords('54220255'), cep_to_coords('54762367'), cep_to_coords('52071070'), cep_to_coords('54580623'), cep_to_coords('55929000'), cep_to_coords('50060482'), cep_to_coords('50870490'), cep_to_coords('55608509'), cep_to_coords('54420130'), cep_to_coords('52050010'), cep_to_coords('51021260'), cep_to_coords('50721310'), cep_to_coords('54330625'), cep_to_coords('54230555'), cep_to_coords('54756115'), cep_to_coords('51030040'), cep_to_coords('50771400'), cep_to_coords('56512680'), cep_to_coords('53230480'), cep_to_coords('54220530'), cep_to_coords('54505505'), cep_to_coords('52060266'), cep_to_coords('53070195'), cep_to_coords('54340068'), cep_to_coords('54753380'), cep_to_coords('53370630'), cep_to_coords('55012484'), cep_to_coords('51110150'), cep_to_coords('51340000'), cep_to_coords('52171130'), cep_to_coords('54720090'), cep_to_coords('54100200'), cep_to_coords('56420000'), cep_to_coords('54720200'), cep_to_coords('50820590'), cep_to_coords('53060350'), cep_to_coords('55038000'), cep_to_coords('52080170'), cep_to_coords('54100020'), cep_to_coords('52050375'), cep_to_coords('53442110'), cep_to_coords('52130021'), cep_to_coords('50870730'), cep_to_coords('54440050'), cep_to_coords('54280755'), cep_to_coords('50940750'), cep_to_coords('58046000'), cep_to_coords('55644130'), cep_to_coords('55034040'), cep_to_coords('43103901'), cep_to_coords('54230181'), cep_to_coords('54753016'), cep_to_coords('54783000'), cep_to_coords('50780540'), cep_to_coords('50800030'), cep_to_coords('53439000'), cep_to_coords('53429540'), cep_to_coords('53160010'), cep_to_coords('50741100'), cep_to_coords('54771380'), cep_to_coords('51370170'), cep_to_coords('53442090'), cep_to_coords('50710020'), cep_to_coords('51021020'), cep_to_coords('51110020'), cep_to_coords('52190090'), cep_to_coords('53413310'), cep_to_coords('54220010'), cep_to_coords('54330125'), cep_to_coords('50771550'), cep_to_coords('53401810'), cep_to_coords('53220280'), cep_to_coords('54120015'), cep_to_coords('51170430'), cep_to_coords('53431832'), cep_to_coords('56903650'), cep_to_coords('56903910'), cep_to_coords('56903000'), cep_to_coords('56903310'), cep_to_coords('56907130'), cep_to_coords('56909320'), cep_to_coords('56903360'), cep_to_coords('56909188'), cep_to_coords('55604300'), cep_to_coords('56503440'), cep_to_coords('55250000'), cep_to_coords('53200140'), cep_to_coords('51011065'), cep_to_coords('55032280'), cep_to_coords('52280160'), cep_to_coords('52291270'), cep_to_coords('54771780'), cep_to_coords('50970060'), cep_to_coords('54774120'), cep_to_coords('54759300'), cep_to_coords('54756470'), cep_to_coords('58920000'), cep_to_coords('56328420'), cep_to_coords('54580015'), cep_to_coords('50129301'), cep_to_coords('50129303'), cep_to_coords('54762542'), cep_to_coords('51270030'), cep_to_coords('17021958'), cep_to_coords('05501464'), cep_to_coords('50721610'), cep_to_coords('52131450'), cep_to_coords('54360090'), cep_to_coords('52131380'), cep_to_coords('50720520'), cep_to_coords('50771520'), cep_to_coords('51011180'), cep_to_coords('54430360'), cep_to_coords('55006260'), cep_to_coords('52620015'), cep_to_coords('53417080'), cep_to_coords('53090260'), cep_to_coords('53160460'), cep_to_coords('51190100'), cep_to_coords('55155590'), cep_to_coords('51030840'), cep_to_coords('55296595'), cep_to_coords('57607010'), cep_to_coords('55152430'), cep_to_coords('55157010'), cep_to_coords('55152060'), cep_to_coords('52280123'), cep_to_coords('52111005'), cep_to_coords('52110131'), cep_to_coords('51110131'), cep_to_coords('52011070'), cep_to_coords('55012010'), cep_to_coords('53540500'), cep_to_coords('54792990'), cep_to_coords('53444430'), cep_to_coords('53240390'), cep_to_coords('54735775'), cep_to_coords('52081270'), cep_to_coords('55298090'), cep_to_coords('55296400'), cep_to_coords('52011050'), cep_to_coords('52190210'), cep_to_coords('55036380'), cep_to_coords('55014265'), cep_to_coords('50760310'), cep_to_coords('51030280'), cep_to_coords('54160350'), cep_to_coords('54440620'), cep_to_coords('54325818'), cep_to_coords('50680350'), cep_to_coords('54762395'), cep_to_coords('50900310'), cep_to_coords('53210170'), cep_to_coords('52120145'), cep_to_coords('53610723'), cep_to_coords('55816390'), cep_to_coords('54080110'), cep_to_coords('54280490'), cep_to_coords('54430220'), cep_to_coords('53610610'), cep_to_coords('50110415'), cep_to_coords('52210440'), cep_to_coords('24910000'), cep_to_coords('51021120'), cep_to_coords('53429520'), cep_to_coords('54330216'), cep_to_coords('54100230'), cep_to_coords('54768320'), cep_to_coords('53250050'), cep_to_coords('52140190'), cep_to_coords('53030030'), cep_to_coords('50761380'), cep_to_coords('50761730'), cep_to_coords('51350120'), cep_to_coords('52090381'), cep_to_coords('55014080'), cep_to_coords('55026080'), cep_to_coords('53421321'), cep_to_coords('50343787'), cep_to_coords('54777080'), cep_to_coords('54780140'), cep_to_coords('58280000'), cep_to_coords('50781651'), cep_to_coords('52070649'), cep_to_coords('50900260'), cep_to_coords('50110000'), cep_to_coords('50720525'), cep_to_coords('52080270'), cep_to_coords('52081340'), cep_to_coords('53300040'), cep_to_coords('51250370'), cep_to_coords('52191140'), cep_to_coords('50630390'), cep_to_coords('53530990'), cep_to_coords('54430112'), cep_to_coords('54400440'), cep_to_coords('51290180'), cep_to_coords('54220295'), cep_to_coords('54762165'), cep_to_coords('50741180'), cep_to_coords('51190330'), cep_to_coords('52060080'), cep_to_coords('52060130'), cep_to_coords('58410220'), cep_to_coords('52081092'), cep_to_coords('50110840'), cep_to_coords('53080750'), cep_to_coords('55157410'), cep_to_coords('55690000'), cep_to_coords('53407060'), cep_to_coords('54490000'), cep_to_coords('52191040'), cep_to_coords('50110190'), cep_to_coords('50771150'), cep_to_coords('52190540'), cep_to_coords('50830300'), cep_to_coords('54400320'), cep_to_coords('54580830'), cep_to_coords('53110440'), cep_to_coords('50110725'), cep_to_coords('54753000'), cep_to_coords('50761780'), cep_to_coords('52010140'), cep_to_coords('55642075'), cep_to_coords('53441530'), cep_to_coords('54520430'), cep_to_coords('54580260'), cep_to_coords('53290220'), cep_to_coords('52280302'), cep_to_coords('50810370'), cep_to_coords('54753080'), cep_to_coords('51230250'), cep_to_coords('52050217'), cep_to_coords('52041720'), cep_to_coords('52041770'), cep_to_coords('54470181'), cep_to_coords('52211265'), cep_to_coords('50370020'), cep_to_coords('50820020'), cep_to_coords('54768705'), cep_to_coords('53300310'), cep_to_coords('52210210'), cep_to_coords('52091050'), cep_to_coords('54762621'), cep_to_coords('56700000'), cep_to_coords('50875090'), cep_to_coords('50770790'), cep_to_coords('55034215'), cep_to_coords('53421037'), cep_to_coords('56903276'), cep_to_coords('53427450'), cep_to_coords('51240060'), cep_to_coords('51240106'), cep_to_coords('50750251'), cep_to_coords('50690525'), cep_to_coords('55016015'), cep_to_coords('56903270'), cep_to_coords('07760000'), cep_to_coords('53220270'), cep_to_coords('53250120'), cep_to_coords('51250350'), cep_to_coords('54330120'), cep_to_coords('53440070'), cep_to_coords('51170560'), cep_to_coords('55735000'), cep_to_coords('51340260'), cep_to_coords('56304270'), cep_to_coords('52031030'), cep_to_coords('54230422'), cep_to_coords('56330075'), cep_to_coords('54420190'), cep_to_coords('51335320'), cep_to_coords('54280240'), cep_to_coords('56903269'), cep_to_coords('56903640'), cep_to_coords('56903300'), cep_to_coords('56912440'), cep_to_coords('56909350'), cep_to_coords('54220220'), cep_to_coords('54725020'), cep_to_coords('53423833'), cep_to_coords('53580360'), cep_to_coords('52070250'), cep_to_coords('52070710'), cep_to_coords('53250240'), cep_to_coords('54325075'), cep_to_coords('53421690'), cep_to_coords('51111230'), cep_to_coords('51280405'), cep_to_coords('05427020'), cep_to_coords('54470190'), cep_to_coords('53429800'), cep_to_coords('54100405'), cep_to_coords('50070190'), cep_to_coords('52280630'), cep_to_coords('54759160'), cep_to_coords('53433760'), cep_to_coords('52050205'), cep_to_coords('56506450'), cep_to_coords('54250100'), cep_to_coords('54365010'), cep_to_coords('56509380'), cep_to_coords('56509370'), cep_to_coords('55150520'), cep_to_coords('53413330'), cep_to_coords('53441050'), cep_to_coords('50670460'), cep_to_coords('51260320'), cep_to_coords('52191270'), cep_to_coords('50810390'), cep_to_coords('50870350'), cep_to_coords('50751180'), cep_to_coords('50751210'), cep_to_coords('53150430'), cep_to_coords('50720670'), cep_to_coords('52280120'), cep_to_coords('55018062'), cep_to_coords('58706130'), cep_to_coords('50760140'), cep_to_coords('53360410'), cep_to_coords('53220581'), cep_to_coords('56505000'), cep_to_coords('56505140'), cep_to_coords('56519160'), cep_to_coords('56120000'), cep_to_coords('55415000'), cep_to_coords('54090130'), cep_to_coords('56320540'), cep_to_coords('55642066'), cep_to_coords('48904150'), cep_to_coords('51030570'), cep_to_coords('54753540'), cep_to_coords('52060120'), cep_to_coords('53046150'), cep_to_coords('55644365'), cep_to_coords('56909660'), cep_to_coords('55032000'), cep_to_coords('53180291'), cep_to_coords('50761350'), cep_to_coords('53350160'), cep_to_coords('50390710'), cep_to_coords('52191020'), cep_to_coords('52090061'), cep_to_coords('56912370'), cep_to_coords('53437170'), cep_to_coords('54762320'), cep_to_coords('50060200'), cep_to_coords('50820070'), cep_to_coords('53350410'), cep_to_coords('54330465'), cep_to_coords('54735300'), cep_to_coords('54510410'), cep_to_coords('55790000'), cep_to_coords('51170435'), cep_to_coords('51021540'), cep_to_coords('50790116'), cep_to_coords('54340710'), cep_to_coords('54450090'), cep_to_coords('51020110'), cep_to_coords('52070005'), cep_to_coords('50610070'), cep_to_coords('54505020'), cep_to_coords('53560200'), cep_to_coords('54759825'), cep_to_coords('53230310'), cep_to_coords('53140100'), cep_to_coords('55038530'), cep_to_coords('52031170'), cep_to_coords('51150060'), cep_to_coords('65765574'), cep_to_coords('50110691'), cep_to_coords('53030190'), cep_to_coords('51020150'), cep_to_coords('52030100'), cep_to_coords('54210410'), cep_to_coords('53350551'), cep_to_coords('56302450'), cep_to_coords('52090280'), cep_to_coords('50630470'), cep_to_coords('50730110'), cep_to_coords('54160290'), cep_to_coords('54300260'), cep_to_coords('51011540'), cep_to_coords('52070445'), cep_to_coords('56903480'), cep_to_coords('56915000'), cep_to_coords('54470610'), cep_to_coords('50980735'), cep_to_coords('50850100'), cep_to_coords('52060460'), cep_to_coords('50731005'), cep_to_coords('55299340'), cep_to_coords('51240490'), cep_to_coords('51240500'), cep_to_coords('54460030'), cep_to_coords('53417190'), cep_to_coords('53401000'), cep_to_coords('53413090'), cep_to_coords('52211000'), cep_to_coords('55034570'), cep_to_coords('55633970'), cep_to_coords('48900000'), cep_to_coords('50790100'), cep_to_coords('54170330'), cep_to_coords('55819901'), cep_to_coords('55032290'), cep_to_coords('53330310'), cep_to_coords('50721455'), cep_to_coords('54505560'), cep_to_coords('50050200'), cep_to_coords('56909484'), cep_to_coords('56909103'), cep_to_coords('56308185'), cep_to_coords('55402956'), cep_to_coords('54100660'), cep_to_coords('54510310'), cep_to_coords('53580730'), cep_to_coords('53635050'), cep_to_coords('53610335'), cep_to_coords('53605680'), cep_to_coords('54505420'), cep_to_coords('50720190'), cep_to_coords('50670179'), cep_to_coords('53402670'), cep_to_coords('52080410'), cep_to_coords('51340080'), cep_to_coords('55008520'), cep_to_coords('54230171'), cep_to_coords('50875130'), cep_to_coords('56516175'), cep_to_coords('58417503'), cep_to_coords('54353330'), cep_to_coords('54515280'), cep_to_coords('50741230'), cep_to_coords('54350040'), cep_to_coords('53530020'), cep_to_coords('53409300'), cep_to_coords('53025080'), cep_to_coords('56355000'), cep_to_coords('51200020'), cep_to_coords('50070160'), cep_to_coords('56430000'), cep_to_coords('54756467'), cep_to_coords('50760820'), cep_to_coords('52131110'), cep_to_coords('54720011'), cep_to_coords('51110310'), cep_to_coords('55818305'), cep_to_coords('52061022'), cep_to_coords('54774250'), cep_to_coords('53240000'), cep_to_coords('51160060'), cep_to_coords('50720140'), cep_to_coords('54300263'), cep_to_coords('54290051'), cep_to_coords('52131145'), cep_to_coords('56912100'), cep_to_coords('52051900'), cep_to_coords('51190040'), cep_to_coords('50720620'), cep_to_coords('55640292'), cep_to_coords('54260010'), cep_to_coords('52041705'), cep_to_coords('56380000'), cep_to_coords('51350080'), cep_to_coords('55345000'), cep_to_coords('51190360'), cep_to_coords('54517505'), cep_to_coords('52090100'), cep_to_coords('53433300'), cep_to_coords('52041540'), cep_to_coords('53510480'), cep_to_coords('54759125'), cep_to_coords('50630160'), cep_to_coords('52050430'), cep_to_coords('54420110'), cep_to_coords('55016440'), cep_to_coords('58328000'), cep_to_coords('54210370'), cep_to_coords('51020170'), cep_to_coords('54080120'), cep_to_coords('52291535'), cep_to_coords('51030510'), cep_to_coords('55022510'), cep_to_coords('51280490'), cep_to_coords('53120248'), cep_to_coords('52130715'), cep_to_coords('54515120'), cep_to_coords('54330250'), cep_to_coords('54470290'), cep_to_coords('53439500'), cep_to_coords('50761290'), cep_to_coords('54768810'), cep_to_coords('51110320'), cep_to_coords('55299445'), cep_to_coords('54725000'), cep_to_coords('53402420'), cep_to_coords('52120280'), cep_to_coords('52080160'), cep_to_coords('50020470'), cep_to_coords('51270290'), cep_to_coords('52111141'), cep_to_coords('50040910'), cep_to_coords('50860220'), cep_to_coords('52110351'), cep_to_coords('55291050'), cep_to_coords('54080381'), cep_to_coords('54330425'), cep_to_coords('54280530'), cep_to_coords('54245260'), cep_to_coords('54100550'), cep_to_coords('54130230'), cep_to_coords('50910580'), cep_to_coords('54420270'), cep_to_coords('54430231'), cep_to_coords('54480240'), cep_to_coords('51230060'), cep_to_coords('51021430'), cep_to_coords('52030040'), cep_to_coords('54515509'), cep_to_coords('51335025'), cep_to_coords('54210010'), cep_to_coords('52041310'), cep_to_coords('52130310'), cep_to_coords('51021290'), cep_to_coords('53450000'), cep_to_coords('53020310'), cep_to_coords('53429280'), cep_to_coords('52111710'), cep_to_coords('52061420'), cep_to_coords('50761650'), cep_to_coords('50730060'), cep_to_coords('52090350'), cep_to_coords('52050300'), cep_to_coords('55016445'), cep_to_coords('56503700'), cep_to_coords('54753040'), cep_to_coords('50740260'), cep_to_coords('54280731'), cep_to_coords('50610520'), cep_to_coords('50940520'), cep_to_coords('53409480'), cep_to_coords('54160458'), cep_to_coords('54470220'), cep_to_coords('54315550'), cep_to_coords('55016375'), cep_to_coords('50820500'), cep_to_coords('56506610'), cep_to_coords('56505230'), cep_to_coords('54090060'), cep_to_coords('54505260'), cep_to_coords('54765160'), cep_to_coords('52191291'), cep_to_coords('56159230'), cep_to_coords('51011685'), cep_to_coords('52240030'), cep_to_coords('58038600'), cep_to_coords('50771300'), cep_to_coords('55014330'), cep_to_coords('55636000'), cep_to_coords('54515480'), cep_to_coords('54330320'), cep_to_coords('50710390'), cep_to_coords('55385000'), cep_to_coords('53407265'), cep_to_coords('55614014'), cep_to_coords('53250400'), cep_to_coords('52130430'), cep_to_coords('54220100'), cep_to_coords('52130020'), cep_to_coords('50600000'), cep_to_coords('55604070'), cep_to_coords('29071971'), cep_to_coords('52081025'), cep_to_coords('50610240'), cep_to_coords('56140000'), cep_to_coords('53429190'), cep_to_coords('50751030'), cep_to_coords('53265464'), cep_to_coords('53421241'), cep_to_coords('56912460'), cep_to_coords('52070620'), cep_to_coords('52090790'), cep_to_coords('50040000'), cep_to_coords('52071090'), cep_to_coords('55034540'), cep_to_coords('55030200'), cep_to_coords('50080090'), cep_to_coords('53370680'), cep_to_coords('53250040'), cep_to_coords('55612290'), cep_to_coords('55608380'), cep_to_coords('53110117'), cep_to_coords('50740290'), cep_to_coords('52390190'), cep_to_coords('55612650'), cep_to_coords('21180020'), cep_to_coords('51180020'), cep_to_coords('54170640'), cep_to_coords('50780140'), cep_to_coords('50731270'), cep_to_coords('50721710'), cep_to_coords('52111030'), cep_to_coords('50870370'), cep_to_coords('55618000'), cep_to_coords('50710340'), cep_to_coords('53550150'), cep_to_coords('53580000'), cep_to_coords('53413500'), cep_to_coords('53441090'), cep_to_coords('54260080'), cep_to_coords('54759315'), cep_to_coords('55150150'), cep_to_coords('53407245'), cep_to_coords('51260330'), cep_to_coords('54580333'), cep_to_coords('50731430'), cep_to_coords('53370810'), cep_to_coords('51230280'), cep_to_coords('53620640'), cep_to_coords('55485000'), cep_to_coords('56830000'), cep_to_coords('50875251'), cep_to_coords('50870600'), cep_to_coords('52130102'), cep_to_coords('50080200'), cep_to_coords('50780170'), cep_to_coords('56912190'), cep_to_coords('56912490'), cep_to_coords('53417070'), cep_to_coords('52081033'), cep_to_coords('51346070'), cep_to_coords('51200060'), cep_to_coords('56909720'), cep_to_coords('05690000'), cep_to_coords('51330471'), cep_to_coords('55006280'), cep_to_coords('52120540'), cep_to_coords('53120540'), cep_to_coords('55022260'), cep_to_coords('54120570'), cep_to_coords('55012140'), cep_to_coords('56306000'), cep_to_coords('53610000'), cep_to_coords('54495110'), cep_to_coords('55016360'), cep_to_coords('51340190'), cep_to_coords('53413240'), cep_to_coords('50090650'), cep_to_coords('55024180'), cep_to_coords('53441300'), cep_to_coords('55012035'), cep_to_coords('55612010'), cep_to_coords('55604605'), cep_to_coords('50830380'), cep_to_coords('50781390'), cep_to_coords('52077290'), cep_to_coords('53040170'), cep_to_coords('54325460'), cep_to_coords('54325395'), cep_to_coords('55036550'), cep_to_coords('55004230'), cep_to_coords('55022660'), cep_to_coords('50670140'), cep_to_coords('50750220'), cep_to_coords('53130515'), cep_to_coords('55155030'), cep_to_coords('55026190'), cep_to_coords('53433510'), cep_to_coords('54525470'), cep_to_coords('55294260'), cep_to_coords('50760560'), cep_to_coords('50711130'), cep_to_coords('55012550'), cep_to_coords('53110040'), cep_to_coords('52021000'), cep_to_coords('55014005'), cep_to_coords('54150080'), cep_to_coords('55018150'), cep_to_coords('52031050'), cep_to_coords('53417330'), cep_to_coords('52191080'), cep_to_coords('53160180'), cep_to_coords('52050030'), cep_to_coords('55554000'), cep_to_coords('54330435'), cep_to_coords('50761420'), cep_to_coords('53110070'), cep_to_coords('54325185'), cep_to_coords('51111130'), cep_to_coords('56511160'), cep_to_coords('54720315'), cep_to_coords('54100313'), cep_to_coords('55018410'), cep_to_coords('54786310'), cep_to_coords('55030521'), cep_to_coords('52111170'), cep_to_coords('51340155'), cep_to_coords('56308250'), cep_to_coords('55024720'), cep_to_coords('53421760'), cep_to_coords('53630145'), cep_to_coords('52121010'), cep_to_coords('50865120'), cep_to_coords('52051460'), cep_to_coords('53429630'), cep_to_coords('53120010'), cep_to_coords('52021150'), cep_to_coords('54210180'), cep_to_coords('52120140'), cep_to_coords('50090000'), cep_to_coords('50060530'), cep_to_coords('51346080'), cep_to_coords('55024460'), cep_to_coords('54710120'), cep_to_coords('52110250'), cep_to_coords('26079000'), cep_to_coords('52090271'), cep_to_coords('50040240'), cep_to_coords('51420080'), cep_to_coords('55014707'), cep_to_coords('55014000'), cep_to_coords('55014020'), cep_to_coords('55012120'), cep_to_coords('54080310'), cep_to_coords('51350170'), cep_to_coords('56909472'), cep_to_coords('56909670'), cep_to_coords('56909680'), cep_to_coords('56903267'), cep_to_coords('56903030'), cep_to_coords('56906260'), cep_to_coords('56906330'), cep_to_coords('56906250'), cep_to_coords('56906310'), cep_to_coords('55154590'), cep_to_coords('56906220'), cep_to_coords('56660000'), cep_to_coords('50870410'), cep_to_coords('56906160'), cep_to_coords('50630460'), cep_to_coords('05424000'), cep_to_coords('50770470'), cep_to_coords('53350170'), cep_to_coords('56906525'), cep_to_coords('50780330'), cep_to_coords('55175000'), cep_to_coords('53630070'), cep_to_coords('52291665'), cep_to_coords('55031636'), cep_to_coords('53220060'), cep_to_coords('54440680'), cep_to_coords('52170330'), cep_to_coords('55816270'), cep_to_coords('55195572'), cep_to_coords('50740470'), cep_to_coords('53640120'), cep_to_coords('51150630'), cep_to_coords('54410240'), cep_to_coords('50760008'), cep_to_coords('52090270'), cep_to_coords('52130040'), cep_to_coords('50690430'), cep_to_coords('52130023'), cep_to_coords('50761770'), cep_to_coords('52070210'), cep_to_coords('52090000'), cep_to_coords('50740310'), cep_to_coords('54110081'), cep_to_coords('50980630'), cep_to_coords('53435750'), cep_to_coords('50060570'), cep_to_coords('50060571'), cep_to_coords('56508227'), cep_to_coords('54786120'), cep_to_coords('55819970'), cep_to_coords('51203090'), cep_to_coords('55295110'), cep_to_coords('50761440'), cep_to_coords('54771400'), cep_to_coords('54774400'), cep_to_coords('54070150'), cep_to_coords('54070170'), cep_to_coords('53250520'), cep_to_coords('52110430'), cep_to_coords('55296180'), cep_to_coords('55295280'), cep_to_coords('51020040'), cep_to_coords('53554009'), cep_to_coords('51170050'), cep_to_coords('52280040'), cep_to_coords('50660150'), cep_to_coords('55012460'), cep_to_coords('55016435'), cep_to_coords('55012040'), cep_to_coords('56511060'), cep_to_coords('55292260'), cep_to_coords('56509807'), cep_to_coords('56506000'), cep_to_coords('53620812'), cep_to_coords('55292590'), cep_to_coords('51190650'), cep_to_coords('53625050'), cep_to_coords('53170110'), cep_to_coords('54705140'), cep_to_coords('55296520'), cep_to_coords('58039081'), cep_to_coords('50720660'), cep_to_coords('50100220'), cep_to_coords('50660420'), cep_to_coords('53413030'), cep_to_coords('56915010'), cep_to_coords('56509570'), cep_to_coords('50791170'), cep_to_coords('56912000'), cep_to_coords('50680901'), cep_to_coords('55608220'), cep_to_coords('53280160'), cep_to_coords('52090195'), cep_to_coords('56509150'), cep_to_coords('53210820'), cep_to_coords('53401105'), cep_to_coords('52280034'), cep_to_coords('54440072'), cep_to_coords('53585165'), cep_to_coords('55298470'), cep_to_coords('52280252'), cep_to_coords('52210350'), cep_to_coords('54420700'), cep_to_coords('53110590'), cep_to_coords('53444420'), cep_to_coords('52120110'), cep_to_coords('55020106'), cep_to_coords('55021395'), cep_to_coords('55602633'), cep_to_coords('53330230'), cep_to_coords('55540999'), cep_to_coords('53407810'), cep_to_coords('52041230'), cep_to_coords('52211440'), cep_to_coords('50100130'), cep_to_coords('51110110'), cep_to_coords('55021330'), cep_to_coords('52010230'), cep_to_coords('53439520'), cep_to_coords('54535180'), cep_to_coords('55296120'), cep_to_coords('52061270'), cep_to_coords('53435701'), cep_to_coords('54360168'), cep_to_coords('56308440'), cep_to_coords('50980660'), cep_to_coords('55641390'), cep_to_coords('51160449'), cep_to_coords('53160655'), cep_to_coords('54470360'), cep_to_coords('50680430'), cep_to_coords('50771510'), cep_to_coords('53423280'), cep_to_coords('53435660'), cep_to_coords('50730270'), cep_to_coords('52170270'), cep_to_coords('55612030'), cep_to_coords('55612170'), cep_to_coords('50751250'), cep_to_coords('54220675'), cep_to_coords('54210570'), cep_to_coords('52221060'), cep_to_coords('50870100'), cep_to_coords('51230315'), cep_to_coords('53439790'), cep_to_coords('51180340'), cep_to_coords('50100360'), cep_to_coords('56912350'), cep_to_coords('56900906'), cep_to_coords('56903230'), cep_to_coords('56912310'), cep_to_coords('56900030'), cep_to_coords('56903431'), cep_to_coords('56903520'), cep_to_coords('56903210'), cep_to_coords('56903350'), cep_to_coords('56903500'), cep_to_coords('51240615'), cep_to_coords('56930000'), cep_to_coords('51170490'), cep_to_coords('55190794'), cep_to_coords('53280010'), cep_to_coords('54768120'), cep_to_coords('53435010'), cep_to_coords('54753370'), cep_to_coords('54753710'), cep_to_coords('54777280'), cep_to_coords('54762610'), cep_to_coords('55610200'), cep_to_coords('52111155'), cep_to_coords('54756780'), cep_to_coords('54759105'), cep_to_coords('56504150'), cep_to_coords('50970120'), cep_to_coords('53240400'), cep_to_coords('55190380'), cep_to_coords('55031460'), cep_to_coords('55192140'), cep_to_coords('55018292'), cep_to_coords('55154070'), cep_to_coords('55179473'), cep_to_coords('53437540'), cep_to_coords('53060822'), cep_to_coords('53350250'), cep_to_coords('56740000'), cep_to_coords('54210360'), cep_to_coords('52221025'), cep_to_coords('52031220'), cep_to_coords('56316710'), cep_to_coords('55294572'), cep_to_coords('56903653'), cep_to_coords('55390000'), cep_to_coords('55026460'), cep_to_coords('55641140'), cep_to_coords('55612180'), cep_to_coords('55604130'), cep_to_coords('55604060'), cep_to_coords('55608350'), cep_to_coords('52081032'), cep_to_coords('55031450'), cep_to_coords('51300070'), cep_to_coords('55112000'), cep_to_coords('50820390'), cep_to_coords('50870270'), cep_to_coords('51270510'), cep_to_coords('50731380'), cep_to_coords('54762787'), cep_to_coords('50050470'), cep_to_coords('55813900'), cep_to_coords('54430440'), cep_to_coords('50761562'), cep_to_coords('55298070'), cep_to_coords('54220080'), cep_to_coords('54220780'), cep_to_coords('54480440'), cep_to_coords('54735185'), cep_to_coords('54730070'), cep_to_coords('53120120'), cep_to_coords('55297814'), cep_to_coords('55291665'), cep_to_coords('55101000'), cep_to_coords('55038510'), cep_to_coords('55292400'), cep_to_coords('54280690'), cep_to_coords('53290040'), cep_to_coords('55038565'), cep_to_coords('53630000'), cep_to_coords('54420590'), cep_to_coords('50060030'), cep_to_coords('55755000'), cep_to_coords('53417290'), cep_to_coords('50711520'), cep_to_coords('54460130'), cep_to_coords('53413190'), cep_to_coords('50110030'), cep_to_coords('50980000'), cep_to_coords('52031110'), cep_to_coords('50900441'), cep_to_coords('56903491'), cep_to_coords('54768200'), cep_to_coords('50960450'), cep_to_coords('54090381'), cep_to_coords('50640700'), cep_to_coords('54220160'), cep_to_coords('55022796'), cep_to_coords('52121280'), cep_to_coords('53435730'), cep_to_coords('56913311'), cep_to_coords('56903311'), cep_to_coords('57000000'), cep_to_coords('54230000'), cep_to_coords('53421640'), cep_to_coords('53290050'), cep_to_coords('54703510'), cep_to_coords('52041620'), cep_to_coords('54765220'), cep_to_coords('52041320'), cep_to_coords('50730070'), cep_to_coords('50680360'), cep_to_coords('54525120'), cep_to_coords('51330230'), cep_to_coords('50860150'), cep_to_coords('55038050'), cep_to_coords('55608095'), cep_to_coords('53444130'), cep_to_coords('53405400'), cep_to_coords('50870540'), cep_to_coords('55643310'), cep_to_coords('55022375'), cep_to_coords('55016380'), cep_to_coords('53130300'), cep_to_coords('52130080'), cep_to_coords('50060590'), cep_to_coords('50750560'), cep_to_coords('09220000'), cep_to_coords('54280795'), cep_to_coords('54410291'), cep_to_coords('53060330'), cep_to_coords('53580760'), cep_to_coords('52040270'), cep_to_coords('52110185'), cep_to_coords('52111200'), cep_to_coords('50060260'), cep_to_coords('50711310'), cep_to_coords('53409030'), cep_to_coords('54400120'), cep_to_coords('53530404'), cep_to_coords('54759620'), cep_to_coords('50721740'), cep_to_coords('52050390'), cep_to_coords('50750145'), cep_to_coords('24735140'), cep_to_coords('51021100'), cep_to_coords('56906100'), cep_to_coords('56912250'), cep_to_coords('56903660'), cep_to_coords('56903234'), cep_to_coords('56903040'), cep_to_coords('56903265'), cep_to_coords('56907170'), cep_to_coords('55641810'), cep_to_coords('52031300'), cep_to_coords('50500000'), cep_to_coords('52041290'), cep_to_coords('53130310'), cep_to_coords('54120180'), cep_to_coords('54270410'), cep_to_coords('52121210'), cep_to_coords('51270560'), cep_to_coords('52081010'), cep_to_coords('54759265'), cep_to_coords('52041539'), cep_to_coords('55644375'), cep_to_coords('52031240'), cep_to_coords('50100330'), cep_to_coords('52170020'), cep_to_coords('53020320'), cep_to_coords('53130090'), cep_to_coords('52031000'), cep_to_coords('53080590'), cep_to_coords('54768662'), cep_to_coords('54768170'), cep_to_coords('54753360'), cep_to_coords('55192400'), cep_to_coords('52050565'), cep_to_coords('50060230'), cep_to_coords('52110125'), cep_to_coords('53010360'), cep_to_coords('53270260'), cep_to_coords('52041220'), cep_to_coords('53435220'), cep_to_coords('53441360'), cep_to_coords('52211151'), cep_to_coords('50760100'), cep_to_coords('54330214'), cep_to_coords('54589540'), cep_to_coords('54768847'), cep_to_coords('53620793'), cep_to_coords('55614240'), cep_to_coords('55380000'), cep_to_coords('57968000'), cep_to_coords('55602971'), cep_to_coords('55604330'), cep_to_coords('51170060'), cep_to_coords('51180500'), cep_to_coords('51011320'), cep_to_coords('55038320'), cep_to_coords('53416550'), cep_to_coords('51340720'), cep_to_coords('50870070'), cep_to_coords('54340720'), cep_to_coords('51190240'), cep_to_coords('54230192'), cep_to_coords('53110510'), cep_to_coords('50720610'), cep_to_coords('54450000'), cep_to_coords('55022420'), cep_to_coords('54580470'), cep_to_coords('50070300'), cep_to_coords('55304000'), cep_to_coords('54170051'), cep_to_coords('55018320'), cep_to_coords('55811220'), cep_to_coords('54100110'), cep_to_coords('54360000'), cep_to_coords('50750500'), cep_to_coords('52120400'), cep_to_coords('54420150'), cep_to_coords('56670000'), cep_to_coords('56667000'), cep_to_coords('53110250'), cep_to_coords('52031190'), cep_to_coords('54270991'), cep_to_coords('55018010'), cep_to_coords('54230075'), cep_to_coords('52070251'), cep_to_coords('70000000'), cep_to_coords('54440190'), cep_to_coords('52291193'), cep_to_coords('50080681'), cep_to_coords('53240160'), cep_to_coords('55296570'), cep_to_coords('53437410'), cep_to_coords('52050174'), cep_to_coords('50751350'), cep_to_coords('56512360'), cep_to_coords('55195112'), cep_to_coords('52191090'), cep_to_coords('54352240'), cep_to_coords('53360160'), cep_to_coords('52120070'), cep_to_coords('51320350'), cep_to_coords('55641410'), cep_to_coords('53437680'), cep_to_coords('52165200'), cep_to_coords('52051090'), cep_to_coords('52090351'), cep_to_coords('50780620'), cep_to_coords('55010350'), cep_to_coords('53437570'), cep_to_coords('53413710'), cep_to_coords('52041100'), cep_to_coords('54535991'), cep_to_coords('54505901'), cep_to_coords('50750000'), cep_to_coords('53605003'), cep_to_coords('50870260'), cep_to_coords('54765000'), cep_to_coords('52080530'), cep_to_coords('53405160'), cep_to_coords('52051180'), cep_to_coords('54100161'), cep_to_coords('53060030'), cep_to_coords('54330186'), cep_to_coords('51230230'), cep_to_coords('51350510'), cep_to_coords('55194133'), cep_to_coords('54330070'), cep_to_coords('53422560'), cep_to_coords('50791060'), cep_to_coords('51230320'), cep_to_coords('56512250'), cep_to_coords('54310410'), cep_to_coords('53407715'), cep_to_coords('53413510'), cep_to_coords('51340210'), cep_to_coords('50770630'), cep_to_coords('51320630'), cep_to_coords('51290610'), cep_to_coords('51345003'), cep_to_coords('50080705'), cep_to_coords('50020030'), cep_to_coords('54100260'), cep_to_coords('54080055'), cep_to_coords('51320330'), cep_to_coords('50721000'), cep_to_coords('53444180'), cep_to_coords('51010380'), cep_to_coords('56903240'), cep_to_coords('56903280'), cep_to_coords('56912110'), cep_to_coords('56903100'), cep_to_coords('53402680'), cep_to_coords('54768110'), cep_to_coords('53431697'), cep_to_coords('53080150'), cep_to_coords('55010240'), cep_to_coords('55022380'), cep_to_coords('55019365'), cep_to_coords('51190060'), cep_to_coords('50010010'), cep_to_coords('52280255'), cep_to_coords('52210230'), cep_to_coords('50070095'), cep_to_coords('55024005'), cep_to_coords('52031320'), cep_to_coords('52130190'), cep_to_coords('53230440'), cep_to_coords('53240370'), cep_to_coords('52191000'), cep_to_coords('53260360'), cep_to_coords('55196043'), cep_to_coords('53510360'), cep_to_coords('54774360'), cep_to_coords('50680400'), cep_to_coords('54780090'), cep_to_coords('50740610'), cep_to_coords('54420161'), cep_to_coords('56314550'), cep_to_coords('56163000'), cep_to_coords('55195199'), cep_to_coords('55194085'), cep_to_coords('55194220'), cep_to_coords('55192280'), cep_to_coords('55192380'), cep_to_coords('52080525'), cep_to_coords('52120185'), cep_to_coords('50110291'), cep_to_coords('53423420'), cep_to_coords('52041572'), cep_to_coords('52030181'), cep_to_coords('53439370'), cep_to_coords('56308155'), cep_to_coords('56320110'), cep_to_coords('54753750'), cep_to_coords('54759197'), cep_to_coords('56220000'), cep_to_coords('54510390'), cep_to_coords('54505970'), cep_to_coords('56912163'), cep_to_coords('56903530'), cep_to_coords('52040140'), cep_to_coords('53110320'), cep_to_coords('54505001'), cep_to_coords('53370045'), cep_to_coords('53240330'), cep_to_coords('53407120'), cep_to_coords('50910230'), cep_to_coords('50820380'), cep_to_coords('53620049'), cep_to_coords('51240020'), cep_to_coords('53610090'), cep_to_coords('53350230'), cep_to_coords('53190160'), cep_to_coords('53422280'), cep_to_coords('52011903'), cep_to_coords('50731240'), cep_to_coords('50660120'), cep_to_coords('50850350'), cep_to_coords('56318530'), cep_to_coords('56316666'), cep_to_coords('55010320'), cep_to_coords('50781480'), cep_to_coords('53441280'), cep_to_coords('53433620'), cep_to_coords('52081070'), cep_to_coords('54210530'), cep_to_coords('50850450'), cep_to_coords('56912470'), cep_to_coords('50640580'), cep_to_coords('54830570'), cep_to_coords('54230570'), cep_to_coords('53080180'), cep_to_coords('55044180'), cep_to_coords('50900541'), cep_to_coords('53625055'), cep_to_coords('54410110'), cep_to_coords('52030000'), cep_to_coords('53030020'), cep_to_coords('55293970'), cep_to_coords('50870050'), cep_to_coords('53330180'), cep_to_coords('53220020'), cep_to_coords('50110470'), cep_to_coords('50820580'), cep_to_coords('53429120'), cep_to_coords('50110280'), cep_to_coords('50110210'), cep_to_coords('50870650'), cep_to_coords('53130240'), cep_to_coords('52030210'), cep_to_coords('51021270'), cep_to_coords('52131122'), cep_to_coords('55614610'), cep_to_coords('50970130'), cep_to_coords('50690000'), cep_to_coords('55295410'), cep_to_coords('53421231'), cep_to_coords('51240050'), cep_to_coords('53441255'), cep_to_coords('52120330'), cep_to_coords('50710110'), cep_to_coords('55296350'), cep_to_coords('55296260'), cep_to_coords('56506470'), cep_to_coords('52211142'), cep_to_coords('50810530'), cep_to_coords('55006160'), cep_to_coords('56515070'), cep_to_coords('55813390'), cep_to_coords('54470490'), cep_to_coords('54250181'), cep_to_coords('05687000'), cep_to_coords('53130520'), cep_to_coords('56509295'), cep_to_coords('50630290'), cep_to_coords('56306040'), cep_to_coords('50100400'), cep_to_coords('54740640'), cep_to_coords('56784000'), cep_to_coords('56150000'), cep_to_coords('56509460'), cep_to_coords('51020320'), cep_to_coords('54430180'), cep_to_coords('50720365'), cep_to_coords('50751077'), cep_to_coords('54330570'), cep_to_coords('51030400'), cep_to_coords('54100010'), cep_to_coords('54110040'), cep_to_coords('50790280'), cep_to_coords('52221040'), cep_to_coords('55325000'), cep_to_coords('53441206'), cep_to_coords('53060543'), cep_to_coords('54768140'), cep_to_coords('55295080'), cep_to_coords('55100078'), cep_to_coords('50810200'), cep_to_coords('52070290'), cep_to_coords('50980750'), cep_to_coords('50781670'), cep_to_coords('52050170'), cep_to_coords('54745150'), cep_to_coords('55292430'), cep_to_coords('55291000'), cep_to_coords('54210323'), cep_to_coords('50770540'), cep_to_coords('54768740'), cep_to_coords('55178000'), cep_to_coords('50040400'), cep_to_coords('50920525'), cep_to_coords('52120312'), cep_to_coords('55155490'), cep_to_coords('51340670'), cep_to_coords('55006281'), cep_to_coords('54589000'), cep_to_coords('54771750'), cep_to_coords('52011890'), cep_to_coords('51340550'), cep_to_coords('52061311'), cep_to_coords('56210000'), cep_to_coords('52120380'), cep_to_coords('52091240'), cep_to_coords('50610130'), cep_to_coords('53080820'), cep_to_coords('53230430'), cep_to_coords('52110070'), cep_to_coords('52011010'), cep_to_coords('54767320'), cep_to_coords('55643662'), cep_to_coords('58052160'), cep_to_coords('54753110'), cep_to_coords('51345570'), cep_to_coords('54470570'), cep_to_coords('55612450'), cep_to_coords('56328220'), cep_to_coords('50110150'), cep_to_coords('55010740'), cep_to_coords('55010340'), cep_to_coords('53545690'), cep_to_coords('54100140'), cep_to_coords('52030720'), cep_to_coords('54756042'), cep_to_coords('50680620'), cep_to_coords('50711180'), cep_to_coords('50670160'), cep_to_coords('50770650'), cep_to_coords('50620000'), cep_to_coords('50620610'), cep_to_coords('50630310'), cep_to_coords('50760487'), cep_to_coords('52160233'), cep_to_coords('50620660'), cep_to_coords('50721450'), cep_to_coords('55608477'), cep_to_coords('54330540'), cep_to_coords('52060170'), cep_to_coords('50670480'), cep_to_coords('51260070'), cep_to_coords('55020230'), cep_to_coords('54250380'), cep_to_coords('53437720'), cep_to_coords('53020140'), cep_to_coords('50771330'), cep_to_coords('50090060'), cep_to_coords('50711000'), cep_to_coords('50640450'), cep_to_coords('54230720'), cep_to_coords('55024830'), cep_to_coords('56922000'), cep_to_coords('50970163'), cep_to_coords('50970445'), cep_to_coords('52021060'), cep_to_coords('52090190'), cep_to_coords('52090495'), cep_to_coords('50741210'), cep_to_coords('54735790'), cep_to_coords('54705310'), cep_to_coords('52130090'), cep_to_coords('53370210'), cep_to_coords('50970270'), cep_to_coords('55034360'), cep_to_coords('52390030'), cep_to_coords('52221250'), cep_to_coords('55240970'), cep_to_coords('51240120'), cep_to_coords('52121000'), cep_to_coords('55192070'), cep_to_coords('54753782'), cep_to_coords('50741310'), cep_to_coords('55294054'), cep_to_coords('52070443'), cep_to_coords('52041390'), cep_to_coords('50110820'), cep_to_coords('50110220'), cep_to_coords('55612470'), cep_to_coords('55614280'), cep_to_coords('54440360'), cep_to_coords('52011126'), cep_to_coords('50020000')


# In[62]:


print(coordenadasrow425to5425)


# In[63]:


row425to5425


# In[64]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in row425to5425.tolist():
    result.append(''.join(pattern.findall(item)))


# In[65]:


print(result)


# In[100]:


dfrow425to5425 = pd.DataFrame(coordenadasrow425to5425, result)


# In[101]:


dfrow425to5425


# In[102]:


dfrow425to5425.reset_index(level=0, inplace=True)


# In[103]:


dfrow425to5425


# In[104]:


dfrow425to5425 = dfrow425to5425.rename(columns={'index':'cep'}) 


# In[105]:


dfrow425to5425


# In[ ]:


dfrow425to5425.reset_index(level=0, inplace=True)


# In[106]:


bancoesusalltabsrais2019nodupsCEPS[['id']][425:5426]


# In[107]:


id425_5426 = bancoesusalltabsrais2019nodupsCEPS[['id']][425:5426]


# In[108]:


id425_5426


# In[109]:


id425_5426.reset_index(level=0, inplace=True)


# In[110]:


id425_5426


# In[113]:


dfrow425to5425['id'] = id425_5426['id']
dfrow425to5425['index'] = id425_5426['index']


# In[114]:


dfrow425to5425


# In[115]:


dfrow425to5425[dfrow425to5425.columns[[4,3,0,1,2]]]


# In[116]:


dfrow425to5425 = dfrow425to5425[dfrow425to5425.columns[[4,3,0,1,2]]]


# In[117]:


dfrow425to5425


# In[119]:


dfrow425to5425.to_excel('dfrow425to5425latlong.xlsx')


# # bancoesusalltabsrais2019nodupsCEPS[5426:10426]

# In[10]:


bancoesusalltabsrais2019nodupsCEPS[5426:10426]


# In[11]:


row5426to10425 = bancoesusalltabsrais2019nodupsCEPS[5426:10426]


# In[12]:


row5426to10425


# In[13]:


row5426to10425.update("cep_to_coords('" + row5426to10425[['cep']].astype(str) + "'),")
print(row5426to10425)


# In[14]:


row5426to10425


# In[15]:


row5426to10425 = row5426to10425.loc[:,'cep']


# In[16]:


row5426to10425


# In[17]:


print(' '.join(row5426to10425))#.tolist()


# In[18]:


coordenadasrow5426to10425 = cep_to_coords('53575051'), cep_to_coords('50640390'), cep_to_coords('53170495'), cep_to_coords('53200060'), cep_to_coords('53590000'), cep_to_coords('53350260'), cep_to_coords('52060420'), cep_to_coords('53110730'), cep_to_coords('53520140'), cep_to_coords('53407000'), cep_to_coords('50640520'), cep_to_coords('55420380'), cep_to_coords('54400620'), cep_to_coords('53510370'), cep_to_coords('53510330'), cep_to_coords('51350320'), cep_to_coords('53560140'), cep_to_coords('53525580'), cep_to_coords('56909205'), cep_to_coords('50790370'), cep_to_coords('57010003'), cep_to_coords('51011020'), cep_to_coords('53020290'), cep_to_coords('56512140'), cep_to_coords('56512200'), cep_to_coords('52061003'), cep_to_coords('50850040'), cep_to_coords('53020110'), cep_to_coords('55604360'), cep_to_coords('51345005'), cep_to_coords('52031231'), cep_to_coords('53320040'), cep_to_coords('50920420'), cep_to_coords('54400290'), cep_to_coords('55297310'), cep_to_coords('51250120'), cep_to_coords('52221080'), cep_to_coords('53419340'), cep_to_coords('50830120'), cep_to_coords('56512170'), cep_to_coords('54270456'), cep_to_coords('55299510'), cep_to_coords('52091071'), cep_to_coords('50660240'), cep_to_coords('53070650'), cep_to_coords('54786001'), cep_to_coords('55190389'), cep_to_coords('53437110'), cep_to_coords('54435325'), cep_to_coords('51270745'), cep_to_coords('56515236'), cep_to_coords('53441495'), cep_to_coords('54310285'), cep_to_coords('54140680'), cep_to_coords('54280246'), cep_to_coords('53425740'), cep_to_coords('51110300'), cep_to_coords('54330375'), cep_to_coords('50910470'), cep_to_coords('54220330'), cep_to_coords('52291080'), cep_to_coords('51030021'), cep_to_coords('52131150'), cep_to_coords('54765495'), cep_to_coords('51345110'), cep_to_coords('54120090'), cep_to_coords('53210230'), cep_to_coords('50120310'), cep_to_coords('56654000'), cep_to_coords('55026130'), cep_to_coords('56310200'), cep_to_coords('54774395'), cep_to_coords('54759420'), cep_to_coords('52041570'), cep_to_coords('55602685'), cep_to_coords('53520030'), cep_to_coords('50781730'), cep_to_coords('50610040'), cep_to_coords('50620060'), cep_to_coords('52080030'), cep_to_coords('53060485'), cep_to_coords('50920560'), cep_to_coords('53090320'), cep_to_coords('50650090'), cep_to_coords('55030135'), cep_to_coords('53435330'), cep_to_coords('51330210'), cep_to_coords('50865000'), cep_to_coords('29061962'), cep_to_coords('52110150'), cep_to_coords('54340280'), cep_to_coords('54340380'), cep_to_coords('52111580'), cep_to_coords('50760740'), cep_to_coords('52191750'), cep_to_coords('51240390'), cep_to_coords('54280113'), cep_to_coords('55016080'), cep_to_coords('53210087'), cep_to_coords('51350560'), cep_to_coords('55024230'), cep_to_coords('56332125'), cep_to_coords('53425790'), cep_to_coords('53150590'), cep_to_coords('53441155'), cep_to_coords('52011300'), cep_to_coords('53300050'), cep_to_coords('55440000'), cep_to_coords('53220100'), cep_to_coords('50900000'), cep_to_coords('56912160'), cep_to_coords('63290000'), cep_to_coords('56909290'), cep_to_coords('56907080'), cep_to_coords('56912151'), cep_to_coords('56903090'), cep_to_coords('56912010'), cep_to_coords('56909650'), cep_to_coords('56912555'), cep_to_coords('56909050'), cep_to_coords('54230490'), cep_to_coords('56508205'), cep_to_coords('53444260'), cep_to_coords('53405440'), cep_to_coords('56750000'), cep_to_coords('51180190'), cep_to_coords('53416420'), cep_to_coords('53409330'), cep_to_coords('52040000'), cep_to_coords('53150435'), cep_to_coords('53422380'), cep_to_coords('54750050'), cep_to_coords('52091025'), cep_to_coords('52160060'), cep_to_coords('53110511'), cep_to_coords('55014530'), cep_to_coords('55004350'), cep_to_coords('50910170'), cep_to_coords('55604220'), cep_to_coords('55604040'), cep_to_coords('51030230'), cep_to_coords('54756032'), cep_to_coords('54765410'), cep_to_coords('55024785'), cep_to_coords('55012430'), cep_to_coords('50770640'), cep_to_coords('51170130'), cep_to_coords('52061220'), cep_to_coords('50670520'), cep_to_coords('53540200'), cep_to_coords('54771480'), cep_to_coords('52280517'), cep_to_coords('50690370'), cep_to_coords('53370640'), cep_to_coords('52190010'), cep_to_coords('54280666'), cep_to_coords('50830340'), cep_to_coords('50830140'), cep_to_coords('51011530'), cep_to_coords('54440320'), cep_to_coords('54310240'), cep_to_coords('51300400'), cep_to_coords('54753460'), cep_to_coords('50860240'), cep_to_coords('55024750'), cep_to_coords('50244000'), cep_to_coords('52020180'), cep_to_coords('50690340'), cep_to_coords('53130490'), cep_to_coords('51330150'), cep_to_coords('55022580'), cep_to_coords('55014520'), cep_to_coords('53580120'), cep_to_coords('50740445'), cep_to_coords('54437230'), cep_to_coords('54771784'), cep_to_coords('53530660'), cep_to_coords('53550147'), cep_to_coords('53043318'), cep_to_coords('51030680'), cep_to_coords('54580205'), cep_to_coords('53120190'), cep_to_coords('55294595'), cep_to_coords('50850312'), cep_to_coords('53439440'), cep_to_coords('51220230'), cep_to_coords('50740460'), cep_to_coords('50192301'), cep_to_coords('51270100'), cep_to_coords('53320130'), cep_to_coords('56503042'), cep_to_coords('50870570'), cep_to_coords('55022460'), cep_to_coords('55016480'), cep_to_coords('56433480'), cep_to_coords('53540040'), cep_to_coords('53425765'), cep_to_coords('55021370'), cep_to_coords('50740390'), cep_to_coords('51300260'), cep_to_coords('50790400'), cep_to_coords('51240460'), cep_to_coords('50760330'), cep_to_coords('54240615'), cep_to_coords('55020120'), cep_to_coords('56912200'), cep_to_coords('52191407'), cep_to_coords('51270000'), cep_to_coords('54120030'), cep_to_coords('53610400'), cep_to_coords('54230117'), cep_to_coords('51350050'), cep_to_coords('55031000'), cep_to_coords('55908000'), cep_to_coords('53130320'), cep_to_coords('53080600'), cep_to_coords('51350160'), cep_to_coords('52120306'), cep_to_coords('52490050'), cep_to_coords('50940235'), cep_to_coords('50741170'), cep_to_coords('52080230'), cep_to_coords('50670430'), cep_to_coords('54460140'), cep_to_coords('51190450'), cep_to_coords('51021470'), cep_to_coords('52130320'), cep_to_coords('50740100'), cep_to_coords('56506410'), cep_to_coords('54415100'), cep_to_coords('54080475'), cep_to_coords('54070260'), cep_to_coords('55293050'), cep_to_coords('50760090'), cep_to_coords('54406020'), cep_to_coords('52221000'), cep_to_coords('56503340'), cep_to_coords('53070540'), cep_to_coords('52121040'), cep_to_coords('50761417'), cep_to_coords('55016500'), cep_to_coords('50810270'), cep_to_coords('54762200'), cep_to_coords('54260140'), cep_to_coords('53437380'), cep_to_coords('54777460'), cep_to_coords('53330540'), cep_to_coords('53130580'), cep_to_coords('54330221'), cep_to_coords('52041380'), cep_to_coords('56326190'), cep_to_coords('55030165'), cep_to_coords('50800340'), cep_to_coords('50790540'), cep_to_coords('54360080'), cep_to_coords('54300055'), cep_to_coords('56304920'), cep_to_coords('50791560'), cep_to_coords('53407730'), cep_to_coords('50751120'), cep_to_coords('54515990'), cep_to_coords('54515250'), cep_to_coords('50980580'), cep_to_coords('51275590'), cep_to_coords('54160060'), cep_to_coords('54250440'), cep_to_coords('53405300'), cep_to_coords('54100112'), cep_to_coords('53260180'), cep_to_coords('55020800'), cep_to_coords('56903235'), cep_to_coords('56895000'), cep_to_coords('56912580'), cep_to_coords('53020360'), cep_to_coords('52165270'), cep_to_coords('53441601'), cep_to_coords('52030050'), cep_to_coords('53431070'), cep_to_coords('53150151'), cep_to_coords('55190100'), cep_to_coords('55195509'), cep_to_coords('52280190'), cep_to_coords('52071400'), cep_to_coords('54765300'), cep_to_coords('53439180'), cep_to_coords('52280650'), cep_to_coords('50741480'), cep_to_coords('52191250'), cep_to_coords('52080310'), cep_to_coords('54765138'), cep_to_coords('54759000'), cep_to_coords('53140000'), cep_to_coords('50711550'), cep_to_coords('53402008'), cep_to_coords('52071020'), cep_to_coords('50810080'), cep_to_coords('54460557'), cep_to_coords('53370460'), cep_to_coords('53330480'), cep_to_coords('52210010'), cep_to_coords('52081082'), cep_to_coords('53230010'), cep_to_coords('55192150'), cep_to_coords('55295475'), cep_to_coords('56920000'), cep_to_coords('53625735'), cep_to_coords('53610260'), cep_to_coords('55610460'), cep_to_coords('55602270'), cep_to_coords('55604271'), cep_to_coords('53010290'), cep_to_coords('53240180'), cep_to_coords('55608507'), cep_to_coords('56503550'), cep_to_coords('56502000'), cep_to_coords('50780270'), cep_to_coords('53290360'), cep_to_coords('56516160'), cep_to_coords('50730265'), cep_to_coords('55014325'), cep_to_coords('51345400'), cep_to_coords('53610050'), cep_to_coords('50680580'), cep_to_coords('53580020'), cep_to_coords('53540202'), cep_to_coords('52165053'), cep_to_coords('54345050'), cep_to_coords('52221200'), cep_to_coords('53417180'), cep_to_coords('51240550'), cep_to_coords('51280520'), cep_to_coords('50060040'), cep_to_coords('54759235'), cep_to_coords('54335000'), cep_to_coords('55644648'), cep_to_coords('53110340'), cep_to_coords('54480070'), cep_to_coords('54310160'), cep_to_coords('54727220'), cep_to_coords('50960140'), cep_to_coords('50980575'), cep_to_coords('53300110'), cep_to_coords('52040390'), cep_to_coords('53570110'), cep_to_coords('55024060'), cep_to_coords('53210090'), cep_to_coords('53370620'), cep_to_coords('55014310'), cep_to_coords('51350390'), cep_to_coords('50720650'), cep_to_coords('55042180'), cep_to_coords('52051390'), cep_to_coords('52390090'), cep_to_coords('55297812'), cep_to_coords('55028575'), cep_to_coords('51111050'), cep_to_coords('54310091'), cep_to_coords('53419180'), cep_to_coords('50711260'), cep_to_coords('55030300'), cep_to_coords('53110030'), cep_to_coords('53415330'), cep_to_coords('54160273'), cep_to_coords('56909135'), cep_to_coords('54320090'), cep_to_coords('55036000'), cep_to_coords('53370070'), cep_to_coords('55194318'), cep_to_coords('54140450'), cep_to_coords('54100460'), cep_to_coords('54368190'), cep_to_coords('54270455'), cep_to_coords('55375000'), cep_to_coords('54330565'), cep_to_coords('53423820'), cep_to_coords('53433740'), cep_to_coords('50980725'), cep_to_coords('56515480'), cep_to_coords('53270010'), cep_to_coords('55016365'), cep_to_coords('54320600'), cep_to_coords('53417020'), cep_to_coords('54580775'), cep_to_coords('54980600'), cep_to_coords('50720290'), cep_to_coords('52160445'), cep_to_coords('51011350'), cep_to_coords('52031201'), cep_to_coords('50670410'), cep_to_coords('54365410'), cep_to_coords('52051230'), cep_to_coords('56440000'), cep_to_coords('53429701'), cep_to_coords('53429790'), cep_to_coords('53435590'), cep_to_coords('56916000'), cep_to_coords('56925000'), cep_to_coords('56622510'), cep_to_coords('55298125'), cep_to_coords('54400082'), cep_to_coords('55299490'), cep_to_coords('52050280'), cep_to_coords('53421131'), cep_to_coords('50760130'), cep_to_coords('52041050'), cep_to_coords('52081410'), cep_to_coords('54753774'), cep_to_coords('53110300'), cep_to_coords('53409720'), cep_to_coords('50607400'), cep_to_coords('52091021'), cep_to_coords('53409630'), cep_to_coords('50780190'), cep_to_coords('54759051'), cep_to_coords('54735140'), cep_to_coords('54727320'), cep_to_coords('05549000'), cep_to_coords('55194106'), cep_to_coords('55008190'), cep_to_coords('55014652'), cep_to_coords('52110360'), cep_to_coords('50790110'), cep_to_coords('54762340'), cep_to_coords('54210361'), cep_to_coords('54517410'), cep_to_coords('54505175'), cep_to_coords('53180070'), cep_to_coords('53180130'), cep_to_coords('53625733'), cep_to_coords('56316220'), cep_to_coords('54210320'), cep_to_coords('50090320'), cep_to_coords('50670220'), cep_to_coords('52011150'), cep_to_coords('53630065'), cep_to_coords('53080660'), cep_to_coords('54340215'), cep_to_coords('55604110'), cep_to_coords('54730000'), cep_to_coords('50920170'), cep_to_coords('52130255'), cep_to_coords('50050190'), cep_to_coords('53520173'), cep_to_coords('55295620'), cep_to_coords('51190235'), cep_to_coords('51190255'), cep_to_coords('53540090'), cep_to_coords('54771071'), cep_to_coords('53510180'), cep_to_coords('53585000'), cep_to_coords('55250970'), cep_to_coords('24768796'), cep_to_coords('52031041'), cep_to_coords('53443130'), cep_to_coords('53530780'), cep_to_coords('50910450'), cep_to_coords('54140262'), cep_to_coords('50731410'), cep_to_coords('53630543'), cep_to_coords('53421680'), cep_to_coords('50771695'), cep_to_coords('50870360'), cep_to_coords('52068080'), cep_to_coords('53070010'), cep_to_coords('52011030'), cep_to_coords('52110260'), cep_to_coords('50860460'), cep_to_coords('50800305'), cep_to_coords('50940550'), cep_to_coords('51290530'), cep_to_coords('51290330'), cep_to_coords('51270150'), cep_to_coords('56740040'), cep_to_coords('50680090'), cep_to_coords('59250340'), cep_to_coords('51021320'), cep_to_coords('55815180'), cep_to_coords('50790420'), cep_to_coords('52131060'), cep_to_coords('55672970'), cep_to_coords('55495970'), cep_to_coords('50770720'), cep_to_coords('52050210'), cep_to_coords('55644176'), cep_to_coords('55644041'), cep_to_coords('55644380'), cep_to_coords('52030225'), cep_to_coords('54727350'), cep_to_coords('51250420'), cep_to_coords('50771500'), cep_to_coords('53437844'), cep_to_coords('54768305'), cep_to_coords('54380270'), cep_to_coords('55024670'), cep_to_coords('56912156'), cep_to_coords('56515710'), cep_to_coords('56760000'), cep_to_coords('56180000'), cep_to_coords('53080000'), cep_to_coords('52020190'), cep_to_coords('53320071'), cep_to_coords('52041690'), cep_to_coords('54250330'), cep_to_coords('56509310'), cep_to_coords('56512310'), cep_to_coords('56512410'), cep_to_coords('52050090'), cep_to_coords('55293200'), cep_to_coords('53401720'), cep_to_coords('54753250'), cep_to_coords('50960640'), cep_to_coords('54762350'), cep_to_coords('51290650'), cep_to_coords('54762748'), cep_to_coords('54753160'), cep_to_coords('55196157'), cep_to_coords('55022050'), cep_to_coords('55031140'), cep_to_coords('55014132'), cep_to_coords('50780310'), cep_to_coords('50780341'), cep_to_coords('50820310'), cep_to_coords('54210130'), cep_to_coords('54505310'), cep_to_coords('54520290'), cep_to_coords('54580650'), cep_to_coords('52131610'), cep_to_coords('54325050'), cep_to_coords('55042075'), cep_to_coords('55559000'), cep_to_coords('54505590'), cep_to_coords('55641290'), cep_to_coords('53370270'), cep_to_coords('54520675'), cep_to_coords('55024190'), cep_to_coords('50820490'), cep_to_coords('53220380'), cep_to_coords('52221085'), cep_to_coords('54753510'), cep_to_coords('55042270'), cep_to_coords('54800970'), cep_to_coords('55018470'), cep_to_coords('53530390'), cep_to_coords('53637195'), cep_to_coords('52280107'), cep_to_coords('56909100'), cep_to_coords('55030490'), cep_to_coords('55030010'), cep_to_coords('55012510'), cep_to_coords('50640160'), cep_to_coords('54580670'), cep_to_coords('53417280'), cep_to_coords('51260089'), cep_to_coords('52080220'), cep_to_coords('53320470'), cep_to_coords('53240515'), cep_to_coords('56230000'), cep_to_coords('52121155'), cep_to_coords('54517370'), cep_to_coords('51110200'), cep_to_coords('50810180'), cep_to_coords('55008090'), cep_to_coords('52061340'), cep_to_coords('53150335'), cep_to_coords('50020360'), cep_to_coords('54517490'), cep_to_coords('55028050'), cep_to_coords('52111190'), cep_to_coords('53210420'), cep_to_coords('52210050'), cep_to_coords('52021970'), cep_to_coords('52040090'), cep_to_coords('52280010'), cep_to_coords('52280080'), cep_to_coords('54100535'), cep_to_coords('52081140'), cep_to_coords('53670000'), cep_to_coords('53370525'), cep_to_coords('50865110'), cep_to_coords('50980695'), cep_to_coords('50050060'), cep_to_coords('62640000'), cep_to_coords('53470340'), cep_to_coords('52060410'), cep_to_coords('52884003'), cep_to_coords('50751620'), cep_to_coords('50751480'), cep_to_coords('55928000'), cep_to_coords('53413530'), cep_to_coords('54230530'), cep_to_coords('50080785'), cep_to_coords('50980715'), cep_to_coords('53441460'), cep_to_coords('51010720'), cep_to_coords('54792110'), cep_to_coords('62400000'), cep_to_coords('51290040'), cep_to_coords('54400160'), cep_to_coords('55016060'), cep_to_coords('52120000'), cep_to_coords('50720030'), cep_to_coords('56304320'), cep_to_coords('54753037'), cep_to_coords('50060280'), cep_to_coords('55608520'), cep_to_coords('54270010'), cep_to_coords('52081350'), cep_to_coords('53439705'), cep_to_coords('56302100'), cep_to_coords('54140610'), cep_to_coords('50740160'), cep_to_coords('55643678'), cep_to_coords('54070180'), cep_to_coords('53070080'), cep_to_coords('55018130'), cep_to_coords('59074390'), cep_to_coords('53620717'), cep_to_coords('53030090'), cep_to_coords('52120031'), cep_to_coords('52011270'), cep_to_coords('51310410'), cep_to_coords('52091130'), cep_to_coords('53545815'), cep_to_coords('53520700'), cep_to_coords('55038180'), cep_to_coords('51290510'), cep_to_coords('53260600'), cep_to_coords('54320003'), cep_to_coords('55002190'), cep_to_coords('50070200'), cep_to_coords('56504120'), cep_to_coords('51020200'), cep_to_coords('53330490'), cep_to_coords('56903340'), cep_to_coords('52070470'), cep_to_coords('50980250'), cep_to_coords('52130260'), cep_to_coords('53130150'), cep_to_coords('52060505'), cep_to_coords('55194280'), cep_to_coords('55191588'), cep_to_coords('52051250'), cep_to_coords('56313140'), cep_to_coords('56302110'), cep_to_coords('56332210'), cep_to_coords('56314465'), cep_to_coords('56320660'), cep_to_coords('52071030'), cep_to_coords('55291170'), cep_to_coords('54774450'), cep_to_coords('55195530'), cep_to_coords('54759030'), cep_to_coords('56980000'), cep_to_coords('53150450'), cep_to_coords('54715810'), cep_to_coords('50721200'), cep_to_coords('55024525'), cep_to_coords('54520100'), cep_to_coords('54580466'), cep_to_coords('52050245'), cep_to_coords('52091490'), cep_to_coords('52031330'), cep_to_coords('53510386'), cep_to_coords('53180012'), cep_to_coords('50980400'), cep_to_coords('53300100'), cep_to_coords('51240230'), cep_to_coords('52050230'), cep_to_coords('50751510'), cep_to_coords('54325061'), cep_to_coords('54756045'), cep_to_coords('53431005'), cep_to_coords('51260080'), cep_to_coords('54450180'), cep_to_coords('51250090'), cep_to_coords('51130115'), cep_to_coords('54460400'), cep_to_coords('54525610'), cep_to_coords('54160100'), cep_to_coords('59000000'), cep_to_coords('53429070'), cep_to_coords('54210440'), cep_to_coords('50070315'), cep_to_coords('55320000'), cep_to_coords('53429150'), cep_to_coords('56507220'), cep_to_coords('53320050'), cep_to_coords('50960320'), cep_to_coords('50160260'), cep_to_coords('50721160'), cep_to_coords('53230030'), cep_to_coords('52090390'), cep_to_coords('56507970'), cep_to_coords('50640650'), cep_to_coords('52081370'), cep_to_coords('52041590'), cep_to_coords('50910110'), cep_to_coords('51011270'), cep_to_coords('54774060'), cep_to_coords('52061082'), cep_to_coords('52061095'), cep_to_coords('53360730'), cep_to_coords('55617970'), cep_to_coords('54600000'), cep_to_coords('42700000'), cep_to_coords('53230370'), cep_to_coords('54400150'), cep_to_coords('54759280'), cep_to_coords('53625665'), cep_to_coords('53635785'), cep_to_coords('53530320'), cep_to_coords('53413140'), cep_to_coords('54762664'), cep_to_coords('53585060'), cep_to_coords('53530725'), cep_to_coords('53520015'), cep_to_coords('53540370'), cep_to_coords('53560070'), cep_to_coords('53431660'), cep_to_coords('53270262'), cep_to_coords('52091139'), cep_to_coords('52081060'), cep_to_coords('52081061'), cep_to_coords('59270685'), cep_to_coords('53620555'), cep_to_coords('54530022'), cep_to_coords('54350836'), cep_to_coords('52060090'), cep_to_coords('54515130'), cep_to_coords('54505195'), cep_to_coords('50450590'), cep_to_coords('54360010'), cep_to_coords('53080430'), cep_to_coords('51350270'), cep_to_coords('54515270'), cep_to_coords('54325290'), cep_to_coords('50090360'), cep_to_coords('55395000'), cep_to_coords('55195006'), cep_to_coords('51240755'), cep_to_coords('53260590'), cep_to_coords('52051410'), cep_to_coords('64748000'), cep_to_coords('53090390'), cep_to_coords('56314420'), cep_to_coords('55190335'), cep_to_coords('55191991'), cep_to_coords('55355000'), cep_to_coords('54530370'), cep_to_coords('44003000'), cep_to_coords('52060380'), cep_to_coords('52291151'), cep_to_coords('54720073'), cep_to_coords('50020170'), cep_to_coords('51345070'), cep_to_coords('50050135'), cep_to_coords('55014320'), cep_to_coords('52280540'), cep_to_coords('51330240'), cep_to_coords('53430250'), cep_to_coords('55016000'), cep_to_coords('58415068'), cep_to_coords('52070632'), cep_to_coords('51150000'), cep_to_coords('53580050'), cep_to_coords('52280240'), cep_to_coords('54150030'), cep_to_coords('54440298'), cep_to_coords('53160200'), cep_to_coords('54300022'), cep_to_coords('50680040'), cep_to_coords('53429620'), cep_to_coords('50720150'), cep_to_coords('54720150'), cep_to_coords('53300140'), cep_to_coords('50771000'), cep_to_coords('50771155'), cep_to_coords('50640120'), cep_to_coords('53407630'), cep_to_coords('55028070'), cep_to_coords('54783620'), cep_to_coords('55039020'), cep_to_coords('50980110'), cep_to_coords('55018450'), cep_to_coords('52191165'), cep_to_coords('56503650'), cep_to_coords('56511340'), cep_to_coords('55014350'), cep_to_coords('54420620'), cep_to_coords('54120181'), cep_to_coords('54756047'), cep_to_coords('56512261'), cep_to_coords('50050150'), cep_to_coords('56511040'), cep_to_coords('13346050'), cep_to_coords('53421021'), cep_to_coords('52121290'), cep_to_coords('55004480'), cep_to_coords('54325435'), cep_to_coords('53050160'), cep_to_coords('54160282'), cep_to_coords('54360007'), cep_to_coords('51010215'), cep_to_coords('51010045'), cep_to_coords('55036525'), cep_to_coords('54210464'), cep_to_coords('52010300'), cep_to_coords('55610105'), cep_to_coords('56503000'), cep_to_coords('55018260'), cep_to_coords('55610014'), cep_to_coords('55608090'), cep_to_coords('53220051'), cep_to_coords('54495170'), cep_to_coords('55612188'), cep_to_coords('54705280'), cep_to_coords('55610351'), cep_to_coords('50910060'), cep_to_coords('53250070'), cep_to_coords('52110031'), cep_to_coords('55038420'), cep_to_coords('53437520'), cep_to_coords('55614620'), cep_to_coords('55606590'), cep_to_coords('51350240'), cep_to_coords('52110530'), cep_to_coords('55032390'), cep_to_coords('52054260'), cep_to_coords('51260210'), cep_to_coords('50730380'), cep_to_coords('53220590'), cep_to_coords('54300264'), cep_to_coords('52140005'), cep_to_coords('53405190'), cep_to_coords('55614015'), cep_to_coords('55612270'), cep_to_coords('53413134'), cep_to_coords('54767120'), cep_to_coords('54505005'), cep_to_coords('50810490'), cep_to_coords('50740330'), cep_to_coords('53530492'), cep_to_coords('50720370'), cep_to_coords('54150353'), cep_to_coords('56316784'), cep_to_coords('52140670'), cep_to_coords('53360420'), cep_to_coords('52110205'), cep_to_coords('53423510'), cep_to_coords('55024155'), cep_to_coords('55006340'), cep_to_coords('53635158'), cep_to_coords('53419903'), cep_to_coords('54505010'), cep_to_coords('53416780'), cep_to_coords('53407270'), cep_to_coords('75830000'), cep_to_coords('52071188'), cep_to_coords('52291240'), cep_to_coords('52090200'), cep_to_coords('51260550'), cep_to_coords('50830460'), cep_to_coords('51260280'), cep_to_coords('53090050'), cep_to_coords('53240710'), cep_to_coords('53407050'), cep_to_coords('56310720'), cep_to_coords('56303990'), cep_to_coords('44590000'), cep_to_coords('56328280'), cep_to_coords('54495233'), cep_to_coords('54260110'), cep_to_coords('55018240'), cep_to_coords('55038155'), cep_to_coords('55190770'), cep_to_coords('54580340'), cep_to_coords('51280010'), cep_to_coords('55877000'), cep_to_coords('56912280'), cep_to_coords('56903380'), cep_to_coords('56906410'), cep_to_coords('55606820'), cep_to_coords('55604275'), cep_to_coords('55608111'), cep_to_coords('52291260'), cep_to_coords('55604350'), cep_to_coords('54580285'), cep_to_coords('50741520'), cep_to_coords('55896000'), cep_to_coords('53625837'), cep_to_coords('50751280'), cep_to_coords('53180122'), cep_to_coords('53180120'), cep_to_coords('52050270'), cep_to_coords('54735285'), cep_to_coords('55018585'), cep_to_coords('51280110'), cep_to_coords('54420050'), cep_to_coords('53441216'), cep_to_coords('54070210'), cep_to_coords('55030620'), cep_to_coords('55026290'), cep_to_coords('55028210'), cep_to_coords('55028120'), cep_to_coords('44315000'), cep_to_coords('52070008'), cep_to_coords('54230482'), cep_to_coords('05514000'), cep_to_coords('26200353'), cep_to_coords('53000060'), cep_to_coords('56503320'), cep_to_coords('51160280'), cep_to_coords('55460970'), cep_to_coords('55819200'), cep_to_coords('55032595'), cep_to_coords('53550580'), cep_to_coords('50720755'), cep_to_coords('53110741'), cep_to_coords('50730665'), cep_to_coords('52061047'), cep_to_coords('54230020'), cep_to_coords('55643021'), cep_to_coords('54520560'), cep_to_coords('54580090'), cep_to_coords('56560000'), cep_to_coords('54410000'), cep_to_coords('54345170'), cep_to_coords('53441130'), cep_to_coords('54520230'), cep_to_coords('54520190'), cep_to_coords('54580395'), cep_to_coords('54525241'), cep_to_coords('54510250'), cep_to_coords('54280670'), cep_to_coords('54580215'), cep_to_coords('54520015'), cep_to_coords('54515499'), cep_to_coords('54510150'), cep_to_coords('54535170'), cep_to_coords('54520110'), cep_to_coords('54535140'), cep_to_coords('54525025'), cep_to_coords('54140240'), cep_to_coords('51270600'), cep_to_coords('54762000'), cep_to_coords('56312675'), cep_to_coords('53401440'), cep_to_coords('54510990'), cep_to_coords('54580375'), cep_to_coords('56903415'), cep_to_coords('54110680'), cep_to_coords('50750040'), cep_to_coords('55014185'), cep_to_coords('55103000'), cep_to_coords('55292220'), cep_to_coords('51021420'), cep_to_coords('50711400'), cep_to_coords('54756475'), cep_to_coords('53240190'), cep_to_coords('55004390'), cep_to_coords('51150410'), cep_to_coords('55030171'), cep_to_coords('54090180'), cep_to_coords('51111150'), cep_to_coords('55018400'), cep_to_coords('52071290'), cep_to_coords('56906371'), cep_to_coords('55610230'), cep_to_coords('55602420'), cep_to_coords('52071380'), cep_to_coords('50110180'), cep_to_coords('54315645'), cep_to_coords('53545700'), cep_to_coords('50761131'), cep_to_coords('55606815'), cep_to_coords('51010190'), cep_to_coords('50761400'), cep_to_coords('53545710'), cep_to_coords('55294310'), cep_to_coords('53260190'), cep_to_coords('54730320'), cep_to_coords('51275010'), cep_to_coords('50790001'), cep_to_coords('50820430'), cep_to_coords('67130670'), cep_to_coords('53439160'), cep_to_coords('55040005'), cep_to_coords('55614110'), cep_to_coords('53421050'), cep_to_coords('52456850'), cep_to_coords('51030480'), cep_to_coords('55014470'), cep_to_coords('55190579'), cep_to_coords('56909130'), cep_to_coords('55614733'), cep_to_coords('53415460'), cep_to_coords('54759150'), cep_to_coords('55610050'), cep_to_coords('51270610'), cep_to_coords('54340320'), cep_to_coords('50761030'), cep_to_coords('50810030'), cep_to_coords('50780500'), cep_to_coords('55608140'), cep_to_coords('51345630'), cep_to_coords('54495615'), cep_to_coords('50040130'), cep_to_coords('55612560'), cep_to_coords('50780655'), cep_to_coords('50060620'), cep_to_coords('55811030'), cep_to_coords('55819317'), cep_to_coords('55816000'), cep_to_coords('53350060'), cep_to_coords('50781440'), cep_to_coords('50750060'), cep_to_coords('54765280'), cep_to_coords('53170200'), cep_to_coords('55018620'), cep_to_coords('53530402'), cep_to_coords('53150140'), cep_to_coords('52190250'), cep_to_coords('51340030'), cep_to_coords('52291120'), cep_to_coords('52080305'), cep_to_coords('52081374'), cep_to_coords('50980635'), cep_to_coords('52090121'), cep_to_coords('52110147'), cep_to_coords('52160230'), cep_to_coords('54510230'), cep_to_coords('53435300'), cep_to_coords('51250130'), cep_to_coords('51320540'), cep_to_coords('54440113'), cep_to_coords('54230030'), cep_to_coords('50100090'), cep_to_coords('50875040'), cep_to_coords('50711440'), cep_to_coords('53540055'), cep_to_coords('53230210'), cep_to_coords('52060160'), cep_to_coords('37410000'), cep_to_coords('54410430'), cep_to_coords('50930230'), cep_to_coords('54505535'), cep_to_coords('53407720'), cep_to_coords('51011650'), cep_to_coords('52070350'), cep_to_coords('52070390'), cep_to_coords('55612050'), cep_to_coords('55608025'), cep_to_coords('50660460'), cep_to_coords('50900375'), cep_to_coords('52190120'), cep_to_coords('50100060'), cep_to_coords('52280223'), cep_to_coords('55004080'), cep_to_coords('55034310'), cep_to_coords('55028250'), cep_to_coords('55012100'), cep_to_coords('55012740'), cep_to_coords('55192642'), cep_to_coords('55192663'), cep_to_coords('54210310'), cep_to_coords('55192185'), cep_to_coords('53030160'), cep_to_coords('51270440'), cep_to_coords('53413154'), cep_to_coords('55190362'), cep_to_coords('55625000'), cep_to_coords('56328180'), cep_to_coords('56330000'), cep_to_coords('56304510'), cep_to_coords('56316640'), cep_to_coords('53433600'), cep_to_coords('54530010'), cep_to_coords('53330520'), cep_to_coords('51260120'), cep_to_coords('50731360'), cep_to_coords('50030130'), cep_to_coords('53226371'), cep_to_coords('54753390'), cep_to_coords('50020060'), cep_to_coords('53270370'), cep_to_coords('52280520'), cep_to_coords('55643010'), cep_to_coords('50610310'), cep_to_coords('55028350'), cep_to_coords('56795000'), cep_to_coords('55028160'), cep_to_coords('51310300'), cep_to_coords('55765000'), cep_to_coords('54777205'), cep_to_coords('53435280'), cep_to_coords('53409135'), cep_to_coords('54460230'), cep_to_coords('53407030'), cep_to_coords('52071705'), cep_to_coords('50730050'), cep_to_coords('51030090'), cep_to_coords('50690675'), cep_to_coords('51011031'), cep_to_coords('50680630'), cep_to_coords('54360180'), cep_to_coords('55760000'), cep_to_coords('55190542'), cep_to_coords('50830370'), cep_to_coords('50900120'), cep_to_coords('50980080'), cep_to_coords('54470590'), cep_to_coords('50790160'), cep_to_coords('56014111'), cep_to_coords('52061142'), cep_to_coords('51345160'), cep_to_coords('52191480'), cep_to_coords('54280634'), cep_to_coords('53510470'), cep_to_coords('50870400'), cep_to_coords('52140550'), cep_to_coords('54705065'), cep_to_coords('50760030'), cep_to_coords('54070000'), cep_to_coords('52041580'), cep_to_coords('55006210'), cep_to_coords('52110510'), cep_to_coords('52080280'), cep_to_coords('54762791'), cep_to_coords('51021228'), cep_to_coords('55008201'), cep_to_coords('54420410'), cep_to_coords('54325360'), cep_to_coords('52090690'), cep_to_coords('53140220'), cep_to_coords('55006360'), cep_to_coords('50980330'), cep_to_coords('55014040'), cep_to_coords('55012480'), cep_to_coords('52032250'), cep_to_coords('55614445'), cep_to_coords('50690580'), cep_to_coords('55030520'), cep_to_coords('54420520'), cep_to_coords('55610470'), cep_to_coords('55612160'), cep_to_coords('55819650'), cep_to_coords('55602010'), cep_to_coords('55608375'), cep_to_coords('55892999'), cep_to_coords('54730190'), cep_to_coords('51320500'), cep_to_coords('51275140'), cep_to_coords('51230475'), cep_to_coords('52081067'), cep_to_coords('55610290'), cep_to_coords('50980050'), cep_to_coords('55014460'), cep_to_coords('54765340'), cep_to_coords('56318260'), cep_to_coords('55608525'), cep_to_coords('55602160'), cep_to_coords('54727030'), cep_to_coords('56565000'), cep_to_coords('54275990'), cep_to_coords('55602410'), cep_to_coords('55604010'), cep_to_coords('55614060'), cep_to_coords('55608790'), cep_to_coords('55602068'), cep_to_coords('55293000'), cep_to_coords('52070300'), cep_to_coords('55612510'), cep_to_coords('55608080'), cep_to_coords('53441390'), cep_to_coords('51240440'), cep_to_coords('52721160'), cep_to_coords('54410025'), cep_to_coords('55604270'), cep_to_coords('55031315'), cep_to_coords('56503162'), cep_to_coords('56503400'), cep_to_coords('23290150'), cep_to_coords('50720710'), cep_to_coords('55038350'), cep_to_coords('56912230'), cep_to_coords('54365220'), cep_to_coords('55643700'), cep_to_coords('53416030'), cep_to_coords('50630740'), cep_to_coords('52070213'), cep_to_coords('52210200'), cep_to_coords('55610150'), cep_to_coords('52160070'), cep_to_coords('50731090'), cep_to_coords('52210110'), cep_to_coords('55037242'), cep_to_coords('54220250'), cep_to_coords('53110471'), cep_to_coords('51030171'), cep_to_coords('54230262'), cep_to_coords('51340650'), cep_to_coords('54720121'), cep_to_coords('54120390'), cep_to_coords('54280260'), cep_to_coords('53570255'), cep_to_coords('51270702'), cep_to_coords('54080300'), cep_to_coords('53570129'), cep_to_coords('53413000'), cep_to_coords('53409520'), cep_to_coords('53180220'), cep_to_coords('52291220'), cep_to_coords('52220110'), cep_to_coords('52071470'), cep_to_coords('52071220'), cep_to_coords('54732826'), cep_to_coords('52091407'), cep_to_coords('52090506'), cep_to_coords('52190150'), cep_to_coords('54260050'), cep_to_coords('55644290'), cep_to_coords('55641110'), cep_to_coords('54515503'), cep_to_coords('55026530'), cep_to_coords('54330665'), cep_to_coords('55000001'), cep_to_coords('54510210'), cep_to_coords('54520000'), cep_to_coords('53150270'), cep_to_coords('50670450'), cep_to_coords('54325622'), cep_to_coords('52111420'), cep_to_coords('52211301'), cep_to_coords('53409090'), cep_to_coords('55020060'), cep_to_coords('55020608'), cep_to_coords('54120054'), cep_to_coords('55198000'), cep_to_coords('55190062'), cep_to_coords('54400333'), cep_to_coords('55192110'), cep_to_coords('50721210'), cep_to_coords('50870440'), cep_to_coords('55195704'), cep_to_coords('55195021'), cep_to_coords('51250250'), cep_to_coords('54525135'), cep_to_coords('53405140'), cep_to_coords('56912060'), cep_to_coords('56912285'), cep_to_coords('56912235'), cep_to_coords('56903655'), cep_to_coords('54160271'), cep_to_coords('55608430'), cep_to_coords('54768030'), cep_to_coords('54330220'), cep_to_coords('55194324'), cep_to_coords('50080270'), cep_to_coords('50710250'), cep_to_coords('55295340'), cep_to_coords('54280732'), cep_to_coords('53180150'), cep_to_coords('50731490'), cep_to_coords('51150660'), cep_to_coords('54330573'), cep_to_coords('53435840'), cep_to_coords('50750510'), cep_to_coords('51170600'), cep_to_coords('54505300'), cep_to_coords('52070190'), cep_to_coords('50890270'), cep_to_coords('53300180'), cep_to_coords('55270250'), cep_to_coords('53330470'), cep_to_coords('54753316'), cep_to_coords('53150250'), cep_to_coords('51010750'), cep_to_coords('53625032'), cep_to_coords('55614295'), cep_to_coords('54230485'), cep_to_coords('51345720'), cep_to_coords('52640070'), cep_to_coords('54100300'), cep_to_coords('55020385'), cep_to_coords('56316540'), cep_to_coords('54140230'), cep_to_coords('51290230'), cep_to_coords('55297290'), cep_to_coords('55295050'), cep_to_coords('56321130'), cep_to_coords('56512090'), cep_to_coords('55506640'), cep_to_coords('54330820'), cep_to_coords('55610070'), cep_to_coords('50070020'), cep_to_coords('51270310'), cep_to_coords('53635085'), cep_to_coords('54325012'), cep_to_coords('54170190'), cep_to_coords('55159899'), cep_to_coords('54430300'), cep_to_coords('55292655'), cep_to_coords('51170580'), cep_to_coords('56509300'), cep_to_coords('56509320'), cep_to_coords('53530285'), cep_to_coords('53240461'), cep_to_coords('52291500'), cep_to_coords('52160385'), cep_to_coords('54355350'), cep_to_coords('56320771'), cep_to_coords('50110115'), cep_to_coords('54762512'), cep_to_coords('55644170'), cep_to_coords('55612095'), cep_to_coords('54735793'), cep_to_coords('53437330'), cep_to_coords('56308210'), cep_to_coords('52070360'), cep_to_coords('50650000'), cep_to_coords('54460375'), cep_to_coords('54100440'), cep_to_coords('54410355'), cep_to_coords('52091410'), cep_to_coords('51010820'), cep_to_coords('50760145'), cep_to_coords('55602040'), cep_to_coords('50070335'), cep_to_coords('50070400'), cep_to_coords('50940240'), cep_to_coords('56907070'), cep_to_coords('53425430'), cep_to_coords('50850110'), cep_to_coords('54140030'), cep_to_coords('54315110'), cep_to_coords('55608810'), cep_to_coords('55608055'), cep_to_coords('53320510'), cep_to_coords('55604490'), cep_to_coords('55296360'), cep_to_coords('55027010'), cep_to_coords('55027350'), cep_to_coords('53433290'), cep_to_coords('53422350'), cep_to_coords('53300000'), cep_to_coords('56309010'), cep_to_coords('55192660'), cep_to_coords('55020390'), cep_to_coords('55018360'), cep_to_coords('55018270'), cep_to_coords('54705650'), cep_to_coords('55014660'), cep_to_coords('52091220'), cep_to_coords('53070191'), cep_to_coords('52291060'), cep_to_coords('53220730'), cep_to_coords('53439090'), cep_to_coords('52041652'), cep_to_coords('54120520'), cep_to_coords('52051005'), cep_to_coords('53220191'), cep_to_coords('53370257'), cep_to_coords('53370830'), cep_to_coords('52221020'), cep_to_coords('55608710'), cep_to_coords('55612360'), cep_to_coords('55642025'), cep_to_coords('55643098'), cep_to_coords('53080838'), cep_to_coords('51260281'), cep_to_coords('50800130'), cep_to_coords('55022280'), cep_to_coords('54737180'), cep_to_coords('50120050'), cep_to_coords('53335431'), cep_to_coords('50670180'), cep_to_coords('53520725'), cep_to_coords('54510001'), cep_to_coords('54720012'), cep_to_coords('51190280'), cep_to_coords('55038828'), cep_to_coords('53407250'), cep_to_coords('53230443'), cep_to_coords('53236440'), cep_to_coords('55038540'), cep_to_coords('54140612'), cep_to_coords('53416080'), cep_to_coords('54340070'), cep_to_coords('53210730'), cep_to_coords('53370194'), cep_to_coords('55004083'), cep_to_coords('53437900'), cep_to_coords('53220780'), cep_to_coords('53300030'), cep_to_coords('50741050'), cep_to_coords('51170040'), cep_to_coords('53210000'), cep_to_coords('53439530'), cep_to_coords('50810400'), cep_to_coords('52050260'), cep_to_coords('50875060'), cep_to_coords('50960270'), cep_to_coords('50780550'), cep_to_coords('54440281'), cep_to_coords('54280704'), cep_to_coords('54230535'), cep_to_coords('52130173'), cep_to_coords('55610090'), cep_to_coords('55608435'), cep_to_coords('53422020'), cep_to_coords('56518899'), cep_to_coords('53407070'), cep_to_coords('50800190'), cep_to_coords('50790230'), cep_to_coords('50910080'), cep_to_coords('54365200'), cep_to_coords('53370840'), cep_to_coords('27235375'), cep_to_coords('54230101'), cep_to_coords('56903600'), cep_to_coords('52060164'), cep_to_coords('55604430'), cep_to_coords('52280041'), cep_to_coords('55030205'), cep_to_coords('54730440'), cep_to_coords('56309460'), cep_to_coords('50080690'), cep_to_coords('52111432'), cep_to_coords('52114432'), cep_to_coords('51160400'), cep_to_coords('54160030'), cep_to_coords('56310746'), cep_to_coords('51030590'), cep_to_coords('55026330'), cep_to_coords('53370080'), cep_to_coords('53442100'), cep_to_coords('52061015'), cep_to_coords('54420020'), cep_to_coords('51350030'), cep_to_coords('53350030'), cep_to_coords('54768390'), cep_to_coords('54580450'), cep_to_coords('50761330'), cep_to_coords('53402020'), cep_to_coords('53370263'), cep_to_coords('55294470'), cep_to_coords('50100150'), cep_to_coords('51190730'), cep_to_coords('54420380'), cep_to_coords('50140160'), cep_to_coords('56320150'), cep_to_coords('50070110'), cep_to_coords('53140140'), cep_to_coords('55030030'), cep_to_coords('53407600'), cep_to_coords('53437750'), cep_to_coords('53441165'), cep_to_coords('50020090'), cep_to_coords('54280633'), cep_to_coords('54771020'), cep_to_coords('56906530'), cep_to_coords('56900100'), cep_to_coords('56912198'), cep_to_coords('77060116'), cep_to_coords('50980685'), cep_to_coords('56903400'), cep_to_coords('5690653'), cep_to_coords('56903475'), cep_to_coords('51250150'), cep_to_coords('50720355'), cep_to_coords('54756590'), cep_to_coords('54705394'), cep_to_coords('51280346'), cep_to_coords('52040491'), cep_to_coords('50731000'), cep_to_coords('54759602'), cep_to_coords('54762290'), cep_to_coords('54777190'), cep_to_coords('50040100'), cep_to_coords('55014646'), cep_to_coords('55192370'), cep_to_coords('55125970'), cep_to_coords('50740250'), cep_to_coords('56320000'), cep_to_coords('15900000'), cep_to_coords('56328010'), cep_to_coords('52070660'), cep_to_coords('54793230'), cep_to_coords('55014750'), cep_to_coords('52041680'), cep_to_coords('50710064'), cep_to_coords('50980450'), cep_to_coords('50970230'), cep_to_coords('50110091'), cep_to_coords('52221140'), cep_to_coords('51335165'), cep_to_coords('54792000'), cep_to_coords('52121390'), cep_to_coords('52041760'), cep_to_coords('53290110'), cep_to_coords('50810100'), cep_to_coords('54762360'), cep_to_coords('55643327'), cep_to_coords('55643040'), cep_to_coords('55643030'), cep_to_coords('53625222'), cep_to_coords('53625030'), cep_to_coords('53645070'), cep_to_coords('52110390'), cep_to_coords('50680560'), cep_to_coords('55300000'), cep_to_coords('50081000'), cep_to_coords('24220215'), cep_to_coords('55250420'), cep_to_coords('54400500'), cep_to_coords('53230115'), cep_to_coords('53030270'), cep_to_coords('53190260'), cep_to_coords('52130011'), cep_to_coords('41830000'), cep_to_coords('53421061'), cep_to_coords('53110490'), cep_to_coords('50640345'), cep_to_coords('53310020'), cep_to_coords('52160190'), cep_to_coords('51260000'), cep_to_coords('52160171'), cep_to_coords('52160170'), cep_to_coords('54720122'), cep_to_coords('51330130'), cep_to_coords('53110430'), cep_to_coords('54771655'), cep_to_coords('53210270'), cep_to_coords('51350130'), cep_to_coords('55296680'), cep_to_coords('55006240'), cep_to_coords('52280033'), cep_to_coords('52090371'), cep_to_coords('51220020'), cep_to_coords('53700990'), cep_to_coords('56912260'), cep_to_coords('54404800'), cep_to_coords('54140480'), cep_to_coords('55014740'), cep_to_coords('56610360'), cep_to_coords('52130060'), cep_to_coords('51067060'), cep_to_coords('54727180'), cep_to_coords('50751080'), cep_to_coords('56318380'), cep_to_coords('53421141'), cep_to_coords('53439290'), cep_to_coords('55816295'), cep_to_coords('53401110'), cep_to_coords('54150180'), cep_to_coords('55614260'), cep_to_coords('52061430'), cep_to_coords('56909070'), cep_to_coords('55608210'), cep_to_coords('55613900'), cep_to_coords('55813280'), cep_to_coords('50870800'), cep_to_coords('50731010'), cep_to_coords('52010070'), cep_to_coords('53441630'), cep_to_coords('55817140'), cep_to_coords('55641350'), cep_to_coords('54762270'), cep_to_coords('55018190'), cep_to_coords('55030580'), cep_to_coords('51430315'), cep_to_coords('55026220'), cep_to_coords('55026100'), cep_to_coords('50050270'), cep_to_coords('55016385'), cep_to_coords('54315090'), cep_to_coords('55016320'), cep_to_coords('55012310'), cep_to_coords('55100027'), cep_to_coords('55012290'), cep_to_coords('55026901'), cep_to_coords('55038310'), cep_to_coords('55490970'), cep_to_coords('54230177'), cep_to_coords('52081191'), cep_to_coords('52081190'), cep_to_coords('52070441'), cep_to_coords('54720814'), cep_to_coords('51250160'), cep_to_coords('52110210'), cep_to_coords('55614580'), cep_to_coords('55608665'), cep_to_coords('51011560'), cep_to_coords('55610260'), cep_to_coords('55602430'), cep_to_coords('55608645'), cep_to_coords('52490170'), cep_to_coords('54020030'), cep_to_coords('55305000'), cep_to_coords('55298135'), cep_to_coords('52121020'), cep_to_coords('83328260'), cep_to_coords('52131660'), cep_to_coords('55027470'), cep_to_coords('54470200'), cep_to_coords('55027990'), cep_to_coords('53433540'), cep_to_coords('50875020'), cep_to_coords('50640740'), cep_to_coords('51345350'), cep_to_coords('56328000'), cep_to_coords('52131580'), cep_to_coords('54330060'), cep_to_coords('53540730'), cep_to_coords('53530495'), cep_to_coords('53140010'), cep_to_coords('53090300'), cep_to_coords('53090140'), cep_to_coords('51280460'), cep_to_coords('50630680'), cep_to_coords('50770480'), cep_to_coords('50100420'), cep_to_coords('53190560'), cep_to_coords('52130250'), cep_to_coords('51190630'), cep_to_coords('53180212'), cep_to_coords('52171160'), cep_to_coords('50200065'), cep_to_coords('50670600'), cep_to_coords('50070620'), cep_to_coords('54230221'), cep_to_coords('50208001'), cep_to_coords('54420120'), cep_to_coords('51310260'), cep_to_coords('50750257'), cep_to_coords('52070032'), cep_to_coords('54440131'), cep_to_coords('54020310'), cep_to_coords('51020310'), cep_to_coords('52019091'), cep_to_coords('58900000'), cep_to_coords('58650000'), cep_to_coords('53401710'), cep_to_coords('52031090'), cep_to_coords('52210380'), cep_to_coords('54520500'), cep_to_coords('54589085'), cep_to_coords('54515100'), cep_to_coords('50771670'), cep_to_coords('52050355'), cep_to_coords('52211310'), cep_to_coords('56912275'), cep_to_coords('55642530'), cep_to_coords('50680610'), cep_to_coords('50080350'), cep_to_coords('55607030'), cep_to_coords('53407240'), cep_to_coords('54070010'), cep_to_coords('52060050'), cep_to_coords('50720752'), cep_to_coords('55604155'), cep_to_coords('54120670'), cep_to_coords('52221240'), cep_to_coords('52470220'), cep_to_coords('53160350'), cep_to_coords('50750090'), cep_to_coords('52020100'), cep_to_coords('52171100'), cep_to_coords('56506100'), cep_to_coords('52040400'), cep_to_coords('54715535'), cep_to_coords('51200030'), cep_to_coords('53240560'), cep_to_coords('56504525'), cep_to_coords('56503450'), cep_to_coords('56503451'), cep_to_coords('50660400'), cep_to_coords('55293440'), cep_to_coords('51275635'), cep_to_coords('55040010'), cep_to_coords('54440100'), cep_to_coords('55008160'), cep_to_coords('56309450'), cep_to_coords('54340565'), cep_to_coords('56909512'), cep_to_coords('55031050'), cep_to_coords('55020440'), cep_to_coords('54756043'), cep_to_coords('50810360'), cep_to_coords('53160160'), cep_to_coords('64695000'), cep_to_coords('53210085'), cep_to_coords('53401970'), cep_to_coords('54250031'), cep_to_coords('51200250'), cep_to_coords('53320121'), cep_to_coords('53429340'), cep_to_coords('52110010'), cep_to_coords('52071200'), cep_to_coords('50050130'), cep_to_coords('53444000'), cep_to_coords('55473000'), cep_to_coords('53407080'), cep_to_coords('53070000'), cep_to_coords('52091180'), cep_to_coords('56700970'), cep_to_coords('50100000'), cep_to_coords('55010200'), cep_to_coords('55026270'), cep_to_coords('50750350'), cep_to_coords('56512000'), cep_to_coords('56906470'), cep_to_coords('53550300'), cep_to_coords('55292323'), cep_to_coords('51010410'), cep_to_coords('52125320'), cep_to_coords('55020000'), cep_to_coords('54330325'), cep_to_coords('53441260'), cep_to_coords('56909125'), cep_to_coords('51350020'), cep_to_coords('54789840'), cep_to_coords('55816410'), cep_to_coords('51160111'), cep_to_coords('54400260'), cep_to_coords('54400360'), cep_to_coords('51160260'), cep_to_coords('55002130'), cep_to_coords('51130370'), cep_to_coords('51340240'), cep_to_coords('55024250'), cep_to_coords('54400180'), cep_to_coords('54580540'), cep_to_coords('54515025'), cep_to_coords('50750020'), cep_to_coords('54100060'), cep_to_coords('50771260'), cep_to_coords('52071540'), cep_to_coords('52190040'), cep_to_coords('53170140'), cep_to_coords('53630255'), cep_to_coords('53610160'), cep_to_coords('53645077'), cep_to_coords('53650060'), cep_to_coords('53630450'), cep_to_coords('53640618'), cep_to_coords('53610280'), cep_to_coords('53020617'), cep_to_coords('53280150'), cep_to_coords('56505210'), cep_to_coords('56504140'), cep_to_coords('56912178'), cep_to_coords('50670170'), cep_to_coords('56503260'), cep_to_coords('50770600'), cep_to_coords('56505250'), cep_to_coords('53421330'), cep_to_coords('52081180'), cep_to_coords('51300052'), cep_to_coords('53630631'), cep_to_coords('53630115'), cep_to_coords('55020591'), cep_to_coords('56328260'), cep_to_coords('87670000'), cep_to_coords('55038070'), cep_to_coords('58500000'), cep_to_coords('53120200'), cep_to_coords('54753500'), cep_to_coords('50780627'), cep_to_coords('56304070'), cep_to_coords('54762797'), cep_to_coords('54150060'), cep_to_coords('55642650'), cep_to_coords('51240540'), cep_to_coords('52060210'), cep_to_coords('55030500'), cep_to_coords('55036650'), cep_to_coords('55021265'), cep_to_coords('50860200'), cep_to_coords('51860200'), cep_to_coords('51150390'), cep_to_coords('53210210'), cep_to_coords('55819030'), cep_to_coords('50970110'), cep_to_coords('54270390'), cep_to_coords('53170580'), cep_to_coords('50970240'), cep_to_coords('51160240'), cep_to_coords('51030800'), cep_to_coords('52051305'), cep_to_coords('53530432'), cep_to_coords('50781130'), cep_to_coords('52070400'), cep_to_coords('55100000'), cep_to_coords('52120304'), cep_to_coords('52051105'), cep_to_coords('55291320'), cep_to_coords('55297640'), cep_to_coords('53210670'), cep_to_coords('56308060'), cep_to_coords('53419610'), cep_to_coords('50720535'), cep_to_coords('53020120'), cep_to_coords('55155970'), cep_to_coords('55310000'), cep_to_coords('55019270'), cep_to_coords('56505090'), cep_to_coords('55298290'), cep_to_coords('55296300'), cep_to_coords('54762650'), cep_to_coords('54774070'), cep_to_coords('50690400'), cep_to_coords('55296010'), cep_to_coords('54450141'), cep_to_coords('51275090'), cep_to_coords('54120370'), cep_to_coords('55030510'), cep_to_coords('50680010'), cep_to_coords('50880010'), cep_to_coords('53403050'), cep_to_coords('51350350'), cep_to_coords('53210590'), cep_to_coords('53425000'), cep_to_coords('55008470'), cep_to_coords('55643588'), cep_to_coords('55030080'), cep_to_coords('71917360'), cep_to_coords('55819110'), cep_to_coords('55815040'), cep_to_coords('51021160'), cep_to_coords('52050225'), cep_to_coords('55034560'), cep_to_coords('52041260'), cep_to_coords('50690610'), cep_to_coords('50751535'), cep_to_coords('52061280'), cep_to_coords('51190070'), cep_to_coords('55031330'), cep_to_coords('54330421'), cep_to_coords('54213692'), cep_to_coords('54300268'), cep_to_coords('52130070'), cep_to_coords('51160110'), cep_to_coords('56923000'), cep_to_coords('06449210'), cep_to_coords('04240080'), cep_to_coords('54766065'), cep_to_coords('54100014'), cep_to_coords('52221045'), cep_to_coords('52070561'), cep_to_coords('52060561'), cep_to_coords('52120201'), cep_to_coords('50060902'), cep_to_coords('54505605'), cep_to_coords('55024610'), cep_to_coords('54360030'), cep_to_coords('54589020'), cep_to_coords('59680000'), cep_to_coords('56308140'), cep_to_coords('54505050'), cep_to_coords('55004420'), cep_to_coords('55014250'), cep_to_coords('55016430'), cep_to_coords('53250210'), cep_to_coords('54589055'), cep_to_coords('65057030'), cep_to_coords('56909150'), cep_to_coords('55612040'), cep_to_coords('55610010'), cep_to_coords('55018561'), cep_to_coords('55018191'), cep_to_coords('55018193'), cep_to_coords('20091968'), cep_to_coords('55020100'), cep_to_coords('52140030'), cep_to_coords('50940165'), cep_to_coords('55014220'), cep_to_coords('55299487'), cep_to_coords('55006380'), cep_to_coords('55006390'), cep_to_coords('53431155'), cep_to_coords('54340090'), cep_to_coords('55016755'), cep_to_coords('56506150'), cep_to_coords('56519495'), cep_to_coords('56512370'), cep_to_coords('51350140'), cep_to_coords('51170470'), cep_to_coords('56505100'), cep_to_coords('56504115'), cep_to_coords('54745020'), cep_to_coords('55295510'), cep_to_coords('56304110'), cep_to_coords('55291140'), cep_to_coords('58805230'), cep_to_coords('51180060'), cep_to_coords('56503360'), cep_to_coords('53401570'), cep_to_coords('55004400'), cep_to_coords('55010540'), cep_to_coords('50680130'), cep_to_coords('55012630'), cep_to_coords('51170480'), cep_to_coords('51030630'), cep_to_coords('52120350'), cep_to_coords('55040120'), cep_to_coords('55024500'), cep_to_coords('55042560'), cep_to_coords('56317360'), cep_to_coords('53417420'), cep_to_coords('50980290'), cep_to_coords('55014021'), cep_to_coords('56308000'), cep_to_coords('56332520'), cep_to_coords('56306660'), cep_to_coords('56331070'), cep_to_coords('56323630'), cep_to_coords('56000300'), cep_to_coords('56302180'), cep_to_coords('55030460'), cep_to_coords('56105000'), cep_to_coords('53620859'), cep_to_coords('50730620'), cep_to_coords('52120510'), cep_to_coords('54350445'), cep_to_coords('56909272'), cep_to_coords('52120035'), cep_to_coords('51031480'), cep_to_coords('34360160'), cep_to_coords('52041610'), cep_to_coords('55608260'), cep_to_coords('56904090'), cep_to_coords('53200100'), cep_to_coords('55642050'), cep_to_coords('52191210'), cep_to_coords('56310640'), cep_to_coords('54350246'), cep_to_coords('50680150'), cep_to_coords('55024590'), cep_to_coords('54460455'), cep_to_coords('54090640'), cep_to_coords('55550970'), cep_to_coords('55641970'), cep_to_coords('55642605'), cep_to_coords('55816450'), cep_to_coords('50740350'), cep_to_coords('50630100'), cep_to_coords('55642140'), cep_to_coords('54330527'), cep_to_coords('56903150'), cep_to_coords('56903220'), cep_to_coords('56903467'), cep_to_coords('56906351'), cep_to_coords('56903290'), cep_to_coords('54310096'), cep_to_coords('50751170'), cep_to_coords('55158390'), cep_to_coords('55165000'), cep_to_coords('55294518'), cep_to_coords('50980270'), cep_to_coords('53260090'), cep_to_coords('55330999'), cep_to_coords('55290340'), cep_to_coords('55292250'), cep_to_coords('53640083'), cep_to_coords('55150220'), cep_to_coords('55505000'), cep_to_coords('55020595'), cep_to_coords('55292340'), cep_to_coords('53030170'), cep_to_coords('55296500'), cep_to_coords('50741011'), cep_to_coords('54520060'), cep_to_coords('53020330'), cep_to_coords('53640019'), cep_to_coords('50743360'), cep_to_coords('50910140'), cep_to_coords('53020340'), cep_to_coords('50660300'), cep_to_coords('51290500'), cep_to_coords('53020350'), cep_to_coords('54777025'), cep_to_coords('50980470'), cep_to_coords('55604170'), cep_to_coords('50090090'), cep_to_coords('52120012'), cep_to_coords('50980590'), cep_to_coords('52150155'), cep_to_coords('53635520'), cep_to_coords('55602230'), cep_to_coords('50830110'), cep_to_coords('50070010'), cep_to_coords('56890000'), cep_to_coords('53150570'), cep_to_coords('54300020'), cep_to_coords('53407400'), cep_to_coords('55602710'), cep_to_coords('55610355'), cep_to_coords('55604278'), cep_to_coords('55612240'), cep_to_coords('52060390'), cep_to_coords('56502130'), cep_to_coords('56503120'), cep_to_coords('56506640'), cep_to_coords('55610065'), cep_to_coords('52130386'), cep_to_coords('52061100'), cep_to_coords('51150450'), cep_to_coords('56519040'), cep_to_coords('53210400'), cep_to_coords('32333323'), cep_to_coords('55040220'), cep_to_coords('56517060'), cep_to_coords('55018330'), cep_to_coords('56906515'), cep_to_coords('55608035'), cep_to_coords('55000190'), cep_to_coords('24474295'), cep_to_coords('50680440'), cep_to_coords('54720035'), cep_to_coords('56306510'), cep_to_coords('50780400'), cep_to_coords('50110290'), cep_to_coords('50100160'), cep_to_coords('55042210'), cep_to_coords('50060450'), cep_to_coords('52211680'), cep_to_coords('56903070'), cep_to_coords('53230420'), cep_to_coords('53441410'), cep_to_coords('53407330'), cep_to_coords('53441110'), cep_to_coords('52221150'), cep_to_coords('50790185'), cep_to_coords('50870080'), cep_to_coords('74567900'), cep_to_coords('53320770'), cep_to_coords('50740200'), cep_to_coords('50960190'), cep_to_coords('53150000'), cep_to_coords('52041660'), cep_to_coords('52490325'), cep_to_coords('50160233'), cep_to_coords('56306230'), cep_to_coords('56309490'), cep_to_coords('56330400'), cep_to_coords('51200010'), cep_to_coords('55645030'), cep_to_coords('55643138'), cep_to_coords('56645030'), cep_to_coords('52150141'), cep_to_coords('53060001'), cep_to_coords('53060000'), cep_to_coords('52171302'), cep_to_coords('52081430'), cep_to_coords('52081450'), cep_to_coords('52160480'), cep_to_coords('51021400'), cep_to_coords('54480200'), cep_to_coords('51335000'), cep_to_coords('52040100'), cep_to_coords('53150280'), cep_to_coords('56302970'), cep_to_coords('52060260'), cep_to_coords('54080220'), cep_to_coords('50910150'), cep_to_coords('53330120'), cep_to_coords('47300000'), cep_to_coords('56906480'), cep_to_coords('56903279'), cep_to_coords('56903620'), cep_to_coords('54735050'), cep_to_coords('56915020'), cep_to_coords('56915120'), cep_to_coords('52044500'), cep_to_coords('53060340'), cep_to_coords('54120010'), cep_to_coords('50711525'), cep_to_coords('51150194'), cep_to_coords('56509586'), cep_to_coords('54300301'), cep_to_coords('50912301'), cep_to_coords('51330295'), cep_to_coords('55008170'), cep_to_coords('54774415'), cep_to_coords('55006200'), cep_to_coords('54771500'), cep_to_coords('51250190'), cep_to_coords('55002140'), cep_to_coords('56512130'), cep_to_coords('51300220'), cep_to_coords('55040260'), cep_to_coords('55028400'), cep_to_coords('56515140'), cep_to_coords('56511310'), cep_to_coords('56512100'), cep_to_coords('56507295'), cep_to_coords('56507255'), cep_to_coords('55018660'), cep_to_coords('54759525'), cep_to_coords('54762765'), cep_to_coords('50760430'), cep_to_coords('56519070'), cep_to_coords('56510100'), cep_to_coords('56509108'), cep_to_coords('56515280'), cep_to_coords('53010220'), cep_to_coords('56509900'), cep_to_coords('56328030'), cep_to_coords('51180040'), cep_to_coords('52010120'), cep_to_coords('52051020'), cep_to_coords('56505131'), cep_to_coords('55016420'), cep_to_coords('55034260'), cep_to_coords('56515360'), cep_to_coords('56517450'), cep_to_coords('54230091'), cep_to_coords('53080075'), cep_to_coords('54490035'), cep_to_coords('51110000'), cep_to_coords('54352305'), cep_to_coords('50680170'), cep_to_coords('51030070'), cep_to_coords('54330290'), cep_to_coords('54777810'), cep_to_coords('52130030'), cep_to_coords('54140500'), cep_to_coords('54325251'), cep_to_coords('52041710'), cep_to_coords('51260400'), cep_to_coords('54410180'), cep_to_coords('54410035'), cep_to_coords('56334899'), cep_to_coords('50630660'), cep_to_coords('04111968'), cep_to_coords('50770170'), cep_to_coords('50751325'), cep_to_coords('50710350'), cep_to_coords('50711100'), cep_to_coords('56320055'), cep_to_coords('53900900'), cep_to_coords('51350670'), cep_to_coords('54355040'), cep_to_coords('54230212'), cep_to_coords('50050050'), cep_to_coords('56903430'), cep_to_coords('52140500'), cep_to_coords('53585080'), cep_to_coords('52280403'), cep_to_coords('55002220'), cep_to_coords('55038470'), cep_to_coords('63180000'), cep_to_coords('51260390'), cep_to_coords('56320140'), cep_to_coords('56328020'), cep_to_coords('50875220'), cep_to_coords('53442170'), cep_to_coords('53160320'), cep_to_coords('56903120'), cep_to_coords('56912070'), cep_to_coords('56906230'), cep_to_coords('53090290'), cep_to_coords('53427230'), cep_to_coords('53620615'), cep_to_coords('54275140'), cep_to_coords('55038415'), cep_to_coords('54792560'), cep_to_coords('51240560'), cep_to_coords('56519020'), cep_to_coords('53370101'), cep_to_coords('50720335'), cep_to_coords('56922990'), cep_to_coords('56906535'), cep_to_coords('56906450'), cep_to_coords('53370092'), cep_to_coords('55022768'), cep_to_coords('55840999'), cep_to_coords('51170110'), cep_to_coords('50930015'), cep_to_coords('54080150'), cep_to_coords('53580390'), cep_to_coords('55614725'), cep_to_coords('51150290'), cep_to_coords('56903390'), cep_to_coords('52130547'), cep_to_coords('53240410'), cep_to_coords('52291023'), cep_to_coords('56503551'), cep_to_coords('52140090'), cep_to_coords('55002370'), cep_to_coords('53050430'), cep_to_coords('53417130'), cep_to_coords('52417130'), cep_to_coords('53565110'), cep_to_coords('57840000'), cep_to_coords('55293160'), cep_to_coords('50780600'), cep_to_coords('50070330'), cep_to_coords('51355024'), cep_to_coords('52280541'), cep_to_coords('53230360'), cep_to_coords('51345130'), cep_to_coords('50721640'), cep_to_coords('54762491'), cep_to_coords('50630480'), cep_to_coords('56506580'), cep_to_coords('55038360'), cep_to_coords('53401250'), cep_to_coords('54350340'), cep_to_coords('55016400'), cep_to_coords('52061470'), cep_to_coords('53417090'), cep_to_coords('55302000'), cep_to_coords('53409255'), cep_to_coords('52041190'), cep_to_coords('55032350'), cep_to_coords('55036745'), cep_to_coords('54420215'), cep_to_coords('53422120'), cep_to_coords('52030190'), cep_to_coords('55036280'), cep_to_coords('56503570'), cep_to_coords('52090720'), cep_to_coords('50800360'), cep_to_coords('55295525'), cep_to_coords('55006120'), cep_to_coords('55294763'), cep_to_coords('56328110'), cep_to_coords('51111080'), cep_to_coords('53625390'), cep_to_coords('55303000'), cep_to_coords('55010090'), cep_to_coords('55010155'), cep_to_coords('56506675'), cep_to_coords('56506540'), cep_to_coords('54410230'), cep_to_coords('55018370'), cep_to_coords('53530416'), cep_to_coords('55602680'), cep_to_coords('54100664'), cep_to_coords('55602460'), cep_to_coords('55032360'), cep_to_coords('55610140'), cep_to_coords('55602480'), cep_to_coords('55295400'), cep_to_coords('55614020'), cep_to_coords('56306480'), cep_to_coords('54740600'), cep_to_coords('54220785'), cep_to_coords('52280480'), cep_to_coords('50780290'), cep_to_coords('55294603'), cep_to_coords('55026075'), cep_to_coords('50980230'), cep_to_coords('51190290'), cep_to_coords('53170135'), cep_to_coords('53417120'), cep_to_coords('50870130'), cep_to_coords('5500000000'), cep_to_coords('56332170'), cep_to_coords('54730750'), cep_to_coords('51346120'), cep_to_coords('52291024'), cep_to_coords('55018213'), cep_to_coords('53620133'), cep_to_coords('52041350'), cep_to_coords('52170350'), cep_to_coords('55819355'), cep_to_coords('52061120'), cep_to_coords('55030020'), cep_to_coords('55036110'), cep_to_coords('53439190'), cep_to_coords('52091262'), cep_to_coords('55037110'), cep_to_coords('54767215'), cep_to_coords('55006310'), cep_to_coords('52131533'), cep_to_coords('55614033'), cep_to_coords('53580540'), cep_to_coords('50670000'), cep_to_coords('50670290'), cep_to_coords('52050038'), cep_to_coords('51200080'), cep_to_coords('52280660'), cep_to_coords('53160270'), cep_to_coords('55155440'), cep_to_coords('55038145'), cep_to_coords('56160000'), cep_to_coords('55151665'), cep_to_coords('52041480'), cep_to_coords('52030295'), cep_to_coords('50771340'), cep_to_coords('52031085'), cep_to_coords('52060000'), cep_to_coords('55018590'), cep_to_coords('56906170'), cep_to_coords('58038142'), cep_to_coords('55008490'), cep_to_coords('56340000'), cep_to_coords('56306498'), cep_to_coords('52131100'), cep_to_coords('54450120'), cep_to_coords('56309000'), cep_to_coords('49020140'), cep_to_coords('56906538'), cep_to_coords('53402115'), cep_to_coords('50771250'), cep_to_coords('56906225'), cep_to_coords('52031230'), cep_to_coords('54768490'), cep_to_coords('52130550'), cep_to_coords('54515410'), cep_to_coords('52190180'), cep_to_coords('52081050'), cep_to_coords('54515350'), cep_to_coords('54510996'), cep_to_coords('56906000'), cep_to_coords('56906280'), cep_to_coords('54765970'), cep_to_coords('55016565'), cep_to_coords('53402532'), cep_to_coords('53190002'), cep_to_coords('53170550'), cep_to_coords('53140180'), cep_to_coords('53080810'), cep_to_coords('54762180'), cep_to_coords('50680220'), cep_to_coords('50090190'), cep_to_coords('52040770'), cep_to_coords('53416610'), cep_to_coords('51560035'), cep_to_coords('50980460'), cep_to_coords('55150550'), cep_to_coords('53030155'), cep_to_coords('50100040'), cep_to_coords('55014075'), cep_to_coords('53416680'), cep_to_coords('55160000'), cep_to_coords('51320480'), cep_to_coords('50940190'), cep_to_coords('52210130'), cep_to_coords('43990000'), cep_to_coords('51240410'), cep_to_coords('52080200'), cep_to_coords('54510300'), cep_to_coords('53427360'), cep_to_coords('55151140'), cep_to_coords('55150270'), cep_to_coords('52171131'), cep_to_coords('55006320'), cep_to_coords('56503280'), cep_to_coords('56504130'), cep_to_coords('56510020'), cep_to_coords('56504090'), cep_to_coords('53409670'), cep_to_coords('50760040'), cep_to_coords('55024300'), cep_to_coords('53439280'), cep_to_coords('52191212'), cep_to_coords('52041520'), cep_to_coords('51240420'), cep_to_coords('56512600'), cep_to_coords('51130050'), cep_to_coords('56310460'), cep_to_coords('50910120'), cep_to_coords('56517500'), cep_to_coords('56485000'), cep_to_coords('52170140'), cep_to_coords('54325492'), cep_to_coords('55008280'), cep_to_coords('55036180'), cep_to_coords('55036580'), cep_to_coords('56515330'), cep_to_coords('56306020'), cep_to_coords('55034261'), cep_to_coords('53640731'), cep_to_coords('53050456'), cep_to_coords('52081533'), cep_to_coords('53150011'), cep_to_coords('52080520'), cep_to_coords('50740500'), cep_to_coords('54250173'), cep_to_coords('51180510'), cep_to_coords('51160910'), cep_to_coords('52160425'), cep_to_coords('50110560'), cep_to_coords('55026490'), cep_to_coords('54350050'), cep_to_coords('52071420'), cep_to_coords('54330480'), cep_to_coords('60000000'), cep_to_coords('56304440'), cep_to_coords('54330015'), cep_to_coords('54520130'), cep_to_coords('54515710'), cep_to_coords('54523040'), cep_to_coords('54470100'), cep_to_coords('54440380'), cep_to_coords('48601330'), cep_to_coords('50050975'), cep_to_coords('56316090'), cep_to_coords('50721750'), cep_to_coords('52091190'), cep_to_coords('53640425'), cep_to_coords('54765120'), cep_to_coords('54756041'), cep_to_coords('54774435'), cep_to_coords('52070560'), cep_to_coords('55818000'), cep_to_coords('53120340'), cep_to_coords('52280460'), cep_to_coords('52280620'), cep_to_coords('52081670'), cep_to_coords('56310030'), cep_to_coords('52051430'), cep_to_coords('52291160'), cep_to_coords('54720175'), cep_to_coords('53090620'), cep_to_coords('55014287'), cep_to_coords('51270160'), cep_to_coords('55642124'), cep_to_coords('55644302'), cep_to_coords('54515440'), cep_to_coords('56509822'), cep_to_coords('56912400'), cep_to_coords('56912540'), cep_to_coords('53240070'), cep_to_coords('53240080'), cep_to_coords('51230310'), cep_to_coords('56505070'), cep_to_coords('50751300'), cep_to_coords('54300042'), cep_to_coords('53320730'), cep_to_coords('52111270'), cep_to_coords('55016035'), cep_to_coords('53401180'), cep_to_coords('53435070'), cep_to_coords('51203320'), cep_to_coords('50780580'), cep_to_coords('51030720'), cep_to_coords('54756455'), cep_to_coords('53330130'), cep_to_coords('56306630'), cep_to_coords('50690700'), cep_to_coords('50860400'), cep_to_coords('50970150'), cep_to_coords('50610010'), cep_to_coords('56509610'), cep_to_coords('56506140'), cep_to_coords('54777050'), cep_to_coords('56512160'), cep_to_coords('54230102'), cep_to_coords('53630095'), cep_to_coords('53625320'), cep_to_coords('50620300'), cep_to_coords('56550358'), cep_to_coords('56512550'), cep_to_coords('55539800'), cep_to_coords('50720490'), cep_to_coords('56314450'), cep_to_coords('54320720'), cep_to_coords('56512510'), cep_to_coords('50040350'), cep_to_coords('50761180'), cep_to_coords('50781740'), cep_to_coords('55016390'), cep_to_coords('51345480'), cep_to_coords('53431165'), cep_to_coords('51290380'), cep_to_coords('50110350'), cep_to_coords('54160590'), cep_to_coords('55642550'), cep_to_coords('55640001'), cep_to_coords('55006332'), cep_to_coords('54350270'), cep_to_coords('56304240'), cep_to_coords('55642680'), cep_to_coords('50690160'), cep_to_coords('54250021'), cep_to_coords('54762784'), cep_to_coords('50030170'), cep_to_coords('52080351'), cep_to_coords('54315560'), cep_to_coords('05857390'), cep_to_coords('55024075'), cep_to_coords('51150110'), cep_to_coords('54330805'), cep_to_coords('54470295'), cep_to_coords('53130430'), cep_to_coords('53620545'), cep_to_coords('56906070'), cep_to_coords('52280640'), cep_to_coords('55038110'), cep_to_coords('54756784'), cep_to_coords('54768540'), cep_to_coords('54762362'), cep_to_coords('54735060'), cep_to_coords('54759050'), cep_to_coords('51121580'), cep_to_coords('53433630'), cep_to_coords('54777553'), cep_to_coords('56306370'), cep_to_coords('56309430'), cep_to_coords('55020150'), cep_to_coords('55036202'), cep_to_coords('48630000'), cep_to_coords('52160234'), cep_to_coords('50040720'), cep_to_coords('54310250'), cep_to_coords('52050190'), cep_to_coords('56909651'), cep_to_coords('55016680'), cep_to_coords('54535110'), cep_to_coords('55190311'), cep_to_coords('50761510'), cep_to_coords('54330490'), cep_to_coords('56330380'), cep_to_coords('54360072'), cep_to_coords('54589225'), cep_to_coords('52191360'), cep_to_coords('55000990'), cep_to_coords('55190971'), cep_to_coords('53260080'), cep_to_coords('50771016'), cep_to_coords('55024175'), cep_to_coords('56512275'), cep_to_coords('55150040'), cep_to_coords('53580045'), cep_to_coords('56860000'), cep_to_coords('51250180'), cep_to_coords('54220060'), cep_to_coords('56332465'), cep_to_coords('53402230'), cep_to_coords('55151740'), cep_to_coords('56328790'), cep_to_coords('56511010'), cep_to_coords('55192617'), cep_to_coords('56517020'), cep_to_coords('55010430'), cep_to_coords('53010100'), cep_to_coords('51240400'), cep_to_coords('54460449'), cep_to_coords('56515050'), cep_to_coords('53180001'), cep_to_coords('53415510'), cep_to_coords('56330122'), cep_to_coords('55010370'), cep_to_coords('54330013'), cep_to_coords('54100370'), cep_to_coords('55010190'), cep_to_coords('56303310'), cep_to_coords('53435470'), cep_to_coords('54140632'), cep_to_coords('50771280'), cep_to_coords('55030390'), cep_to_coords('50865190'), cep_to_coords('50790041'), cep_to_coords('50820403'), cep_to_coords('54705185'), cep_to_coords('54777395'), cep_to_coords('53370650'), cep_to_coords('52081480'), cep_to_coords('50980390'), cep_to_coords('50950060'), cep_to_coords('52110515'), cep_to_coords('51170445'), cep_to_coords('50670200'), cep_to_coords('50100390'), cep_to_coords('53110710'), cep_to_coords('55002035'), cep_to_coords('56320810'), cep_to_coords('55296250'), cep_to_coords('56903238'), cep_to_coords('08111971'), cep_to_coords('56330260'), cep_to_coords('54250003'), cep_to_coords('56330020'), cep_to_coords('20725260'), cep_to_coords('53415300'), cep_to_coords('53439155'), cep_to_coords('54400280'), cep_to_coords('54410222'), cep_to_coords('55294535'), cep_to_coords('55295215'), cep_to_coords('55299505'), cep_to_coords('51020031'), cep_to_coords('50781590'), cep_to_coords('55194357'), cep_to_coords('55036025'), cep_to_coords('52121130'), cep_to_coords('50110537'), cep_to_coords('54320140'), cep_to_coords('55610030'), cep_to_coords('52091154'), cep_to_coords('53110480'), cep_to_coords('53431830'), cep_to_coords('52280580'), cep_to_coords('55641778'), cep_to_coords('55644150'), cep_to_coords('55641310'), cep_to_coords('55643060'), cep_to_coords('55641075'), cep_to_coords('52170010'), cep_to_coords('53437140'), cep_to_coords('03244090'), cep_to_coords('55220000'), cep_to_coords('56903590'), cep_to_coords('56909300'), cep_to_coords('52090385'), cep_to_coords('53439410'), cep_to_coords('54394103'), cep_to_coords('53630053'), cep_to_coords('53300230'), cep_to_coords('54515340'), cep_to_coords('50090400'), cep_to_coords('59185000'), cep_to_coords('53620118'), cep_to_coords('50830540'), cep_to_coords('50760260'), cep_to_coords('50820520'), cep_to_coords('51230402'), cep_to_coords('52291113'), cep_to_coords('51330170'), cep_to_coords('51350540'), cep_to_coords('55641190'), cep_to_coords('50090550'), cep_to_coords('52021120'), cep_to_coords('53441201'), cep_to_coords('54440370'), cep_to_coords('51330200'), cep_to_coords('54330422'), cep_to_coords('51350370'), cep_to_coords('54280547'), cep_to_coords('50650180'), cep_to_coords('53444360'), cep_to_coords('55155510'), cep_to_coords('51310230'), cep_to_coords('55158430'), cep_to_coords('51290590'), cep_to_coords('52041800'), cep_to_coords('54720071'), cep_to_coords('55150005'), cep_to_coords('50850160'), cep_to_coords('55152380'), cep_to_coords('51021390'), cep_to_coords('54759135'), cep_to_coords('50721755'), cep_to_coords('54350030'), cep_to_coords('54580245'), cep_to_coords('55641120'), cep_to_coords('50721320'), cep_to_coords('54120040'), cep_to_coords('56322610'), cep_to_coords('55014755'), cep_to_coords('54789835'), cep_to_coords('56512290'), cep_to_coords('53120220'), cep_to_coords('55297160'), cep_to_coords('54330050'), cep_to_coords('03961030'), cep_to_coords('52190281'), cep_to_coords('51345730'), cep_to_coords('55192060'), cep_to_coords('56395970'), cep_to_coords('55022300'), cep_to_coords('54765360'), cep_to_coords('55195515'), cep_to_coords('50791000'), cep_to_coords('53425080'), cep_to_coords('56332190'), cep_to_coords('56320750'), cep_to_coords('56330360'), cep_to_coords('50010430'), cep_to_coords('52171090'), cep_to_coords('55606460'), cep_to_coords('50050390'), cep_to_coords('55024470'), cep_to_coords('52490030'), cep_to_coords('50781330'), cep_to_coords('50740220'), cep_to_coords('56309050'), cep_to_coords('53150680'), cep_to_coords('53150020'), cep_to_coords('51180260'), cep_to_coords('50810140'), cep_to_coords('51350090'), cep_to_coords('50041055'), cep_to_coords('54780320'), cep_to_coords('52120275'), cep_to_coords('51030771'), cep_to_coords('52221305'), cep_to_coords('55608130'), cep_to_coords('50080520'), cep_to_coords('54800992'), cep_to_coords('66666666'), cep_to_coords('55042090'), cep_to_coords('54510160'), cep_to_coords('54525560'), cep_to_coords('53625215'), cep_to_coords('53409420'), cep_to_coords('54515080'), cep_to_coords('54535330'), cep_to_coords('54580390'), cep_to_coords('54580440'), cep_to_coords('54250600'), cep_to_coords('54589040'), cep_to_coords('55608315'), cep_to_coords('55610354'), cep_to_coords('54100500'), cep_to_coords('53550560'), cep_to_coords('53530490'), cep_to_coords('55606803'), cep_to_coords('53416540'), cep_to_coords('53240510'), cep_to_coords('53413600'), cep_to_coords('53230450'), cep_to_coords('53442130'), cep_to_coords('53421650'), cep_to_coords('53300170'), cep_to_coords('51030420'), cep_to_coords('51280150'), cep_to_coords('51190400'), cep_to_coords('50791340'), cep_to_coords('50850030'), cep_to_coords('51030740'), cep_to_coords('51160035'), cep_to_coords('52060200'), cep_to_coords('50070395'), cep_to_coords('54580570'), cep_to_coords('54230597'), cep_to_coords('55607400'), cep_to_coords('55612145'), cep_to_coords('55612243'), cep_to_coords('54410605'), cep_to_coords('55604380'), cep_to_coords('54120441'), cep_to_coords('54340486'), cep_to_coords('54230121'), cep_to_coords('54450151'), cep_to_coords('54450160'), cep_to_coords('55602520'), cep_to_coords('54330410'), cep_to_coords('54080400'), cep_to_coords('56000080'), cep_to_coords('50620705'), cep_to_coords('52090240'), cep_to_coords('52201220'), cep_to_coords('52071182'), cep_to_coords('55038775'), cep_to_coords('51020080'), cep_to_coords('52031021'), cep_to_coords('53401670'), cep_to_coords('53545620'), cep_to_coords('52221031'), cep_to_coords('53409350'), cep_to_coords('55010280'), cep_to_coords('55195097'), cep_to_coords('55194245'), cep_to_coords('54768267'), cep_to_coords('54762630'), cep_to_coords('54756505'), cep_to_coords('54759016'), cep_to_coords('55291380'), cep_to_coords('55295160'), cep_to_coords('53530476'), cep_to_coords('52081300'), cep_to_coords('55192000'), cep_to_coords('55196065'), cep_to_coords('55190052'), cep_to_coords('21171260'), cep_to_coords('53435670'), cep_to_coords('54767680'), cep_to_coords('51011050'), cep_to_coords('54768792'), cep_to_coords('55022235'), cep_to_coords('52070550'), cep_to_coords('55643090'), cep_to_coords('56312808'), cep_to_coords('53080290'), cep_to_coords('51111020'), cep_to_coords('50870110'), cep_to_coords('56316470'), cep_to_coords('55644010'), cep_to_coords('55643240'), cep_to_coords('52050405'), cep_to_coords('55640991'), cep_to_coords('54580100'), cep_to_coords('54500990'), cep_to_coords('52401550'), cep_to_coords('51320030'), cep_to_coords('54768080'), cep_to_coords('54330510'), cep_to_coords('51160380'), cep_to_coords('50751655'), cep_to_coords('54230112'), cep_to_coords('54350305'), cep_to_coords('53620250'), cep_to_coords('54759102'), cep_to_coords('55610060'), cep_to_coords('54440590'), cep_to_coords('52071362'), cep_to_coords('53330110'), cep_to_coords('55614500'), cep_to_coords('03982000'), cep_to_coords('50741140'), cep_to_coords('53409580'), cep_to_coords('54430000'), cep_to_coords('52110165'), cep_to_coords('53270431'), cep_to_coords('52050361'), cep_to_coords('50050075'), cep_to_coords('54080490'), cep_to_coords('53140270'), cep_to_coords('53442040'), cep_to_coords('53210290'), cep_to_coords('50751200'), cep_to_coords('53530220'), cep_to_coords('50790721'), cep_to_coords('55158740'), cep_to_coords('55152330'), cep_to_coords('54735440'), cep_to_coords('53350040'), cep_to_coords('55014644'), cep_to_coords('56326300'), cep_to_coords('51300210'), cep_to_coords('50720560'), cep_to_coords('55020201'), cep_to_coords('50690220'), cep_to_coords('50400303'), cep_to_coords('50751695'), cep_to_coords('54437120'), cep_to_coords('54759390'), cep_to_coords('50770440'), cep_to_coords('55031080'), cep_to_coords('52291000'), cep_to_coords('56909270'), cep_to_coords('50690090'), cep_to_coords('54580765'), cep_to_coords('54260013'), cep_to_coords('54580275'), cep_to_coords('52060615'), cep_to_coords('51170090'), cep_to_coords('53120250'), cep_to_coords('50780080'), cep_to_coords('54330755'), cep_to_coords('51270540'), cep_to_coords('50720600'), cep_to_coords('52221001'), cep_to_coords('50730390'), cep_to_coords('52090210'), cep_to_coords('54520765'), cep_to_coords('50090630'), cep_to_coords('53080610'), cep_to_coords('53635230'), cep_to_coords('26017000'), cep_to_coords('50760510'), cep_to_coords('53190130'), cep_to_coords('52060310'), cep_to_coords('54080200'), cep_to_coords('53140040'), cep_to_coords('55158320'), cep_to_coords('55158760'), cep_to_coords('54210500'), cep_to_coords('55154507'), cep_to_coords('52280104'), cep_to_coords('50630520'), cep_to_coords('54505025'), cep_to_coords('55008400'), cep_to_coords('51010250'), cep_to_coords('52110090'), cep_to_coords('55299500'), cep_to_coords('55155050'), cep_to_coords('50806220'), cep_to_coords('52214060'), cep_to_coords('55602450'), cep_to_coords('52140390'), cep_to_coords('50960020'), cep_to_coords('54240420'), cep_to_coords('56312191'), cep_to_coords('54759345'), cep_to_coords('50920603'), cep_to_coords('51170650'), cep_to_coords('54762330'), cep_to_coords('50640525'), cep_to_coords('54220070'), cep_to_coords('52050250'), cep_to_coords('54440390'), cep_to_coords('50720170'), cep_to_coords('56330055'), cep_to_coords('56435435'), cep_to_coords('56302150'), cep_to_coords('54440310'), cep_to_coords('53409110'), cep_to_coords('63260000'), cep_to_coords('56503350'), cep_to_coords('56912251'), cep_to_coords('52070635'), cep_to_coords('50781735'), cep_to_coords('51290400'), cep_to_coords('55291684'), cep_to_coords('55040140'), cep_to_coords('50060540'), cep_to_coords('56323820'), cep_to_coords('56318100'), cep_to_coords('56507340'), cep_to_coords('51190430'), cep_to_coords('51290480'), cep_to_coords('52280210'), cep_to_coords('53409100'), cep_to_coords('50680310'), cep_to_coords('50711050'), cep_to_coords('56316698'), cep_to_coords('55297035'), cep_to_coords('55295375'), cep_to_coords('54330590'), cep_to_coords('55291250'), cep_to_coords('54240900'), cep_to_coords('50600100'), cep_to_coords('55151635'), cep_to_coords('50680380'), cep_to_coords('53230660'), cep_to_coords('54400530'), cep_to_coords('52291600'), cep_to_coords('50110610'), cep_to_coords('56321000'), cep_to_coords('53220260'), cep_to_coords('51020300'), cep_to_coords('50110830'), cep_to_coords('55612235'), cep_to_coords('53403100'), cep_to_coords('56503460'), cep_to_coords('51010120'), cep_to_coords('52120245'), cep_to_coords('50640690'), cep_to_coords('50900220'), cep_to_coords('53421800'), cep_to_coords('54230085'), cep_to_coords('54320380'), cep_to_coords('50920075'), cep_to_coords('53640578'), cep_to_coords('54762400'), cep_to_coords('54517485'), cep_to_coords('54580675'), cep_to_coords('54552035'), cep_to_coords('50050100'), cep_to_coords('54160425'), cep_to_coords('54530130'), cep_to_coords('54530120'), cep_to_coords('54517245'), cep_to_coords('54525080'), cep_to_coords('54535280'), cep_to_coords('54580410'), cep_to_coords('54520420'), cep_to_coords('54505170'), cep_to_coords('54580636'), cep_to_coords('54410490'), cep_to_coords('53421130'), cep_to_coords('53510190'), cep_to_coords('50731284'), cep_to_coords('54670380'), cep_to_coords('50875200'), cep_to_coords('54430050'), cep_to_coords('54100570'), cep_to_coords('55195249'), cep_to_coords('54070240'), cep_to_coords('54150680'), cep_to_coords('54210080'), cep_to_coords('55191692'), cep_to_coords('54220800'), cep_to_coords('54140491'), cep_to_coords('50900270'), cep_to_coords('54768495'), cep_to_coords('54759422'), cep_to_coords('54759645'), cep_to_coords('52041120'), cep_to_coords('52070643'), cep_to_coords('54440081'), cep_to_coords('54170641'), cep_to_coords('54090010'), cep_to_coords('54330700'), cep_to_coords('55610210'), cep_to_coords('55620010'), cep_to_coords('55604020'), cep_to_coords('50610515'), cep_to_coords('56304360'), cep_to_coords('56512070'), cep_to_coords('52060440'), cep_to_coords('55022600'), cep_to_coords('54786290'), cep_to_coords('56903260'), cep_to_coords('54360040'), cep_to_coords('56903050'), cep_to_coords('56903248'), cep_to_coords('56912290'), cep_to_coords('56906430'), cep_to_coords('56909164'), cep_to_coords('50630590'), cep_to_coords('51230370'), cep_to_coords('54290090'), cep_to_coords('50721570'), cep_to_coords('53120110'), cep_to_coords('50680785'), cep_to_coords('53270280'), cep_to_coords('52091610'), cep_to_coords('52171110'), cep_to_coords('50650250'), cep_to_coords('53429240'), cep_to_coords('50741280'), cep_to_coords('54756812'), cep_to_coords('15417000'), cep_to_coords('51300090'), cep_to_coords('50050025'), cep_to_coords('51240000'), cep_to_coords('50630440'), cep_to_coords('50920100'), cep_to_coords('53401210'), cep_to_coords('50630280'), cep_to_coords('53580700'), cep_to_coords('55158020'), cep_to_coords('55157346'), cep_to_coords('55158100'), cep_to_coords('54260015'), cep_to_coords('54768620'), cep_to_coords('55805000'), cep_to_coords('51345020'), cep_to_coords('51190030'), cep_to_coords('51230100'), cep_to_coords('55597979'), cep_to_coords('51270480'), cep_to_coords('53433180'), cep_to_coords('50730320'), cep_to_coords('51345390'), cep_to_coords('55157250'), cep_to_coords('53417701'), cep_to_coords('55158085'), cep_to_coords('55155070'), cep_to_coords('55010210'), cep_to_coords('53437760'), cep_to_coords('55298665'), cep_to_coords('52120150'), cep_to_coords('50640710'), cep_to_coords('51170420'), cep_to_coords('54353300'), cep_to_coords('55297000'), cep_to_coords('53280080'), cep_to_coords('55293220'), cep_to_coords('55024050'), cep_to_coords('56512480'), cep_to_coords('50630790'), cep_to_coords('56320195'), cep_to_coords('50100015'), cep_to_coords('53423140'), cep_to_coords('55036020'), cep_to_coords('35588000'), cep_to_coords('54240440'), cep_to_coords('53443000'), cep_to_coords('56515200'), cep_to_coords('53403680'), cep_to_coords('51310310'), cep_to_coords('56515460'), cep_to_coords('53240587'), cep_to_coords('55016240'), cep_to_coords('52280220'), cep_to_coords('56304020'), cep_to_coords('50640320'), cep_to_coords('53444280'), cep_to_coords('53401481'), cep_to_coords('54759675'), cep_to_coords('56321630'), cep_to_coords('52070030'), cep_to_coords('50630350'), cep_to_coords('50630360'), cep_to_coords('53230330'), cep_to_coords('51150480'), cep_to_coords('50771090'), cep_to_coords('54720000'), cep_to_coords('54320040'), cep_to_coords('50730290'), cep_to_coords('56306335'), cep_to_coords('50740360'), cep_to_coords('52150010'), cep_to_coords('52080123'), cep_to_coords('56302690'), cep_to_coords('54762224'), cep_to_coords('54580070'), cep_to_coords('54783075'), cep_to_coords('54720293'), cep_to_coords('53620330'), cep_to_coords('53190200'), cep_to_coords('54735040'), cep_to_coords('56320780'), cep_to_coords('55297010'), cep_to_coords('55292760'), cep_to_coords('52171269'), cep_to_coords('50940590'), cep_to_coords('54160355'), cep_to_coords('56000800'), cep_to_coords('54520410'), cep_to_coords('55602630'), cep_to_coords('54571100'), cep_to_coords('54120270'), cep_to_coords('55612130'), cep_to_coords('54325715'), cep_to_coords('56304570'), cep_to_coords('56345000'), cep_to_coords('54762642'), cep_to_coords('54705000'), cep_to_coords('55038651'), cep_to_coords('55044070'), cep_to_coords('50610350'), cep_to_coords('54470140'), cep_to_coords('53402723'), cep_to_coords('55610080'), cep_to_coords('55608420'), cep_to_coords('51190220'), cep_to_coords('53409340'), cep_to_coords('55444110'), cep_to_coords('52111020'), cep_to_coords('53530580'), cep_to_coords('50060295'), cep_to_coords('54320160'), cep_to_coords('54520530'), cep_to_coords('54430240'), cep_to_coords('54520200'), cep_to_coords('54350700'), cep_to_coords('54350230'), cep_to_coords('54440240'), cep_to_coords('50731500'), cep_to_coords('50680370'), cep_to_coords('53370520'), cep_to_coords('53417708'), cep_to_coords('55296600'), cep_to_coords('54410274'), cep_to_coords('55612020'), cep_to_coords('50400600'), cep_to_coords('53620796'), cep_to_coords('51280030'), cep_to_coords('51150725'), cep_to_coords('52071211'), cep_to_coords('54240100'), cep_to_coords('54150160'), cep_to_coords('53300090'), cep_to_coords('53370250'), cep_to_coords('51240310'), cep_to_coords('54430311'), cep_to_coords('55606640'), cep_to_coords('54735125'), cep_to_coords('50940200'), cep_to_coords('54110041'), cep_to_coords('53070250'), cep_to_coords('53350000'), cep_to_coords('53450390'), cep_to_coords('53090040'), cep_to_coords('51280500'), cep_to_coords('51320450'), cep_to_coords('54330780'), cep_to_coords('54270222'), cep_to_coords('50960290'), cep_to_coords('53417250'), cep_to_coords('55641340'), cep_to_coords('50640290'), cep_to_coords('55024158'), cep_to_coords('55038550'), cep_to_coords('55645152'), cep_to_coords('54090040'), cep_to_coords('50770310'), cep_to_coords('51320100'), cep_to_coords('51250360'), cep_to_coords('55642145'), cep_to_coords('53025010'), cep_to_coords('50830270'), cep_to_coords('58326000'), cep_to_coords('52071151'), cep_to_coords('55038038'), cep_to_coords('51023210'), cep_to_coords('54735670'), cep_to_coords('50711092'), cep_to_coords('18270001'), cep_to_coords('52280300'), cep_to_coords('53421100'), cep_to_coords('55602700'), cep_to_coords('55291300'), cep_to_coords('55297090'), cep_to_coords('05340000'), cep_to_coords('51345410'), cep_to_coords('50942019'), cep_to_coords('52490020'), cep_to_coords('54470120'), cep_to_coords('55014161'), cep_to_coords('55028230'), cep_to_coords('55813440'), cep_to_coords('56332385'), cep_to_coords('50920230'), cep_to_coords('51350570'), cep_to_coords('53480120'), cep_to_coords('55020080'), cep_to_coords('53421391'), cep_to_coords('53320700'), cep_to_coords('50781420'), cep_to_coords('53825000'), cep_to_coords('52120430'), cep_to_coords('51110090'), cep_to_coords('54762060'), cep_to_coords('55022040'), cep_to_coords('55295515'), cep_to_coords('55295230'), cep_to_coords('55290630'), cep_to_coords('55291735'), cep_to_coords('50080970'), cep_to_coords('53230470'), cep_to_coords('54340060'), cep_to_coords('53635735'), cep_to_coords('53530575'), cep_to_coords('55036050'), cep_to_coords('12248628'), cep_to_coords('56332010'), cep_to_coords('54320035'), cep_to_coords('51260200'), cep_to_coords('52071323'), cep_to_coords('54727370'), cep_to_coords('54080210'), cep_to_coords('55031030'), cep_to_coords('50700300'), cep_to_coords('51010680'), cep_to_coords('54510122'), cep_to_coords('53250340'), cep_to_coords('56506520'), cep_to_coords('54765315'), cep_to_coords('50930180'), cep_to_coords('51200070'), cep_to_coords('53320160'), cep_to_coords('55038560'), cep_to_coords('55004470'), cep_to_coords('54325041'), cep_to_coords('53640060'), cep_to_coords('54325060'), cep_to_coords('50751380'), cep_to_coords('53413420'), cep_to_coords('53520580'), cep_to_coords('52070110'), cep_to_coords('53540360'), cep_to_coords('55190788'), cep_to_coords('55190600'), cep_to_coords('55016250'), cep_to_coords('55614560'), cep_to_coords('51052020'), cep_to_coords('55608250'), cep_to_coords('55642108'), cep_to_coords('55641400'), cep_to_coords('55645000'), cep_to_coords('56306080'), cep_to_coords('52291800'), cep_to_coords('53050230'), cep_to_coords('54505585'), cep_to_coords('54589230'), cep_to_coords('55294220'), cep_to_coords('50900360'), cep_to_coords('50860190'), cep_to_coords('51150550'), cep_to_coords('52291090'), cep_to_coords('50790490'), cep_to_coords('55819190'), cep_to_coords('51330008'), cep_to_coords('50761100'), cep_to_coords('50865070'), cep_to_coords('54240400'), cep_to_coords('52291076'), cep_to_coords('54160720'), cep_to_coords('53050140'), cep_to_coords('53420150'), cep_to_coords('50720210'), cep_to_coords('53330240'), cep_to_coords('50940602'), cep_to_coords('52280090'), cep_to_coords('50650140'), cep_to_coords('53433750'), cep_to_coords('52061115'), cep_to_coords('55158060'), cep_to_coords('50640330'), cep_to_coords('51010150'), cep_to_coords('54774100'), cep_to_coords('56320795'), cep_to_coords('51203910'), cep_to_coords('50730030'), cep_to_coords('53350490'), cep_to_coords('51761058'), cep_to_coords('52091187'), cep_to_coords('54220246'), cep_to_coords('50780602'), cep_to_coords('54420140'), cep_to_coords('53560640'), cep_to_coords('51010330'), cep_to_coords('54170090'), cep_to_coords('56332450'), cep_to_coords('51340410'), cep_to_coords('54270420'), cep_to_coords('50053000'), cep_to_coords('56519475'), cep_to_coords('56516100'), cep_to_coords('55155411'), cep_to_coords('56512115'), cep_to_coords('52111623'), cep_to_coords('52090062'), cep_to_coords('52120311'), cep_to_coords('50192309'), cep_to_coords('54220715'), cep_to_coords('54720050'), cep_to_coords('50860390'), cep_to_coords('05012010'), cep_to_coords('50100460'), cep_to_coords('53030070'), cep_to_coords('55031130'), cep_to_coords('55295580'), cep_to_coords('55294545'), cep_to_coords('55290385'), cep_to_coords('55299385'), cep_to_coords('55290493'), cep_to_coords('55294665'), cep_to_coords('55294000'), cep_to_coords('55220294'), cep_to_coords('55298645'), cep_to_coords('55298140'), cep_to_coords('55296035'), cep_to_coords('55299536'), cep_to_coords('55295380'), cep_to_coords('55294150'), cep_to_coords('55014467'), cep_to_coords('55297685'), cep_to_coords('55150090'), cep_to_coords('56515420'), cep_to_coords('55038215'), cep_to_coords('53400701'), cep_to_coords('52030150'), cep_to_coords('56551140'), cep_to_coords('50123013'), cep_to_coords('55194270'), cep_to_coords('50670400'), cep_to_coords('55028370'), cep_to_coords('55604440'), cep_to_coords('53060668'), cep_to_coords('52291205'), cep_to_coords('52291110'), cep_to_coords('50741500'), cep_to_coords('51310380'), cep_to_coords('54080320'), cep_to_coords('54240060'), cep_to_coords('50820400'), cep_to_coords('55024440'), cep_to_coords('50830060'), cep_to_coords('55015335'), cep_to_coords('50721360'), cep_to_coords('53020280'), cep_to_coords('53250600'), cep_to_coords('55612410'), cep_to_coords('55022220'), cep_to_coords('54440570'), cep_to_coords('52031160'), cep_to_coords('52061480'), cep_to_coords('54325031'), cep_to_coords('54440020'), cep_to_coords('58912190'), cep_to_coords('55158530'), cep_to_coords('52291100'), cep_to_coords('52090675'), cep_to_coords('52171290'), cep_to_coords('52071255'), cep_to_coords('51275660'), cep_to_coords('50670610'), cep_to_coords('50060410'), cep_to_coords('48903190'), cep_to_coords('52111570'), cep_to_coords('50610390'), cep_to_coords('54756090'), cep_to_coords('53403010'), cep_to_coords('50650310'), cep_to_coords('55036445'), cep_to_coords('48306347'), cep_to_coords('56303347'), cep_to_coords('55641150'), cep_to_coords('55642160'), cep_to_coords('56318360'), cep_to_coords('54589200'), cep_to_coords('52131295'), cep_to_coords('50720715'), cep_to_coords('71324870'), cep_to_coords('52050035'), cep_to_coords('56906050'), cep_to_coords('56909370'), cep_to_coords('54365000'), cep_to_coords('56918000'), cep_to_coords('55019035'), cep_to_coords('51011051'), cep_to_coords('53431255'), cep_to_coords('54150120'), cep_to_coords('52060376'), cep_to_coords('50240000'), cep_to_coords('50060090'), cep_to_coords('50870480'), cep_to_coords('51345150'), cep_to_coords('50030050'), cep_to_coords('54330635'), cep_to_coords('52130091'), cep_to_coords('53300130'), cep_to_coords('52170320'), cep_to_coords('53290320'), cep_to_coords('51260250'), cep_to_coords('54525375'), cep_to_coords('54330760'), cep_to_coords('53070130'), cep_to_coords('50910050'), cep_to_coords('52130205'), cep_to_coords('53200620'), cep_to_coords('55291859'), cep_to_coords('53220000'), cep_to_coords('55813330'), cep_to_coords('53423300'), cep_to_coords('52080093'), cep_to_coords('54250171'), cep_to_coords('54325291'), cep_to_coords('54210463'), cep_to_coords('52913291'), cep_to_coords('54460025'), cep_to_coords('55643000'), cep_to_coords('52080141'), cep_to_coords('54520350'), cep_to_coords('50515005'), cep_to_coords('54737110'), cep_to_coords('52110240'), cep_to_coords('52221190'), cep_to_coords('52231295'), cep_to_coords('50791180'), cep_to_coords('52190222'), cep_to_coords('54330100'), cep_to_coords('54720675'), cep_to_coords('53431330'), cep_to_coords('51030210'), cep_to_coords('55024272'), cep_to_coords('54325021'), cep_to_coords('50060150'), cep_to_coords('54160231'), cep_to_coords('50865130'), cep_to_coords('54220090'), cep_to_coords('54325220'), cep_to_coords('15385000'), cep_to_coords('52131062'), cep_to_coords('55152450'), cep_to_coords('54759070'), cep_to_coords('54250262'), cep_to_coords('53370600'), cep_to_coords('550000000'), cep_to_coords('55152030'), cep_to_coords('50791301'), cep_to_coords('54777290'), cep_to_coords('54735755'), cep_to_coords('53444390'), cep_to_coords('51270380'), cep_to_coords('55290360'), cep_to_coords('55294265'), cep_to_coords('55295555'), cep_to_coords('55259000'), cep_to_coords('55292650'), cep_to_coords('55294380'), cep_to_coords('55295310'), cep_to_coords('55294395'), cep_to_coords('55297560'), cep_to_coords('55294520'), cep_to_coords('52050202'), cep_to_coords('51230485'), cep_to_coords('55292125'), cep_to_coords('53429085'), cep_to_coords('56512380'), cep_to_coords('56517030'), cep_to_coords('50740340'), cep_to_coords('54410323'), cep_to_coords('53370230'), cep_to_coords('56328120'), cep_to_coords('55014450'), cep_to_coords('55036170'), cep_to_coords('55014135'), cep_to_coords('56320745'), cep_to_coords('54315185'), cep_to_coords('54240070'), cep_to_coords('55295150'), cep_to_coords('53405263'), cep_to_coords('56505350'), cep_to_coords('51340165'), cep_to_coords('53340470'), cep_to_coords('54220131'), cep_to_coords('51345331'), cep_to_coords('52090085'), cep_to_coords('52191565'), cep_to_coords('56314500'), cep_to_coords('50790205'), cep_to_coords('50409610'), cep_to_coords('56326120'), cep_to_coords('55643640'), cep_to_coords('53620570'), cep_to_coords('53040151'), cep_to_coords('51350450'), cep_to_coords('53433780'), cep_to_coords('50850090'), cep_to_coords('55608510'), cep_to_coords('54170023'), cep_to_coords('54330562'), cep_to_coords('54759245'), cep_to_coords('54330230'), cep_to_coords('53565380'), cep_to_coords('50070340'), cep_to_coords('50731272'), cep_to_coords('50830350'), cep_to_coords('50680160'), cep_to_coords('51111021'), cep_to_coords('53444290'), cep_to_coords('51270691'), cep_to_coords('54290315'), cep_to_coords('55028450'), cep_to_coords('51300010'), cep_to_coords('54762260'), cep_to_coords('54768040'), cep_to_coords('54783250'), cep_to_coords('55190576'), cep_to_coords('55196000'), cep_to_coords('55192390'), cep_to_coords('51290570'), cep_to_coords('55292603'), cep_to_coords('54230630'), cep_to_coords('52280518'), cep_to_coords('56515410'), cep_to_coords('53090310'), cep_to_coords('55038290'), cep_to_coords('54400170'), cep_to_coords('04752005'), cep_to_coords('54350690'), cep_to_coords('54280380'), cep_to_coords('50960430'), cep_to_coords('50761190'), cep_to_coords('54230640'), cep_to_coords('52091155'), cep_to_coords('53630494'), cep_to_coords('54735796'), cep_to_coords('52060502'), cep_to_coords('55012190'), cep_to_coords('55150021'), cep_to_coords('50760235'), cep_to_coords('50030590'), cep_to_coords('55018290'), cep_to_coords('55040200'), cep_to_coords('55028130'), cep_to_coords('55036385'), cep_to_coords('55036500'), cep_to_coords('55006480'), cep_to_coords('55008144'), cep_to_coords('55666666'), cep_to_coords('55034561'), cep_to_coords('53407420'), cep_to_coords('55036220'), cep_to_coords('56503090'), cep_to_coords('54460280'), cep_to_coords('55620970'), cep_to_coords('51340660'), cep_to_coords('50110172'), cep_to_coords('56302971'), cep_to_coords('55500970'), cep_to_coords('05078000'), cep_to_coords('51310120'), cep_to_coords('53404000'), cep_to_coords('53416590'), cep_to_coords('54340200'), cep_to_coords('55819715'), cep_to_coords('53409750'), cep_to_coords('55608700'), cep_to_coords('54460110'), cep_to_coords('52120470'), cep_to_coords('52130450'), cep_to_coords('55022350'), cep_to_coords('50070370'), cep_to_coords('54250211'), cep_to_coords('55111200'), cep_to_coords('56337600'), cep_to_coords('56503859'), cep_to_coords('55813430'), cep_to_coords('52111624'), cep_to_coords('51300441'), cep_to_coords('51240130'), cep_to_coords('50711240'), cep_to_coords('52111600'), cep_to_coords('55295260'), cep_to_coords('52291013'), cep_to_coords('54280532'), cep_to_coords('50790350'), cep_to_coords('56515230'), cep_to_coords('53620020'), cep_to_coords('55294804'), cep_to_coords('54230090'), cep_to_coords('54320020'), cep_to_coords('55291120'), cep_to_coords('55291625'), cep_to_coords('53020312'), cep_to_coords('50080040'), cep_to_coords('50630430'), cep_to_coords('54330657'), cep_to_coords('54330756'), cep_to_coords('54753470'), cep_to_coords('50080053'), cep_to_coords('55297120'), cep_to_coords('55294830'), cep_to_coords('55297810'), cep_to_coords('55293270'), cep_to_coords('55299270'), cep_to_coords('55296060'), cep_to_coords('50080680'), cep_to_coords('50790030'), cep_to_coords('55291460'), cep_to_coords('55306054'), cep_to_coords('52041360'), cep_to_coords('55292071'), cep_to_coords('50970360'), cep_to_coords('56512220'), cep_to_coords('54250250'), cep_to_coords('50900520'), cep_to_coords('50900550'), cep_to_coords('54315160'), cep_to_coords('53330220'), cep_to_coords('53050167'), cep_to_coords('56503675'), cep_to_coords('55042340'), cep_to_coords('50771010'), cep_to_coords('50110020'), cep_to_coords('54120420'), cep_to_coords('53435031'), cep_to_coords('50830130'), cep_to_coords('57062585'), cep_to_coords('55034195'), cep_to_coords('50040080'), cep_to_coords('54720320'), cep_to_coords('53435560'), cep_to_coords('50721060'), cep_to_coords('51330360'), cep_to_coords('56318010'), cep_to_coords('54762600'), cep_to_coords('54420004'), cep_to_coords('55812140'), cep_to_coords('55026241'), cep_to_coords('55016370'), cep_to_coords('50751190'), cep_to_coords('55020365'), cep_to_coords('53625020'), cep_to_coords('54510994'), cep_to_coords('53330010'), cep_to_coords('50721235'), cep_to_coords('53220050'), cep_to_coords('53060100'), cep_to_coords('50690570'), cep_to_coords('53422460'), cep_to_coords('53431460'), cep_to_coords('55294420'), cep_to_coords('53409400'), cep_to_coords('50060360'), cep_to_coords('53431380'), cep_to_coords('54340220'), cep_to_coords('54515290'), cep_to_coords('53413150'), cep_to_coords('50780100'), cep_to_coords('50900025'), cep_to_coords('50920832'), cep_to_coords('50630610'), cep_to_coords('54400230'), cep_to_coords('50650280'), cep_to_coords('53540720'), cep_to_coords('54120500'), cep_to_coords('54250221'), cep_to_coords('53300440'), cep_to_coords('53585142'), cep_to_coords('53190150'), cep_to_coords('53560150'), cep_to_coords('50680410'), cep_to_coords('54768500'), cep_to_coords('56312887'), cep_to_coords('53525712'), cep_to_coords('52280271'), cep_to_coords('55644120'), cep_to_coords('50080081'), cep_to_coords('55295153'), cep_to_coords('53640240'), cep_to_coords('50010050'), cep_to_coords('52031475'), cep_to_coords('54410311'), cep_to_coords('53585295'), cep_to_coords('53330530'), cep_to_coords('53011040'), cep_to_coords('53110111'), cep_to_coords('54753700'), cep_to_coords('54771700'), cep_to_coords('54753120'), cep_to_coords('54759350'), cep_to_coords('52070160'), cep_to_coords('53140820'), cep_to_coords('50820140'), cep_to_coords('53422070'), cep_to_coords('53416570'), cep_to_coords('55026610'), cep_to_coords('55030025'), cep_to_coords('53421340'), cep_to_coords('53060270'), cep_to_coords('50370170'), cep_to_coords('56320726'), cep_to_coords('56328970'), cep_to_coords('92200290'), cep_to_coords('50920550'), cep_to_coords('50030240'), cep_to_coords('56304500'), cep_to_coords('56907020'), cep_to_coords('54230130'), cep_to_coords('54340015'), cep_to_coords('55297799'), cep_to_coords('56909620'), cep_to_coords('55012490'), cep_to_coords('55034070'), cep_to_coords('50761080'), cep_to_coords('54777204'), cep_to_coords('50881040'), cep_to_coords('52091260'), cep_to_coords('53435700'), cep_to_coords('50910430'), cep_to_coords('53405180'), cep_to_coords('54150193'), cep_to_coords('54756125'), cep_to_coords('50870090'), cep_to_coords('56310666'), cep_to_coords('50790035'), cep_to_coords('51280240'), cep_to_coords('52191540'), cep_to_coords('52090110'), cep_to_coords('43253534'), cep_to_coords('54360465'), cep_to_coords('56070040'), cep_to_coords('54767455'), cep_to_coords('53360100'), cep_to_coords('55021260'), cep_to_coords('55020425'), cep_to_coords('50610370'), cep_to_coords('52020320'), cep_to_coords('54280263'), cep_to_coords('50600700'), cep_to_coords('53442060'), cep_to_coords('51330260'), cep_to_coords('51230193'), cep_to_coords('56512670'), cep_to_coords('54420201'), cep_to_coords('50730480'), cep_to_coords('55026205'), cep_to_coords('53415536'), cep_to_coords('50630000'), cep_to_coords('51230270'), cep_to_coords('51120183'), cep_to_coords('50741460'), cep_to_coords('50910395'), cep_to_coords('50721010'), cep_to_coords('51130130'), cep_to_coords('53439070'), cep_to_coords('06260100'), cep_to_coords('50790112'), cep_to_coords('55295490'), cep_to_coords('55293600'), cep_to_coords('55299400'), cep_to_coords('55298000'), cep_to_coords('55294040'), cep_to_coords('55296080'), cep_to_coords('55292490'), cep_to_coords('55292660'), cep_to_coords('55299630'), cep_to_coords('54210210'), cep_to_coords('55298670'), cep_to_coords('50822140'), cep_to_coords('52130240'), cep_to_coords('51220210'), cep_to_coords('53420416'), cep_to_coords('55641740'), cep_to_coords('55642128'), cep_to_coords('55296530'), cep_to_coords('64018018'), cep_to_coords('51022400'), cep_to_coords('23121212'), cep_to_coords('55028020'), cep_to_coords('55032240'), cep_to_coords('53370300'), cep_to_coords('53404255'), cep_to_coords('52490130'), cep_to_coords('56320710'), cep_to_coords('51350600'), cep_to_coords('55002971'), cep_to_coords('51290110'), cep_to_coords('51260020'), cep_to_coords('50731450'), cep_to_coords('51290212'), cep_to_coords('55008360'), cep_to_coords('54100170'), cep_to_coords('55018003'), cep_to_coords('50640360'), cep_to_coords('50620720'), cep_to_coords('60810090'), cep_to_coords('49035000'), cep_to_coords('54430035'), cep_to_coords('50800075'), cep_to_coords('52091080'), cep_to_coords('55014748'), cep_to_coords('50710410'), cep_to_coords('54505541'), cep_to_coords('55292350'), cep_to_coords('55014668'), cep_to_coords('52090680'), cep_to_coords('51345610'), cep_to_coords('51190300'), cep_to_coords('52020160'), cep_to_coords('54450210'), cep_to_coords('50830090'), cep_to_coords('52060370'), cep_to_coords('51002130'), cep_to_coords('50680285'), cep_to_coords('55030440'), cep_to_coords('54290055'), cep_to_coords('42342342'), cep_to_coords('53444040'), cep_to_coords('52291530'), cep_to_coords('52510530'), cep_to_coords('54450200'), cep_to_coords('50761560'), cep_to_coords('54765125'), cep_to_coords('53640290'), cep_to_coords('53640104'), cep_to_coords('53530380'), cep_to_coords('53635170'), cep_to_coords('53637555'), cep_to_coords('54520240'), cep_to_coords('54500992'), cep_to_coords('54340100'), cep_to_coords('54510170'), cep_to_coords('54518085'), cep_to_coords('53420110'), cep_to_coords('53435200'), cep_to_coords('54320410'), cep_to_coords('54290261'), cep_to_coords('54170201'), cep_to_coords('53010032'), cep_to_coords('50640640'), cep_to_coords('51240330'), cep_to_coords('54580498'), cep_to_coords('54753130'), cep_to_coords('54735782'), cep_to_coords('54762490'), cep_to_coords('50721340'), cep_to_coords('54774430'), cep_to_coords('54781300'), cep_to_coords('52071131'), cep_to_coords('50741510'), cep_to_coords('55195193'), cep_to_coords('56309440'), cep_to_coords('55610100'), cep_to_coords('50720330'), cep_to_coords('50875050'), cep_to_coords('54325210'), cep_to_coords('50980090'), cep_to_coords('52060235'), cep_to_coords('50810380'), cep_to_coords('53640280'), cep_to_coords('53030000'), cep_to_coords('54400220'), cep_to_coords('55038280'), cep_to_coords('50970030'), cep_to_coords('56328250'), cep_to_coords('50090785'), cep_to_coords('50010230'), cep_to_coords('54430040'), cep_to_coords('52120254'), cep_to_coords('54519100'), cep_to_coords('54766090'), cep_to_coords('56903320'), cep_to_coords('53220210'), cep_to_coords('51350060'), cep_to_coords('51011470'), cep_to_coords('53060320'), cep_to_coords('53220560'), cep_to_coords('53330600'), cep_to_coords('53300150'), cep_to_coords('51260580'), cep_to_coords('51480580'), cep_to_coords('52010060'), cep_to_coords('50820040'), cep_to_coords('53290130'), cep_to_coords('55606800'), cep_to_coords('53610181'), cep_to_coords('50790440'), cep_to_coords('52280370'), cep_to_coords('51340045'), cep_to_coords('53439240'), cep_to_coords('51150750'), cep_to_coords('48604160'), cep_to_coords('51240990'), cep_to_coords('51275210'), cep_to_coords('51203102'), cep_to_coords('51330060'), cep_to_coords('51240300'), cep_to_coords('56308090'), cep_to_coords('54160210'), cep_to_coords('51180210'), cep_to_coords('50910130'), cep_to_coords('50670630'), cep_to_coords('50641200'), cep_to_coords('56332615'), cep_to_coords('55614070'), cep_to_coords('51130230'), cep_to_coords('56328620'), cep_to_coords('50920000'), cep_to_coords('51300360'), cep_to_coords('51323329'), cep_to_coords('54220130'), cep_to_coords('50110130'), cep_to_coords('51190190'), cep_to_coords('55038650'), cep_to_coords('55010500'), cep_to_coords('55297040'), cep_to_coords('55295281'), cep_to_coords('55292010'), cep_to_coords('55297805'), cep_to_coords('50770340'), cep_to_coords('55298175'), cep_to_coords('55298300'), cep_to_coords('54230575'), cep_to_coords('53404440'), cep_to_coords('55295440'), cep_to_coords('52081290'), cep_to_coords('55034450'), cep_to_coords('55170800'), cep_to_coords('53443180'), cep_to_coords('50721370'), cep_to_coords('56509410'), cep_to_coords('56509750'), cep_to_coords('55030380'), cep_to_coords('56912321'), cep_to_coords('53010390'), cep_to_coords('55036750'), cep_to_coords('55028133'), cep_to_coords('52091170'), cep_to_coords('50870640'), cep_to_coords('53477100'), cep_to_coords('55020335'), cep_to_coords('50870580'), cep_to_coords('55021410'), cep_to_coords('50740410'), cep_to_coords('51280370'), cep_to_coords('56312000'), cep_to_coords('50910240'), cep_to_coords('55020610'), cep_to_coords('55020210'), cep_to_coords('56312261'), cep_to_coords('50771410'), cep_to_coords('53610620'), cep_to_coords('54712350'), cep_to_coords('52190080'), cep_to_coords('52111620'), cep_to_coords('50660360'), cep_to_coords('50660315'), cep_to_coords('54230200'), cep_to_coords('56320775'), cep_to_coords('54120070'), cep_to_coords('55014590'), cep_to_coords('55026902'), cep_to_coords('55026005'), cep_to_coords('50870340'), cep_to_coords('52110461'), cep_to_coords('50940180'), cep_to_coords('50040050'), cep_to_coords('52041970'), cep_to_coords('54140370'), cep_to_coords('55602170'), cep_to_coords('55006140'), cep_to_coords('51160230'), cep_to_coords('55155020'), cep_to_coords('54753695'), cep_to_coords('54753798'), cep_to_coords('54759430'), cep_to_coords('54762682'), cep_to_coords('55194348'), cep_to_coords('55190020'), cep_to_coords('55016260'), cep_to_coords('50640383'), cep_to_coords('53435740'), cep_to_coords('55028760'), cep_to_coords('56320570'), cep_to_coords('56909210'), cep_to_coords('56904110'), cep_to_coords('42334234'), cep_to_coords('50620370'), cep_to_coords('50791487'), cep_to_coords('50800330'), cep_to_coords('50860110'), cep_to_coords('54759170'), cep_to_coords('55036340'), cep_to_coords('52291070'), cep_to_coords('74768015'), cep_to_coords('50340200'), cep_to_coords('55610280'), cep_to_coords('50110340'), cep_to_coords('53180210'), cep_to_coords('56330060'), cep_to_coords('54290540'), cep_to_coords('52060540'), cep_to_coords('50740150'), cep_to_coords('56327070'), cep_to_coords('52031341'), cep_to_coords('56800330'), cep_to_coords('56509650'), cep_to_coords('56512340'), cep_to_coords('56503224'), cep_to_coords('51320510'), cep_to_coords('53260100'), cep_to_coords('55640091'), cep_to_coords('51100000'), cep_to_coords('55296050'), cep_to_coords('54210490'), cep_to_coords('50850200'), cep_to_coords('56302070'), cep_to_coords('51020350'), cep_to_coords('54150630'), cep_to_coords('54120713'), cep_to_coords('55816555'), cep_to_coords('55642520'), cep_to_coords('50610190'), cep_to_coords('52170240'), cep_to_coords('54520250'), cep_to_coords('54460360'), cep_to_coords('52160301'), cep_to_coords('54535000'), cep_to_coords('54759460'), cep_to_coords('54759503'), cep_to_coords('51270681'), cep_to_coords('50790080'), cep_to_coords('54789355'), cep_to_coords('56320320'), cep_to_coords('55606140'), cep_to_coords('55195638'), cep_to_coords('56331020'), cep_to_coords('55195001'), cep_to_coords('56309500'), cep_to_coords('54430420'), cep_to_coords('51335040'), cep_to_coords('51340255'), cep_to_coords('54220050'), cep_to_coords('56912420'), cep_to_coords('56906141'), cep_to_coords('53530665'), cep_to_coords('53220460'), cep_to_coords('53435150'), cep_to_coords('53416660'), cep_to_coords('53270265'), cep_to_coords('50710395'), cep_to_coords('54220215'), cep_to_coords('53330450'), cep_to_coords('54789375'), cep_to_coords('55914642'), cep_to_coords('52280575'), cep_to_coords('50790250'), cep_to_coords('50610631'), cep_to_coords('50721410'), cep_to_coords('50711080'), cep_to_coords('26583660'), cep_to_coords('53200037'), cep_to_coords('54510110'), cep_to_coords('55294836'), cep_to_coords('52130026'), cep_to_coords('50781111'), cep_to_coords('51350340'), cep_to_coords('53150045'), cep_to_coords('05450000'), cep_to_coords('53409050'), cep_to_coords('54160320'), cep_to_coords('53170451'), cep_to_coords('54080430'), cep_to_coords('50050090'), cep_to_coords('54530090'), cep_to_coords('54535290'), cep_to_coords('55291490'), cep_to_coords('50810280'), cep_to_coords('55002300'), cep_to_coords('55014370'), cep_to_coords('50730190'), cep_to_coords('53550040'), cep_to_coords('53423470'), cep_to_coords('53060505'), cep_to_coords('53009000'), cep_to_coords('52081250'), cep_to_coords('53330060'), cep_to_coords('54765320'), cep_to_coords('51200200'), cep_to_coords('51345260'), cep_to_coords('50791182'), cep_to_coords('50791461'), cep_to_coords('52121435'), cep_to_coords('50690530'), cep_to_coords('52170370'), cep_to_coords('96213002'), cep_to_coords('54762750'), cep_to_coords('54220260'), cep_to_coords('56320806'), cep_to_coords('55614080'), cep_to_coords('55192614'), cep_to_coords('53425615'), cep_to_coords('52721775'), cep_to_coords('52280373'), cep_to_coords('51330180'), cep_to_coords('50630330'), cep_to_coords('58753080'), cep_to_coords('50721275'), cep_to_coords('50910410'), cep_to_coords('50910400'), cep_to_coords('54735330'), cep_to_coords('51240215'), cep_to_coords('54753580'), cep_to_coords('54753583'), cep_to_coords('52191555'), cep_to_coords('50780200'), cep_to_coords('50761170'), cep_to_coords('53413650'), cep_to_coords('52132103'), cep_to_coords('50731220'), cep_to_coords('50920838'), cep_to_coords('50920828'), cep_to_coords('54080392'), cep_to_coords('54100080'), cep_to_coords('50721270'), cep_to_coords('50790220'), cep_to_coords('50690670'), cep_to_coords('50830590'), cep_to_coords('54150560'), cep_to_coords('50760020'), cep_to_coords('53416020'), cep_to_coords('56317250'), cep_to_coords('54300425'), cep_to_coords('54350680'), cep_to_coords('56912324'), cep_to_coords('54765236'), cep_to_coords('54325120'), cep_to_coords('54505971'), cep_to_coords('53060090'), cep_to_coords('51250320'), cep_to_coords('55866000'), cep_to_coords('54762843'), cep_to_coords('55018220'), cep_to_coords('51170160'), cep_to_coords('54580465'), cep_to_coords('53180315'), cep_to_coords('52081320'), cep_to_coords('54768350'), cep_to_coords('54510340'), cep_to_coords('54720060'), cep_to_coords('54580140'), cep_to_coords('55606593'), cep_to_coords('55606230'), cep_to_coords('56330270'), cep_to_coords('56312811'), cep_to_coords('54777100'), cep_to_coords('52052130'), cep_to_coords('50680340'), cep_to_coords('54759550'), cep_to_coords('53437550'), cep_to_coords('50110740'), cep_to_coords('54420370'), cep_to_coords('57045265'), cep_to_coords('56304000'), cep_to_coords('52211240'), cep_to_coords('53530446'), cep_to_coords('52090725'), cep_to_coords('50060250'), cep_to_coords('50750360'), cep_to_coords('54705300'), cep_to_coords('56314455'), cep_to_coords('50930040'), cep_to_coords('53140330'), cep_to_coords('54340630'), cep_to_coords('51011038'), cep_to_coords('54400190'), cep_to_coords('54783990'), cep_to_coords('52160075'), cep_to_coords('51345170'), cep_to_coords('51350550'), cep_to_coords('56503146'), cep_to_coords('50790901'), cep_to_coords('50850321'), cep_to_coords('56515320'), cep_to_coords('53250250'), cep_to_coords('52091306'), cep_to_coords('56312561'), cep_to_coords('53403480'), cep_to_coords('53300390'), cep_to_coords('53806700'), cep_to_coords('53341090'), cep_to_coords('53436460'), cep_to_coords('53110630'), cep_to_coords('55642558'), cep_to_coords('52280250'), cep_to_coords('51130110'), cep_to_coords('53370158'), cep_to_coords('52130227'), cep_to_coords('53540220'), cep_to_coords('53550045'), cep_to_coords('54360109'), cep_to_coords('52060323'), cep_to_coords('54400600'), cep_to_coords('52121045'), cep_to_coords('50720430'), cep_to_coords('52190320'), cep_to_coords('50620131'), cep_to_coords('50640020'), cep_to_coords('50060310'), cep_to_coords('53240491'), cep_to_coords('54756356'), cep_to_coords('54768460'), cep_to_coords('54320626'), cep_to_coords('54774030'), cep_to_coords('53429130'), cep_to_coords('50690730'), cep_to_coords('56465666'), cep_to_coords('53429680'), cep_to_coords('50690222'), cep_to_coords('56313010'), cep_to_coords('50781780'), cep_to_coords('51340380'), cep_to_coords('50830420'), cep_to_coords('54360121'), cep_to_coords('51030150'), cep_to_coords('52060320'), cep_to_coords('50630209'), cep_to_coords('54330705'), cep_to_coords('52130380'), cep_to_coords('52090070'), cep_to_coords('54110240'), cep_to_coords('55293290'), cep_to_coords('54430190'), cep_to_coords('52031125'), cep_to_coords('50761430'), cep_to_coords('56302440'), cep_to_coords('54310130'), cep_to_coords('52210180'), cep_to_coords('55192566'), cep_to_coords('55190404'), cep_to_coords('55020090'), cep_to_coords('55036567'), cep_to_coords('51345220'), cep_to_coords('51270570'), cep_to_coords('55030140'), cep_to_coords('55020215'), cep_to_coords('51190580'), cep_to_coords('55028010'), cep_to_coords('58985000'), cep_to_coords('50751130'), cep_to_coords('52130241'), cep_to_coords('52110340'), cep_to_coords('56302170'), cep_to_coords('56312225'), cep_to_coords('54310301'), cep_to_coords('56312035'), cep_to_coords('56912410'), cep_to_coords('53370265'), cep_to_coords('32040300'), cep_to_coords('53402786'), cep_to_coords('52211033'), cep_to_coords('55195003'), cep_to_coords('52291020'), cep_to_coords('52060230'), cep_to_coords('52280610'), cep_to_coords('50920151'), cep_to_coords('56312075'), cep_to_coords('53250000'), cep_to_coords('52150340'), cep_to_coords('50790530'), cep_to_coords('50912309'), cep_to_coords('54768775'), cep_to_coords('51260670'), cep_to_coords('55030060'), cep_to_coords('54330080'), cep_to_coords('50820560'), cep_to_coords('50791235'), cep_to_coords('50870150'), cep_to_coords('50870120'), cep_to_coords('50910020'), cep_to_coords('53437810'), cep_to_coords('51335350'), cep_to_coords('54580175'), cep_to_coords('53110080'), cep_to_coords('56302460'), cep_to_coords('56312435'), cep_to_coords('56328752'), cep_to_coords('55606490'), cep_to_coords('50620120'), cep_to_coords('55602530'), cep_to_coords('55608280'), cep_to_coords('55614035'), cep_to_coords('55608560'), cep_to_coords('55298655'), cep_to_coords('55292315'), cep_to_coords('55292070'), cep_to_coords('55292319'), cep_to_coords('55292317'), cep_to_coords('52020130'), cep_to_coords('55296390'), cep_to_coords('55292000'), cep_to_coords('55293080'), cep_to_coords('55296670'), cep_to_coords('55298651'), cep_to_coords('55294530'), cep_to_coords('53120101'), cep_to_coords('53040085'), cep_to_coords('55295903'), cep_to_coords('55294600'), cep_to_coords('55293530'), cep_to_coords('55292405'), cep_to_coords('55296190'), cep_to_coords('55860970'), cep_to_coords('50790111'), cep_to_coords('55299378'), cep_to_coords('56328400'), cep_to_coords('56506040'), cep_to_coords('56512285'), cep_to_coords('56510060'), cep_to_coords('53443740'), cep_to_coords('62900000'), cep_to_coords('55032220'), cep_to_coords('50760615'), cep_to_coords('55016470'), cep_to_coords('52211280'), cep_to_coords('50690280'), cep_to_coords('54420226'), cep_to_coords('52280070'), cep_to_coords('51150272'), cep_to_coords('52120021'), cep_to_coords('52051070'), cep_to_coords('52050071'), cep_to_coords('50730540'), cep_to_coords('54240260'), cep_to_coords('55010420'), cep_to_coords('56909478'), cep_to_coords('55018060'), cep_to_coords('53350055'), cep_to_coords('50781350'), cep_to_coords('55022250'), cep_to_coords('55195839'), cep_to_coords('55190865'), cep_to_coords('56332590'), cep_to_coords('54100100'), cep_to_coords('53540250'), cep_to_coords('51190570'), cep_to_coords('51190485'), cep_to_coords('55014635'), cep_to_coords('55006465'), cep_to_coords('55032520'), cep_to_coords('53625405'), cep_to_coords('50761790'), cep_to_coords('50760490'), cep_to_coords('50830500'), cep_to_coords('52020901'), cep_to_coords('50760007'), cep_to_coords('54325660'), cep_to_coords('55014280'), cep_to_coords('55014580'), cep_to_coords('50731125'), cep_to_coords('50080620'), cep_to_coords('50720395'), cep_to_coords('54705060'), cep_to_coords('50050095'), cep_to_coords('50781500'), cep_to_coords('52131120'), cep_to_coords('53060360'), cep_to_coords('56330320'), cep_to_coords('50771815'), cep_to_coords('55038750'), cep_to_coords('55545000'), cep_to_coords('54723095'), cep_to_coords('54580210'), cep_to_coords('52130382'), cep_to_coords('56509190'), cep_to_coords('52165170'), cep_to_coords('50800150'), cep_to_coords('53421700'), cep_to_coords('53080720'), cep_to_coords('53090020'), cep_to_coords('51011635'), cep_to_coords('51011160'), cep_to_coords('55024020'), cep_to_coords('55813700'), cep_to_coords('56813320'), cep_to_coords('50040030'), cep_to_coords('55038020'), cep_to_coords('51290290'), cep_to_coords('52390130'), cep_to_coords('53060780'), cep_to_coords('55292059'), cep_to_coords('50690740'), cep_to_coords('53435060'), cep_to_coords('52071081'), cep_to_coords('52071085'), cep_to_coords('51030760'), cep_to_coords('52050290'), cep_to_coords('56514035'), cep_to_coords('52071332'), cep_to_coords('13454475'), cep_to_coords('53640655'), cep_to_coords('51330530'), cep_to_coords('51340235'), cep_to_coords('53220350'), cep_to_coords('53350130'), cep_to_coords('56909630'), cep_to_coords('55195039'), cep_to_coords('52070170'), cep_to_coords('54768652'), cep_to_coords('55612281'), cep_to_coords('55608621'), cep_to_coords('55006220'), cep_to_coords('53110180'), cep_to_coords('54330571'), cep_to_coords('54765150'), cep_to_coords('54786180'), cep_to_coords('54762798'), cep_to_coords('56331170'), cep_to_coords('55813220'), cep_to_coords('50810300'), cep_to_coords('54767640'), cep_to_coords('55816490'), cep_to_coords('55819910'), cep_to_coords('51340170'), cep_to_coords('02964030'), cep_to_coords('55685000'), cep_to_coords('53431570'), cep_to_coords('53403540'), cep_to_coords('50110175'), cep_to_coords('55012250'), cep_to_coords('52061490'), cep_to_coords('53350340'), cep_to_coords('52291251'), cep_to_coords('55642260'), cep_to_coords('55641798'), cep_to_coords('52280060'), cep_to_coords('55644355'), cep_to_coords('55642090'), cep_to_coords('55644360'), cep_to_coords('55644161'), cep_to_coords('55022130'), cep_to_coords('55022700'), cep_to_coords('55193524'), cep_to_coords('50031750'), cep_to_coords('52051382'), cep_to_coords('54430510'), cep_to_coords('53010000'), cep_to_coords('53070060'), cep_to_coords('56903010'), cep_to_coords('56906255'), cep_to_coords('56909093'), cep_to_coords('52130010'), cep_to_coords('52031020'), cep_to_coords('54100605'), cep_to_coords('53160450'), cep_to_coords('53110230'), cep_to_coords('54370020'), cep_to_coords('50720200'), cep_to_coords('53160098'), cep_to_coords('53160130'), cep_to_coords('50790300'), cep_to_coords('55038125'), cep_to_coords('42343242'), cep_to_coords('52130177'), cep_to_coords('50940260'), cep_to_coords('51110130'), cep_to_coords('52280350'), cep_to_coords('50790060'), cep_to_coords('54325297'), cep_to_coords('51030670'), cep_to_coords('50970165'), cep_to_coords('53170450'), cep_to_coords('53493380'), cep_to_coords('50670080'), cep_to_coords('50970160'), cep_to_coords('53230040'), cep_to_coords('50760110'), cep_to_coords('51280230'), cep_to_coords('50820230'), cep_to_coords('50760465'), cep_to_coords('53270225'), cep_to_coords('54230580'), cep_to_coords('54786560'), cep_to_coords('50781720'), cep_to_coords('51250260'), cep_to_coords('51320180'), cep_to_coords('55292320'), cep_to_coords('55294690'), cep_to_coords('55296270'), cep_to_coords('55302990'), cep_to_coords('55295170'), cep_to_coords('55299310'), cep_to_coords('55291260'), cep_to_coords('55295550'), cep_to_coords('55296487'), cep_to_coords('54270215'), cep_to_coords('50900130'), cep_to_coords('53250260'), cep_to_coords('55155140'), cep_to_coords('55150510'), cep_to_coords('51340135'), cep_to_coords('54768745'), cep_to_coords('50768745'), cep_to_coords('53645071'), cep_to_coords('55602400'), cep_to_coords('53530394'), cep_to_coords('55594900'), cep_to_coords('54515110'), cep_to_coords('50710480'), cep_to_coords('53441010'), cep_to_coords('53270655'), cep_to_coords('53417230'), cep_to_coords('55294282'), cep_to_coords('53635195'), cep_to_coords('52140350'), cep_to_coords('51170310'), cep_to_coords('53330050'), cep_to_coords('56503250'), cep_to_coords('55250999'), cep_to_coords('50910575'), cep_to_coords('56503180'), cep_to_coords('52090040'), cep_to_coords('55019030'), cep_to_coords('54325245'), cep_to_coords('53407020'), cep_to_coords('56328140'), cep_to_coords('55297370'), cep_to_coords('55028395'), cep_to_coords('56310787'), cep_to_coords('54220510'), cep_to_coords('52041560'), cep_to_coords('56312125'), cep_to_coords('50730550'), cep_to_coords('53439490'), cep_to_coords('50761401'), cep_to_coords('54737140'), cep_to_coords('55031110'), cep_to_coords('53070610'), cep_to_coords('56319590'), cep_to_coords('54530025'), cep_to_coords('54517280'), cep_to_coords('50090260'), cep_to_coords('56332034'), cep_to_coords('55027130'), cep_to_coords('54325440'), cep_to_coords('56320080'), cep_to_coords('50860900'), cep_to_coords('51150620'), cep_to_coords('50830575'), cep_to_coords('54777230'), cep_to_coords('55020154'), cep_to_coords('51415048'), cep_to_coords('55024210'), cep_to_coords('55002002'), cep_to_coords('55022320'), cep_to_coords('51290340'), cep_to_coords('58000000'), cep_to_coords('52061320'), cep_to_coords('55018795'), cep_to_coords('51250460'), cep_to_coords('51335420'), cep_to_coords('50630410'), cep_to_coords('53441000'), cep_to_coords('56328320'), cep_to_coords('55020745'), cep_to_coords('53250310'), cep_to_coords('55152130'), cep_to_coords('55040250'), cep_to_coords('53610340'), cep_to_coords('53635055'), cep_to_coords('50731200'), cep_to_coords('54762785'), cep_to_coords('50960480'), cep_to_coords('54580240'), cep_to_coords('58052285'), cep_to_coords('50730150'), cep_to_coords('50090010'), cep_to_coords('05781270'), cep_to_coords('53320401'), cep_to_coords('54250620'), cep_to_coords('52011000'), cep_to_coords('55010080'), cep_to_coords('51180200'), cep_to_coords('50060400'), cep_to_coords('50751570'), cep_to_coords('54315183'), cep_to_coords('56300175'), cep_to_coords('51200150'), cep_to_coords('53560000'), cep_to_coords('56515780'), cep_to_coords('55192630'), cep_to_coords('52080180'), cep_to_coords('54715505'), cep_to_coords('55192620'), cep_to_coords('55028577'), cep_to_coords('54160500'), cep_to_coords('55643210'), cep_to_coords('04218000'), cep_to_coords('55641784'), cep_to_coords('51110025'), cep_to_coords('52211510'), cep_to_coords('52040091'), cep_to_coords('53250130'), cep_to_coords('54325338'), cep_to_coords('54090480'), cep_to_coords('54100740'), cep_to_coords('52111500'), cep_to_coords('50670090'), cep_to_coords('50660090'), cep_to_coords('50050480'), cep_to_coords('54759085'), cep_to_coords('50910160'), cep_to_coords('55608450'), cep_to_coords('48903115'), cep_to_coords('56555000'), cep_to_coords('52090052'), cep_to_coords('50760670'), cep_to_coords('53040200'), cep_to_coords('50810603'), cep_to_coords('54270751'), cep_to_coords('54100510'), cep_to_coords('55644204'), cep_to_coords('52041395'), cep_to_coords('54737050'), cep_to_coords('54774190'), cep_to_coords('50060020'), cep_to_coords('50630630'), cep_to_coords('50640670'), cep_to_coords('55010270'), cep_to_coords('56308080'), cep_to_coords('56175000'), cep_to_coords('56310130'), cep_to_coords('50920430'), cep_to_coords('53540680'), cep_to_coords('50760340'), cep_to_coords('51170220'), cep_to_coords('55291040'), cep_to_coords('55292785'), cep_to_coords('55292445'), cep_to_coords('55291603'), cep_to_coords('55293240'), cep_to_coords('55293246'), cep_to_coords('54737555'), cep_to_coords('56312101'), cep_to_coords('55158510'), cep_to_coords('55157060'), cep_to_coords('54753530'), cep_to_coords('54723105'), cep_to_coords('29154465'), cep_to_coords('55155531'), cep_to_coords('55153005'), cep_to_coords('56503625'), cep_to_coords('51800006'), cep_to_coords('50740190'), cep_to_coords('50670280'), cep_to_coords('54490058'), cep_to_coords('53401630'), cep_to_coords('51345200'), cep_to_coords('53200640'), cep_to_coords('56503615'), cep_to_coords('56506420'), cep_to_coords('51011030'), cep_to_coords('52081220'), cep_to_coords('50050080'), cep_to_coords('53260184'), cep_to_coords('56317180'), cep_to_coords('53421291'), cep_to_coords('50100200'), cep_to_coords('10050280'), cep_to_coords('54325243'), cep_to_coords('51170350'), cep_to_coords('56320390'), cep_to_coords('58520000'), cep_to_coords('52012460'), cep_to_coords('56515150'), cep_to_coords('53421770'), cep_to_coords('52120094'), cep_to_coords('61030320'), cep_to_coords('50920150'), cep_to_coords('50940540'), cep_to_coords('53404310'), cep_to_coords('50100340'), cep_to_coords('50920620'), cep_to_coords('50771060'), cep_to_coords('50090340'), cep_to_coords('50660210'), cep_to_coords('56320670'), cep_to_coords('51160020'), cep_to_coords('56320370'), cep_to_coords('55038450'), cep_to_coords('55016460'), cep_to_coords('50640100'), cep_to_coords('50760470'), cep_to_coords('50711135'), cep_to_coords('50760565'), cep_to_coords('55642825'), cep_to_coords('55099899'), cep_to_coords('53170075'), cep_to_coords('53429090'), cep_to_coords('56328875'), cep_to_coords('52280700'), cep_to_coords('55641600'), cep_to_coords('53300240'), cep_to_coords('51275330'), cep_to_coords('53223402'), cep_to_coords('50875190'), cep_to_coords('56312065'), cep_to_coords('50110110'), cep_to_coords('52040120'), cep_to_coords('56508070'), cep_to_coords('52260160'), cep_to_coords('55644250'), cep_to_coords('51290450'), cep_to_coords('55010570'), cep_to_coords('54430293'), cep_to_coords('55018510'), cep_to_coords('53439110'), cep_to_coords('54290097'), cep_to_coords('52280000'), cep_to_coords('52150240'), cep_to_coords('50751410'), cep_to_coords('53580141'), cep_to_coords('54735430'), cep_to_coords('53210030'), cep_to_coords('56312270'), cep_to_coords('52090220'), cep_to_coords('50870010'), cep_to_coords('52120032'), cep_to_coords('53402830'), cep_to_coords('54220670'), cep_to_coords('50430910'), cep_to_coords('50710260'), cep_to_coords('51350360'), cep_to_coords('56318470'), cep_to_coords('56308030'), cep_to_coords('56312340'), cep_to_coords('55018420'), cep_to_coords('53570145'), cep_to_coords('56320050'), cep_to_coords('56328330'), cep_to_coords('50050055'), cep_to_coords('54765330'), cep_to_coords('54771070'), cep_to_coords('54767160'), cep_to_coords('56306140'), cep_to_coords('54786990'), cep_to_coords('55645210'), cep_to_coords('51240225'), cep_to_coords('56516120'), cep_to_coords('55002160'), cep_to_coords('55295420'), cep_to_coords('54517040'), cep_to_coords('52191085'), cep_to_coords('56330770'), cep_to_coords('55190048'), cep_to_coords('56312395'), cep_to_coords('56312230'), cep_to_coords('56331120'), cep_to_coords('54589285'), cep_to_coords('50770230'), cep_to_coords('53437770'), cep_to_coords('52221110'), cep_to_coords('54520030'), cep_to_coords('55040145'), cep_to_coords('53110170'), cep_to_coords('53620530'), cep_to_coords('53210062'), cep_to_coords('53221062'), cep_to_coords('55610170'), cep_to_coords('50770690'), cep_to_coords('54430150'), cep_to_coords('54750001'), cep_to_coords('53433610'), cep_to_coords('56330480'), cep_to_coords('55010160'), cep_to_coords('56309410'), cep_to_coords('54520220'), cep_to_coords('52041330'), cep_to_coords('54762710'), cep_to_coords('55290291'), cep_to_coords('55018480'), cep_to_coords('55014070'), cep_to_coords('55040465'), cep_to_coords('55299526'), cep_to_coords('55297440'), cep_to_coords('55295220'), cep_to_coords('55294510'), cep_to_coords('55298480'), cep_to_coords('55291310'), cep_to_coords('55297590'), cep_to_coords('55298145'), cep_to_coords('51021774'), cep_to_coords('55292060'), cep_to_coords('55299530'), cep_to_coords('55098095'), cep_to_coords('14815000'), cep_to_coords('55299544'), cep_to_coords('55296470'), cep_to_coords('53421181'), cep_to_coords('53405636'), cep_to_coords('55292595'), cep_to_coords('55030000'), cep_to_coords('55018655'), cep_to_coords('52061312'), cep_to_coords('55643530'), cep_to_coords('50650440'), cep_to_coords('55644669'), cep_to_coords('55644300'), cep_to_coords('55644000'), cep_to_coords('55641050'), cep_to_coords('55038140'), cep_to_coords('53180090'), cep_to_coords('52130360'), cep_to_coords('52211220'), cep_to_coords('50010970'), cep_to_coords('55285000'), cep_to_coords('55032370'), cep_to_coords('05675000'), cep_to_coords('53210800'), cep_to_coords('54759020'), cep_to_coords('50791090'), cep_to_coords('56512080'), cep_to_coords('53525711'), cep_to_coords('50721550'), cep_to_coords('54749990'), cep_to_coords('56512190'), cep_to_coords('53050181'), cep_to_coords('54100560'), cep_to_coords('50780700'), cep_to_coords('54735210'), cep_to_coords('56510030'), cep_to_coords('54410570'), cep_to_coords('55011755'), cep_to_coords('53150660'), cep_to_coords('53130680'), cep_to_coords('53404525'), cep_to_coords('50100100'), cep_to_coords('53409490'), cep_to_coords('53409690'), cep_to_coords('51320340'), cep_to_coords('52031290'), cep_to_coords('52090375'), cep_to_coords('50680120'), cep_to_coords('52010190'), cep_to_coords('54759310'), cep_to_coords('50056902'), cep_to_coords('53645300'), cep_to_coords('53620745'), cep_to_coords('53190740'), cep_to_coords('54330485'), cep_to_coords('54260380'), cep_to_coords('55024725'), cep_to_coords('55014131'), cep_to_coords('55020360'), cep_to_coords('53020071'), cep_to_coords('53350150'), cep_to_coords('53510020'), cep_to_coords('50760518'), cep_to_coords('52070511'), cep_to_coords('56332090'), cep_to_coords('56320380'), cep_to_coords('52090331'), cep_to_coords('50500500'), cep_to_coords('53640155'), cep_to_coords('52011120'), cep_to_coords('53585770'), cep_to_coords('51052230'), cep_to_coords('50751125'), cep_to_coords('52061002'), cep_to_coords('53416572'), cep_to_coords('53510000'), cep_to_coords('53330161'), cep_to_coords('52211630'), cep_to_coords('50760001'), cep_to_coords('50076002'), cep_to_coords('55150030'), cep_to_coords('63010970'), cep_to_coords('54260003'), cep_to_coords('50060100'), cep_to_coords('50730090'), cep_to_coords('50100370'), cep_to_coords('51330290'), cep_to_coords('51190480'), cep_to_coords('54765455'), cep_to_coords('53160330'), cep_to_coords('54777470'), cep_to_coords('52070150'), cep_to_coords('53411011'), cep_to_coords('50800070'), cep_to_coords('54170020'), cep_to_coords('56909110'), cep_to_coords('54315100'), cep_to_coords('55130970'), cep_to_coords('51021904'), cep_to_coords('55030350'), cep_to_coords('54786190'), cep_to_coords('54762327'), cep_to_coords('54774080'), cep_to_coords('54777180'), cep_to_coords('52130375'), cep_to_coords('55030100'), cep_to_coords('55016081'), cep_to_coords('56509260'), cep_to_coords('54380154'), cep_to_coords('53530755'), cep_to_coords('56328470'), cep_to_coords('54510420'), cep_to_coords('52190050'), cep_to_coords('54160270'), cep_to_coords('56906537'), cep_to_coords('56909486'), cep_to_coords('54580265'), cep_to_coords('55034380'), cep_to_coords('55034400'), cep_to_coords('55602330'), cep_to_coords('53230270'), cep_to_coords('55038230'), cep_to_coords('51021250'), cep_to_coords('54210090'), cep_to_coords('56304421'), cep_to_coords('53403251'), cep_to_coords('53210310'), cep_to_coords('56330620'), cep_to_coords('55028333'), cep_to_coords('55042030'), cep_to_coords('55004081'), cep_to_coords('55006285'), cep_to_coords('55036151'), cep_to_coords('05568000'), cep_to_coords('55028290'), cep_to_coords('55018640'), cep_to_coords('55027000'), cep_to_coords('55012080'), cep_to_coords('55020445'), cep_to_coords('55022170'), cep_to_coords('55004240'), cep_to_coords('50780645'), cep_to_coords('55642338'), cep_to_coords('55641320'), cep_to_coords('55641490'), cep_to_coords('55640992'), cep_to_coords('55641408'), cep_to_coords('55641665'), cep_to_coords('55643470'), cep_to_coords('55642220'), cep_to_coords('55643290'), cep_to_coords('56320630'), cep_to_coords('56322740'), cep_to_coords('52121560'), cep_to_coords('55008480'), cep_to_coords('55044030'), cep_to_coords('55018061'), cep_to_coords('55018020'), cep_to_coords('55018131'), cep_to_coords('55026340'), cep_to_coords('50800230'), cep_to_coords('53190010'), cep_to_coords('52280535'), cep_to_coords('54280585'), cep_to_coords('50810340'), cep_to_coords('53190110'), cep_to_coords('56330470'), cep_to_coords('53441380'), cep_to_coords('56302290'), cep_to_coords('69980000'), cep_to_coords('56555555'), cep_to_coords('09940170'), cep_to_coords('50865135'), cep_to_coords('54350600'), cep_to_coords('15600000'), cep_to_coords('50050160'), cep_to_coords('53270380'), cep_to_coords('54580565'), cep_to_coords('56313750'), cep_to_coords('50741272'), cep_to_coords('50930090'), cep_to_coords('55291220'), cep_to_coords('55291707'), cep_to_coords('55293300'), cep_to_coords('55299588'), cep_to_coords('55291240'), cep_to_coords('55292100'), cep_to_coords('50005000'), cep_to_coords('55291410'), cep_to_coords('50730100'), cep_to_coords('54730410'), cep_to_coords('50040440'), cep_to_coords('55012270'), cep_to_coords('50771140'), cep_to_coords('56505065'), cep_to_coords('51011041'), cep_to_coords('51011570'), cep_to_coords('54400250'), cep_to_coords('50760003')


# In[19]:


print(coordenadasrow5426to10425)


# In[20]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in row5426to10425.tolist():
    result.append(''.join(pattern.findall(item)))


# In[21]:


print(result)


# In[22]:


dfrow5426to10425 = pd.DataFrame(coordenadasrow5426to10425, result)


# In[23]:


dfrow5426to10425 


# In[24]:


dfrow5426to10425.reset_index(level=0, inplace=True)


# In[25]:


dfrow5426to10425


# In[27]:


dfrow5426to10425 = dfrow5426to10425.rename(columns={'index':'cep'}) 


# In[28]:


dfrow5426to10425


# In[ ]:


#dfrow5426to10425.reset_index(level=0, inplace=True)


# In[29]:


bancoesusalltabsrais2019nodupsCEPS[['id']][5426:10426]


# In[30]:


id5426_10425 = bancoesusalltabsrais2019nodupsCEPS[['id']][5426:10426]


# In[31]:


id5426_10425


# In[32]:


id5426_10425.reset_index(level=0, inplace=True)


# In[33]:


id5426_10425


# In[34]:


dfrow5426to10425['id'] = id5426_10425['id']
dfrow5426to10425['index'] = id5426_10425['index']


# In[35]:


dfrow5426to10425


# In[36]:


dfrow5426to10425[dfrow5426to10425.columns[[4,3,0,1,2]]]


# In[37]:


dfrow5426to10425 = dfrow5426to10425[dfrow5426to10425.columns[[4,3,0,1,2]]]


# In[38]:


dfrow5426to10425


# In[39]:


dfrow5426to10425.to_excel('dfrow5426to10425latlong.xlsx')


# # bancoesusalltabsrais2019nodupsCEPS[10426:15426]

# In[40]:


bancoesusalltabsrais2019nodupsCEPS[10426:15426]


# In[41]:


row10426to15425 = bancoesusalltabsrais2019nodupsCEPS[10426:15426]


# In[42]:


row10426to15425 


# In[43]:


row10426to15425.update("cep_to_coords('" + row10426to15425[['cep']].astype(str) + "'),")
print(row10426to15425)


# In[44]:


row10426to15425 = row10426to15425.loc[:,'cep']


# In[45]:


print(' '.join(row10426to15425))


# In[46]:


coordenadasrow10426to15425 = cep_to_coords('53210360'), cep_to_coords('55604125'), cep_to_coords('54735570'), cep_to_coords('53409450'), cep_to_coords('56512010'), cep_to_coords('55150170'), cep_to_coords('55154515'), cep_to_coords('56509612'), cep_to_coords('56509838'), cep_to_coords('56503390'), cep_to_coords('51260350'), cep_to_coords('55040060'), cep_to_coords('52071370'), cep_to_coords('52071321'), cep_to_coords('56328090'), cep_to_coords('54170700'), cep_to_coords('54100141'), cep_to_coords('51170460'), cep_to_coords('50751415'), cep_to_coords('50760440'), cep_to_coords('52171151'), cep_to_coords('53565320'), cep_to_coords('56512320'), cep_to_coords('55291547'), cep_to_coords('53421392'), cep_to_coords('55022370'), cep_to_coords('54737070'), cep_to_coords('58055020'), cep_to_coords('56270000'), cep_to_coords('52117230'), cep_to_coords('50770320'), cep_to_coords('52040081'), cep_to_coords('51031021'), cep_to_coords('50870690'), cep_to_coords('54753300'), cep_to_coords('54753180'), cep_to_coords('54774642'), cep_to_coords('54220348'), cep_to_coords('50980480'), cep_to_coords('51021050'), cep_to_coords('54360011'), cep_to_coords('56319655'), cep_to_coords('55030600'), cep_to_coords('56302400'), cep_to_coords('50910190'), cep_to_coords('53433170'), cep_to_coords('56511150'), cep_to_coords('52210220'), cep_to_coords('55008390'), cep_to_coords('53020299'), cep_to_coords('54340035'), cep_to_coords('53441420'), cep_to_coords('50761703'), cep_to_coords('55016002'), cep_to_coords('55027180'), cep_to_coords('50771600'), cep_to_coords('50900660'), cep_to_coords('50810461'), cep_to_coords('50680060'), cep_to_coords('52060500'), cep_to_coords('50790145'), cep_to_coords('56504045'), cep_to_coords('51011660'), cep_to_coords('52221130'), cep_to_coords('51200040'), cep_to_coords('50690550'), cep_to_coords('54100495'), cep_to_coords('53150440'), cep_to_coords('52070540'), cep_to_coords('53402011'), cep_to_coords('55819020'), cep_to_coords('51240450'), cep_to_coords('54767080'), cep_to_coords('54325763'), cep_to_coords('53130130'), cep_to_coords('54735112'), cep_to_coords('54160272'), cep_to_coords('53570080'), cep_to_coords('51350391'), cep_to_coords('51030100'), cep_to_coords('52081700'), cep_to_coords('50564624'), cep_to_coords('55028200'), cep_to_coords('54517125'), cep_to_coords('54515450'), cep_to_coords('55604370'), cep_to_coords('55006010'), cep_to_coords('55022230'), cep_to_coords('55612136'), cep_to_coords('55004030'), cep_to_coords('51350460'), cep_to_coords('55194405'), cep_to_coords('55022440'), cep_to_coords('56506590'), cep_to_coords('56308040'), cep_to_coords('53010120'), cep_to_coords('56909168'), cep_to_coords('55190836'), cep_to_coords('56320600'), cep_to_coords('55020040'), cep_to_coords('52080097'), cep_to_coords('53220381'), cep_to_coords('52228073'), cep_to_coords('52435000'), cep_to_coords('56306525'), cep_to_coords('56318080'), cep_to_coords('52041385'), cep_to_coords('56906390'), cep_to_coords('56903242'), cep_to_coords('56903278'), cep_to_coords('54786390'), cep_to_coords('52080001'), cep_to_coords('55620535'), cep_to_coords('55610420'), cep_to_coords('52390480'), cep_to_coords('51190080'), cep_to_coords('54430041'), cep_to_coords('56317170'), cep_to_coords('53635171'), cep_to_coords('55041050'), cep_to_coords('56312280'), cep_to_coords('53270540'), cep_to_coords('52403010'), cep_to_coords('56313550'), cep_to_coords('56313345'), cep_to_coords('56322000'), cep_to_coords('55150001'), cep_to_coords('55022610'), cep_to_coords('55648000'), cep_to_coords('56304280'), cep_to_coords('55020270'), cep_to_coords('56306240'), cep_to_coords('09550640'), cep_to_coords('56330180'), cep_to_coords('58835000'), cep_to_coords('50790140'), cep_to_coords('53020060'), cep_to_coords('53605750'), cep_to_coords('56309170'), cep_to_coords('51170530'), cep_to_coords('50780000'), cep_to_coords('56304610'), cep_to_coords('56330750'), cep_to_coords('05546000'), cep_to_coords('52280030'), cep_to_coords('54720018'), cep_to_coords('50620550'), cep_to_coords('54320366'), cep_to_coords('54370470'), cep_to_coords('56503470'), cep_to_coords('50060002'), cep_to_coords('54120445'), cep_to_coords('55298190'), cep_to_coords('56328170'), cep_to_coords('54410011'), cep_to_coords('50070495'), cep_to_coords('55433057'), cep_to_coords('51150070'), cep_to_coords('54705575'), cep_to_coords('54705073'), cep_to_coords('50090215'), cep_to_coords('51250290'), cep_to_coords('53450020'), cep_to_coords('55292210'), cep_to_coords('54520140'), cep_to_coords('53330730'), cep_to_coords('54774565'), cep_to_coords('53560249'), cep_to_coords('53080501'), cep_to_coords('52081420'), cep_to_coords('51300420'), cep_to_coords('54090160'), cep_to_coords('53220790'), cep_to_coords('53110640'), cep_to_coords('53402690'), cep_to_coords('52171271'), cep_to_coords('52041725'), cep_to_coords('50710290'), cep_to_coords('57036540'), cep_to_coords('50630240'), cep_to_coords('56306505'), cep_to_coords('54280070'), cep_to_coords('53070160'), cep_to_coords('53540660'), cep_to_coords('55028080'), cep_to_coords('56302600'), cep_to_coords('48650000'), cep_to_coords('54735660'), cep_to_coords('55292150'), cep_to_coords('53840901'), cep_to_coords('53640901'), cep_to_coords('52090272'), cep_to_coords('55020020'), cep_to_coords('59900000'), cep_to_coords('56312510'), cep_to_coords('52131130'), cep_to_coords('56312321'), cep_to_coords('54440297'), cep_to_coords('50741470'), cep_to_coords('50110440'), cep_to_coords('51230050'), cep_to_coords('55019015'), cep_to_coords('52170100'), cep_to_coords('51230480'), cep_to_coords('54250010'), cep_to_coords('54220021'), cep_to_coords('51270060'), cep_to_coords('50721725'), cep_to_coords('50875250'), cep_to_coords('50030970'), cep_to_coords('55014395'), cep_to_coords('55028340'), cep_to_coords('54280255'), cep_to_coords('54340740'), cep_to_coords('54330350'), cep_to_coords('54330727'), cep_to_coords('53530422'), cep_to_coords('54330830'), cep_to_coords('53431335'), cep_to_coords('50781120'), cep_to_coords('50860270'), cep_to_coords('53040360'), cep_to_coords('50920722'), cep_to_coords('50760080'), cep_to_coords('51350110'), cep_to_coords('54786490'), cep_to_coords('50020180'), cep_to_coords('53540480'), cep_to_coords('56321520'), cep_to_coords('54759140'), cep_to_coords('53407140'), cep_to_coords('53110760'), cep_to_coords('53431755'), cep_to_coords('53415530'), cep_to_coords('55010000'), cep_to_coords('50060060'), cep_to_coords('55295105'), cep_to_coords('53180110'), cep_to_coords('52210080'), cep_to_coords('55235000'), cep_to_coords('55195036'), cep_to_coords('55024153'), cep_to_coords('52320100'), cep_to_coords('54777440'), cep_to_coords('54762794'), cep_to_coords('50771440'), cep_to_coords('56309412'), cep_to_coords('52160565'), cep_to_coords('52280515'), cep_to_coords('55195554'), cep_to_coords('52221270'), cep_to_coords('58130300'), cep_to_coords('54510500'), cep_to_coords('54589100'), cep_to_coords('54518040'), cep_to_coords('52061040'), cep_to_coords('54767016'), cep_to_coords('52041575'), cep_to_coords('56906121'), cep_to_coords('56906303'), cep_to_coords('54345030'), cep_to_coords('58073000'), cep_to_coords('53260050'), cep_to_coords('50865030'), cep_to_coords('53407275'), cep_to_coords('55608431'), cep_to_coords('52011250'), cep_to_coords('53620480'), cep_to_coords('56318410'), cep_to_coords('56310658'), cep_to_coords('48903050'), cep_to_coords('50011030'), cep_to_coords('52211417'), cep_to_coords('56306320'), cep_to_coords('56316170'), cep_to_coords('55022000'), cep_to_coords('55018690'), cep_to_coords('53530464'), cep_to_coords('56310560'), cep_to_coords('52150081'), cep_to_coords('55297250'), cep_to_coords('55294828'), cep_to_coords('56330520'), cep_to_coords('50070310'), cep_to_coords('55152120'), cep_to_coords('53270270'), cep_to_coords('55020050'), cep_to_coords('56320705'), cep_to_coords('56306380'), cep_to_coords('56310350'), cep_to_coords('51330090'), cep_to_coords('56503070'), cep_to_coords('55291670'), cep_to_coords('50720230'), cep_to_coords('56320040'), cep_to_coords('50970250'), cep_to_coords('54896202'), cep_to_coords('53433260'), cep_to_coords('53405778'), cep_to_coords('53415030'), cep_to_coords('52171235'), cep_to_coords('56509810'), cep_to_coords('54280261'), cep_to_coords('38610000'), cep_to_coords('55044010'), cep_to_coords('53350050'), cep_to_coords('52120314'), cep_to_coords('52120440'), cep_to_coords('56509290'), cep_to_coords('55641651'), cep_to_coords('56513020'), cep_to_coords('56509720'), cep_to_coords('56720310'), cep_to_coords('54230100'), cep_to_coords('50640140'), cep_to_coords('51270230'), cep_to_coords('53240760'), cep_to_coords('53610010'), cep_to_coords('51011200'), cep_to_coords('58428850'), cep_to_coords('56322420'), cep_to_coords('50072080'), cep_to_coords('25041015'), cep_to_coords('50050550'), cep_to_coords('51070210'), cep_to_coords('53540180'), cep_to_coords('53550680'), cep_to_coords('53523150'), cep_to_coords('52131241'), cep_to_coords('54360120'), cep_to_coords('53020520'), cep_to_coords('53421101'), cep_to_coords('52190530'), cep_to_coords('52091090'), cep_to_coords('54790390'), cep_to_coords('54230220'), cep_to_coords('56503331'), cep_to_coords('55036610'), cep_to_coords('55006110'), cep_to_coords('55642210'), cep_to_coords('55031410'), cep_to_coords('50790900'), cep_to_coords('53290245'), cep_to_coords('52190242'), cep_to_coords('55038200'), cep_to_coords('55028510'), cep_to_coords('52731430'), cep_to_coords('50110755'), cep_to_coords('55081856'), cep_to_coords('50810210'), cep_to_coords('51010800'), cep_to_coords('54430295'), cep_to_coords('50980600'), cep_to_coords('50877010'), cep_to_coords('52070582'), cep_to_coords('50781570'), cep_to_coords('54140261'), cep_to_coords('55024518'), cep_to_coords('50970090'), cep_to_coords('56310010'), cep_to_coords('53150055'), cep_to_coords('54530080'), cep_to_coords('54771030'), cep_to_coords('50220170'), cep_to_coords('50110495'), cep_to_coords('52211460'), cep_to_coords('52291250'), cep_to_coords('55036530'), cep_to_coords('54766010'), cep_to_coords('54220560'), cep_to_coords('52191240'), cep_to_coords('54470580'), cep_to_coords('52020110'), cep_to_coords('55205028'), cep_to_coords('52280228'), cep_to_coords('50760680'), cep_to_coords('54518160'), cep_to_coords('53210091'), cep_to_coords('56318320'), cep_to_coords('50090230'), cep_to_coords('52060510'), cep_to_coords('50780460'), cep_to_coords('52111581'), cep_to_coords('55816680'), cep_to_coords('55022405'), cep_to_coords('55018423'), cep_to_coords('55018570'), cep_to_coords('55018760'), cep_to_coords('55018600'), cep_to_coords('55016520'), cep_to_coords('55020430'), cep_to_coords('55018580'), cep_to_coords('52171030'), cep_to_coords('50110226'), cep_to_coords('50030210'), cep_to_coords('54765240'), cep_to_coords('54786380'), cep_to_coords('54756063'), cep_to_coords('56909030'), cep_to_coords('55192365'), cep_to_coords('53060545'), cep_to_coords('52280130'), cep_to_coords('52070330'), cep_to_coords('52070015'), cep_to_coords('54410461'), cep_to_coords('56906186'), cep_to_coords('51345540'), cep_to_coords('55194265'), cep_to_coords('55643738'), cep_to_coords('50721680'), cep_to_coords('50721630'), cep_to_coords('51030220'), cep_to_coords('55606280'), cep_to_coords('52061020'), cep_to_coords('52080470'), cep_to_coords('55610511'), cep_to_coords('51250000'), cep_to_coords('54768455'), cep_to_coords('51150250'), cep_to_coords('53300010'), cep_to_coords('54515180'), cep_to_coords('55006490'), cep_to_coords('56300990'), cep_to_coords('56320095'), cep_to_coords('55024585'), cep_to_coords('48906145'), cep_to_coords('56309040'), cep_to_coords('53435430'), cep_to_coords('56330250'), cep_to_coords('56310785'), cep_to_coords('56323745'), cep_to_coords('56309330'), cep_to_coords('53150400'), cep_to_coords('56314050'), cep_to_coords('56512470'), cep_to_coords('51030250'), cep_to_coords('52041060'), cep_to_coords('54450005'), cep_to_coords('03632060'), cep_to_coords('50910070'), cep_to_coords('55158135'), cep_to_coords('54330210'), cep_to_coords('56503100'), cep_to_coords('56903490'), cep_to_coords('56320360'), cep_to_coords('53230170'), cep_to_coords('55612400'), cep_to_coords('53425600'), cep_to_coords('55038167'), cep_to_coords('56322070'), cep_to_coords('55034410'), cep_to_coords('56508185'), cep_to_coords('56511220'), cep_to_coords('56309480'), cep_to_coords('55195593'), cep_to_coords('55028460'), cep_to_coords('56306560'), cep_to_coords('54735400'), cep_to_coords('52041095'), cep_to_coords('53404090'), cep_to_coords('50640310'), cep_to_coords('56509030'), cep_to_coords('50780520'), cep_to_coords('55015290'), cep_to_coords('55296640'), cep_to_coords('52111280'), cep_to_coords('53565150'), cep_to_coords('53441230'), cep_to_coords('50791305'), cep_to_coords('50740440'), cep_to_coords('51170450'), cep_to_coords('53429580'), cep_to_coords('56306350'), cep_to_coords('50344450'), cep_to_coords('53444070'), cep_to_coords('53403490'), cep_to_coords('50760455'), cep_to_coords('55642835'), cep_to_coords('53610035'), cep_to_coords('51250300'), cep_to_coords('Resultados'), cep_to_coords('50670906'), cep_to_coords('51120010'), cep_to_coords('53020100'), cep_to_coords('53439510'), cep_to_coords('50080115'), cep_to_coords('50100120'), cep_to_coords('51010780'), cep_to_coords('52091120'), cep_to_coords('54730660'), cep_to_coords('56332115'), cep_to_coords('51271260'), cep_to_coords('52050145'), cep_to_coords('54715500'), cep_to_coords('53437240'), cep_to_coords('55014640'), cep_to_coords('54723080'), cep_to_coords('56312804'), cep_to_coords('51011120'), cep_to_coords('53080380'), cep_to_coords('53181110'), cep_to_coords('52291095'), cep_to_coords('50820641'), cep_to_coords('50940510'), cep_to_coords('50721615'), cep_to_coords('55291650'), cep_to_coords('50710280'), cep_to_coords('52050120'), cep_to_coords('52071230'), cep_to_coords('54210460'), cep_to_coords('54080281'), cep_to_coords('54300032'), cep_to_coords('25064037'), cep_to_coords('51190350'), cep_to_coords('51340724'), cep_to_coords('53070150'), cep_to_coords('50790130'), cep_to_coords('55700972'), cep_to_coords('54360130'), cep_to_coords('50680320'), cep_to_coords('54730430'), cep_to_coords('53090210'), cep_to_coords('54260530'), cep_to_coords('53439010'), cep_to_coords('51335140'), cep_to_coords('52221310'), cep_to_coords('52120290'), cep_to_coords('50960070'), cep_to_coords('53444540'), cep_to_coords('53150390'), cep_to_coords('53050300'), cep_to_coords('53170791'), cep_to_coords('54080380'), cep_to_coords('50030040'), cep_to_coords('53402855'), cep_to_coords('55608033'), cep_to_coords('52120183'), cep_to_coords('52060582'), cep_to_coords('51060582'), cep_to_coords('52090330'), cep_to_coords('51260290'), cep_to_coords('56306150'), cep_to_coords('52081040'), cep_to_coords('52071411'), cep_to_coords('56320460'), cep_to_coords('58755000'), cep_to_coords('54330345'), cep_to_coords('54300085'), cep_to_coords('54300031'), cep_to_coords('54340495'), cep_to_coords('56320190'), cep_to_coords('54110030'), cep_to_coords('52280730'), cep_to_coords('52150015'), cep_to_coords('54768814'), cep_to_coords('54756037'), cep_to_coords('54765290'), cep_to_coords('50640230'), cep_to_coords('50850370'), cep_to_coords('50030120'), cep_to_coords('55022150'), cep_to_coords('50810350'), cep_to_coords('52171265'), cep_to_coords('50080101'), cep_to_coords('50080180'), cep_to_coords('58070200'), cep_to_coords('52070220'), cep_to_coords('52710030'), cep_to_coords('54786550'), cep_to_coords('51270482'), cep_to_coords('50731260'), cep_to_coords('51335460'), cep_to_coords('54170030'), cep_to_coords('50761120'), cep_to_coords('54735780'), cep_to_coords('78455000'), cep_to_coords('53550025'), cep_to_coords('54580805'), cep_to_coords('54530510'), cep_to_coords('50751360'), cep_to_coords('50751405'), cep_to_coords('52210340'), cep_to_coords('54940040'), cep_to_coords('54505530'), cep_to_coords('52030250'), cep_to_coords('55295210'), cep_to_coords('56318460'), cep_to_coords('56306060'), cep_to_coords('56320706'), cep_to_coords('56328430'), cep_to_coords('53421490'), cep_to_coords('56320650'), cep_to_coords('53080300'), cep_to_coords('50760135'), cep_to_coords('51330280'), cep_to_coords('53630620'), cep_to_coords('53620505'), cep_to_coords('53060730'), cep_to_coords('53510560'), cep_to_coords('53510510'), cep_to_coords('53080280'), cep_to_coords('55642200'), cep_to_coords('55641728'), cep_to_coords('50731100'), cep_to_coords('53090450'), cep_to_coords('56510000'), cep_to_coords('55645040'), cep_to_coords('50960360'), cep_to_coords('56510200'), cep_to_coords('56506400'), cep_to_coords('56510400'), cep_to_coords('50781490'), cep_to_coords('50900180'), cep_to_coords('53422250'), cep_to_coords('50920661'), cep_to_coords('56510440'), cep_to_coords('56506660'), cep_to_coords('50770550'), cep_to_coords('51240360'), cep_to_coords('52150120'), cep_to_coords('55190522'), cep_to_coords('51330470'), cep_to_coords('51320545'), cep_to_coords('54330150'), cep_to_coords('53230250'), cep_to_coords('53050240'), cep_to_coords('53431480'), cep_to_coords('51150560'), cep_to_coords('54720702'), cep_to_coords('56512651'), cep_to_coords('55042110'), cep_to_coords('50630710'), cep_to_coords('52280035'), cep_to_coords('53530240'), cep_to_coords('53545180'), cep_to_coords('53433340'), cep_to_coords('50711320'), cep_to_coords('52130035'), cep_to_coords('51330380'), cep_to_coords('52140460'), cep_to_coords('55010305'), cep_to_coords('56328480'), cep_to_coords('55643050'), cep_to_coords('54735820'), cep_to_coords('56332635'), cep_to_coords('50751070'), cep_to_coords('51240370'), cep_to_coords('52130325'), cep_to_coords('55643130'), cep_to_coords('54720325'), cep_to_coords('54230625'), cep_to_coords('53401230'), cep_to_coords('52091450'), cep_to_coords('55819180'), cep_to_coords('51061080'), cep_to_coords('88092836'), cep_to_coords('68693290'), cep_to_coords('51270694'), cep_to_coords('53413300'), cep_to_coords('53550663'), cep_to_coords('54110200'), cep_to_coords('50720040'), cep_to_coords('50080490'), cep_to_coords('54783310'), cep_to_coords('56512660'), cep_to_coords('50070235'), cep_to_coords('51270260'), cep_to_coords('56318340'), cep_to_coords('53441620'), cep_to_coords('51290587'), cep_to_coords('54100290'), cep_to_coords('54090020'), cep_to_coords('54160020'), cep_to_coords('54150638'), cep_to_coords('54160101'), cep_to_coords('54100320'), cep_to_coords('54140060'), cep_to_coords('55602555'), cep_to_coords('54777360'), cep_to_coords('52070571'), cep_to_coords('52131470'), cep_to_coords('53250450'), cep_to_coords('50180040'), cep_to_coords('51150030'), cep_to_coords('56328310'), cep_to_coords('56306381'), cep_to_coords('56314330'), cep_to_coords('55008080'), cep_to_coords('55042040'), cep_to_coords('55036140'), cep_to_coords('54345210'), cep_to_coords('56312706'), cep_to_coords('54777815'), cep_to_coords('56313000'), cep_to_coords('50910280'), cep_to_coords('50820130'), cep_to_coords('52531541'), cep_to_coords('54530210'), cep_to_coords('54515991'), cep_to_coords('52071082'), cep_to_coords('53131155'), cep_to_coords('54762666'), cep_to_coords('54340095'), cep_to_coords('54330153'), cep_to_coords('57057540'), cep_to_coords('55006202'), cep_to_coords('55034010'), cep_to_coords('51340225'), cep_to_coords('52031065'), cep_to_coords('56512020'), cep_to_coords('56327040'), cep_to_coords('50850230'), cep_to_coords('55010009'), cep_to_coords('55014620'), cep_to_coords('55031070'), cep_to_coords('54460222'), cep_to_coords('64000000'), cep_to_coords('55012050'), cep_to_coords('51340540'), cep_to_coords('55610202'), cep_to_coords('55606225'), cep_to_coords('52121180'), cep_to_coords('50720493'), cep_to_coords('50910560'), cep_to_coords('52041172'), cep_to_coords('55297430'), cep_to_coords('53350080'), cep_to_coords('53360190'), cep_to_coords('55292570'), cep_to_coords('63100000'), cep_to_coords('55280900'), cep_to_coords('55292262'), cep_to_coords('55292277'), cep_to_coords('55293170'), cep_to_coords('55298195'), cep_to_coords('55294110'), cep_to_coords('55296130'), cep_to_coords('55299440'), cep_to_coords('55299442'), cep_to_coords('55299610'), cep_to_coords('55295796'), cep_to_coords('55296150'), cep_to_coords('55291617'), cep_to_coords('55294180'), cep_to_coords('55295575'), cep_to_coords('55295530'), cep_to_coords('56306710'), cep_to_coords('54280430'), cep_to_coords('54762410'), cep_to_coords('56312800'), cep_to_coords('56310000'), cep_to_coords('56318550'), cep_to_coords('56309240'), cep_to_coords('56322720'), cep_to_coords('53370290'), cep_to_coords('56318060'), cep_to_coords('56332610'), cep_to_coords('55540970'), cep_to_coords('56730000'), cep_to_coords('51010550'), cep_to_coords('53444380'), cep_to_coords('50761630'), cep_to_coords('52210331'), cep_to_coords('52210300'), cep_to_coords('53210640'), cep_to_coords('53402360'), cep_to_coords('56320720'), cep_to_coords('56306300'), cep_to_coords('52131305'), cep_to_coords('55299521'), cep_to_coords('56318160'), cep_to_coords('56328627'), cep_to_coords('56316040'), cep_to_coords('56503060'), cep_to_coords('55643250'), cep_to_coords('53320320'), cep_to_coords('51150001'), cep_to_coords('54325570'), cep_to_coords('54330202'), cep_to_coords('55291737'), cep_to_coords('54410585'), cep_to_coords('55294860'), cep_to_coords('53110731'), cep_to_coords('50080290'), cep_to_coords('51170610'), cep_to_coords('53441570'), cep_to_coords('50711230'), cep_to_coords('50771070'), cep_to_coords('52021041'), cep_to_coords('50761145'), cep_to_coords('50761342'), cep_to_coords('50771685'), cep_to_coords('51150120'), cep_to_coords('51150320'), cep_to_coords('50731065'), cep_to_coords('54535210'), cep_to_coords('54765440'), cep_to_coords('50780201'), cep_to_coords('52280360'), cep_to_coords('50980785'), cep_to_coords('54100610'), cep_to_coords('55014847'), cep_to_coords('50751010'), cep_to_coords('52170340'), cep_to_coords('56306405'), cep_to_coords('50420640'), cep_to_coords('50920270'), cep_to_coords('51340390'), cep_to_coords('50710160'), cep_to_coords('55012110'), cep_to_coords('55032180'), cep_to_coords('54525990'), cep_to_coords('51170340'), cep_to_coords('51080280'), cep_to_coords('50701340'), cep_to_coords('50080190'), cep_to_coords('50970400'), cep_to_coords('55034530'), cep_to_coords('54715270'), cep_to_coords('02403011'), cep_to_coords('57530000'), cep_to_coords('53413580'), cep_to_coords('54410200'), cep_to_coords('53605495'), cep_to_coords('53407520'), cep_to_coords('53585320'), cep_to_coords('53510440'), cep_to_coords('52130200'), cep_to_coords('50780260'), cep_to_coords('50640600'), cep_to_coords('50192091'), cep_to_coords('51290360'), cep_to_coords('52071130'), cep_to_coords('52081072'), cep_to_coords('52041512'), cep_to_coords('53060240'), cep_to_coords('55194055'), cep_to_coords('50980675'), cep_to_coords('51275320'), cep_to_coords('53160250'), cep_to_coords('53230220'), cep_to_coords('51310430'), cep_to_coords('52081490'), cep_to_coords('52131014'), cep_to_coords('54320150'), cep_to_coords('55038480'), cep_to_coords('55004280'), cep_to_coords('55014360'), cep_to_coords('55018121'), cep_to_coords('55044140'), cep_to_coords('55038570'), cep_to_coords('55030150'), cep_to_coords('55038330'), cep_to_coords('55018280'), cep_to_coords('55014170'), cep_to_coords('55038170'), cep_to_coords('55027500'), cep_to_coords('55014415'), cep_to_coords('55027100'), cep_to_coords('55006195'), cep_to_coords('55038160'), cep_to_coords('56353700'), cep_to_coords('54510440'), cep_to_coords('54517285'), cep_to_coords('55044020'), cep_to_coords('54768310'), cep_to_coords('52160500'), cep_to_coords('50760540'), cep_to_coords('50790240'), cep_to_coords('51310220'), cep_to_coords('54350768'), cep_to_coords('52041460'), cep_to_coords('50760012'), cep_to_coords('52060585'), cep_to_coords('53350240'), cep_to_coords('56912590'), cep_to_coords('53090900'), cep_to_coords('50060380'), cep_to_coords('52120480'), cep_to_coords('53635555'), cep_to_coords('55032210'), cep_to_coords('53620120'), cep_to_coords('55024130'), cep_to_coords('50150250'), cep_to_coords('54360070'), cep_to_coords('50920590'), cep_to_coords('56308070'), cep_to_coords('54170170'), cep_to_coords('51203021'), cep_to_coords('55645999'), cep_to_coords('54730640'), cep_to_coords('55298590'), cep_to_coords('54762250'), cep_to_coords('55032510'), cep_to_coords('55292300'), cep_to_coords('51290150'), cep_to_coords('56330230'), cep_to_coords('55030050'), cep_to_coords('55100500'), cep_to_coords('53030625'), cep_to_coords('50960340'), cep_to_coords('54210314'), cep_to_coords('56328460'), cep_to_coords('58100158'), cep_to_coords('50600303'), cep_to_coords('52080350'), cep_to_coords('50300340'), cep_to_coords('55602001'), cep_to_coords('50670100'), cep_to_coords('56323805'), cep_to_coords('54786300'), cep_to_coords('56328540'), cep_to_coords('56306550'), cep_to_coords('55042230'), cep_to_coords('52130160'), cep_to_coords('50750250'), cep_to_coords('56313660'), cep_to_coords('55296195'), cep_to_coords('52041140'), cep_to_coords('50860050'), cep_to_coords('55010100'), cep_to_coords('55034060'), cep_to_coords('53010150'), cep_to_coords('51010360'), cep_to_coords('52280485'), cep_to_coords('55294794'), cep_to_coords('56304340'), cep_to_coords('55641708'), cep_to_coords('55006180'), cep_to_coords('55004360'), cep_to_coords('54100672'), cep_to_coords('53160760'), cep_to_coords('53437340'), cep_to_coords('54340705'), cep_to_coords('54310600'), cep_to_coords('50720480'), cep_to_coords('51260240'), cep_to_coords('53270093'), cep_to_coords('50850000'), cep_to_coords('54315000'), cep_to_coords('53560110'), cep_to_coords('51110280'), cep_to_coords('56326240'), cep_to_coords('53144160'), cep_to_coords('53431030'), cep_to_coords('50110330'), cep_to_coords('50771680'), cep_to_coords('50730630'), cep_to_coords('50060900'), cep_to_coords('55012070'), cep_to_coords('54735800'), cep_to_coords('55151710'), cep_to_coords('54280441'), cep_to_coords('54730310'), cep_to_coords('52870495'), cep_to_coords('53230230'), cep_to_coords('53150345'), cep_to_coords('50721325'), cep_to_coords('53190210'), cep_to_coords('53370843'), cep_to_coords('53150010'), cep_to_coords('50781422'), cep_to_coords('52165100'), cep_to_coords('52081503'), cep_to_coords('54735195'), cep_to_coords('50040250'), cep_to_coords('56330760'), cep_to_coords('56310120'), cep_to_coords('56302080'), cep_to_coords('54280030'), cep_to_coords('53530448'), cep_to_coords('53403080'), cep_to_coords('53550080'), cep_to_coords('53433000'), cep_to_coords('54777275'), cep_to_coords('54756440'), cep_to_coords('52021140'), cep_to_coords('52190480'), cep_to_coords('50110675'), cep_to_coords('50830190'), cep_to_coords('50771790'), cep_to_coords('50790171'), cep_to_coords('54090112'), cep_to_coords('55195024'), cep_to_coords('52110140'), cep_to_coords('51310080'), cep_to_coords('52081560'), cep_to_coords('50740280'), cep_to_coords('54310295'), cep_to_coords('52091140'), cep_to_coords('55195012'), cep_to_coords('50741440'), cep_to_coords('52150160'), cep_to_coords('52190264'), cep_to_coords('55612291'), cep_to_coords('52041730'), cep_to_coords('55038640'), cep_to_coords('55018595'), cep_to_coords('50920220'), cep_to_coords('56903160'), cep_to_coords('55041200'), cep_to_coords('54510005'), cep_to_coords('52140430'), cep_to_coords('55021250'), cep_to_coords('52031248'), cep_to_coords('54070200'), cep_to_coords('51741150'), cep_to_coords('53444140'), cep_to_coords('50560500'), cep_to_coords('53070400'), cep_to_coords('55816210'), cep_to_coords('55028556'), cep_to_coords('54240165'), cep_to_coords('54120320'), cep_to_coords('55815000'), cep_to_coords('55304970'), cep_to_coords('55295345'), cep_to_coords('53130140'), cep_to_coords('52061140'), cep_to_coords('55022210'), cep_to_coords('55004430'), cep_to_coords('55028576'), cep_to_coords('55042220'), cep_to_coords('56318000'), cep_to_coords('56304210'), cep_to_coords('52211560'), cep_to_coords('56320620'), cep_to_coords('54759210'), cep_to_coords('50630080'), cep_to_coords('54505120'), cep_to_coords('55156320'), cep_to_coords('50970210'), cep_to_coords('56301992'), cep_to_coords('54070110'), cep_to_coords('00000100'), cep_to_coords('50730400'), cep_to_coords('55016330'), cep_to_coords('53110420'), cep_to_coords('56506914'), cep_to_coords('56509582'), cep_to_coords('56508255'), cep_to_coords('54080500'), cep_to_coords('54330591'), cep_to_coords('55001020'), cep_to_coords('55299425'), cep_to_coords('50910320'), cep_to_coords('52160000'), cep_to_coords('50870230'), cep_to_coords('56506691'), cep_to_coords('56510090'), cep_to_coords('52071192'), cep_to_coords('56320065'), cep_to_coords('50850022'), cep_to_coords('50920199'), cep_to_coords('51190591'), cep_to_coords('53443110'), cep_to_coords('56503630'), cep_to_coords('56304010'), cep_to_coords('50610020'), cep_to_coords('53360260'), cep_to_coords('52160839'), cep_to_coords('54478989'), cep_to_coords('50070130'), cep_to_coords('52502006'), cep_to_coords('55036535'), cep_to_coords('54580630'), cep_to_coords('52060295'), cep_to_coords('50910000'), cep_to_coords('53720000'), cep_to_coords('54786900'), cep_to_coords('50720725'), cep_to_coords('51170185'), cep_to_coords('51170125'), cep_to_coords('52090480'), cep_to_coords('53441210'), cep_to_coords('50660350'), cep_to_coords('50110040'), cep_to_coords('54430284'), cep_to_coords('51170250'), cep_to_coords('56328200'), cep_to_coords('54250110'), cep_to_coords('53090180'), cep_to_coords('52111595'), cep_to_coords('53090170'), cep_to_coords('53030230'), cep_to_coords('54765365'), cep_to_coords('52131600'), cep_to_coords('52030030'), cep_to_coords('50770150'), cep_to_coords('52151260'), cep_to_coords('50913201'), cep_to_coords('69083180'), cep_to_coords('56509200'), cep_to_coords('56506320'), cep_to_coords('51346060'), cep_to_coords('50640021'), cep_to_coords('52061341'), cep_to_coords('55016160'), cep_to_coords('54520770'), cep_to_coords('50730140'), cep_to_coords('51340125'), cep_to_coords('53320260'), cep_to_coords('54783550'), cep_to_coords('53010060'), cep_to_coords('53250410'), cep_to_coords('55190056'), cep_to_coords('55194142'), cep_to_coords('55192245'), cep_to_coords('53645090'), cep_to_coords('53025030'), cep_to_coords('54780510'), cep_to_coords('53540150'), cep_to_coords('52291125'), cep_to_coords('50060670'), cep_to_coords('51240080'), cep_to_coords('51330385'), cep_to_coords('52111390'), cep_to_coords('52081081'), cep_to_coords('50741030'), cep_to_coords('51330265'), cep_to_coords('55191631'), cep_to_coords('55194225'), cep_to_coords('58297000'), cep_to_coords('51280140'), cep_to_coords('56330340'), cep_to_coords('51270710'), cep_to_coords('52111695'), cep_to_coords('55606250'), cep_to_coords('55602020'), cep_to_coords('56312085'), cep_to_coords('50030220'), cep_to_coords('54520400'), cep_to_coords('54505905'), cep_to_coords('56318830'), cep_to_coords('52221100'), cep_to_coords('52211195'), cep_to_coords('53419350'), cep_to_coords('52291115'), cep_to_coords('53230371'), cep_to_coords('52140440'), cep_to_coords('52121320'), cep_to_coords('55602261'), cep_to_coords('50790170'), cep_to_coords('55105000'), cep_to_coords('54750350'), cep_to_coords('55024270'), cep_to_coords('55006470'), cep_to_coords('55028410'), cep_to_coords('55293420'), cep_to_coords('55002053'), cep_to_coords('53230510'), cep_to_coords('53404410'), cep_to_coords('53404420'), cep_to_coords('53417480'), cep_to_coords('53630385'), cep_to_coords('54100275'), cep_to_coords('54100671'), cep_to_coords('93600000'), cep_to_coords('54325085'), cep_to_coords('51270130'), cep_to_coords('53421780'), cep_to_coords('54250070'), cep_to_coords('50711035'), cep_to_coords('55604630'), cep_to_coords('57460000'), cep_to_coords('56506510'), cep_to_coords('50030260'), cep_to_coords('53240442'), cep_to_coords('52020380'), cep_to_coords('52031022'), cep_to_coords('51280290'), cep_to_coords('50781770'), cep_to_coords('55038388'), cep_to_coords('55294570'), cep_to_coords('54740690'), cep_to_coords('53320201'), cep_to_coords('50761760'), cep_to_coords('50671300'), cep_to_coords('52071440'), cep_to_coords('56798463'), cep_to_coords('56318155'), cep_to_coords('53625740'), cep_to_coords('53150442'), cep_to_coords('51010470'), cep_to_coords('50930280'), cep_to_coords('55020140'), cep_to_coords('54100144'), cep_to_coords('53433800'), cep_to_coords('53402030'), cep_to_coords('53270050'), cep_to_coords('07230450'), cep_to_coords('51270020'), cep_to_coords('52210260'), cep_to_coords('52291064'), cep_to_coords('50050360'), cep_to_coords('50060430'), cep_to_coords('52170040'), cep_to_coords('55298680'), cep_to_coords('90660692'), cep_to_coords('52050590'), cep_to_coords('54090360'), cep_to_coords('55034510'), cep_to_coords('56320790'), cep_to_coords('50403030'), cep_to_coords('54352190'), cep_to_coords('53402019'), cep_to_coords('53421380'), cep_to_coords('53421441'), cep_to_coords('53435702'), cep_to_coords('52070645'), cep_to_coords('50630785'), cep_to_coords('51200170'), cep_to_coords('50900160'), cep_to_coords('55012060'), cep_to_coords('55024745'), cep_to_coords('56332098'), cep_to_coords('54280405'), cep_to_coords('50900330'), cep_to_coords('50193209'), cep_to_coords('50620450'), cep_to_coords('50721700'), cep_to_coords('53420320'), cep_to_coords('54720689'), cep_to_coords('55819610'), cep_to_coords('55575000'), cep_to_coords('52110315'), cep_to_coords('52280405'), cep_to_coords('51011230'), cep_to_coords('52280493'), cep_to_coords('42807069'), cep_to_coords('50720415'), cep_to_coords('55299485'), cep_to_coords('50865040'), cep_to_coords('50610480'), cep_to_coords('65464564'), cep_to_coords('54768083'), cep_to_coords('52010240'), cep_to_coords('56330500'), cep_to_coords('56320490'), cep_to_coords('56320470'), cep_to_coords('50930178'), cep_to_coords('55024603'), cep_to_coords('55043080'), cep_to_coords('56316754'), cep_to_coords('56321140'), cep_to_coords('55028458'), cep_to_coords('55022455'), cep_to_coords('55043020'), cep_to_coords('50050330'), cep_to_coords('55043240'), cep_to_coords('52211400'), cep_to_coords('52211080'), cep_to_coords('52111050'), cep_to_coords('55034490'), cep_to_coords('55024740'), cep_to_coords('54330970'), cep_to_coords('55020175'), cep_to_coords('52081005'), cep_to_coords('50910210'), cep_to_coords('52081210'), cep_to_coords('52120295'), cep_to_coords('52050381'), cep_to_coords('52071625'), cep_to_coords('52079625'), cep_to_coords('54766025'), cep_to_coords('52211001'), cep_to_coords('55294490'), cep_to_coords('51290300'), cep_to_coords('55108500'), cep_to_coords('55190359'), cep_to_coords('51290020'), cep_to_coords('54330291'), cep_to_coords('52110469'), cep_to_coords('51203130'), cep_to_coords('51230490'), cep_to_coords('53625577'), cep_to_coords('53210560'), cep_to_coords('55012030'), cep_to_coords('53230241'), cep_to_coords('42850000'), cep_to_coords('53405000'), cep_to_coords('53429325'), cep_to_coords('50760710'), cep_to_coords('50670070'), cep_to_coords('50780420'), cep_to_coords('51240770'), cep_to_coords('55008050'), cep_to_coords('55020260'), cep_to_coords('54740820'), cep_to_coords('54768055'), cep_to_coords('54765055'), cep_to_coords('55292030'), cep_to_coords('55038040'), cep_to_coords('54830200'), cep_to_coords('54280510'), cep_to_coords('53570137'), cep_to_coords('53250005'), cep_to_coords('53110210'), cep_to_coords('54730730'), cep_to_coords('54720683'), cep_to_coords('56328905'), cep_to_coords('54759080'), cep_to_coords('54762210'), cep_to_coords('50670360'), cep_to_coords('55604050'), cep_to_coords('52291071'), cep_to_coords('54275070'), cep_to_coords('53250170'), cep_to_coords('54315198'), cep_to_coords('51021780'), cep_to_coords('06455020'), cep_to_coords('54330083'), cep_to_coords('56519150'), cep_to_coords('56512460'), cep_to_coords('56512475'), cep_to_coords('53150350'), cep_to_coords('53585140'), cep_to_coords('55641200'), cep_to_coords('55298520'), cep_to_coords('54774290'), cep_to_coords('51260370'), cep_to_coords('50760085'), cep_to_coords('52090273'), cep_to_coords('52031244'), cep_to_coords('52110160'), cep_to_coords('52070547'), cep_to_coords('54310140'), cep_to_coords('53310140'), cep_to_coords('54330797'), cep_to_coords('53160402'), cep_to_coords('53435090'), cep_to_coords('54100645'), cep_to_coords('53407355'), cep_to_coords('52051007'), cep_to_coords('53030180'), cep_to_coords('50760650'), cep_to_coords('54780340'), cep_to_coords('54720270'), cep_to_coords('53240200'), cep_to_coords('55813550'), cep_to_coords('50791001'), cep_to_coords('54753740'), cep_to_coords('51110340'), cep_to_coords('54737000'), cep_to_coords('54762460'), cep_to_coords('51260296'), cep_to_coords('52131210'), cep_to_coords('52071241'), cep_to_coords('52090274'), cep_to_coords('53130110'), cep_to_coords('52120220'), cep_to_coords('56310450'), cep_to_coords('13604038'), cep_to_coords('54762720'), cep_to_coords('54420160'), cep_to_coords('55608050'), cep_to_coords('52021070'), cep_to_coords('51101101'), cep_to_coords('03804040'), cep_to_coords('50810600'), cep_to_coords('53270191'), cep_to_coords('55602570'), cep_to_coords('52090101'), cep_to_coords('54325340'), cep_to_coords('53421260'), cep_to_coords('53625744'), cep_to_coords('52211260'), cep_to_coords('53444161'), cep_to_coords('51050150'), cep_to_coords('50750215'), cep_to_coords('55296710'), cep_to_coords('54580035'), cep_to_coords('50050452'), cep_to_coords('55002410'), cep_to_coords('50791415'), cep_to_coords('50791410'), cep_to_coords('55004492'), cep_to_coords('56903250'), cep_to_coords('52090245'), cep_to_coords('52031250'), cep_to_coords('54300051'), cep_to_coords('54525190'), cep_to_coords('56490000'), cep_to_coords('56902236'), cep_to_coords('53370800'), cep_to_coords('50741040'), cep_to_coords('55008460'), cep_to_coords('55028420'), cep_to_coords('52291030'), cep_to_coords('55291725'), cep_to_coords('55022160'), cep_to_coords('53200470'), cep_to_coords('55002050'), cep_to_coords('53320491'), cep_to_coords('50002970'), cep_to_coords('56318400'), cep_to_coords('55032618'), cep_to_coords('53320010'), cep_to_coords('52050220'), cep_to_coords('53230400'), cep_to_coords('53160690'), cep_to_coords('53416150'), cep_to_coords('52131425'), cep_to_coords('54350160'), cep_to_coords('53405490'), cep_to_coords('50080082'), cep_to_coords('54762100'), cep_to_coords('54250030'), cep_to_coords('56515215'), cep_to_coords('53170350'), cep_to_coords('53409130'), cep_to_coords('55022490'), cep_to_coords('54280745'), cep_to_coords('50930220'), cep_to_coords('50711450'), cep_to_coords('50060290'), cep_to_coords('55294400'), cep_to_coords('54792420'), cep_to_coords('50761561'), cep_to_coords('51320150'), cep_to_coords('52130005'), cep_to_coords('55042130'), cep_to_coords('57550000'), cep_to_coords('55816430'), cep_to_coords('53433070'), cep_to_coords('52210170'), cep_to_coords('53270670'), cep_to_coords('53270676'), cep_to_coords('56506740'), cep_to_coords('53330400'), cep_to_coords('55020011'), cep_to_coords('55020009'), cep_to_coords('50810620'), cep_to_coords('55291110'), cep_to_coords('50820620'), cep_to_coords('52070450'), cep_to_coords('52071361'), cep_to_coords('52171010'), cep_to_coords('53120590'), cep_to_coords('53260470'), cep_to_coords('55032010'), cep_to_coords('52111450'), cep_to_coords('51345470'), cep_to_coords('56904100'), cep_to_coords('52061103'), cep_to_coords('53080811'), cep_to_coords('55034130'), cep_to_coords('50660060'), cep_to_coords('55816570'), cep_to_coords('56506460'), cep_to_coords('56312560'), cep_to_coords('54580352'), cep_to_coords('51280410'), cep_to_coords('53441660'), cep_to_coords('5555555555'), cep_to_coords('55034550'), cep_to_coords('50920080'), cep_to_coords('54768770'), cep_to_coords('55641692'), cep_to_coords('54530340'), cep_to_coords('53401590'), cep_to_coords('50775140'), cep_to_coords('52020040'), cep_to_coords('52110241'), cep_to_coords('50751040'), cep_to_coords('52120190'), cep_to_coords('50760570'), cep_to_coords('50870300'), cep_to_coords('52031371'), cep_to_coords('50720640'), cep_to_coords('53431135'), cep_to_coords('53250360'), cep_to_coords('53370020'), cep_to_coords('54765485'), cep_to_coords('05206170'), cep_to_coords('52165052'), cep_to_coords('50720135'), cep_to_coords('54325725'), cep_to_coords('52280142'), cep_to_coords('50970260'), cep_to_coords('52221331'), cep_to_coords('54410090'), cep_to_coords('51180180'), cep_to_coords('54490545'), cep_to_coords('50060390'), cep_to_coords('50791260'), cep_to_coords('53060525'), cep_to_coords('53420130'), cep_to_coords('56512650'), cep_to_coords('50900150'), cep_to_coords('09784100'), cep_to_coords('56169000'), cep_to_coords('55192415'), cep_to_coords('56511000'), cep_to_coords('55008268'), cep_to_coords('52130085'), cep_to_coords('50520340'), cep_to_coords('50000002'), cep_to_coords('55014400'), cep_to_coords('55028115'), cep_to_coords('55032120'), cep_to_coords('55020325'), cep_to_coords('55612615'), cep_to_coords('55030610'), cep_to_coords('55018777'), cep_to_coords('55038205'), cep_to_coords('55032391'), cep_to_coords('55032015'), cep_to_coords('55030051'), cep_to_coords('70073901'), cep_to_coords('52041650'), cep_to_coords('52021170'), cep_to_coords('50751085'), cep_to_coords('50751400'), cep_to_coords('55195196'), cep_to_coords('52070718'), cep_to_coords('54426315'), cep_to_coords('52280170'), cep_to_coords('54350120'), cep_to_coords('53409848'), cep_to_coords('52041735'), cep_to_coords('54330252'), cep_to_coords('54325275'), cep_to_coords('55002180'), cep_to_coords('54759115'), cep_to_coords('54765345'), cep_to_coords('53070240'), cep_to_coords('54756220'), cep_to_coords('52010900'), cep_to_coords('56310505'), cep_to_coords('54730650'), cep_to_coords('51220110'), cep_to_coords('50810170'), cep_to_coords('53625095'), cep_to_coords('55295325'), cep_to_coords('53417707'), cep_to_coords('54430070'), cep_to_coords('54400640'), cep_to_coords('50760170'), cep_to_coords('50710950'), cep_to_coords('50730120'), cep_to_coords('50070255'), cep_to_coords('50781560'), cep_to_coords('54160360'), cep_to_coords('54315322'), cep_to_coords('56318230'), cep_to_coords('53431050'), cep_to_coords('55296370'), cep_to_coords('55614290'), cep_to_coords('53413110'), cep_to_coords('58370000'), cep_to_coords('53416170'), cep_to_coords('50070555'), cep_to_coords('56505460'), cep_to_coords('50680520'), cep_to_coords('54210340'), cep_to_coords('54421003'), cep_to_coords('53637060'), cep_to_coords('63150000'), cep_to_coords('55032145'), cep_to_coords('55014730'), cep_to_coords('55014706'), cep_to_coords('55027630'), cep_to_coords('22024270'), cep_to_coords('53070120'), cep_to_coords('51290260'), cep_to_coords('54365340'), cep_to_coords('55022470'), cep_to_coords('55020300'), cep_to_coords('13426271'), cep_to_coords('55014550'), cep_to_coords('55040240'), cep_to_coords('54410070'), cep_to_coords('51340227'), cep_to_coords('53130360'), cep_to_coords('53230120'), cep_to_coords('52131430'), cep_to_coords('55004055'), cep_to_coords('52170050'), cep_to_coords('54720120'), cep_to_coords('53340343'), cep_to_coords('53120410'), cep_to_coords('50721580'), cep_to_coords('53640131'), cep_to_coords('53010031'), cep_to_coords('53080520'), cep_to_coords('51310480'), cep_to_coords('52030220'), cep_to_coords('55026180'), cep_to_coords('53190340'), cep_to_coords('53250460'), cep_to_coords('53050400'), cep_to_coords('55028310'), cep_to_coords('52210030'), cep_to_coords('50110570'), cep_to_coords('50720315'), cep_to_coords('50710080'), cep_to_coords('51230637'), cep_to_coords('53070020'), cep_to_coords('55036670'), cep_to_coords('52081453'), cep_to_coords('51210000'), cep_to_coords('50740505'), cep_to_coords('50740520'), cep_to_coords('91410000'), cep_to_coords('54120410'), cep_to_coords('50110005'), cep_to_coords('55642660'), cep_to_coords('55642651'), cep_to_coords('54100240'), cep_to_coords('52170360'), cep_to_coords('50720500'), cep_to_coords('51345500'), cep_to_coords('50110006'), cep_to_coords('55008540'), cep_to_coords('51050050'), cep_to_coords('53060070'), cep_to_coords('52211580'), cep_to_coords('51260660'), cep_to_coords('50791362'), cep_to_coords('06051975'), cep_to_coords('55595970'), cep_to_coords('53960000'), cep_to_coords('55608040'), cep_to_coords('55604600'), cep_to_coords('56909430'), cep_to_coords('54768090'), cep_to_coords('52091197'), cep_to_coords('55019255'), cep_to_coords('55021290'), cep_to_coords('55028105'), cep_to_coords('53640250'), cep_to_coords('50721400'), cep_to_coords('55018753'), cep_to_coords('55019220'), cep_to_coords('55014766'), cep_to_coords('50610560'), cep_to_coords('52131161'), cep_to_coords('54756688'), cep_to_coords('53560030'), cep_to_coords('54315510'), cep_to_coords('56912174'), cep_to_coords('55024195'), cep_to_coords('5500000'), cep_to_coords('56310290'), cep_to_coords('54754150'), cep_to_coords('54300360'), cep_to_coords('52280486'), cep_to_coords('52081330'), cep_to_coords('53620109'), cep_to_coords('51190150'), cep_to_coords('54350330'), cep_to_coords('50650430'), cep_to_coords('51340630'), cep_to_coords('54430100'), cep_to_coords('55299774'), cep_to_coords('56330420'), cep_to_coords('54270370'), cep_to_coords('55152010'), cep_to_coords('51275500'), cep_to_coords('54080460'), cep_to_coords('55014160'), cep_to_coords('57860000'), cep_to_coords('56302230'), cep_to_coords('51340234'), cep_to_coords('54767440'), cep_to_coords('55155550'), cep_to_coords('55291633'), cep_to_coords('55156435'), cep_to_coords('50960550'), cep_to_coords('51340185'), cep_to_coords('56320160'), cep_to_coords('55024140'), cep_to_coords('50650290'), cep_to_coords('53160480'), cep_to_coords('54340645'), cep_to_coords('55016570'), cep_to_coords('53230620'), cep_to_coords('52070392'), cep_to_coords('53320100'), cep_to_coords('55022205'), cep_to_coords('56511020'), cep_to_coords('55292161'), cep_to_coords('51180370'), cep_to_coords('51345080'), cep_to_coords('53407130'), cep_to_coords('51230160'), cep_to_coords('56512150'), cep_to_coords('53431275'), cep_to_coords('55034100'), cep_to_coords('56510140'), cep_to_coords('54325330'), cep_to_coords('53610435'), cep_to_coords('51345300'), cep_to_coords('51240430'), cep_to_coords('51011600'), cep_to_coords('05529000'), cep_to_coords('55008321'), cep_to_coords('24865445'), cep_to_coords('50640480'), cep_to_coords('51190530'), cep_to_coords('55032480'), cep_to_coords('55010318'), cep_to_coords('55010590'), cep_to_coords('55024120'), cep_to_coords('55031150'), cep_to_coords('55641070'), cep_to_coords('51030290'), cep_to_coords('55036010'), cep_to_coords('56519260'), cep_to_coords('54315155'), cep_to_coords('51020340'), cep_to_coords('50710200'), cep_to_coords('55006283'), cep_to_coords('54517020'), cep_to_coords('54420331'), cep_to_coords('53240575'), cep_to_coords('50710610'), cep_to_coords('50750590'), cep_to_coords('50750140'), cep_to_coords('50900240'), cep_to_coords('50790180'), cep_to_coords('52130100'), cep_to_coords('55297570'), cep_to_coords('55038760'), cep_to_coords('54340680'), cep_to_coords('55028360'), cep_to_coords('55028042'), cep_to_coords('55010330'), cep_to_coords('55020377'), cep_to_coords('55032001'), cep_to_coords('53240300'), cep_to_coords('52171040'), cep_to_coords('55642640'), cep_to_coords('54270992'), cep_to_coords('55900973'), cep_to_coords('53230590'), cep_to_coords('52080019'), cep_to_coords('53240130'), cep_to_coords('19911230'), cep_to_coords('54777530'), cep_to_coords('53060495'), cep_to_coords('51230670'), cep_to_coords('54777270'), cep_to_coords('54715000'), cep_to_coords('50820231'), cep_to_coords('52121310'), cep_to_coords('50930130'), cep_to_coords('55905000'), cep_to_coords('56903470'), cep_to_coords('50630560'), cep_to_coords('52110310'), cep_to_coords('50762901'), cep_to_coords('50760825'), cep_to_coords('52038081'), cep_to_coords('52280524'), cep_to_coords('53230000'), cep_to_coords('53110435'), cep_to_coords('50050385'), cep_to_coords('55608505'), cep_to_coords('55645480'), cep_to_coords('50721121'), cep_to_coords('53405322'), cep_to_coords('54220490'), cep_to_coords('54220351'), cep_to_coords('50760002'), cep_to_coords('56508200'), cep_to_coords('55028459'), cep_to_coords('55813100'), cep_to_coords('55813106'), cep_to_coords('52051330'), cep_to_coords('50920480'), cep_to_coords('55818565'), cep_to_coords('55819741'), cep_to_coords('55813401'), cep_to_coords('55819320'), cep_to_coords('52040070'), cep_to_coords('54759215'), cep_to_coords('53160360'), cep_to_coords('54100150'), cep_to_coords('52211490'), cep_to_coords('50770680'), cep_to_coords('52160050'), cep_to_coords('50771630'), cep_to_coords('51230180'), cep_to_coords('54774460'), cep_to_coords('50620020'), cep_to_coords('54250090'), cep_to_coords('54765210'), cep_to_coords('50030290'), cep_to_coords('55038385'), cep_to_coords('54768360'), cep_to_coords('52211180'), cep_to_coords('50020190'), cep_to_coords('55299370'), cep_to_coords('51320260'), cep_to_coords('55026520'), cep_to_coords('56304460'), cep_to_coords('51260600'), cep_to_coords('52140260'), cep_to_coords('50771560'), cep_to_coords('55158340'), cep_to_coords('55034340'), cep_to_coords('50860090'), cep_to_coords('51320390'), cep_to_coords('54130060'), cep_to_coords('55021030'), cep_to_coords('50820540'), cep_to_coords('52150150'), cep_to_coords('52191041'), cep_to_coords('55153184'), cep_to_coords('55030310'), cep_to_coords('55038670'), cep_to_coords('56328805'), cep_to_coords('50910300'), cep_to_coords('50080170'), cep_to_coords('55155971'), cep_to_coords('54777200'), cep_to_coords('54715800'), cep_to_coords('53540210'), cep_to_coords('56515080'), cep_to_coords('51330070'), cep_to_coords('51150191'), cep_to_coords('53370165'), cep_to_coords('51190655'), cep_to_coords('51220300'), cep_to_coords('29700010'), cep_to_coords('53240260'), cep_to_coords('54120440'), cep_to_coords('53417370'), cep_to_coords('53060190'), cep_to_coords('55008140'), cep_to_coords('53413250'), cep_to_coords('52090360'), cep_to_coords('52030200'), cep_to_coords('58074725'), cep_to_coords('54420625'), cep_to_coords('53435642'), cep_to_coords('55038120'), cep_to_coords('52120530'), cep_to_coords('50760178'), cep_to_coords('54735320'), cep_to_coords('51300470'), cep_to_coords('51320431'), cep_to_coords('56322100'), cep_to_coords('56322180'), cep_to_coords('55028161'), cep_to_coords('56506600'), cep_to_coords('55010110'), cep_to_coords('50710040'), cep_to_coords('54330530'), cep_to_coords('50781530'), cep_to_coords('50620260'), cep_to_coords('53433031'), cep_to_coords('54230412'), cep_to_coords('55292550'), cep_to_coords('53442140'), cep_to_coords('53429810'), cep_to_coords('54300063'), cep_to_coords('53550825'), cep_to_coords('53419255'), cep_to_coords('50830250'), cep_to_coords('56509780'), cep_to_coords('56503130'), cep_to_coords('56503310'), cep_to_coords('51280060'), cep_to_coords('52120135'), cep_to_coords('45600222'), cep_to_coords('55265000'), cep_to_coords('56318370'), cep_to_coords('56312285'), cep_to_coords('50720060'), cep_to_coords('55035580'), cep_to_coords('55038095'), cep_to_coords('55002090'), cep_to_coords('55612600'), cep_to_coords('55612440'), cep_to_coords('55602060'), cep_to_coords('55044105'), cep_to_coords('55034240'), cep_to_coords('56312785'), cep_to_coords('52061316'), cep_to_coords('53180040'), cep_to_coords('53160230'), cep_to_coords('53200080'), cep_to_coords('53160030'), cep_to_coords('53240470'), cep_to_coords('52061313'), cep_to_coords('54400003'), cep_to_coords('50900560'), cep_to_coords('52160210'), cep_to_coords('52190111'), cep_to_coords('55294270'), cep_to_coords('55294273'), cep_to_coords('55294271'), cep_to_coords('51200220'), cep_to_coords('54762455'), cep_to_coords('54740655'), cep_to_coords('53240630'), cep_to_coords('52070410'), cep_to_coords('55608671'), cep_to_coords('53421630'), cep_to_coords('50110643'), cep_to_coords('53140310'), cep_to_coords('54230010'), cep_to_coords('52070172'), cep_to_coords('55028065'), cep_to_coords('55008200'), cep_to_coords('54325130'), cep_to_coords('53280270'), cep_to_coords('50670240'), cep_to_coords('50123910'), cep_to_coords('55030555'), cep_to_coords('54330640'), cep_to_coords('55151816'), cep_to_coords('54705424'), cep_to_coords('55008620'), cep_to_coords('55027490'), cep_to_coords('54350092'), cep_to_coords('51023130'), cep_to_coords('54230065'), cep_to_coords('56517070'), cep_to_coords('52190201'), cep_to_coords('56503091'), cep_to_coords('55294480'), cep_to_coords('55294615'), cep_to_coords('53520720'), cep_to_coords('54230128'), cep_to_coords('54310335'), cep_to_coords('53290150'), cep_to_coords('53416060'), cep_to_coords('53415060'), cep_to_coords('54280298'), cep_to_coords('54100420'), cep_to_coords('53240420'), cep_to_coords('54330415'), cep_to_coords('55294430'), cep_to_coords('56330290'), cep_to_coords('53290165'), cep_to_coords('53260221'), cep_to_coords('53610520'), cep_to_coords('52071190'), cep_to_coords('52131250'), cep_to_coords('51350165'), cep_to_coords('50760420'), cep_to_coords('51330160'), cep_to_coords('54230401'), cep_to_coords('53110370'), cep_to_coords('50170440'), cep_to_coords('53230080'), cep_to_coords('53270035'), cep_to_coords('50741360'), cep_to_coords('53423500'), cep_to_coords('51340430'), cep_to_coords('55612080'), cep_to_coords('56509115'), cep_to_coords('55297790'), cep_to_coords('50070600'), cep_to_coords('53150332'), cep_to_coords('54505060'), cep_to_coords('50780720'), cep_to_coords('50923109'), cep_to_coords('52021080'), cep_to_coords('50781370'), cep_to_coords('55041350'), cep_to_coords('56321270'), cep_to_coords('56970000'), cep_to_coords('56318090'), cep_to_coords('55028390'), cep_to_coords('52010160'), cep_to_coords('50040540'), cep_to_coords('55024260'), cep_to_coords('55028580'), cep_to_coords('55049000'), cep_to_coords('55008391'), cep_to_coords('55030570'), cep_to_coords('55658000'), cep_to_coords('55023370'), cep_to_coords('55503165'), cep_to_coords('54330483'), cep_to_coords('54727230'), cep_to_coords('53220131'), cep_to_coords('56511270'), cep_to_coords('52031010'), cep_to_coords('51230430'), cep_to_coords('50830200'), cep_to_coords('50050530'), cep_to_coords('53020421'), cep_to_coords('32291070'), cep_to_coords('56314380'), cep_to_coords('56326090'), cep_to_coords('50110260'), cep_to_coords('51100150'), cep_to_coords('55018421'), cep_to_coords('55026145'), cep_to_coords('54100270'), cep_to_coords('72900000'), cep_to_coords('52141230'), cep_to_coords('50761300'), cep_to_coords('50900020'), cep_to_coords('54210305'), cep_to_coords('52190310'), cep_to_coords('50730590'), cep_to_coords('52091608'), cep_to_coords('52211171'), cep_to_coords('52120322'), cep_to_coords('60710030'), cep_to_coords('52140531'), cep_to_coords('54436149'), cep_to_coords('56912390'), cep_to_coords('52090504'), cep_to_coords('55010020'), cep_to_coords('55012590'), cep_to_coords('55292090'), cep_to_coords('50790050'), cep_to_coords('54756274'), cep_to_coords('51335510'), cep_to_coords('50690710'), cep_to_coords('50741340'), cep_to_coords('54280570'), cep_to_coords('51260480'), cep_to_coords('54120150'), cep_to_coords('54430410'), cep_to_coords('53650320'), cep_to_coords('55798000'), cep_to_coords('55014535'), cep_to_coords('52140140'), cep_to_coords('52160770'), cep_to_coords('52211252'), cep_to_coords('51340570'), cep_to_coords('52280303'), cep_to_coords('51150370'), cep_to_coords('54315260'), cep_to_coords('53441600'), cep_to_coords('54733290'), cep_to_coords('53220520'), cep_to_coords('50620190'), cep_to_coords('54220370'), cep_to_coords('55299475'), cep_to_coords('51330100'), cep_to_coords('53615010'), cep_to_coords('55299418'), cep_to_coords('55608160'), cep_to_coords('54720255'), cep_to_coords('50610540'), cep_to_coords('52071630'), cep_to_coords('55160970'), cep_to_coords('55155660'), cep_to_coords('55151810'), cep_to_coords('54530480'), cep_to_coords('50723330'), cep_to_coords('56912080'), cep_to_coords('54170140'), cep_to_coords('51340105'), cep_to_coords('50920060'), cep_to_coords('75690000'), cep_to_coords('54530035'), cep_to_coords('55642620'), cep_to_coords('55291130'), cep_to_coords('56508237'), cep_to_coords('55294267'), cep_to_coords('51190200'), cep_to_coords('55028455'), cep_to_coords('56508180'), cep_to_coords('56512230'), cep_to_coords('55016200'), cep_to_coords('50791050'), cep_to_coords('55813620'), cep_to_coords('53425620'), cep_to_coords('53416470'), cep_to_coords('50791160'), cep_to_coords('52210322'), cep_to_coords('53360120'), cep_to_coords('53419720'), cep_to_coords('53429445'), cep_to_coords('50920820'), cep_to_coords('50820920'), cep_to_coords('52291083'), cep_to_coords('51170070'), cep_to_coords('91160210'), cep_to_coords('55299350'), cep_to_coords('55296030'), cep_to_coords('53401140'), cep_to_coords('50920030'), cep_to_coords('52220210'), cep_to_coords('51335255'), cep_to_coords('54759175'), cep_to_coords('51250390'), cep_to_coords('55010610'), cep_to_coords('54270350'), cep_to_coords('53350790'), cep_to_coords('52131015'), cep_to_coords('52070035'), cep_to_coords('50730121'), cep_to_coords('52110435'), cep_to_coords('52160806'), cep_to_coords('54480030'), cep_to_coords('53637105'), cep_to_coords('54705151'), cep_to_coords('54730282'), cep_to_coords('53540340'), cep_to_coords('55642028'), cep_to_coords('54505265'), cep_to_coords('55002120'), cep_to_coords('56505191'), cep_to_coords('53140300'), cep_to_coords('50910302'), cep_to_coords('52280590'), cep_to_coords('55645120'), cep_to_coords('55642229'), cep_to_coords('54270160'), cep_to_coords('50771430'), cep_to_coords('50800260'), cep_to_coords('53080530'), cep_to_coords('52090433'), cep_to_coords('50791020'), cep_to_coords('52081130'), cep_to_coords('50110535'), cep_to_coords('50750080'), cep_to_coords('52070232'), cep_to_coords('52171085'), cep_to_coords('50710400'), cep_to_coords('52160120'), cep_to_coords('50760050'), cep_to_coords('52080175'), cep_to_coords('53010300'), cep_to_coords('51335210'), cep_to_coords('55641080'), cep_to_coords('51320420'), cep_to_coords('52490000'), cep_to_coords('50650360'), cep_to_coords('51150600'), cep_to_coords('54300510'), cep_to_coords('56320130'), cep_to_coords('56903264'), cep_to_coords('55008430'), cep_to_coords('55036250'), cep_to_coords('55022005'), cep_to_coords('55604030'), cep_to_coords('51190540'), cep_to_coords('50750130'), cep_to_coords('50006002'), cep_to_coords('53360060'), cep_to_coords('54786330'), cep_to_coords('53515510'), cep_to_coords('48680000'), cep_to_coords('52160830'), cep_to_coords('52070212'), cep_to_coords('56508175'), cep_to_coords('52125240'), cep_to_coords('55040305'), cep_to_coords('56907250'), cep_to_coords('55191579'), cep_to_coords('55192569'), cep_to_coords('55031170'), cep_to_coords('52031131'), cep_to_coords('51021041'), cep_to_coords('53270220'), cep_to_coords('54580322'), cep_to_coords('50630065'), cep_to_coords('53425020'), cep_to_coords('52191405'), cep_to_coords('50660000'), cep_to_coords('52291520'), cep_to_coords('51011480'), cep_to_coords('55291230'), cep_to_coords('55294330'), cep_to_coords('55298185'), cep_to_coords('55294007'), cep_to_coords('55294670'), cep_to_coords('54230645'), cep_to_coords('55294808'), cep_to_coords('53180010'), cep_to_coords('44790000'), cep_to_coords('55158520'), cep_to_coords('55150210'), cep_to_coords('51150203'), cep_to_coords('51150150'), cep_to_coords('51275260'), cep_to_coords('52060344'), cep_to_coords('52031216'), cep_to_coords('54735420'), cep_to_coords('54735280'), cep_to_coords('54735826'), cep_to_coords('50660080'), cep_to_coords('51300140'), cep_to_coords('50910370'), cep_to_coords('54170555'), cep_to_coords('55002260'), cep_to_coords('56304390'), cep_to_coords('61654625'), cep_to_coords('53140200'), cep_to_coords('52070644'), cep_to_coords('56503080'), cep_to_coords('54705120'), cep_to_coords('55194145'), cep_to_coords('50110165'), cep_to_coords('54230284'), cep_to_coords('54771610'), cep_to_coords('53415488'), cep_to_coords('54715150'), cep_to_coords('55038025'), cep_to_coords('53415210'), cep_to_coords('51291841'), cep_to_coords('52040160'), cep_to_coords('54715555'), cep_to_coords('52170110'), cep_to_coords('56312470'), cep_to_coords('53350630'), cep_to_coords('54720796'), cep_to_coords('54580270'), cep_to_coords('55811170'), cep_to_coords('53050010'), cep_to_coords('54535010'), cep_to_coords('52091150'), cep_to_coords('51270401'), cep_to_coords('53320180'), cep_to_coords('54786210'), cep_to_coords('54720730'), cep_to_coords('53250192'), cep_to_coords('52010102'), cep_to_coords('54070040'), cep_to_coords('52120610'), cep_to_coords('54720246'), cep_to_coords('54710680'), cep_to_coords('55030480'), cep_to_coords('54759340'), cep_to_coords('52081542'), cep_to_coords('52291195'), cep_to_coords('53190370'), cep_to_coords('50082026'), cep_to_coords('53200400'), cep_to_coords('53441500'), cep_to_coords('59280295'), cep_to_coords('53370285'), cep_to_coords('50640560'), cep_to_coords('51330220'), cep_to_coords('55294410'), cep_to_coords('55944410'), cep_to_coords('56909535'), cep_to_coords('50760025'), cep_to_coords('55022110'), cep_to_coords('55026110'), cep_to_coords('55022550'), cep_to_coords('50280260'), cep_to_coords('55034500'), cep_to_coords('55027380'), cep_to_coords('53433250'), cep_to_coords('52090665'), cep_to_coords('52031242'), cep_to_coords('54753170'), cep_to_coords('52061110'), cep_to_coords('53360355'), cep_to_coords('54330265'), cep_to_coords('52080120'), cep_to_coords('55030070'), cep_to_coords('52061030'), cep_to_coords('53422050'), cep_to_coords('55155410'), cep_to_coords('53570160'), cep_to_coords('54220040'), cep_to_coords('50780530'), cep_to_coords('52280071'), cep_to_coords('55155720'), cep_to_coords('50780440'), cep_to_coords('53444240'), cep_to_coords('53444250'), cep_to_coords('55014728'), cep_to_coords('53260380'), cep_to_coords('50930160'), cep_to_coords('54220650'), cep_to_coords('50630090'), cep_to_coords('54440530'), cep_to_coords('55155570'), cep_to_coords('56318190'), cep_to_coords('55014610'), cep_to_coords('55154130'), cep_to_coords('50201101'), cep_to_coords('53090560'), cep_to_coords('55012420'), cep_to_coords('53220700'), cep_to_coords('55016535'), cep_to_coords('55040335'), cep_to_coords('54756490'), cep_to_coords('53170120'), cep_to_coords('53417440'), cep_to_coords('56516085'), cep_to_coords('56516901'), cep_to_coords('56509808'), cep_to_coords('56505180'), cep_to_coords('50900200'), cep_to_coords('56503480'), cep_to_coords('53130330'), cep_to_coords('56314495'), cep_to_coords('54410320'), cep_to_coords('54589420'), cep_to_coords('50080230'), cep_to_coords('50730200'), cep_to_coords('69055021'), cep_to_coords('55036245'), cep_to_coords('51230390'), cep_to_coords('53010111'), cep_to_coords('55010293'), cep_to_coords('51310123'), cep_to_coords('55298205'), cep_to_coords('54325135'), cep_to_coords('52040260'), cep_to_coords('56505420'), cep_to_coords('50980755'), cep_to_coords('55014440'), cep_to_coords('54350812'), cep_to_coords('53010030'), cep_to_coords('51310180'), cep_to_coords('51010460'), cep_to_coords('54440540'), cep_to_coords('53630565'), cep_to_coords('53270501'), cep_to_coords('55027230'), cep_to_coords('55020025'), cep_to_coords('54525130'), cep_to_coords('50100140'), cep_to_coords('50050235'), cep_to_coords('58489000'), cep_to_coords('51310330'), cep_to_coords('50970410'), cep_to_coords('55835970'), cep_to_coords('53050341'), cep_to_coords('51335260'), cep_to_coords('53545240'), cep_to_coords('54730280'), cep_to_coords('54080290'), cep_to_coords('54510400'), cep_to_coords('53770000'), cep_to_coords('53110020'), cep_to_coords('54735650'), cep_to_coords('54730100'), cep_to_coords('55592972'), cep_to_coords('56509856'), cep_to_coords('53370750'), cep_to_coords('53401700'), cep_to_coords('50791484'), cep_to_coords('54315381'), cep_to_coords('56302770'), cep_to_coords('56312053'), cep_to_coords('51010290'), cep_to_coords('53220150'), cep_to_coords('50630490'), cep_to_coords('55612590'), cep_to_coords('55024540'), cep_to_coords('56332118'), cep_to_coords('55034430'), cep_to_coords('55031235'), cep_to_coords('53290300'), cep_to_coords('54490350'), cep_to_coords('50860120'), cep_to_coords('55014456'), cep_to_coords('50640275'), cep_to_coords('50721280'), cep_to_coords('50810220'), cep_to_coords('50480120'), cep_to_coords('54280180'), cep_to_coords('55014540'), cep_to_coords('55014543'), cep_to_coords('55016620'), cep_to_coords('50720120'), cep_to_coords('55016230'), cep_to_coords('55012130'), cep_to_coords('55028190'), cep_to_coords('55240600'), cep_to_coords('55012750'), cep_to_coords('55019380'), cep_to_coords('55032485'), cep_to_coords('55022410'), cep_to_coords('52210390'), cep_to_coords('50760515'), cep_to_coords('50741420'), cep_to_coords('54515190'), cep_to_coords('55042290'), cep_to_coords('53620132'), cep_to_coords('53334060'), cep_to_coords('55294565'), cep_to_coords('56509620'), cep_to_coords('50610260'), cep_to_coords('50870630'), cep_to_coords('50790500'), cep_to_coords('54730331'), cep_to_coords('55150320'), cep_to_coords('51160310'), cep_to_coords('55293180'), cep_to_coords('50820470'), cep_to_coords('50770590'), cep_to_coords('55010070'), cep_to_coords('55034150'), cep_to_coords('51040020'), cep_to_coords('04362060'), cep_to_coords('51170000'), cep_to_coords('56509362'), cep_to_coords('56509230'), cep_to_coords('50670190'), cep_to_coords('50790210'), cep_to_coords('54470495'), cep_to_coords('51260030'), cep_to_coords('54720074'), cep_to_coords('55034580'), cep_to_coords('52131592'), cep_to_coords('56318030'), cep_to_coords('54730165'), cep_to_coords('54410510'), cep_to_coords('56503370'), cep_to_coords('54160507'), cep_to_coords('55296518'), cep_to_coords('52090285'), cep_to_coords('55016140'), cep_to_coords('54530085'), cep_to_coords('54777010'), cep_to_coords('52130421'), cep_to_coords('54230232'), cep_to_coords('50761343'), cep_to_coords('56308200'), cep_to_coords('50041100'), cep_to_coords('56320610'), cep_to_coords('50760660'), cep_to_coords('54280325'), cep_to_coords('53416575'), cep_to_coords('50630230'), cep_to_coords('54762622'), cep_to_coords('54220640'), cep_to_coords('50721120'), cep_to_coords('53250320'), cep_to_coords('56328595'), cep_to_coords('58410000'), cep_to_coords('13100810'), cep_to_coords('50070085'), cep_to_coords('11111111'), cep_to_coords('52110550'), cep_to_coords('55014453'), cep_to_coords('51310270'), cep_to_coords('54777355'), cep_to_coords('53160830'), cep_to_coords('52121270'), cep_to_coords('55294782'), cep_to_coords('54480220'), cep_to_coords('53060814'), cep_to_coords('53280161'), cep_to_coords('50060190'), cep_to_coords('53402785'), cep_to_coords('55816590'), cep_to_coords('50740140'), cep_to_coords('55008310'), cep_to_coords('55608330'), cep_to_coords('56310745'), cep_to_coords('50870770'), cep_to_coords('53050031'), cep_to_coords('54720105'), cep_to_coords('52291655'), cep_to_coords('62656465'), cep_to_coords('50740690'), cep_to_coords('52030174'), cep_to_coords('52030180'), cep_to_coords('55520970'), cep_to_coords('53405813'), cep_to_coords('54340716'), cep_to_coords('54350105'), cep_to_coords('56903130'), cep_to_coords('53270180'), cep_to_coords('53565360'), cep_to_coords('53565130'), cep_to_coords('54777455'), cep_to_coords('56312420'), cep_to_coords('55002400'), cep_to_coords('54350465'), cep_to_coords('51190310'), cep_to_coords('54230260'), cep_to_coords('53240090'), cep_to_coords('55024040'), cep_to_coords('55014560'), cep_to_coords('54735590'), cep_to_coords('55604670'), cep_to_coords('50751340'), cep_to_coords('50865160'), cep_to_coords('20800090'), cep_to_coords('56503230'), cep_to_coords('50870740'), cep_to_coords('56515235'), cep_to_coords('56506650'), cep_to_coords('56502025'), cep_to_coords('55299838'), cep_to_coords('56509250'), cep_to_coords('56502340'), cep_to_coords('54768070'), cep_to_coords('53416640'), cep_to_coords('53444170'), cep_to_coords('54330180'), cep_to_coords('52021160'), cep_to_coords('52070140'), cep_to_coords('50620510'), cep_to_coords('55024520'), cep_to_coords('50721787'), cep_to_coords('54325296'), cep_to_coords('55014490'), cep_to_coords('52240150'), cep_to_coords('52040510'), cep_to_coords('52140020'), cep_to_coords('52020185'), cep_to_coords('50030610'), cep_to_coords('54705088'), cep_to_coords('50731250'), cep_to_coords('53530480'), cep_to_coords('54110130'), cep_to_coords('55024320'), cep_to_coords('56331278'), cep_to_coords('54120590'), cep_to_coords('55030052'), cep_to_coords('50680190'), cep_to_coords('53530392'), cep_to_coords('53570020'), cep_to_coords('52210421'), cep_to_coords('56509635'), cep_to_coords('53407510'), cep_to_coords('53290260'), cep_to_coords('53040040'), cep_to_coords('56318490'), cep_to_coords('53421785'), cep_to_coords('54260011'), cep_to_coords('52051050'), cep_to_coords('55012210'), cep_to_coords('56306580'), cep_to_coords('53090270'), cep_to_coords('55016650'), cep_to_coords('54530300'), cep_to_coords('54756555'), cep_to_coords('52080061'), cep_to_coords('50690720'), cep_to_coords('54230465'), cep_to_coords('52080150'), cep_to_coords('09390722'), cep_to_coords('52031252'), cep_to_coords('55026261'), cep_to_coords('54753705'), cep_to_coords('41250280'), cep_to_coords('55014365'), cep_to_coords('88309660'), cep_to_coords('50260670'), cep_to_coords('54280330'), cep_to_coords('09111967'), cep_to_coords('54520160'), cep_to_coords('11542080'), cep_to_coords('53190240'), cep_to_coords('50080570'), cep_to_coords('54090114'), cep_to_coords('52091304'), cep_to_coords('53550530'), cep_to_coords('53120520'), cep_to_coords('56314060'), cep_to_coords('56328270'), cep_to_coords('63430000'), cep_to_coords('56332004'), cep_to_coords('50860030'), cep_to_coords('50870620'), cep_to_coords('55032560'), cep_to_coords('50070060'), cep_to_coords('55018630'), cep_to_coords('53210450'), cep_to_coords('52081735'), cep_to_coords('56903266'), cep_to_coords('52041280'), cep_to_coords('55015340'), cep_to_coords('55019330'), cep_to_coords('55016082'), cep_to_coords('52071125'), cep_to_coords('52150290'), cep_to_coords('52125040'), cep_to_coords('52120360'), cep_to_coords('52160495'), cep_to_coords('50980775'), cep_to_coords('54589330'), cep_to_coords('54420060'), cep_to_coords('50610600'), cep_to_coords('51330450'), cep_to_coords('53442150'), cep_to_coords('52160510'), cep_to_coords('52011320'), cep_to_coords('55036260'), cep_to_coords('54310660'), cep_to_coords('52111002'), cep_to_coords('54505150'), cep_to_coords('53402110'), cep_to_coords('53030120'), cep_to_coords('50720540'), cep_to_coords('51320220'), cep_to_coords('54759225'), cep_to_coords('58740400'), cep_to_coords('54789765'), cep_to_coords('53625200'), cep_to_coords('53630457'), cep_to_coords('56328130'), cep_to_coords('52170415'), cep_to_coords('55080000'), cep_to_coords('52221410'), cep_to_coords('52091212'), cep_to_coords('56906040'), cep_to_coords('52360080'), cep_to_coords('54470040'), cep_to_coords('54330900'), cep_to_coords('53250480'), cep_to_coords('50970405'), cep_to_coords('56515590'), cep_to_coords('53401690'), cep_to_coords('53530690'), cep_to_coords('54230031'), cep_to_coords('51260720'), cep_to_coords('25482858'), cep_to_coords('56312040'), cep_to_coords('56310370'), cep_to_coords('50830320'), cep_to_coords('50750265'), cep_to_coords('54440545'), cep_to_coords('50751439'), cep_to_coords('51030130'), cep_to_coords('53080450'), cep_to_coords('50830430'), cep_to_coords('51345100'), cep_to_coords('55018380'), cep_to_coords('50920592'), cep_to_coords('55002170'), cep_to_coords('53530466'), cep_to_coords('50741465'), cep_to_coords('54310060'), cep_to_coords('54762662'), cep_to_coords('50720440'), cep_to_coords('51203013'), cep_to_coords('52031175'), cep_to_coords('55024350'), cep_to_coords('54705110'), cep_to_coords('55024820'), cep_to_coords('58401454'), cep_to_coords('50711430'), cep_to_coords('51320360'), cep_to_coords('51320440'), cep_to_coords('50790330'), cep_to_coords('54715180'), cep_to_coords('53170370'), cep_to_coords('52270370'), cep_to_coords('53170250'), cep_to_coords('53080030'), cep_to_coords('56509615'), cep_to_coords('52090050'), cep_to_coords('54250270'), cep_to_coords('56515010'), cep_to_coords('53429780'), cep_to_coords('50750030'), cep_to_coords('51280260'), cep_to_coords('52075250'), cep_to_coords('54230505'), cep_to_coords('51300141'), cep_to_coords('55022670'), cep_to_coords('54774421'), cep_to_coords('50711070'), cep_to_coords('51345050'), cep_to_coords('50830570'), cep_to_coords('55298065'), cep_to_coords('54290082'), cep_to_coords('54280542'), cep_to_coords('56503330'), cep_to_coords('53070140'), cep_to_coords('53190250'), cep_to_coords('50980655'), cep_to_coords('54280720'), cep_to_coords('54730200'), cep_to_coords('55642110'), cep_to_coords('54220245'), cep_to_coords('54420400'), cep_to_coords('53435350'), cep_to_coords('54260330'), cep_to_coords('55034030'), cep_to_coords('52075331'), cep_to_coords('54220341'), cep_to_coords('54380081'), cep_to_coords('50650160'), cep_to_coords('50711420'), cep_to_coords('54260222'), cep_to_coords('08150000'), cep_to_coords('53240108'), cep_to_coords('54735740'), cep_to_coords('52041700'), cep_to_coords('56328275'), cep_to_coords('72870128'), cep_to_coords('55027550'), cep_to_coords('53416140'), cep_to_coords('52020011'), cep_to_coords('53640020'), cep_to_coords('05693000'), cep_to_coords('53540260'), cep_to_coords('50781660'), cep_to_coords('53080020'), cep_to_coords('52110290'), cep_to_coords('53120300'), cep_to_coords('50080800'), cep_to_coords('54520460'), cep_to_coords('54762030'), cep_to_coords('51010240'), cep_to_coords('51010510'), cep_to_coords('50780130'), cep_to_coords('54315420'), cep_to_coords('55298170'), cep_to_coords('55606215'), cep_to_coords('53210280'), cep_to_coords('55002010'), cep_to_coords('55028075'), cep_to_coords('55028000'), cep_to_coords('51110100'), cep_to_coords('52030195'), cep_to_coords('51150010'), cep_to_coords('52190291'), cep_to_coords('50910040'), cep_to_coords('52031260'), cep_to_coords('53530290'), cep_to_coords('50910270'), cep_to_coords('51340590'), cep_to_coords('50711060'), cep_to_coords('55024110'), cep_to_coords('56316140'), cep_to_coords('55004450'), cep_to_coords('55004452'), cep_to_coords('55002060'), cep_to_coords('55016555'), cep_to_coords('55027090'), cep_to_coords('55014380'), cep_to_coords('56312050'), cep_to_coords('50620570'), cep_to_coords('50760240'), cep_to_coords('52081003'), cep_to_coords('56316675'), cep_to_coords('56314505'), cep_to_coords('50841002'), cep_to_coords('56316480'), cep_to_coords('52120215'), cep_to_coords('53421371'), cep_to_coords('50910530'), cep_to_coords('52120230'), cep_to_coords('53350001'), cep_to_coords('50790360'), cep_to_coords('55038015'), cep_to_coords('53350760'), cep_to_coords('51340640'), cep_to_coords('55037190'), cep_to_coords('54170350'), cep_to_coords('52071270'), cep_to_coords('50761425'), cep_to_coords('52050091'), cep_to_coords('50002309'), cep_to_coords('53360350'), cep_to_coords('54740290'), cep_to_coords('55154105'), cep_to_coords('53610727'), cep_to_coords('53570294'), cep_to_coords('54580560'), cep_to_coords('56200580'), cep_to_coords('53520010'), cep_to_coords('55038730'), cep_to_coords('55026250'), cep_to_coords('55302970'), cep_to_coords('55022485'), cep_to_coords('52130410'), cep_to_coords('53520230'), cep_to_coords('55155040'), cep_to_coords('55154140'), cep_to_coords('55032420'), cep_to_coords('55296160'), cep_to_coords('55158070'), cep_to_coords('55152510'), cep_to_coords('55867000'), cep_to_coords('50070550'), cep_to_coords('53530428'), cep_to_coords('53420000'), cep_to_coords('55296280'), cep_to_coords('55150690'), cep_to_coords('55155690'), cep_to_coords('56515311'), cep_to_coords('54515540'), cep_to_coords('56322230'), cep_to_coords('53433080'), cep_to_coords('53320020'), cep_to_coords('50650200'), cep_to_coords('50820080'), cep_to_coords('50820210'), cep_to_coords('50731020'), cep_to_coords('55002200'), cep_to_coords('54330785'), cep_to_coords('53080195'), cep_to_coords('53130545'), cep_to_coords('53130543'), cep_to_coords('55298310'), cep_to_coords('55292130'), cep_to_coords('56318833'), cep_to_coords('56322210'), cep_to_coords('50791500'), cep_to_coords('55016070'), cep_to_coords('55014680'), cep_to_coords('55016020'), cep_to_coords('53210060'), cep_to_coords('55036095'), cep_to_coords('54325560'), cep_to_coords('50660270'), cep_to_coords('52131543'), cep_to_coords('53230180'), cep_to_coords('53425410'), cep_to_coords('52211190'), cep_to_coords('52280560'), cep_to_coords('51280430'), cep_to_coords('55032605'), cep_to_coords('53431360'), cep_to_coords('53401744'), cep_to_coords('50751470'), cep_to_coords('55028324'), cep_to_coords('55297130'), cep_to_coords('52010260'), cep_to_coords('55030470'), cep_to_coords('53431450'), cep_to_coords('52091470'), cep_to_coords('50780250'), cep_to_coords('52280082'), cep_to_coords('54120025'), cep_to_coords('50760155'), cep_to_coords('54360110'), cep_to_coords('54530003'), cep_to_coords('54767065'), cep_to_coords('50110758'), cep_to_coords('55024240'), cep_to_coords('54340475'), cep_to_coords('50080724'), cep_to_coords('55815080'), cep_to_coords('56332665'), cep_to_coords('53060020'), cep_to_coords('53210251'), cep_to_coords('52221220'), cep_to_coords('50800270'), cep_to_coords('51320670'), cep_to_coords('52060463'), cep_to_coords('50920190'), cep_to_coords('50910540'), cep_to_coords('53439426'), cep_to_coords('53429170'), cep_to_coords('54300061'), cep_to_coords('56302430'), cep_to_coords('51300150'), cep_to_coords('53170050'), cep_to_coords('55295120'), cep_to_coords('53402485'), cep_to_coords('55296380'), cep_to_coords('55032320'), cep_to_coords('52091076'), cep_to_coords('53610833'), cep_to_coords('53435040'), cep_to_coords('57730250'), cep_to_coords('55030090'), cep_to_coords('56511140'), cep_to_coords('56511202'), cep_to_coords('56519340'), cep_to_coords('52131240'), cep_to_coords('53070200'), cep_to_coords('53350350'), cep_to_coords('55020310'), cep_to_coords('56519090'), cep_to_coords('52081660'), cep_to_coords('54100050'), cep_to_coords('56509450'), cep_to_coords('55414000'), cep_to_coords('55295535'), cep_to_coords('51230665'), cep_to_coords('54150231'), cep_to_coords('53405600'), cep_to_coords('54505015'), cep_to_coords('53320550'), cep_to_coords('53080060'), cep_to_coords('53409540'), cep_to_coords('53413390'), cep_to_coords('50080102'), cep_to_coords('52111210'), cep_to_coords('22765660'), cep_to_coords('53240280'), cep_to_coords('54230392'), cep_to_coords('50771780'), cep_to_coords('55006440'), cep_to_coords('50090690'), cep_to_coords('56328500'), cep_to_coords('50780050'), cep_to_coords('53439140'), cep_to_coords('52081730'), cep_to_coords('52061355'), cep_to_coords('52121110'), cep_to_coords('56319630'), cep_to_coords('50030902'), cep_to_coords('52080663'), cep_to_coords('50721800'), cep_to_coords('50080460'), cep_to_coords('53160560'), cep_to_coords('55643120'), cep_to_coords('55644846'), cep_to_coords('55641470'), cep_to_coords('54510010'), cep_to_coords('50010300'), cep_to_coords('50760590'), cep_to_coords('55018560'), cep_to_coords('54220725'), cep_to_coords('58220725'), cep_to_coords('54522125'), cep_to_coords('54517095'), cep_to_coords('54753730'), cep_to_coords('50790600'), cep_to_coords('50690750'), cep_to_coords('52140502'), cep_to_coords('54275030'), cep_to_coords('50660190'), cep_to_coords('50730005'), cep_to_coords('50650370'), cep_to_coords('55819250'), cep_to_coords('52280363'), cep_to_coords('52171025'), cep_to_coords('51240780'), cep_to_coords('54090290'), cep_to_coords('07114250'), cep_to_coords('54735710'), cep_to_coords('54740540'), cep_to_coords('54330040'), cep_to_coords('53210510'), cep_to_coords('52111079'), cep_to_coords('50650050'), cep_to_coords('51130340'), cep_to_coords('50601000'), cep_to_coords('50790615'), cep_to_coords('50060160'), cep_to_coords('50980350'), cep_to_coords('54210394'), cep_to_coords('50660180'), cep_to_coords('50970290'), cep_to_coords('53170620'), cep_to_coords('54715655'), cep_to_coords('54330405'), cep_to_coords('51340050'), cep_to_coords('50761132'), cep_to_coords('50690170'), cep_to_coords('56800999'), cep_to_coords('56912560'), cep_to_coords('54240435'), cep_to_coords('50129310'), cep_to_coords('55018001'), cep_to_coords('09150230'), cep_to_coords('53120330'), cep_to_coords('55813410'), cep_to_coords('53421511'), cep_to_coords('51260220'), cep_to_coords('53413400'), cep_to_coords('56515610'), cep_to_coords('53280310'), cep_to_coords('50070325'), cep_to_coords('55815105'), cep_to_coords('54759195'), cep_to_coords('52081230'), cep_to_coords('54517275'), cep_to_coords('50100242'), cep_to_coords('54490056'), cep_to_coords('55290372'), cep_to_coords('55294370'), cep_to_coords('54410295'), cep_to_coords('53416720'), cep_to_coords('55813450'), cep_to_coords('53580603'), cep_to_coords('55819420'), cep_to_coords('53220070'), cep_to_coords('53080360'), cep_to_coords('52040430'), cep_to_coords('50900461'), cep_to_coords('52090304'), cep_to_coords('55291673'), cep_to_coords('54325270'), cep_to_coords('51160170'), cep_to_coords('51250321'), cep_to_coords('51270590'), cep_to_coords('50751290'), cep_to_coords('54210322'), cep_to_coords('53433210'), cep_to_coords('55038370'), cep_to_coords('55643200'), cep_to_coords('51275510'), cep_to_coords('54325295'), cep_to_coords('54580812'), cep_to_coords('52091121'), cep_to_coords('53130120'), cep_to_coords('53580370'), cep_to_coords('54762303'), cep_to_coords('52131160'), cep_to_coords('55644230'), cep_to_coords('55024220'), cep_to_coords('55002030'), cep_to_coords('55015370'), cep_to_coords('55813540'), cep_to_coords('54120050'), cep_to_coords('54762335'), cep_to_coords('55020370'), cep_to_coords('51270340'), cep_to_coords('50660290'), cep_to_coords('53350300'), cep_to_coords('55038795'), cep_to_coords('50870220'), cep_to_coords('51170200'), cep_to_coords('51150770'), cep_to_coords('52040241'), cep_to_coords('50761140'), cep_to_coords('52130440'), cep_to_coords('55290505'), cep_to_coords('11432290'), cep_to_coords('55010290'), cep_to_coords('56320120'), cep_to_coords('55022480'), cep_to_coords('55016210'), cep_to_coords('56303002'), cep_to_coords('50050145'), cep_to_coords('51170620'), cep_to_coords('53190600'), cep_to_coords('55293485'), cep_to_coords('53635605'), cep_to_coords('52280670'), cep_to_coords('55038520'), cep_to_coords('54780360'), cep_to_coords('50875080'), cep_to_coords('55816440'), cep_to_coords('54740710'), cep_to_coords('50980615'), cep_to_coords('50920180'), cep_to_coords('51011440'), cep_to_coords('52080130'), cep_to_coords('50640570'), cep_to_coords('55156530'), cep_to_coords('55155700'), cep_to_coords('53090470'), cep_to_coords('52070650'), cep_to_coords('50761700'), cep_to_coords('50090540'), cep_to_coords('53530790'), cep_to_coords('52240480'), cep_to_coords('05551090'), cep_to_coords('55045025'), cep_to_coords('55038315'), cep_to_coords('52061061'), cep_to_coords('50741490'), cep_to_coords('55155400'), cep_to_coords('55008590'), cep_to_coords('56509350'), cep_to_coords('55813170'), cep_to_coords('51180483'), cep_to_coords('54727200'), cep_to_coords('56506500'), cep_to_coords('56508170'), cep_to_coords('50940280'), cep_to_coords('56510420'), cep_to_coords('50080761'), cep_to_coords('53413325'), cep_to_coords('51260100'), cep_to_coords('56318040'), cep_to_coords('52061300'), cep_to_coords('54786360'), cep_to_coords('53110260'), cep_to_coords('55006045'), cep_to_coords('55292725'), cep_to_coords('55292720'), cep_to_coords('54768790'), cep_to_coords('54410315'), cep_to_coords('54515447'), cep_to_coords('48902310'), cep_to_coords('50711350'), cep_to_coords('54220380'), cep_to_coords('50091230'), cep_to_coords('54515405'), cep_to_coords('53530610'), cep_to_coords('50210240'), cep_to_coords('56509510'), cep_to_coords('52006010'), cep_to_coords('50730285'), cep_to_coords('50830100'), cep_to_coords('52120160'), cep_to_coords('52120560'), cep_to_coords('53444020'), cep_to_coords('53421350'), cep_to_coords('50610050'), cep_to_coords('54777410'), cep_to_coords('53180051'), cep_to_coords('30060580'), cep_to_coords('51150310'), cep_to_coords('55024070'), cep_to_coords('52056070'), cep_to_coords('52110051'), cep_to_coords('51190610'), cep_to_coords('50730220'), cep_to_coords('51001040'), cep_to_coords('54210081'), cep_to_coords('55038410'), cep_to_coords('54759200'), cep_to_coords('53330140'), cep_to_coords('52280600'), cep_to_coords('51260060'), cep_to_coords('53630033'), cep_to_coords('54756030'), cep_to_coords('55297210'), cep_to_coords('55295240'), cep_to_coords('55604150'), cep_to_coords('54220235'), cep_to_coords('56330120'), cep_to_coords('54420470'), cep_to_coords('54490355'), cep_to_coords('55110000'), cep_to_coords('50620590'), cep_to_coords('54786040'), cep_to_coords('50730230'), cep_to_coords('56950999'), cep_to_coords('54100403'), cep_to_coords('51310020'), cep_to_coords('51240100'), cep_to_coords('50670590'), cep_to_coords('56323830'), cep_to_coords('55006002'), cep_to_coords('55012482'), cep_to_coords('55036545'), cep_to_coords('55031412'), cep_to_coords('50690725'), cep_to_coords('50192310'), cep_to_coords('50690545'), cep_to_coords('53150050'), cep_to_coords('50100310'), cep_to_coords('50610501'), cep_to_coords('50630140'), cep_to_coords('50920830'), cep_to_coords('50860060'), cep_to_coords('53429760'), cep_to_coords('50870710'), cep_to_coords('50870005'), cep_to_coords('51110070'), cep_to_coords('51260380'), cep_to_coords('50860160'), cep_to_coords('54767840'), cep_to_coords('53270325'), cep_to_coords('50050170'), cep_to_coords('54100252'), cep_to_coords('55014445'), cep_to_coords('53320465'), cep_to_coords('54220600'), cep_to_coords('53240371'), cep_to_coords('50711210'), cep_to_coords('51160030'), cep_to_coords('56912186'), cep_to_coords('55010260'), cep_to_coords('55027200'), cep_to_coords('56328600'), cep_to_coords('50070090'), cep_to_coords('50791041'), cep_to_coords('51340530'), cep_to_coords('51010630'), cep_to_coords('55032200'), cep_to_coords('50930685'), cep_to_coords('50920140'), cep_to_coords('53439595'), cep_to_coords('53404015'), cep_to_coords('54090400'), cep_to_coords('52171285'), cep_to_coords('56507020'), cep_to_coords('55026000'), cep_to_coords('55151715'), cep_to_coords('54220750'), cep_to_coords('52031310'), cep_to_coords('55038805'), cep_to_coords('55026120'), cep_to_coords('50660100'), cep_to_coords('54705142'), cep_to_coords('56519465'), cep_to_coords('18682842'), cep_to_coords('50820460'), cep_to_coords('53401600'), cep_to_coords('54250260'), cep_to_coords('56509725'), cep_to_coords('50731146'), cep_to_coords('56330065'), cep_to_coords('56509530'), cep_to_coords('52130140'), cep_to_coords('50721030'), cep_to_coords('55020530'), cep_to_coords('52190260'), cep_to_coords('53409010'), cep_to_coords('54715010'), cep_to_coords('50860020'), cep_to_coords('54705340'), cep_to_coords('51280330'), cep_to_coords('55028081'), cep_to_coords('55016670'), cep_to_coords('55038275'), cep_to_coords('55031418'), cep_to_coords('54777535'), cep_to_coords('55038610'), cep_to_coords('55004410'), cep_to_coords('54140640'), cep_to_coords('52131031'), cep_to_coords('50610250'), cep_to_coords('56505440'), cep_to_coords('50110370'), cep_to_coords('56312110'), cep_to_coords('55158460'), cep_to_coords('55026410'), cep_to_coords('55695970'), cep_to_coords('54735750'), cep_to_coords('55818595'), cep_to_coords('53170410'), cep_to_coords('53080310'), cep_to_coords('52031241'), cep_to_coords('53990999'), cep_to_coords('50791470'), cep_to_coords('50770820'), cep_to_coords('53441207'), cep_to_coords('54340250'), cep_to_coords('54325170'), cep_to_coords('54160560'), cep_to_coords('50740930'), cep_to_coords('55194275'), cep_to_coords('56306640'), cep_to_coords('53190014'), cep_to_coords('52280434'), cep_to_coords(', 5502036'), cep_to_coords('55608695'), cep_to_coords('55602240'), cep_to_coords('50710345'), cep_to_coords('56320800'), cep_to_coords('50870200'), cep_to_coords('54580780'), cep_to_coords('54759061'), cep_to_coords('53401730'), cep_to_coords('52280526'), cep_to_coords('50680390'), cep_to_coords('50680239'), cep_to_coords('55604013'), cep_to_coords('54100674'), cep_to_coords('54230431'), cep_to_coords('50630720'), cep_to_coords('54767775'), cep_to_coords('56517600'), cep_to_coords('52221372'), cep_to_coords('54490245'), cep_to_coords('55004391'), cep_to_coords('50900500'), cep_to_coords('55168000'), cep_to_coords('50610500'), cep_to_coords('53403485'), cep_to_coords('55152400'), cep_to_coords('52140540'), cep_to_coords('54430280'), cep_to_coords('50970020'), cep_to_coords('53020500'), cep_to_coords('55016590'), cep_to_coords('55157380'), cep_to_coords('54080440'), cep_to_coords('52080400'), cep_to_coords('56504100'), cep_to_coords('54765480'), cep_to_coords('55158780'), cep_to_coords('52131301'), cep_to_coords('54705840'), cep_to_coords('55641185'), cep_to_coords('53120170'), cep_to_coords('56533331'), cep_to_coords('51230380'), cep_to_coords('52140130'), cep_to_coords('51011450'), cep_to_coords('53427250'), cep_to_coords('53025070'), cep_to_coords('53240492'), cep_to_coords('51270140'), cep_to_coords('54470080'), cep_to_coords('54460311'), cep_to_coords('48840000'), cep_to_coords('51111111'), cep_to_coords('53240640'), cep_to_coords('56508160'), cep_to_coords('54774040'), cep_to_coords('52390360'), cep_to_coords('52130204'), cep_to_coords('56323540'), cep_to_coords('56512450'), cep_to_coords('52091040'), cep_to_coords('54735785'), cep_to_coords('55640100'), cep_to_coords('56509240'), cep_to_coords('54580230'), cep_to_coords('51130530'), cep_to_coords('54768750'), cep_to_coords('54765140'), cep_to_coords('51290640'), cep_to_coords('54100650'), cep_to_coords('55813640'), cep_to_coords('52031043'), cep_to_coords('52170300'), cep_to_coords('55608740'), cep_to_coords('55606630'), cep_to_coords('50721350'), cep_to_coords('50980565'), cep_to_coords('53370970'), cep_to_coords('51330320'), cep_to_coords('56328080'), cep_to_coords('56519041'), cep_to_coords('54762050'), cep_to_coords('54756285'), cep_to_coords('55293540'), cep_to_coords('56318575'), cep_to_coords('50811020'), cep_to_coords('50680110'), cep_to_coords('52051145'), cep_to_coords('54530140'), cep_to_coords('54717160'), cep_to_coords('54345142'), cep_to_coords('56909460'), cep_to_coords('53409080'), cep_to_coords('53530530'), cep_to_coords('54771455'), cep_to_coords('51180310'), cep_to_coords('55030320'), cep_to_coords('56312450'), cep_to_coords('51150090'), cep_to_coords('52060335'), cep_to_coords('55036018'), cep_to_coords('54210243'), cep_to_coords('56314190'), cep_to_coords('50780340'), cep_to_coords('55155560'), cep_to_coords('53180290'), cep_to_coords('55295520'), cep_to_coords('54120080'), cep_to_coords('50805120'), cep_to_coords('51071610'), cep_to_coords('51011190'), cep_to_coords('51220040'), cep_to_coords('54786030'), cep_to_coords('53170318'), cep_to_coords('53090000'), cep_to_coords('50060520'), cep_to_coords('53460000'), cep_to_coords('51160270'), cep_to_coords('52080075'), cep_to_coords('55044042'), cep_to_coords('51021304'), cep_to_coords('58390000'), cep_to_coords('54470270'), cep_to_coords('50791520'), cep_to_coords('56330301'), cep_to_coords('50900450'), cep_to_coords('54580639'), cep_to_coords('54735425'), cep_to_coords('56309650'), cep_to_coords('53020020'), cep_to_coords('55023010'), cep_to_coords('50820320'), cep_to_coords('51130390'), cep_to_coords('52111440'), cep_to_coords('52131400'), cep_to_coords('52131370'), cep_to_coords('55710010'), cep_to_coords('50950000'), cep_to_coords('54410380'), cep_to_coords('55606810'), cep_to_coords('55611010'), cep_to_coords('55606620'), cep_to_coords('55608230'), cep_to_coords('55602380'), cep_to_coords('55015320'), cep_to_coords('54140690'), cep_to_coords('55250001'), cep_to_coords('56318220'), cep_to_coords('52010100'), cep_to_coords('55034575'), cep_to_coords('55038185'), cep_to_coords('64753000'), cep_to_coords('50930250'), cep_to_coords('55111000'), cep_to_coords('54320640'), cep_to_coords('52040030'), cep_to_coords('74001970'), cep_to_coords('54100111'), cep_to_coords('54720022'), cep_to_coords('54777155'), cep_to_coords('50213402'), cep_to_coords('54290280'), cep_to_coords('57170110'), cep_to_coords('55026010'), cep_to_coords('55038100'), cep_to_coords('51023013'), cep_to_coords('51275220'), cep_to_coords('55194300'), cep_to_coords('52071331'), cep_to_coords('55037250'), cep_to_coords('54325480'), cep_to_coords('54792250'), cep_to_coords('53350838'), cep_to_coords('50800400'), cep_to_coords('55034520'), cep_to_coords('56515680'), cep_to_coords('56506360'), cep_to_coords('52080300'), cep_to_coords('54470340'), cep_to_coords('51340027'), cep_to_coords('51030200'), cep_to_coords('50770741'), cep_to_coords('54505400'), cep_to_coords('52030420'), cep_to_coords('55604460'), cep_to_coords('51240380'), cep_to_coords('55030012'), cep_to_coords('53620370'), cep_to_coords('54737150'), cep_to_coords('53050276'), cep_to_coords('53370690'), cep_to_coords('53350190'), cep_to_coords('51500000'), cep_to_coords('53040020'), cep_to_coords('56320010'), cep_to_coords('52291150'), cep_to_coords('56517790'), cep_to_coords('27285170'), cep_to_coords('50620220'), cep_to_coords('53510320'), cep_to_coords('55021320'), cep_to_coords('53422530'), cep_to_coords('63500000'), cep_to_coords('51912410'), cep_to_coords('54777452'), cep_to_coords('63024540'), cep_to_coords('56909525'), cep_to_coords('54320290'), cep_to_coords('54325370'), cep_to_coords('53370195'), cep_to_coords('52122000'), cep_to_coords('56328230'), cep_to_coords('52090311'), cep_to_coords('52091030'), cep_to_coords('52031120'), cep_to_coords('50761628'), cep_to_coords('51170150'), cep_to_coords('56318180'), cep_to_coords('55020570'), cep_to_coords('55016752'), cep_to_coords('53290250'), cep_to_coords('55031010'), cep_to_coords('55016450'), cep_to_coords('56330300'), cep_to_coords('56519420'), cep_to_coords('13607258'), cep_to_coords('55293051'), cep_to_coords('56319595'), cep_to_coords('52140080'), cep_to_coords('41710340'), cep_to_coords('53051800'), cep_to_coords('53050180'), cep_to_coords('52090298'), cep_to_coords('53610110'), cep_to_coords('51770270'), cep_to_coords('56304190'), cep_to_coords('54230170'), cep_to_coords('54762760'), cep_to_coords('54345550'), cep_to_coords('50710305'), cep_to_coords('52121142'), cep_to_coords('53040970'), cep_to_coords('54330005'), cep_to_coords('53550710'), cep_to_coords('54735784'), cep_to_coords('50750100'), cep_to_coords('50819220'), cep_to_coords('50710220'), cep_to_coords('55032650'), cep_to_coords('55040280'), cep_to_coords('56316430'), cep_to_coords('53090420'), cep_to_coords('55026291'), cep_to_coords('53630480'), cep_to_coords('50875180'), cep_to_coords('55157520'), cep_to_coords('54345032'), cep_to_coords('51400509'), cep_to_coords('52081510'), cep_to_coords('53435320'), cep_to_coords('54730102'), cep_to_coords('50040900'), cep_to_coords('55014553'), cep_to_coords('53170440'), cep_to_coords('53433330'), cep_to_coords('54140700'), cep_to_coords('53260460'), cep_to_coords('55032600'), cep_to_coords('53400390'), cep_to_coords('53640615'), cep_to_coords('50711515'), cep_to_coords('09340000'), cep_to_coords('55314420'), cep_to_coords('55008570'), cep_to_coords('53270390'), cep_to_coords('52208640'), cep_to_coords('55019126'), cep_to_coords('51150192'), cep_to_coords('50770060'), cep_to_coords('51130080'), cep_to_coords('55014150'), cep_to_coords('54535190'), cep_to_coords('54570000'), cep_to_coords('53130370'), cep_to_coords('55036570'), cep_to_coords('56312593'), cep_to_coords('54510060'), cep_to_coords('52690042'), cep_to_coords('52061317'), cep_to_coords('50110420'), cep_to_coords('52280735'), cep_to_coords('56512040'), cep_to_coords('50730330'), cep_to_coords('50411200'), cep_to_coords('56519140'), cep_to_coords('53431100'), cep_to_coords('53550046'), cep_to_coords('53080690'), cep_to_coords('56316660'), cep_to_coords('56320700'), cep_to_coords('56306390'), cep_to_coords('56330700'), cep_to_coords('56310661'), cep_to_coords('55020200'), cep_to_coords('52081091'), cep_to_coords('52221030'), cep_to_coords('52131381'), cep_to_coords('50760355'), cep_to_coords('52090660'), cep_to_coords('52090051'), cep_to_coords('52171215'), cep_to_coords('20830380'), cep_to_coords('50630420'), cep_to_coords('52071600'), cep_to_coords('50721555'), cep_to_coords('50920610'), cep_to_coords('51070310'), cep_to_coords('51340731'), cep_to_coords('53422100'), cep_to_coords('50790011'), cep_to_coords('53435630'), cep_to_coords('54720191'), cep_to_coords('53441400'), cep_to_coords('50120320'), cep_to_coords('58748000'), cep_to_coords('56322020'), cep_to_coords('52054380'), cep_to_coords('53010160'), cep_to_coords('51260510'), cep_to_coords('51011370'), cep_to_coords('55747420'), cep_to_coords('56312330'), cep_to_coords('55606613'), cep_to_coords('55006230'), cep_to_coords('55040235'), cep_to_coords('54080510'), cep_to_coords('55012002'), cep_to_coords('52061625'), cep_to_coords('51190550'), cep_to_coords('53210330'), cep_to_coords('54360112'), cep_to_coords('54755000'), cep_to_coords('50721730'), cep_to_coords('55038380'), cep_to_coords('55012570'), cep_to_coords('55819370'), cep_to_coords('55044060'), cep_to_coords('55020810'), cep_to_coords('55028600'), cep_to_coords('55040315'), cep_to_coords('55040513'), cep_to_coords('55018625'), cep_to_coords('56332054'), cep_to_coords('55008290'), cep_to_coords('55819295'), cep_to_coords('53437650'), cep_to_coords('54170360'), cep_to_coords('55614065'), cep_to_coords('55614250'), cep_to_coords('55606150'), cep_to_coords('55606570'), cep_to_coords('54100662'), cep_to_coords('56512075'), cep_to_coords('52280745'), cep_to_coords('55016615'), cep_to_coords('56306180'), cep_to_coords('56505190'), cep_to_coords('59500000'), cep_to_coords('53150580'), cep_to_coords('54796274'), cep_to_coords('51011210'), cep_to_coords('54430080'), cep_to_coords('52221290'), cep_to_coords('03665000'), cep_to_coords('53441585'), cep_to_coords('54580795'), cep_to_coords('52390455'), cep_to_coords('56512065'), cep_to_coords('50680420'), cep_to_coords('54150450'), cep_to_coords('55012061'), cep_to_coords('56321430'), cep_to_coords('50800350'), cep_to_coords('55024755'), cep_to_coords('53413210'), cep_to_coords('54720065'), cep_to_coords('56510230'), cep_to_coords('55002250'), cep_to_coords('52081021'), cep_to_coords('51345060'), cep_to_coords('55000030'), cep_to_coords('51270180'), cep_to_coords('13222420'), cep_to_coords('58753000'), cep_to_coords('53060690'), cep_to_coords('50751283'), cep_to_coords('53416190'), cep_to_coords('50711445'), cep_to_coords('56509760'), cep_to_coords('55645683'), cep_to_coords('56310265'), cep_to_coords('54762076'), cep_to_coords('50110557'), cep_to_coords('50790061'), cep_to_coords('50920460'), cep_to_coords('53160170'), cep_to_coords('53413260'), cep_to_coords('55150590'), cep_to_coords('50980535'), cep_to_coords('51345071'), cep_to_coords('52125190'), cep_to_coords('55293210'), cep_to_coords('50070900'), cep_to_coords('55195635'), cep_to_coords('56304130'), cep_to_coords('55608253'), cep_to_coords('55028155'), cep_to_coords('55030582'), cep_to_coords('55016025'), cep_to_coords('55014435'), cep_to_coords('56312660'), cep_to_coords('56330535'), cep_to_coords('55014600'), cep_to_coords('55038190'), cep_to_coords('55038325'), cep_to_coords('52040130'), cep_to_coords('55297300'), cep_to_coords('54767820'), cep_to_coords('54330775'), cep_to_coords('55032460'), cep_to_coords('54330215'), cep_to_coords('54325423'), cep_to_coords('51345380'), cep_to_coords('54325033'), cep_to_coords('53290350'), cep_to_coords('55610160'), cep_to_coords('55608672'), cep_to_coords('60710010'), cep_to_coords('50900210'), cep_to_coords('53422300'), cep_to_coords('54735906'), cep_to_coords('56506190'), cep_to_coords('53510050'), cep_to_coords('53565350'), cep_to_coords('51030320'), cep_to_coords('55022792'), cep_to_coords('55297431'), cep_to_coords('55291400'), cep_to_coords('53439470'), cep_to_coords('53170900'), cep_to_coords('50454706'), cep_to_coords('53415430'), cep_to_coords('50610330'), cep_to_coords('54230042'), cep_to_coords('53540010'), cep_to_coords('54753200'), cep_to_coords('55032270'), cep_to_coords('05518520'), cep_to_coords('52041581'), cep_to_coords('53401240'), cep_to_coords('56506010'), cep_to_coords('52081251'), cep_to_coords('58175000'), cep_to_coords('54768480'), cep_to_coords('51330472'), cep_to_coords('55036138'), cep_to_coords('50670210'), cep_to_coords('54460120'), cep_to_coords('54470060'), cep_to_coords('52081037'), cep_to_coords('53431377'), cep_to_coords('54505250'), cep_to_coords('51330440'), cep_to_coords('50865145'), cep_to_coords('54410210'), cep_to_coords('56318020'), cep_to_coords('54530045'), cep_to_coords('55815270'), cep_to_coords('56502315'), cep_to_coords('53442320'), cep_to_coords('52211090'), cep_to_coords('50630500'), cep_to_coords('52060070'), cep_to_coords('54753600'), cep_to_coords('55012710'), cep_to_coords('56906150'), cep_to_coords('55038665'), cep_to_coords('55020047'), cep_to_coords('55020245'), cep_to_coords('52021381'), cep_to_coords('52031381'), cep_to_coords('55020535'), cep_to_coords('55014055'), cep_to_coords('55024305'), cep_to_coords('55019090'), cep_to_coords('50920530'), cep_to_coords('54160080'), cep_to_coords('51260410'), cep_to_coords('50960400'), cep_to_coords('52490340'), cep_to_coords('54100475'), cep_to_coords('52211160'), cep_to_coords('52280525'), cep_to_coords('50780410'), cep_to_coords('55030290'), cep_to_coords('52031430'), cep_to_coords('55155710'), cep_to_coords('53422010'), cep_to_coords('53409790'), cep_to_coords('54280710'), cep_to_coords('54350450'), cep_to_coords('56519400'), cep_to_coords('59800000'), cep_to_coords('54490221'), cep_to_coords('52270051'), cep_to_coords('55014340'), cep_to_coords('50110717'), cep_to_coords('54350260'), cep_to_coords('53416651'), cep_to_coords('60110140'), cep_to_coords('53210970'), cep_to_coords('55028554'), cep_to_coords('52190121'), cep_to_coords('52041701'), cep_to_coords('50060772'), cep_to_coords('55297320'), cep_to_coords('53040101'), cep_to_coords('53153361'), cep_to_coords('56506120'), cep_to_coords('56509040'), cep_to_coords('54715801'), cep_to_coords('56912593'), cep_to_coords('56906203'), cep_to_coords('52040105'), cep_to_coords('55563000'), cep_to_coords('53030280'), cep_to_coords('56503540'), cep_to_coords('41514363'), cep_to_coords('52280219'), cep_to_coords('53190180'), cep_to_coords('53545160'), cep_to_coords('54765010'), cep_to_coords('53415320'), cep_to_coords('54535320'), cep_to_coords('53510390'), cep_to_coords('53360250'), cep_to_coords('54753690'), cep_to_coords('56504010'), cep_to_coords('56505390'), cep_to_coords('56515430'), cep_to_coords('53520170'), cep_to_coords('53429370'), cep_to_coords('55643370'), cep_to_coords('79590000'), cep_to_coords('50070050'), cep_to_coords('55020508'), cep_to_coords('50090140'), cep_to_coords('50791131'), cep_to_coords('52211255'), cep_to_coords('55014195'), cep_to_coords('56306070'), cep_to_coords('55016700'), cep_to_coords('55024468'), cep_to_coords('55010300'), cep_to_coords('55036555'), cep_to_coords('55042580'), cep_to_coords('53418140'), cep_to_coords('55036163'), cep_to_coords('50790390'), cep_to_coords('52170130'), cep_to_coords('54765100'), cep_to_coords('54753581'), cep_to_coords('55602281'), cep_to_coords('53413720'), cep_to_coords('54090080'), cep_to_coords('54360096'), cep_to_coords('55024640'), cep_to_coords('55006430'), cep_to_coords('51240725'), cep_to_coords('55030240'), cep_to_coords('55038130'), cep_to_coords('55032430'), cep_to_coords('50760226'), cep_to_coords('55036051'), cep_to_coords('54220350'), cep_to_coords('54520120'), cep_to_coords('54720199'), cep_to_coords('55012553'), cep_to_coords('53545020'), cep_to_coords('51150190'), cep_to_coords('56503840'), cep_to_coords('54589150'), cep_to_coords('52210150'), cep_to_coords('51310024'), cep_to_coords('54767130'), cep_to_coords('53560400'), cep_to_coords('52020250'), cep_to_coords('52060520'), cep_to_coords('54315015'), cep_to_coords('50980510'), cep_to_coords('54510105'), cep_to_coords('53403330'), cep_to_coords('51320240'), cep_to_coords('54410281'), cep_to_coords('54230021'), cep_to_coords('54774340'), cep_to_coords('53270686'), cep_to_coords('54170680'), cep_to_coords('53610275'), cep_to_coords('59090590'), cep_to_coords('52041210'), cep_to_coords('54230500'), cep_to_coords('55296590'), cep_to_coords('55294170'), cep_to_coords('55299839'), cep_to_coords('52008053'), cep_to_coords('52070670'), cep_to_coords('52211155'), cep_to_coords('55036240'), cep_to_coords('56308160'), cep_to_coords('55024770'), cep_to_coords('56314390'), cep_to_coords('56320240'), cep_to_coords('54628857'), cep_to_coords('55016290'), cep_to_coords('52011140'), cep_to_coords('50781620'), cep_to_coords('50740221'), cep_to_coords('56320840'), cep_to_coords('52131540'), cep_to_coords('50110390'), cep_to_coords('54220110'), cep_to_coords('50060460'), cep_to_coords('23040150'), cep_to_coords('50940490'), cep_to_coords('55609010'), cep_to_coords('55243605'), cep_to_coords('52041005'), cep_to_coords('54430332'), cep_to_coords('51150140'), cep_to_coords('53420170'), cep_to_coords('52280516'), cep_to_coords('51275000'), cep_to_coords('52070121'), cep_to_coords('54352045'), cep_to_coords('53280100'), cep_to_coords('55157310'), cep_to_coords('53423825'), cep_to_coords('55153060'), cep_to_coords('55158030'), cep_to_coords('55151670'), cep_to_coords('54280722'), cep_to_coords('50760315'), cep_to_coords('54100584'), cep_to_coords('50760545'), cep_to_coords('54280480'), cep_to_coords('54762435'), cep_to_coords('50620560'), cep_to_coords('56312131'), cep_to_coords('52081460'), cep_to_coords('51335220'), cep_to_coords('53041725'), cep_to_coords('53330270'), cep_to_coords('55295590'), cep_to_coords('52081100'), cep_to_coords('55295290'), cep_to_coords('50060130'), cep_to_coords('50740230'), cep_to_coords('53270261'), cep_to_coords('50050909'), cep_to_coords('56505400'), cep_to_coords('56503800'), cep_to_coords('53421825'), cep_to_coords('54510550'), cep_to_coords('54250225'), cep_to_coords('54535310'), cep_to_coords('55024580'), cep_to_coords('51290410'), cep_to_coords('50960460'), cep_to_coords('54730260'), cep_to_coords('56512315'), cep_to_coords('55012200'), cep_to_coords('52041470'), cep_to_coords('50110520'), cep_to_coords('55297260'), cep_to_coords('53401310'), cep_to_coords('53585355'), cep_to_coords('51190160'), cep_to_coords('55014532'), cep_to_coords('50980490'), cep_to_coords('55811040'), cep_to_coords('54440270'), cep_to_coords('53120260'), cep_to_coords('52280042'), cep_to_coords('55036200'), cep_to_coords('09171630'), cep_to_coords('50900570'), cep_to_coords('52081580'), cep_to_coords('53630516'), cep_to_coords('54723040'), cep_to_coords('50680140'), cep_to_coords('54070250'), cep_to_coords('50940100'), cep_to_coords('54735700'), cep_to_coords('55398972'), cep_to_coords('53170012'), cep_to_coords('50770970'), cep_to_coords('54340102'), cep_to_coords('54762421'), cep_to_coords('55890970'), cep_to_coords('54762415'), cep_to_coords('54774625'), cep_to_coords('56329816'), cep_to_coords('53413010'), cep_to_coords('53413165'), cep_to_coords('52111613'), cep_to_coords('54783375'), cep_to_coords('50060585'), cep_to_coords('51310290'), cep_to_coords('51250570'), cep_to_coords('51190351'), cep_to_coords('55297680'), cep_to_coords('05678000'), cep_to_coords('51270680'), cep_to_coords('55297180'), cep_to_coords('52091351'), cep_to_coords('52160220'), cep_to_coords('52111100'), cep_to_coords('52030590'), cep_to_coords('52090140'), cep_to_coords('51130260'), cep_to_coords('50920630'), cep_to_coords('54530420'), cep_to_coords('55155060'), cep_to_coords('52160825'), cep_to_coords('50630810'), cep_to_coords('50721321'), cep_to_coords('52031460'), cep_to_coords('51260694'), cep_to_coords('52041605'), cep_to_coords('55150190'), cep_to_coords('54737080 |'), cep_to_coords('55014705'), cep_to_coords('50721790'), cep_to_coords('53170794'), cep_to_coords('53170790'), cep_to_coords('50701014'), cep_to_coords('55295270'), cep_to_coords('50781721'), cep_to_coords('50920755'), cep_to_coords('50090370'), cep_to_coords('51220270'), cep_to_coords('53431355'), cep_to_coords('51350171'), cep_to_coords('53160370'), cep_to_coords('53435130'), cep_to_coords('53320350'), cep_to_coords('54340785'), cep_to_coords('51130280'), cep_to_coords('568000000'), cep_to_coords('54710130'), cep_to_coords('55609715'), cep_to_coords('50830400'), cep_to_coords('56308240'), cep_to_coords('51150185'), cep_to_coords('50690470'), cep_to_coords('50781745'), cep_to_coords('53570450'), cep_to_coords('54774585'), cep_to_coords('50610380'), cep_to_coords('54762638'), cep_to_coords('54353200'), cep_to_coords('53605420'), cep_to_coords('48904083'), cep_to_coords('52120373'), cep_to_coords('54420515'), cep_to_coords('52171255'), cep_to_coords('52070512'), cep_to_coords('50680640'), cep_to_coords('55293010'), cep_to_coords('56909190'), cep_to_coords('54786660'), cep_to_coords('52211330'), cep_to_coords('50900420'), cep_to_coords('55872500'), cep_to_coords('56310040'), cep_to_coords('54352265'), cep_to_coords('50100010'), cep_to_coords('50680760'), cep_to_coords('50810410'), cep_to_coords('51240070'), cep_to_coords('53290270'), cep_to_coords('52280410'), cep_to_coords('56312171'), cep_to_coords('55153595'), cep_to_coords('52041531'), cep_to_coords('56328165'), cep_to_coords('56302765'), cep_to_coords('54380193'), cep_to_coords('53545150'), cep_to_coords('56360304'), cep_to_coords('54737030'), cep_to_coords('56321640'), cep_to_coords('54205021'), cep_to_coords('50650150'), cep_to_coords('53530775'), cep_to_coords('52280490'), cep_to_coords('55155170'), cep_to_coords('55008266'), cep_to_coords('55034650'), cep_to_coords('55036171'), cep_to_coords('55036375'), cep_to_coords('55036713'), cep_to_coords('55010600'), cep_to_coords('55032325'), cep_to_coords('50680240'), cep_to_coords('54520540'), cep_to_coords('54280785'), cep_to_coords('50630245'), cep_to_coords('54210270'), cep_to_coords('35195000'), cep_to_coords('54745370'), cep_to_coords('53330201'), cep_to_coords('53580030'), cep_to_coords('52080015'), cep_to_coords('52291271'), cep_to_coords('52081610'), cep_to_coords('52140501'), cep_to_coords('52490005'), cep_to_coords('51090730'), cep_to_coords('55296563'), cep_to_coords('56519490'), cep_to_coords('52081615'), cep_to_coords('50720158'), cep_to_coords('50350350'), cep_to_coords('56505480'), cep_to_coords('50020200'), cep_to_coords('51160080'), cep_to_coords('54365210'), cep_to_coords('53250441'), cep_to_coords('56511170'), cep_to_coords('50730685'), cep_to_coords('54810460'), cep_to_coords('54780050'), cep_to_coords('55294695'), cep_to_coords('54410001'), cep_to_coords('56503745'), cep_to_coords('56517100'), cep_to_coords('55032340'), cep_to_coords('48010970'), cep_to_coords('52060485'), cep_to_coords('53110421'), cep_to_coords('56517755'), cep_to_coords('50856112'), cep_to_coords('50690300'), cep_to_coords('51345210'), cep_to_coords('55816310'), cep_to_coords('54330330'), cep_to_coords('55031430'), cep_to_coords('55016760'), cep_to_coords('55813180'), cep_to_coords('55815020'), cep_to_coords('52160100'), cep_to_coords('52080077'), cep_to_coords('55295390'), cep_to_coords('56318635'), cep_to_coords('54740720'), cep_to_coords('53210320'), cep_to_coords('55610020'), cep_to_coords('55612330'), cep_to_coords('51340020'), cep_to_coords('51190090'), cep_to_coords('53515530'), cep_to_coords('55044104'), cep_to_coords('54320317'), cep_to_coords('54735120'), cep_to_coords('54580530'), cep_to_coords('54580637'), cep_to_coords('56314350'), cep_to_coords('52111560'), cep_to_coords('51130470'), cep_to_coords('55022570'), cep_to_coords('55060180'), cep_to_coords('55028255'), cep_to_coords('55024157'), cep_to_coords('55012240'), cep_to_coords('55016410'), cep_to_coords('54070080'), cep_to_coords('55030153'), cep_to_coords('55018170'), cep_to_coords('54768768'), cep_to_coords('55819270'), cep_to_coords('56511030'), cep_to_coords('56906455'), cep_to_coords('54240080'), cep_to_coords('56507325'), cep_to_coords('55299848'), cep_to_coords('52221259'), cep_to_coords('50070540'), cep_to_coords('53090760'), cep_to_coords('56308001'), cep_to_coords('55010630'), cep_to_coords('54517060'), cep_to_coords('50640150'), cep_to_coords('50940310'), cep_to_coords('55814040'), cep_to_coords('52061045'), cep_to_coords('54756630'), cep_to_coords('53407620'), cep_to_coords('53405260'), cep_to_coords('52040280'), cep_to_coords('53421560'), cep_to_coords('55024550'), cep_to_coords('82120012'), cep_to_coords('54220460'), cep_to_coords('53090710'), cep_to_coords('50020021'), cep_to_coords('51131410'), cep_to_coords('52090150'), cep_to_coords('55038240'), cep_to_coords('55021280'), cep_to_coords('55036760'), cep_to_coords('55108000'), cep_to_coords('55038045'), cep_to_coords('55014672'), cep_to_coords('55016750'), cep_to_coords('56320825'), cep_to_coords('56332514'), cep_to_coords('56314320'), cep_to_coords('56332600'), cep_to_coords('56306280'), cep_to_coords('56309420'), cep_to_coords('56302500'), cep_to_coords('56306130'), cep_to_coords('55019225'), cep_to_coords('50850180'), cep_to_coords('56330280'), cep_to_coords('54715220'), cep_to_coords('50875015'), cep_to_coords('53090510'), cep_to_coords('55037240'), cep_to_coords('50970000'), cep_to_coords('50731222'), cep_to_coords('50810130'), cep_to_coords('50720570'), cep_to_coords('54705283'), cep_to_coords('54759025'), cep_to_coords('54753779'), cep_to_coords('54762155'), cep_to_coords('52060340'), cep_to_coords('55610083'), cep_to_coords('55154525'), cep_to_coords('55152230'), cep_to_coords('52111480'), cep_to_coords('51300020'), cep_to_coords('55292141'), cep_to_coords('55299000'), cep_to_coords('55294738'), cep_to_coords('50610280'), cep_to_coords('55020415'), cep_to_coords('54515515'), cep_to_coords('55158810'), cep_to_coords('56310110'), cep_to_coords('56332379'), cep_to_coords('56330160'), cep_to_coords('56332000'), cep_to_coords('55036310'), cep_to_coords('56328450'), cep_to_coords('56320680'), cep_to_coords('25290000'), cep_to_coords('33296518'), cep_to_coords('54320601'), cep_to_coords('56313500'), cep_to_coords('56306220'), cep_to_coords('56304230'), cep_to_coords('51023103'), cep_to_coords('05436080'), cep_to_coords('56302280'), cep_to_coords('44630000'), cep_to_coords('56304060'), cep_to_coords('55295560'), cep_to_coords('50751421'), cep_to_coords('50751425'), cep_to_coords('54505330'), cep_to_coords('54280402'), cep_to_coords('50800000'), cep_to_coords('53545120'), cep_to_coords('53350450'), cep_to_coords('56510280'), cep_to_coords('51320190'), cep_to_coords('54705130'), cep_to_coords('54120160'), cep_to_coords('54150090'), cep_to_coords('54330815'), cep_to_coords('53520115'), cep_to_coords('53230610'), cep_to_coords('55024310'), cep_to_coords('50540340'), cep_to_coords('53220110'), cep_to_coords('53409710'), cep_to_coords('53050272'), cep_to_coords('52721430'), cep_to_coords('52280550'), cep_to_coords('52070590'), cep_to_coords('56322600'), cep_to_coords('49280000'), cep_to_coords('54335800'), cep_to_coords('56504005'), cep_to_coords('56304090'), cep_to_coords('52080370'), cep_to_coords('54240341'), cep_to_coords('54580437'), cep_to_coords('56332710'), cep_to_coords('53625080'), cep_to_coords('56306440'), cep_to_coords('52120715'), cep_to_coords('50720250'), cep_to_coords('54410514'), cep_to_coords('50710315'), cep_to_coords('50710432'), cep_to_coords('51270111'), cep_to_coords('50900530'), cep_to_coords('54330175'), cep_to_coords('50110155'), cep_to_coords('53407760'), cep_to_coords('56326290'), cep_to_coords('56323000'), cep_to_coords('50060720'), cep_to_coords('52090415'), cep_to_coords('52091350'), cep_to_coords('54507113'), cep_to_coords('55004300'), cep_to_coords('55040040'), cep_to_coords('55027370'), cep_to_coords('56328653'), cep_to_coords('56331230'), cep_to_coords('56310320'), cep_to_coords('56306190'), cep_to_coords('56312440'), cep_to_coords('56330585'), cep_to_coords('54240170'), cep_to_coords('56310240'), cep_to_coords('52095565'), cep_to_coords('52121095'), cep_to_coords('53610455'), cep_to_coords('55012560'), cep_to_coords('55290004'), cep_to_coords('51180062'), cep_to_coords('54753410'), cep_to_coords('52090160'), cep_to_coords('56316000'), cep_to_coords('54580225'), cep_to_coords('54520150'), cep_to_coords('54515015'), cep_to_coords('54590 000'), cep_to_coords('51011580'), cep_to_coords('53525720'), cep_to_coords('53350550'), cep_to_coords('56302330'), cep_to_coords('54505290'), cep_to_coords('54330254'), cep_to_coords('50850500'), cep_to_coords('54737770'), cep_to_coords('55292530'), cep_to_coords('52091535'), cep_to_coords('53429450'), cep_to_coords('52190510'), cep_to_coords('13560710'), cep_to_coords('51250580'), cep_to_coords('13575380'), cep_to_coords('50791360'), cep_to_coords('50810190'), cep_to_coords('54580590'), cep_to_coords('54580030'), cep_to_coords('52120120'), cep_to_coords('54315570'), cep_to_coords('55292020'), cep_to_coords('54250305'), cep_to_coords('56320740'), cep_to_coords('56320786'), cep_to_coords('53020070'), cep_to_coords('53290330'), cep_to_coords('53070045'), cep_to_coords('50010310'), cep_to_coords('54766075'), cep_to_coords('56505280'), cep_to_coords('54310150'), cep_to_coords('50860760'), cep_to_coords('53431440'), cep_to_coords('54400350'), cep_to_coords('54320500'), cep_to_coords('51250380'), cep_to_coords('51220060'), cep_to_coords('54580335'), cep_to_coords('51190010'), cep_to_coords('53540000'), cep_to_coords('54410705'), cep_to_coords('53417703'), cep_to_coords('51260140'), cep_to_coords('54090437'), cep_to_coords('55020600'), cep_to_coords('54230071'), cep_to_coords('50040110'), cep_to_coords('55038630'), cep_to_coords('50070105'), cep_to_coords('52230410'), cep_to_coords('56517750'), cep_to_coords('52130490'), cep_to_coords('53412775'), cep_to_coords('53402775'), cep_to_coords('54240755'), cep_to_coords('54767321'), cep_to_coords('53409360'), cep_to_coords('54325337'), cep_to_coords('52110146'), cep_to_coords('53320030'), cep_to_coords('54325380'), cep_to_coords('54635330'), cep_to_coords('54120053'), cep_to_coords('50233386'), cep_to_coords('53625090'), cep_to_coords('51090900'), cep_to_coords('53370365'), cep_to_coords('55036300'), cep_to_coords('50515105'), cep_to_coords('50870250'), cep_to_coords('55034020'), cep_to_coords('54300302'), cep_to_coords('52070002'), cep_to_coords('53110591'), cep_to_coords('55612060'), cep_to_coords('50080045'), cep_to_coords('55020165'), cep_to_coords('56906321'), cep_to_coords('50690600'), cep_to_coords('56620000'), cep_to_coords('56950970'), cep_to_coords('53441540'), cep_to_coords('50870185'), cep_to_coords('54290016'), cep_to_coords('50650420'), cep_to_coords('54325372'), cep_to_coords('52061081'), cep_to_coords('54589750'), cep_to_coords('55012160'), cep_to_coords('55012600'), cep_to_coords('55018605'), cep_to_coords('51030460'), cep_to_coords('52050350'), cep_to_coords('55293260'), cep_to_coords('82050190'), cep_to_coords('53620675'), cep_to_coords('50920290'), cep_to_coords('54330365'), cep_to_coords('56503660'), cep_to_coords('54786220'), cep_to_coords('55564000'), cep_to_coords('55006030'), cep_to_coords('55034250'), cep_to_coords('54705090'), cep_to_coords('50730300'), cep_to_coords('51290280'), cep_to_coords('51010620'), cep_to_coords('54823023'), cep_to_coords('56328903'), cep_to_coords('56509360'), cep_to_coords('52041542'), cep_to_coords('53407410'), cep_to_coords('54340440'), cep_to_coords('54344000'), cep_to_coords('55012255'), cep_to_coords('70862540'), cep_to_coords('56306090'), cep_to_coords('50751150'), cep_to_coords('56510240'), cep_to_coords('50090290'), cep_to_coords('53250500'), cep_to_coords('52390020'), cep_to_coords('55022560'), cep_to_coords('63010420'), cep_to_coords('54765390'), cep_to_coords('52280045'), cep_to_coords('53220550'), cep_to_coords('55020185'), cep_to_coords('52090043'), cep_to_coords('50870020'), cep_to_coords('55004011'), cep_to_coords('22010060'), cep_to_coords('54380365'), cep_to_coords('52070430'), cep_to_coords('52121450'), cep_to_coords('55296310'), cep_to_coords('51170550'), cep_to_coords('53437010'), cep_to_coords('58345078'), cep_to_coords('53700970'), cep_to_coords('54430270'), cep_to_coords('54100180'), cep_to_coords('53580350'), cep_to_coords('56605490'), cep_to_coords('55299537'), cep_to_coords('55296034'), cep_to_coords('55296210'), cep_to_coords('54767730'), cep_to_coords('32040050'), cep_to_coords('56507130'), cep_to_coords('50940380'), cep_to_coords('50900510'), cep_to_coords('50850260'), cep_to_coords('53070480'), cep_to_coords('51345490'), cep_to_coords('50920410'), cep_to_coords('54340790'), cep_to_coords('55640013'), cep_to_coords('55020041'), cep_to_coords('55002070'), cep_to_coords('55002071'), cep_to_coords('53320540'), cep_to_coords('54735170'), cep_to_coords('53150720'), cep_to_coords('56304560'), cep_to_coords('56312245'), cep_to_coords('54310825'), cep_to_coords('55022164'), cep_to_coords('51180610'), cep_to_coords('55295100'), cep_to_coords('56322040'), cep_to_coords('54430400'), cep_to_coords('54280400'), cep_to_coords('51260340'), cep_to_coords('51260490'), cep_to_coords('52121385'), cep_to_coords('51320620'), cep_to_coords('55150120'), cep_to_coords('52081031'), cep_to_coords('50761302'), cep_to_coords('55610250'), cep_to_coords('52071091'), cep_to_coords('55296070'), cep_to_coords('56322520'), cep_to_coords('50900620'), cep_to_coords('54737060'), cep_to_coords('51110220'), cep_to_coords('55294140'), cep_to_coords('54762570'), cep_to_coords('56100260'), cep_to_coords('51010200'), cep_to_coords('52091019'), cep_to_coords('51260500'), cep_to_coords('53545660'), cep_to_coords('50790235'), cep_to_coords('54620520'), cep_to_coords('52050790'), cep_to_coords('53320450'), cep_to_coords('54330260'), cep_to_coords('54270220'), cep_to_coords('55195602'), cep_to_coords('56332320'), cep_to_coords('50820950'), cep_to_coords('50870680'), cep_to_coords('52081690'), cep_to_coords('53370801'), cep_to_coords('54774645'), cep_to_coords('50868050'), cep_to_coords('51030205'), cep_to_coords('51230200'), cep_to_coords('52211430'), cep_to_coords('54756105'), cep_to_coords('55195815'), cep_to_coords('59625130'), cep_to_coords('55012300'), cep_to_coords('50820510'), cep_to_coords('54705790'), cep_to_coords('53433720'), cep_to_coords('54730220'), cep_to_coords('50810310'), cep_to_coords('50721330'), cep_to_coords('53265627'), cep_to_coords('51190680'), cep_to_coords('55192425'), cep_to_coords('50760335'), cep_to_coords('50640610'), cep_to_coords('50070065'), cep_to_coords('50760237'), cep_to_coords('53403590'), cep_to_coords('53436670'), cep_to_coords('53435475'), cep_to_coords('53110130'), cep_to_coords('54753480'), cep_to_coords('52120253'), cep_to_coords('50820450'), cep_to_coords('52071240'), cep_to_coords('55816460'), cep_to_coords('55031020'), cep_to_coords('02132000'), cep_to_coords('54520040'), cep_to_coords('54400010'), cep_to_coords('55016315'), cep_to_coords('55023180'), cep_to_coords('55604240'), cep_to_coords('55606190'), cep_to_coords('52040221'), cep_to_coords('50100320'), cep_to_coords('52031370'), cep_to_coords('53437195'), cep_to_coords('53421221'), cep_to_coords('55023200'), cep_to_coords('50050425'), cep_to_coords('53090570'), cep_to_coords('54750666'), cep_to_coords('50790510'), cep_to_coords('51330000'), cep_to_coords('54460610'), cep_to_coords('52131676'), cep_to_coords('54490064'), cep_to_coords('51345605'), cep_to_coords('54705141'), cep_to_coords('55642600'), cep_to_coords('53230380'), cep_to_coords('51280450'), cep_to_coords('54210100'), cep_to_coords('54315085'), cep_to_coords('55291100'), cep_to_coords('54470230'), cep_to_coords('56509550'), cep_to_coords('56506375'), cep_to_coords('56310230'), cep_to_coords('54765060'), cep_to_coords('55022705'), cep_to_coords('55043220'), cep_to_coords('54720243'), cep_to_coords('51150500'), cep_to_coords('50650010'), cep_to_coords('53407110'), cep_to_coords('35158115'), cep_to_coords('52110520'), cep_to_coords('55014654'), cep_to_coords('50980200'), cep_to_coords('51160140'), cep_to_coords('53423440'), cep_to_coords('53520000'), cep_to_coords('56302380'), cep_to_coords('50870510'), cep_to_coords('53230570'), cep_to_coords('51011280'), cep_to_coords('52031400'), cep_to_coords('53110120'), cep_to_coords('50790565'), cep_to_coords('50129039'), cep_to_coords('56308220'), cep_to_coords('51290313'), cep_to_coords('52090450'), cep_to_coords('50730500'), cep_to_coords('50760350'), cep_to_coords('54766060'), cep_to_coords('52280390'), cep_to_coords('55814210'), cep_to_coords('54765170'), cep_to_coords('54765250'), cep_to_coords('32340200'), cep_to_coords('56103235'), cep_to_coords('50751430'), cep_to_coords('54100400'), cep_to_coords('50771775'), cep_to_coords('55036130'), cep_to_coords('52051190'), cep_to_coords('50604345'), cep_to_coords('53435020'), cep_to_coords('53030210'), cep_to_coords('50660030'), cep_to_coords('52010030'), cep_to_coords('53409530'), cep_to_coords('23409135'), cep_to_coords('52050330'), cep_to_coords('56312520'), cep_to_coords('55294540'), cep_to_coords('52081310'), cep_to_coords('54090544'), cep_to_coords('51430170'), cep_to_coords('50790605'), cep_to_coords('54510180'), cep_to_coords('50050310'), cep_to_coords('52210140'), cep_to_coords('51346110'), cep_to_coords('54220660'), cep_to_coords('50680585'), cep_to_coords('52110155'), cep_to_coords('54210170'), cep_to_coords('50830490'), cep_to_coords('53140110'), cep_to_coords('52125140'), cep_to_coords('52121410'), cep_to_coords('53031000'), cep_to_coords('52211070'), cep_to_coords('56326007'), cep_to_coords('53298340'), cep_to_coords('54325390'), cep_to_coords('50970215'), cep_to_coords('50721770'), cep_to_coords('53160040'), cep_to_coords('55291740'), cep_to_coords('50701557'), cep_to_coords('50791557'), cep_to_coords('54460290'), cep_to_coords('50940220'), cep_to_coords('69917748'), cep_to_coords('50473410'), cep_to_coords('53130630'), cep_to_coords('54330027'), cep_to_coords('53417340'), cep_to_coords('56314540'), cep_to_coords('56332145'), cep_to_coords('51345190'), cep_to_coords('53421412'), cep_to_coords('53439270'), cep_to_coords('55602381'), cep_to_coords('52390420'), cep_to_coords('54720220'), cep_to_coords('55022090'), cep_to_coords('56313600'), cep_to_coords('52081655'), cep_to_coords('53150600'), cep_to_coords('50760700'), cep_to_coords('56502285'), cep_to_coords('50640350'), cep_to_coords('50690705'), cep_to_coords('53439570'), cep_to_coords('51330560'), cep_to_coords('51330020'), cep_to_coords('54515070'), cep_to_coords('56507335'), cep_to_coords('52210430'), cep_to_coords('55740970'), cep_to_coords('55036305'), cep_to_coords('52131690'), cep_to_coords('50620530'), cep_to_coords('55044090'), cep_to_coords('55012025'), cep_to_coords('55023130'), cep_to_coords('55012380'), cep_to_coords('55010101'), cep_to_coords('55014768'), cep_to_coords('55014200'), cep_to_coords('52041400'), cep_to_coords('53010140'), cep_to_coords('52110590'), cep_to_coords('53401070'), cep_to_coords('51270010'), cep_to_coords('55018757'), cep_to_coords('50900320'), cep_to_coords('50751310'), cep_to_coords('52052110'), cep_to_coords('50721540'), cep_to_coords('53421660'), cep_to_coords('81021010'), cep_to_coords('51033440'), cep_to_coords('52081122'), cep_to_coords('54230271'), cep_to_coords('52060282'), cep_to_coords('52091092'), cep_to_coords('50860140'), cep_to_coords('54325450'), cep_to_coords('53545650'), cep_to_coords('52090785'), cep_to_coords('53300160'), cep_to_coords('53230100'), cep_to_coords('53170030'), cep_to_coords('50670420'), cep_to_coords('53240438'), cep_to_coords('50920300'), cep_to_coords('53110611'), cep_to_coords('53550725'), cep_to_coords('52191375'), cep_to_coords('53140090'), cep_to_coords('52410015'), cep_to_coords('55608625'), cep_to_coords('55608626'), cep_to_coords('53040330'), cep_to_coords('50850150'), cep_to_coords('52071060'), cep_to_coords('50810330'), cep_to_coords('50102301'), cep_to_coords('53035600'), cep_to_coords('53417690'), cep_to_coords('54325580'), cep_to_coords('51250440'), cep_to_coords('52221092'), cep_to_coords('54360106'), cep_to_coords('52050600'), cep_to_coords('50780070'), cep_to_coords('50050590'), cep_to_coords('55813630'), cep_to_coords('54510050'), cep_to_coords('54580408'), cep_to_coords('55038150'), cep_to_coords('55810410'), cep_to_coords('55642170'), cep_to_coords('50130120'), cep_to_coords('50730470'), cep_to_coords('52080646'), cep_to_coords('52090020'), cep_to_coords('53645345'), cep_to_coords('54530040'), cep_to_coords('55292045'), cep_to_coords('55920045'), cep_to_coords('55291679'), cep_to_coords('53370360'), cep_to_coords('53240439'), cep_to_coords('56312351'), cep_to_coords('53080331'), cep_to_coords('54780210'), cep_to_coords('55192651'), cep_to_coords('50648125'), cep_to_coords('54325550'), cep_to_coords('53435611'), cep_to_coords('54325498'), cep_to_coords('50761900'), cep_to_coords('54520155'), cep_to_coords('54715330'), cep_to_coords('53425590'), cep_to_coords('54325225'), cep_to_coords('55020152'), cep_to_coords('56330025'), cep_to_coords('54230201'), cep_to_coords('54495406'), cep_to_coords('53080010'), cep_to_coords('54325195'), cep_to_coords('52051042'), cep_to_coords('54460060'), cep_to_coords('50920390'), cep_to_coords('56502318'), cep_to_coords('55641025'), cep_to_coords('56912158'), cep_to_coords('52111413'), cep_to_coords('54520590'), cep_to_coords('52131013'), cep_to_coords('52070502'), cep_to_coords('53610263'), cep_to_coords('55016530'), cep_to_coords('54330460'), cep_to_coords('54410600'), cep_to_coords('54250543'), cep_to_coords('53444411'), cep_to_coords('55018205'), cep_to_coords('55002500'), cep_to_coords('50080430'), cep_to_coords('55145971'), cep_to_coords('50771320'), cep_to_coords('55296290'), cep_to_coords('55299528'), cep_to_coords('55190714'), cep_to_coords('55008115'), cep_to_coords('55022540'), cep_to_coords('55019120'), cep_to_coords('50110525'), cep_to_coords('53020440'), cep_to_coords('54330024'), cep_to_coords('53417550'), cep_to_coords('52080070'), cep_to_coords('53290000'), cep_to_coords('53421440'), cep_to_coords('52091421'), cep_to_coords('53120515'), cep_to_coords('52010430'), cep_to_coords('52031280'), cep_to_coords('54410524'), cep_to_coords('54330253'), cep_to_coords('50012301'), cep_to_coords('54510140'), cep_to_coords('54589005'), cep_to_coords('54730250'), cep_to_coords('51350590'), cep_to_coords('50780060'), cep_to_coords('59139123'), cep_to_coords('54759465'), cep_to_coords('54420640'), cep_to_coords('55299535'), cep_to_coords('55291200'), cep_to_coords('52081603'), cep_to_coords('50960000'), cep_to_coords('55154055'), cep_to_coords('53260000'), cep_to_coords('50610420'), cep_to_coords('50751160'), cep_to_coords('64600000'), cep_to_coords('54705212'), cep_to_coords('53620433'), cep_to_coords('54753260'), cep_to_coords('56504110'), cep_to_coords('54740670'), cep_to_coords('53130460'), cep_to_coords('53030240'), cep_to_coords('50020068'), cep_to_coords('50090380'), cep_to_coords('56306690'), cep_to_coords('53070170'), cep_to_coords('53240060'), cep_to_coords('50780240'), cep_to_coords('55043000'), cep_to_coords('53433730'), cep_to_coords('54790000'), cep_to_coords('54789530'), cep_to_coords('53200350'), cep_to_coords('54430020'), cep_to_coords('51140290'), cep_to_coords('53220370'), cep_to_coords('53421431'), cep_to_coords('54330385'), cep_to_coords('50920515'), cep_to_coords('50060510'), cep_to_coords('54535040'), cep_to_coords('50090220'), cep_to_coords('54720682'), cep_to_coords('53441650'), cep_to_coords('54210535'), cep_to_coords('53090280'), cep_to_coords('53240171'), cep_to_coords('51030410'), cep_to_coords('56912550'), cep_to_coords('52061150'), cep_to_coords('56115665'), cep_to_coords('51150254'), cep_to_coords('54365400'), cep_to_coords('50960200'), cep_to_coords('50090640'), cep_to_coords('56312760'), cep_to_coords('51260150'), cep_to_coords('51170080'), cep_to_coords('50720225'), cep_to_coords('54230135'), cep_to_coords('52211635'), cep_to_coords('53419700'), cep_to_coords('53810250'), cep_to_coords('51071132'), cep_to_coords('51010300'), cep_to_coords('53530650'), cep_to_coords('50320700'), cep_to_coords('54400520'), cep_to_coords('50740530'), cep_to_coords('50791380'), cep_to_coords('53415500'), cep_to_coords('55027290'), cep_to_coords('62670000'), cep_to_coords('55294590'), cep_to_coords('53625656'), cep_to_coords('55294130'), cep_to_coords('56512260'), cep_to_coords('51011130'), cep_to_coords('51260170'), cep_to_coords('55027150'), cep_to_coords('50620350'), cep_to_coords('51920000'), cep_to_coords('53409055'), cep_to_coords('54430450'), cep_to_coords('52131030'), cep_to_coords('50690655'), cep_to_coords('54759065'), cep_to_coords('55020110'), cep_to_coords('53060529'), cep_to_coords('53030140'), cep_to_coords('53635753'), cep_to_coords('50791011'), cep_to_coords('52439430'), cep_to_coords('53610256'), cep_to_coords('51110140'), cep_to_coords('56314470'), cep_to_coords('53370240'), cep_to_coords('53413903'), cep_to_coords('50791330'), cep_to_coords('55293055'), cep_to_coords('50980100'), cep_to_coords('52121300'), cep_to_coords('56507285'), cep_to_coords('53407480'), cep_to_coords('50811340'), cep_to_coords('52061190'), cep_to_coords('11701240'), cep_to_coords('54515535'), cep_to_coords('20741430'), cep_to_coords('50640030'), cep_to_coords('53433200'), cep_to_coords('53520171'), cep_to_coords('54789500'), cep_to_coords('55604381'), cep_to_coords('52090123'), cep_to_coords('52071095'), cep_to_coords('52302100'), cep_to_coords('50060905'), cep_to_coords('50010927'), cep_to_coords('53230600'), cep_to_coords('52131622'), cep_to_coords('54330183'), cep_to_coords('55036235'), cep_to_coords('50030010'), cep_to_coords('54320261'), cep_to_coords('55019240'), cep_to_coords('55024170'), cep_to_coords('55024370'), cep_to_coords('52291140'), cep_to_coords('53444320'), cep_to_coords('53372022'), cep_to_coords('54370220'), cep_to_coords('53421251'), cep_to_coords('53401010'), cep_to_coords('54410610'), cep_to_coords('56309175'), cep_to_coords('54740545'), cep_to_coords('50790580'), cep_to_coords('53220810'), cep_to_coords('51110230'), cep_to_coords('54580595'), cep_to_coords('56302160'), cep_to_coords('53021010'), cep_to_coords('52221090'), cep_to_coords('56306425'), cep_to_coords('55155370'), cep_to_coords('55154615'), cep_to_coords('55153020'), cep_to_coords('53560175'), cep_to_coords('54330305'), cep_to_coords('51203103'), cep_to_coords('50781825'), cep_to_coords('51320560'), cep_to_coords('53330370'), cep_to_coords('56310655'), cep_to_coords('52020038'), cep_to_coords('50620340'), cep_to_coords('56321190'), cep_to_coords('56332440'), cep_to_coords('55296288'), cep_to_coords('51170520'), cep_to_coords('55292201'), cep_to_coords('55292585'), cep_to_coords('55194121'), cep_to_coords('53320480'), cep_to_coords('55299525'), cep_to_coords('53150650'), cep_to_coords('54352075'), cep_to_coords('50110310'), cep_to_coords('53430040'), cep_to_coords('55608780'), cep_to_coords('55612380'), cep_to_coords('53612386'), cep_to_coords('54589400'), cep_to_coords('55060000'), cep_to_coords('53417300'), cep_to_coords('55020266'), cep_to_coords('50820640'), cep_to_coords('50730260'), cep_to_coords('50721190'), cep_to_coords('52081193'), cep_to_coords('54505251'), cep_to_coords('56512570'), cep_to_coords('55038740'), cep_to_coords('51350280'), cep_to_coords('51335280'), cep_to_coords('56302515'), cep_to_coords('50711030'), cep_to_coords('54440495'), cep_to_coords('17730000'), cep_to_coords('53610405'), cep_to_coords('55900971'), cep_to_coords('04124150'), cep_to_coords('50720320'), cep_to_coords('55818635'), cep_to_coords('51275310'), cep_to_coords('54762026'), cep_to_coords('53425040'), cep_to_coords('52280051'), cep_to_coords('55012150'), cep_to_coords('51020720'), cep_to_coords('55030430'), cep_to_coords('55008530'), cep_to_coords('55027600'), cep_to_coords('51240270'), cep_to_coords('52210280')


# In[47]:


print(coordenadasrow10426to15425)


# In[48]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in row10426to15425.tolist():
    result.append(''.join(pattern.findall(item)))


# In[49]:


print(result)


# In[50]:


dfrow10426to15425 = pd.DataFrame(coordenadasrow10426to15425, result)


# In[51]:


dfrow10426to15425.reset_index(level=0, inplace=True)


# In[52]:


dfrow10426to15425 = dfrow10426to15425.rename(columns={'index':'cep'})


# In[59]:


bancoesusalltabsrais2019nodupsCEPS[['id']][10426:15426]


# In[60]:


id10426to15425 = bancoesusalltabsrais2019nodupsCEPS[['id']][10426:15426]


# In[61]:


id10426to15425.reset_index(level=0,inplace=True)


# In[62]:


id10426to15425


# In[63]:


dfrow10426to15425['id'] = id10426to15425['id']
dfrow10426to15425['index'] = id10426to15425['index']


# In[67]:


dfrow10426to15425


# In[70]:


dfrow10426to15425[dfrow10426to15425.columns[[4,3,0,1,2]]]


# In[71]:


dfrow10426to15425 = dfrow10426to15425[dfrow10426to15425.columns[[4,3,0,1,2]]]


# In[72]:


dfrow10426to15425


# In[73]:


dfrow10426to15425.to_excel('dfrow10426to15425latlong.xlsx')


# # bancoesusalltabsrais2019nodupsCEPS[15426:20426]

# In[75]:


bancoesusalltabsrais2019nodupsCEPS[15426:20426]


# In[76]:


row15426to20425 = bancoesusalltabsrais2019nodupsCEPS[15426:20426]


# In[77]:


row15426to20425.update("cep_to_coords('" + row15426to20425[['cep']].astype(str) + "'),")
print(row15426to20425)


# In[78]:


row15426to20425 = row15426to20425.loc[:,'cep']


# In[79]:


row15426to20425


# In[80]:


print(' '.join(row15426to20425))


# In[81]:


coordenadasrow15426to20425 = cep_to_coords('55040090'), cep_to_coords('56310740'), cep_to_coords('55606240'), cep_to_coords('556000000'), cep_to_coords('52211790'), cep_to_coords('53422240'), cep_to_coords('54768425'), cep_to_coords('51150420'), cep_to_coords('55158820'), cep_to_coords('53421430'), cep_to_coords('53012301'), cep_to_coords('50030200'), cep_to_coords('51121350'), cep_to_coords('54410322'), cep_to_coords('54410790'), cep_to_coords('54140350'), cep_to_coords('54470160'), cep_to_coords('56915035'), cep_to_coords('53270015'), cep_to_coords('69057120'), cep_to_coords('53370350'), cep_to_coords('51350230'), cep_to_coords('53560120'), cep_to_coords('53540160'), cep_to_coords('55034320'), cep_to_coords('54290031'), cep_to_coords('51170030'), cep_to_coords('55008970'), cep_to_coords('54290080'), cep_to_coords('50850060'), cep_to_coords('52080081'), cep_to_coords('56506090'), cep_to_coords('53370540'), cep_to_coords('50820260'), cep_to_coords('51230465'), cep_to_coords('54525243'), cep_to_coords('55813310'), cep_to_coords('51011653'), cep_to_coords('55551500'), cep_to_coords('56503132'), cep_to_coords('56506430'), cep_to_coords('51345140'), cep_to_coords('51345710'), cep_to_coords('50791473'), cep_to_coords('50920580'), cep_to_coords('54520580'), cep_to_coords('55612370'), cep_to_coords('55614390'), cep_to_coords('55817210'), cep_to_coords('53550596'), cep_to_coords('51320550'), cep_to_coords('56302350'), cep_to_coords('54720480'), cep_to_coords('53415390'), cep_to_coords('53040190'), cep_to_coords('52000010'), cep_to_coords('48905430'), cep_to_coords('56316818'), cep_to_coords('55641762'), cep_to_coords('52171190'), cep_to_coords('53435120'), cep_to_coords('53654136'), cep_to_coords('54100571'), cep_to_coords('53417561'), cep_to_coords('53230500'), cep_to_coords('52120195'), cep_to_coords('50950970'), cep_to_coords('56000640'), cep_to_coords('04011033'), cep_to_coords('53433110'), cep_to_coords('50910510'), cep_to_coords('54730194'), cep_to_coords('56320820'), cep_to_coords('54735220'), cep_to_coords('53230050'), cep_to_coords('55036225'), cep_to_coords('52061310'), cep_to_coords('53030130'), cep_to_coords('55038208'), cep_to_coords('53300350'), cep_to_coords('52140520'), cep_to_coords('55291060'), cep_to_coords('54315380'), cep_to_coords('55157530'), cep_to_coords('54580840'), cep_to_coords('54440160'), cep_to_coords('50820150'), cep_to_coords('50335350'), cep_to_coords('50751115'), cep_to_coords('55163000'), cep_to_coords('54230015'), cep_to_coords('54283330'), cep_to_coords('54290061'), cep_to_coords('50870610'), cep_to_coords('51190690'), cep_to_coords('55294160'), cep_to_coords('53437495'), cep_to_coords('55296512'), cep_to_coords('55157020'), cep_to_coords('56306100'), cep_to_coords('54120210'), cep_to_coords('14120210'), cep_to_coords('53620470'), cep_to_coords('53610530'), cep_to_coords('55643071'), cep_to_coords('51170510'), cep_to_coords('52280143'), cep_to_coords('51310420'), cep_to_coords('52080340'), cep_to_coords('54510370'), cep_to_coords('55817670'), cep_to_coords('55813415'), cep_to_coords('50900290'), cep_to_coords('53417687'), cep_to_coords('51012360'), cep_to_coords('53403505'), cep_to_coords('51020400'), cep_to_coords('53510970'), cep_to_coords('56360357'), cep_to_coords('50800390'), cep_to_coords('50751084'), cep_to_coords('53140070'), cep_to_coords('52211420'), cep_to_coords('50900440'), cep_to_coords('20200010'), cep_to_coords('55219000'), cep_to_coords('55002210'), cep_to_coords('54774650'), cep_to_coords('54330395'), cep_to_coords('50810495'), cep_to_coords('50740685'), cep_to_coords('50760790'), cep_to_coords('53423460'), cep_to_coords('52191720'), cep_to_coords('53580620'), cep_to_coords('55292290'), cep_to_coords('52211202'), cep_to_coords('08761450'), cep_to_coords('50110064'), cep_to_coords('51010270'), cep_to_coords('54310322'), cep_to_coords('53423000'), cep_to_coords('53423290'), cep_to_coords('53407650'), cep_to_coords('54260430'), cep_to_coords('54315091'), cep_to_coords('52130300'), cep_to_coords('52071080'), cep_to_coords('52191340'), cep_to_coords('50771727'), cep_to_coords('55813820'), cep_to_coords('53429440'), cep_to_coords('50630030'), cep_to_coords('52280651'), cep_to_coords('54340020'), cep_to_coords('55043010'), cep_to_coords('55008475'), cep_to_coords('41110200'), cep_to_coords('51150050'), cep_to_coords('55153645'), cep_to_coords('54460611'), cep_to_coords('55155730'), cep_to_coords('54520390'), cep_to_coords('55154015'), cep_to_coords('52171425'), cep_to_coords('51230170'), cep_to_coords('54460340'), cep_to_coords('55152440'), cep_to_coords('54110170'), cep_to_coords('52091041'), cep_to_coords('53360340'), cep_to_coords('53090400'), cep_to_coords('55294050'), cep_to_coords('54330397'), cep_to_coords('55295395'), cep_to_coords('55290395'), cep_to_coords('50940170'), cep_to_coords('52081570'), cep_to_coords('45913020'), cep_to_coords('53565560'), cep_to_coords('51350420'), cep_to_coords('50740320'), cep_to_coords('54762065'), cep_to_coords('50740420'), cep_to_coords('54080140'), cep_to_coords('54170580'), cep_to_coords('52125130'), cep_to_coords('54745820'), cep_to_coords('51290440'), cep_to_coords('53170310'), cep_to_coords('50989270'), cep_to_coords('52280224'), cep_to_coords('53600420'), cep_to_coords('50740426'), cep_to_coords('52280141'), cep_to_coords('50171170'), cep_to_coords('53714725'), cep_to_coords('53433565'), cep_to_coords('53050100'), cep_to_coords('53060760'), cep_to_coords('54171170'), cep_to_coords('53645270'), cep_to_coords('50010290'), cep_to_coords('52211025'), cep_to_coords('54230270'), cep_to_coords('55016640'), cep_to_coords('53170510'), cep_to_coords('52140135'), cep_to_coords('54070140'), cep_to_coords('53630030'), cep_to_coords('05434060'), cep_to_coords('50771360'), cep_to_coords('50810470'), cep_to_coords('52130570'), cep_to_coords('53413660'), cep_to_coords('52120281'), cep_to_coords('54315340'), cep_to_coords('56513011'), cep_to_coords('55026170'), cep_to_coords('55817120'), cep_to_coords('55818535'), cep_to_coords('56322735'), cep_to_coords('44435000'), cep_to_coords('55020341'), cep_to_coords('55020502'), cep_to_coords('55020518'), cep_to_coords('55020830'), cep_to_coords('56318240'), cep_to_coords('53402610'), cep_to_coords('55641130'), cep_to_coords('54762684'), cep_to_coords('54580815'), cep_to_coords('54350080'), cep_to_coords('53290090'), cep_to_coords('54519090'), cep_to_coords('55294717'), cep_to_coords('50830280'), cep_to_coords('55291160'), cep_to_coords('53605500'), cep_to_coords('55293280'), cep_to_coords('53415307'), cep_to_coords('53401074'), cep_to_coords('56512110'), cep_to_coords('55296110'), cep_to_coords('54210571'), cep_to_coords('50050300'), cep_to_coords('51260216'), cep_to_coords('53560155'), cep_to_coords('55642420'), cep_to_coords('56326000'), cep_to_coords('52081526'), cep_to_coords('56510508'), cep_to_coords('50021140'), cep_to_coords('50070700'), cep_to_coords('50729290'), cep_to_coords('50720295'), cep_to_coords('50900250'), cep_to_coords('50791392'), cep_to_coords('52081368'), cep_to_coords('53610230'), cep_to_coords('53427625'), cep_to_coords('53290410'), cep_to_coords('53290102'), cep_to_coords('53421000'), cep_to_coords('54315081'), cep_to_coords('54450100'), cep_to_coords('54310210'), cep_to_coords('53423710'), cep_to_coords('51335067'), cep_to_coords('52020120'), cep_to_coords('51310331'), cep_to_coords('54230172'), cep_to_coords('55294325'), cep_to_coords('53570400'), cep_to_coords('53620625'), cep_to_coords('54310423'), cep_to_coords('52150185'), cep_to_coords('53409738'), cep_to_coords('54490360'), cep_to_coords('54753145'), cep_to_coords('55644609'), cep_to_coords('52041410'), cep_to_coords('51200210'), cep_to_coords('53491460'), cep_to_coords('56318450'), cep_to_coords('53427590'), cep_to_coords('53417490'), cep_to_coords('53401441'), cep_to_coords('53180260'), cep_to_coords('55030220'), cep_to_coords('54353430'), cep_to_coords('55102000'), cep_to_coords('55018122'), cep_to_coords('53070430'), cep_to_coords('51190490'), cep_to_coords('52130400'), cep_to_coords('53401160'), cep_to_coords('53439813'), cep_to_coords('55155470'), cep_to_coords('53620461'), cep_to_coords('53610417'), cep_to_coords('53180305'), cep_to_coords('50040370'), cep_to_coords('53550664'), cep_to_coords('23050180'), cep_to_coords('54360107'), cep_to_coords('07853030'), cep_to_coords('55292061'), cep_to_coords('56509520'), cep_to_coords('52280032'), cep_to_coords('56512101'), cep_to_coords('50800240'), cep_to_coords('53442180'), cep_to_coords('35072066'), cep_to_coords('54310345'), cep_to_coords('54325252'), cep_to_coords('50020150'), cep_to_coords('50670110'), cep_to_coords('50940090'), cep_to_coords('50912031'), cep_to_coords('54446028'), cep_to_coords('55816630'), cep_to_coords('55024340'), cep_to_coords('55028180'), cep_to_coords('50721020'), cep_to_coords('51170210'), cep_to_coords('54220200'), cep_to_coords('50660200'), cep_to_coords('05187430'), cep_to_coords('50780160'), cep_to_coords('54350250'), cep_to_coords('53610305'), cep_to_coords('54280410'), cep_to_coords('53433360'), cep_to_coords('02032030'), cep_to_coords('54762078'), cep_to_coords('56309620'), cep_to_coords('53010490'), cep_to_coords('52130148'), cep_to_coords('52041375'), cep_to_coords('54240560'), cep_to_coords('53605030'), cep_to_coords('53220710'), cep_to_coords('55819230'), cep_to_coords('54720235'), cep_to_coords('55610040'), cep_to_coords('56312640'), cep_to_coords('54450300'), cep_to_coords('54320350'), cep_to_coords('54220352'), cep_to_coords('54220410'), cep_to_coords('63250000'), cep_to_coords('28915400'), cep_to_coords('54352035'), cep_to_coords('56332595'), cep_to_coords('55400999'), cep_to_coords('51190710'), cep_to_coords('52041085'), cep_to_coords('50620330'), cep_to_coords('50760830'), cep_to_coords('56517770'), cep_to_coords('54345570'), cep_to_coords('52020200'), cep_to_coords('52050080'), cep_to_coords('55016090'), cep_to_coords('55124460'), cep_to_coords('55024760'), cep_to_coords('55106500'), cep_to_coords('55612090'), cep_to_coords('56320715'), cep_to_coords('56332495'), cep_to_coords('50191290'), cep_to_coords('56318350'), cep_to_coords('90538595'), cep_to_coords('51190739'), cep_to_coords('50090520'), cep_to_coords('55155414'), cep_to_coords('50830330'), cep_to_coords('56512685'), cep_to_coords('55293190'), cep_to_coords('55294210'), cep_to_coords('52021031'), cep_to_coords('53402050'), cep_to_coords('53442070'), cep_to_coords('54210536'), cep_to_coords('51240520'), cep_to_coords('52131281'), cep_to_coords('53431110'), cep_to_coords('56509842'), cep_to_coords('52091273'), cep_to_coords('52110190'), cep_to_coords('55014190'), cep_to_coords('48900195'), cep_to_coords('53180170'), cep_to_coords('53170180'), cep_to_coords('52020222'), cep_to_coords('54315275'), cep_to_coords('53020410'), cep_to_coords('50060050'), cep_to_coords('51030050'), cep_to_coords('53110650'), cep_to_coords('53545090'), cep_to_coords('52060145'), cep_to_coords('51110250'), cep_to_coords('52280385'), cep_to_coords('53170130'), cep_to_coords('53635040'), cep_to_coords('52130575'), cep_to_coords('53409195'), cep_to_coords('54353355'), cep_to_coords('56515500'), cep_to_coords('54735830'), cep_to_coords('53417040'), cep_to_coords('50640620'), cep_to_coords('50721557'), cep_to_coords('52041521'), cep_to_coords('52081075'), cep_to_coords('54505390'), cep_to_coords('54774595'), cep_to_coords('54517150'), cep_to_coords('50720220'), cep_to_coords('55816405'), cep_to_coords('53427260'), cep_to_coords('52090069'), cep_to_coords('54330500'), cep_to_coords('55299384'), cep_to_coords('53510496'), cep_to_coords('53403320'), cep_to_coords('53403250'), cep_to_coords('53403150'), cep_to_coords('55299411'), cep_to_coords('51345091'), cep_to_coords('54745050'), cep_to_coords('56912182'), cep_to_coords('54280340'), cep_to_coords('52081390'), cep_to_coords('50860130'), cep_to_coords('59535000'), cep_to_coords('53080422'), cep_to_coords('55819710'), cep_to_coords('54580385'), cep_to_coords('54220590'), cep_to_coords('54090410'), cep_to_coords('54589295'), cep_to_coords('55602620'), cep_to_coords('55606175'), cep_to_coords('55614702'), cep_to_coords('50680470'), cep_to_coords('53630732'), cep_to_coords('55819765'), cep_to_coords('53080510'), cep_to_coords('55355970'), cep_to_coords('51350220'), cep_to_coords('56309810'), cep_to_coords('54759110'), cep_to_coords('50011660'), cep_to_coords('50610080'), cep_to_coords('51220160'), cep_to_coords('83707554'), cep_to_coords('54759100'), cep_to_coords('52071244'), cep_to_coords('55030120'), cep_to_coords('55021035'), cep_to_coords('53421361'), cep_to_coords('53130380'), cep_to_coords('24220020'), cep_to_coords('52165450'), cep_to_coords('52070462'), cep_to_coords('50930370'), cep_to_coords('54767420'), cep_to_coords('54420610'), cep_to_coords('53170013'), cep_to_coords('54220349'), cep_to_coords('52211780'), cep_to_coords('55291641'), cep_to_coords('55298040'), cep_to_coords('55014335'), cep_to_coords('55158580'), cep_to_coords('53620436'), cep_to_coords('55293184'), cep_to_coords('55296464'), cep_to_coords('54720275'), cep_to_coords('51280380'), cep_to_coords('52160400'), cep_to_coords('53409510'), cep_to_coords('50610700'), cep_to_coords('56332018'), cep_to_coords('56313310'), cep_to_coords('55012760'), cep_to_coords('53321265'), cep_to_coords('52081036'), cep_to_coords('50750190'), cep_to_coords('55038206'), cep_to_coords('54745824'), cep_to_coords('55031060'), cep_to_coords('50711170'), cep_to_coords('55292357'), cep_to_coords('53422400'), cep_to_coords('53435180'), cep_to_coords('52070280'), cep_to_coords('51160010'), cep_to_coords('53180450'), cep_to_coords('53405720'), cep_to_coords('55026040'), cep_to_coords('50711025'), cep_to_coords('51030500'), cep_to_coords('54444350'), cep_to_coords('50640270'), cep_to_coords('51250220'), cep_to_coords('50741300'), cep_to_coords('53080677'), cep_to_coords('53220451'), cep_to_coords('54517240'), cep_to_coords('54510020'), cep_to_coords('54540020'), cep_to_coords('54510401'), cep_to_coords('54540401'), cep_to_coords('54535270'), cep_to_coords('54535350'), cep_to_coords('52031023'), cep_to_coords('52130391'), cep_to_coords('51340145'), cep_to_coords('52050175'), cep_to_coords('51130560'), cep_to_coords('53439760'), cep_to_coords('53370155'), cep_to_coords('52126300'), cep_to_coords('50711380'), cep_to_coords('55014390'), cep_to_coords('50791080'), cep_to_coords('55006060'), cep_to_coords('50900430'), cep_to_coords('54320670'), cep_to_coords('53150040'), cep_to_coords('53402300'), cep_to_coords('55292335'), cep_to_coords('55036465'), cep_to_coords('54410085'), cep_to_coords('54740310'), cep_to_coords('54589415'), cep_to_coords('55291690'), cep_to_coords('52020390'), cep_to_coords('50630150'), cep_to_coords('53510380'), cep_to_coords('53443090'), cep_to_coords('50771490'), cep_to_coords('52030130'), cep_to_coords('52041740'), cep_to_coords('53435760'), cep_to_coords('52210270'), cep_to_coords('50900050'), cep_to_coords('54220225'), cep_to_coords('54315530'), cep_to_coords('54315270'), cep_to_coords('50123021'), cep_to_coords('52700000'), cep_to_coords('54140010'), cep_to_coords('53280190'), cep_to_coords('50790090'), cep_to_coords('55020030'), cep_to_coords('51275620'), cep_to_coords('53220011'), cep_to_coords('53160162'), cep_to_coords('53270211'), cep_to_coords('53403365'), cep_to_coords('52141040'), cep_to_coords('02323730'), cep_to_coords('56509210'), cep_to_coords('52111511'), cep_to_coords('54430224'), cep_to_coords('51030430'), cep_to_coords('52210060'), cep_to_coords('53040160'), cep_to_coords('54310360'), cep_to_coords('50050410'), cep_to_coords('53110410'), cep_to_coords('54080970'), cep_to_coords('54120560'), cep_to_coords('54589015'), cep_to_coords('34000500'), cep_to_coords('55038305'), cep_to_coords('49800000'), cep_to_coords('54329160'), cep_to_coords('51230675'), cep_to_coords('51340095'), cep_to_coords('50930190'), cep_to_coords('50920340'), cep_to_coords('54440106'), cep_to_coords('52160300'), cep_to_coords('55608415'), cep_to_coords('55608030'), cep_to_coords('55018531'), cep_to_coords('52091291'), cep_to_coords('54535400'), cep_to_coords('54320550'), cep_to_coords('52090102'), cep_to_coords('55031416'), cep_to_coords('63560000'), cep_to_coords('56332650'), cep_to_coords('51240765'), cep_to_coords('50020490'), cep_to_coords('51320080'), cep_to_coords('50970460'), cep_to_coords('50761182'), cep_to_coords('51310160'), cep_to_coords('52165040'), cep_to_coords('50660250'), cep_to_coords('50690410'), cep_to_coords('50730510'), cep_to_coords('54230151'), cep_to_coords('54340706'), cep_to_coords('53405355'), cep_to_coords('55158230'), cep_to_coords('55157040'), cep_to_coords('55155680'), cep_to_coords('55040080'), cep_to_coords('54767415'), cep_to_coords('53525150'), cep_to_coords('53565120'), cep_to_coords('50720123'), cep_to_coords('87998026'), cep_to_coords('56328710'), cep_to_coords('56330575'), cep_to_coords('51260261'), cep_to_coords('55295600'), cep_to_coords('55818160'), cep_to_coords('59990000'), cep_to_coords('55295115'), cep_to_coords('53409755'), cep_to_coords('50630255'), cep_to_coords('19200000'), cep_to_coords('51031580'), cep_to_coords('53640230'), cep_to_coords('54080450'), cep_to_coords('54380060'), cep_to_coords('54510030'), cep_to_coords('53605055'), cep_to_coords('54759745'), cep_to_coords('52190200'), cep_to_coords('52165010'), cep_to_coords('53421120'), cep_to_coords('53409245'), cep_to_coords('53423550'), cep_to_coords('50650380'), cep_to_coords('53439803'), cep_to_coords('53431340'), cep_to_coords('53436900'), cep_to_coords('53407100'), cep_to_coords('53403740'), cep_to_coords('53270110'), cep_to_coords('53180211'), cep_to_coords('53160240'), cep_to_coords('56331050'), cep_to_coords('55814090'), cep_to_coords('51250030'), cep_to_coords('55298230'), cep_to_coords('55296090'), cep_to_coords('53530460'), cep_to_coords('55027120'), cep_to_coords('52191160'), cep_to_coords('52160115'), cep_to_coords('55010150'), cep_to_coords('53431590'), cep_to_coords('53421071'), cep_to_coords('54762497'), cep_to_coords('56322745'), cep_to_coords('56510080'), cep_to_coords('52280521'), cep_to_coords('51290010'), cep_to_coords('56310730'), cep_to_coords('55032530'), cep_to_coords('53060510'), cep_to_coords('53417684'), cep_to_coords('52120900'), cep_to_coords('56328755'), cep_to_coords('55036090'), cep_to_coords('56328530'), cep_to_coords('56323210'), cep_to_coords('56322440'), cep_to_coords('51230635'), cep_to_coords('55020520'), cep_to_coords('52140290'), cep_to_coords('54230111'), cep_to_coords('54765475'), cep_to_coords('54786240'), cep_to_coords('53270500'), cep_to_coords('51170380'), cep_to_coords('50110620'), cep_to_coords('50690480'), cep_to_coords('50612410'), cep_to_coords('52150050'), cep_to_coords('56504070'), cep_to_coords('53290290'), cep_to_coords('53360200'), cep_to_coords('53360000'), cep_to_coords('53422410'), cep_to_coords('52211640'), cep_to_coords('53431790'), cep_to_coords('05112120'), cep_to_coords('53610733'), cep_to_coords('54710650'), cep_to_coords('56328520'), cep_to_coords('50761265'), cep_to_coords('53439060'), cep_to_coords('53401610'), cep_to_coords('53437370'), cep_to_coords('53416120'), cep_to_coords('53433120'), cep_to_coords('53290280'), cep_to_coords('52570145'), cep_to_coords('53427060'), cep_to_coords('53413780'), cep_to_coords('55825975'), cep_to_coords('55020765'), cep_to_coords('55194408'), cep_to_coords('53441120'), cep_to_coords('54789460'), cep_to_coords('52041070'), cep_to_coords('50710210'), cep_to_coords('56511260'), cep_to_coords('53435410'), cep_to_coords('54525100'), cep_to_coords('56308260'), cep_to_coords('51230130'), cep_to_coords('53409181'), cep_to_coords('56316290'), cep_to_coords('56330580'), cep_to_coords('54080032'), cep_to_coords('52140380'), cep_to_coords('53240761'), cep_to_coords('53010381'), cep_to_coords('50980465'), cep_to_coords('50060315'), cep_to_coords('53150070'), cep_to_coords('56316696'), cep_to_coords('56304480'), cep_to_coords('54230230'), cep_to_coords('50781291'), cep_to_coords('54756770'), cep_to_coords('52130350'), cep_to_coords('52160990'), cep_to_coords('51340270'), cep_to_coords('53160730'), cep_to_coords('50100380'), cep_to_coords('53441480'), cep_to_coords('55024743'), cep_to_coords('55016310'), cep_to_coords('56317090'), cep_to_coords('56328075'), cep_to_coords('58758000'), cep_to_coords('56316460'), cep_to_coords('56308280'), cep_to_coords('56312550'), cep_to_coords('50690060'), cep_to_coords('54762425'), cep_to_coords('52011100'), cep_to_coords('55609150'), cep_to_coords('51300190'), cep_to_coords('52121470'), cep_to_coords('06329180'), cep_to_coords('55008550'), cep_to_coords('54170660'), cep_to_coords('54280646'), cep_to_coords('55602580'), cep_to_coords('53413230'), cep_to_coords('53560550'), cep_to_coords('52140310'), cep_to_coords('53560690'), cep_to_coords('55293340'), cep_to_coords('53150060'), cep_to_coords('53090780'), cep_to_coords('53020111'), cep_to_coords('56310020'), cep_to_coords('53637205'), cep_to_coords('50090710'), cep_to_coords('50910440'), cep_to_coords('54332572'), cep_to_coords('53360010'), cep_to_coords('52071431'), cep_to_coords('55034140'), cep_to_coords('52090620'), cep_to_coords('54229150'), cep_to_coords('54160280'), cep_to_coords('55602540'), cep_to_coords('55022270'), cep_to_coords('56302270'), cep_to_coords('53560220'), cep_to_coords('53409304'), cep_to_coords('59309840'), cep_to_coords('51230400'), cep_to_coords('54735100'), cep_to_coords('51290615'), cep_to_coords('51024370'), cep_to_coords('50731510'), cep_to_coords('55296755'), cep_to_coords('54759196'), cep_to_coords('52124063'), cep_to_coords('54280289'), cep_to_coords('50730170'), cep_to_coords('50750340'), cep_to_coords('51110270'), cep_to_coords('51280124'), cep_to_coords('56505105'), cep_to_coords('56508222'), cep_to_coords('56509785'), cep_to_coords('54280725'), cep_to_coords('56509045'), cep_to_coords('53422420'), cep_to_coords('53415305'), cep_to_coords('53425540'), cep_to_coords('53220340'), cep_to_coords('53060572'), cep_to_coords('51080090'), cep_to_coords('54720023'), cep_to_coords('54762615'), cep_to_coords('50040170'), cep_to_coords('50770380'), cep_to_coords('53405081'), cep_to_coords('52280613'), cep_to_coords('50791290'), cep_to_coords('55192075'), cep_to_coords('53421520'), cep_to_coords('51160460'), cep_to_coords('51340460'), cep_to_coords('54150097'), cep_to_coords('53893879'), cep_to_coords('53425605'), cep_to_coords('53431315'), cep_to_coords('53530486'), cep_to_coords('55544000'), cep_to_coords('55004440'), cep_to_coords('53110050'), cep_to_coords('50920540'), cep_to_coords('56440999'), cep_to_coords('53350205'), cep_to_coords('53020461'), cep_to_coords('54090546'), cep_to_coords('54200235'), cep_to_coords('53423600'), cep_to_coords('53429245'), cep_to_coords('51300451'), cep_to_coords('55840970'), cep_to_coords('56509840'), cep_to_coords('56906020'), cep_to_coords('53190785'), cep_to_coords('53060470'), cep_to_coords('53545110'), cep_to_coords('53402510'), cep_to_coords('54315070'), cep_to_coords('53409560'), cep_to_coords('55019130'), cep_to_coords('55022650'), cep_to_coords('54470150'), cep_to_coords('54360140'), cep_to_coords('54320007'), cep_to_coords('55819735'), cep_to_coords('54325771'), cep_to_coords('54340180'), cep_to_coords('55038680'), cep_to_coords('54495185'), cep_to_coords('53520100'), cep_to_coords('53621740'), cep_to_coords('51030765'), cep_to_coords('55292580'), cep_to_coords('55296540'), cep_to_coords('55296544'), cep_to_coords('53070280'), cep_to_coords('52291690'), cep_to_coords('54400240'), cep_to_coords('53423350'), cep_to_coords('53360480'), cep_to_coords('53431710'), cep_to_coords('53401510'), cep_to_coords('53416202'), cep_to_coords('53025120'), cep_to_coords('53180435'), cep_to_coords('53407700'), cep_to_coords('50920725'), cep_to_coords('51270350'), cep_to_coords('53401338'), cep_to_coords('52070513'), cep_to_coords('55898000'), cep_to_coords('53520530'), cep_to_coords('51230330'), cep_to_coords('59038094'), cep_to_coords('53423837'), cep_to_coords('54230423'), cep_to_coords('53422451'), cep_to_coords('50740345'), cep_to_coords('55151705'), cep_to_coords('54589899'), cep_to_coords('54786110'), cep_to_coords('52081240'), cep_to_coords('50110320'), cep_to_coords('54735805'), cep_to_coords('53250150'), cep_to_coords('52090041'), cep_to_coords('53420090'), cep_to_coords('52280180'), cep_to_coords('25689689'), cep_to_coords('53520190'), cep_to_coords('53520203'), cep_to_coords('55095120'), cep_to_coords('54789180'), cep_to_coords('52490060'), cep_to_coords('54300091'), cep_to_coords('54280440'), cep_to_coords('53421035'), cep_to_coords('05217040'), cep_to_coords('50060220'), cep_to_coords('52041200'), cep_to_coords('50820440'), cep_to_coords('52280413'), cep_to_coords('20680030'), cep_to_coords('50120420'), cep_to_coords('53110660'), cep_to_coords('53330000'), cep_to_coords('50610490'), cep_to_coords('51340310'), cep_to_coords('52130265'), cep_to_coords('55014162'), cep_to_coords('54310610'), cep_to_coords('54400610'), cep_to_coords('53610205'), cep_to_coords('54789770'), cep_to_coords('54495435'), cep_to_coords('54589050'), cep_to_coords('54520520'), cep_to_coords('54340515'), cep_to_coords('55614103'), cep_to_coords('54495320'), cep_to_coords('50800140'), cep_to_coords('50920655'), cep_to_coords('54410155'), cep_to_coords('55155650'), cep_to_coords('11895286'), cep_to_coords('51609290'), cep_to_coords('56512500'), cep_to_coords('50850190'), cep_to_coords('50760495'), cep_to_coords('53401270'), cep_to_coords('41641140'), cep_to_coords('53401095'), cep_to_coords('53620255'), cep_to_coords('53409736'), cep_to_coords('53545600'), cep_to_coords('55155280'), cep_to_coords('55154025'), cep_to_coords('55294858'), cep_to_coords('54896632'), cep_to_coords('54020540'), cep_to_coords('54040010'), cep_to_coords('50010360'), cep_to_coords('51275080'), cep_to_coords('52091520'), cep_to_coords('52171580'), cep_to_coords('52171280'), cep_to_coords('53000370'), cep_to_coords('56319390'), cep_to_coords('52080101'), cep_to_coords('51190340'), cep_to_coords('53444210'), cep_to_coords('20050150'), cep_to_coords('54737160'), cep_to_coords('51011652'), cep_to_coords('56306310'), cep_to_coords('53535450'), cep_to_coords('54420172'), cep_to_coords('54767195'), cep_to_coords('52021280'), cep_to_coords('54031140'), cep_to_coords('59640410'), cep_to_coords('55608735'), cep_to_coords('52111150'), cep_to_coords('55642095'), cep_to_coords('53421670'), cep_to_coords('53230550'), cep_to_coords('53230150'), cep_to_coords('54616546'), cep_to_coords('54720808'), cep_to_coords('56332230'), cep_to_coords('50820060'), cep_to_coords('50070405'), cep_to_coords('53120230'), cep_to_coords('55761550'), cep_to_coords('55741390'), cep_to_coords('51260300'), cep_to_coords('52390170'), cep_to_coords('54720780'), cep_to_coords('54740315'), cep_to_coords('51320070'), cep_to_coords('55002240'), cep_to_coords('55020320'), cep_to_coords('52190041'), cep_to_coords('55030420'), cep_to_coords('55020470'), cep_to_coords('50650350'), cep_to_coords('51250230'), cep_to_coords('50760760'), cep_to_coords('50636000'), cep_to_coords('53625295'), cep_to_coords('50740480'), cep_to_coords('54240555'), cep_to_coords('56510380'), cep_to_coords('52051210'), cep_to_coords('52130014'), cep_to_coords('51330050'), cep_to_coords('56160546'), cep_to_coords('52040220'), cep_to_coords('51190390'), cep_to_coords('50102303'), cep_to_coords('53431775'), cep_to_coords('53525735'), cep_to_coords('50640210'), cep_to_coords('50670510'), cep_to_coords('54910430'), cep_to_coords('52190520'), cep_to_coords('54280660'), cep_to_coords('54787878'), cep_to_coords('54330355'), cep_to_coords('53409270'), cep_to_coords('54730751'), cep_to_coords('52150135'), cep_to_coords('50900090'), cep_to_coords('53337064'), cep_to_coords('54774020'), cep_to_coords('51230420'), cep_to_coords('59571523'), cep_to_coords('51260680'), cep_to_coords('53560410'), cep_to_coords('53525740'), cep_to_coords('09854410'), cep_to_coords('50989625'), cep_to_coords('52030080'), cep_to_coords('53150275'), cep_to_coords('56319395'), cep_to_coords('53350390'), cep_to_coords('50751270'), cep_to_coords('54330110'), cep_to_coords('51320195'), cep_to_coords('54735360'), cep_to_coords('54070280'), cep_to_coords('56505025'), cep_to_coords('56506490'), cep_to_coords('53590990'), cep_to_coords('50670901'), cep_to_coords('54250604'), cep_to_coords('50721670'), cep_to_coords('54270450'), cep_to_coords('54429766'), cep_to_coords('53413151'), cep_to_coords('54100665'), cep_to_coords('56330210'), cep_to_coords('51280070'), cep_to_coords('51030745'), cep_to_coords('50940350'), cep_to_coords('52120181'), cep_to_coords('54350840'), cep_to_coords('53130160'), cep_to_coords('53090120'), cep_to_coords('53230520'), cep_to_coords('65645645'), cep_to_coords('53320530'), cep_to_coords('55012350'), cep_to_coords('48970000'), cep_to_coords('56320300'), cep_to_coords('56306347'), cep_to_coords('53240650'), cep_to_coords('54786690'), cep_to_coords('55012260'), cep_to_coords('50741485'), cep_to_coords('52720020'), cep_to_coords('53220580'), cep_to_coords('51021200'), cep_to_coords('55299542'), cep_to_coords('50980670'), cep_to_coords('54260440'), cep_to_coords('51220120'), cep_to_coords('52060220'), cep_to_coords('50720740'), cep_to_coords('51190737'), cep_to_coords('55153220'), cep_to_coords('42041160'), cep_to_coords('53270600'), cep_to_coords('54325730'), cep_to_coords('53413070'), cep_to_coords('55292390'), cep_to_coords('53010310'), cep_to_coords('42090320'), cep_to_coords('51010490'), cep_to_coords('53421590'), cep_to_coords('50740425'), cep_to_coords('55002505'), cep_to_coords('52081501'), cep_to_coords('50810491'), cep_to_coords('56312650'), cep_to_coords('53320370'), cep_to_coords('50690390'), cep_to_coords('53415160'), cep_to_coords('56511130'), cep_to_coords('53417160'), cep_to_coords('54510220'), cep_to_coords('53415490'), cep_to_coords('53441787'), cep_to_coords('52070715'), cep_to_coords('53320620'), cep_to_coords('58432355'), cep_to_coords('53420800'), cep_to_coords('02979000'), cep_to_coords('50980190'), cep_to_coords('52150370'), cep_to_coords('55022784'), cep_to_coords('50900480'), cep_to_coords('52280512'), cep_to_coords('51010177'), cep_to_coords('53220470'), cep_to_coords('54230072'), cep_to_coords('54100670'), cep_to_coords('54735012'), cep_to_coords('54150522'), cep_to_coords('54786670'), cep_to_coords('54517390'), cep_to_coords('55642122'), cep_to_coords('55030280'), cep_to_coords('52110080'), cep_to_coords('53534028'), cep_to_coords('53330560'), cep_to_coords('52120251'), cep_to_coords('50760580'), cep_to_coords('52160808'), cep_to_coords('53320600'), cep_to_coords('50070125'), cep_to_coords('51250010'), cep_to_coords('54530700'), cep_to_coords('51340085'), cep_to_coords('55019210'), cep_to_coords('51160050'), cep_to_coords('56323470'), cep_to_coords('52080465'), cep_to_coords('51113040'), cep_to_coords('51345790'), cep_to_coords('54280514'), cep_to_coords('50900600'), cep_to_coords('50640420'), cep_to_coords('53443016'), cep_to_coords('55020170'), cep_to_coords('63416680'), cep_to_coords('54774705'), cep_to_coords('53402450'), cep_to_coords('52610100'), cep_to_coords('53320520'), cep_to_coords('53407660'), cep_to_coords('54720025'), cep_to_coords('52006108'), cep_to_coords('50620630'), cep_to_coords('50930030'), cep_to_coords('52140270'), cep_to_coords('56510580'), cep_to_coords('53330280'), cep_to_coords('53370790'), cep_to_coords('56306353'), cep_to_coords('54320622'), cep_to_coords('54720265'), cep_to_coords('53630635'), cep_to_coords('53437565'), cep_to_coords('53417400'), cep_to_coords('50640260'), cep_to_coords('52080680'), cep_to_coords('52221385'), cep_to_coords('52070004'), cep_to_coords('56506665'), cep_to_coords('52125030'), cep_to_coords('54310232'), cep_to_coords('52070600'), cep_to_coords('52040252'), cep_to_coords('53350478'), cep_to_coords('53220180'), cep_to_coords('51190515'), cep_to_coords('50771160'), cep_to_coords('54335025'), cep_to_coords('51230322'), cep_to_coords('52170630'), cep_to_coords('53060241'), cep_to_coords('52011005'), cep_to_coords('54325141'), cep_to_coords('54786200'), cep_to_coords('53430340'), cep_to_coords('51060160'), cep_to_coords('50070490'), cep_to_coords('50110690'), cep_to_coords('53130060'), cep_to_coords('53560460'), cep_to_coords('53560201'), cep_to_coords('56516030'), cep_to_coords('56503510'), cep_to_coords('56508212'), cep_to_coords('51275290'), cep_to_coords('50650220'), cep_to_coords('51340513'), cep_to_coords('51200090'), cep_to_coords('55294810'), cep_to_coords('55014658'), cep_to_coords('54100640'), cep_to_coords('52121093'), cep_to_coords('54100360'), cep_to_coords('56517780'), cep_to_coords('54791467'), cep_to_coords('50910345'), cep_to_coords('52639898'), cep_to_coords('56318175'), cep_to_coords('53525034'), cep_to_coords('53280260'), cep_to_coords('54080350'), cep_to_coords('54745350'), cep_to_coords('54745080'), cep_to_coords('70373010'), cep_to_coords('52190311'), cep_to_coords('52080140'), cep_to_coords('51210060'), cep_to_coords('54771710'), cep_to_coords('52070948'), cep_to_coords('51345590'), cep_to_coords('53620763'), cep_to_coords('53560071'), cep_to_coords('54320250'), cep_to_coords('53550970'), cep_to_coords('53431235'), cep_to_coords('54315016'), cep_to_coords('56515380'), cep_to_coords('55576000'), cep_to_coords('50670250'), cep_to_coords('53565135'), cep_to_coords('50630220'), cep_to_coords('20171260'), cep_to_coords('53510620'), cep_to_coords('53564123'), cep_to_coords('22560000'), cep_to_coords('55002161'), cep_to_coords('55008070'), cep_to_coords('55018430'), cep_to_coords('05590000'), cep_to_coords('55295500'), cep_to_coords('56328490'), cep_to_coords('56323020'), cep_to_coords('56321720'), cep_to_coords('56332220'), cep_to_coords('65480000'), cep_to_coords('56318390'), cep_to_coords('56328560'), cep_to_coords('56322570'), cep_to_coords('56318310'), cep_to_coords('56313520'), cep_to_coords('54460330'), cep_to_coords('50070480'), cep_to_coords('56319300'), cep_to_coords('50080710'), cep_to_coords('53310630'), cep_to_coords('50960390'), cep_to_coords('55294630'), cep_to_coords('56515291'), cep_to_coords('54705680'), cep_to_coords('52020050'), cep_to_coords('53413050'), cep_to_coords('53110310'), cep_to_coords('50770280'), cep_to_coords('53419640'), cep_to_coords('54720215'), cep_to_coords('50081410'), cep_to_coords('53110350'), cep_to_coords('54730680'), cep_to_coords('54310020'), cep_to_coords('54090280'), cep_to_coords('51190470'), cep_to_coords('54715770'), cep_to_coords('51160410'), cep_to_coords('56502325'), cep_to_coords('52110470'), cep_to_coords('54315301'), cep_to_coords('53416593'), cep_to_coords('55002191'), cep_to_coords('50690500'), cep_to_coords('52150002'), cep_to_coords('51190600'), cep_to_coords('52291065'), cep_to_coords('54715100'), cep_to_coords('60115270'), cep_to_coords('55642590'), cep_to_coords('51320200'), cep_to_coords('55150230'), cep_to_coords('56506435'), cep_to_coords('56506020'), cep_to_coords('50100470'), cep_to_coords('56506050'), cep_to_coords('58460000'), cep_to_coords('52490190'), cep_to_coords('52031435'), cep_to_coords('52061395'), cep_to_coords('53431600'), cep_to_coords('53140350'), cep_to_coords('52120309'), cep_to_coords('82120320'), cep_to_coords('53990970'), cep_to_coords('79290000'), cep_to_coords('54479020'), cep_to_coords('51011300'), cep_to_coords('52121141'), cep_to_coords('52217101'), cep_to_coords('55605100'), cep_to_coords('53020610'), cep_to_coords('50870660'), cep_to_coords('50021370'), cep_to_coords('55014473'), cep_to_coords('55298505'), cep_to_coords('57600000'), cep_to_coords('51345770'), cep_to_coords('56332070'), cep_to_coords('48905509'), cep_to_coords('56318745'), cep_to_coords('53540310'), cep_to_coords('54580580'), cep_to_coords('50780710'), cep_to_coords('52011181'), cep_to_coords('53431305'), cep_to_coords('55155540'), cep_to_coords('55299775'), cep_to_coords('53637155'), cep_to_coords('56328440'), cep_to_coords('563120150'), cep_to_coords('55293231'), cep_to_coords('56332175'), cep_to_coords('51270280'), cep_to_coords('56848000'), cep_to_coords('54080204'), cep_to_coords('53200210'), cep_to_coords('56330565'), cep_to_coords('51350480'), cep_to_coords('53030300'), cep_to_coords('51220250'), cep_to_coords('56320640'), cep_to_coords('53140340'), cep_to_coords('56509080'), cep_to_coords('50791361'), cep_to_coords('54230615'), cep_to_coords('53421820'), cep_to_coords('56330035'), cep_to_coords('56511360'), cep_to_coords('50930400'), cep_to_coords('54315351'), cep_to_coords('52040460'), cep_to_coords('50912093'), cep_to_coords('55020010'), cep_to_coords('53370660'), cep_to_coords('54250001'), cep_to_coords('55012540'), cep_to_coords('53130135'), cep_to_coords('50690650'), cep_to_coords('52090840'), cep_to_coords('53290160'), cep_to_coords('57960000'), cep_to_coords('55030545'), cep_to_coords('52130340'), cep_to_coords('54230241'), cep_to_coords('52660064'), cep_to_coords('53040030'), cep_to_coords('53433470'), cep_to_coords('52091615'), cep_to_coords('53080190'), cep_to_coords('55358529'), cep_to_coords('55002450'), cep_to_coords('52190485'), cep_to_coords('56312676'), cep_to_coords('50640000'), cep_to_coords('50640080'), cep_to_coords('53401740'), cep_to_coords('53401742'), cep_to_coords('54774325'), cep_to_coords('53320512'), cep_to_coords('53417510'), cep_to_coords('53280410'), cep_to_coords('55644200'), cep_to_coords('55296170'), cep_to_coords('54437050'), cep_to_coords('55158450'), cep_to_coords('53421161'), cep_to_coords('50820160'), cep_to_coords('53050142'), cep_to_coords('52111690'), cep_to_coords('52091380'), cep_to_coords('52165400'), cep_to_coords('53290230'), cep_to_coords('56519110'), cep_to_coords('50930210'), cep_to_coords('50900590'), cep_to_coords('54340711'), cep_to_coords('55038090'), cep_to_coords('55380970'), cep_to_coords('55020070'), cep_to_coords('54767121'), cep_to_coords('55026191'), cep_to_coords('51260710'), cep_to_coords('55297170'), cep_to_coords('53270590'), cep_to_coords('53605810'), cep_to_coords('53437630'), cep_to_coords('53250390'), cep_to_coords('53441180'), cep_to_coords('53230200'), cep_to_coords('51290600'), cep_to_coords('50590610'), cep_to_coords('50123010'), cep_to_coords('51170170'), cep_to_coords('50751560'), cep_to_coords('53220230'), cep_to_coords('54710000'), cep_to_coords('52081141'), cep_to_coords('54220610'), cep_to_coords('54345710'), cep_to_coords('55020490'), cep_to_coords('50090210'), cep_to_coords('52040490'), cep_to_coords('54460376'), cep_to_coords('53409070'), cep_to_coords('54250255'), cep_to_coords('50761575'), cep_to_coords('55195578'), cep_to_coords('55819000'), cep_to_coords('50750580'), cep_to_coords('52280305'), cep_to_coords('51250040'), cep_to_coords('54740030'), cep_to_coords('53403410'), cep_to_coords('54430131'), cep_to_coords('54410440'), cep_to_coords('53433265'), cep_to_coords('54777000'), cep_to_coords('54774130'), cep_to_coords('55195656'), cep_to_coords('52160520'), cep_to_coords('51010245'), cep_to_coords('50770430'), cep_to_coords('50740466'), cep_to_coords('50830248'), cep_to_coords('53620000'), cep_to_coords('53080570'), cep_to_coords('54515460'), cep_to_coords('53439120'), cep_to_coords('52191300'), cep_to_coords('52070535'), cep_to_coords('53402055'), cep_to_coords('53530620'), cep_to_coords('27470521'), cep_to_coords('55020035'), cep_to_coords('53540230'), cep_to_coords('54160448'), cep_to_coords('54315450'), cep_to_coords('53435970'), cep_to_coords('53620580'), cep_to_coords('56316804'), cep_to_coords('54290062'), cep_to_coords('53417560'), cep_to_coords('56313040'), cep_to_coords('54100443'), cep_to_coords('50630620'), cep_to_coords('50920064'), cep_to_coords('55032451'), cep_to_coords('52081521'), cep_to_coords('53605535'), cep_to_coords('55027220'), cep_to_coords('53290180'), cep_to_coords('55008320'), cep_to_coords('55813370'), cep_to_coords('55299493'), cep_to_coords('56328340'), cep_to_coords('55006400'), cep_to_coords('56330335'), cep_to_coords('51030900'), cep_to_coords('54460100'), cep_to_coords('50920653'), cep_to_coords('53260220'), cep_to_coords('52031150'), cep_to_coords('56312201'), cep_to_coords('56509580'), cep_to_coords('51190440'), cep_to_coords('52103090'), cep_to_coords('50750370'), cep_to_coords('52040500'), cep_to_coords('53620730'), cep_to_coords('53620605'), cep_to_coords('54520270'), cep_to_coords('54280285'), cep_to_coords('53530406'), cep_to_coords('54753670'), cep_to_coords('54720075'), cep_to_coords('53220402'), cep_to_coords('50070475'), cep_to_coords('56517460'), cep_to_coords('53630160'), cep_to_coords('50721390'), cep_to_coords('58150000'), cep_to_coords('55643020'), cep_to_coords('52121090'), cep_to_coords('52280444'), cep_to_coords('54160260'), cep_to_coords('51170370'), cep_to_coords('54325815'), cep_to_coords('53403290'), cep_to_coords('48902233'), cep_to_coords('56312195'), cep_to_coords('50777040'), cep_to_coords('54160655'), cep_to_coords('52070515'), cep_to_coords('52091232'), cep_to_coords('54170127'), cep_to_coords('51300271'), cep_to_coords('44001184'), cep_to_coords('50970390'), cep_to_coords('50110720'), cep_to_coords('53620471'), cep_to_coords('55002470'), cep_to_coords('50070140'), cep_to_coords('52060240'), cep_to_coords('54340590'), cep_to_coords('54735250'), cep_to_coords('51020904'), cep_to_coords('51345600'), cep_to_coords('50850275'), cep_to_coords('51140030'), cep_to_coords('52060470'), cep_to_coords('53060473'), cep_to_coords('54709213'), cep_to_coords('52125150'), cep_to_coords('55020780'), cep_to_coords('56309660'), cep_to_coords('51160250'), cep_to_coords('56316566'), cep_to_coords('53370293'), cep_to_coords('52280496'), cep_to_coords('53560270'), cep_to_coords('56314040'), cep_to_coords('53402145'), cep_to_coords('50110785'), cep_to_coords('50681040'), cep_to_coords('53441440'), cep_to_coords('54768856'), cep_to_coords('50751320'), cep_to_coords('52041654'), cep_to_coords('50820280'), cep_to_coords('50700400'), cep_to_coords('53407150'), cep_to_coords('53230070'), cep_to_coords('50640220'), cep_to_coords('48900411'), cep_to_coords('30670360'), cep_to_coords('54280786'), cep_to_coords('53520710'), cep_to_coords('52025205'), cep_to_coords('54450130'), cep_to_coords('53320181'), cep_to_coords('56332460'), cep_to_coords('53420210'), cep_to_coords('53565470'), cep_to_coords('53540760'), cep_to_coords('50960470'), cep_to_coords('54280254'), cep_to_coords('54325376'), cep_to_coords('50870190'), cep_to_coords('55036830'), cep_to_coords('41900600'), cep_to_coords('62010090'), cep_to_coords('55037500'), cep_to_coords('53370820'), cep_to_coords('53090550'), cep_to_coords('03267150'), cep_to_coords('54150700'), cep_to_coords('06454070'), cep_to_coords('51547350'), cep_to_coords('72318105'), cep_to_coords('51345340'), cep_to_coords('50710460'), cep_to_coords('53437730'), cep_to_coords('56509000'), cep_to_coords('56310100'), cep_to_coords('55016660'), cep_to_coords('55006050'), cep_to_coords('55038115'), cep_to_coords('55010640'), cep_to_coords('55038255'), cep_to_coords('55006000'), cep_to_coords('55012470'), cep_to_coords('55019340'), cep_to_coords('55020395'), cep_to_coords('55020537'), cep_to_coords('55016300'), cep_to_coords('55018058'), cep_to_coords('55018745'), cep_to_coords('55016170'), cep_to_coords('55010470'), cep_to_coords('55004310'), cep_to_coords('55020265'), cep_to_coords('55008040'), cep_to_coords('55024311'), cep_to_coords('55021275'), cep_to_coords('55036055'), cep_to_coords('55014245'), cep_to_coords('55020380'), cep_to_coords('55019025'), cep_to_coords('55026050'), cep_to_coords('55020250'), cep_to_coords('55027400'), cep_to_coords('55026230'), cep_to_coords('55010315'), cep_to_coords('55034600'), cep_to_coords('55031205'), cep_to_coords('55031240'), cep_to_coords('55028170'), cep_to_coords('55010130'), cep_to_coords('55037080'), cep_to_coords('55014500'), cep_to_coords('55022640'), cep_to_coords('55006250'), cep_to_coords('55014385'), cep_to_coords('52110540'), cep_to_coords('54340438'), cep_to_coords('55026360'), cep_to_coords('50910200'), cep_to_coords('54759514'), cep_to_coords('50721240'), cep_to_coords('50720241'), cep_to_coords('52280272'), cep_to_coords('52111180'), cep_to_coords('52021200'), cep_to_coords('53200190'), cep_to_coords('56912380'), cep_to_coords('53360520'), cep_to_coords('55022120'), cep_to_coords('54350930'), cep_to_coords('54737560'), cep_to_coords('52071610'), cep_to_coords('54762755'), cep_to_coords('53404220'), cep_to_coords('55006463'), cep_to_coords('51020329'), cep_to_coords('54774410'), cep_to_coords('52041750'), cep_to_coords('51290270'), cep_to_coords('52091020'), cep_to_coords('52080210'), cep_to_coords('53130170'), cep_to_coords('54140510'), cep_to_coords('50771080'), cep_to_coords('56515335'), cep_to_coords('55617000'), cep_to_coords('54505225'), cep_to_coords('58312000'), cep_to_coords('50740240'), cep_to_coords('52280572'), cep_to_coords('50730605'), cep_to_coords('54792530'), cep_to_coords('54768780'), cep_to_coords('56306355'), cep_to_coords('50570170'), cep_to_coords('53421610'), cep_to_coords('50720260'), cep_to_coords('51290120'), cep_to_coords('54310244'), cep_to_coords('53220101'), cep_to_coords('54783020'), cep_to_coords('54783050'), cep_to_coords('51240790'), cep_to_coords('53240521'), cep_to_coords('50091200'), cep_to_coords('53401540'), cep_to_coords('52140051'), cep_to_coords('53160070'), cep_to_coords('51345031'), cep_to_coords('54230033'), cep_to_coords('14860000'), cep_to_coords('56506270'), cep_to_coords('54730740'), cep_to_coords('51160390'), cep_to_coords('51150270'), cep_to_coords('52090815'), cep_to_coords('54340640'), cep_to_coords('56330030'), cep_to_coords('53610282'), cep_to_coords('55270970'), cep_to_coords('53560590'), cep_to_coords('50260020'), cep_to_coords('54580180'), cep_to_coords('00000900'), cep_to_coords('55818425'), cep_to_coords('52090340'), cep_to_coords('51310040'), cep_to_coords('50080400'), cep_to_coords('51130060'), cep_to_coords('563283400'), cep_to_coords('56909640'), cep_to_coords('50960080'), cep_to_coords('54762585'), cep_to_coords('55296725'), cep_to_coords('51040400'), cep_to_coords('53433810'), cep_to_coords('56314150'), cep_to_coords('56310220'), cep_to_coords('53666520'), cep_to_coords('55008085'), cep_to_coords('54220431'), cep_to_coords('54753720'), cep_to_coords('52170250'), cep_to_coords('54150091'), cep_to_coords('54735380'), cep_to_coords('50920050'), cep_to_coords('52070120'), cep_to_coords('54870300'), cep_to_coords('51130270'), cep_to_coords('51240110'), cep_to_coords('52280420'), cep_to_coords('50781520'), cep_to_coords('50781715'), cep_to_coords('54705620'), cep_to_coords('03147000'), cep_to_coords('52125210'), cep_to_coords('54765005'), cep_to_coords('54315250'), cep_to_coords('51120130'), cep_to_coords('51275070'), cep_to_coords('51260530'), cep_to_coords('54730044'), cep_to_coords('51280143'), cep_to_coords('52291052'), cep_to_coords('53405040'), cep_to_coords('54100465'), cep_to_coords('52071133'), cep_to_coords('54250311'), cep_to_coords('53545750'), cep_to_coords('55813270'), cep_to_coords('05676000'), cep_to_coords('50940690'), cep_to_coords('52030960'), cep_to_coords('50790040'), cep_to_coords('56310605'), cep_to_coords('52160228'), cep_to_coords('53150160'), cep_to_coords('54733040'), cep_to_coords('50781750'), cep_to_coords('54737065'), cep_to_coords('54740550'), cep_to_coords('56509155'), cep_to_coords('54715190'), cep_to_coords('50670530'), cep_to_coords('52160227'), cep_to_coords('52130481'), cep_to_coords('50750200'), cep_to_coords('21230230'), cep_to_coords('50020160'), cep_to_coords('50720350'), cep_to_coords('54280131'), cep_to_coords('52280522'), cep_to_coords('53230231'), cep_to_coords('50630265'), cep_to_coords('50050910'), cep_to_coords('55002350'), cep_to_coords('52121114'), cep_to_coords('52080390'), cep_to_coords('55022085'), cep_to_coords('53260595'), cep_to_coords('55299410'), cep_to_coords('56310310'), cep_to_coords('56328350'), cep_to_coords('55036030'), cep_to_coords('54440450'), cep_to_coords('48903000'), cep_to_coords('56332756'), cep_to_coords('56316270'), cep_to_coords('52170160'), cep_to_coords('51010180'), cep_to_coords('50810090'), cep_to_coords('52130270'), cep_to_coords('55158050'), cep_to_coords('55158215'), cep_to_coords('50620170'), cep_to_coords('55158120'), cep_to_coords('51340195'), cep_to_coords('55292255'), cep_to_coords('54460190'), cep_to_coords('50810055'), cep_to_coords('53404550'), cep_to_coords('56503790'), cep_to_coords('56515290'), cep_to_coords('55004270'), cep_to_coords('52191500'), cep_to_coords('51330371'), cep_to_coords('52090080'), cep_to_coords('51340300'), cep_to_coords('54325490'), cep_to_coords('52091075'), cep_to_coords('05568020'), cep_to_coords('53402005'), cep_to_coords('53220103'), cep_to_coords('50760300'), cep_to_coords('51240320'), cep_to_coords('52291630'), cep_to_coords('54120450'), cep_to_coords('52140200'), cep_to_coords('51011090'), cep_to_coords('51320290'), cep_to_coords('54715710'), cep_to_coords('53550120'), cep_to_coords('53320150'), cep_to_coords('54789010'), cep_to_coords('50761240'), cep_to_coords('54440525'), cep_to_coords('53433560'), cep_to_coords('54580460'), cep_to_coords('52090278'), cep_to_coords('52081380'), cep_to_coords('54730180'), cep_to_coords('54210542'), cep_to_coords('52050051'), cep_to_coords('51320275'), cep_to_coords('50770350'), cep_to_coords('54777125'), cep_to_coords('53320380'), cep_to_coords('53610360'), cep_to_coords('56312015'), cep_to_coords('53140162'), cep_to_coords('53415470'), cep_to_coords('54400460'), cep_to_coords('52110400'), cep_to_coords('51330374'), cep_to_coords('52021215'), cep_to_coords('50732250'), cep_to_coords('54250550'), cep_to_coords('50910360'), cep_to_coords('53421460'), cep_to_coords('53433030'), cep_to_coords('53230540'), cep_to_coords('21020280'), cep_to_coords('20011030'), cep_to_coords('54330321'), cep_to_coords('53420290'), cep_to_coords('53407500'), cep_to_coords('54720520'), cep_to_coords('50040390'), cep_to_coords('54786650'), cep_to_coords('53421530'), cep_to_coords('52121570'), cep_to_coords('54310220'), cep_to_coords('54150395'), cep_to_coords('50960240'), cep_to_coords('50000011'), cep_to_coords('53220320'), cep_to_coords('53409240'), cep_to_coords('52021190'), cep_to_coords('52160090'), cep_to_coords('53422390'), cep_to_coords('55813810'), cep_to_coords('52120460'), cep_to_coords('52130390'), cep_to_coords('51345387'), cep_to_coords('50850324'), cep_to_coords('52490160'), cep_to_coords('25487214'), cep_to_coords('54230041'), cep_to_coords('53416000'), cep_to_coords('53402013'), cep_to_coords('54756015'), cep_to_coords('52280400'), cep_to_coords('52130174'), cep_to_coords('50690140'), cep_to_coords('54720196'), cep_to_coords('51130500'), cep_to_coords('55022221'), cep_to_coords('50900040'), cep_to_coords('53439350'), cep_to_coords('52061130'), cep_to_coords('54720667'), cep_to_coords('55016155'), cep_to_coords('53560123'), cep_to_coords('50050220'), cep_to_coords('54735310'), cep_to_coords('53419735'), cep_to_coords('54530020'), cep_to_coords('53170010'), cep_to_coords('54230420'), cep_to_coords('53360020'), cep_to_coords('55642115'), cep_to_coords('52020035'), cep_to_coords('50751117'), cep_to_coords('51010430'), cep_to_coords('52101120'), cep_to_coords('52140590'), cep_to_coords('55018740'), cep_to_coords('50030000'), cep_to_coords('52291074'), cep_to_coords('5528000000'), cep_to_coords('55292480'), cep_to_coords('55036455'), cep_to_coords('50850380'), cep_to_coords('51190736'), cep_to_coords('56316738'), cep_to_coords('56312810'), cep_to_coords('50940030'), cep_to_coords('50731320'), cep_to_coords('50620651'), cep_to_coords('52121211'), cep_to_coords('54270500'), cep_to_coords('51120000'), cep_to_coords('53530438'), cep_to_coords('53080830'), cep_to_coords('56322060'), cep_to_coords('56316600'), cep_to_coords('55602215'), cep_to_coords('50751260'), cep_to_coords('55150580'), cep_to_coords('55151570'), cep_to_coords('55151750'), cep_to_coords('52131061'), cep_to_coords('52080595'), cep_to_coords('55818575'), cep_to_coords('55816220'), cep_to_coords('55019155'), cep_to_coords('54440045'), cep_to_coords('50080780'), cep_to_coords('53441430'), cep_to_coords('55199000'), cep_to_coords('50910090'), cep_to_coords('51031300'), cep_to_coords('52120001'), cep_to_coords('50711044'), cep_to_coords('54756602'), cep_to_coords('54080172'), cep_to_coords('56331000'), cep_to_coords('51300143'), cep_to_coords('50005054'), cep_to_coords('52081665'), cep_to_coords('50850140'), cep_to_coords('53270240'), cep_to_coords('51112111'), cep_to_coords('50820570'), cep_to_coords('52111602'), cep_to_coords('50350560'), cep_to_coords('54230382'), cep_to_coords('54420260'), cep_to_coords('54170210'), cep_to_coords('53431325'), cep_to_coords('52490040'), cep_to_coords('57270000'), cep_to_coords('01121963'), cep_to_coords('50791460'), cep_to_coords('50770601'), cep_to_coords('53630503'), cep_to_coords('50920055'), cep_to_coords('24933545'), cep_to_coords('53030430'), cep_to_coords('53419130'), cep_to_coords('54260012'), cep_to_coords('50960330'), cep_to_coords('54555526'), cep_to_coords('52130019'), cep_to_coords('52211041'), cep_to_coords('52070082'), cep_to_coords('55024685'), cep_to_coords('50830080'), cep_to_coords('51230440'), cep_to_coords('50711500'), cep_to_coords('53330030'), cep_to_coords('50701440'), cep_to_coords('54315030'), cep_to_coords('52040083'), cep_to_coords('50720033'), cep_to_coords('54735235'), cep_to_coords('54735225'), cep_to_coords('50910330'), cep_to_coords('56326200'), cep_to_coords('50940541'), cep_to_coords('54517375'), cep_to_coords('54120510'), cep_to_coords('51300440'), cep_to_coords('53435450'), cep_to_coords('53550008'), cep_to_coords('54580525'), cep_to_coords('50712040'), cep_to_coords('53150110'), cep_to_coords('54780756'), cep_to_coords('32090320'), cep_to_coords('54740020'), cep_to_coords('54100271'), cep_to_coords('56328060'), cep_to_coords('55641430'), cep_to_coords('50865101'), cep_to_coords('51250140'), cep_to_coords('50690420'), cep_to_coords('52280050'), cep_to_coords('56321490'), cep_to_coords('56332758'), cep_to_coords('55154680'), cep_to_coords('56318270'), cep_to_coords('50690250'), cep_to_coords('53330260'), cep_to_coords('55018180'), cep_to_coords('54230582'), cep_to_coords('53510335'), cep_to_coords('54303060'), cep_to_coords('33140320'), cep_to_coords('52121350'), cep_to_coords('51130520'), cep_to_coords('53403440'), cep_to_coords('54752035'), cep_to_coords('54320110'), cep_to_coords('15562131'), cep_to_coords('52170080'), cep_to_coords('52121037'), cep_to_coords('52113480'), cep_to_coords('54320025'), cep_to_coords('53370198'), cep_to_coords('53330070'), cep_to_coords('54510280'), cep_to_coords('52080058'), cep_to_coords('52190042'), cep_to_coords('53939310'), cep_to_coords('56625000'), cep_to_coords('53170630'), cep_to_coords('50720580'), cep_to_coords('52282420'), cep_to_coords('53403690'), cep_to_coords('56320796'), cep_to_coords('50771350'), cep_to_coords('54350110'), cep_to_coords('05093000'), cep_to_coords('50710320'), cep_to_coords('52171150'), cep_to_coords('52291675'), cep_to_coords('53300380'), cep_to_coords('53407780'), cep_to_coords('54280110'), cep_to_coords('52171310'), cep_to_coords('56912225'), cep_to_coords('53443580'), cep_to_coords('52061155'), cep_to_coords('50090310'), cep_to_coords('53429530'), cep_to_coords('51210902'), cep_to_coords('54368070'), cep_to_coords('53610850'), cep_to_coords('53110580'), cep_to_coords('56319600'), cep_to_coords('50870040'), cep_to_coords('50791251'), cep_to_coords('54320181'), cep_to_coords('51010372'), cep_to_coords('53625075'), cep_to_coords('50210120'), cep_to_coords('54150660'), cep_to_coords('54090460'), cep_to_coords('53260120'), cep_to_coords('50051030'), cep_to_coords('51290140'), cep_to_coords('52091060'), cep_to_coords('55819035'), cep_to_coords('50791113'), cep_to_coords('53020370'), cep_to_coords('56316210'), cep_to_coords('54220280'), cep_to_coords('50491203'), cep_to_coords('51260630'), cep_to_coords('53610762'), cep_to_coords('52090373'), cep_to_coords('50800181'), cep_to_coords('80000000'), cep_to_coords('53050060'), cep_to_coords('52150022'), cep_to_coords('51290560'), cep_to_coords('50980640'), cep_to_coords('54410151'), cep_to_coords('55008030'), cep_to_coords('55819170'), cep_to_coords('53402812'), cep_to_coords('53585760'), cep_to_coords('54365240'), cep_to_coords('51270660'), cep_to_coords('52131420'), cep_to_coords('54320141'), cep_to_coords('55006505'), cep_to_coords('54768765'), cep_to_coords('54768155'), cep_to_coords('50730080'), cep_to_coords('51290571'), cep_to_coords('54440400'), cep_to_coords('52070260'), cep_to_coords('56318210'), cep_to_coords('50741330'), cep_to_coords('51030640'), cep_to_coords('53370297'), cep_to_coords('54556465'), cep_to_coords('54340430'), cep_to_coords('54355680'), cep_to_coords('54790660'), cep_to_coords('55294500'), cep_to_coords('56302685'), cep_to_coords('52170070'), cep_to_coords('50711620'), cep_to_coords('20781530'), cep_to_coords('53230490'), cep_to_coords('53625471'), cep_to_coords('54580345'), cep_to_coords('54110001'), cep_to_coords('50055525'), cep_to_coords('50192390'), cep_to_coords('53435355'), cep_to_coords('54720085'), cep_to_coords('50910573'), cep_to_coords('50741540'), cep_to_coords('51345360'), cep_to_coords('51345090'), cep_to_coords('53060490'), cep_to_coords('53010401'), cep_to_coords('53530452'), cep_to_coords('54610310'), cep_to_coords('54335120'), cep_to_coords('08720000'), cep_to_coords('52081583'), cep_to_coords('53090080'), cep_to_coords('53110670'), cep_to_coords('54517720'), cep_to_coords('54460650'), cep_to_coords('50092500'), cep_to_coords('53429200'), cep_to_coords('54762110'), cep_to_coords('54789525'), cep_to_coords('52810070'), cep_to_coords('53620827'), cep_to_coords('53422450'), cep_to_coords('53437151'), cep_to_coords('54735460'), cep_to_coords('50620620'), cep_to_coords('55027080'), cep_to_coords('50875010'), cep_to_coords('50110120'), cep_to_coords('52191111'), cep_to_coords('51270550'), cep_to_coords('51010580'), cep_to_coords('55811020'), cep_to_coords('53210211'), cep_to_coords('54710001'), cep_to_coords('52050146'), cep_to_coords('55819140'), cep_to_coords('53070640'), cep_to_coords('05202110'), cep_to_coords('53413590'), cep_to_coords('50670620'), cep_to_coords('55014327'), cep_to_coords('55018350'), cep_to_coords('55014260'), cep_to_coords('56331210'), cep_to_coords('52165250'), cep_to_coords('50860100'), cep_to_coords('56313340'), cep_to_coords('55019105'), cep_to_coords('56322620'), cep_to_coords('52280424'), cep_to_coords('52211010'), cep_to_coords('54580794'), cep_to_coords('55111600'), cep_to_coords('53442580'), cep_to_coords('53090433'), cep_to_coords('53435720'), cep_to_coords('50040303'), cep_to_coords('54240460'), cep_to_coords('50070530'), cep_to_coords('53570370'), cep_to_coords('53170077'), cep_to_coords('56330523'), cep_to_coords('54325042'), cep_to_coords('54430310'), cep_to_coords('54100231'), cep_to_coords('52090760'), cep_to_coords('54750655'), cep_to_coords('54360032'), cep_to_coords('52280260'), cep_to_coords('52080252'), cep_to_coords('52111550'), cep_to_coords('50771725'), cep_to_coords('50670580'), cep_to_coords('52090780'), cep_to_coords('51111240'), cep_to_coords('54735565'), cep_to_coords('56330130'), cep_to_coords('52140120'), cep_to_coords('53416600'), cep_to_coords('50690505'), cep_to_coords('55815067'), cep_to_coords('50810550'), cep_to_coords('56310280'), cep_to_coords('54490263'), cep_to_coords('54340405'), cep_to_coords('53120160'), cep_to_coords('52110110'), cep_to_coords('54580310'), cep_to_coords('54753590'), cep_to_coords('53040080'), cep_to_coords('54160445'), cep_to_coords('55291270'), cep_to_coords('54400130'), cep_to_coords('50830220'), cep_to_coords('53630345'), cep_to_coords('50960010'), cep_to_coords('53260520'), cep_to_coords('54753281'), cep_to_coords('51340035'), cep_to_coords('52081260'), cep_to_coords('52190527'), cep_to_coords('52291170'), cep_to_coords('50770620'), cep_to_coords('50760160'), cep_to_coords('50090560'), cep_to_coords('55813350'), cep_to_coords('53402762'), cep_to_coords('54090580'), cep_to_coords('54100681'), cep_to_coords('54100673'), cep_to_coords('50780360'), cep_to_coords('50080510'), cep_to_coords('51240695'), cep_to_coords('53220805'), cep_to_coords('51030540'), cep_to_coords('20000000'), cep_to_coords('54320680'), cep_to_coords('55811210'), cep_to_coords('53020490'), cep_to_coords('50860360'), cep_to_coords('51410310'), cep_to_coords('52190535'), cep_to_coords('51275615'), cep_to_coords('53620845'), cep_to_coords('51010068'), cep_to_coords('53407430'), cep_to_coords('54070310'), cep_to_coords('54754125'), cep_to_coords('54100730'), cep_to_coords('54580665'), cep_to_coords('54090533'), cep_to_coords('53180053'), cep_to_coords('54210400'), cep_to_coords('54530450'), cep_to_coords('54759355'), cep_to_coords('55024735'), cep_to_coords('55641590'), cep_to_coords('55030512'), cep_to_coords('50660130'), cep_to_coords('57545841'), cep_to_coords('55530640'), cep_to_coords('54767622'), cep_to_coords('53250750'), cep_to_coords('53250350'), cep_to_coords('55024825'), cep_to_coords('55643140'), cep_to_coords('55643405'), cep_to_coords('51020972'), cep_to_coords('56328510'), cep_to_coords('54360215'), cep_to_coords('50822010'), cep_to_coords('50940500'), cep_to_coords('51140470'), cep_to_coords('50860170'), cep_to_coords('15121996'), cep_to_coords('50404002'), cep_to_coords('55038405'), cep_to_coords('55614010'), cep_to_coords('52060610'), cep_to_coords('56509330'), cep_to_coords('53530436'), cep_to_coords('55006057'), cep_to_coords('54210451'), cep_to_coords('54240510'), cep_to_coords('50940580'), cep_to_coords('52291580'), cep_to_coords('51017180'), cep_to_coords('54140600'), cep_to_coords('50910350'), cep_to_coords('53210120'), cep_to_coords('54410276'), cep_to_coords('51010730'), cep_to_coords('52111010'), cep_to_coords('52150001'), cep_to_coords('51310345'), cep_to_coords('53170830'), cep_to_coords('55602510'), cep_to_coords('53150200'), cep_to_coords('50010140'), cep_to_coords('53441205'), cep_to_coords('54517215'), cep_to_coords('51116010'), cep_to_coords('52130130'), cep_to_coords('50640660'), cep_to_coords('52131040'), cep_to_coords('50080580'), cep_to_coords('53270230'), cep_to_coords('54210522'), cep_to_coords('40721510'), cep_to_coords('54310710'), cep_to_coords('54490074'), cep_to_coords('50830700'), cep_to_coords('52110001'), cep_to_coords('52190525'), cep_to_coords('59507000'), cep_to_coords('53520550'), cep_to_coords('50875125'), cep_to_coords('53530555'), cep_to_coords('53060370'), cep_to_coords('54360123'), cep_to_coords('51350210'), cep_to_coords('54280081'), cep_to_coords('56509245'), cep_to_coords('52070665'), cep_to_coords('52081160'), cep_to_coords('52121520'), cep_to_coords('53422160'), cep_to_coords('53402190'), cep_to_coords('51340795'), cep_to_coords('53421140'), cep_to_coords('55014050'), cep_to_coords('55604210'), cep_to_coords('54210350'), cep_to_coords('54280520'), cep_to_coords('56312095'), cep_to_coords('48901140'), cep_to_coords('51270561'), cep_to_coords('52191125'), cep_to_coords('52040210'), cep_to_coords('50650240'), cep_to_coords('53419730'), cep_to_coords('53605730'), cep_to_coords('51010401'), cep_to_coords('54240050'), cep_to_coords('53160500'), cep_to_coords('53402780'), cep_to_coords('50680116'), cep_to_coords('50920510'), cep_to_coords('50720745'), cep_to_coords('50850322'), cep_to_coords('50791240'), cep_to_coords('50210300'), cep_to_coords('55643185'), cep_to_coords('54080180'), cep_to_coords('53442133'), cep_to_coords('53150330'), cep_to_coords('52081441'), cep_to_coords('54300220'), cep_to_coords('52110030'), cep_to_coords('55643070'), cep_to_coords('54519140'), cep_to_coords('56509730'), cep_to_coords('52090001'), cep_to_coords('54315615'), cep_to_coords('54517470'), cep_to_coords('50771145'), cep_to_coords('55036335'), cep_to_coords('04965000'), cep_to_coords('50960050'), cep_to_coords('50610290'), cep_to_coords('51030190'), cep_to_coords('52060530'), cep_to_coords('50125040'), cep_to_coords('55644282'), cep_to_coords('54720173'), cep_to_coords('52291200'), cep_to_coords('55010670'), cep_to_coords('55642065'), cep_to_coords('55641250'), cep_to_coords('50620280'), cep_to_coords('52160131'), cep_to_coords('52191130'), cep_to_coords('50650070'), cep_to_coords('55641195'), cep_to_coords('50940160'), cep_to_coords('53415340'), cep_to_coords('52415340'), cep_to_coords('52020080'), cep_to_coords('56312130'), cep_to_coords('56331220'), cep_to_coords('50030908'), cep_to_coords('54325240'), cep_to_coords('51220220'), cep_to_coords('54230092'), cep_to_coords('54320092'), cep_to_coords('50640070'), cep_to_coords('51320530'), cep_to_coords('50620480'), cep_to_coords('56515300'), cep_to_coords('50791364'), cep_to_coords('53560700'), cep_to_coords('54460555'), cep_to_coords('54470595'), cep_to_coords('53510490'), cep_to_coords('24071974'), cep_to_coords('53640340'), cep_to_coords('54210033'), cep_to_coords('52191135'), cep_to_coords('53439330'), cep_to_coords('53422570'), cep_to_coords('54310080'), cep_to_coords('56050902'), cep_to_coords('50940070'), cep_to_coords('54270250'), cep_to_coords('52165090'), cep_to_coords('52120261'), cep_to_coords('50731730'), cep_to_coords('53370200'), cep_to_coords('50120301'), cep_to_coords('53230271'), cep_to_coords('54280190'), cep_to_coords('50110435'), cep_to_coords('54230122'), cep_to_coords('55004241'), cep_to_coords('52080091'), cep_to_coords('50110392'), cep_to_coords('53290060'), cep_to_coords('35710000'), cep_to_coords('53570060'), cep_to_coords('53435260'), cep_to_coords('54515655'), cep_to_coords('53407470'), cep_to_coords('54702225'), cep_to_coords('50910570'), cep_to_coords('54250370'), cep_to_coords('50620160'), cep_to_coords('50730310'), cep_to_coords('50030300'), cep_to_coords('52111290'), cep_to_coords('55150211'), cep_to_coords('53625450'), cep_to_coords('51180001'), cep_to_coords('53490000'), cep_to_coords('54360156'), cep_to_coords('55643230'), cep_to_coords('65800220'), cep_to_coords('51250900'), cep_to_coords('50990330'), cep_to_coords('52211159'), cep_to_coords('50830010'), cep_to_coords('52111582'), cep_to_coords('52040141'), cep_to_coords('52111060'), cep_to_coords('52070640'), cep_to_coords('55643065'), cep_to_coords('50660160'), cep_to_coords('54589355'), cep_to_coords('54522080'), cep_to_coords('50780970'), cep_to_coords('54290018'), cep_to_coords('54350090'), cep_to_coords('50710135'), cep_to_coords('55644188'), cep_to_coords('50760215'), cep_to_coords('52211075'), cep_to_coords('53640245'), cep_to_coords('52031380'), cep_to_coords('50750160'), cep_to_coords('56509385'), cep_to_coords('50790318'), cep_to_coords('54771646'), cep_to_coords('54280476'), cep_to_coords('54280760'), cep_to_coords('54315390'), cep_to_coords('54210537'), cep_to_coords('54517335'), cep_to_coords('54580726'), cep_to_coords('54730560'), cep_to_coords('55038175'), cep_to_coords('52131011'), cep_to_coords('53160400'), cep_to_coords('54240040'), cep_to_coords('52190122'), cep_to_coords('52191330'), cep_to_coords('52111614'), cep_to_coords('53550000'), cep_to_coords('53041151'), cep_to_coords('55038019'), cep_to_coords('55036397'), cep_to_coords('55641260'), cep_to_coords('56306810'), cep_to_coords('56309270'), cep_to_coords('50930100'), cep_to_coords('54340655'), cep_to_coords('51003012'), cep_to_coords('53401050'), cep_to_coords('53570990'), cep_to_coords('50751365'), cep_to_coords('56331240'), cep_to_coords('55152200'), cep_to_coords('53401770'), cep_to_coords('50780630'), cep_to_coords('53130271'), cep_to_coords('53560180'), cep_to_coords('56181000'), cep_to_coords('53530520'), cep_to_coords('54290120'), cep_to_coords('52280404'), cep_to_coords('53160380'), cep_to_coords('51010660'), cep_to_coords('50660040'), cep_to_coords('54705380'), cep_to_coords('20710020'), cep_to_coords('54410372'), cep_to_coords('50450015'), cep_to_coords('54340210'), cep_to_coords('51600030'), cep_to_coords('52160850'), cep_to_coords('56310190'), cep_to_coords('53615460'), cep_to_coords('52051282'), cep_to_coords('53416730'), cep_to_coords('54320623'), cep_to_coords('50080560'), cep_to_coords('53040210'), cep_to_coords('50090440'), cep_to_coords('54960470'), cep_to_coords('51460312'), cep_to_coords('51335290'), cep_to_coords('50610230'), cep_to_coords('53210445'), cep_to_coords('50070230'), cep_to_coords('54150330'), cep_to_coords('52041585'), cep_to_coords('53150130'), cep_to_coords('51190640'), cep_to_coords('51340330'), cep_to_coords('52160350'), cep_to_coords('54360176'), cep_to_coords('54620173'), cep_to_coords('47800000'), cep_to_coords('51340226'), cep_to_coords('53370291'), cep_to_coords('53200380'), cep_to_coords('53320389'), cep_to_coords('56610970'), cep_to_coords('50910100'), cep_to_coords('53070370'), cep_to_coords('52031450'), cep_to_coords('50110100'), cep_to_coords('89204050'), cep_to_coords('53403820'), cep_to_coords('53560121'), cep_to_coords('51290170'), cep_to_coords('54740560'), cep_to_coords('54250382'), cep_to_coords('54767125'), cep_to_coords('54400105'), cep_to_coords('54705490'), cep_to_coords('52090250'), cep_to_coords('52280780'), cep_to_coords('50781690'), cep_to_coords('52150168'), cep_to_coords('53220750'), cep_to_coords('52190475'), cep_to_coords('58250340'), cep_to_coords('53510430'), cep_to_coords('53430010'), cep_to_coords('55641265'), cep_to_coords('55642000'), cep_to_coords('55641105'), cep_to_coords('55640675'), cep_to_coords('54529240'), cep_to_coords('26302100'), cep_to_coords('54150603'), cep_to_coords('53350846'), cep_to_coords('54280420'), cep_to_coords('54325025'), cep_to_coords('51010015'), cep_to_coords('19907236'), cep_to_coords('53160163'), cep_to_coords('55642630'), cep_to_coords('52090561'), cep_to_coords('08111300'), cep_to_coords('54510270'), cep_to_coords('55293455'), cep_to_coords('55292190'), cep_to_coords('55644260'), cep_to_coords('55645899'), cep_to_coords('55642068'), cep_to_coords('55641790'), cep_to_coords('55641818'), cep_to_coords('53413350'), cep_to_coords('56313030'), cep_to_coords('56313070'), cep_to_coords('52211230'), cep_to_coords('53370791'), cep_to_coords('50930150'), cep_to_coords('54140180'), cep_to_coords('53330390'), cep_to_coords('52080100'), cep_to_coords('50912302'), cep_to_coords('53442190'), cep_to_coords('56503253'), cep_to_coords('53402832'), cep_to_coords('56304030'), cep_to_coords('52050410'), cep_to_coords('51250400'), cep_to_coords('54355691'), cep_to_coords('54740460'), cep_to_coords('50870700'), cep_to_coords('54315101'), cep_to_coords('54315391'), cep_to_coords('51280390'), cep_to_coords('54440490'), cep_to_coords('54767083'), cep_to_coords('52221405'), cep_to_coords('53110680'), cep_to_coords('50786640'), cep_to_coords('53431285'), cep_to_coords('50740533'), cep_to_coords('53660970'), cep_to_coords('54315047'), cep_to_coords('54330065'), cep_to_coords('53620040'), cep_to_coords('54440170'), cep_to_coords('54450030'), cep_to_coords('54350235'), cep_to_coords('18208100'), cep_to_coords('05560000'), cep_to_coords('51270370'), cep_to_coords('50110070'), cep_to_coords('52191510'), cep_to_coords('54220705'), cep_to_coords('54120083'), cep_to_coords('53625753'), cep_to_coords('54490133'), cep_to_coords('28890000'), cep_to_coords('54525420'), cep_to_coords('54315580'), cep_to_coords('54470090'), cep_to_coords('51150003'), cep_to_coords('52071320'), cep_to_coords('50680270'), cep_to_coords('50770220'), cep_to_coords('53422260'), cep_to_coords('54786170'), cep_to_coords('54753812'), cep_to_coords('50791181'), cep_to_coords('54765550'), cep_to_coords('54300201'), cep_to_coords('54589220'), cep_to_coords('50850304'), cep_to_coords('12686647'), cep_to_coords('53260140'), cep_to_coords('56784010'), cep_to_coords('54780010'), cep_to_coords('53625513'), cep_to_coords('54450135'), cep_to_coords('50770020'), cep_to_coords('54705392'), cep_to_coords('52111220'), cep_to_coords('53250200'), cep_to_coords('53421600'), cep_to_coords('54767200'), cep_to_coords('51160330'), cep_to_coords('51290070'), cep_to_coords('51340740'), cep_to_coords('50080740'), cep_to_coords('51260232'), cep_to_coords('53580130'), cep_to_coords('52130151'), cep_to_coords('60360840'), cep_to_coords('54420805'), cep_to_coords('50820100'), cep_to_coords('51345180'), cep_to_coords('50761605'), cep_to_coords('53210061'), cep_to_coords('54753070'), cep_to_coords('51220260'), cep_to_coords('52070090'), cep_to_coords('50680790'), cep_to_coords('50980795'), cep_to_coords('52081192'), cep_to_coords('51290130'), cep_to_coords('50920130'), cep_to_coords('53423480'), cep_to_coords('50910520'), cep_to_coords('56509435'), cep_to_coords('56509825'), cep_to_coords('50721300'), cep_to_coords('50900030'), cep_to_coords('50670665'), cep_to_coords('53620360'), cep_to_coords('52121400'), cep_to_coords('53640214'), cep_to_coords('41211550'), cep_to_coords('52135689'), cep_to_coords('53421845'), cep_to_coords('50791512'), cep_to_coords('50860370'), cep_to_coords('50830480'), cep_to_coords('50721778'), cep_to_coords('53625115'), cep_to_coords('53290240'), cep_to_coords('53010230'), cep_to_coords('51230970'), cep_to_coords('54410050'), cep_to_coords('54280695'), cep_to_coords('54530530'), cep_to_coords('54410350'), cep_to_coords('70262513'), cep_to_coords('53421115'), cep_to_coords('01307010'), cep_to_coords('56505370'), cep_to_coords('50791366'), cep_to_coords('50920152'), cep_to_coords('50970480'), cep_to_coords('56316510'), cep_to_coords('50690620'), cep_to_coords('53470417'), cep_to_coords('51250310'), cep_to_coords('52280506'), cep_to_coords('53220010'), cep_to_coords('53370912'), cep_to_coords('55816540'), cep_to_coords('53220600'), cep_to_coords('53130180'), cep_to_coords('52071490'), cep_to_coords('53170035'), cep_to_coords('53560248'), cep_to_coords('53320000'), cep_to_coords('54325690'), cep_to_coords('53370320'), cep_to_coords('54070100'), cep_to_coords('54783030'), cep_to_coords('50110250'), cep_to_coords('52191030'), cep_to_coords('52250521'), cep_to_coords('53280152'), cep_to_coords('50110743'), cep_to_coords('55028430'), cep_to_coords('54490501'), cep_to_coords('51120100'), cep_to_coords('52081745'), cep_to_coords('54515470'), cep_to_coords('52071150'), cep_to_coords('52091420'), cep_to_coords('54210341'), cep_to_coords('51290620'), cep_to_coords('55293445'), cep_to_coords('56328190'), cep_to_coords('55645108'), cep_to_coords('56508080'), cep_to_coords('56302340'), cep_to_coords('55036232'), cep_to_coords('55022080'), cep_to_coords('52291072'), cep_to_coords('50980800'), cep_to_coords('53405370'), cep_to_coords('55815100'), cep_to_coords('56590305'), cep_to_coords('53443480'), cep_to_coords('54340500'), cep_to_coords('53520240'), cep_to_coords('51310019'), cep_to_coords('54320081'), cep_to_coords('54352390'), cep_to_coords('54340010'), cep_to_coords('54520683'), cep_to_coords('56519010'), cep_to_coords('52071350'), cep_to_coords('54150230'), cep_to_coords('51330461'), cep_to_coords('53260222'), cep_to_coords('06454000'), cep_to_coords('52211030'), cep_to_coords('51260570'), cep_to_coords('53403495'), cep_to_coords('50721220'), cep_to_coords('54325765'), cep_to_coords('52090508'), cep_to_coords('55642670'), cep_to_coords('55010490'), cep_to_coords('08563230'), cep_to_coords('54450240'), cep_to_coords('53530750'), cep_to_coords('53230240'), cep_to_coords('54759165'), cep_to_coords('54705085'), cep_to_coords('50010024'), cep_to_coords('50771640'), cep_to_coords('52130463'), cep_to_coords('53110750'), cep_to_coords('54430230'), cep_to_coords('54090439'), cep_to_coords('70324813'), cep_to_coords('53210050'), cep_to_coords('54774050'), cep_to_coords('50731665'), cep_to_coords('53570027'), cep_to_coords('53540080'), cep_to_coords('50110800'), cep_to_coords('52091177'), cep_to_coords('52090260'), cep_to_coords('52140231'), cep_to_coords('50781680'), cep_to_coords('52131221'), cep_to_coords('53260280'), cep_to_coords('52211060'), cep_to_coords('50920682'), cep_to_coords('69057550'), cep_to_coords('52081200'), cep_to_coords('53550070'), cep_to_coords('54730041'), cep_to_coords('50931203'), cep_to_coords('50060750'), cep_to_coords('58707420'), cep_to_coords('54580820'), cep_to_coords('54320001'), cep_to_coords('55292052'), cep_to_coords('53280400'), cep_to_coords('53060300'), cep_to_coords('55195018'), cep_to_coords('53545550'), cep_to_coords('54370172'), cep_to_coords('53645290'), cep_to_coords('50790270'), cep_to_coords('23071420'), cep_to_coords('52131308'), cep_to_coords('53429710'), cep_to_coords('53401620'), cep_to_coords('56503025'), cep_to_coords('56509545'), cep_to_coords('56513080'), cep_to_coords('53170330'), cep_to_coords('51200750'), cep_to_coords('54280245'), cep_to_coords('53402270'), cep_to_coords('53130220'), cep_to_coords('53439900'), cep_to_coords('54310161'), cep_to_coords('53530310'), cep_to_coords('54140608'), cep_to_coords('50070045'), cep_to_coords('53441321'), cep_to_coords('54240655'), cep_to_coords('53402014'), cep_to_coords('55190591'), cep_to_coords('54518235'), cep_to_coords('56502230'), cep_to_coords('56502230 '), cep_to_coords('55819380'), cep_to_coords('55195542'), cep_to_coords('55819325'), cep_to_coords('57525000'), cep_to_coords('50050015'), cep_to_coords('50771690'), cep_to_coords('50711470'), cep_to_coords('50620470'), cep_to_coords('50751610'), cep_to_coords('51330590'), cep_to_coords('54360054'), cep_to_coords('50870750'), cep_to_coords('52131050'), cep_to_coords('54705600'), cep_to_coords('53444160'), cep_to_coords('55004141'), cep_to_coords('54330469'), cep_to_coords('52165080'), cep_to_coords('52012260'), cep_to_coords('54752640'), cep_to_coords('53010350'), cep_to_coords('53550020'), cep_to_coords('52091628'), cep_to_coords('53200330'), cep_to_coords('54400045'), cep_to_coords('55641698'), cep_to_coords('52050011'), cep_to_coords('52291040'), cep_to_coords('52130600'), cep_to_coords('52170150'), cep_to_coords('56323660'), cep_to_coords('50636501'), cep_to_coords('54705284'), cep_to_coords('55470030'), cep_to_coords('53419285'), cep_to_coords('50810050'), cep_to_coords('51280530'), cep_to_coords('53510110'), cep_to_coords('55644652'), cep_to_coords('50865170'), cep_to_coords('54786100'), cep_to_coords('54786080'), cep_to_coords('54705200'), cep_to_coords('54786021'), cep_to_coords('51260700'), cep_to_coords('52061145'), cep_to_coords('50720100'), cep_to_coords('52280364'), cep_to_coords('11654068'), cep_to_coords('53250020'), cep_to_coords('57768180'), cep_to_coords('53620425'), cep_to_coords('55608500'), cep_to_coords('53444100'), cep_to_coords('52490110'), cep_to_coords('51230410'), cep_to_coords('52090430'), cep_to_coords('51190380'), cep_to_coords('52350870'), cep_to_coords('50040330'), cep_to_coords('31081964'), cep_to_coords('54100212'), cep_to_coords('54370123'), cep_to_coords('53409230'), cep_to_coords('55004460'), cep_to_coords('55608045'), cep_to_coords('51300450'), cep_to_coords('52211670'), cep_to_coords('58082000'), cep_to_coords('54525180'), cep_to_coords('52070201'), cep_to_coords('54460565'), cep_to_coords('53550015'), cep_to_coords('54070190'), cep_to_coords('55158140'), cep_to_coords('50940730'), cep_to_coords('50791109'), cep_to_coords('52071162'), cep_to_coords('54090050'), cep_to_coords('55299600'), cep_to_coords('53404358'), cep_to_coords('54759600'), cep_to_coords('53230580'), cep_to_coords('54792370'), cep_to_coords('50980280'), cep_to_coords('54765380'), cep_to_coords('53180680'), cep_to_coords('52130281'), cep_to_coords('54777300'), cep_to_coords('54460150'), cep_to_coords('54240745'), cep_to_coords('50070220'), cep_to_coords('54783750'), cep_to_coords('54753092'), cep_to_coords('54759630'), cep_to_coords('51111060'), cep_to_coords('55024660'), cep_to_coords('53409740'), cep_to_coords('54730130'), cep_to_coords('51150650'), cep_to_coords('55020211'), cep_to_coords('55292282'), cep_to_coords('52081531'), cep_to_coords('55641440'), cep_to_coords('55643660'), cep_to_coords('55644395'), cep_to_coords('55643102'), cep_to_coords('53403810'), cep_to_coords('56313580'), cep_to_coords('55293450'), cep_to_coords('53640210'), cep_to_coords('50731390'), cep_to_coords('51190320'), cep_to_coords('52390180'), cep_to_coords('52125200'), cep_to_coords('54330758'), cep_to_coords('54170024'), cep_to_coords('55006203'), cep_to_coords('02075040'), cep_to_coords('50781280'), cep_to_coords('53550051'), cep_to_coords('54365420'), cep_to_coords('54723055'), cep_to_coords('54521010'), cep_to_coords('52160475'), cep_to_coords('51220140'), cep_to_coords('50761660'), cep_to_coords('55643340'), cep_to_coords('53090160'), cep_to_coords('53403730'), cep_to_coords('54340190'), cep_to_coords('51021489'), cep_to_coords('52211570'), cep_to_coords('41750300'), cep_to_coords('52070340'), cep_to_coords('54320320'), cep_to_coords('51021440'), cep_to_coords('54756100'), cep_to_coords('50865210'), cep_to_coords('50820690'), cep_to_coords('54410272'), cep_to_coords('53620700'), cep_to_coords('52071260'), cep_to_coords('50870470'), cep_to_coords('50050560'), cep_to_coords('53545735'), cep_to_coords('52171045'), cep_to_coords('53444415'), cep_to_coords('52291063'), cep_to_coords('50670560'), cep_to_coords('50680690'), cep_to_coords('50791530'), cep_to_coords('53250111'), cep_to_coords('09010000'), cep_to_coords('54150100'), cep_to_coords('54735794'), cep_to_coords('52131666'), cep_to_coords('51022000'), cep_to_coords('55664000'), cep_to_coords('52090145'), cep_to_coords('52160805'), cep_to_coords('56312205'), cep_to_coords('50050490'), cep_to_coords('52111470'), cep_to_coords('54220210'), cep_to_coords('52210450'), cep_to_coords('53637030'), cep_to_coords('50770360'), cep_to_coords('52111433'), cep_to_coords('52131085'), cep_to_coords('51310240'), cep_to_coords('51345530'), cep_to_coords('55123011'), cep_to_coords('54771640'), cep_to_coords('53370740'), cep_to_coords('54325171'), cep_to_coords('55020640'), cep_to_coords('11531000'), cep_to_coords('55194327'), cep_to_coords('54340725'), cep_to_coords('54360104'), cep_to_coords('53320280'), cep_to_coords('54756380'), cep_to_coords('53405730'), cep_to_coords('08695080'), cep_to_coords('51260765'), cep_to_coords('55640160'), cep_to_coords('50865020'), cep_to_coords('51030761'), cep_to_coords('55027590'), cep_to_coords('51150350'), cep_to_coords('50771650'), cep_to_coords('55194460'), cep_to_coords('55192100'), cep_to_coords('55190774'), cep_to_coords('55006282'), cep_to_coords('53637150'), cep_to_coords('49020020'), cep_to_coords('55027060'), cep_to_coords('52070320'), cep_to_coords('54735160'), cep_to_coords('50875030'), cep_to_coords('55265490'), cep_to_coords('50090390'), cep_to_coords('52140110'), cep_to_coords('52141100'), cep_to_coords('54330382'), cep_to_coords('54230057'), cep_to_coords('56909242'), cep_to_coords('53370000'), cep_to_coords('54230131'), cep_to_coords('54230150'), cep_to_coords('54753520'), cep_to_coords('51010025'), cep_to_coords('20830270'), cep_to_coords('50090800'), cep_to_coords('54768300'), cep_to_coords('55014045'), cep_to_coords('55006025'), cep_to_coords('55294368'), cep_to_coords('54270435'), cep_to_coords('54774765'), cep_to_coords('53030290'), cep_to_coords('56302470'), cep_to_coords('56503074'), cep_to_coords('54250605'), cep_to_coords('55610015'), cep_to_coords('51030225'), cep_to_coords('50640300'), cep_to_coords('56506903'), cep_to_coords('54430232'), cep_to_coords('53444340'), cep_to_coords('53370130'), cep_to_coords('51110190'), cep_to_coords('53130200'), cep_to_coords('53130670'), cep_to_coords('54270401'), cep_to_coords('54920310'), cep_to_coords('54715160'), cep_to_coords('53260441'), cep_to_coords('52210231'), cep_to_coords('52160310'), cep_to_coords('52060115'), cep_to_coords('50912330'), cep_to_coords('53635150'), cep_to_coords('56510330'), cep_to_coords('50680050'), cep_to_coords('55819070'), cep_to_coords('55819265'), cep_to_coords('52071161'), cep_to_coords('54100401'), cep_to_coords('55602600'), cep_to_coords('54786640'), cep_to_coords('54792590'), cep_to_coords('53330700'), cep_to_coords('54780540'), cep_to_coords('53530472'), cep_to_coords('53640200'), cep_to_coords('54355410'), cep_to_coords('50980475'), cep_to_coords('50740222'), cep_to_coords('50751100'), cep_to_coords('55010410'), cep_to_coords('53422360'), cep_to_coords('56509814'), cep_to_coords('53620012'), cep_to_coords('54280673'), cep_to_coords('53510160'), cep_to_coords('53280710'), cep_to_coords('52020013'), cep_to_coords('52348120'), cep_to_coords('54756358'), cep_to_coords('50940080'), cep_to_coords('55644040'), cep_to_coords('54170510'), cep_to_coords('50770450'), cep_to_coords('55800999'), cep_to_coords('53540270'), cep_to_coords('50020020'), cep_to_coords('54735290'), cep_to_coords('54762835'), cep_to_coords('54519050'), cep_to_coords('54735680'), cep_to_coords('51240510'), cep_to_coords('50780150'), cep_to_coords('56322590'), cep_to_coords('53423020'), cep_to_coords('53545100'), cep_to_coords('55019150'), cep_to_coords('52721170'), cep_to_coords('52120175'), cep_to_coords('53180340'), cep_to_coords('55642610'), cep_to_coords('53610322'), cep_to_coords('53160680'), cep_to_coords('53240490'), cep_to_coords('54330407'), cep_to_coords('50760345'), cep_to_coords('53620655'), cep_to_coords('51345101'), cep_to_coords('51761340'), cep_to_coords('53409180'), cep_to_coords('56332352'), cep_to_coords('54404900'), cep_to_coords('51300550'), cep_to_coords('51300410'), cep_to_coords('55592971'), cep_to_coords('53060515'), cep_to_coords('55016180'), cep_to_coords('54350085'), cep_to_coords('52131495'), cep_to_coords('50630320'), cep_to_coords('54430421'), cep_to_coords('55042010'), cep_to_coords('54460320'), cep_to_coords('53629700'), cep_to_coords('50761610'), cep_to_coords('56313060'), cep_to_coords('56322200'), cep_to_coords('52090395'), cep_to_coords('52210351'), cep_to_coords('56326310'), cep_to_coords('54325530'), cep_to_coords('55815340'), cep_to_coords('55004180'), cep_to_coords('50630110'), cep_to_coords('54100590'), cep_to_coords('57086130'), cep_to_coords('53545280'), cep_to_coords('52191060'), cep_to_coords('52250500'), cep_to_coords('54700825'), cep_to_coords('53350090'), cep_to_coords('55298360'), cep_to_coords('52160290'), cep_to_coords('54320370'), cep_to_coords('53441762'), cep_to_coords('54765135'), cep_to_coords('52140510'), cep_to_coords('53421480'), cep_to_coords('53441470'), cep_to_coords('54310030'), cep_to_coords('10208890'), cep_to_coords('54753351'), cep_to_coords('53420080'), cep_to_coords('53403400'), cep_to_coords('53417275'), cep_to_coords('54210511'), cep_to_coords('54735265'), cep_to_coords('53370400'), cep_to_coords('53420670'), cep_to_coords('53240360'), cep_to_coords('56304410'), cep_to_coords('53421160'), cep_to_coords('53240380'), cep_to_coords('50740300'), cep_to_coords('50670320'), cep_to_coords('56320785'), cep_to_coords('50780280'), cep_to_coords('51130580'), cep_to_coords('50800050'), cep_to_coords('50750620'), cep_to_coords('53360180'), cep_to_coords('03371000'), cep_to_coords('52390100'), cep_to_coords('52140100'), cep_to_coords('50020050'), cep_to_coords('55815070'), cep_to_coords('54720736'), cep_to_coords('53330510'), cep_to_coords('53150220'), cep_to_coords('51010055'), cep_to_coords('54777400'), cep_to_coords('53407540'), cep_to_coords('50940330'), cep_to_coords('53407010'), cep_to_coords('50050900'), cep_to_coords('51030790'), cep_to_coords('47560420'), cep_to_coords('54401039'), cep_to_coords('54260150'), cep_to_coords('53260440'), cep_to_coords('55298380'), cep_to_coords('53080050'), cep_to_coords('53425060'), cep_to_coords('55295595'), cep_to_coords('52060082'), cep_to_coords('53431520'), cep_to_coords('53425460'), cep_to_coords('53010130'), cep_to_coords('51290520'), cep_to_coords('52051370'), cep_to_coords('55642370'), cep_to_coords('55024715'), cep_to_coords('53370621'), cep_to_coords('51190020'), cep_to_coords('23042021'), cep_to_coords('53605065'), cep_to_coords('55855000'), cep_to_coords('51240250'), cep_to_coords('53370730'), cep_to_coords('50751086'), cep_to_coords('52280570'), cep_to_coords('54210055'), cep_to_coords('54753778'), cep_to_coords('55644175'), cep_to_coords('50751590'), cep_to_coords('52071235'), cep_to_coords('55295970'), cep_to_coords('51280250'), cep_to_coords('51275040'), cep_to_coords('51150220'), cep_to_coords('54777210'), cep_to_coords('50771580'), cep_to_coords('50660050'), cep_to_coords('54140620'), cep_to_coords('54762590'), cep_to_coords('54759335'), cep_to_coords('55640460'), cep_to_coords('51020905'), cep_to_coords('54325400'), cep_to_coords('50760158'), cep_to_coords('54730270'), cep_to_coords('53545080'), cep_to_coords('53413351'), cep_to_coords('50090100'), cep_to_coords('50751622'), cep_to_coords('53090330'), cep_to_coords('50070055'), cep_to_coords('52090030'), cep_to_coords('54240650'), cep_to_coords('54325063'), cep_to_coords('54730285'), cep_to_coords('50050105'), cep_to_coords('50870530'), cep_to_coords('52211163'), cep_to_coords('53423823'), cep_to_coords('52010465'), cep_to_coords('50690150'), cep_to_coords('52511080'), cep_to_coords('51260310'), cep_to_coords('55644070'), cep_to_coords('53640000'), cep_to_coords('51340017'), cep_to_coords('53560250'), cep_to_coords('52540070'), cep_to_coords('53540070'), cep_to_coords('54330825'), cep_to_coords('50980505'), cep_to_coords('54733280'), cep_to_coords('54435000'), cep_to_coords('53200310'), cep_to_coords('52190495'), cep_to_coords('55641744'), cep_to_coords('54260360'), cep_to_coords('52040380'), cep_to_coords('54740832'), cep_to_coords('51340115'), cep_to_coords('55399000'), cep_to_coords('54325020'), cep_to_coords('53220630'), cep_to_coords('54240550'), cep_to_coords('54310441'), cep_to_coords('50010080'), cep_to_coords('54350644'), cep_to_coords('55777000'), cep_to_coords('55550972'), cep_to_coords('50720385'), cep_to_coords('55641905'), cep_to_coords('54786340'), cep_to_coords('53080055'), cep_to_coords('55014091'), cep_to_coords('32143430'), cep_to_coords('50090030'), cep_to_coords('50830160'), cep_to_coords('50660010'), cep_to_coords('55030340'), cep_to_coords('54786070'), cep_to_coords('54365070'), cep_to_coords('53370262'), cep_to_coords('13456411'), cep_to_coords('51290501'), cep_to_coords('51250280'), cep_to_coords('53090190'), cep_to_coords('52140280'), cep_to_coords('53580150'), cep_to_coords('55296630'), cep_to_coords('5600000000'), cep_to_coords('55016710'), cep_to_coords('50020520'), cep_to_coords('551900000'), cep_to_coords('56312645'), cep_to_coords('55021010'), cep_to_coords('56310780'), cep_to_coords('55014656'), cep_to_coords('54210070'), cep_to_coords('51220130'), cep_to_coords('54368160'), cep_to_coords('50711460'), cep_to_coords('50711510'), cep_to_coords('56503695'), cep_to_coords('53240700'), cep_to_coords('56512120'), cep_to_coords('55194100'), cep_to_coords('53404150'), cep_to_coords('41720075'), cep_to_coords('50060330'), cep_to_coords('51275100'), cep_to_coords('56509120'), cep_to_coords('52020260'), cep_to_coords('52031212'), cep_to_coords('54762712'), cep_to_coords('53240460'), cep_to_coords('50980240'), cep_to_coords('50760575'), cep_to_coords('54789320'), cep_to_coords('50100415'), cep_to_coords('53429785'), cep_to_coords('56506591'), cep_to_coords('50630661'), cep_to_coords('54270445'), cep_to_coords('50900010'), cep_to_coords('53413490'), cep_to_coords('52011901'), cep_to_coords('51240551'), cep_to_coords('50910340'), cep_to_coords('52051440'), cep_to_coords('51240140'), cep_to_coords('52181250'), cep_to_coords('54519030'), cep_to_coords('53413132'), cep_to_coords('50080150'), cep_to_coords('52011220'), cep_to_coords('52041151'), cep_to_coords('68721000'), cep_to_coords('50090180'), cep_to_coords('56332113'), cep_to_coords('55034271'), cep_to_coords('50680755'), cep_to_coords('50630591'), cep_to_coords('52090870'), cep_to_coords('55291290'), cep_to_coords('53630835'), cep_to_coords('53830835'), cep_to_coords('52291051'), cep_to_coords('54430322'), cep_to_coords('53530434'), cep_to_coords('54430680'), cep_to_coords('55036405'), cep_to_coords('55026021'), cep_to_coords('56520420'), cep_to_coords('52081795'), cep_to_coords('54220991'), cep_to_coords('52121430'), cep_to_coords('50209302'), cep_to_coords('56313680'), cep_to_coords('50970140'), cep_to_coords('53422090'), cep_to_coords('53530033'), cep_to_coords('53520220'), cep_to_coords('50720515'), cep_to_coords('53437600'), cep_to_coords('51230460'), cep_to_coords('50870460'), cep_to_coords('55027605'), cep_to_coords('55036532'), cep_to_coords('59144098'), cep_to_coords('53050455'), cep_to_coords('51130430'), cep_to_coords('50980710'), cep_to_coords('54250580'), cep_to_coords('50720840'), cep_to_coords('51340780'), cep_to_coords('54230442'), cep_to_coords('54160505'), cep_to_coords('53060280'), cep_to_coords('54737200'), cep_to_coords('53615055'), cep_to_coords('56515570'), cep_to_coords('52121361'), cep_to_coords('51335430'), cep_to_coords('51021450'), cep_to_coords('53060230'), cep_to_coords('51010170'), cep_to_coords('55026380'), cep_to_coords('53413040'), cep_to_coords('55292280'), cep_to_coords('55293277'), cep_to_coords('54759290'), cep_to_coords('54520735'), cep_to_coords('53530760'), cep_to_coords('51340295'), cep_to_coords('55022575'), cep_to_coords('55004210'), cep_to_coords('54100030'), cep_to_coords('50080100'), cep_to_coords('52061525'), cep_to_coords('55291745'), cep_to_coords('51217650'), cep_to_coords('51130480'), cep_to_coords('53637227'), cep_to_coords('53060705'), cep_to_coords('54490540'), cep_to_coords('54330430'), cep_to_coords('50920651'), cep_to_coords('09760000'), cep_to_coords('06864020'), cep_to_coords('51240800'), cep_to_coords('54250180'), cep_to_coords('50810290'), cep_to_coords('50740036'), cep_to_coords('53615548'), cep_to_coords('53580140'), cep_to_coords('52081504'), cep_to_coords('51340722'), cep_to_coords('53413560'), cep_to_coords('52071360'), cep_to_coords('52040240'), cep_to_coords('52121190'), cep_to_coords('54070270'), cep_to_coords('51180467'), cep_to_coords('51280350'), cep_to_coords('51160090'), cep_to_coords('50110630'), cep_to_coords('54320325'), cep_to_coords('54735413'), cep_to_coords('53120151'), cep_to_coords('52191075'), cep_to_coords('51330080'), cep_to_coords('53350270'), cep_to_coords('55643792'), cep_to_coords('53435460'), cep_to_coords('54756405'), cep_to_coords('51029319'), cep_to_coords('50900470'), cep_to_coords('52081385'), cep_to_coords('21330080'), cep_to_coords('50060560'), cep_to_coords('53545580'), cep_to_coords('54140720'), cep_to_coords('56906261'), cep_to_coords('50751460'), cep_to_coords('55192385'), cep_to_coords('53421121'), cep_to_coords('54460670'), cep_to_coords('52071450'), cep_to_coords('55012280'), cep_to_coords('54352300'), cep_to_coords('50751140'), cep_to_coords('50720300'), cep_to_coords('38430000'), cep_to_coords('53050050'), cep_to_coords('53431295'), cep_to_coords('52061260'), cep_to_coords('50620210'), cep_to_coords('50110391'), cep_to_coords('57606060'), cep_to_coords('50850320'), cep_to_coords('53160310'), cep_to_coords('50620365'), cep_to_coords('54766137'), cep_to_coords('54170280'), cep_to_coords('52191301'), cep_to_coords('52130460'), cep_to_coords('55042200'), cep_to_coords('55192608'), cep_to_coords('55150101'), cep_to_coords('53420160'), cep_to_coords('52060480'), cep_to_coords('54325470'), cep_to_coords('52111435'), cep_to_coords('56330550'), cep_to_coords('56332327'), cep_to_coords('52190280'), cep_to_coords('55040075'), cep_to_coords('54160970'), cep_to_coords('50930200'), cep_to_coords('52280508'), cep_to_coords('50771101'), cep_to_coords('54340775'), cep_to_coords('54250430'), cep_to_coords('54450430'), cep_to_coords('53250430'), cep_to_coords('55038758'), cep_to_coords('50670285'), cep_to_coords('52041420'), cep_to_coords('55022750'), cep_to_coords('50070210'), cep_to_coords('50731150'), cep_to_coords('52270230'), cep_to_coords('55680970'), cep_to_coords('56316010'), cep_to_coords('55813665'), cep_to_coords('52111611'), cep_to_coords('53230390'), cep_to_coords('51150248'), cep_to_coords('51190500'), cep_to_coords('51335130'), cep_to_coords('54430430'), cep_to_coords('53401560'), cep_to_coords('53413520'), cep_to_coords('52101013'), cep_to_coords('56328637'), cep_to_coords('50080420'), cep_to_coords('78045350'), cep_to_coords('56317100'), cep_to_coords('56318580'), cep_to_coords('58120300'), cep_to_coords('54280726'), cep_to_coords('53435510'), cep_to_coords('54720802'), cep_to_coords('55544564'), cep_to_coords('53520990'), cep_to_coords('54580190'), cep_to_coords('50070250'), cep_to_coords('51300142'), cep_to_coords('51180495'), cep_to_coords('55028140'), cep_to_coords('53610053'), cep_to_coords('52091383'), cep_to_coords('53080620'), cep_to_coords('52211123'), cep_to_coords('50730541'), cep_to_coords('53170460'), cep_to_coords('50640305'), cep_to_coords('53421091'), cep_to_coords('54771740'), cep_to_coords('54110140'), cep_to_coords('52210240'), cep_to_coords('51040252'), cep_to_coords('53150100'), cep_to_coords('50080670'), cep_to_coords('52121225'), cep_to_coords('53211310'), cep_to_coords('56519120'), cep_to_coords('56509806'), cep_to_coords('55608010'), cep_to_coords('54774170'), cep_to_coords('50910310'), cep_to_coords('54522005'), cep_to_coords('53160020'), cep_to_coords('53350360'), cep_to_coords('54720005'), cep_to_coords('54735115'), cep_to_coords('54756280'), cep_to_coords('51130610'), cep_to_coords('55038500'), cep_to_coords('55031426'), cep_to_coords('55032160'), cep_to_coords('52031200'), cep_to_coords('51240512'), cep_to_coords('52490530'), cep_to_coords('53530484'), cep_to_coords('54170780'), cep_to_coords('53300250'), cep_to_coords('50294410'), cep_to_coords('56306250'), cep_to_coords('55642130'), cep_to_coords('55640265'), cep_to_coords('52150100'), cep_to_coords('53180041'), cep_to_coords('55016150'), cep_to_coords('55020760'), cep_to_coords('55040190'), cep_to_coords('53400010'), cep_to_coords('53421750'), cep_to_coords('54410486'), cep_to_coords('50751330'), cep_to_coords('55038030'), cep_to_coords('55032380'), cep_to_coords('55043060'), cep_to_coords('55024800'), cep_to_coords('55006235'), cep_to_coords('55036150'), cep_to_coords('55022430'), cep_to_coords('55130972'), cep_to_coords('55036795'), cep_to_coords('55030630'), cep_to_coords('55020061'), cep_to_coords('55010030'), cep_to_coords('55020340'), cep_to_coords('54100511'), cep_to_coords('77270000'), cep_to_coords('52160250'), cep_to_coords('54410475'), cep_to_coords('52171445'), cep_to_coords('53431685'), cep_to_coords('54080170'), cep_to_coords('54275000'), cep_to_coords('50751081'), cep_to_coords('68515000'), cep_to_coords('54430210'), cep_to_coords('52040170'), cep_to_coords('53402605'), cep_to_coords('54220580'), cep_to_coords('54160465'), cep_to_coords('54580770'), cep_to_coords('53240530'), cep_to_coords('54758080'), cep_to_coords('51340224'), cep_to_coords('53300313'), cep_to_coords('53441750'), cep_to_coords('53290400'), cep_to_coords('56507015'), cep_to_coords('56503580'), cep_to_coords('55034205'), cep_to_coords('53637575'), cep_to_coords('52104000'), cep_to_coords('52131460'), cep_to_coords('52160820'), cep_to_coords('54100658'), cep_to_coords('53431125'), cep_to_coords('50900170'), cep_to_coords('53190201'), cep_to_coords('52071326'), cep_to_coords('50790405'), cep_to_coords('54720294'), cep_to_coords('55643160'), cep_to_coords('52120005'), cep_to_coords('53615600'), cep_to_coords('54100485'), cep_to_coords('38703204'), cep_to_coords('57442000'), cep_to_coords('55020081'), cep_to_coords('54100551'), cep_to_coords('53423520'), cep_to_coords('52121125'), cep_to_coords('52131521'), cep_to_coords('56302370'), cep_to_coords('50660410'), cep_to_coords('55294792'), cep_to_coords('55292520'), cep_to_coords('55008110'), cep_to_coords('55008093'), cep_to_coords('50820670'), cep_to_coords('53560293'), cep_to_coords('54280531'), cep_to_coords('54768505'), cep_to_coords('54280210'), cep_to_coords('50040260'), cep_to_coords('50110015'), cep_to_coords('56509340'), cep_to_coords('52111120'), cep_to_coords('50970420'), cep_to_coords('54762450'), cep_to_coords('50601651'), cep_to_coords('55014211'), cep_to_coords('55622000'), cep_to_coords('52111685'), cep_to_coords('52090465'), cep_to_coords('55010220'), cep_to_coords('54460223'), cep_to_coords('54430223'), cep_to_coords('53610308'), cep_to_coords('55008210'), cep_to_coords('54120728'), cep_to_coords('55297011'), cep_to_coords('54230060'), cep_to_coords('50640820'), cep_to_coords('07750000'), cep_to_coords('54525000'), cep_to_coords('55642745'), cep_to_coords('50135130'), cep_to_coords('55630210'), cep_to_coords('53320140'), cep_to_coords('53421271'), cep_to_coords('51180270'), cep_to_coords('52130456'), cep_to_coords('51190520'), cep_to_coords('50750280'), cep_to_coords('55038438'), cep_to_coords('55010111'), cep_to_coords('56320200'), cep_to_coords('56000340'), cep_to_coords('54240565'), cep_to_coords('55020151'), cep_to_coords('56314210'), cep_to_coords('52211610'), cep_to_coords('60791080'), cep_to_coords('53320230'), cep_to_coords('53550500'), cep_to_coords('53240551'), cep_to_coords('56310150'), cep_to_coords('51345370'), cep_to_coords('50960570'), cep_to_coords('56326060'), cep_to_coords('56232380'), cep_to_coords('56323280'), cep_to_coords('53141190'), cep_to_coords('54140140'), cep_to_coords('54120685'), cep_to_coords('54490202'), cep_to_coords('50720070'), cep_to_coords('25160280'), cep_to_coords('56312576'), cep_to_coords('54759400'), cep_to_coords('54785407'), cep_to_coords('54230280'), cep_to_coords('54470010'), cep_to_coords('51170980'), cep_to_coords('54170720'), cep_to_coords('52090090'), cep_to_coords('51530530'), cep_to_coords('02758000'), cep_to_coords('53421531'), cep_to_coords('53140131'), cep_to_coords('53300330'), cep_to_coords('53417030'), cep_to_coords('53210665'), cep_to_coords('50020055'), cep_to_coords('53429460'), cep_to_coords('51130535'), cep_to_coords('05663010'), cep_to_coords('54330185'), cep_to_coords('53637250'), cep_to_coords('54340610'), cep_to_coords('54410260'), cep_to_coords('55150595'), cep_to_coords('51102026'), cep_to_coords('52171060'), cep_to_coords('03279000'), cep_to_coords('54786025'), cep_to_coords('69074230'), cep_to_coords('54410250'), cep_to_coords('55032572'), cep_to_coords('55002100'), cep_to_coords('50875210'), cep_to_coords('56506385'), cep_to_coords('56322580'), cep_to_coords('50791231'), cep_to_coords('54290112'), cep_to_coords('56322680'), cep_to_coords('56312665'), cep_to_coords('52171380'), cep_to_coords('50731210'), cep_to_coords('52632100'), cep_to_coords('54767690'), cep_to_coords('50110597'), cep_to_coords('54350435'), cep_to_coords('52130970'), cep_to_coords('55608401'), cep_to_coords('50010460'), cep_to_coords('51130021'), cep_to_coords('55641775'), cep_to_coords('51120060'), cep_to_coords('51320444'), cep_to_coords('53637805'), cep_to_coords('53190650'), cep_to_coords('55036390'), cep_to_coords('53210831'), cep_to_coords('53647610'), cep_to_coords('55364761'), cep_to_coords('53437510'), cep_to_coords('50050127'), cep_to_coords('50870160'), cep_to_coords('51345450'), cep_to_coords('52710140'), cep_to_coords('56323150'), cep_to_coords('50741320'), cep_to_coords('50760057'), cep_to_coords('55195623'), cep_to_coords('53421790'), cep_to_coords('53090043'), cep_to_coords('53540380'), cep_to_coords('54786500'), cep_to_coords('54783440'), cep_to_coords('55644218'), cep_to_coords('52211370'), cep_to_coords('52110458'), cep_to_coords('53620693'), cep_to_coords('52090182'), cep_to_coords('53090490'), cep_to_coords('50790314'), cep_to_coords('50740442'), cep_to_coords('50790606'), cep_to_coords('52121680'), cep_to_coords('51170591'), cep_to_coords('55296735'), cep_to_coords('51290200'), cep_to_coords('52081400'), cep_to_coords('54280421'), cep_to_coords('54444000'), cep_to_coords('54120675'), cep_to_coords('53407450'), cep_to_coords('54490505'), cep_to_coords('55012530'), cep_to_coords('53423130'), cep_to_coords('51010145'), cep_to_coords('50850112'), cep_to_coords('51350100'), cep_to_coords('56506530'), cep_to_coords('53080080'), cep_to_coords('50865155'), cep_to_coords('52111630'), cep_to_coords('53270150'), cep_to_coords('53370380'), cep_to_coords('54400404'), cep_to_coords('54760000'), cep_to_coords('53120270'), cep_to_coords('54720165'), cep_to_coords('55026193'), cep_to_coords('54350355'), cep_to_coords('54150785'), cep_to_coords('55027460'), cep_to_coords('52091024'), cep_to_coords('52091330'), cep_to_coords('51130160'), cep_to_coords('52140205'), cep_to_coords('53640303'), cep_to_coords('54505140'), cep_to_coords('56909162'), cep_to_coords('55014405'), cep_to_coords('21339210'), cep_to_coords('56505020'), cep_to_coords('559000000'), cep_to_coords('55293460'), cep_to_coords('53605665'), cep_to_coords('56903060'), cep_to_coords('54325351'), cep_to_coords('52290000'), cep_to_coords('55014210'), cep_to_coords('56306357'), cep_to_coords('56505080'), cep_to_coords('56302020'), cep_to_coords('56364456'), cep_to_coords('56304445'), cep_to_coords('51275360'), cep_to_coords('54330674'), cep_to_coords('56310763'), cep_to_coords('55658970'), cep_to_coords('53370825'), cep_to_coords('53415450'), cep_to_coords('50650100'), cep_to_coords('50800210'), cep_to_coords('53545130'), cep_to_coords('50040160'), cep_to_coords('54705055'), cep_to_coords('53350380'), cep_to_coords('53190830'), cep_to_coords('53640610'), cep_to_coords('56309110'), cep_to_coords('55030130'), cep_to_coords('53413370'), cep_to_coords('53422430'), cep_to_coords('52090513'), cep_to_coords('26121996'), cep_to_coords('52211660'), cep_to_coords('53210101'), cep_to_coords('54330464'), cep_to_coords('50741141'), cep_to_coords('53650769'), cep_to_coords('53111111'), cep_to_coords('53416250'), cep_to_coords('53402155'), cep_to_coords('53212032'), cep_to_coords('53550660'), cep_to_coords('52090120'), cep_to_coords('52090042'), cep_to_coords('56515310'), cep_to_coords('56509020'), cep_to_coords('53270251'), cep_to_coords('54735350'), cep_to_coords('54880000'), cep_to_coords('53530396'), cep_to_coords('56310762'), cep_to_coords('54230293'), cep_to_coords('55536000'), cep_to_coords('51345010'), cep_to_coords('52090700'), cep_to_coords('54440287'), cep_to_coords('53417380'), cep_to_coords('53640354'), cep_to_coords('53020160'), cep_to_coords('54330677'), cep_to_coords('53920310'), cep_to_coords('51200000'), cep_to_coords('52291044'), cep_to_coords('52280441'), cep_to_coords('50110066'), cep_to_coords('54080070'), cep_to_coords('51250450'), cep_to_coords('53417052'), cep_to_coords('51020002'), cep_to_coords('53570023'), cep_to_coords('54325700'), cep_to_coords('18520000'), cep_to_coords('51266004'), cep_to_coords('52070642'), cep_to_coords('55195254'), cep_to_coords('52090440'), cep_to_coords('55030152'), cep_to_coords('54720095'), cep_to_coords('52280504'), cep_to_coords('54727195'), cep_to_coords('54505480'), cep_to_coords('54355320'), cep_to_coords('55540100'), cep_to_coords('53335090'), cep_to_coords('53090430'), cep_to_coords('53407090'), cep_to_coords('52130381'), cep_to_coords('55643694'), cep_to_coords('50110793'), cep_to_coords('51170395'), cep_to_coords('55819150'), cep_to_coords('51270082'), cep_to_coords('53310971'), cep_to_coords('51150580'), cep_to_coords('54330315'), cep_to_coords('55293310'), cep_to_coords('54280681'), cep_to_coords('50985685'), cep_to_coords('53180100'), cep_to_coords('54505907'), cep_to_coords('55010440'), cep_to_coords('53413470'), cep_to_coords('50410480'), cep_to_coords('54280661'), cep_to_coords('54170147'), cep_to_coords('54290260'), cep_to_coords('56912270'), cep_to_coords('56942270'), cep_to_coords('55825500'), cep_to_coords('58825000'), cep_to_coords('48909067'), cep_to_coords('54365505'), cep_to_coords('56250970'), cep_to_coords('53550720'), cep_to_coords('56302050'), cep_to_coords('56306290'), cep_to_coords('52091460'), cep_to_coords('54410075'), cep_to_coords('54495670'), cep_to_coords('52081740'), cep_to_coords('54210150'), cep_to_coords('52111240'), cep_to_coords('56503411'), cep_to_coords('56506230'), cep_to_coords('56512300'), cep_to_coords('53401190'), cep_to_coords('50940360'), cep_to_coords('50711055'), cep_to_coords('52050316'), cep_to_coords('54767750'), cep_to_coords('50870170'), cep_to_coords('53405460'), cep_to_coords('56308115'), cep_to_coords('54230559'), cep_to_coords('54520620'), cep_to_coords('52221320'), cep_to_coords('50060240'), cep_to_coords('51250530'), cep_to_coords('51340040'), cep_to_coords('53640100'), cep_to_coords('01222001'), cep_to_coords('53220240'), cep_to_coords('54735070'), cep_to_coords('51010500'), cep_to_coords('51180507'), cep_to_coords('54410512'), cep_to_coords('50110727'), cep_to_coords('50791390'), cep_to_coords('56512430'), cep_to_coords('50390923'), cep_to_coords('50200000'), cep_to_coords('54730201'), cep_to_coords('54753660'), cep_to_coords('53620666'), cep_to_coords('53443510'), cep_to_coords('53360700'), cep_to_coords('50771020'), cep_to_coords('56323510'), cep_to_coords('53620270'), cep_to_coords('50110140'), cep_to_coords('54720822'), cep_to_coords('55014670'), cep_to_coords('51290630'), cep_to_coords('50760185'), cep_to_coords('56303992'), cep_to_coords('52090765'), cep_to_coords('53429755'), cep_to_coords('53399400'), cep_to_coords('54100512'), cep_to_coords('53404300'), cep_to_coords('52040251'), cep_to_coords('56503765'), cep_to_coords('51350260'), cep_to_coords('50980038'), cep_to_coords('54780455'), cep_to_coords('54753990'), cep_to_coords('53650590'), cep_to_coords('50730440'), cep_to_coords('54422540'), cep_to_coords('50681600'), cep_to_coords('50970340'), cep_to_coords('53530440'), cep_to_coords('53060010'), cep_to_coords('53080671'), cep_to_coords('54100572'), cep_to_coords('53050190'), cep_to_coords('55026210'), cep_to_coords('53025122'), cep_to_coords('55297811'), cep_to_coords('54739710'), cep_to_coords('51310091'), cep_to_coords('51340070'), cep_to_coords('55294528'), cep_to_coords('52291102'), cep_to_coords('50293092'), cep_to_coords('50710550'), cep_to_coords('53433530'), cep_to_coords('54150170'), cep_to_coords('56306360'), cep_to_coords('52051031'), cep_to_coords('53550780'), cep_to_coords('54020000'), cep_to_coords('56306410'), cep_to_coords('55640720'), cep_to_coords('52071040'), cep_to_coords('53425560'), cep_to_coords('51345462'), cep_to_coords('53443150'), cep_to_coords('55036183'), cep_to_coords('54470390'), cep_to_coords('53635035'), cep_to_coords('54300064'), cep_to_coords('59721260'), cep_to_coords('54410560'), cep_to_coords('50130260'), cep_to_coords('53100105'), cep_to_coords('54220620'), cep_to_coords('50810010'), cep_to_coords('53520150'), cep_to_coords('50731095'), cep_to_coords('52121015'), cep_to_coords('53370610'), cep_to_coords('50630550'), cep_to_coords('52041240'), cep_to_coords('55819780'), cep_to_coords('53170309'), cep_to_coords('56512291'), cep_to_coords('50640170'), cep_to_coords('52071215'), cep_to_coords('54212444'), cep_to_coords('53545740'), cep_to_coords('54210280'), cep_to_coords('51340180'), cep_to_coords('50394093'), cep_to_coords('56600970'), cep_to_coords('53260550'), cep_to_coords('51110287'), cep_to_coords('52131310'), cep_to_coords('43420940'), cep_to_coords('51510160'), cep_to_coords('50390403'), cep_to_coords('51111110'), cep_to_coords('52270240'), cep_to_coords('54490215'), cep_to_coords('50120590'), cep_to_coords('51270720'), cep_to_coords('55641055'), cep_to_coords('53220132'), cep_to_coords('54160612'), cep_to_coords('50960490'), cep_to_coords('54170155'), cep_to_coords('54170135'), cep_to_coords('54150096'), cep_to_coords('54150190'), cep_to_coords('55642490'), cep_to_coords('52230510'), cep_to_coords('56280999'), cep_to_coords('563000000'), cep_to_coords('55016345'), cep_to_coords('53180092'), cep_to_coords('53413460'), cep_to_coords('50865140'), cep_to_coords('54315490'), cep_to_coords('50390493'), cep_to_coords('55155390'), cep_to_coords('53550790'), cep_to_coords('54021380'), cep_to_coords('56959000'), cep_to_coords('56312805'), cep_to_coords('54160274'), cep_to_coords('55194378'), cep_to_coords('Logradouro'), cep_to_coords('56312060'), cep_to_coords('55819130'), cep_to_coords('55298560'), cep_to_coords('53080040'), cep_to_coords('53525170'), cep_to_coords('53525790'), cep_to_coords('51051360'), cep_to_coords('53390350'), cep_to_coords('55028135'), cep_to_coords('54020560'), cep_to_coords('52071300'), cep_to_coords('50875150'), cep_to_coords('56160780'), cep_to_coords('51113032'), cep_to_coords('53240040'), cep_to_coords('56507330'), cep_to_coords('56506390'), cep_to_coords('50850262'), cep_to_coords('50820180'), cep_to_coords('54170550'), cep_to_coords('50129319'), cep_to_coords('50625030'), cep_to_coords('54325800'), cep_to_coords('52221165'), cep_to_coords('54320805'), cep_to_coords('52080368'), cep_to_coords('56313190'), cep_to_coords('50761475'), cep_to_coords('51150610'), cep_to_coords('55036290'), cep_to_coords('52050037'), cep_to_coords('51130640'), cep_to_coords('53451421'), cep_to_coords('57500000'), cep_to_coords('53402022'), cep_to_coords('51021210'), cep_to_coords('53630784'), cep_to_coords('53637070'), cep_to_coords('51161410'), cep_to_coords('55014130'), cep_to_coords('52401000'), cep_to_coords('54780081'), cep_to_coords('53230971'), cep_to_coords('56310490'), cep_to_coords('50290302'), cep_to_coords('50071355'), cep_to_coords('54280535'), cep_to_coords('53210063'), cep_to_coords('50030330'), cep_to_coords('50761275'), cep_to_coords('55608320'), cep_to_coords('55810160'), cep_to_coords('54765435'), cep_to_coords('50960370'), cep_to_coords('54580292'), cep_to_coords('54230285'), cep_to_coords('54330160'), cep_to_coords('54580646'), cep_to_coords('56904210'), cep_to_coords('54110070'), cep_to_coords('55032450'), cep_to_coords('55557800'), cep_to_coords('55298640'), cep_to_coords('55018575'), cep_to_coords('50711270'), cep_to_coords('54315410'), cep_to_coords('11120958'), cep_to_coords('53530442'), cep_to_coords('53409380'), cep_to_coords('53403493'), cep_to_coords('55296450'), cep_to_coords('54260570'), cep_to_coords('53640170'), cep_to_coords('53110472'), cep_to_coords('55021315'), cep_to_coords('54070230'), cep_to_coords('53402354'), cep_to_coords('53403560'), cep_to_coords('50030660'), cep_to_coords('54730777'), cep_to_coords('54360158'), cep_to_coords('56460999'), cep_to_coords('59040050'), cep_to_coords('53150340'), cep_to_coords('86401599'), cep_to_coords('54782990'), cep_to_coords('51010690'), cep_to_coords('52111235'), cep_to_coords('53417350'), cep_to_coords('51030750'), cep_to_coords('54470092'), cep_to_coords('54140150'), cep_to_coords('55038700'), cep_to_coords('55019275'), cep_to_coords('54786350'), cep_to_coords('55130001'), cep_to_coords('50940410'), cep_to_coords('53010050'), cep_to_coords('50601411'), cep_to_coords('55818410'), cep_to_coords('62500000'), cep_to_coords('56636000'), cep_to_coords('55363000'), cep_to_coords('54796720'), cep_to_coords('54359265'), cep_to_coords('55641694'), cep_to_coords('52651160'), cep_to_coords('50759645'), cep_to_coords('54781010'), cep_to_coords('55641601'), cep_to_coords('54440015'), cep_to_coords('54220095'), cep_to_coords('56509795'), cep_to_coords('54280550'), cep_to_coords('50006090'), cep_to_coords('55155670'), cep_to_coords('52051010'), cep_to_coords('51320230'), cep_to_coords('56505310'), cep_to_coords('53425760'), cep_to_coords('54410520'), cep_to_coords('50810710'), cep_to_coords('53417705'), cep_to_coords('53431792'), cep_to_coords('56302410'), cep_to_coords('54380293'), cep_to_coords('53120030'), cep_to_coords('55194742'), cep_to_coords('53620697'), cep_to_coords('52390350'), cep_to_coords('52050440'), cep_to_coords('56909496'), cep_to_coords('50790640'), cep_to_coords('55002495'), cep_to_coords('55606299'), cep_to_coords('53560133'), cep_to_coords('56440970'), cep_to_coords('54753325'), cep_to_coords('56314220'), cep_to_coords('56511120'), cep_to_coords('55190350'), cep_to_coords('53650140'), cep_to_coords('54080075'), cep_to_coords('54340335'), cep_to_coords('55570999'), cep_to_coords('54489950'), cep_to_coords('54100032'), cep_to_coords('52070221'), cep_to_coords('55292761'), cep_to_coords('54460035'), cep_to_coords('51310540'), cep_to_coords('54490575'), cep_to_coords('55561000'), cep_to_coords('50680480'), cep_to_coords('56515180'), cep_to_coords('53417260'), cep_to_coords('54495080'), cep_to_coords('51071280'), cep_to_coords('28108213'), cep_to_coords('54522120'), cep_to_coords('54410300'), cep_to_coords('55024530'), cep_to_coords('53635650'), cep_to_coords('53585148'), cep_to_coords('56585148'), cep_to_coords('50120312'), cep_to_coords('53635580'), cep_to_coords('55030285'), cep_to_coords('53620103'), cep_to_coords('55614420'), cep_to_coords('56503685'), cep_to_coords('50651250'), cep_to_coords('55194190'), cep_to_coords('54410487'), cep_to_coords('54230160'), cep_to_coords('51200180'), cep_to_coords('52850150'), cep_to_coords('54580845'), cep_to_coords('54450340'), cep_to_coords('54220272'), cep_to_coords('50548050'), cep_to_coords('54170525'), cep_to_coords('55040475'), cep_to_coords('20740250'), cep_to_coords('58041110'), cep_to_coords('56320420'), cep_to_coords('55020601'), cep_to_coords('56320725'), cep_to_coords('56756000'), cep_to_coords('53431620'), cep_to_coords('50198151'), cep_to_coords('54210250'), cep_to_coords('54160611'), cep_to_coords('53401545'), cep_to_coords('50006057'), cep_to_coords('55019375'), cep_to_coords('51270110'), cep_to_coords('52291575'), cep_to_coords('55298565'), cep_to_coords('54332015'), cep_to_coords('45980000'), cep_to_coords('53433645'), cep_to_coords('15810472'), cep_to_coords('53200280'), cep_to_coords('52081625'), cep_to_coords('52211852'), cep_to_coords('51200110'), cep_to_coords('50791370'), cep_to_coords('50050054'), cep_to_coords('51270081'), cep_to_coords('50000055'), cep_to_coords('56507290'), cep_to_coords('50781621'), cep_to_coords('52090555'), cep_to_coords('53409835'), cep_to_coords('50680490'), cep_to_coords('53425652'), cep_to_coords('56503108'), cep_to_coords('52060020'), cep_to_coords('55817700'), cep_to_coords('56313730'), cep_to_coords('55196225'), cep_to_coords('54320152'), cep_to_coords('54210550'), cep_to_coords('55021255'), cep_to_coords('50800370'), cep_to_coords('53437080'), cep_to_coords('51100515'), cep_to_coords('53300400'), cep_to_coords('53419090'), cep_to_coords('53070230'), cep_to_coords('53637054'), cep_to_coords('50000003'), cep_to_coords('50670030'), cep_to_coords('54720192'), cep_to_coords('52091245'), cep_to_coords('53100000'), cep_to_coords('52150060'), cep_to_coords('51010350'), cep_to_coords('51061170'), cep_to_coords('55192235'), cep_to_coords('50910290'), cep_to_coords('53620663'), cep_to_coords('52662066'), cep_to_coords('50940390'), cep_to_coords('50050020'), cep_to_coords('50970220'), cep_to_coords('51530020'), cep_to_coords('53210490'), cep_to_coords('52050085'), cep_to_coords('51270692'), cep_to_coords('54090455'), cep_to_coords('52170190'), cep_to_coords('54041380'), cep_to_coords('53444139'), cep_to_coords('54300122'), cep_to_coords('51300460'), cep_to_coords('52280380'), cep_to_coords('55050000'), cep_to_coords('55608416'), cep_to_coords('52011480'), cep_to_coords('50040909'), cep_to_coords('50221220'), cep_to_coords('27081996'), cep_to_coords('50620500'), cep_to_coords('53435080'), cep_to_coords('52120710'), cep_to_coords('54450121'), cep_to_coords('54280150'), cep_to_coords('51335170'), cep_to_coords('54315630'), cep_to_coords('54410165'), cep_to_coords('54517250'), cep_to_coords('56316776'), cep_to_coords('52190220'), cep_to_coords('55000200'), cep_to_coords('55155480'), cep_to_coords('55155548'), cep_to_coords('53620672'), cep_to_coords('54350730'), cep_to_coords('53500990'), cep_to_coords('51320320'), cep_to_coords('53407690'), cep_to_coords('54330010'), cep_to_coords('52091122'), cep_to_coords('50707876'), cep_to_coords('50780490'), cep_to_coords('55028092'), cep_to_coords('54750100'), cep_to_coords('56321500'), cep_to_coords('52150121'), cep_to_coords('50930095'), cep_to_coords('54768045'), cep_to_coords('52160487'), cep_to_coords('54777620'), cep_to_coords('53545310'), cep_to_coords('53290348'), cep_to_coords('56423525'), cep_to_coords('52081532'), cep_to_coords('55815095'), cep_to_coords('52090323'), cep_to_coords('55295060'), cep_to_coords('55294491'), cep_to_coords('53417360'), cep_to_coords('55299782'), cep_to_coords('56316702'), cep_to_coords('52010050'), cep_to_coords('54720125'), cep_to_coords('53605695'), cep_to_coords('52320090'), cep_to_coords('52110166'), cep_to_coords('56912610'), cep_to_coords('54759370'), cep_to_coords('51260740'), cep_to_coords('56317392'), cep_to_coords('56332660'), cep_to_coords('52090374'), cep_to_coords('54330042'), cep_to_coords('54210580'), cep_to_coords('52160670'), cep_to_coords('50515151'), cep_to_coords('51340221'), cep_to_coords('50791463'), cep_to_coords('50761755'), cep_to_coords('51020330'), cep_to_coords('50050520'), cep_to_coords('50790025'), cep_to_coords('56515170'), cep_to_coords('54220347'), cep_to_coords('54227000'), cep_to_coords('00011000'), cep_to_coords('51000411'), cep_to_coords('51250430'), cep_to_coords('84794887'), cep_to_coords('54762756'), cep_to_coords('53090100'), cep_to_coords('50320090'), cep_to_coords('53060060'), cep_to_coords('53020010'), cep_to_coords('54110035'), cep_to_coords('56512350'), cep_to_coords('55030260'), cep_to_coords('56503610'), cep_to_coords('55026231'), cep_to_coords('52060910'), cep_to_coords('55292420'), cep_to_coords('53190185'), cep_to_coords('54080190'), cep_to_coords('53425250'), cep_to_coords('53550050'), cep_to_coords('54589035'), cep_to_coords('50970650'), cep_to_coords('51400070'), cep_to_coords('54400070'), cep_to_coords('50915040'), cep_to_coords('54350665'), cep_to_coords('50900720'), cep_to_coords('23091974'), cep_to_coords('28101965'), cep_to_coords('15091967'), cep_to_coords('50270370'), cep_to_coords('50960520'), cep_to_coords('55620200'), cep_to_coords('53585255'), cep_to_coords('53405520'), cep_to_coords('54280241'), cep_to_coords('50505151'), cep_to_coords('54410195'), cep_to_coords('51500500'), cep_to_coords('51240760'), cep_to_coords('54400225'), cep_to_coords('52510110'), cep_to_coords('52711030'), cep_to_coords('52165180'), cep_to_coords('16592182'), cep_to_coords('51120270'), cep_to_coords('51020142'), cep_to_coords('54777600'), cep_to_coords('50580120'), cep_to_coords('50123012'), cep_to_coords('52080850'), cep_to_coords('70590380'), cep_to_coords('53520165'), cep_to_coords('56509712'), cep_to_coords('50910490'), cep_to_coords('55552000'), cep_to_coords('55292145'), cep_to_coords('50720700'), cep_to_coords('50960100'), cep_to_coords('52020215'), cep_to_coords('50820170'), cep_to_coords('50790105'), cep_to_coords('53571130'), cep_to_coords('56327085'), cep_to_coords('54325590'), cep_to_coords('53415400'), cep_to_coords('55195027'), cep_to_coords('54270380'), cep_to_coords('55192512'), cep_to_coords('53370770'), cep_to_coords('55157240'), cep_to_coords('51340090'), cep_to_coords('51120320'), cep_to_coords('50184515'), cep_to_coords('55040415'), cep_to_coords('56515600'), cep_to_coords('53260390'), cep_to_coords('52041490'), cep_to_coords('51340320'), cep_to_coords('53427085'), cep_to_coords('50790261'), cep_to_coords('95458939'), cep_to_coords('54320230'), cep_to_coords('52050251'), cep_to_coords('54410695'), cep_to_coords('55195614'), cep_to_coords('51011081'), cep_to_coords('54780610'), cep_to_coords('51118050'), cep_to_coords('53422959'), cep_to_coords('54768240'), cep_to_coords('55340970'), cep_to_coords('56308045'), cep_to_coords('50030310'), cep_to_coords('52160980'), cep_to_coords('25687436'), cep_to_coords('00001000'), cep_to_coords('55021075'), cep_to_coords('51011101'), cep_to_coords('51753779'), cep_to_coords('50690080'), cep_to_coords('51515450'), cep_to_coords('56903204'), cep_to_coords('53210390'), cep_to_coords('52031075'), cep_to_coords('54330477'), cep_to_coords('54090230'), cep_to_coords('53430437'), cep_to_coords('52121212'), cep_to_coords('50761490'), cep_to_coords('55192230'), cep_to_coords('50031023'), cep_to_coords('53201302'), cep_to_coords('48908241'), cep_to_coords('51345620'), cep_to_coords('51771470'), cep_to_coords('50771470'), cep_to_coords('55293590'), cep_to_coords('55294320'), cep_to_coords('54430216'), cep_to_coords('54420450'), cep_to_coords('54783080'), cep_to_coords('55006420'), cep_to_coords('55028240'), cep_to_coords('21170270'), cep_to_coords('52040060'), cep_to_coords('55008241'), cep_to_coords('55024430'), cep_to_coords('53120280'), cep_to_coords('56316616'), cep_to_coords('50791250'), cep_to_coords('51345320'), cep_to_coords('51052110'), cep_to_coords('55152530'), cep_to_coords('55152480'), cep_to_coords('50080770'), cep_to_coords('51160360'), cep_to_coords('55153543'), cep_to_coords('50080750'), cep_to_coords('54275055'), cep_to_coords('50511510'), cep_to_coords('51220065'), cep_to_coords('53404010'), cep_to_coords('50791253'), cep_to_coords('52111705'), cep_to_coords('54330136'), cep_to_coords('55296165'), cep_to_coords('55612420'), cep_to_coords('56515270'), cep_to_coords('50151515'), cep_to_coords('52121041'), cep_to_coords('53404190'), cep_to_coords('55153500'), cep_to_coords('55027050'), cep_to_coords('52490400'), cep_to_coords('54403060'), cep_to_coords('52140400'), cep_to_coords('52070171'), cep_to_coords('53550690'), cep_to_coords('54140032'), cep_to_coords('54900000'), cep_to_coords('40293092'), cep_to_coords('50102901'), cep_to_coords('50390349'), cep_to_coords('50293029'), cep_to_coords('54270072'), cep_to_coords('50239029'), cep_to_coords('50293039'), cep_to_coords('50292309'), cep_to_coords('50090909'), cep_to_coords('50751230'), cep_to_coords('56512206'), cep_to_coords('53130510'), cep_to_coords('53404450'), cep_to_coords('56519330'), cep_to_coords('29039990'), cep_to_coords('90000000'), cep_to_coords('53320043'), cep_to_coords('52090357'), cep_to_coords('51280170'), cep_to_coords('51280480'), cep_to_coords('51240750'), cep_to_coords('51280401'), cep_to_coords('53401665'), cep_to_coords('51421000'), cep_to_coords('50810560'), cep_to_coords('52490140'), cep_to_coords('50740441'), cep_to_coords('53049750'), cep_to_coords('54511519'), cep_to_coords('53444330'), cep_to_coords('53412000'), cep_to_coords('55299450'), cep_to_coords('55435971'), cep_to_coords('56318050'), cep_to_coords('56511110'), cep_to_coords('56507345'), cep_to_coords('56320410'), cep_to_coords('52111609'), cep_to_coords('53404110'), cep_to_coords('53441573'), cep_to_coords('53250266'), cep_to_coords('52390340'), cep_to_coords('53413620'), cep_to_coords('41010240'), cep_to_coords('55819440'), cep_to_coords('50123991'), cep_to_coords('55158308'), cep_to_coords('52110300'), cep_to_coords('09071996'), cep_to_coords('50721150'), cep_to_coords('56512121'), cep_to_coords('53545225'), cep_to_coords('53545640'), cep_to_coords('54720295'), cep_to_coords('53370185'), cep_to_coords('50151550'), cep_to_coords('51250270'), cep_to_coords('50781700'), cep_to_coords('54360021'), cep_to_coords('53431630'), cep_to_coords('53439811'), cep_to_coords('53565714'), cep_to_coords('56320400'), cep_to_coords('52110180'), cep_to_coords('52140250'), cep_to_coords('50761775'), cep_to_coords('53540390'), cep_to_coords('51330010'), cep_to_coords('54250015'), cep_to_coords('55025275'), cep_to_coords('54230018'), cep_to_coords('52050400'), cep_to_coords('52051400'), cep_to_coords('55985000'), cep_to_coords('52140360'), cep_to_coords('50140250'), cep_to_coords('53419251'), cep_to_coords('51340522'), cep_to_coords('56509105'), cep_to_coords('54783700'), cep_to_coords('55293181'), cep_to_coords('50720213'), cep_to_coords('50731175'), cep_to_coords('53433190'), cep_to_coords('55155120'), cep_to_coords('55156280'), cep_to_coords('55151745'), cep_to_coords('54430412'), cep_to_coords('50780370'), cep_to_coords('54280676'), cep_to_coords('55153160'), cep_to_coords('51290350'), cep_to_coords('55195626'), cep_to_coords('50781200'), cep_to_coords('54270405'), cep_to_coords('50115150'), cep_to_coords('50740540'), cep_to_coords('55240333'), cep_to_coords('54756383'), cep_to_coords('54490184'), cep_to_coords('52070636'), cep_to_coords('55643532'), cep_to_coords('53120241'), cep_to_coords('55291611'), cep_to_coords('54580520'), cep_to_coords('50123901'), cep_to_coords('51150520'), cep_to_coords('52120321'), cep_to_coords('50810492'), cep_to_coords('54410615'), cep_to_coords('50130090'), cep_to_coords('55037106'), cep_to_coords('56309780'), cep_to_coords('56323340'), cep_to_coords('53429110'), cep_to_coords('03121993'), cep_to_coords('50125200'), cep_to_coords('52091612'), cep_to_coords('54000720'), cep_to_coords('50960170'), cep_to_coords('52070545'), cep_to_coords('53409733'), cep_to_coords('52710340'), cep_to_coords('21021970'), cep_to_coords('55295200'), cep_to_coords('54517190'), cep_to_coords('54140270'), cep_to_coords('54410373'), cep_to_coords('51021180'), cep_to_coords('55297490'), cep_to_coords('50770110'), cep_to_coords('50760250'), cep_to_coords('55112200'), cep_to_coords('54100437'), cep_to_coords('55395970'), cep_to_coords('55030540'), cep_to_coords('51260708'), cep_to_coords('54430211'), cep_to_coords('53415740'), cep_to_coords('52221325'), cep_to_coords('53427591'), cep_to_coords('53545590'), cep_to_coords('51041200'), cep_to_coords('56506160'), cep_to_coords('50620490'), cep_to_coords('54510200'), cep_to_coords('52191195'), cep_to_coords('52090284'), cep_to_coords('50740510'), cep_to_coords('50560670'), cep_to_coords('50920710'), cep_to_coords('54365360'), cep_to_coords('50650270'), cep_to_coords('52171021'), cep_to_coords('50150505'), cep_to_coords('54350638'), cep_to_coords('52160415'), cep_to_coords('50915500'), cep_to_coords('55155260'), cep_to_coords('55158770'), cep_to_coords('50451050'), cep_to_coords('50790415'), cep_to_coords('52160780'), cep_to_coords('54140420'), cep_to_coords('14091961'), cep_to_coords('50000005'), cep_to_coords('54160594'), cep_to_coords('55154505'), cep_to_coords('55154580'), cep_to_coords('55130999'), cep_to_coords('25390000'), cep_to_coords('51111120'), cep_to_coords('54762635'), cep_to_coords('55529000'), cep_to_coords('54240665'), cep_to_coords('51222310'), cep_to_coords('54756430'), cep_to_coords('50870720'), cep_to_coords('56000900'), cep_to_coords('56903580'), cep_to_coords('54325695'), cep_to_coords('51011902'), cep_to_coords('53510540'), cep_to_coords('53540740'), cep_to_coords('53520120'), cep_to_coords('55607700'), cep_to_coords('51360560'), cep_to_coords('54330673'), cep_to_coords('54210312'), cep_to_coords('54330142'), cep_to_coords('51260214'), cep_to_coords('52120170'), cep_to_coords('50050140'), cep_to_coords('54786410'), cep_to_coords('50920070'), cep_to_coords('50970070'), cep_to_coords('55299415'), cep_to_coords('54240600'), cep_to_coords('55028172'), cep_to_coords('50930060'), cep_to_coords('54756655'), cep_to_coords('54785840'), cep_to_coords('53230320'), cep_to_coords('51230281'), cep_to_coords('50192901'), cep_to_coords('54759055'), cep_to_coords('50620090'), cep_to_coords('53300370'), cep_to_coords('54460386'), cep_to_coords('54460385'), cep_to_coords('53330330'), cep_to_coords('55022310'), cep_to_coords('52110007'), cep_to_coords('52090183'), cep_to_coords('50875100'), cep_to_coords('54170570'), cep_to_coords('55014358'), cep_to_coords('56909240'), cep_to_coords('55297265'), cep_to_coords('53401235'), cep_to_coords('55294728'), cep_to_coords('54320465'), cep_to_coords('54325007'), cep_to_coords('55291812'), cep_to_coords('54510032'), cep_to_coords('55020153'), cep_to_coords('55019345'), cep_to_coords('55151620'), cep_to_coords('55158115'), cep_to_coords('55150790'), cep_to_coords('54745520'), cep_to_coords('50740055'), cep_to_coords('56327075'), cep_to_coords('55614210'), cep_to_coords('50390110'), cep_to_coords('53401613'), cep_to_coords('54320215'), cep_to_coords('55541000'), cep_to_coords('50790590'), cep_to_coords('52060435'), cep_to_coords('54090320'), cep_to_coords('50155051'), cep_to_coords('55813520'), cep_to_coords('52131280'), cep_to_coords('56328570'), cep_to_coords('55153340'), cep_to_coords('52439230'), cep_to_coords('52081440'), cep_to_coords('53650817'), cep_to_coords('51340232'), cep_to_coords('53300450'), cep_to_coords('51240680'), cep_to_coords('52060271'), cep_to_coords('55024280'), cep_to_coords('53443700'), cep_to_coords('55151640'), cep_to_coords('53625834'), cep_to_coords('50761670'), cep_to_coords('53435190'), cep_to_coords('53422370'), cep_to_coords('54440055'), cep_to_coords('55030395'), cep_to_coords('53160470'), cep_to_coords('52120374'), cep_to_coords('26280000'), cep_to_coords('56313770'), cep_to_coords('55190401'), cep_to_coords('50771820'), cep_to_coords('53415280'), cep_to_coords('51345820'), cep_to_coords('50865280'), cep_to_coords('52041064'), cep_to_coords('51400160'), cep_to_coords('54400270'), cep_to_coords('52150163'), cep_to_coords('59720870'), cep_to_coords('54280132'), cep_to_coords('56787310'), cep_to_coords('52127000'), cep_to_coords('55293237'), cep_to_coords('50970265'), cep_to_coords('50678830'), cep_to_coords('50670830'), cep_to_coords('55292665'), cep_to_coords('21454545'), cep_to_coords('53620525'), cep_to_coords('53424181'), cep_to_coords('56464635'), cep_to_coords('54759570'), cep_to_coords('54330778'), cep_to_coords('20601050'), cep_to_coords('52120580'), cep_to_coords('54520315'), cep_to_coords('11184273'), cep_to_coords('54783490'), cep_to_coords('55191639'), cep_to_coords('55028090'), cep_to_coords('53575192'), cep_to_coords('50650060'), cep_to_coords('56330625'), cep_to_coords('53350100'), cep_to_coords('55192654'), cep_to_coords('54150650'), cep_to_coords('59912398'), cep_to_coords('50612302'), cep_to_coords('44927000'), cep_to_coords('52111404'), cep_to_coords('51260610'), cep_to_coords('51275480'), cep_to_coords('54230001'), cep_to_coords('51023000'), cep_to_coords('52031130'), cep_to_coords('54735736'), cep_to_coords('50080340'), cep_to_coords('54090522'), cep_to_coords('54365380'), cep_to_coords('51230111'), cep_to_coords('50711040'), cep_to_coords('41697839'), cep_to_coords('50080310'), cep_to_coords('53320460'), cep_to_coords('52111612'), cep_to_coords('54741380'), cep_to_coords('51110010'), cep_to_coords('53300712'), cep_to_coords('50505050'), cep_to_coords('54330222'), cep_to_coords('54320070'), cep_to_coords('51345580'), cep_to_coords('53520520'), cep_to_coords('54315128'), cep_to_coords('54768280'), cep_to_coords('55294525'), cep_to_coords('50515050'), cep_to_coords('55293025'), cep_to_coords('56509256'), cep_to_coords('55296410'), cep_to_coords('56205000'), cep_to_coords('54542170'), cep_to_coords('55015040'), cep_to_coords('54140046'), cep_to_coords('50120451'), cep_to_coords('51460030'), cep_to_coords('53000700'), cep_to_coords('56320805'), cep_to_coords('54762544'), cep_to_coords('55012330'), cep_to_coords('50123210'), cep_to_coords('54771605'), cep_to_coords('50690665'), cep_to_coords('53479400'), cep_to_coords('54170556'), cep_to_coords('54786013'), cep_to_coords('53410230'), cep_to_coords('51240650'), cep_to_coords('50830830'), cep_to_coords('55190530'), cep_to_coords('55190399'), cep_to_coords('54756677'), cep_to_coords('56313640'), cep_to_coords('54090063'), cep_to_coords('56512042'), cep_to_coords('54120703'), cep_to_coords('55296620'), cep_to_coords('53453020'), cep_to_coords('55819760'), cep_to_coords('51130135'), cep_to_coords('55207000'), cep_to_coords('56313540'), cep_to_coords('54230045'), cep_to_coords('52280112'), cep_to_coords('50030080'), cep_to_coords('51035160'), cep_to_coords('54530110'), cep_to_coords('53421250'), cep_to_coords('50741515'), cep_to_coords('56328070'), cep_to_coords('50750240'), cep_to_coords('53420340'), cep_to_coords('54330450')


# In[82]:


print(coordenadasrow15426to20425)


# In[83]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in row15426to20425.tolist():
    result.append(''.join(pattern.findall(item)))


# In[84]:


print(result)


# In[85]:


dfrow15426to20425 = pd.DataFrame(coordenadasrow15426to20425, result)


# In[86]:


dfrow15426to20425.reset_index(level=0, inplace=True)


# In[87]:


dfrow15426to20425 = dfrow15426to20425.rename(columns={'index':'cep'}) 


# In[88]:


dfrow15426to20425


# In[89]:


bancoesusalltabsrais2019nodupsCEPS[['id']][15426:20426]


# In[90]:


id15426to20425 = bancoesusalltabsrais2019nodupsCEPS[['id']][15426:20426]


# In[91]:


id15426to20425.reset_index(level=0, inplace=True)


# In[92]:


dfrow15426to20425['id'] = id15426to20425['id']
dfrow15426to20425['index'] = id15426to20425['index']


# In[93]:


dfrow15426to20425[dfrow15426to20425.columns[[4,3,0,1,2]]]


# In[94]:


dfrow15426to20425 = dfrow15426to20425[dfrow15426to20425.columns[[4,3,0,1,2]]]


# In[95]:


dfrow15426to20425


# In[96]:


dfrow15426to20425.to_excel('dfrow15426to20425latlong.xlsx')


# # bancoesusalltabsrais2019nodupsCEPS[20426:25425]

# In[10]:


bancoesusalltabsrais2019nodupsCEPS[20426:25425]


# In[11]:


row20426to25425 = bancoesusalltabsrais2019nodupsCEPS[20426:25425]


# In[12]:


row20426to25425


# In[13]:


row20426to25425.update("cep_to_coords('" + row20426to25425[['cep']].astype(str) + "'),")
print(row20426to25425)


# In[14]:


row20426to25425


# In[15]:


row20426to25425=row20426to25425.loc[:,'cep']


# In[16]:


row20426to25425


# In[17]:


print(' '.join(row20426to25425))#.tolist()


# In[18]:


coordenadasrow20426to25425 = cep_to_coords('54410340'), cep_to_coords('54230430'), cep_to_coords('55608411'), cep_to_coords('51030695'), cep_to_coords('48903035'), cep_to_coords('54420360'), cep_to_coords('53480484'), cep_to_coords('53770140'), cep_to_coords('51020370'), cep_to_coords('56304310'), cep_to_coords('55084158'), cep_to_coords('54260018'), cep_to_coords('54290491'), cep_to_coords('52091370'), cep_to_coords('54300152'), cep_to_coords('55040020'), cep_to_coords('55152350'), cep_to_coords('54407019'), cep_to_coords('54070070'), cep_to_coords('52070675'), cep_to_coords('55019053'), cep_to_coords('52390085'), cep_to_coords('53401300'), cep_to_coords('50770710'), cep_to_coords('50960410'), cep_to_coords('52090510'), cep_to_coords('52101111'), cep_to_coords('54325062'), cep_to_coords('51011690'), cep_to_coords('50050365'), cep_to_coords('53551038'), cep_to_coords('55014565'), cep_to_coords('53650775'), cep_to_coords('55157546'), cep_to_coords('53541180'), cep_to_coords('53220142'), cep_to_coords('54856551'), cep_to_coords('54520050'), cep_to_coords('52053950'), cep_to_coords('54280395'), cep_to_coords('55816400'), cep_to_coords('55192125'), cep_to_coords('54360230'), cep_to_coords('55293130'), cep_to_coords('54767310'), cep_to_coords('55018700'), cep_to_coords('52081705'), cep_to_coords('54771090'), cep_to_coords('05912309'), cep_to_coords('50630570'), cep_to_coords('52280216'), cep_to_coords('50181505'), cep_to_coords('53230730'), cep_to_coords('54410710'), cep_to_coords('52190243'), cep_to_coords('50630545'), cep_to_coords('51020440'), cep_to_coords('55026640'), cep_to_coords('52210081'), cep_to_coords('53150080'), cep_to_coords('53520801'), cep_to_coords('53099000'), cep_to_coords('52500000'), cep_to_coords('5459000000'), cep_to_coords('54580065'), cep_to_coords('55012075'), cep_to_coords('52040045'), cep_to_coords('95840000'), cep_to_coords('55037105'), cep_to_coords('55032190'), cep_to_coords('06454005'), cep_to_coords('54320285'), cep_to_coords('56328617'), cep_to_coords('54715140'), cep_to_coords('54720686'), cep_to_coords('52291650'), cep_to_coords('55294155'), cep_to_coords('52110350'), cep_to_coords('52150165'), cep_to_coords('54325080'), cep_to_coords('54777450'), cep_to_coords('52291103'), cep_to_coords('50551505'), cep_to_coords('54440296'), cep_to_coords('52211113'), cep_to_coords('56310783'), cep_to_coords('52009116'), cep_to_coords('50660140'), cep_to_coords('54310054'), cep_to_coords('50851505'), cep_to_coords('53421720'), cep_to_coords('53525750'), cep_to_coords('53505905'), cep_to_coords('50515150'), cep_to_coords('53270290'), cep_to_coords('54325810'), cep_to_coords('55292330'), cep_to_coords('52280320'), cep_to_coords('50151505'), cep_to_coords('53620445'), cep_to_coords('50060903'), cep_to_coords('56314710'), cep_to_coords('56312807'), cep_to_coords('50193201'), cep_to_coords('53421051'), cep_to_coords('56506380'), cep_to_coords('54515538'), cep_to_coords('50360010'), cep_to_coords('52280742'), cep_to_coords('51065011'), cep_to_coords('55015660'), cep_to_coords('54370155'), cep_to_coords('53170085'), cep_to_coords('54330340'), cep_to_coords('56322350'), cep_to_coords('56320500'), cep_to_coords('53610570'), cep_to_coords('56323810'), cep_to_coords('54460473'), cep_to_coords('54340305'), cep_to_coords('55194215'), cep_to_coords('52800000'), cep_to_coords('55020362'), cep_to_coords('56317190'), cep_to_coords('56321150'), cep_to_coords('55034290'), cep_to_coords('54032913'), cep_to_coords('56509390'), cep_to_coords('54350096'), cep_to_coords('54330211'), cep_to_coords('54140460'), cep_to_coords('52090235'), cep_to_coords('54353275'), cep_to_coords('54120230'), cep_to_coords('54390315'), cep_to_coords('52280340'), cep_to_coords('52091070'), cep_to_coords('54720681'), cep_to_coords('54720040'), cep_to_coords('53310240'), cep_to_coords('52051030'), cep_to_coords('50771290'), cep_to_coords('52280233'), cep_to_coords('50515181'), cep_to_coords('52070471'), cep_to_coords('54091230'), cep_to_coords('53471171'), cep_to_coords('50011520'), cep_to_coords('55021420'), cep_to_coords('55873415'), cep_to_coords('51345230'), cep_to_coords('53630685'), cep_to_coords('51345120'), cep_to_coords('50740640'), cep_to_coords('54270017'), cep_to_coords('52271170'), cep_to_coords('51020379'), cep_to_coords('53420070'), cep_to_coords('54723085'), cep_to_coords('50850010'), cep_to_coords('54540615'), cep_to_coords('54517510'), cep_to_coords('55038720'), cep_to_coords('53510385'), cep_to_coords('55010055'), cep_to_coords('52090230'), cep_to_coords('55294363'), cep_to_coords('54720021'), cep_to_coords('52041315'), cep_to_coords('50930390'), cep_to_coords('50870495'), cep_to_coords('50870491'), cep_to_coords('53430030'), cep_to_coords('55190700'), cep_to_coords('65000000'), cep_to_coords('53401615'), cep_to_coords('55154695'), cep_to_coords('53080540'), cep_to_coords('54753181'), cep_to_coords('54170516'), cep_to_coords('56505360'), cep_to_coords('54220700'), cep_to_coords('53170497'), cep_to_coords('50640025'), cep_to_coords('53429750'), cep_to_coords('55297798'), cep_to_coords('55819240'), cep_to_coords('53333333'), cep_to_coords('51111970'), cep_to_coords('51781690'), cep_to_coords('50780523'), cep_to_coords('54735085'), cep_to_coords('51030032'), cep_to_coords('55644385'), cep_to_coords('52010220'), cep_to_coords('55192395'), cep_to_coords('55190650'), cep_to_coords('53417521'), cep_to_coords('55027595'), cep_to_coords('55020388'), cep_to_coords('55006102'), cep_to_coords('54325057'), cep_to_coords('51010535'), cep_to_coords('53415420'), cep_to_coords('55019095'), cep_to_coords('24823053'), cep_to_coords('55294335'), cep_to_coords('55014022'), cep_to_coords('52701180'), cep_to_coords('55019250'), cep_to_coords('55295350'), cep_to_coords('53031030'), cep_to_coords('50120000'), cep_to_coords('54580365'), cep_to_coords('05363520'), cep_to_coords('55195109'), cep_to_coords('53635020'), cep_to_coords('53060290'), cep_to_coords('53637160'), cep_to_coords('56316645'), cep_to_coords('55034610'), cep_to_coords('55002340'), cep_to_coords('55032445'), cep_to_coords('54735789'), cep_to_coords('53230340'), cep_to_coords('54400430'), cep_to_coords('55018340'), cep_to_coords('50570160'), cep_to_coords('50760730'), cep_to_coords('54240108'), cep_to_coords('53510770'), cep_to_coords('54735756'), cep_to_coords('54715320'), cep_to_coords('55008270'), cep_to_coords('51021012'), cep_to_coords('51346090'), cep_to_coords('52081087'), cep_to_coords('54460355'), cep_to_coords('50820090'), cep_to_coords('52071658'), cep_to_coords('53650080'), cep_to_coords('54090390'), cep_to_coords('51460000'), cep_to_coords('5205134'), cep_to_coords('52211165'), cep_to_coords('55211430'), cep_to_coords('50651210'), cep_to_coords('54260571'), cep_to_coords('51280340'), cep_to_coords('53270022'), cep_to_coords('51505050'), cep_to_coords('50912903'), cep_to_coords('50850250'), cep_to_coords('50770730'), cep_to_coords('53520300'), cep_to_coords('56316450'), cep_to_coords('51290605'), cep_to_coords('55020504'), cep_to_coords('55612293'), cep_to_coords('52081770'), cep_to_coords('50720971'), cep_to_coords('53430620'), cep_to_coords('54325415'), cep_to_coords('56310330'), cep_to_coords('56323370'), cep_to_coords('55504000'), cep_to_coords('51515050'), cep_to_coords('50360350'), cep_to_coords('56320590'), cep_to_coords('54790140'), cep_to_coords('55293282'), cep_to_coords('52390521'), cep_to_coords('53610180'), cep_to_coords('52090122'), cep_to_coords('53640143'), cep_to_coords('52121345'), cep_to_coords('52291015'), cep_to_coords('50690590'), cep_to_coords('54160660'), cep_to_coords('53431055'), cep_to_coords('50810230'), cep_to_coords('53250637'), cep_to_coords('52021090'), cep_to_coords('55299560'), cep_to_coords('50050890'), cep_to_coords('50050904'), cep_to_coords('50820550'), cep_to_coords('52131012'), cep_to_coords('54330088'), cep_to_coords('52061510'), cep_to_coords('54090170'), cep_to_coords('24090270'), cep_to_coords('53407710'), cep_to_coords('51230325'), cep_to_coords('51320060'), cep_to_coords('50770460'), cep_to_coords('51270320'), cep_to_coords('54520645'), cep_to_coords('50060502'), cep_to_coords('51020420'), cep_to_coords('55191451'), cep_to_coords('55292610'), cep_to_coords('54302900'), cep_to_coords('55574800'), cep_to_coords('54295220'), cep_to_coords('52171748'), cep_to_coords('52131181'), cep_to_coords('53423240'), cep_to_coords('54090300'), cep_to_coords('53620635'), cep_to_coords('54530005'), cep_to_coords('54245230'), cep_to_coords('52190270'), cep_to_coords('55018610'), cep_to_coords('54505595'), cep_to_coords('43300490'), cep_to_coords('56509778'), cep_to_coords('52150200'), cep_to_coords('53421110'), cep_to_coords('53421011'), cep_to_coords('54735190'), cep_to_coords('53640161'), cep_to_coords('56332195'), cep_to_coords('50110783'), cep_to_coords('53525600'), cep_to_coords('53501456'), cep_to_coords('54270440'), cep_to_coords('54756350'), cep_to_coords('54000210'), cep_to_coords('51260332'), cep_to_coords('50730490'), cep_to_coords('54777085'), cep_to_coords('54772230'), cep_to_coords('55292120'), cep_to_coords('55209117'), cep_to_coords('53625110'), cep_to_coords('55022290'), cep_to_coords('50740720'), cep_to_coords('50570290'), cep_to_coords('54240090'), cep_to_coords('55294181'), cep_to_coords('54090070'), cep_to_coords('50950007'), cep_to_coords('52025002'), cep_to_coords('55036040'), cep_to_coords('55813580'), cep_to_coords('53660000'), cep_to_coords('52041959'), cep_to_coords('56308270'), cep_to_coords('54360155'), cep_to_coords('55022400'), cep_to_coords('53433380'), cep_to_coords('55194520'), cep_to_coords('54759097'), cep_to_coords('54759680'), cep_to_coords('56313275'), cep_to_coords('57710280'), cep_to_coords('56306200'), cep_to_coords('55558000'), cep_to_coords('56306485'), cep_to_coords('52130152'), cep_to_coords('54330394'), cep_to_coords('51100280'), cep_to_coords('55158170'), cep_to_coords('54260300'), cep_to_coords('52130222'), cep_to_coords('52080265'), cep_to_coords('52070971'), cep_to_coords('50007009'), cep_to_coords('52021100'), cep_to_coords('52080102'), cep_to_coords('52111135'), cep_to_coords('54170125'), cep_to_coords('49949268'), cep_to_coords('52071315'), cep_to_coords('51191602'), cep_to_coords('52051232'), cep_to_coords('54462158'), cep_to_coords('50771460'), cep_to_coords('53401535'), cep_to_coords('05249030'), cep_to_coords('55292078'), cep_to_coords('52210152'), cep_to_coords('50913209'), cep_to_coords('55008545'), cep_to_coords('54505035'), cep_to_coords('52250250'), cep_to_coords('53439802'), cep_to_coords('53403510'), cep_to_coords('53443410'), cep_to_coords('55018300'), cep_to_coords('18091999'), cep_to_coords('54430727'), cep_to_coords('54495050'), cep_to_coords('56321570'), cep_to_coords('556200000'), cep_to_coords('56906140'), cep_to_coords('54768015'), cep_to_coords('53545070'), cep_to_coords('50020008'), cep_to_coords('50161606'), cep_to_coords('53350070'), cep_to_coords('53580040'), cep_to_coords('53178792'), cep_to_coords('53170792'), cep_to_coords('54510902'), cep_to_coords('54122170'), cep_to_coords('5630434'), cep_to_coords('51091220'), cep_to_coords('54589235'), cep_to_coords('54340437'), cep_to_coords('56751360'), cep_to_coords('50720742'), cep_to_coords('54505465'), cep_to_coords('53405603'), cep_to_coords('56504460'), cep_to_coords('56500309'), cep_to_coords('52010010'), cep_to_coords('53429720'), cep_to_coords('54350035'), cep_to_coords('50340140'), cep_to_coords('53423580'), cep_to_coords('55299776'), cep_to_coords('54490506'), cep_to_coords('53010280'), cep_to_coords('56316100'), cep_to_coords('12500000'), cep_to_coords('55021360'), cep_to_coords('53640360'), cep_to_coords('55010060'), cep_to_coords('55430520'), cep_to_coords('54368180'), cep_to_coords('53409040'), cep_to_coords('52062430'), cep_to_coords('53433400'), cep_to_coords('54460590'), cep_to_coords('78195000'), cep_to_coords('58170570'), cep_to_coords('53530570'), cep_to_coords('40161640'), cep_to_coords('53170020'), cep_to_coords('55604420'), cep_to_coords('54325750'), cep_to_coords('50771370'), cep_to_coords('32041070'), cep_to_coords('52022026'), cep_to_coords('53300420'), cep_to_coords('54390410'), cep_to_coords('35295510'), cep_to_coords('54410080'), cep_to_coords('52130551'), cep_to_coords('54280767'), cep_to_coords('54360150'), cep_to_coords('56912450'), cep_to_coords('53060400'), cep_to_coords('53160220'), cep_to_coords('51240664'), cep_to_coords('53545680'), cep_to_coords('50750252'), cep_to_coords('52131670'), cep_to_coords('50680915'), cep_to_coords('54366006'), cep_to_coords('52210360'), cep_to_coords('52070720'), cep_to_coords('55292625'), cep_to_coords('54430130'), cep_to_coords('54510190'), cep_to_coords('52125160'), cep_to_coords('52111350'), cep_to_coords('51150735'), cep_to_coords('50470740'), cep_to_coords('54410345'), cep_to_coords('51290122'), cep_to_coords('56540412'), cep_to_coords('54730043'), cep_to_coords('51300310'), cep_to_coords('50620320'), cep_to_coords('51270050'), cep_to_coords('51150615'), cep_to_coords('55291657'), cep_to_coords('56516080'), cep_to_coords('50920161'), cep_to_coords('52090387'), cep_to_coords('53585050'), cep_to_coords('55294182'), cep_to_coords('50750380'), cep_to_coords('51290060'), cep_to_coords('56332545'), cep_to_coords('52130207'), cep_to_coords('53250690'), cep_to_coords('55024341'), cep_to_coords('55354000'), cep_to_coords('30122020'), cep_to_coords('54765025'), cep_to_coords('52030270'), cep_to_coords('53220160'), cep_to_coords('53403225'), cep_to_coords('52221102'), cep_to_coords('52180404'), cep_to_coords('52080480'), cep_to_coords('56330521'), cep_to_coords('54270240'), cep_to_coords('50661610'), cep_to_coords('55420150'), cep_to_coords('55819560'), cep_to_coords('54370030'), cep_to_coords('50061616'), cep_to_coords('50690320'), cep_to_coords('51330120'), cep_to_coords('50070902'), cep_to_coords('54350290'), cep_to_coords('54789425'), cep_to_coords('53360090'), cep_to_coords('53350005'), cep_to_coords('51260730'), cep_to_coords('52191406'), cep_to_coords('54300291'), cep_to_coords('53370710'), cep_to_coords('56312578'), cep_to_coords('54120680'), cep_to_coords('54520510'), cep_to_coords('54170661'), cep_to_coords('50940900'), cep_to_coords('52150082'), cep_to_coords('50650230'), cep_to_coords('53441450'), cep_to_coords('53409810'), cep_to_coords('55815060'), cep_to_coords('50781755'), cep_to_coords('50660310'), cep_to_coords('53280250'), cep_to_coords('54330075'), cep_to_coords('55294634'), cep_to_coords('55038128'), cep_to_coords('54768785'), cep_to_coords('52291190'), cep_to_coords('53350700'), cep_to_coords('51275600'), cep_to_coords('53150003'), cep_to_coords('22337598'), cep_to_coords('52710002'), cep_to_coords('53370374'), cep_to_coords('56234000'), cep_to_coords('51781421'), cep_to_coords('55290020'), cep_to_coords('56310170'), cep_to_coords('51335740'), cep_to_coords('52111175'), cep_to_coords('50060710'), cep_to_coords('52212119'), cep_to_coords('54410005'), cep_to_coords('52003010'), cep_to_coords('54730600'), cep_to_coords('53431705'), cep_to_coords('50770651'), cep_to_coords('50913091'), cep_to_coords('54735256'), cep_to_coords('52051320'), cep_to_coords('55614450'), cep_to_coords('52190030'), cep_to_coords('52280565'), cep_to_coords('54460425'), cep_to_coords('52291206'), cep_to_coords('54430695'), cep_to_coords('53270531'), cep_to_coords('50730280'), cep_to_coords('51260640'), cep_to_coords('54230560'), cep_to_coords('51011360'), cep_to_coords('56312740'), cep_to_coords('54525210'), cep_to_coords('54768020'), cep_to_coords('56316690'), cep_to_coords('56332020'), cep_to_coords('56312161'), cep_to_coords('52220565'), cep_to_coords('53431265'), cep_to_coords('50102391'), cep_to_coords('50860230'), cep_to_coords('53490550'), cep_to_coords('50950035'), cep_to_coords('50050115'), cep_to_coords('54340445'), cep_to_coords('50791005'), cep_to_coords('50060631'), cep_to_coords('53441341'), cep_to_coords('51275280'), cep_to_coords('50721140'), cep_to_coords('55811250'), cep_to_coords('55191681'), cep_to_coords('52160842'), cep_to_coords('50700080'), cep_to_coords('56508232'), cep_to_coords('51150360'), cep_to_coords('50640039'), cep_to_coords('50930360'), cep_to_coords('10747198'), cep_to_coords('52160065'), cep_to_coords('53110285'), cep_to_coords('53625706'), cep_to_coords('53615047'), cep_to_coords('52120025'), cep_to_coords('54280387'), cep_to_coords('53090130'), cep_to_coords('03580700'), cep_to_coords('54450150'), cep_to_coords('56313352'), cep_to_coords('55816420'), cep_to_coords('35002564'), cep_to_coords('54762580'), cep_to_coords('54320632'), cep_to_coords('53444449'), cep_to_coords('53441270'), cep_to_coords('55297140'), cep_to_coords('52010045'), cep_to_coords('56910000'), cep_to_coords('54430442'), cep_to_coords('53100130'), cep_to_coords('52091045'), cep_to_coords('51180455'), cep_to_coords('50940700'), cep_to_coords('54792410'), cep_to_coords('53413480'), cep_to_coords('51230620'), cep_to_coords('54730150'), cep_to_coords('55293708'), cep_to_coords('52610120'), cep_to_coords('43150519'), cep_to_coords('55153802'), cep_to_coords('52191050'), cep_to_coords('59300000'), cep_to_coords('50781790'), cep_to_coords('52090400'), cep_to_coords('50051360'), cep_to_coords('50110092'), cep_to_coords('53409430'), cep_to_coords('53429270'), cep_to_coords('53180320'), cep_to_coords('50670470'), cep_to_coords('57750000'), cep_to_coords('54756772'), cep_to_coords('52092122'), cep_to_coords('52097122'), cep_to_coords('50670270'), cep_to_coords('55500600'), cep_to_coords('53170280'), cep_to_coords('53010005'), cep_to_coords('53425610'), cep_to_coords('54430520'), cep_to_coords('54430560'), cep_to_coords('50790660'), cep_to_coords('53444085'), cep_to_coords('55150620'), cep_to_coords('50720722'), cep_to_coords('53647710'), cep_to_coords('50777064'), cep_to_coords('53540110'), cep_to_coords('54140000'), cep_to_coords('54723135'), cep_to_coords('53005000'), cep_to_coords('53635140'), cep_to_coords('50870900'), cep_to_coords('52041600'), cep_to_coords('52111400'), cep_to_coords('54530030'), cep_to_coords('51240810'), cep_to_coords('54210060'), cep_to_coords('53620190'), cep_to_coords('55190582'), cep_to_coords('54011210'), cep_to_coords('51275485'), cep_to_coords('55294580'), cep_to_coords('55294439'), cep_to_coords('56312329'), cep_to_coords('56314715'), cep_to_coords('56334859'), cep_to_coords('56313740'), cep_to_coords('55042235'), cep_to_coords('52051080'), cep_to_coords('55012690'), cep_to_coords('50060715'), cep_to_coords('50805540'), cep_to_coords('52091282'), cep_to_coords('51020360'), cep_to_coords('50940531'), cep_to_coords('54100390'), cep_to_coords('50601100'), cep_to_coords('51190260'), cep_to_coords('54325235'), cep_to_coords('51335230'), cep_to_coords('50008206'), cep_to_coords('51300300'), cep_to_coords('50101125'), cep_to_coords('52090002'), cep_to_coords('54090150'), cep_to_coords('55040004'), cep_to_coords('50790625'), cep_to_coords('50019230'), cep_to_coords('54353395'), cep_to_coords('53040100'), cep_to_coords('50012930'), cep_to_coords('50620491'), cep_to_coords('02041973'), cep_to_coords('54270023'), cep_to_coords('55195818'), cep_to_coords('52240400'), cep_to_coords('54420228'), cep_to_coords('55819330'), cep_to_coords('54150070'), cep_to_coords('53370205'), cep_to_coords('50501923'), cep_to_coords('55157675'), cep_to_coords('54325095'), cep_to_coords('55006170'), cep_to_coords('50721137'), cep_to_coords('56321730'), cep_to_coords('56317377'), cep_to_coords('53437361'), cep_to_coords('53120175'), cep_to_coords('55292440'), cep_to_coords('54777265'), cep_to_coords('54735792'), cep_to_coords('52091270'), cep_to_coords('54330066'), cep_to_coords('53402410'), cep_to_coords('53430135'), cep_to_coords('54710240'), cep_to_coords('55024467'), cep_to_coords('52060103'), cep_to_coords('55195843'), cep_to_coords('50721420'), cep_to_coords('48600000'), cep_to_coords('56308015'), cep_to_coords('53420190'), cep_to_coords('53565160'), cep_to_coords('54250312'), cep_to_coords('54768798'), cep_to_coords('53530420'), cep_to_coords('53580640'), cep_to_coords('50820360'), cep_to_coords('54786250'), cep_to_coords('53293370'), cep_to_coords('55158680'), cep_to_coords('55816224'), cep_to_coords('54735500'), cep_to_coords('22900000'), cep_to_coords('50610470'), cep_to_coords('56903460'), cep_to_coords('48903020'), cep_to_coords('56304450'), cep_to_coords('56306330'), cep_to_coords('50791132'), cep_to_coords('53250510'), cep_to_coords('53120191'), cep_to_coords('53635080'), cep_to_coords('54280679'), cep_to_coords('54130010'), cep_to_coords('5503840'), cep_to_coords('50730111'), cep_to_coords('53180140'), cep_to_coords('55194330'), cep_to_coords('55192593'), cep_to_coords('52080026'), cep_to_coords('54350140'), cep_to_coords('54330130'), cep_to_coords('52071530'), cep_to_coords('52191181'), cep_to_coords('54350100'), cep_to_coords('52120410'), cep_to_coords('54726115'), cep_to_coords('50670120'), cep_to_coords('50930101'), cep_to_coords('57770510'), cep_to_coords('50770290'), cep_to_coords('53444370'), cep_to_coords('56330240'), cep_to_coords('56935000'), cep_to_coords('55038555'), cep_to_coords('53639205'), cep_to_coords('53430015'), cep_to_coords('54756376'), cep_to_coords('55010120'), cep_to_coords('53412270'), cep_to_coords('50960350'), cep_to_coords('53560115'), cep_to_coords('52078026'), cep_to_coords('54771240'), cep_to_coords('55026390'), cep_to_coords('54160570'), cep_to_coords('50690715'), cep_to_coords('50860450'), cep_to_coords('54786341'), cep_to_coords('53020547'), cep_to_coords('54410236'), cep_to_coords('55643698'), cep_to_coords('55291280'), cep_to_coords('55296055'), cep_to_coords('53220013'), cep_to_coords('55605294'), cep_to_coords('55290175'), cep_to_coords('56318250'), cep_to_coords('52380090'), cep_to_coords('58818555'), cep_to_coords('52081371'), cep_to_coords('53625600'), cep_to_coords('53160322'), cep_to_coords('54430055'), cep_to_coords('50690585'), cep_to_coords('51335365'), cep_to_coords('15205015'), cep_to_coords('51010125'), cep_to_coords('52191475'), cep_to_coords('55293905'), cep_to_coords('55195202'), cep_to_coords('52191350'), cep_to_coords('50720970'), cep_to_coords('53402685'), cep_to_coords('55157070'), cep_to_coords('50910116'), cep_to_coords('55158143'), cep_to_coords('55018070'), cep_to_coords('56328410'), cep_to_coords('50788350'), cep_to_coords('52120340'), cep_to_coords('55002150'), cep_to_coords('53402117'), cep_to_coords('51270313'), cep_to_coords('54774375'), cep_to_coords('54505055'), cep_to_coords('56519100'), cep_to_coords('50870330'), cep_to_coords('56326840'), cep_to_coords('54330115'), cep_to_coords('54420300'), cep_to_coords('50721130'), cep_to_coords('53421280'), cep_to_coords('51330305'), cep_to_coords('52091100'), cep_to_coords('50810610'), cep_to_coords('54771550'), cep_to_coords('53433320'), cep_to_coords('51250080'), cep_to_coords('54315662'), cep_to_coords('52171001'), cep_to_coords('55293250'), cep_to_coords('55506218'), cep_to_coords('53419070'), cep_to_coords('56503425'), cep_to_coords('56540235'), cep_to_coords('55036560'), cep_to_coords('52071225'), cep_to_coords('54559000'), cep_to_coords('55152080'), cep_to_coords('55153004'), cep_to_coords('44700000'), cep_to_coords('53431735'), cep_to_coords('45400000'), cep_to_coords('55122180'), cep_to_coords('53540320'), cep_to_coords('50680275'), cep_to_coords('52150145'), cep_to_coords('52061105'), cep_to_coords('54490183'), cep_to_coords('52230291'), cep_to_coords('50665050'), cep_to_coords('52120091'), cep_to_coords('52071245'), cep_to_coords('53610835'), cep_to_coords('55295330'), cep_to_coords('50782038'), cep_to_coords('56312400'), cep_to_coords('53020000'), cep_to_coords('55119040'), cep_to_coords('50640072'), cep_to_coords('52131680'), cep_to_coords('50415546'), cep_to_coords('53407640'), cep_to_coords('50930219'), cep_to_coords('54705285'), cep_to_coords('50781135'), cep_to_coords('52090197'), cep_to_coords('50820660'), cep_to_coords('53419620'), cep_to_coords('52291091'), cep_to_coords('52240860'), cep_to_coords('58072500'), cep_to_coords('56506705'), cep_to_coords('50050225'), cep_to_coords('54786140'), cep_to_coords('54150051'), cep_to_coords('56515390'), cep_to_coords('54470430'), cep_to_coords('55298075'), cep_to_coords('56317130'), cep_to_coords('56312725'), cep_to_coords('55158620'), cep_to_coords('44999000'), cep_to_coords('53650291'), cep_to_coords('59220140'), cep_to_coords('53620440'), cep_to_coords('52280470'), cep_to_coords('50912390'), cep_to_coords('53421142'), cep_to_coords('55012670'), cep_to_coords('57616200'), cep_to_coords('53409410'), cep_to_coords('55090591'), cep_to_coords('53530540'), cep_to_coords('50129030'), cep_to_coords('52031480'), cep_to_coords('53413410'), cep_to_coords('55294812'), cep_to_coords('50761200'), cep_to_coords('52071441'), cep_to_coords('51310315'), cep_to_coords('05205004'), cep_to_coords('52081311'), cep_to_coords('54280471'), cep_to_coords('54270221'), cep_to_coords('54733240'), cep_to_coords('53374000'), cep_to_coords('53416245'), cep_to_coords('56517760'), cep_to_coords('51300019'), cep_to_coords('55016745'), cep_to_coords('50070510'), cep_to_coords('54753430'), cep_to_coords('54410028'), cep_to_coords('50912600'), cep_to_coords('20/06/1996'), cep_to_coords('53620813'), cep_to_coords('52041024'), cep_to_coords('54783710'), cep_to_coords('54325015'), cep_to_coords('54280035'), cep_to_coords('50040190'), cep_to_coords('54759475'), cep_to_coords('51270695'), cep_to_coords('51330580'), cep_to_coords('50270037'), cep_to_coords('24245105'), cep_to_coords('55292748'), cep_to_coords('50701120'), cep_to_coords('55008172'), cep_to_coords('52108050'), cep_to_coords('54330800'), cep_to_coords('54589215'), cep_to_coords('55194414'), cep_to_coords('52090064'), cep_to_coords('50840220'), cep_to_coords('51200100'), cep_to_coords('54330111'), cep_to_coords('55294153'), cep_to_coords('81119630'), cep_to_coords('55290355'), cep_to_coords('50920717'), cep_to_coords('52071442'), cep_to_coords('50102399'), cep_to_coords('51051230'), cep_to_coords('52291035'), cep_to_coords('42051230'), cep_to_coords('50417360'), cep_to_coords('51330245'), cep_to_coords('55294795'), cep_to_coords('50110841'), cep_to_coords('51260722'), cep_to_coords('50630180'), cep_to_coords('51180470'), cep_to_coords('50681050'), cep_to_coords('54410111'), cep_to_coords('54759410'), cep_to_coords('53403070'), cep_to_coords('50320290'), cep_to_coords('54705372'), cep_to_coords('54260620'), cep_to_coords('51330172'), cep_to_coords('56518000'), cep_to_coords('52191190'), cep_to_coords('52071454'), cep_to_coords('52711080'), cep_to_coords('50921130'), cep_to_coords('52610140'), cep_to_coords('51140000'), cep_to_coords('54789360'), cep_to_coords('21041992'), cep_to_coords('53417112'), cep_to_coords('55614006'), cep_to_coords('55610078'), cep_to_coords('51240708'), cep_to_coords('54330754'), cep_to_coords('55818500'), cep_to_coords('53440330'), cep_to_coords('51021001'), cep_to_coords('52221375'), cep_to_coords('54280417'), cep_to_coords('50720511'), cep_to_coords('56960000'), cep_to_coords('55020400'), cep_to_coords('56332305'), cep_to_coords('56316635'), cep_to_coords('56310750'), cep_to_coords('29071961'), cep_to_coords('52271500'), cep_to_coords('51240052'), cep_to_coords('53439710'), cep_to_coords('54735720'), cep_to_coords('51250490'), cep_to_coords('50350040'), cep_to_coords('55027640'), cep_to_coords('50530510'), cep_to_coords('50711560'), cep_to_coords('52191530'), cep_to_coords('55036430'), cep_to_coords('54460666'), cep_to_coords('54230475'), cep_to_coords('54315325'), cep_to_coords('55019145'), cep_to_coords('50780110'), cep_to_coords('51350023'), cep_to_coords('54222222'), cep_to_coords('55191025'), cep_to_coords('50325300'), cep_to_coords('56388020'), cep_to_coords('56308041'), cep_to_coords('56310025'), cep_to_coords('56330140'), cep_to_coords('52121034'), cep_to_coords('53421571'), cep_to_coords('54330593'), cep_to_coords('53090460'), cep_to_coords('54325610'), cep_to_coords('54320021'), cep_to_coords('54450371'), cep_to_coords('54410371'), cep_to_coords('55292265'), cep_to_coords('52900000'), cep_to_coords('99487441'), cep_to_coords('55030530'), cep_to_coords('50129390'), cep_to_coords('53210370'), cep_to_coords('50780670'), cep_to_coords('03023748'), cep_to_coords('51275440'), cep_to_coords('53150240'), cep_to_coords('52080080'), cep_to_coords('54676120'), cep_to_coords('51220070'), cep_to_coords('50760530'), cep_to_coords('52210475'), cep_to_coords('52081790'), cep_to_coords('52140455'), cep_to_coords('56516170'), cep_to_coords('52160840'), cep_to_coords('52111395'), cep_to_coords('50110842'), cep_to_coords('50261550'), cep_to_coords('52091174'), cep_to_coords('54380245'), cep_to_coords('60750225'), cep_to_coords('56517000'), cep_to_coords('54783590'), cep_to_coords('50920085'), cep_to_coords('54150123'), cep_to_coords('52090055'), cep_to_coords('52160020'), cep_to_coords('50430190'), cep_to_coords('50751450'), cep_to_coords('51300023'), cep_to_coords('55150425'), cep_to_coords('50040070'), cep_to_coords('54735530'), cep_to_coords('54410225'), cep_to_coords('53417702'), cep_to_coords('53200035'), cep_to_coords('52121160'), cep_to_coords('51310265'), cep_to_coords('50771735'), cep_to_coords('52090621'), cep_to_coords('56503824'), cep_to_coords('50110773'), cep_to_coords('53436000'), cep_to_coords('52191045'), cep_to_coords('55818390'), cep_to_coords('54325035'), cep_to_coords('56909555'), cep_to_coords('54786590'), cep_to_coords('52130285'), cep_to_coords('54460235'), cep_to_coords('51250100'), cep_to_coords('56909234'), cep_to_coords('53190060'), cep_to_coords('250000000'), cep_to_coords('54210572'), cep_to_coords('56509050'), cep_to_coords('54210092'), cep_to_coords('52480400'), cep_to_coords('52091051'), cep_to_coords('50740321'), cep_to_coords('54150442'), cep_to_coords('51111620'), cep_to_coords('55195182'), cep_to_coords('51275060'), cep_to_coords('54220275'), cep_to_coords('52390600'), cep_to_coords('56456645'), cep_to_coords('55195545'), cep_to_coords('54230242'), cep_to_coords('55195557'), cep_to_coords('53060150'), cep_to_coords('52006015'), cep_to_coords('15440018'), cep_to_coords('53080090'), cep_to_coords('53150506'), cep_to_coords('53425835'), cep_to_coords('53320200'), cep_to_coords('52160605'), cep_to_coords('52280435'), cep_to_coords('54325705'), cep_to_coords('56331090'), cep_to_coords('53425665'), cep_to_coords('51335050'), cep_to_coords('54589360'), cep_to_coords('54735087'), cep_to_coords('54720664'), cep_to_coords('56516180'), cep_to_coords('56509830'), cep_to_coords('52190000'), cep_to_coords('55170970'), cep_to_coords('56503560'), cep_to_coords('53080351'), cep_to_coords('53370190'), cep_to_coords('53080550'), cep_to_coords('56509470'), cep_to_coords('55041000'), cep_to_coords('55021065'), cep_to_coords('55297801'), cep_to_coords('59091395'), cep_to_coords('54240290'), cep_to_coords('54120290'), cep_to_coords('50001000'), cep_to_coords('53433245'), cep_to_coords('55018154'), cep_to_coords('54777350'), cep_to_coords('50660003'), cep_to_coords('52070581'), cep_to_coords('52110143'), cep_to_coords('50900700'), cep_to_coords('50040060'), cep_to_coords('55294740'), cep_to_coords('54280614'), cep_to_coords('55299844'), cep_to_coords('55290844'), cep_to_coords('54100160'), cep_to_coords('55010310'), cep_to_coords('52266484'), cep_to_coords('54777060'), cep_to_coords('54756585'), cep_to_coords('55293070'), cep_to_coords('54353991'), cep_to_coords('50020070'), cep_to_coords('52040152'), cep_to_coords('54420351'), cep_to_coords('54325110'), cep_to_coords('54325010'), cep_to_coords('54250431'), cep_to_coords('52090133'), cep_to_coords('53615120'), cep_to_coords('54421140'), cep_to_coords('51180130'), cep_to_coords('56503715'), cep_to_coords('55030053'), cep_to_coords('57453070'), cep_to_coords('54080390'), cep_to_coords('53090095'), cep_to_coords('52390445'), cep_to_coords('55292710'), cep_to_coords('54830510'), cep_to_coords('55607010'), cep_to_coords('55292160'), cep_to_coords('55294211'), cep_to_coords('55022166'), cep_to_coords('56460970'), cep_to_coords('54732000'), cep_to_coords('56321700'), cep_to_coords('56306800'), cep_to_coords('56320230'), cep_to_coords('44900000'), cep_to_coords('56332128'), cep_to_coords('51334071'), cep_to_coords('55643390'), cep_to_coords('55291635'), cep_to_coords('51230141'), cep_to_coords('54115094'), cep_to_coords('54050094'), cep_to_coords('54120705'), cep_to_coords('55158350'), cep_to_coords('50736006'), cep_to_coords('53404480'), cep_to_coords('53441150'), cep_to_coords('52081110'), cep_to_coords('54800600'), cep_to_coords('54280320'), cep_to_coords('51121045'), cep_to_coords('50280820'), cep_to_coords('52130370'), cep_to_coords('54440550'), cep_to_coords('52211140'), cep_to_coords('52210250'), cep_to_coords('52125230'), cep_to_coords('51270490'), cep_to_coords('54430390'), cep_to_coords('55026480'), cep_to_coords('52400023'), cep_to_coords('54360062'), cep_to_coords('55022100'), cep_to_coords('50771390'), cep_to_coords('55291661'), cep_to_coords('54510093'), cep_to_coords('53610070'), cep_to_coords('53439260'), cep_to_coords('52131401'), cep_to_coords('53402017'), cep_to_coords('52041500'), cep_to_coords('56505410'), cep_to_coords('52090161'), cep_to_coords('55032440'), cep_to_coords('56504085'), cep_to_coords('54413010'), cep_to_coords('53620794'), cep_to_coords('55293315'), cep_to_coords('54423622'), cep_to_coords('50920705'), cep_to_coords('53420300'), cep_to_coords('53402752'), cep_to_coords('54310094'), cep_to_coords('52280265'), cep_to_coords('54268921'), cep_to_coords('54340002'), cep_to_coords('54420680'), cep_to_coords('55530500'), cep_to_coords('50330300'), cep_to_coords('55298171'), cep_to_coords('56140321'), cep_to_coords('55153785'), cep_to_coords('54210462'), cep_to_coords('63000000'), cep_to_coords('54280543'), cep_to_coords('55022520'), cep_to_coords('54160513'), cep_to_coords('45000000'), cep_to_coords('52151141'), cep_to_coords('52154340'), cep_to_coords('53417580'), cep_to_coords('52191211'), cep_to_coords('50760370'), cep_to_coords('53560510'), cep_to_coords('53160610'), cep_to_coords('50002080'), cep_to_coords('20110226'), cep_to_coords('55040430'), cep_to_coords('55602180'), cep_to_coords('55614670'), cep_to_coords('54280770'), cep_to_coords('52150270'), cep_to_coords('55155770'), cep_to_coords('54420540'), cep_to_coords('53605725'), cep_to_coords('51564653'), cep_to_coords('56300201'), cep_to_coords('52160165'), cep_to_coords('54774225'), cep_to_coords('50710930'), cep_to_coords('51030328'), cep_to_coords('53020170'), cep_to_coords('54750110'), cep_to_coords('53429255'), cep_to_coords('55027190'), cep_to_coords('56505260'), cep_to_coords('54753240'), cep_to_coords('54767410'), cep_to_coords('56318290'), cep_to_coords('55004220'), cep_to_coords('56328040'), cep_to_coords('56318140'), cep_to_coords('53640788'), cep_to_coords('51310055'), cep_to_coords('53620857'), cep_to_coords('55114760'), cep_to_coords('55014805'), cep_to_coords('55608135'), cep_to_coords('57762115'), cep_to_coords('53645560'), cep_to_coords('52000005'), cep_to_coords('54735620'), cep_to_coords('53320360'), cep_to_coords('56509270'), cep_to_coords('52130590'), cep_to_coords('54330390'), cep_to_coords('50711640'), cep_to_coords('34410160'), cep_to_coords('52130226'), cep_to_coords('24687526'), cep_to_coords('55028037'), cep_to_coords('55042630'), cep_to_coords('53545570'), cep_to_coords('52171447'), cep_to_coords('54140630'), cep_to_coords('22051971'), cep_to_coords('55018162'), cep_to_coords('51290312'), cep_to_coords('54325310'), cep_to_coords('54352310'), cep_to_coords('54325521'), cep_to_coords('50850590'), cep_to_coords('51280090'), cep_to_coords('54520670'), cep_to_coords('55155080'), cep_to_coords('55158480'), cep_to_coords('52170400'), cep_to_coords('53439540'), cep_to_coords('53401880'), cep_to_coords('55445365'), cep_to_coords('53260044'), cep_to_coords('50791490'), cep_to_coords('74080060'), cep_to_coords('50630670'), cep_to_coords('53360251'), cep_to_coords('53403305'), cep_to_coords('50040310'), cep_to_coords('53270675'), cep_to_coords('50720240'), cep_to_coords('55578970'), cep_to_coords('54100210'), cep_to_coords('53625025'), cep_to_coords('53585315'), cep_to_coords('52060300'), cep_to_coords('54495495'), cep_to_coords('24593510'), cep_to_coords('50850240'), cep_to_coords('56316550'), cep_to_coords('54115008'), cep_to_coords('54517230'), cep_to_coords('55292640'), cep_to_coords('54786260'), cep_to_coords('56332490'), cep_to_coords('50620710'), cep_to_coords('54762067'), cep_to_coords('55608504'), cep_to_coords('50110777'), cep_to_coords('55294793'), cep_to_coords('51347715'), cep_to_coords('50780120'), cep_to_coords('53401456'), cep_to_coords('52060321'), cep_to_coords('54815515'), cep_to_coords('55606845'), cep_to_coords('50620140'), cep_to_coords('53421411'), cep_to_coords('51330420'), cep_to_coords('54260170'), cep_to_coords('55430970'), cep_to_coords('56316310'), cep_to_coords('56321280'), cep_to_coords('56065150'), cep_to_coords('50123019'), cep_to_coords('54768370'), cep_to_coords('50909123'), cep_to_coords('55027310'), cep_to_coords('54110090'), cep_to_coords('55030588'), cep_to_coords('51025330'), cep_to_coords('51335180'), cep_to_coords('51230640'), cep_to_coords('50760546'), cep_to_coords('52020420'), cep_to_coords('50110010'), cep_to_coords('53302620'), cep_to_coords('52190052'), cep_to_coords('54830330'), cep_to_coords('56332290'), cep_to_coords('53401580'), cep_to_coords('51030780'), cep_to_coords('56515100'), cep_to_coords('53425810'), cep_to_coords('54325305'), cep_to_coords('50350305'), cep_to_coords('52190283'), cep_to_coords('57910970'), cep_to_coords('55602130'), cep_to_coords('51150035'), cep_to_coords('53429820'), cep_to_coords('51220055'), cep_to_coords('50440700'), cep_to_coords('56508405'), cep_to_coords('54315130'), cep_to_coords('50660220'), cep_to_coords('55294642'), cep_to_coords('54730620'), cep_to_coords('81960253'), cep_to_coords('25689999'), cep_to_coords('51032585'), cep_to_coords('53420120'), cep_to_coords('52091072'), cep_to_coords('50620582'), cep_to_coords('50760165'), cep_to_coords('53525185'), cep_to_coords('56310756'), cep_to_coords('56323385'), cep_to_coords('52080138'), cep_to_coords('52125060'), cep_to_coords('52291062'), cep_to_coords('53422470'), cep_to_coords('53630125'), cep_to_coords('53407606'), cep_to_coords('54160310'), cep_to_coords('50791363'), cep_to_coords('54210339'), cep_to_coords('51290390'), cep_to_coords('52071432'), cep_to_coords('48601320'), cep_to_coords('36543541'), cep_to_coords('52090036'), cep_to_coords('53660260'), cep_to_coords('54325030'), cep_to_coords('52211120'), cep_to_coords('54440404'), cep_to_coords('51340710'), cep_to_coords('50940660'), cep_to_coords('53405280'), cep_to_coords('54720345'), cep_to_coords('42190130'), cep_to_coords('53422490'), cep_to_coords('53429690'), cep_to_coords('50780940'), cep_to_coords('53441140'), cep_to_coords('53510130'), cep_to_coords('52910000'), cep_to_coords('54735600'), cep_to_coords('56328185'), cep_to_coords('53130420'), cep_to_coords('54753255'), cep_to_coords('53409847'), cep_to_coords('51320140'), cep_to_coords('56312240'), cep_to_coords('56312041'), cep_to_coords('56320185'), cep_to_coords('50601010'), cep_to_coords('55400100'), cep_to_coords('57270573'), cep_to_coords('51300080'), cep_to_coords('50600010'), cep_to_coords('50010120'), cep_to_coords('55155450'), cep_to_coords('54140360'), cep_to_coords('54290220'), cep_to_coords('55815415'), cep_to_coords('50120392'), cep_to_coords('55004050'), cep_to_coords('50920839'), cep_to_coords('52190695'), cep_to_coords('54786085'), cep_to_coords('50760840'), cep_to_coords('53337050'), cep_to_coords('54354555'), cep_to_coords('56505270'), cep_to_coords('53320750'), cep_to_coords('52520500'), cep_to_coords('57730070'), cep_to_coords('54580620'), cep_to_coords('54130160'), cep_to_coords('54350430'), cep_to_coords('51012070'), cep_to_coords('55450020'), cep_to_coords('56510250'), cep_to_coords('53415417'), cep_to_coords('53080135'), cep_to_coords('52160845'), cep_to_coords('52071299'), cep_to_coords('50620711'), cep_to_coords('53530070'), cep_to_coords('55608655'), cep_to_coords('55157590'), cep_to_coords('56308110'), cep_to_coords('56320450'), cep_to_coords('53635660'), cep_to_coords('54250350'), cep_to_coords('53090351'), cep_to_coords('51340215'), cep_to_coords('51730322'), cep_to_coords('54350734'), cep_to_coords('56313240'), cep_to_coords('55700970'), cep_to_coords('52021370'), cep_to_coords('50040480'), cep_to_coords('53423320'), cep_to_coords('50810540'), cep_to_coords('50110745'), cep_to_coords('54280350'), cep_to_coords('28101973'), cep_to_coords('50781400'), cep_to_coords('58074050'), cep_to_coords('54352130'), cep_to_coords('52170030'), cep_to_coords('50909120'), cep_to_coords('50980415'), cep_to_coords('54250491'), cep_to_coords('55192085'), cep_to_coords('56330530'), cep_to_coords('50920826'), cep_to_coords('54767390'), cep_to_coords('56332762'), cep_to_coords('53413540'), cep_to_coords('53210410'), cep_to_coords('53190668'), cep_to_coords('55155790'), cep_to_coords('56306030'), cep_to_coords('54759220'), cep_to_coords('51180400'), cep_to_coords('53421070'), cep_to_coords('54300050'), cep_to_coords('54580020'), cep_to_coords('5546000'), cep_to_coords('50711410'), cep_to_coords('54515506'), cep_to_coords('54410788'), cep_to_coords('55813325'), cep_to_coords('54411100'), cep_to_coords('52190330'), cep_to_coords('52080552'), cep_to_coords('52221141'), cep_to_coords('54745240'), cep_to_coords('43116590'), cep_to_coords('54689254'), cep_to_coords('55027240'), cep_to_coords('35630415'), cep_to_coords('54515548'), cep_to_coords('53180610'), cep_to_coords('52171286'), cep_to_coords('56318330'), cep_to_coords('50900140'), cep_to_coords('51130630'), cep_to_coords('53640146'), cep_to_coords('50192320'), cep_to_coords('53200702'), cep_to_coords('50920040'), cep_to_coords('56512012'), cep_to_coords('54160433'), cep_to_coords('54080202'), cep_to_coords('54580402'), cep_to_coords('53625579'), cep_to_coords('53690692'), cep_to_coords('50830710'), cep_to_coords('56512560'), cep_to_coords('56502320'), cep_to_coords('55291330'), cep_to_coords('54404605'), cep_to_coords('54480020'), cep_to_coords('55614640'), cep_to_coords('51240150'), cep_to_coords('54460420'), cep_to_coords('53540450'), cep_to_coords('54505370'), cep_to_coords('50640060'), cep_to_coords('51260360'), cep_to_coords('54495490'), cep_to_coords('54720170'), cep_to_coords('53220250'), cep_to_coords('52291092'), cep_to_coords('50620410'), cep_to_coords('52080540'), cep_to_coords('53525710'), cep_to_coords('50050901'), cep_to_coords('55385970'), cep_to_coords('50790065'), cep_to_coords('53360330'), cep_to_coords('56304300'), cep_to_coords('51210210'), cep_to_coords('51250251'), cep_to_coords('54765145'), cep_to_coords('52051432'), cep_to_coords('56320755'), cep_to_coords('52190312'), cep_to_coords('51051395'), cep_to_coords('56302420'), cep_to_coords('51320421'), cep_to_coords('50490520'), cep_to_coords('50400290'), cep_to_coords('51280300'), cep_to_coords('52390270'), cep_to_coords('52221470'), cep_to_coords('52291010'), cep_to_coords('74410007'), cep_to_coords('52090570'), cep_to_coords('52136102'), cep_to_coords('50830390'), cep_to_coords('53562012'), cep_to_coords('51220200'), cep_to_coords('50620080'), cep_to_coords('54130070'), cep_to_coords('53610595'), cep_to_coords('54120635'), cep_to_coords('56302630'), cep_to_coords('52121150'), cep_to_coords('56326110'), cep_to_coords('50670040'), cep_to_coords('54150422'), cep_to_coords('51230327'), cep_to_coords('50960310'), cep_to_coords('56354500'), cep_to_coords('50802003'), cep_to_coords('55816565'), cep_to_coords('53270335'), cep_to_coords('52221360'), cep_to_coords('53010071'), cep_to_coords('51080180'), cep_to_coords('53403580'), cep_to_coords('53550550'), cep_to_coords('54470052'), cep_to_coords('52110170'), cep_to_coords('56312241'), cep_to_coords('53417285'), cep_to_coords('54470070'), cep_to_coords('52470070'), cep_to_coords('55042380'), cep_to_coords('50612033'), cep_to_coords('54280571'), cep_to_coords('52230232'), cep_to_coords('53407255'), cep_to_coords('53620714'), cep_to_coords('50760230'), cep_to_coords('54460170'), cep_to_coords('54720300'), cep_to_coords('56519310'), cep_to_coords('55852000'), cep_to_coords('56508210'), cep_to_coords('51030345'), cep_to_coords('53200700'), cep_to_coords('53270711'), cep_to_coords('55016540'), cep_to_coords('55819386'), cep_to_coords('54080230'), cep_to_coords('53260250'), cep_to_coords('50721380'), cep_to_coords('55014690'), cep_to_coords('55815077'), cep_to_coords('54280751'), cep_to_coords('55026430'), cep_to_coords('53370430'), cep_to_coords('52071153'), cep_to_coords('54789025'), cep_to_coords('54786740'), cep_to_coords('55195241'), cep_to_coords('53030110'), cep_to_coords('48000900'), cep_to_coords('56912220'), cep_to_coords('50610123'), cep_to_coords('52121120'), cep_to_coords('54720804'), cep_to_coords('50010240'), cep_to_coords('52221131'), cep_to_coords('56503680'), cep_to_coords('54360125'), cep_to_coords('50120391'), cep_to_coords('50000600'), cep_to_coords('50601202'), cep_to_coords('51330175'), cep_to_coords('78444381'), cep_to_coords('56505045'), cep_to_coords('54753776'), cep_to_coords('51082300'), cep_to_coords('50640375'), cep_to_coords('52080060'), cep_to_coords('51290565'), cep_to_coords('56511190'), cep_to_coords('51001142'), cep_to_coords('55192360'), cep_to_coords('50971000'), cep_to_coords('54325066'), cep_to_coords('36907367'), cep_to_coords('52290060'), cep_to_coords('56316590'), cep_to_coords('56312385'), cep_to_coords('55018608'), cep_to_coords('55014746'), cep_to_coords('55195590'), cep_to_coords('54440041'), cep_to_coords('53040070'), cep_to_coords('52110489'), cep_to_coords('54741470'), cep_to_coords('52210321'), cep_to_coords('52160802'), cep_to_coords('50960650'), cep_to_coords('53437560'), cep_to_coords('35130174'), cep_to_coords('54767220'), cep_to_coords('61944760'), cep_to_coords('51020197'), cep_to_coords('53423250'), cep_to_coords('54735055'), cep_to_coords('53040340'), cep_to_coords('54505710'), cep_to_coords('55614425'), cep_to_coords('55608605'), cep_to_coords('55560860'), cep_to_coords('51011275'), cep_to_coords('50781528'), cep_to_coords('53131676'), cep_to_coords('54280025'), cep_to_coords('57730000'), cep_to_coords('51345175'), cep_to_coords('54330474'), cep_to_coords('54470350'), cep_to_coords('55299951'), cep_to_coords('55299515'), cep_to_coords('56328800'), cep_to_coords('55292455'), cep_to_coords('55819480'), cep_to_coords('54430225'), cep_to_coords('52090695'), cep_to_coords('55020536'), cep_to_coords('55818501'), cep_to_coords('50660340'), cep_to_coords('5517500'), cep_to_coords('55014800'), cep_to_coords('54735370'), cep_to_coords('56312301'), cep_to_coords('55641370'), cep_to_coords('53190780'), cep_to_coords('51120090'), cep_to_coords('53403253'), cep_to_coords('52133151'), cep_to_coords('53585120'), cep_to_coords('54322500'), cep_to_coords('64685000'), cep_to_coords('55004481'), cep_to_coords('52125070'), cep_to_coords('54380085'), cep_to_coords('55155610'), cep_to_coords('52120472'), cep_to_coords('56510430'), cep_to_coords('54160665'), cep_to_coords('53560540'), cep_to_coords('51020024'), cep_to_coords('53580032'), cep_to_coords('56515550'), cep_to_coords('50750125'), cep_to_coords('51310060'), cep_to_coords('53520525'), cep_to_coords('54353420'), cep_to_coords('54170120'), cep_to_coords('53070530'), cep_to_coords('50920440'), cep_to_coords('51750515'), cep_to_coords('52111920'), cep_to_coords('50193019'), cep_to_coords('52140511'), cep_to_coords('52510510'), cep_to_coords('5800000000'), cep_to_coords('98589243'), cep_to_coords('52091235'), cep_to_coords('50980545'), cep_to_coords('55292360'), cep_to_coords('52090013'), cep_to_coords('56307205'), cep_to_coords('51720070'), cep_to_coords('57720070'), cep_to_coords('52121582'), cep_to_coords('55032250'), cep_to_coords('54735571'), cep_to_coords('55965000'), cep_to_coords('56915015'), cep_to_coords('55294511'), cep_to_coords('51325012'), cep_to_coords('10110280'), cep_to_coords('51340002'), cep_to_coords('54260460'), cep_to_coords('54505340'), cep_to_coords('54170460'), cep_to_coords('35520322'), cep_to_coords('50711071'), cep_to_coords('51011550'), cep_to_coords('54490580'), cep_to_coords('52041655'), cep_to_coords('54362072'), cep_to_coords('52165195'), cep_to_coords('56504065'), cep_to_coords('55895105'), cep_to_coords('52090605'), cep_to_coords('53530740'), cep_to_coords('50810150'), cep_to_coords('54940090'), cep_to_coords('50820441'), cep_to_coords('50420390'), cep_to_coords('50420350'), cep_to_coords('54705759'), cep_to_coords('54315197'), cep_to_coords('55035125'), cep_to_coords('56312540'), cep_to_coords('53625340'), cep_to_coords('52091191'), cep_to_coords('54080060'), cep_to_coords('52170410'), cep_to_coords('54400502'), cep_to_coords('56512841'), cep_to_coords('54580970'), cep_to_coords('54517015'), cep_to_coords('54250602'), cep_to_coords('50980150'), cep_to_coords('56504075'), cep_to_coords('53350476'), cep_to_coords('50620390'), cep_to_coords('53320340'), cep_to_coords('52020041'), cep_to_coords('51250050'), cep_to_coords('53443730'), cep_to_coords('53457040'), cep_to_coords('55818550'), cep_to_coords('54330316'), cep_to_coords('55815410'), cep_to_coords('50970102'), cep_to_coords('53320270'), cep_to_coords('55296140'), cep_to_coords('54310711'), cep_to_coords('54768242'), cep_to_coords('54000270'), cep_to_coords('54783290'), cep_to_coords('54789390'), cep_to_coords('56904220'), cep_to_coords('55815110'), cep_to_coords('52260620'), cep_to_coords('27051977'), cep_to_coords('52130131'), cep_to_coords('54725210'), cep_to_coords('53625444'), cep_to_coords('56312135'), cep_to_coords('55608120'), cep_to_coords('56316370'), cep_to_coords('54410060'), cep_to_coords('52280530'), cep_to_coords('54352255'), cep_to_coords('51275410'), cep_to_coords('54320011'), cep_to_coords('50006500'), cep_to_coords('55290010'), cep_to_coords('53615065'), cep_to_coords('50193210'), cep_to_coords('54100310'), cep_to_coords('55980000'), cep_to_coords('54771770'), cep_to_coords('53510200'), cep_to_coords('51330370'), cep_to_coords('55627710'), cep_to_coords('50870670'), cep_to_coords('54735245'), cep_to_coords('56320822'), cep_to_coords('51275250'), cep_to_coords('54762800'), cep_to_coords('53425650'), cep_to_coords('54068060'), cep_to_coords('52150250'), cep_to_coords('53360580'), cep_to_coords('50192391'), cep_to_coords('53480413'), cep_to_coords('54340600'), cep_to_coords('51610250'), cep_to_coords('05071999'), cep_to_coords('53625355'), cep_to_coords('54275120'), cep_to_coords('55158063'), cep_to_coords('52110432'), cep_to_coords('50870180'), cep_to_coords('51280310'), cep_to_coords('53290401'), cep_to_coords('50060370'), cep_to_coords('54400555'), cep_to_coords('50614144'), cep_to_coords('51280080'), cep_to_coords('52165051'), cep_to_coords('55519000'), cep_to_coords('54696315'), cep_to_coords('54126355'), cep_to_coords('56507260'), cep_to_coords('56730240'), cep_to_coords('55192572'), cep_to_coords('51170540'), cep_to_coords('50711670'), cep_to_coords('51130118'), cep_to_coords('56326360'), cep_to_coords('54439200'), cep_to_coords('53645337'), cep_to_coords('54771660'), cep_to_coords('5300000000'), cep_to_coords('50000001'), cep_to_coords('50800010'), cep_to_coords('53635590'), cep_to_coords('54525400'), cep_to_coords('54260001'), cep_to_coords('53153400'), cep_to_coords('53421170'), cep_to_coords('56313400'), cep_to_coords('53416050'), cep_to_coords('54021000'), cep_to_coords('53030340'), cep_to_coords('52070050'), cep_to_coords('50769000'), cep_to_coords('51070120'), cep_to_coords('51120170'), cep_to_coords('50760013'), cep_to_coords('55194025'), cep_to_coords('54720798'), cep_to_coords('56322542'), cep_to_coords('56340390'), cep_to_coords('53520260'), cep_to_coords('52689888'), cep_to_coords('50910600'), cep_to_coords('13223420'), cep_to_coords('53401611'), cep_to_coords('50611411'), cep_to_coords('53260030'), cep_to_coords('52291108'), cep_to_coords('50100430'), cep_to_coords('50741240'), cep_to_coords('50770900'), cep_to_coords('52041501'), cep_to_coords('54698332'), cep_to_coords('52150080'), cep_to_coords('54786520'), cep_to_coords('54410902'), cep_to_coords('50614114'), cep_to_coords('52111318'), cep_to_coords('50090213'), cep_to_coords('56325700'), cep_to_coords('50540160'), cep_to_coords('51191080'), cep_to_coords('25280043'), cep_to_coords('54767135'), cep_to_coords('53560570'), cep_to_coords('53530600'), cep_to_coords('56503012'), cep_to_coords('54325232'), cep_to_coords('54100676'), cep_to_coords('53530330'), cep_to_coords('54360047'), cep_to_coords('54420525'), cep_to_coords('53130635'), cep_to_coords('53403691'), cep_to_coords('53160410'), cep_to_coords('54720155'), cep_to_coords('55644639'), cep_to_coords('55645721'), cep_to_coords('51040500'), cep_to_coords('55813250'), cep_to_coords('56316800'), cep_to_coords('56310430'), cep_to_coords('53653004'), cep_to_coords('50875105'), cep_to_coords('53131120'), cep_to_coords('52070271'), cep_to_coords('50730740'), cep_to_coords('52280062'), cep_to_coords('54280073'), cep_to_coords('53431105'), cep_to_coords('54310362'), cep_to_coords('55154570'), cep_to_coords('52340045'), cep_to_coords('56061411'), cep_to_coords('53114455'), cep_to_coords('54150602'), cep_to_coords('55294390'), cep_to_coords('52040092'), cep_to_coords('53425720'), cep_to_coords('56310250'), cep_to_coords('56302162'), cep_to_coords('52080201'), cep_to_coords('54360142'), cep_to_coords('52031486'), cep_to_coords('50624000'), cep_to_coords('53310480'), cep_to_coords('55870970'), cep_to_coords('54315050'), cep_to_coords('56332760'), cep_to_coords('55010265'), cep_to_coords('55292246'), cep_to_coords('55292245'), cep_to_coords('51320520'), cep_to_coords('52655420'), cep_to_coords('54330543'), cep_to_coords('55295156'), cep_to_coords('55150110'), cep_to_coords('56327150'), cep_to_coords('53280050'), cep_to_coords('54325770'), cep_to_coords('56950972'), cep_to_coords('52090060'), cep_to_coords('50791133'), cep_to_coords('54580120'), cep_to_coords('54768843'), cep_to_coords('51350430'), cep_to_coords('50760485'), cep_to_coords('52280175'), cep_to_coords('52121235'), cep_to_coords('56000020'), cep_to_coords('54170815'), cep_to_coords('50471010'), cep_to_coords('55291350'), cep_to_coords('53431770'), cep_to_coords('53510670'), cep_to_coords('53160060'), cep_to_coords('51170230'), cep_to_coords('55292375'), cep_to_coords('53585010'), cep_to_coords('54490700'), cep_to_coords('54420440'), cep_to_coords('51240203'), cep_to_coords('53200270'), cep_to_coords('52211705'), cep_to_coords('54735255'), cep_to_coords('53640074'), cep_to_coords('53401660'), cep_to_coords('54330055'), cep_to_coords('50620310'), cep_to_coords('57180050'), cep_to_coords('53402525'), cep_to_coords('51171055'), cep_to_coords('53405540'), cep_to_coords('50791355'), cep_to_coords('50123902'), cep_to_coords('53512010'), cep_to_coords('54730160'), cep_to_coords('54777140'), cep_to_coords('53190660'), cep_to_coords('50721620'), cep_to_coords('56390000'), cep_to_coords('56313630'), cep_to_coords('53435453'), cep_to_coords('53350370'), cep_to_coords('24/10/1972'), cep_to_coords('52190251'), cep_to_coords('50000233'), cep_to_coords('53540170'), cep_to_coords('56302161'), cep_to_coords('51021528'), cep_to_coords('54100021'), cep_to_coords('53425625'), cep_to_coords('53402650'), cep_to_coords('53530645'), cep_to_coords('53437640'), cep_to_coords('55640295'), cep_to_coords('55811100'), cep_to_coords('55810550'), cep_to_coords('55814150'), cep_to_coords('54762181'), cep_to_coords('52071620'), cep_to_coords('55294823'), cep_to_coords('28860000'), cep_to_coords('56332700'), cep_to_coords('56331300'), cep_to_coords('56330150'), cep_to_coords('56502355'), cep_to_coords('54355594'), cep_to_coords('53560770'), cep_to_coords('51060070'), cep_to_coords('51180280'), cep_to_coords('53220107'), cep_to_coords('50080035'), cep_to_coords('54080470'), cep_to_coords('55560970'), cep_to_coords('56515580'), cep_to_coords('51270112'), cep_to_coords('53620200'), cep_to_coords('55819100'), cep_to_coords('52111642'), cep_to_coords('54580050'), cep_to_coords('53150180'), cep_to_coords('54280727'), cep_to_coords('56506370'), cep_to_coords('53140740'), cep_to_coords('54325222'), cep_to_coords('55670541'), cep_to_coords('53270340'), cep_to_coords('53360560'), cep_to_coords('54140541'), cep_to_coords('55902000'), cep_to_coords('55015530'), cep_to_coords('53403520'), cep_to_coords('52131021'), cep_to_coords('54330360'), cep_to_coords('53087005'), cep_to_coords('54530315'), cep_to_coords('53220123'), cep_to_coords('54520550'), cep_to_coords('54517430'), cep_to_coords('50410700'), cep_to_coords('54589065'), cep_to_coords('57440320'), cep_to_coords('61020480'), cep_to_coords('56505430'), cep_to_coords('50005090'), cep_to_coords('51230261'), cep_to_coords('53433665'), cep_to_coords('50610191'), cep_to_coords('54715795'), cep_to_coords('51240530'), cep_to_coords('52191740'), cep_to_coords('52191095'), cep_to_coords('53409505'), cep_to_coords('54250622'), cep_to_coords('53520180'), cep_to_coords('54345150'), cep_to_coords('50830640'), cep_to_coords('52081760'), cep_to_coords('20690290'), cep_to_coords('50749240'), cep_to_coords('55192599'), cep_to_coords('53610346'), cep_to_coords('52091500'), cep_to_coords('50110545'), cep_to_coords('53530200'), cep_to_coords('53433270'), cep_to_coords('52191005'), cep_to_coords('54270660'), cep_to_coords('10373073'), cep_to_coords('55155600'), cep_to_coords('55293230'), cep_to_coords('53060487'), cep_to_coords('55296188'), cep_to_coords('52080057'), cep_to_coords('59230050'), cep_to_coords('52190105'), cep_to_coords('52291645'), cep_to_coords('50880795'), cep_to_coords('52090527'), cep_to_coords('55666500'), cep_to_coords('55816311'), cep_to_coords('51170190'), cep_to_coords('53270245'), cep_to_coords('56580365'), cep_to_coords('56912268'), cep_to_coords('53815105'), cep_to_coords('50960690'), cep_to_coords('55010525'), cep_to_coords('55670260'), cep_to_coords('55150615'), cep_to_coords('46900000'), cep_to_coords('55027635'), cep_to_coords('54368110'), cep_to_coords('50771521'), cep_to_coords('55195598'), cep_to_coords('54345020'), cep_to_coords('54580730'), cep_to_coords('51030490'), cep_to_coords('54495070'), cep_to_coords('55153555'), cep_to_coords('50550555'), cep_to_coords('50192903'), cep_to_coords('55194130'), cep_to_coords('51650280'), cep_to_coords('54310075'), cep_to_coords('54310750'), cep_to_coords('54762623'), cep_to_coords('54245250'), cep_to_coords('50731180'), cep_to_coords('50780380'), cep_to_coords('53415710'), cep_to_coords('50641230'), cep_to_coords('51130705'), cep_to_coords('50750970'), cep_to_coords('54230520'), cep_to_coords('52121605'), cep_to_coords('52226010'), cep_to_coords('54230300'), cep_to_coords('55292270'), cep_to_coords('56326150'), cep_to_coords('55299698'), cep_to_coords('55036605'), cep_to_coords('54365619'), cep_to_coords('55030110'), cep_to_coords('69900000'), cep_to_coords('50870210'), cep_to_coords('52010400'), cep_to_coords('51270700'), cep_to_coords('55643115'), cep_to_coords('54340545'), cep_to_coords('54340478'), cep_to_coords('50930185'), cep_to_coords('54269836'), cep_to_coords('51209310'), cep_to_coords('53020050'), cep_to_coords('53510340'), cep_to_coords('51220231'), cep_to_coords('51180482'), cep_to_coords('55000870'), cep_to_coords('50192302'), cep_to_coords('55026471'), cep_to_coords('55609730'), cep_to_coords('54767770'), cep_to_coords('53240550'), cep_to_coords('55294360'), cep_to_coords('53330660'), cep_to_coords('53429410'), cep_to_coords('50820122'), cep_to_coords('59442040'), cep_to_coords('59442090'), cep_to_coords('55813320'), cep_to_coords('52221153'), cep_to_coords('50190690'), cep_to_coords('53070300'), cep_to_coords('56314370'), cep_to_coords('53403130'), cep_to_coords('52270090'), cep_to_coords('54767240'), cep_to_coords('50070650'), cep_to_coords('52090775'), cep_to_coords('45430100'), cep_to_coords('50741555'), cep_to_coords('52080190'), cep_to_coords('51340450'), cep_to_coords('51275050'), cep_to_coords('55030230'), cep_to_coords('53515485'), cep_to_coords('53580720'), cep_to_coords('50371000'), cep_to_coords('56912264'), cep_to_coords('54430303'), cep_to_coords('53421710'), cep_to_coords('56512625'), cep_to_coords('53530050'), cep_to_coords('52280215'), cep_to_coords('55819680'), cep_to_coords('53330545'), cep_to_coords('52020900'), cep_to_coords('50791540'), cep_to_coords('52165031'), cep_to_coords('50680250'), cep_to_coords('53550126'), cep_to_coords('54320002'), cep_to_coords('50100600'), cep_to_coords('54370140'), cep_to_coords('51330285'), cep_to_coords('52070631'), cep_to_coords('53402735'), cep_to_coords('53640192'), cep_to_coords('52040051'), cep_to_coords('54140320'), cep_to_coords('53416301'), cep_to_coords('50690210'), cep_to_coords('52090076'), cep_to_coords('30071968'), cep_to_coords('50820145'), cep_to_coords('54140120'), cep_to_coords('50711540'), cep_to_coords('50912310'), cep_to_coords('50401200'), cep_to_coords('54100250'), cep_to_coords('54090250'), cep_to_coords('56912184'), cep_to_coords('52980020'), cep_to_coords('54430120'), cep_to_coords('54130190'), cep_to_coords('52020244'), cep_to_coords('55811080'), cep_to_coords('56362015'), cep_to_coords('52291425'), cep_to_coords('35500026'), cep_to_coords('56515130'), cep_to_coords('52091411'), cep_to_coords('51280550'), cep_to_coords('51150242'), cep_to_coords('51110260'), cep_to_coords('55819630'), cep_to_coords('55816070'), cep_to_coords('55818210'), cep_to_coords('55155530'), cep_to_coords('54110071'), cep_to_coords('50930110'), cep_to_coords('53620240'), cep_to_coords('55000140'), cep_to_coords('52113031'), cep_to_coords('55193100'), cep_to_coords('55293100'), cep_to_coords('51433047'), cep_to_coords('53407365'), cep_to_coords('54325780'), cep_to_coords('55614710'), cep_to_coords('53434180'), cep_to_coords('54410120'), cep_to_coords('56021360'), cep_to_coords('53609400'), cep_to_coords('51010172'), cep_to_coords('53505720'), cep_to_coords('51103031'), cep_to_coords('54260412'), cep_to_coords('52210062'), cep_to_coords('53150021'), cep_to_coords('53402162'), cep_to_coords('55230000'), cep_to_coords('53545060'), cep_to_coords('51250210'), cep_to_coords('53330500'), cep_to_coords('54370160'), cep_to_coords('54470103'), cep_to_coords('52130452'), cep_to_coords('41290300'), cep_to_coords('54330231'), cep_to_coords('55433024'), cep_to_coords('54340587'), cep_to_coords('52001100'), cep_to_coords('52091430'), cep_to_coords('50720080'), cep_to_coords('53320390'), cep_to_coords('52031440'), cep_to_coords('51179240'), cep_to_coords('56312080'), cep_to_coords('52160410'), cep_to_coords('54762135'), cep_to_coords('53439590'), cep_to_coords('50640121'), cep_to_coords('50850390'), cep_to_coords('54470520'), cep_to_coords('52080235'), cep_to_coords('54325153'), cep_to_coords('54230610'), cep_to_coords('53315390'), cep_to_coords('50371260'), cep_to_coords('81984262'), cep_to_coords('53429100'), cep_to_coords('56912187'), cep_to_coords('52291085'), cep_to_coords('53200300'), cep_to_coords('56532500'), cep_to_coords('58870000'), cep_to_coords('55292325'), cep_to_coords('52230130'), cep_to_coords('54589535'), cep_to_coords('50660670'), cep_to_coords('55036452'), cep_to_coords('52228023'), cep_to_coords('54210313'), cep_to_coords('52080320'), cep_to_coords('54715060'), cep_to_coords('54715210'), cep_to_coords('52280108'), cep_to_coords('53403311'), cep_to_coords('51340500'), cep_to_coords('50193109'), cep_to_coords('53210081'), cep_to_coords('53423270'), cep_to_coords('51345270'), cep_to_coords('50110236'), cep_to_coords('55298080'), cep_to_coords('53135400'), cep_to_coords('54020090'), cep_to_coords('55602152'), cep_to_coords('53550820'), cep_to_coords('52680391'), cep_to_coords('52280391'), cep_to_coords('51131370'), cep_to_coords('50670540'), cep_to_coords('55154595'), cep_to_coords('55295020'), cep_to_coords('50090693'), cep_to_coords('53409550'), cep_to_coords('55296538'), cep_to_coords('54769425'), cep_to_coords('52040230'), cep_to_coords('54767378'), cep_to_coords('54000450'), cep_to_coords('55813300'), cep_to_coords('54220333'), cep_to_coords('54705640'), cep_to_coords('51250252'), cep_to_coords('55152110'), cep_to_coords('50050315'), cep_to_coords('54325630'), cep_to_coords('54280140'), cep_to_coords('59910410'), cep_to_coords('54495376'), cep_to_coords('54430340'), cep_to_coords('56503045'), cep_to_coords('51300029'), cep_to_coords('54330259'), cep_to_coords('50791680'), cep_to_coords('54270460'), cep_to_coords('55190509'), cep_to_coords('53431495'), cep_to_coords('53051000'), cep_to_coords('55194160'), cep_to_coords('52070520'), cep_to_coords('54320280'), cep_to_coords('55192205'), cep_to_coords('55190368'), cep_to_coords('55192506'), cep_to_coords('51270701'), cep_to_coords('55179000'), cep_to_coords('55192420'), cep_to_coords('55190776'), cep_to_coords('53345510'), cep_to_coords('50920715'), cep_to_coords('54315820'), cep_to_coords('53415200'), cep_to_coords('54216270'), cep_to_coords('55819135'), cep_to_coords('54522075'), cep_to_coords('51250620'), cep_to_coords('55811010'), cep_to_coords('52462132'), cep_to_coords('52051680'), cep_to_coords('51030710'), cep_to_coords('50930141'), cep_to_coords('54450280'), cep_to_coords('53409846'), cep_to_coords('54340350'), cep_to_coords('53220109'), cep_to_coords('63109000'), cep_to_coords('54340436'), cep_to_coords('54700175'), cep_to_coords('54730735'), cep_to_coords('50010100'), cep_to_coords('50112820'), cep_to_coords('3613000148'), cep_to_coords('50690680'), cep_to_coords('50740060'), cep_to_coords('52081534'), cep_to_coords('54730240'), cep_to_coords('54353090'), cep_to_coords('55299899'), cep_to_coords('52490310'), cep_to_coords('50049120'), cep_to_coords('04581050'), cep_to_coords('54320820'), cep_to_coords('54460300'), cep_to_coords('55550900'), cep_to_coords('54410377'), cep_to_coords('54170320'), cep_to_coords('54735815'), cep_to_coords('65465464'), cep_to_coords('54730360'), cep_to_coords('56903465'), cep_to_coords('54745010'), cep_to_coords('55030640'), cep_to_coords('50711220'), cep_to_coords('55016630'), cep_to_coords('53110770'), cep_to_coords('51340060'), cep_to_coords('50771970'), cep_to_coords('55610440'), cep_to_coords('54740010'), cep_to_coords('53416555'), cep_to_coords('54100291'), cep_to_coords('15101967'), cep_to_coords('50690760'), cep_to_coords('50721115'), cep_to_coords('54515050'), cep_to_coords('50960671'), cep_to_coords('51330500'), cep_to_coords('50980300'), cep_to_coords('53401601'), cep_to_coords('50980020'), cep_to_coords('52030031'), cep_to_coords('50610610'), cep_to_coords('52120421'), cep_to_coords('54789542'), cep_to_coords('55195042'), cep_to_coords('54789635'), cep_to_coords('54345605'), cep_to_coords('53411703'), cep_to_coords('50100480'), cep_to_coords('54560000'), cep_to_coords('50020220'), cep_to_coords('50870780'), cep_to_coords('53441308'), cep_to_coords('56515240'), cep_to_coords('53630977'), cep_to_coords('53090125'), cep_to_coords('54290020'), cep_to_coords('54740530'), cep_to_coords('53510100'), cep_to_coords('53080833'), cep_to_coords('56503530'), cep_to_coords('55152370'), cep_to_coords('56228000'), cep_to_coords('55151120'), cep_to_coords('55292110'), cep_to_coords('56326825'), cep_to_coords('53405711'), cep_to_coords('55818415'), cep_to_coords('51021031'), cep_to_coords('53002160'), cep_to_coords('54520165'), cep_to_coords('51621550'), cep_to_coords('53429290'), cep_to_coords('56333015'), cep_to_coords('53605540'), cep_to_coords('50783320'), cep_to_coords('53520020'), cep_to_coords('54495200'), cep_to_coords('51020051'), cep_to_coords('53637200'), cep_to_coords('52060490'), cep_to_coords('55026435'), cep_to_coords('530000000'), cep_to_coords('53080171'), cep_to_coords('52091110'), cep_to_coords('50751275'), cep_to_coords('55014396'), cep_to_coords('53550770'), cep_to_coords('54250536'), cep_to_coords('50060120'), cep_to_coords('50020800'), cep_to_coords('56100000'), cep_to_coords('50191130'), cep_to_coords('5549000'), cep_to_coords('84410695'), cep_to_coords('55150080'), cep_to_coords('50920901'), cep_to_coords('53423800'), cep_to_coords('50791685'), cep_to_coords('50730011'), cep_to_coords('54320138'), cep_to_coords('51230401'), cep_to_coords('56332335'), cep_to_coords('56231045'), cep_to_coords('50650004'), cep_to_coords('53610330'), cep_to_coords('50101760'), cep_to_coords('50210210'), cep_to_coords('56740170'), cep_to_coords('56320774'), cep_to_coords('50100110'), cep_to_coords('54786675'), cep_to_coords('54530260'), cep_to_coords('54315061'), cep_to_coords('53500015'), cep_to_coords('51270200'), cep_to_coords('54580252'), cep_to_coords('53550590'), cep_to_coords('55299357'), cep_to_coords('53439800'), cep_to_coords('55290400'), cep_to_coords('59792000'), cep_to_coords('55652000'), cep_to_coords('51140660'), cep_to_coords('54705830'), cep_to_coords('56630000'), cep_to_coords('53637050'), cep_to_coords('55816650'), cep_to_coords('55816610'), cep_to_coords('55816810'), cep_to_coords('59029560'), cep_to_coords('54525360'), cep_to_coords('51437400'), cep_to_coords('54580582'), cep_to_coords('53239140'), cep_to_coords('53630407'), cep_to_coords('50740014'), cep_to_coords('54382055'), cep_to_coords('54080361'), cep_to_coords('50630050'), cep_to_coords('53530260'), cep_to_coords('52030490'), cep_to_coords('50770560'), cep_to_coords('52160080'), cep_to_coords('51170528'), cep_to_coords('56316827'), cep_to_coords('55819600'), cep_to_coords('52170420'), cep_to_coords('55608180'), cep_to_coords('51110370'), cep_to_coords('53630477'), cep_to_coords('50688180'), cep_to_coords('53429830'), cep_to_coords('52116622'), cep_to_coords('53190440'), cep_to_coords('51350291'), cep_to_coords('55641670'), cep_to_coords('55195629'), cep_to_coords('54720016'), cep_to_coords('53530414'), cep_to_coords('51335027'), cep_to_coords('53350015'), cep_to_coords('52081990'), cep_to_coords('53335020'), cep_to_coords('53530630'), cep_to_coords('50751790'), cep_to_coords('50640202'), cep_to_coords('54170675'), cep_to_coords('54450310'), cep_to_coords('52080212'), cep_to_coords('56309290'), cep_to_coords('48905541'), cep_to_coords('54470285'), cep_to_coords('52130453'), cep_to_coords('50781125'), cep_to_coords('54705152'), cep_to_coords('53441350'), cep_to_coords('53320300'), cep_to_coords('53421220'), cep_to_coords('51250293'), cep_to_coords('52390033'), cep_to_coords('53570288'), cep_to_coords('55031120'), cep_to_coords('50010070'), cep_to_coords('54786090'), cep_to_coords('55157430'), cep_to_coords('53320045'), cep_to_coords('55240220'), cep_to_coords('52221390'), cep_to_coords('53433050'), cep_to_coords('52131625'), cep_to_coords('51250304'), cep_to_coords('50470555'), cep_to_coords('15081993'), cep_to_coords('52071317'), cep_to_coords('56503192'), cep_to_coords('54090369'), cep_to_coords('54756270'), cep_to_coords('52035020'), cep_to_coords('55036538'), cep_to_coords('54315002'), cep_to_coords('54580295'), cep_to_coords('54330842'), cep_to_coords('54150150'), cep_to_coords('54340443'), cep_to_coords('52130505'), cep_to_coords('55150440'), cep_to_coords('50830040'), cep_to_coords('51340110'), cep_to_coords('55001650'), cep_to_coords('50912321'), cep_to_coords('54240390'), cep_to_coords('54789118'), cep_to_coords('48602590'), cep_to_coords('54400380'), cep_to_coords('51260005'), cep_to_coords('56330070'), cep_to_coords('50912039'), cep_to_coords('53190820'), cep_to_coords('55614465'), cep_to_coords('50960420'), cep_to_coords('55151645'), cep_to_coords('50830562'), cep_to_coords('50100030'), cep_to_coords('55612250'), cep_to_coords('50012932'), cep_to_coords('51345650'), cep_to_coords('55028035'), cep_to_coords('52150123'), cep_to_coords('52070394'), cep_to_coords('54510635'), cep_to_coords('51250410'), cep_to_coords('50900370'), cep_to_coords('53545800'), cep_to_coords('53545662'), cep_to_coords('54325125'), cep_to_coords('50760010'), cep_to_coords('54100312'), cep_to_coords('54431331'), cep_to_coords('50640750'), cep_to_coords('53050520'), cep_to_coords('54130220'), cep_to_coords('54330035'), cep_to_coords('51130190'), cep_to_coords('54490069'), cep_to_coords('54210547'), cep_to_coords('50980595'), cep_to_coords('55299900'), cep_to_coords('53020383'), cep_to_coords('54705240'), cep_to_coords('53419330'), cep_to_coords('50090692'), cep_to_coords('50920708'), cep_to_coords('55194393'), cep_to_coords('50980666'), cep_to_coords('50870290'), cep_to_coords('55642080'), cep_to_coords('69300050'), cep_to_coords('53310780'), cep_to_coords('51021054'), cep_to_coords('54777040'), cep_to_coords('50671020'), cep_to_coords('50193102'), cep_to_coords('04070860'), cep_to_coords('54270805'), cep_to_coords('51030715'), cep_to_coords('51410021'), cep_to_coords('59950000'), cep_to_coords('55614083'), cep_to_coords('51275200'), cep_to_coords('53260260'), cep_to_coords('54410367'), cep_to_coords('51220135'), cep_to_coords('54325045'), cep_to_coords('54505130'), cep_to_coords('54315062'), cep_to_coords('53060440'), cep_to_coords('55190848'), cep_to_coords('54420315'), cep_to_coords('56233000'), cep_to_coords('54495190'), cep_to_coords('51011380'), cep_to_coords('53650710'), cep_to_coords('54340660'), cep_to_coords('50050570'), cep_to_coords('52111380'), cep_to_coords('52191200'), cep_to_coords('54771681'), cep_to_coords('50021330'), cep_to_coords('51250547'), cep_to_coords('54240410'), cep_to_coords('56201000'), cep_to_coords('54460322'), cep_to_coords('52060010'), cep_to_coords('54753712'), cep_to_coords('48903600'), cep_to_coords('50660330'), cep_to_coords('56600500'), cep_to_coords('52090177'), cep_to_coords('53401458'), cep_to_coords('56332360'), cep_to_coords('53444162'), cep_to_coords('54789400'), cep_to_coords('52071385'), cep_to_coords('52825000'), cep_to_coords('54368150'), cep_to_coords('51330473'), cep_to_coords('51250240'), cep_to_coords('54730350'), cep_to_coords('54705470'), cep_to_coords('52031365'), cep_to_coords('54460160'), cep_to_coords('50770719'), cep_to_coords('54260350'), cep_to_coords('55157420'), cep_to_coords('54768464'), cep_to_coords('55002104'), cep_to_coords('54251733'), cep_to_coords('53610450'), cep_to_coords('53401320'), cep_to_coords('53625315'), cep_to_coords('50771745'), cep_to_coords('55816320'), cep_to_coords('53650525'), cep_to_coords('53401445'), cep_to_coords('50670640'), cep_to_coords('51300540'), cep_to_coords('52071545'), cep_to_coords('55158045'), cep_to_coords('50920160'), cep_to_coords('54350125'), cep_to_coords('53525700'), cep_to_coords('53650640'), cep_to_coords('52280208'), cep_to_coords('50660306'), cep_to_coords('53435604'), cep_to_coords('51340524'), cep_to_coords('56680000'), cep_to_coords('53433040'), cep_to_coords('53625125'), cep_to_coords('53570214'), cep_to_coords('53565530'), cep_to_coords('54460682'), cep_to_coords('53540510'), cep_to_coords('54315375'), cep_to_coords('54090270'), cep_to_coords('54340490'), cep_to_coords('55194200'), cep_to_coords('50600380'), cep_to_coords('49100000'), cep_to_coords('52011290'), cep_to_coords('53640031'), cep_to_coords('53350351'), cep_to_coords('55804000'), cep_to_coords('55814600'), cep_to_coords('54765035'), cep_to_coords('52211115'), cep_to_coords('52090611'), cep_to_coords('50010971'), cep_to_coords('33020006'), cep_to_coords('53420010'), cep_to_coords('50690575'), cep_to_coords('55153181'), cep_to_coords('68742005'), cep_to_coords('53150665'), cep_to_coords('545900000'), cep_to_coords('54315358'), cep_to_coords('54880675'), cep_to_coords('54320411'), cep_to_coords('59190000'), cep_to_coords('55346500'), cep_to_coords('53589991'), cep_to_coords('66019300'), cep_to_coords('54762652'), cep_to_coords('55819550'), cep_to_coords('55608678'), cep_to_coords('54510478'), cep_to_coords('55014780'), cep_to_coords('51390235'), cep_to_coords('54100580'), cep_to_coords('50930680'), cep_to_coords('50930281'), cep_to_coords('54430630'), cep_to_coords('51012286'), cep_to_coords('52125270'), cep_to_coords('55024765'), cep_to_coords('55150430'), cep_to_coords('54090392'), cep_to_coords('54275110'), cep_to_coords('53150320'), cep_to_coords('12568966'), cep_to_coords('52800040'), cep_to_coords('16658965'), cep_to_coords('50740556'), cep_to_coords('25866515'), cep_to_coords('12586987'), cep_to_coords('12589687'), cep_to_coords('55299430'), cep_to_coords('54774580'), cep_to_coords('54720123'), cep_to_coords('54160275'), cep_to_coords('05103790'), cep_to_coords('53510428'), cep_to_coords('53404590'), cep_to_coords('52111601'), cep_to_coords('52390032'), cep_to_coords('56325742'), cep_to_coords('52191175'), cep_to_coords('50192039'), cep_to_coords('53510433'), cep_to_coords('50820200'), cep_to_coords('50660070'), cep_to_coords('54080240'), cep_to_coords('50640568'), cep_to_coords('50031293'), cep_to_coords('51730180'), cep_to_coords('53370815'), cep_to_coords('54738050'), cep_to_coords('53137070'), cep_to_coords('54740740'), cep_to_coords('50711150'), cep_to_coords('52120491'), cep_to_coords('55630125'), cep_to_coords('52090180'), cep_to_coords('51010310'), cep_to_coords('11111997'), cep_to_coords('51346100'), cep_to_coords('53585020'), cep_to_coords('54340709'), cep_to_coords('50600070'), cep_to_coords('55602200'), cep_to_coords('53270310'), cep_to_coords('51070461'), cep_to_coords('51254200'), cep_to_coords('53320630'), cep_to_coords('50666760'), cep_to_coords('50090450'), cep_to_coords('53360370'), cep_to_coords('54726120'), cep_to_coords('16121961'), cep_to_coords('54420320'), cep_to_coords('53270255'), cep_to_coords('53433500'), cep_to_coords('50192319'), cep_to_coords('53360220'), cep_to_coords('52291041'), cep_to_coords('55022390'), cep_to_coords('54767360'), cep_to_coords('51340600'), cep_to_coords('50640378'), cep_to_coords('55296194'), cep_to_coords('55151770'), cep_to_coords('52191110'), cep_to_coords('52125080'), cep_to_coords('50910460'), cep_to_coords('53650808'), cep_to_coords('50090694'), cep_to_coords('50230430'), cep_to_coords('54737090'), cep_to_coords('54774350'), cep_to_coords('54730013'), cep_to_coords('54720285'), cep_to_coords('56318610'), cep_to_coords('56314410'), cep_to_coords('56310753'), cep_to_coords('55920999'), cep_to_coords('54519170'), cep_to_coords('52165045'), cep_to_coords('54505490'), cep_to_coords('55022445'), cep_to_coords('52090682'), cep_to_coords('54270351'), cep_to_coords('17700000'), cep_to_coords('54515526'), cep_to_coords('53625448'), cep_to_coords('54520070'), cep_to_coords('53570275'), cep_to_coords('54737310'), cep_to_coords('52390080'), cep_to_coords('54763220'), cep_to_coords('54715440'), cep_to_coords('55038460'), cep_to_coords('55019360'), cep_to_coords('54140263'), cep_to_coords('53433230'), cep_to_coords('53400080'), cep_to_coords('53330290'), cep_to_coords('54708757'), cep_to_coords('54280610'), cep_to_coords('56332310'), cep_to_coords('04111992'), cep_to_coords('50170900'), cep_to_coords('55721775'), cep_to_coords('50810580'), cep_to_coords('56517090'), cep_to_coords('55296560'), cep_to_coords('52130461'), cep_to_coords('54753811'), cep_to_coords('50960477'), cep_to_coords('53401305'), cep_to_coords('50912392'), cep_to_coords('53439720'), cep_to_coords('12121968'), cep_to_coords('56509005'), cep_to_coords('50761750'), cep_to_coords('56330220'), cep_to_coords('56314000'), cep_to_coords('53405110'), cep_to_coords('50150160'), cep_to_coords('54530100'), cep_to_coords('55580999'), cep_to_coords('50790113'), cep_to_coords('55816510'), cep_to_coords('50711530'), cep_to_coords('51800060'), cep_to_coords('53685113'), cep_to_coords('51940260'), cep_to_coords('56310520'), cep_to_coords('41110000'), cep_to_coords('54250610'), cep_to_coords('50100590'), cep_to_coords('52130295'), cep_to_coords('54290111'), cep_to_coords('54280631'), cep_to_coords('52041285'), cep_to_coords('53409843'), cep_to_coords('54411315'), cep_to_coords('54505540'), cep_to_coords('50620670'), cep_to_coords('50060705'), cep_to_coords('50970187'), cep_to_coords('55156405'), cep_to_coords('55578008'), cep_to_coords('52131290'), cep_to_coords('55150770'), cep_to_coords('53525742'), cep_to_coords('52121495'), cep_to_coords('53426720'), cep_to_coords('53530235'), cep_to_coords('51011006'), cep_to_coords('50700000'), cep_to_coords('52291126'), cep_to_coords('53350441'), cep_to_coords('53090230'), cep_to_coords('52090170'), cep_to_coords('54525230'), cep_to_coords('50791351'), cep_to_coords('54670060'), cep_to_coords('54325242'), cep_to_coords('54525430'), cep_to_coords('53405060'), cep_to_coords('53110060'), cep_to_coords('52290070'), cep_to_coords('54789505'), cep_to_coords('53170240'), cep_to_coords('53270715'), cep_to_coords('56502190'), cep_to_coords('52080062'), cep_to_coords('52061230'), cep_to_coords('55192563'), cep_to_coords('55795000'), cep_to_coords('55017400'), cep_to_coords('54520490'), cep_to_coords('54380160'), cep_to_coords('54825000'), cep_to_coords('53249000'), cep_to_coords('55645694'), cep_to_coords('53500150'), cep_to_coords('55490291'), cep_to_coords('53429330'), cep_to_coords('56312295'), cep_to_coords('53421363'), cep_to_coords('54240375'), cep_to_coords('54777680'), cep_to_coords('53497793'), cep_to_coords('54705083'), cep_to_coords('54740410'), cep_to_coords('52390223'), cep_to_coords('56313650'), cep_to_coords('52191520'), cep_to_coords('54310204'), cep_to_coords('54210450'), cep_to_coords('53560010'), cep_to_coords('51179300'), cep_to_coords('54310001'), cep_to_coords('52130230'), cep_to_coords('55024160'), cep_to_coords('55813339'), cep_to_coords('53635030'), cep_to_coords('54300060'), cep_to_coords('21340000'), cep_to_coords('52240071'), cep_to_coords('51345036'), cep_to_coords('53420200'), cep_to_coords('55153615'), cep_to_coords('55191457'), cep_to_coords('56504025'), cep_to_coords('53545670'), cep_to_coords('55195079'), cep_to_coords('55190733'), cep_to_coords('53650772'), cep_to_coords('54150115'), cep_to_coords('54480430'), cep_to_coords('55195500'), cep_to_coords('50700020'), cep_to_coords('54170040'), cep_to_coords('50790700'), cep_to_coords('51335160'), cep_to_coords('53625736'), cep_to_coords('54250493'), cep_to_coords('56316340'), cep_to_coords('53550540'), cep_to_coords('10314013'), cep_to_coords('50920570'), cep_to_coords('56333025'), cep_to_coords('54230142'), cep_to_coords('50711115'), cep_to_coords('52130201'), cep_to_coords('12568968'), cep_to_coords('54315540'), cep_to_coords('54768298'), cep_to_coords('52160490'), cep_to_coords('54517180'), cep_to_coords('53830470'), cep_to_coords('54505500'), cep_to_coords('52031500'), cep_to_coords('54580542'), cep_to_coords('56909175'), cep_to_coords('51060410'), cep_to_coords('55644675'), cep_to_coords('56915080'), cep_to_coords('51240815'), cep_to_coords('54715055'), cep_to_coords('50791138'), cep_to_coords('56304620'), cep_to_coords('54505510'), cep_to_coords('55606265'), cep_to_coords('69300000'), cep_to_coords('50790595'), cep_to_coords('54325023'), cep_to_coords('52125260'), cep_to_coords('53160820'), cep_to_coords('53615490'), cep_to_coords('50480000'), cep_to_coords('54720140'), cep_to_coords('52211472'), cep_to_coords('51115000'), cep_to_coords('50620540'), cep_to_coords('52130180'), cep_to_coords('55157400'), cep_to_coords('51150380'), cep_to_coords('50190293'), cep_to_coords('54756325'), cep_to_coords('54325640'), cep_to_coords('50680590'), cep_to_coords('55035000'), cep_to_coords('50480550'), cep_to_coords('53402615'), cep_to_coords('55644224'), cep_to_coords('54705585'), cep_to_coords('51290490'), cep_to_coords('54733100'), cep_to_coords('53540750'), cep_to_coords('55012090'), cep_to_coords('54420570'), cep_to_coords('52021210'), cep_to_coords('55955000'), cep_to_coords('54768708'), cep_to_coords('54315680'), cep_to_coords('53431610'), cep_to_coords('50860210'), cep_to_coords('54400235'), cep_to_coords('54759621'), cep_to_coords('54490670'), cep_to_coords('54443016'), cep_to_coords('51171130'), cep_to_coords('54768778'), cep_to_coords('54774670'), cep_to_coords('53422030'), cep_to_coords('54090394'), cep_to_coords('53419195'), cep_to_coords('54780780'), cep_to_coords('54441625'), cep_to_coords('54330720'), cep_to_coords('54727140'), cep_to_coords('54325230'), cep_to_coords('51030880'), cep_to_coords('52131005'), cep_to_coords('55158750'), cep_to_coords('50930170'), cep_to_coords('53637130'), cep_to_coords('50701123'), cep_to_coords('53250161'), cep_to_coords('54450500'), cep_to_coords('54650270'), cep_to_coords('52390310'), cep_to_coords('55004090'), cep_to_coords('54515040'), cep_to_coords('53545770'), cep_to_coords('53300120'), cep_to_coords('53455610'), cep_to_coords('51030735'), cep_to_coords('51031070'), cep_to_coords('10987707'), cep_to_coords('55813560'), cep_to_coords('50021360'), cep_to_coords('50780025'), cep_to_coords('54100470'), cep_to_coords('53570135'), cep_to_coords('50760205'), cep_to_coords('54720812'), cep_to_coords('53408410'), cep_to_coords('60325000'), cep_to_coords('54100145'), cep_to_coords('54300080'), cep_to_coords('44290111'), cep_to_coords('51202190'), cep_to_coords('50820121'), cep_to_coords('53320500'), cep_to_coords('54433302'), cep_to_coords('55021020'), cep_to_coords('55814130'), cep_to_coords('55640315'), cep_to_coords('54727020'), cep_to_coords('58424213'), cep_to_coords('51340120'), cep_to_coords('54100153'), cep_to_coords('53419670'), cep_to_coords('53560600'), cep_to_coords('52580531'), cep_to_coords('53280370'), cep_to_coords('50110187'), cep_to_coords('50701460'), cep_to_coords('53565362'), cep_to_coords('54727240'), cep_to_coords('50340640'), cep_to_coords('35054271'), cep_to_coords('53545720'), cep_to_coords('53525660'), cep_to_coords('53520666'), cep_to_coords('54420395'), cep_to_coords('50193108'), cep_to_coords('53552220'), cep_to_coords('54300079'), cep_to_coords('53545014'), cep_to_coords('50110213'), cep_to_coords('54093393'), cep_to_coords('52110480'), cep_to_coords('54019230'), cep_to_coords('50791391'), cep_to_coords('53270635'), cep_to_coords('52070485'), cep_to_coords('52390495'), cep_to_coords('53620144'), cep_to_coords('52081527'), cep_to_coords('50789790'), cep_to_coords('54250280'), cep_to_coords('52590415'), cep_to_coords('54789689'), cep_to_coords('53640579'), cep_to_coords('50087013'), cep_to_coords('55292225'), cep_to_coords('50830560'), cep_to_coords('54330735'), cep_to_coords('51320720'), cep_to_coords('51270735'), cep_to_coords('50660380'), cep_to_coords('54090081'), cep_to_coords('51290609'), cep_to_coords('53734040'), cep_to_coords('54150621'), cep_to_coords('52200210'), cep_to_coords('54120362'), cep_to_coords('54530410'), cep_to_coords('54290041'), cep_to_coords('53220800'), cep_to_coords('55815600'), cep_to_coords('50440350'), cep_to_coords('50791350'), cep_to_coords('56328660'), cep_to_coords('56285000'), cep_to_coords('54160600'), cep_to_coords('54123000'), cep_to_coords('55005054'), cep_to_coords('53431356'), cep_to_coords('54790001'), cep_to_coords('54730001'), cep_to_coords('53580320'), cep_to_coords('50620240'), cep_to_coords('54325200'), cep_to_coords('50920668'), cep_to_coords('55811070'), cep_to_coords('53170520'), cep_to_coords('50671250'), cep_to_coords('52030410'), cep_to_coords('53560560'), cep_to_coords('54160447'), cep_to_coords('54420735'), cep_to_coords('54774115'), cep_to_coords('51030600'), cep_to_coords('53530785'), cep_to_coords('54721430'), cep_to_coords('50850308'), cep_to_coords('54920680'), cep_to_coords('52130245'), cep_to_coords('50000200'), cep_to_coords('50980040'), cep_to_coords('50760060'), cep_to_coords('50875131'), cep_to_coords('53413290'), cep_to_coords('54495408'), cep_to_coords('54415548'), cep_to_coords('54170783'), cep_to_coords('54510325'), cep_to_coords('53635070'), cep_to_coords('55018310'), cep_to_coords('52291199'), cep_to_coords('54160700'), cep_to_coords('34100160'), cep_to_coords('53160720'), cep_to_coords('52090065'), cep_to_coords('52240500'), cep_to_coords('73437170'), cep_to_coords('56517650'), cep_to_coords('50080205'), cep_to_coords('53413160'), cep_to_coords('52131032'), cep_to_coords('50740070'), cep_to_coords('50971090'), cep_to_coords('52111185'), cep_to_coords('50751020'), cep_to_coords('25689464'), cep_to_coords('51345111'), cep_to_coords('53402529'), cep_to_coords('55296452'), cep_to_coords('12568933'), cep_to_coords('52090111'), cep_to_coords('54720205'), cep_to_coords('52131427'), cep_to_coords('53402640'), cep_to_coords('53900970'), cep_to_coords('54170523'), cep_to_coords('54123333'), cep_to_coords('52280494'), cep_to_coords('56506350'), cep_to_coords('50620110'), cep_to_coords('52170170'), cep_to_coords('54740400'), cep_to_coords('54100815'), cep_to_coords('54500050'), cep_to_coords('54500500'), cep_to_coords('51119013'), cep_to_coords('56303050'), cep_to_coords('54720657'), cep_to_coords('54740657'), cep_to_coords('51210160'), cep_to_coords('54270024'), cep_to_coords('55292512'), cep_to_coords('54762540'), cep_to_coords('52052310'), cep_to_coords('53450360'), cep_to_coords('52030230'), cep_to_coords('56503050'), cep_to_coords('53620786'), cep_to_coords('50865150'), cep_to_coords('50810510'), cep_to_coords('53450030'), cep_to_coords('54720290'), cep_to_coords('53635680'), cep_to_coords('55020315'), cep_to_coords('55292675'), cep_to_coords('53554012'), cep_to_coords('52030102'), cep_to_coords('54250111'), cep_to_coords('53415496'), cep_to_coords('55152210'), cep_to_coords('55818430'), cep_to_coords('54345530'), cep_to_coords('54130120'), cep_to_coords('53530005'), cep_to_coords('60801111'), cep_to_coords('50415241'), cep_to_coords('53490350'), cep_to_coords('52191570'), cep_to_coords('53415301'), cep_to_coords('51330110'), cep_to_coords('56325732'), cep_to_coords('55645162'), cep_to_coords('58520230'), cep_to_coords('48903100'), cep_to_coords('56303640'), cep_to_coords('56312530'), cep_to_coords('54123330'), cep_to_coords('52510493'), cep_to_coords('50731515'), cep_to_coords('53000401'), cep_to_coords('50193202'), cep_to_coords('53140020'), cep_to_coords('52041715'), cep_to_coords('56516060'), cep_to_coords('54220690'), cep_to_coords('54450285'), cep_to_coords('50774121'), cep_to_coords('53010190'), cep_to_coords('50912091'), cep_to_coords('50970247'), cep_to_coords('54410580'), cep_to_coords('56903236'), cep_to_coords('10000000'), cep_to_coords('54120021'), cep_to_coords('52096056'), cep_to_coords('54325250'), cep_to_coords('21032021'), cep_to_coords('55024380'), cep_to_coords('56317150'), cep_to_coords('50620600'), cep_to_coords('52090552'), cep_to_coords('53405744'), cep_to_coords('55614455'), cep_to_coords('50460120'), cep_to_coords('55008420'), cep_to_coords('50900035'), cep_to_coords('50800035'), cep_to_coords('54705288'), cep_to_coords('53270111'), cep_to_coords('51270630'), cep_to_coords('54730370'), cep_to_coords('55195000'), cep_to_coords('55291739'), cep_to_coords('53110461'), cep_to_coords('52012078'), cep_to_coords('53402900'), cep_to_coords('53401130'), cep_to_coords('55402250'), cep_to_coords('56280975'), cep_to_coords('54440440'), cep_to_coords('53080400'), cep_to_coords('54250333'), cep_to_coords('54730281'), cep_to_coords('55020631'), cep_to_coords('55070020'), cep_to_coords('54120416'), cep_to_coords('55037281'), cep_to_coords('55195524'), cep_to_coords('55194303'), cep_to_coords('52280531'), cep_to_coords('56306415'), cep_to_coords('54280494'), cep_to_coords('54130200'), cep_to_coords('53635615'), cep_to_coords('52171287'), cep_to_coords('51240720'), cep_to_coords('51275570'), cep_to_coords('54762338'), cep_to_coords('54230910'), cep_to_coords('50450110'), cep_to_coords('52221021'), cep_to_coords('50740545'), cep_to_coords('50960210'), cep_to_coords('50740121'), cep_to_coords('55365970'), cep_to_coords('56365970'), cep_to_coords('50740025'), cep_to_coords('50340045'), cep_to_coords('55016220'), cep_to_coords('54360127'), cep_to_coords('54333021'), cep_to_coords('55630972'), cep_to_coords('52125100'), cep_to_coords('53220192'), cep_to_coords('55016395'), cep_to_coords('53530222'), cep_to_coords('54321200'), cep_to_coords('53423400'), cep_to_coords('51330215'), cep_to_coords('23032021'), cep_to_coords('56318500'), cep_to_coords('50790592'), cep_to_coords('53210575'), cep_to_coords('54160281'), cep_to_coords('50920119'), cep_to_coords('53405390'), cep_to_coords('53416040'), cep_to_coords('54170015'), cep_to_coords('54786270'), cep_to_coords('54315025'), cep_to_coords('12569896'), cep_to_coords('12588888'), cep_to_coords('26568988'), cep_to_coords('15464646'), cep_to_coords('54330271'), cep_to_coords('12625648'), cep_to_coords('53100600'), cep_to_coords('54774775'), cep_to_coords('55644320'), cep_to_coords('51030062'), cep_to_coords('55666000'), cep_to_coords('50750270'), cep_to_coords('50875201'), cep_to_coords('51011271'), cep_to_coords('53439680'), cep_to_coords('53425630'), cep_to_coords('50671340'), cep_to_coords('54320540'), cep_to_coords('52180281'), cep_to_coords('50731111'), cep_to_coords('54520330'), cep_to_coords('55293150'), cep_to_coords('55152300'), cep_to_coords('55238390'), cep_to_coords('51250500'), cep_to_coords('54320470'), cep_to_coords('54783340'), cep_to_coords('52060258'), cep_to_coords('53413060'), cep_to_coords('52031600'), cep_to_coords('22222222'), cep_to_coords('53635177'), cep_to_coords('53413696'), cep_to_coords('55612193'), cep_to_coords('56550970'), cep_to_coords('53407790'), cep_to_coords('50920825'), cep_to_coords('55191456'), cep_to_coords('51300352'), cep_to_coords('54735511'), cep_to_coords('50740101'), cep_to_coords('05912303'), cep_to_coords('53260060'), cep_to_coords('52216070'), cep_to_coords('53625278'), cep_to_coords('53640350'), cep_to_coords('53230300'), cep_to_coords('53580055'), cep_to_coords('55150160'), cep_to_coords('52510055'), cep_to_coords('53520050'), cep_to_coords('50080080'), cep_to_coords('53575163'), cep_to_coords('55018525'), cep_to_coords('53585220'), cep_to_coords('52010110'), cep_to_coords('54315541'), cep_to_coords('53520310'), cep_to_coords('50120200'), cep_to_coords('54279055'), cep_to_coords('51025700'), cep_to_coords('53525604'), cep_to_coords('51600400'), cep_to_coords('53100170'), cep_to_coords('50730003'), cep_to_coords('52090365'), cep_to_coords('53220235'), cep_to_coords('53403325'), cep_to_coords('52060381'), cep_to_coords('52190054'), cep_to_coords('52190045'), cep_to_coords('53139160'), cep_to_coords('55020240'), cep_to_coords('53000960'), cep_to_coords('50080210'), cep_to_coords('54580422'), cep_to_coords('52031215'), cep_to_coords('25698748'), cep_to_coords('53427240'), cep_to_coords('55153180'), cep_to_coords('52090035'), cep_to_coords('52280601'), cep_to_coords('50920010'), cep_to_coords('50750300'), cep_to_coords('54000400'), cep_to_coords('53610425'), cep_to_coords('54120085'), cep_to_coords('55813400'), cep_to_coords('55818420'), cep_to_coords('52290120'), cep_to_coords('53120320'), cep_to_coords('50791252'), cep_to_coords('55292475'), cep_to_coords('50923192'), cep_to_coords('51275550'), cep_to_coords('54705412'), cep_to_coords('54260441'), cep_to_coords('55027390'), cep_to_coords('50913202'), cep_to_coords('55036475'), cep_to_coords('54325612'), cep_to_coords('51150080'), cep_to_coords('50050791'), cep_to_coords('52131638'), cep_to_coords('54353811'), cep_to_coords('53525195'), cep_to_coords('54368100'), cep_to_coords('54275170'), cep_to_coords('54080090'), cep_to_coords('50791440'), cep_to_coords('52131390'), cep_to_coords('53413155'), cep_to_coords('52230280'), cep_to_coords('54774438'), cep_to_coords('54325008'), cep_to_coords('54494335'), cep_to_coords('52190211'), cep_to_coords('56312320'), cep_to_coords('50080360'), cep_to_coords('53080650'), cep_to_coords('50260250'), cep_to_coords('50960615'), cep_to_coords('56331130'), cep_to_coords('56510410'), cep_to_coords('54352105'), cep_to_coords('52060550'), cep_to_coords('32041030'), cep_to_coords('54315230'), cep_to_coords('56909700'), cep_to_coords('50630405'), cep_to_coords('54705115'), cep_to_coords('56320811'), cep_to_coords('56331310'), cep_to_coords('56318835'), cep_to_coords('56314510'), cep_to_coords('56323650'), cep_to_coords('56322050'), cep_to_coords('56313675'), cep_to_coords('54240710'), cep_to_coords('52606900'), cep_to_coords('55257500'), cep_to_coords('53405713'), cep_to_coords('55190040'), cep_to_coords('54330232'), cep_to_coords('50320310'), cep_to_coords('53640065'), cep_to_coords('55610180'), cep_to_coords('55818025'), cep_to_coords('50780450'), cep_to_coords('53625607'), cep_to_coords('50650330'), cep_to_coords('50731505'), cep_to_coords('53423770'), cep_to_coords('54350755'), cep_to_coords('56310795'), cep_to_coords('50480400'), cep_to_coords('53510280'), cep_to_coords('50430460'), cep_to_coords('50110240'), cep_to_coords('52080052'), cep_to_coords('53690170'), cep_to_coords('51335190'), cep_to_coords('52081215'), cep_to_coords('51260760'), cep_to_coords('53402427'), cep_to_coords('55152360'), cep_to_coords('51340075'), cep_to_coords('51020820'), cep_to_coords('40510140'), cep_to_coords('53404100'), cep_to_coords('54580731'), cep_to_coords('50750450'), cep_to_coords('52081391'), cep_to_coords('52525225'), cep_to_coords('12568888'), cep_to_coords('54250150'), cep_to_coords('54759368'), cep_to_coords('54750080'), cep_to_coords('54505070'), cep_to_coords('55156250'), cep_to_coords('55925000'), cep_to_coords('53620728'), cep_to_coords('55298490'), cep_to_coords('53130100'), cep_to_coords('56909020'), cep_to_coords('55295640'), cep_to_coords('54771794'), cep_to_coords('54762090'), cep_to_coords('54520992'), cep_to_coords('54400040'), cep_to_coords('56312150'), cep_to_coords('52191290'), cep_to_coords('52130024'), cep_to_coords('54270600'), cep_to_coords('52082097'), cep_to_coords('54240110'), cep_to_coords('51270670'), cep_to_coords('55192410'), cep_to_coords('52070242'), cep_to_coords('51350151'), cep_to_coords('51330176'), cep_to_coords('51027370'), cep_to_coords('50800170'), cep_to_coords('53437530'), cep_to_coords('50781510'), cep_to_coords('54520570'), cep_to_coords('53408770'), cep_to_coords('54280293'), cep_to_coords('53580621'), cep_to_coords('54515020'), cep_to_coords('53290335'), cep_to_coords('52090377'), cep_to_coords('35698888'), cep_to_coords('12568889'), cep_to_coords('52051790'), cep_to_coords('31314654'), cep_to_coords('54452063'), cep_to_coords('54730610'), cep_to_coords('50904000'), cep_to_coords('53565550'), cep_to_coords('54330037'), cep_to_coords('53250060'), cep_to_coords('68168934'), cep_to_coords('50300210'), cep_to_coords('55291390'), cep_to_coords('56625110'), cep_to_coords('51150530'), cep_to_coords('55294802'), cep_to_coords('54330980'), cep_to_coords('54440150'), cep_to_coords('50771110'), cep_to_coords('53160530'), cep_to_coords('50800105'), cep_to_coords('50770740'), cep_to_coords('53944490'), cep_to_coords('51300290'), cep_to_coords('55191585'), cep_to_coords('36349577'), cep_to_coords('55153140'), cep_to_coords('52125025'), cep_to_coords('54325105'), cep_to_coords('54517415'), cep_to_coords('53200290'), cep_to_coords('55815260'), cep_to_coords('56502296'), cep_to_coords('55813000'), cep_to_coords('53429160'), cep_to_coords('50920320'), cep_to_coords('50761579'), cep_to_coords('54460080'), cep_to_coords('53530080'), cep_to_coords('55604450'), cep_to_coords('54353250'), cep_to_coords('55152390'), cep_to_coords('50690560'), cep_to_coords('50930192'), cep_to_coords('50603060'), cep_to_coords('52390560'), cep_to_coords('54260520'), cep_to_coords('56519170'), cep_to_coords('51280280'), cep_to_coords('56515045'), cep_to_coords('53402160'), cep_to_coords('50640380'), cep_to_coords('51345420'), cep_to_coords('53085000'), cep_to_coords('50010160'), cep_to_coords('55154090'), cep_to_coords('51110050'), cep_to_coords('55019020'), cep_to_coords('55008041'), cep_to_coords('53409460'), cep_to_coords('55030210'), cep_to_coords('53422230'), cep_to_coords('54786570'), cep_to_coords('51400080'), cep_to_coords('53160312'), cep_to_coords('54786150'), cep_to_coords('53350474'), cep_to_coords('50615550'), cep_to_coords('50100520'), cep_to_coords('51704500'), cep_to_coords('52190115'), cep_to_coords('56508440'), cep_to_coords('54280740'), cep_to_coords('54240301'), cep_to_coords('53231400'), cep_to_coords('56314400'), cep_to_coords('43625115'), cep_to_coords('52090650'), cep_to_coords('51350191'), cep_to_coords('53160590'), cep_to_coords('53625410'), cep_to_coords('54310561'), cep_to_coords('25699874'), cep_to_coords('23659899'), cep_to_coords('52219125'), cep_to_coords('53025020'), cep_to_coords('555000000'), cep_to_coords('55645106'), cep_to_coords('51180061'), cep_to_coords('54410185'), cep_to_coords('56903200'), cep_to_coords('54705213'), cep_to_coords('53190380'), cep_to_coords('58329000'), cep_to_coords('55707000'), cep_to_coords('55298010'), cep_to_coords('55292600'), cep_to_coords('53999000'), cep_to_coords('58040090'), cep_to_coords('52090014'), cep_to_coords('54730960'), cep_to_coords('12/04/1971'), cep_to_coords('55818490'), cep_to_coords('55158160'), cep_to_coords('53417540'), cep_to_coords('52280221'), cep_to_coords('50941209'), cep_to_coords('54230670'), cep_to_coords('50771130'), cep_to_coords('52090081'), cep_to_coords('54365260'), cep_to_coords('56503216'), cep_to_coords('54280754'), cep_to_coords('53610161'), cep_to_coords('54325710'), cep_to_coords('50750210'), cep_to_coords('54535340'), cep_to_coords('53270190'), cep_to_coords('50875016'), cep_to_coords('50923190'), cep_to_coords('55292450'), cep_to_coords('53080640'), cep_to_coords('53070625'), cep_to_coords('52280555'), cep_to_coords('50070525'), cep_to_coords('51351000'), cep_to_coords('54352290'), cep_to_coords('51030520'), cep_to_coords('53611000'), cep_to_coords('53610300'), cep_to_coords('51345290'), cep_to_coords('54320180'), cep_to_coords('53610296'), cep_to_coords('51290232'), cep_to_coords('52090287'), cep_to_coords('53290222'), cep_to_coords('52091280'), cep_to_coords('53634205'), cep_to_coords('54120273'), cep_to_coords('53635260'), cep_to_coords('53630135'), cep_to_coords('53520155'), cep_to_coords('54280102'), cep_to_coords('53610370'), cep_to_coords('55290470'), cep_to_coords('53090440'), cep_to_coords('55297620'), cep_to_coords('56312268'), cep_to_coords('56909514'), cep_to_coords('56909090'), cep_to_coords('56909480'), cep_to_coords('56904250'), cep_to_coords('55644340'), cep_to_coords('56909661'), cep_to_coords('51317476'), cep_to_coords('53402500'), cep_to_coords('51245390'), cep_to_coords('51160454'), cep_to_coords('53080740'), cep_to_coords('50650665'), cep_to_coords('54380000'), cep_to_coords('50860290'), cep_to_coords('50110553'), cep_to_coords('54310103'), cep_to_coords('50711031'), cep_to_coords('55641822'), cep_to_coords('50791409'), cep_to_coords('54315460'), cep_to_coords('50362123'), cep_to_coords('53110032'), cep_to_coords('50680670'), cep_to_coords('52160555'), cep_to_coords('50771220'), cep_to_coords('56501055'), cep_to_coords('54786400'), cep_to_coords('55016280'), cep_to_coords('55154100'), cep_to_coords('55818510'), cep_to_coords('55815021'), cep_to_coords('51335335'), cep_to_coords('53570136'), cep_to_coords('54325615'), cep_to_coords('55000403'), cep_to_coords('53320375'), cep_to_coords('54325026'), cep_to_coords('55816300'), cep_to_coords('53350750'), cep_to_coords('53403065'), cep_to_coords('54530108'), cep_to_coords('54737210'), cep_to_coords('54400295'), cep_to_coords('54430261'), cep_to_coords('24715710'), cep_to_coords('54788100'), cep_to_coords('53350825'), cep_to_coords('54401140'), cep_to_coords('55298637'), cep_to_coords('55298025'), cep_to_coords('55291190'), cep_to_coords('56306260'), cep_to_coords('55642740'), cep_to_coords('50751538'), cep_to_coords('53422140'), cep_to_coords('52120270'), cep_to_coords('50912319'), cep_to_coords('50771740'), cep_to_coords('53250030'), cep_to_coords('53110442'), cep_to_coords('50000700'), cep_to_coords('55012481'), cep_to_coords('51110490'), cep_to_coords('53520508'), cep_to_coords('51101130'), cep_to_coords('51345760'), cep_to_coords('51190735'), cep_to_coords('53530625'), cep_to_coords('53530615'), cep_to_coords('55012500'), cep_to_coords('54580827'), cep_to_coords('53604447'), cep_to_coords('50780430'), cep_to_coords('56517670'), cep_to_coords('54789815'), cep_to_coords('54325381'), cep_to_coords('61000000'), cep_to_coords('54715501'), cep_to_coords('50070240'), cep_to_coords('54525480'), cep_to_coords('54220170'), cep_to_coords('54330090'), cep_to_coords('55014720'), cep_to_coords('54517050'), cep_to_coords('54360026'), cep_to_coords('55556000'), cep_to_coords('52211031'), cep_to_coords('50770066'), cep_to_coords('50730710'), cep_to_coords('52150012'), cep_to_coords('55158790'), cep_to_coords('55295587'), cep_to_coords('51330225'), cep_to_coords('54768420'), cep_to_coords('55810300'), cep_to_coords('54505200'), cep_to_coords('54210509'), cep_to_coords('51150258'), cep_to_coords('53270285'), cep_to_coords('54774425'), cep_to_coords('25290570'), cep_to_coords('54450620'), cep_to_coords('50870310'), cep_to_coords('53640150'), cep_to_coords('53403750'), cep_to_coords('55292370'), cep_to_coords('48000000'), cep_to_coords('55295122'), cep_to_coords('55015160'), cep_to_coords('52390104'), cep_to_coords('54325626'), cep_to_coords('55018051'), cep_to_coords('50010913'), cep_to_coords('55012650'), cep_to_coords('54260510'), cep_to_coords('59330000'), cep_to_coords('66098980'), cep_to_coords('52080420'), cep_to_coords('56503532'), cep_to_coords('52656564'), cep_to_coords('50650321'), cep_to_coords('54266136'), cep_to_coords('53423410'), cep_to_coords('50940912'), cep_to_coords('54580255'), cep_to_coords('54340322'), cep_to_coords('54100438'), cep_to_coords('53260041'), cep_to_coords('11236588'), cep_to_coords('55610203'), cep_to_coords('55002052'), cep_to_coords('53405070'), cep_to_coords('54580416'), cep_to_coords('53560060'), cep_to_coords('55094110'), cep_to_coords('11231592'), cep_to_coords('52400000'), cep_to_coords('50640010'), cep_to_coords('53610234'), cep_to_coords('50170120'), cep_to_coords('55292240'), cep_to_coords('61209805'), cep_to_coords('55014410'), cep_to_coords('56323620'), cep_to_coords('56320830'), cep_to_coords('56331160'), cep_to_coords('56309200'), cep_to_coords('55819350'), cep_to_coords('55034120'), cep_to_coords('53545840'), cep_to_coords('55154690'), cep_to_coords('14320304'), cep_to_coords('54756275'), cep_to_coords('53401760'), cep_to_coords('68565240'), cep_to_coords('51250550'), cep_to_coords('55443500'), cep_to_coords('53000522'), cep_to_coords('53650781'), cep_to_coords('05081994'), cep_to_coords('50680550'), cep_to_coords('51180530'), cep_to_coords('55020525'), cep_to_coords('54505450'), cep_to_coords('54501000'), cep_to_coords('54330550'), cep_to_coords('51370041'), cep_to_coords('54440220'), cep_to_coords('53421041'), cep_to_coords('54325445'), cep_to_coords('51250540'), cep_to_coords('54220332'), cep_to_coords('54777043'), cep_to_coords('54280686'), cep_to_coords('53250700'), cep_to_coords('53427655'), cep_to_coords('53200360'), cep_to_coords('53640336'), cep_to_coords('55608000'), cep_to_coords('55040030'), cep_to_coords('51260160'), cep_to_coords('53413345'), cep_to_coords('55606830'), cep_to_coords('54230095'), cep_to_coords('54753345'), cep_to_coords('53407320'), cep_to_coords('54789370'), cep_to_coords('51030264'), cep_to_coords('55617470'), cep_to_coords('55818455'), cep_to_coords('54140300'), cep_to_coords('54352070'), cep_to_coords('53370266'), cep_to_coords('55292200'), cep_to_coords('55299820'), cep_to_coords('53010240'), cep_to_coords('50087222'), cep_to_coords('52071410'), cep_to_coords('52090825'), cep_to_coords('52060904'), cep_to_coords('51346040'), cep_to_coords('52091366'), cep_to_coords('53530498'), cep_to_coords('52636589'), cep_to_coords('53200240'), cep_to_coords('54170802'), cep_to_coords('52191292'), cep_to_coords('55157595'), cep_to_coords('55020450'), cep_to_coords('55155460'), cep_to_coords('51570480'), cep_to_coords('53246700'), cep_to_coords('51300030'), cep_to_coords('54510655'), cep_to_coords('56509812'), cep_to_coords('51335005'), cep_to_coords('52061600'), cep_to_coords('54160005'), cep_to_coords('50940400'), cep_to_coords('54170663'), cep_to_coords('55614170'), cep_to_coords('56960120'), cep_to_coords('55644462'), cep_to_coords('51420000'), cep_to_coords('55290330'), cep_to_coords('95020002'), cep_to_coords('56511210'), cep_to_coords('54777315'), cep_to_coords('51340350'), cep_to_coords('50932109'), cep_to_coords('52011800'), cep_to_coords('55195842'), cep_to_coords('50900395'), cep_to_coords('54420015'), cep_to_coords('52580755'), cep_to_coords('50239190'), cep_to_coords('50000440'), cep_to_coords('53585030'), cep_to_coords('53422510'), cep_to_coords('50731112'), cep_to_coords('53413525'), cep_to_coords('51176024'), cep_to_coords('52390160'), cep_to_coords('52280558'), cep_to_coords('54580284'), cep_to_coords('53439801'), cep_to_coords('52091159'), cep_to_coords('50711145'), cep_to_coords('51130070'), cep_to_coords('05212001'), cep_to_coords('55152070'), cep_to_coords('52010080'), cep_to_coords('55608200'), cep_to_coords('53421211'), cep_to_coords('57400030'), cep_to_coords('54240303'), cep_to_coords('52654616'), cep_to_coords('54330585'), cep_to_coords('55608770'), cep_to_coords('51180490'), cep_to_coords('53580670'), cep_to_coords('53417770'), cep_to_coords('53415290'), cep_to_coords('51035800'), cep_to_coords('51021007'), cep_to_coords('77777777'), cep_to_coords('52291066'), cep_to_coords('51160150'), cep_to_coords('54733200'), cep_to_coords('54160490'), cep_to_coords('50931029'), cep_to_coords('54783715'), cep_to_coords('51010260'), cep_to_coords('54420505'), cep_to_coords('54240340'), cep_to_coords('51220180'), cep_to_coords('56503160'), cep_to_coords('54762365'), cep_to_coords('54150350'), cep_to_coords('52080273'), cep_to_coords('50760005'), cep_to_coords('55038725'), cep_to_coords('53220815'), cep_to_coords('50330170'), cep_to_coords('50510520'), cep_to_coords('53560014'), cep_to_coords('52160229'), cep_to_coords('53510170'), cep_to_coords('53200505'), cep_to_coords('53565520'), cep_to_coords('50491209'), cep_to_coords('53402590'), cep_to_coords('51180460'), cep_to_coords('55020580'), cep_to_coords('54780000'), cep_to_coords('56143000'), cep_to_coords('55006330'), cep_to_coords('53429140'), cep_to_coords('54230402'), cep_to_coords('25265615'), cep_to_coords('55292235'), cep_to_coords('50640102'), cep_to_coords('43111111'), cep_to_coords('54350170'), cep_to_coords('53409770'), cep_to_coords('53170072'), cep_to_coords('53605550'), cep_to_coords('55642500'), cep_to_coords('53565410'), cep_to_coords('51150510'), cep_to_coords('54517716'), cep_to_coords('52140521'), cep_to_coords('50060145'), cep_to_coords('50131420'), cep_to_coords('53210100'), cep_to_coords('55032422'), cep_to_coords('53417500'), cep_to_coords('53421261'), cep_to_coords('54517205'), cep_to_coords('54333070'), cep_to_coords('55608195'), cep_to_coords('50931209'), cep_to_coords('50860242'), cep_to_coords('50610210'), cep_to_coords('51290240'), cep_to_coords('52291011'), cep_to_coords('53405570'), cep_to_coords('52081780'), cep_to_coords('56503512'), cep_to_coords('55150630'), cep_to_coords('55006111'), cep_to_coords('52140530'), cep_to_coords('51160130'), cep_to_coords('55008285'), cep_to_coords('54345705'), cep_to_coords('52040410'), cep_to_coords('54435610'), cep_to_coords('53930050'), cep_to_coords('50010370'), cep_to_coords('55008231'), cep_to_coords('51120244'), cep_to_coords('51330275'), cep_to_coords('50740201'), cep_to_coords('54360167'), cep_to_coords('50470210'), cep_to_coords('51220170'), cep_to_coords('53635174'), cep_to_coords('53630190'), cep_to_coords('53320170'), cep_to_coords('54290335'), cep_to_coords('25656646'), cep_to_coords('56302390'), cep_to_coords('53600600'), cep_to_coords('50970630'), cep_to_coords('54082060'), cep_to_coords('53060220'), cep_to_coords('54531200'), cep_to_coords('50941203'), cep_to_coords('55158815'), cep_to_coords('55296038'), cep_to_coords('50390123'), cep_to_coords('53402635'), cep_to_coords('55190058'), cep_to_coords('50110845'), cep_to_coords('52091211'), cep_to_coords('25698988'), cep_to_coords('54320400'), cep_to_coords('50183022'), cep_to_coords('54460221'), cep_to_coords('55157030'), cep_to_coords('54323080'), cep_to_coords('54320022'), cep_to_coords('54767375'), cep_to_coords('53120180'), cep_to_coords('52080115'), cep_to_coords('54705450'), cep_to_coords('51240715'), cep_to_coords('53421150'), cep_to_coords('54420530'), cep_to_coords('53120931'), cep_to_coords('74959198'), cep_to_coords('54705093'), cep_to_coords('56566655'), cep_to_coords('54287037'), cep_to_coords('54330217'), cep_to_coords('50780625'), cep_to_coords('55019085'), cep_to_coords('56454648'), cep_to_coords('53423790'), cep_to_coords('54756506'), cep_to_coords('51270675'), cep_to_coords('55818454'), cep_to_coords('54771130'), cep_to_coords('53650025'), cep_to_coords('50730655'), cep_to_coords('57150000'), cep_to_coords('51260421'), cep_to_coords('52110232'), cep_to_coords('56320791'), cep_to_coords('55214555'), cep_to_coords('53431430'), cep_to_coords('54786505'), cep_to_coords('70864669'), cep_to_coords('53170335'), cep_to_coords('53205050'), cep_to_coords('54250231'), cep_to_coords('53645040'), cep_to_coords('56310700'), cep_to_coords('70859846'), cep_to_coords('54752000'), cep_to_coords('53640160'), cep_to_coords('55015030'), cep_to_coords('52230430'), cep_to_coords('25665664'), cep_to_coords('52070504'), cep_to_coords('54310421'), cep_to_coords('50920049'), cep_to_coords('54768730'), cep_to_coords('50710148'), cep_to_coords('50700600'), cep_to_coords('50791190'), cep_to_coords('50660178'), cep_to_coords('52100330'), cep_to_coords('54761165'), cep_to_coords('52020005'), cep_to_coords('54325100'), cep_to_coords('52070444'), cep_to_coords('54160530'), cep_to_coords('54460380'), cep_to_coords('29152877'), cep_to_coords('53635160'), cep_to_coords('53670970'), cep_to_coords('20970100'), cep_to_coords('54090560'), cep_to_coords('53620550'), cep_to_coords('54090026'), cep_to_coords('56320087'), cep_to_coords('54352295'), cep_to_coords('56509625'), cep_to_coords('50942190'), cep_to_coords('50761335'), cep_to_coords('50625816'), cep_to_coords('53437590'), cep_to_coords('54580418'), cep_to_coords('25441215'), cep_to_coords('54589165'), cep_to_coords('55769000'), cep_to_coords('53525525'), cep_to_coords('22825000'), cep_to_coords('50080030'), cep_to_coords('51330171'), cep_to_coords('54320300'), cep_to_coords('50731120'), cep_to_coords('53670080'), cep_to_coords('23262135'), cep_to_coords('53402167'), cep_to_coords('55041400'), cep_to_coords('53280052'), cep_to_coords('55461390'), cep_to_coords('53580080'), cep_to_coords('54420500'), cep_to_coords('53421470'), cep_to_coords('54490500'), cep_to_coords('53423530'), cep_to_coords('53405301'), cep_to_coords('51245555'), cep_to_coords('56308120'), cep_to_coords('56316786'), cep_to_coords('50791469'), cep_to_coords('51011141'), cep_to_coords('50940640'), cep_to_coords('52070463'), cep_to_coords('54595090'), cep_to_coords('54762120'), cep_to_coords('55004000'), cep_to_coords('54517110'), cep_to_coords('53650315'), cep_to_coords('50912312'), cep_to_coords('50671400'), cep_to_coords('50080530'), cep_to_coords('54315665'), cep_to_coords('54100455'), cep_to_coords('52171288'), cep_to_coords('21130180'), cep_to_coords('54730016'), cep_to_coords('56512280'), cep_to_coords('55037085'), cep_to_coords('54700100'), cep_to_coords('54733050'), cep_to_coords('50910102'), cep_to_coords('50129321'), cep_to_coords('51335100'), cep_to_coords('54900070'), cep_to_coords('55817010'), cep_to_coords('52090625'), cep_to_coords('51305340'), cep_to_coords('55291659'), cep_to_coords('51022222'), cep_to_coords('53435704'), cep_to_coords('51220280'), cep_to_coords('56656645'), cep_to_coords('54530190'), cep_to_coords('54325281'), cep_to_coords('55299444'), cep_to_coords('54720013'), cep_to_coords('54730720'), cep_to_coords('50740700'), cep_to_coords('50060904'), cep_to_coords('54580496'), cep_to_coords('51021454'), cep_to_coords('51335500'), cep_to_coords('50412930'), cep_to_coords('54220265'), cep_to_coords('53160175'), cep_to_coords('54215390'), cep_to_coords('45500000'), cep_to_coords('54539190'), cep_to_coords('50690616'), cep_to_coords('50329190'), cep_to_coords('54767330'), cep_to_coords('54460395'), cep_to_coords('51130920'), cep_to_coords('54320151'), cep_to_coords('53510332'), cep_to_coords('52081034'), cep_to_coords('55435090'), cep_to_coords('55642485'), cep_to_coords('29217209'), cep_to_coords('54733310'), cep_to_coords('50920662'), cep_to_coords('50110647'), cep_to_coords('51310190'), cep_to_coords('54535370'), cep_to_coords('52135020'), cep_to_coords('50640112'), cep_to_coords('54580823'), cep_to_coords('52042380'), cep_to_coords('50912320'), cep_to_coords('580000000'), cep_to_coords('50009059'), cep_to_coords('53422320'), cep_to_coords('50110485'), cep_to_coords('53230160'), cep_to_coords('52040200'), cep_to_coords('55197090'), cep_to_coords('55611490'), cep_to_coords('52090715'), cep_to_coords('53403140'), cep_to_coords('54140020'), cep_to_coords('51310545'), cep_to_coords('52071115'), cep_to_coords('52130275'), cep_to_coords('52110420'), cep_to_coords('54000120'), cep_to_coords('58800000'), cep_to_coords('55155430'), cep_to_coords('54315350'), cep_to_coords('50904185'), cep_to_coords('54680285'), cep_to_coords('54440200'), cep_to_coords('54160090'), cep_to_coords('54756091'), cep_to_coords('54777508'), cep_to_coords('54325192'), cep_to_coords('53402170'), cep_to_coords('55151685'), cep_to_coords('54375192'), cep_to_coords('83569944'), cep_to_coords('52090005'), cep_to_coords('12574896'), cep_to_coords('53620736'), cep_to_coords('51030754'), cep_to_coords('50780680'), cep_to_coords('50830310'), cep_to_coords('54440535'), cep_to_coords('55155721'), cep_to_coords('53402120'), cep_to_coords('54160040'), cep_to_coords('53421151'), cep_to_coords('54353160'), cep_to_coords('53050830'), cep_to_coords('53370480'), cep_to_coords('45421000'), cep_to_coords('57767321'), cep_to_coords('55295140'), cep_to_coords('51245552'), cep_to_coords('50761230'), cep_to_coords('51061460'), cep_to_coords('53620852'), cep_to_coords('50570510'), cep_to_coords('53060415'), cep_to_coords('54100444'), cep_to_coords('52240560'), cep_to_coords('55294839'), cep_to_coords('53070630'), cep_to_coords('50790427'), cep_to_coords('43700025'), cep_to_coords('50650014'), cep_to_coords('50391203'), cep_to_coords('50960180'), cep_to_coords('54444010'), cep_to_coords('53370310'), cep_to_coords('54210510'), cep_to_coords('54333460'), cep_to_coords('54370060'), cep_to_coords('54325144'), cep_to_coords('21110250'), cep_to_coords('53418170'), cep_to_coords('50921093'), cep_to_coords('54280055'), cep_to_coords('52240020'), cep_to_coords('54523090'), cep_to_coords('55815090'), cep_to_coords('54735305'), cep_to_coords('52291413'), cep_to_coords('64979610'), cep_to_coords('54500994'), cep_to_coords('51300200'), cep_to_coords('56912355'), cep_to_coords('52074800'), cep_to_coords('55295630'), cep_to_coords('56317388'), cep_to_coords('55556500'), cep_to_coords('52051155'), cep_to_coords('55294786'), cep_to_coords('55608282'), cep_to_coords('56346000'), cep_to_coords('55294720'), cep_to_coords('54390027'), cep_to_coords('54275020'), cep_to_coords('54325740'), cep_to_coords('50620010'), cep_to_coords('63630000'), cep_to_coords('51300022'), cep_to_coords('53443040'), cep_to_coords('55018230'), cep_to_coords('55030360'), cep_to_coords('53515515'), cep_to_coords('54365170'), cep_to_coords('50680700'), cep_to_coords('53254070'), cep_to_coords('50650210'), cep_to_coords('52131271'), cep_to_coords('55134690'), cep_to_coords('51014555'), cep_to_coords('50710014'), cep_to_coords('50920240'), cep_to_coords('54230190'), cep_to_coords('53407180'), cep_to_coords('50030906'), cep_to_coords('52091105'), cep_to_coords('54740320'), cep_to_coords('54280111'), cep_to_coords('54540550'), cep_to_coords('51300180'), cep_to_coords('54270255'), cep_to_coords('53427570'), cep_to_coords('54352100'), cep_to_coords('53423310'), cep_to_coords('51170180'), cep_to_coords('54735520'), cep_to_coords('55190004'), cep_to_coords('56316748'), cep_to_coords('54325081'), cep_to_coords('56326330'), cep_to_coords('52110471'), cep_to_coords('50923019'), cep_to_coords('55715970'), cep_to_coords('51320442'), cep_to_coords('54325071'), cep_to_coords('54360175'), cep_to_coords('53550095'), cep_to_coords('52070573'), cep_to_coords('50392109'), cep_to_coords('54210456'), cep_to_coords('54170710'), cep_to_coords('50751455'), cep_to_coords('51021011'), cep_to_coords('51270541'), cep_to_coords('51170041'), cep_to_coords('54100023'), cep_to_coords('54520705'), cep_to_coords('52150130'), cep_to_coords('51230231'), cep_to_coords('22655656'), cep_to_coords('26566645'), cep_to_coords('53431650'), cep_to_coords('52564444'), cep_to_coords('65664645'), cep_to_coords('52111110'), cep_to_coords('55291729'), cep_to_coords('50650190'), cep_to_coords('54715410'), cep_to_coords('55169000'), cep_to_coords('54705215'), cep_to_coords('50011050'), cep_to_coords('53615045'), cep_to_coords('51320531'), cep_to_coords('55604042'), cep_to_coords('50330210'), cep_to_coords('25090260'), cep_to_coords('50670392'), cep_to_coords('55018460'), cep_to_coords('54260040'), cep_to_coords('52070920'), cep_to_coords('53130730'), cep_to_coords('52150330'), cep_to_coords('52150090'), cep_to_coords('52120750'), cep_to_coords('52280850'), cep_to_coords('53600615'), cep_to_coords('51220035'), cep_to_coords('53420060'), cep_to_coords('53530412'), cep_to_coords('50130180'), cep_to_coords('52190225'), cep_to_coords('56503144'), cep_to_coords('56323460'), cep_to_coords('23140130'), cep_to_coords('54705320'), cep_to_coords('54430455'), cep_to_coords('51190170'), cep_to_coords('54410030'), cep_to_coords('53530424'), cep_to_coords('54160460'), cep_to_coords('53405261'), cep_to_coords('54715650'), cep_to_coords('52150169'), cep_to_coords('53651200'), cep_to_coords('54490504'), cep_to_coords('54490260'), cep_to_coords('50791450'), cep_to_coords('56515260'), cep_to_coords('54090630'), cep_to_coords('53635675'), cep_to_coords('52041510'), cep_to_coords('52121425'), cep_to_coords('56503850'), cep_to_coords('53401735'), cep_to_coords('51570370'), cep_to_coords('53580312'), cep_to_coords('54445000'), cep_to_coords('54442010'), cep_to_coords('53497000'), cep_to_coords('54330165'), cep_to_coords('50980663'), cep_to_coords('53140195'), cep_to_coords('50110292'), cep_to_coords('52160690'), cep_to_coords('54245170'), cep_to_coords('55194417'), cep_to_coords('54330417'), cep_to_coords('50940185'), cep_to_coords('54090261'), cep_to_coords('52175170'), cep_to_coords('53437580'), cep_to_coords('52080355'), cep_to_coords('54080493'), cep_to_coords('51150372'), cep_to_coords('50970114'), cep_to_coords('53421400'), cep_to_coords('52212534'), cep_to_coords('55298141'), cep_to_coords('50344165'), cep_to_coords('50620200'), cep_to_coords('55038425'), cep_to_coords('23157887'), cep_to_coords('52720585'), cep_to_coords('56940000'), cep_to_coords('56310550'), cep_to_coords('55608592'), cep_to_coords('55429000'), cep_to_coords('56585879'), cep_to_coords('56309770'), cep_to_coords('55144000'), cep_to_coords('53625747'), cep_to_coords('53460407'), cep_to_coords('55295433'), cep_to_coords('56000840'), cep_to_coords('54170001'), cep_to_coords('55026140'), cep_to_coords('54715070'), cep_to_coords('53405625'), cep_to_coords('54360165'), cep_to_coords('50222310'), cep_to_coords('53180180'), cep_to_coords('55265970'), cep_to_coords('50680601'), cep_to_coords('51030675'), cep_to_coords('54210595'), cep_to_coords('53570001'), cep_to_coords('54850080'), cep_to_coords('53545820'), cep_to_coords('53510730'), cep_to_coords('50920331'), cep_to_coords('54519040'), cep_to_coords('53170011'), cep_to_coords('50203191'), cep_to_coords('54400550'), cep_to_coords('55156485'), cep_to_coords('55813120'), cep_to_coords('51240675'), cep_to_coords('50930025'), cep_to_coords('50750150'), cep_to_coords('53413401'), cep_to_coords('50030350'), cep_to_coords('53370501'), cep_to_coords('52569874'), cep_to_coords('55036060'), cep_to_coords('50780685'), cep_to_coords('53630615'), cep_to_coords('53640293'), cep_to_coords('53620107'), cep_to_coords('56512305'), cep_to_coords('54490002'), cep_to_coords('52110535'), cep_to_coords('54470281'), cep_to_coords('53315630'), cep_to_coords('54762680'), cep_to_coords('55299382'), cep_to_coords('50565026'), cep_to_coords('50781650'), cep_to_coords('54325292'), cep_to_coords('54440049'), cep_to_coords('54987887'), cep_to_coords('53560790'), cep_to_coords('50111430'), cep_to_coords('33120241'), cep_to_coords('54505235'), cep_to_coords('51120040'), cep_to_coords('55019005'), cep_to_coords('52203375'), cep_to_coords('52191281'), cep_to_coords('56512001'), cep_to_coords('54505316'), cep_to_coords('55655970'), cep_to_coords('51180031'), cep_to_coords('48904501'), cep_to_coords('53320210'), cep_to_coords('53413630'), cep_to_coords('51210145'), cep_to_coords('55428057'), cep_to_coords('53442020'), cep_to_coords('65063640'), cep_to_coords('55018540'), cep_to_coords('65465646'), cep_to_coords('55814660'), cep_to_coords('56156446'), cep_to_coords('53433590'), cep_to_coords('65664564'), cep_to_coords('50920122'), cep_to_coords('54129007'), cep_to_coords('53637800'), cep_to_coords('53090060'), cep_to_coords('53600543'), cep_to_coords('55640094'), cep_to_coords('53373303'), cep_to_coords('54248165'), cep_to_coords('52411010'), cep_to_coords('50690510'), cep_to_coords('52001120'), cep_to_coords('53437620'), cep_to_coords('52211047'), cep_to_coords('54100046'), cep_to_coords('51320280'), cep_to_coords('53042762'), cep_to_coords('05123002'), cep_to_coords('55014555'), cep_to_coords('55195800'), cep_to_coords('52020091'), cep_to_coords('53270695'), cep_to_coords('50721575'), cep_to_coords('52636899'), cep_to_coords('53525250'), cep_to_coords('52250220'), cep_to_coords('55297439'), cep_to_coords('54705127'), cep_to_coords('54720625'), cep_to_coords('51365160'), cep_to_coords('54715050'), cep_to_coords('50130760'), cep_to_coords('50761701'), cep_to_coords('53630485'), cep_to_coords('54315195'), cep_to_coords('54535470'), cep_to_coords('52140151'), cep_to_coords('50640250'), cep_to_coords('52140230'), cep_to_coords('50690708'), cep_to_coords('50920695'), cep_to_coords('55550015'), cep_to_coords('50690709'), cep_to_coords('51470166'), cep_to_coords('52160232'), cep_to_coords('50820055'), cep_to_coords('53402123'), cep_to_coords('54360149'), cep_to_coords('50800261'), cep_to_coords('50695450'), cep_to_coords('53409310'), cep_to_coords('55609100'), cep_to_coords('54160250'), cep_to_coords('54340201'), cep_to_coords('53030220'), cep_to_coords('55645220'), cep_to_coords('51761570'), cep_to_coords('55813230'), cep_to_coords('52211055'), cep_to_coords('54086024'), cep_to_coords('53580105'), cep_to_coords('53580455'), cep_to_coords('55030190'), cep_to_coords('54706360'), cep_to_coords('55292080'), cep_to_coords('52091515'), cep_to_coords('54400346'), cep_to_coords('51320090'), cep_to_coords('54517260'), cep_to_coords('55037270'), cep_to_coords('53635185'), cep_to_coords('55360970'), cep_to_coords('55038660'), cep_to_coords('55040100'), cep_to_coords('54580130'), cep_to_coords('54515411'), cep_to_coords('53570570'), cep_to_coords('31651564'), cep_to_coords('52564848'), cep_to_coords('54727190'), cep_to_coords('53625500'), cep_to_coords('54745015'), cep_to_coords('53220211'), cep_to_coords('54490320'), cep_to_coords('54450320'), cep_to_coords('55192521'), cep_to_coords('53411330'), cep_to_coords('56314610'), cep_to_coords('55614716'), cep_to_coords('54535300'), cep_to_coords('56517752'), cep_to_coords('56519130'), cep_to_coords('50660230'), cep_to_coords('51110240'), cep_to_coords('50620695'), cep_to_coords('50110351'), cep_to_coords('52204021'), cep_to_coords('54733120'), cep_to_coords('50669075'), cep_to_coords('55830000'), cep_to_coords('55606660'), cep_to_coords('54360108'), cep_to_coords('51180046'), cep_to_coords('53625294'), cep_to_coords('50920198'), cep_to_coords('54190720'), cep_to_coords('55158190'), cep_to_coords('55608467'), cep_to_coords('52009045'), cep_to_coords('54723065'), cep_to_coords('50380320'), cep_to_coords('54759045'), cep_to_coords('53402845'), cep_to_coords('53320790'), cep_to_coords('14061963'), cep_to_coords('52046120'), cep_to_coords('55816530'), cep_to_coords('32465466'), cep_to_coords('51564623'), cep_to_coords('55036393'), cep_to_coords('50760690'), cep_to_coords('53620804'), cep_to_coords('86625503'), cep_to_coords('53003510'), cep_to_coords('50780628'), cep_to_coords('50921321'), cep_to_coords('52081035'), cep_to_coords('50802220'), cep_to_coords('55816470'), cep_to_coords('54460450'), cep_to_coords('50950030'), cep_to_coords('50760305'), cep_to_coords('50710455'), cep_to_coords('65414666'), cep_to_coords('55034280'), cep_to_coords('54090413'), cep_to_coords('54705150'), cep_to_coords('53429795'), cep_to_coords('53340280'), cep_to_coords('55475000'), cep_to_coords('53535000'), cep_to_coords('56909172'), cep_to_coords('54170790'), cep_to_coords('50620840'), cep_to_coords('54325662'), cep_to_coords('54530430'), cep_to_coords('52210290'), cep_to_coords('52120435'), cep_to_coords('53423160'), cep_to_coords('52110581'), cep_to_coords('52060330'), cep_to_coords('55887000'), cep_to_coords('54582080'), cep_to_coords('50320240'), cep_to_coords('50680061'), cep_to_coords('54320655'), cep_to_coords('55029901'), cep_to_coords('53437846'), cep_to_coords('52031401'), cep_to_coords('54760425'), cep_to_coords('51111270'), cep_to_coords('53690745'), cep_to_coords('56509764'), cep_to_coords('54120240'), cep_to_coords('55811160'), cep_to_coords('54589155'), cep_to_coords('52165075'), cep_to_coords('53449110'), cep_to_coords('54125787'), cep_to_coords('54877888'), cep_to_coords('55195091'), cep_to_coords('53563110'), cep_to_coords('55317000'), cep_to_coords('55019165'), cep_to_coords('55030295'), cep_to_coords('50771805'), cep_to_coords('55295386'), cep_to_coords('05410025'), cep_to_coords('53635180'), cep_to_coords('54715825'), cep_to_coords('54360094'), cep_to_coords('50960600'), cep_to_coords('52103991'), cep_to_coords('52740220'), cep_to_coords('51102117'), cep_to_coords('54580396'), cep_to_coords('50980585'), cep_to_coords('53550141'), cep_to_coords('53419200'), cep_to_coords('52081039'), cep_to_coords('52091163'), cep_to_coords('53550148'), cep_to_coords('55154605'), cep_to_coords('53550125'), cep_to_coords('50790430'), cep_to_coords('55818545'), cep_to_coords('53370280'), cep_to_coords('54580803'), cep_to_coords('56516000'), cep_to_coords('54420012'), cep_to_coords('55034370'), cep_to_coords('50453011'), cep_to_coords('51206070'), cep_to_coords('56506655'), cep_to_coords('53610337'), cep_to_coords('51230290'), cep_to_coords('05305015'), cep_to_coords('50930330'), cep_to_coords('53620687'), cep_to_coords('50110170'), cep_to_coords('55032570'), cep_to_coords('55645714'), cep_to_coords('52333333'), cep_to_coords('55024675'), cep_to_coords('53170420'), cep_to_coords('557900000'), cep_to_coords('53132555'), cep_to_coords('50080220'), cep_to_coords('52659698'), cep_to_coords('55022060'), cep_to_coords('50110505'), cep_to_coords('55034420'), cep_to_coords('55191606'), cep_to_coords('55030207'), cep_to_coords('43441625'), cep_to_coords('05111104'), cep_to_coords('50440370'), cep_to_coords('51240705'), cep_to_coords('54100520'), cep_to_coords('50790428'), cep_to_coords('50980661'), cep_to_coords('54762752'), cep_to_coords('54110359'), cep_to_coords('54350172'), cep_to_coords('52040560'), cep_to_coords('52121021'), cep_to_coords('52191220'), cep_to_coords('54345510'), cep_to_coords('50059120'), cep_to_coords('52280450'), cep_to_coords('54771798'), cep_to_coords('54490110'), cep_to_coords('52020450'), cep_to_coords('52165054'), cep_to_coords('52141075'), cep_to_coords('54290290'), cep_to_coords('53630335'), cep_to_coords('59070100'), cep_to_coords('55608545'), cep_to_coords('55153100'), cep_to_coords('52640320'), cep_to_coords('53530454'), cep_to_coords('50930260'), cep_to_coords('54774780'), cep_to_coords('51695000'), cep_to_coords('53540190'), cep_to_coords('54460620'), cep_to_coords('55614177'), cep_to_coords('55192255'), cep_to_coords('52111545'), cep_to_coords('50721646'), cep_to_coords('50725640'), cep_to_coords('54730630'), cep_to_coords('53610752'), cep_to_coords('50960670'), cep_to_coords('55004320'), cep_to_coords('50890300'), cep_to_coords('55154712'), cep_to_coords('53560710'), cep_to_coords('55290280'), cep_to_coords('55608570'), cep_to_coords('54357555'), cep_to_coords('53320240'), cep_to_coords('56306340'), cep_to_coords('54330742'), cep_to_coords('53530150'), cep_to_coords('55151040'), cep_to_coords('55495440'), cep_to_coords('5450000'), cep_to_coords('53060740'), cep_to_coords('55192587'), cep_to_coords('53402240'), cep_to_coords('53439306'), cep_to_coords('55295570'), cep_to_coords('55705970'), cep_to_coords('54300062'), cep_to_coords('55640245'), cep_to_coords('54210533'), cep_to_coords('53210790'), cep_to_coords('50705372'), cep_to_coords('53433255'), cep_to_coords('53120150'), cep_to_coords('55641494'), cep_to_coords('54756480'), cep_to_coords('52280307'), cep_to_coords('53160401'), cep_to_coords('55014708'), cep_to_coords('54460241'), cep_to_coords('53010250'), cep_to_coords('55299165'), cep_to_coords('54515640'), cep_to_coords('54420460'), cep_to_coords('54762420'), cep_to_coords('54270813'), cep_to_coords('55120021'), cep_to_coords('56537000'), cep_to_coords('54410400'), cep_to_coords('54420420'), cep_to_coords('36316480'), cep_to_coords('55640302'), cep_to_coords('56321530'), cep_to_coords('55145970'), cep_to_coords('54320485'), cep_to_coords('54330353'), cep_to_coords('54190050'), cep_to_coords('51201420'), cep_to_coords('54774260'), cep_to_coords('53400308'), cep_to_coords('54792470'), cep_to_coords('54756665'), cep_to_coords('54350115'), cep_to_coords('53520325'), cep_to_coords('545000'), cep_to_coords('54430590'), cep_to_coords('53570105'), cep_to_coords('56312845'), cep_to_coords('53620114'), cep_to_coords('53545653'), cep_to_coords('53080121'), cep_to_coords('52210002'), cep_to_coords('55602560'), cep_to_coords('53565115'), cep_to_coords('52090131'), cep_to_coords('5076130'), cep_to_coords('52091158'), cep_to_coords('50090430'), cep_to_coords('53350500'), cep_to_coords('56309195'), cep_to_coords('53441505'), cep_to_coords('52190385'), cep_to_coords('50640800'), cep_to_coords('50080330'), cep_to_coords('54270055'), cep_to_coords('53401627'), cep_to_coords('5303061'), cep_to_coords('53440713'), cep_to_coords('5478300'), cep_to_coords('53180430'), cep_to_coords('50680230'), cep_to_coords('54520535'), cep_to_coords('54270158'), cep_to_coords('54756231'), cep_to_coords('54768595'), cep_to_coords('53050200'), cep_to_coords('54325628'), cep_to_coords('53360110'), cep_to_coords('54780092'), cep_to_coords('53640068'), cep_to_coords('54410370'), cep_to_coords('53620590'), cep_to_coords('50290000'), cep_to_coords('53427220'), cep_to_coords('55614000'), cep_to_coords('50690454'), cep_to_coords('5303210'), cep_to_coords('54768690'), cep_to_coords('56330045'), cep_to_coords('53405710'), cep_to_coords('55294100'), cep_to_coords('53520390'), cep_to_coords('54789250'), cep_to_coords('56318775'), cep_to_coords('54505410'), cep_to_coords('53525713'), cep_to_coords('56515470'), cep_to_coords('54315145'), cep_to_coords('55530970'), cep_to_coords('56306470'), cep_to_coords('54505350'), cep_to_coords('50731530'), cep_to_coords('50771015'), cep_to_coords('56321180'), cep_to_coords('54040000'), cep_to_coords('53270080'), cep_to_coords('54530540'), cep_to_coords('52221035')


# In[19]:


print(coordenadasrow20426to25425)


# In[20]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in row20426to25425.tolist():
    result.append(''.join(pattern.findall(item)))


# In[21]:


print(result)


# In[22]:


dfrow20426to25425 = pd.DataFrame(coordenadasrow20426to25425, result)


# In[23]:


dfrow20426to25425


# In[24]:


dfrow20426to25425.reset_index(level=0, inplace=True)


# In[25]:


dfrow20426to25425


# In[26]:


dfrow20426to25425 = dfrow20426to25425.rename(columns={'index':'cep'}) 


# In[27]:


bancoesusalltabsrais2019nodupsCEPS[['id']][20426:25425]


# In[28]:


id20426_25424 = bancoesusalltabsrais2019nodupsCEPS[['id']][20426:25425]


# In[30]:


id20426_25424.reset_index(level=0, inplace=True)


# In[31]:


id20426_25424


# In[32]:


dfrow20426to25425['id'] = id20426_25424['id']
dfrow20426to25425['index'] = id20426_25424['index']


# In[33]:


dfrow20426to25425


# In[34]:


dfrow20426to25425[dfrow20426to25425.columns[[4,3,0,1,2]]]


# In[35]:


dfrow20426to25425 = dfrow20426to25425[dfrow20426to25425.columns[[4,3,0,1,2]]]


# In[36]:


dfrow20426to25425


# In[37]:


dfrow20426to25425.to_excel('dfrow20426to25425latlong.xlsx')


# # All latsandlongs

# In[1]:


import pandas as pd


# In[2]:


dfrow0to425 = pd.read_excel('dfrow0to425latlong.xlsx')


# In[3]:


dfrow0to425


# In[13]:


dfrow0to425.rename({'Unnamed: 0':'index'}, axis=1, inplace=True)


# In[14]:


dfrow0to425


# In[15]:


dfrow0to425.to_excel('dfrow0to425latlong.xlsx')


# In[16]:


dfrow0to425 = pd.read_excel('dfrow0to425latlong.xlsx')


# In[17]:


dfrow0to425


# In[20]:


dfrow0to425.drop({'Unnamed: 0'}, axis=1, inplace=True)


# In[25]:


dfrow0to425


# In[26]:


dfrow0to425.to_excel('dfrow0to425latlong.xlsx', index=False)


# In[23]:


dfrow425to5425 = pd.read_excel('dfrow425to5425latlong.xlsx')


# In[24]:


dfrow425to5425


# In[27]:


dfrow425to5425.drop('Unnamed: 0', axis=1, inplace=True)


# In[28]:


dfrow425to5425


# In[31]:


dfrow425to5425.to_excel('dfrow425to5425latlong.xlsx', index=False)


# In[ ]:





# In[54]:


dfrow5426to10425 = pd.read_excel('dfrow5426to10425latlong.xlsx')


# In[55]:


dfrow5426to10425


# In[56]:


dfrow5426to10425.drop('Unnamed: 0', axis=1, inplace=True)


# In[57]:


dfrow5426to10425


# In[58]:


dfrow5426to10425.to_excel('dfrow5426to10425latlong.xlsx', index = False)


# In[ ]:





# In[33]:


dfrow10426to15425 = pd.read_excel('dfrow10426to15425latlong.xlsx')


# In[34]:


dfrow10426to15425


# In[35]:


dfrow10426to15425.drop('Unnamed: 0', axis = 1, inplace=True)


# In[36]:


dfrow10426to15425


# In[37]:


dfrow10426to15425.to_excel('dfrow10426to15425latlong.xlsx', index = False)


# In[ ]:





# In[38]:


dfrow15426to20425 = pd.read_excel('dfrow15426to20425latlong.xlsx')


# In[39]:


dfrow15426to20425


# In[41]:


dfrow15426to20425.drop('Unnamed: 0', axis=1, inplace=True)


# In[42]:


dfrow15426to20425


# In[43]:


dfrow15426to20425.to_excel('dfrow15426to20425latlong.xlsx', index=False)


# In[ ]:





# In[44]:


dfrow20426to25425 = pd.read_excel('dfrow20426to25425latlong.xlsx')


# In[45]:


dfrow20426to25425


# In[47]:


dfrow20426to25425.drop('Unnamed: 0', axis=1, inplace=True)


# In[48]:


dfrow20426to25425


# In[49]:


dfrow20426to25425.to_excel('dfrow20426to25425latlong.xlsx', index = False)


# In[ ]:





# In[ ]:





# In[59]:


dfrow0to425 = pd.read_excel('dfrow0to425latlong.xlsx')
dfrow425to5425 = pd.read_excel('dfrow425to5425latlong.xlsx')
dfrow5426to10425 = pd.read_excel('dfrow5426to10425latlong.xlsx')
dfrow10426to15425 = pd.read_excel('dfrow10426to15425latlong.xlsx')
dfrow15426to20425 = pd.read_excel('dfrow15426to20425latlong.xlsx')
dfrow20426to25425 = pd.read_excel('dfrow20426to25425latlong.xlsx')


# In[51]:


dfrow0to425


# In[52]:


dfrow425to5425


# In[60]:


dfrow5426to10425


# In[53]:


dfrow10426to15425


# In[62]:


dfrow15426to20425


# In[61]:


dfrow20426to25425


# In[63]:


#dfrow0to425, dfrow425to5425, dfrow5426to10425, dfrow10426to15425, dfrow15426to20425, dfrow20426to25425


# In[64]:


pd.concat([dfrow0to425, dfrow425to5425, dfrow5426to10425, dfrow10426to15425, dfrow15426to20425, dfrow20426to25425])


# In[84]:


dfrow0to25425 = pd.concat([dfrow0to425, dfrow425to5425, dfrow5426to10425, dfrow10426to15425, dfrow15426to20425, dfrow20426to25425])


# In[85]:


dfrow0to25425


# In[88]:


dfrow0to25425['cep'].astype(str).str.replace('.0', '', regex=False)


# removing [traling zero](https://stackoverflow.com/questions/42403907/how-to-round-remove-traling-0-zeros-in-pandas-column) from a dataframe

# In[89]:


dfrow0to25425['cep']=dfrow0to25425['cep'].astype(str).str.replace('.0', '', regex=False)


# In[90]:


dfrow0to25425


# In[92]:


dfrow0to25425.dtypes


# In[96]:


dfrow0to25425['cep'].isna().sum()


# In[98]:


dfrow0to25425.to_excel('dfrow0to25425latlong.xlsx', index=False)


# In[ ]:





# # Merging back with the whole data

# In[99]:


dfrow0to25425 = pd.read_excel('dfrow0to25425latlong.xlsx')


# In[100]:


dfrow0to25425


# In[101]:


dfrow0to25425['cep']=dfrow0to25425['cep'].astype(str).str.replace('.0', '', regex=False)


# In[102]:


dfrow0to25425


# In[103]:


#the data with all columns

#bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[ ]:


#the data with all ceps

#cepbancoesusalltabsrais2019 = pd.read_excel('cepbancoesusalltabsrais2019.xlsx')


# In[104]:


#the data will no duplicates ceps 

#bancoesusalltabsrais2019nodupsCEPS = pd.read_csv('bancoesusalltabsrais2019nodupsCEPS.csv')


# In[108]:


cepbancoesusalltabsrais2019 = pd.read_excel('cepbancoesusalltabsrais2019.xlsx')


# In[109]:


cepbancoesusalltabsrais2019


# In[36]:


#it should have over 252k rows, it is skipping the empty cells, I don't want that

#it made no difference actually, over 2k were empty cells


# In[122]:


cepbancoesusalltabsrais2019 = pd.read_excel('cepabancoesusalltabsrais2019.xlsx')


# In[123]:


cepbancoesusalltabsrais2019


# In[128]:


cepbancoesusalltabsrais2019['cep'] = cepbancoesusalltabsrais2019['cep'].str.replace('.','')
cepbancoesusalltabsrais2019['cep'] = cepbancoesusalltabsrais2019['cep'].str.replace('-','')


# In[129]:


cepbancoesusalltabsrais2019['cep']


# In[130]:


cepbancoesusalltabsrais2019


# In[131]:


dfrow0to25425


# In[157]:


cepbancoesusalltabsrais2019.merge(dfrow0to25425, how='inner',on='cep',indicator=True)


# In[158]:


allcepsmerge_bancoesusalltabsrais2019 = cepbancoesusalltabsrais2019.merge(dfrow0to25425, how='inner',on='cep',indicator=True)


# In[159]:


allcepsmerge_bancoesusalltabsrais2019.to_excel('allcepsmerge_bancoesusalltabsrais2019.xlsx', index=False)


# In[160]:


allcepsmerge_bancoesusalltabsrais2019


# In[27]:


#it worked nice as expected, but those empty rows (over 2k rows) will make the data lose important observations

#after testing below the 2k rows of data was never lost


# In[134]:


bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[135]:


bancoesusalltabsrais2019


# In[137]:


bancoesusalltabsrais2019[['cep']]


# In[138]:


onlycep_bancoesusalltabsrais2019=bancoesusalltabsrais2019[['cep']]


# In[142]:


onlycep_bancoesusalltabsrais2019


# In[146]:


onlycep_bancoesusalltabsrais2019.reset_index(level=0, inplace=True)


# In[148]:


onlycep_bancoesusalltabsrais2019


# In[149]:


onlycep_bancoesusalltabsrais2019['cep'] = onlycep_bancoesusalltabsrais2019['cep'].str.replace('.','')
onlycep_bancoesusalltabsrais2019['cep'] = onlycep_bancoesusalltabsrais2019['cep'].str.replace('-','')
onlycep_bancoesusalltabsrais2019['cep']


# In[150]:


onlycep_bancoesusalltabsrais2019


# In[152]:


onlycep_bancoesusalltabsrais2019.to_excel('onlycep_bancoesusalltabsrais2019.xlsx',index=False)


# In[153]:


onlycep_bancoesusalltabsrais2019


# In[154]:


dfrow0to25425


# In[155]:


onlycep_bancoesusalltabsrais2019.merge(dfrow0to25425, how='inner', on='cep', indicator=True)


# In[161]:


onlycep_bancoesusalltabsrais2019merge2indexes = onlycep_bancoesusalltabsrais2019.merge(dfrow0to25425, how='inner', on='cep', indicator=True)


# In[162]:


onlycep_bancoesusalltabsrais2019merge2indexes.to_excel('onlycep_bancoesusalltabsrais2019merge2indexes.xlsx', index=False)


# In[156]:


#it made no difference, it had the same results 236677 rows out of 252397


# ## now merging back with the whole dataset with all columns 

# In[1]:


import pandas as pd


# In[2]:


allcepsmerge_bancoesusalltabsrais2019 = pd.read_excel('allcepsmerge_bancoesusalltabsrais2019.xlsx')


# In[3]:


allcepsmerge_bancoesusalltabsrais2019


# In[4]:


bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[5]:


bancoesusalltabsrais2019.head(3)


# In[6]:


bancoesusalltabsrais2019['cep']


# In[7]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('.','')
bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('-','')
bancoesusalltabsrais2019['cep']


# In[8]:


bancoesusalltabsrais2019


# In[9]:


bancoesusalltabsrais2019[['cep']]


# In[12]:


bancoesusalltabsrais2019['cep'].dtype


# In[18]:


bancoesusalltabsrais2019.drop('_merge', axis=1,inplace=True)


# In[19]:


bancoesusalltabsrais2019.head(3)


# In[20]:


allcepsmerge_bancoesusalltabsrais2019.head(3)


# In[21]:


allcepsmerge_bancoesusalltabsrais2019.drop('_merge', axis=1, inplace=True)


# In[22]:


allcepsmerge_bancoesusalltabsrais2019


# In[14]:


allcepsmerge_bancoesusalltabsrais2019['cep'].dtype


# In[15]:


allcepsmerge_bancoesusalltabsrais2019['cep'] = allcepsmerge_bancoesusalltabsrais2019['cep'].astype(str)


# In[16]:


allcepsmerge_bancoesusalltabsrais2019['cep'].dtype


# In[24]:


allcepsmerge_bancoesusalltabsrais2019.drop(['id','index'], axis=1, inplace=True)


# In[25]:


allcepsmerge_bancoesusalltabsrais2019


# In[27]:


bancoesusalltabsrais2019.head(3)


# In[28]:


pd.set_option('display.max_columns',None)


# In[30]:


bancoesusalltabsrais2019.head(3)


# In[31]:


bancoesusalltabsrais2019.drop('notificadorEmail', axis=1, inplace=True)


# In[33]:


bancoesusalltabsrais2019.drop('telefoneContato', axis=1, inplace=True)


# In[38]:


bancoesusalltabsrais2019.drop('nomeCompleto', axis=1, inplace=True)


# In[65]:


bancoesusalltabsrais2019.drop('telefone', axis=1, inplace=True)


# In[77]:


bancoesusalltabsrais2019.head(3)


# In[44]:


bancoesusalltabsrais2019['origem'].unique()


# In[76]:


pd.set_option('display.max_rows', 100)


# In[69]:


bancoesusalltabsrais2019.dtypes


# In[50]:


bancoesusalltabsrais2019['Ind Trab Parcial'].max()


# In[51]:


bancoesusalltabsrais2019['Ind Trab Parcial'].min()


# In[53]:


bancoesusalltabsrais2019['Ind Trab Parcial'] = bancoesusalltabsrais2019['Ind Trab Parcial'].astype('int8')


# In[54]:


bancoesusalltabsrais2019['Ind Trab Intermitente'].max()


# In[55]:


bancoesusalltabsrais2019['Ind Trab Intermitente'].min()


# In[58]:


bancoesusalltabsrais2019['Ind Trab Intermitente'] = bancoesusalltabsrais2019['Ind Trab Parcial'].astype('int8')


# In[71]:


bancoesusalltabsrais2019['Idade'].max()


# In[72]:


bancoesusalltabsrais2019['Idade'].min()


# In[73]:


bancoesusalltabsrais2019['Idade'] = bancoesusalltabsrais2019['Idade'].astype('int8')


# In[ ]:





# changing dtypes will reduce a lot of memory
# 
# [Reducing memory usage in pandas with smaller datatypes](https://towardsdatascience.com/reducing-memory-usage-in-pandas-with-smaller-datatypes-b527635830af)
# 
# 
# [Understanding Data Types in Python](https://jakevdp.github.io/PythonDataScienceHandbook/02.01-understanding-data-types.html)

# In[52]:


'''
Data type	Description
bool_	Boolean (True or False) stored as a byte
int_	Default integer type (same as C long; normally either int64 or int32)
intc	Identical to C int (normally int32 or int64)
intp	Integer used for indexing (same as C ssize_t; normally either int32 or int64)
int8	Byte (-128 to 127)
int16	Integer (-32768 to 32767)
int32	Integer (-2147483648 to 2147483647)
int64	Integer (-9223372036854775808 to 9223372036854775807)
uint8	Unsigned integer (0 to 255)
uint16	Unsigned integer (0 to 65535)
uint32	Unsigned integer (0 to 4294967295)
uint64	Unsigned integer (0 to 18446744073709551615)
float_	Shorthand for float64.
float16	Half precision float: sign bit, 5 bits exponent, 10 bits mantissa
float32	Single precision float: sign bit, 8 bits exponent, 23 bits mantissa
float64	Double precision float: sign bit, 11 bits exponent, 52 bits mantissa
complex_	Shorthand for complex128.
complex64	Complex number, represented by two 32-bit floats
complex128	Complex number, represented by two 64-bit floats
'''


# In[ ]:





# In[116]:


bancoesusalltabsrais2019.info()


# In[99]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].max()


# In[80]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].min()


# In[83]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].memory_usage


# In[88]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].str.replace(',','.')


# In[89]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC']=bancoesusalltabsrais2019['Vl Rem Janeiro CC'].str.replace(',','.')


# In[90]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC']


# In[95]:


#bancoesusalltabsrais2019['Vl Rem Janeiro CC'].str.replace('.0', '', regex=False)


# In[94]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].str.lstrip('0')


# In[96]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'] = bancoesusalltabsrais2019['Vl Rem Janeiro CC'].str.lstrip('0')


# In[100]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].max()


# In[101]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].min()


# In[106]:


bancoesusalltabsrais2019['Vl Rem Janeiro CC'].str.rstrip('.0')


# In[ ]:


Vl Rem Janeiro CC                                                object
Vl Rem Fevereiro CC                                              object
Vl Rem Março CC                                                  object
Vl Rem Abril CC                                                  object
Vl Rem Maio CC                                                   object
Vl Rem Junho CC                                                  object
Vl Rem Julho CC                                                  object
Vl Rem Agosto CC                                                 object
Vl Rem Setembro CC                                               object
Vl Rem Outubro CC                                                object
Vl Rem Novembro CC                                               object


# In[110]:


bancoesusalltabsrais2019['Vl Rem Fevereiro CC'].max()


# In[108]:


bancoesusalltabsrais2019['Vl Rem Fevereiro CC'].min()


# In[111]:


bancoesusalltabsrais2019['Vl Rem Fevereiro CC'].str.rstrip('.0')


# In[113]:


bancoesusalltabsrais2019['Vl Rem Fevereiro CC'] = bancoesusalltabsrais2019['Vl Rem Fevereiro CC'].str.replace(',','.')
bancoesusalltabsrais2019['Vl Rem Fevereiro CC'] = bancoesusalltabsrais2019['Vl Rem Fevereiro CC'].str.lstrip('0')
bancoesusalltabsrais2019['Vl Rem Fevereiro CC'] = bancoesusalltabsrais2019['Vl Rem Fevereiro CC'].str.rstrip('.0')
bancoesusalltabsrais2019['Vl Rem Fevereiro CC']


# In[115]:


bancoesusalltabsrais2019['Vl Rem Março CC'] = bancoesusalltabsrais2019['Vl Rem Março CC'].str.replace(',','.')
bancoesusalltabsrais2019['Vl Rem Março CC'] = bancoesusalltabsrais2019['Vl Rem Março CC'].str.lstrip('0')
bancoesusalltabsrais2019['Vl Rem Março CC'] = bancoesusalltabsrais2019['Vl Rem Março CC'].str.rstrip('.0')
bancoesusalltabsrais2019['Vl Rem Março CC']


# In[ ]:





# In[ ]:


#this actually increased memory usage


# In[ ]:





# In[39]:


#notificadorEmail and telefoneContato and nomeCompleto columns were dropped to allocate memory for the merge but it still 
#did not work 


# In[117]:


bancoesusalltabsrais2019.merge(allcepsmerge_bancoesusalltabsrais2019, how='inner',on='cep', indicator=True)


# In[ ]:





# # this isn't working, I'll merge with the bancoesus selecionado

# In[119]:


#which has fewer columns 


# In[1]:


import dask
import dask.dataframe as dd


# In[2]:


bancoesusrais2019selecionado = dd.read_excel('bancoesusrais2019selecionado.xlsx')


# From Excel to [CSV](https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python)

# In[ ]:





# In[ ]:





# In[ ]:





# In[3]:


import pandas as pd


# In[4]:


bancoesusrais2019selecionado = pd.read_excel('bancoesusrais2019selecionado.xlsx')


# In[5]:


bancoesusrais2019selecionado.shape


# In[32]:


bancoesusrais2019selecionado.head(3)


# In[33]:


bancoesusrais2019selecionado.to_csv('bancoesusrais2019selecionado.csv', sep=',', index=False)


# In[12]:


bancoesusrais2019selecionado.info()


# In[35]:


bancoesusrais2019selecionadocsv = pd.read_csv('bancoesusrais2019selecionado.csv')


# In[36]:


bancoesusrais2019selecionadocsv.shape


# In[37]:


bancoesusrais2019selecionadocsv.head(3)


# In[38]:


bancoesusrais2019selecionadocsv.drop('Unnamed: 0', axis=1,inplace=True)


# In[40]:


bancoesusrais2019selecionadocsv.head(3)


# In[13]:


bancoesusrais2019selecionadocsv.info()


# In[14]:


allcepsmerge_bancoesusalltabsrais2019 = pd.read_excel('allcepsmerge_bancoesusalltabsrais2019.xlsx')


# In[15]:


allcepsmerge_bancoesusalltabsrais2019


# In[ ]:





# In[16]:


allcepsmerge_bancoesusalltabsrais2019['cep'] = allcepsmerge_bancoesusalltabsrais2019['cep'].astype(str)


# In[ ]:


#allcepsmerge_bancoesusalltabsrais2019.drop(['id','index','_merge'], axis=1, inplace=True)


# In[17]:


allcepsmerge_bancoesusalltabsrais2019.drop(['_merge'], axis=1, inplace=True)


# In[19]:


allcepsmerge_bancoesusalltabsrais2019.info()


# In[22]:


allcepsmerge_bancoesusalltabsrais2019.to_csv('allcepsmerge_bancoesusalltabsrais2019.csv',sep=',',index=False)


# In[23]:


allcepsmerge_bancoesusalltabsrais2019csv = pd.read_csv('allcepsmerge_bancoesusalltabsrais2019.csv')


# In[24]:


allcepsmerge_bancoesusalltabsrais2019csv.shape


# In[25]:


allcepsmerge_bancoesusalltabsrais2019csv.head(3)


# In[32]:


bancoesusrais2019selecionado['Escolaridade após 2005'].max()


# In[38]:


bancoesusrais2019selecionado['estado'].unique()


# In[39]:


bancoesusrais2019selecionado.drop('estado',axis=1,inplace=True)


# In[ ]:


bancoesusrais2019selecionado


# In[33]:


bancoesusrais2019selecionado['Escolaridade após 2005'] = bancoesusrais2019selecionado['Escolaridade após 2005'].astype('int8')


# In[14]:


bancoesusrais2019selecionado['IBGE Subsetor']


# In[17]:


bancoesusrais2019selecionado['Qtd Dias Afastamento']


# In[18]:


bancoesusrais2019selecionado['Qtd Dias Afastamento'].max()


# In[21]:


bancoesusrais2019selecionado['Qtd Dias Afastamento'] = bancoesusrais2019selecionado['Qtd Dias Afastamento'].astype('int16')


# In[15]:


bancoesusrais2019selecionado['IBGE Subsetor'] = bancoesusrais2019selecionado['IBGE Subsetor'].astype('int8')


# In[25]:


bancoesusrais2019selecionado['Mun Trab'].max()            


# In[27]:


bancoesusrais2019selecionado['Mun Trab'].min()       


# In[28]:


bancoesusrais2019selecionado['Mun Trab'] = bancoesusrais2019selecionado['Mun Trab'].astype('int32')


# In[ ]:


'''
Data type	Description
bool_	Boolean (True or False) stored as a byte
int_	Default integer type (same as C long; normally either int64 or int32)
intc	Identical to C int (normally int32 or int64)
intp	Integer used for indexing (same as C ssize_t; normally either int32 or int64)
int8	Byte (-128 to 127)
int16	Integer (-32768 to 32767)
int32	Integer (-2147483648 to 2147483647)
int64	Integer (-9223372036854775808 to 9223372036854775807)
uint8	Unsigned integer (0 to 255)
uint16	Unsigned integer (0 to 65535)
uint32	Unsigned integer (0 to 4294967295)
uint64	Unsigned integer (0 to 18446744073709551615)
float_	Shorthand for float64.
float16	Half precision float: sign bit, 5 bits exponent, 10 bits mantissa
float32	Single precision float: sign bit, 8 bits exponent, 23 bits mantissa
float64	Double precision float: sign bit, 11 bits exponent, 52 bits mantissa
complex_	Shorthand for complex128.
complex64	Complex number, represented by two 32-bit floats
complex128	Complex number, represented by two 64-bit floats
'''


# In[ ]:





# In[ ]:





# In[ ]:





# In[20]:


#https://www.pythonpool.com/python-memory-error/


# In[ ]:





# In[1]:


import sys
sys.version


# In[28]:


np.zeros((275370420,), dtype='uint8')


# In[31]:


np.zeros((20,275370417), dtype='uint8')


# In[42]:


allcepsmerge_bancoesusalltabsrais2019csv['cep'] = allcepsmerge_bancoesusalltabsrais2019csv['cep'].astype(str)


# In[ ]:





# In[43]:


bancoesusrais2019selecionadocsv.merge(allcepsmerge_bancoesusalltabsrais2019csv, how='inner',on='cep', indicator='_merge2')


# In[12]:


import numpy as np


# In[13]:


np.zeros((20,275370417), dtype='int8')


# In[20]:


np.zeros((275370417,), dtype='uint8')


# # merge with bancoesusrais2019selecionadocnaecbo.xlsx to test

# In[42]:


bancoesusrais2019selecionadocnaecbo = pd.read_excel('bancoesusrais2019selecionadocnaecbo.xlsx')


# In[43]:


bancoesusrais2019selecionadocnaecbo.shape


# In[44]:


bancoesusrais2019selecionadocnaecbo.head(3)


# In[45]:


bancoesusrais2019selecionadocnaecbo.merge(allcepsmerge_bancoesusalltabsrais2019, how='inner',on='cep', indicator=True)


# In[46]:


#https://stackoverflow.com/questions/58705843/unable-to-allocate-array-with-shape-1482535-67826-and-data-type-int64


# In[47]:


#https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type !!!


# In[48]:


#https://www.quora.com/How-can-I-deal-with-the-memory-error-generated-by-large-Numpy-Python-arrays


# In[49]:


#https://www.kaggle.com/yuliagm/how-to-work-with-big-datasets-on-16g-ram-dask!!!


# # Merging with dask 

# [Dask](https://docs.dask.org/en/latest/dataframe.html)

# In[44]:


import gc


# In[45]:


del bancoesusrais2019selecionado
del allcepsmerge_bancoesusalltabsrais2019


# In[46]:


gc.collect()


# In[1]:


import dask
import dask.dataframe as dd


# In[2]:


allcepsmerge_bancoesusalltabsrais2019csv = dd.read_csv('allcepsmerge_bancoesusalltabsrais2019.csv')


# In[3]:


allcepsmerge_bancoesusalltabsrais2019csv.head(3)


# In[4]:


allcepsmerge_bancoesusalltabsrais2019csv.dtypes


# In[5]:


dtypes = {
        'cep'                  : 'str',
        'CBO Ocupação 2002'    : 'str',
}


# In[6]:


bancoesusrais2019selecionadocsv = dd.read_csv('bancoesusrais2019selecionado.csv', dtype=dtypes)


# In[7]:


bancoesusrais2019selecionadocsv.dtypes


# In[8]:


bancoesusrais2019selecionadocsv['cep']= bancoesusrais2019selecionadocsv['cep'].astype('str')


# In[9]:


allcepsmerge_bancoesusalltabsrais2019csv['cep'] = allcepsmerge_bancoesusalltabsrais2019csv['cep'].astype('str')


# In[10]:


bancoesusrais2019selecionadocsv['cep'] = bancoesusrais2019selecionadocsv['cep'].replace('/','')


# In[ ]:





# In[11]:


bancoesusrais2019selecionadocsv['cep'].dtype


# In[12]:


allcepsmerge_bancoesusalltabsrais2019csv['cep'].dtype


# In[16]:


allcepsmerge_bancoesusalltabsrais2019csv['cep'].isna().sum().compute()


# In[31]:


#bancoesusrais2019selecionadocsv['CBO Ocupação 2002']= bancoesusrais2019selecionadocsv['CBO Ocupação 2002'].astype('str')


# In[ ]:





# In[17]:


dd.merge(bancoesusrais2019selecionadocsv,allcepsmerge_bancoesusalltabsrais2019csv, how='inner',on='cep', indicator='_merge2')


# In[18]:


bancoesusrais2019selecionando_allcepsmerge = dd.merge(bancoesusrais2019selecionadocsv,allcepsmerge_bancoesusalltabsrais2019csv, how='inner',on='cep', indicator='_merge2')


# In[22]:


bancoesusrais2019selecionando_allcepsmerge.head()


# In[ ]:


bancoesusrais2019selecionando_allcepsmerge.to_csv('bancoesusrais2019selecionando_allcepsmerge.csv', sep=',', index=False)


# In[44]:


import numpy as np


# In[47]:


np.zeros((27941574,), dtype='int8')


# In[45]:


np.zeros((23, 88938798), dtype='int8')


# In[ ]:





# # Use join sorting the values before

# In[49]:


#otherwise it would have to change all dtypes on the whole data, than save as csv, open it, then use dask to merge and save it 
#to csv


# In[ ]:


#merging by chunkzise might also work https://www.kaggle.com/yuliagm/how-to-work-with-big-datasets-on-16g-ram-dask


# In[2]:


import pandas as pd


# In[3]:


bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[4]:


bancoesusalltabsrais2019.head(3)


# In[5]:


bancoesusalltabsrais2019['cep']


# In[6]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('.','')
bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('-','')
bancoesusalltabsrais2019['cep']


# In[7]:


bancoesusalltabsrais2019


# In[8]:


bancoesusalltabsrais2019[['cep']]


# In[9]:


bancoesusalltabsrais2019['cep'].dtype


# In[10]:


bancoesusalltabsrais2019.drop('_merge', axis=1,inplace=True)


# In[11]:


bancoesusalltabsrais2019.head(3)


# In[12]:


bancoesusalltabsrais2019.sort_values(['cep'])


# In[13]:


pd.set_option('display.max_columns', None)


# In[15]:


bancoesusalltabsrais2019.memory_usage()


# In[16]:


bancoesusalltabsrais2019.info()


# In[17]:


bancoesusalltabsrais2019.columns


# In[18]:


bancoesusalltabsrais2019.columns.get_loc('cep')


# In[24]:


bancoesusalltabsrais2019.sort_values(['cep'], ascending = False)


# In[30]:


bancoesusalltabsrais2019['cep'].sort_values(ascending=False).head(20)


# In[31]:


bancoesusalltabsrais2019['cep'].sort_values().head(20)


# In[45]:


bancoesusalltabsrais2019


# In[46]:


allcepsmerge_bancoesusalltabsrais2019 = pd.read_excel('allcepsmerge_bancoesusalltabsrais2019.xlsx')


# In[47]:


allcepsmerge_bancoesusalltabsrais2019.shape


# In[49]:


allcepsmerge_bancoesusalltabsrais2019.head()


# In[66]:


allcepsmerge_bancoesusalltabsrais2019[250:300]


# In[37]:


allcepsmerge_bancoesusalltabsrais2019.drop('_merge',axis=1, inplace=True)


# In[39]:


allcepsmerge_bancoesusalltabsrais2019.drop(['index', 'id'], axis=1, inplace=True)


# In[40]:


allcepsmerge_bancoesusalltabsrais2019


# In[67]:


allcepsmerge_bancoesusalltabsrais2019.info()


# In[50]:


allcepsmerge_bancoesusalltabsrais2019.sort_values('cep', ascending =False).head(30)


# In[56]:


bancoesusalltabsrais2019['cep'].sort_values(ascending =False).head(30)


# In[57]:


#using join would not work, although I had an id and index, it will be different from the original data


# # Ray library 

# In[68]:


#https://docs.ray.io/en/master/data/dataset.html


# In[69]:


pip install ray


# In[1]:


pip install modin


# In[3]:


pip install ray[default]


# In[6]:


ray.shutdown()


# In[ ]:


import modin.pandas as pd
import ray 

ray.init(include_dashboard=False)
#ray.init(address="127.0.0.1:8265")
bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[ ]:


ray.init(redis_address="127.0.0.1:8265")


# In[ ]:





# # using kagle notebook 

# In[1]:


#https://www.kaggle.com/code


# In[ ]:


#https://www.kaggle.com/andreluizcoelho/notebookd852836828/edit


# In[1]:


#'Your notebook tried to allocate more memory than is available. It has restarted.' over 16GB of memory on kaggle was still not 
#enough


# # Pyspark

# In[2]:


pip install pyspark


# In[1]:


import pyspark


# In[2]:


pyspark


# In[3]:


from pyspark.sql import SparkSession


# In[14]:


spark = SparkSession.builder.getOrCreate()
#this first had the error 
#Java gateway process exited before sending its port number
#to fix it see it below, but for me what worked is what I wrote two cells below


# In[12]:


'''After trying over fifteen resources - and perusing about twice that many - the only one that works is this previously- 
non-upvoted answer https://stackoverflow.com/a/55326797/1056563:

export PYSPARK_SUBMIT_ARGS="--master local[2] pyspark-shell"

It's not important whether to use local[2] or local or local[*]: what is required is the format including the critical 
pyspark-shell piece.

Another way to handle this - and more resistant to environmental vagaries - 
is having the following line handy in your python code:

os.environ["PYSPARK_SUBMIT_ARGS"] = "pyspark-shell"

'''


# In[11]:


#I installed mySQL, then install JAVA, both from .exe, spark I only installed through pip intall pyspark, 
#then, it worked opening the shell 'shell.cpython-38.pyc' that is on C:\Users\andre\anaconda3\Lib\site-packages\pyspark\python\pyspark\__pycache__


# In[15]:


spark.version


# In[16]:


pyspark


# In[22]:


df = spark.read.csv("allcepsmerge_bancoesusalltabsrais2019.csv")
# Displays the content of the DataFrame to stdout
df.show()


# In[23]:


df.head(3)


# In[24]:


df.head()


# In[31]:


df1 = spark.read.csv('bancoesusrais2019selecionado.csv', s)
df1.show()


# In[32]:


newdf=df1.merge(df2, how='inner', on='cep', indicator=True)


# In[34]:


#pyspark does not have merge, it has unionAll and unionByName which would be equivalent to join
#and it needs the same number of columns
#https://mungingdata.com/pyspark/union-unionbyname-merge-dataframes/


# In[33]:


res = df.unionByName(df1)
res.show()


# In[36]:


#at least I got it running, although after many problems, two days, having to install and do stuff on mysql, install java
#fix stuff to run pyspark, etc


# In[ ]:





# In[ ]:





# ## connecting to mySQL 

# In[14]:


pip install mysql-connector-python


# In[4]:


import mysql.connector as mdb


# In[5]:


#mdb.connect(user = 'amndre', password='passwd', db ='what')


# In[8]:


from getpass import getpass
from  mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    ) as connection:
        print(connection)
except Error as e:
    print(e)


# In[35]:


#import os


# In[36]:


#os.environ["PYSPARK_SUBMIT_ARGS"] = "pyspark-shell"


# In[13]:


import pyspark


# In[14]:


pyspark


# In[19]:


spark.version


# In[10]:


from pyspark.sql import SparkSession


# In[20]:


#spark = SparkSession.builder.getOrCreate()


# In[12]:


#import os


# In[13]:


#os.environ["PYSPARK_SUBMIT_ARGS"] = "pyspark-shell"


# In[ ]:





# In[6]:


from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row

df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])
df


# In[ ]:





# In[ ]:


#this below will probably be the best option that will solve my problem


# # importing chunks and merging by chunks or by reduced number of rows, 
# # then concat

# In[37]:


#https://www.kaggle.com/yuliagm/how-to-work-with-big-datasets-on-16g-ram-dask


# In[1]:


'''
#set up an empty dataframe
df_converted = pd.DataFrame()

#we are going to work with chunks of size 1 million rows
chunksize = 10 ** 6

#in each chunk, filter for values that have 'is_attributed'==1, and merge these values into one dataframe
for chunk in pd.read_csv('../input/train.csv', chunksize=chunksize, dtype=dtypes):
    filtered = (chunk[(np.where(chunk['is_attributed']==1, True, False))])
    df_converted = pd.concat([df_converted, filtered], ignore_index=True, )
'''


# In[2]:


'''
df_converted.info()
'''


# In[3]:


'''
df_converted.head()
'''


# In[4]:


'''
train = pd.read_csv('../input/train.csv', nrows=10000, dtype=dtypes)
train.head()
'''


# In[5]:


'''
#plain skipping looses heading info.  It's OK for files that don't have headings, 
#or dataframes you'll be linking together, or where you make your own custom headings...
train = pd.read_csv('../input/train.csv', skiprows=5000000, nrows=1000000, header = None, dtype=dtypes)
train.head()
'''


# In[6]:


'''
#but if you want to import the headings from the original file
#skip first 5mil rows, but use the first row for heading:
train = pd.read_csv('../input/train.csv', skiprows=range(1, 5000000), nrows=1000000, dtype=dtypes)
train.head()
'''


# the examples above came from [here](https://www.kaggle.com/yuliagm/how-to-work-with-big-datasets-on-16g-ram-dask)

# In[7]:


import pandas as pd


# In[8]:


bancoesusalltabsrais2019 = pd.read_excel('bancoesusalltabs_04012020to08052021rais2019.xlsx')


# In[9]:


bancoesusalltabsrais2019.shape


# In[10]:


bancoesusalltabsrais2019.head(3)


# In[11]:


bancoesusalltabsrais2019.to_csv('bancoesusalltabs_04012020to08052021rais2019.csv',sep=',',index=False)


# In[12]:


del bancoesusalltabsrais2019 


# In[13]:


import gc


# In[14]:


gc.collect()


# In[19]:


#https://stackify.com/python-garbage-collection/
#garbage collection should not be used often


# # merging by nrows 

# In[1]:


import pandas as pd


# In[2]:


bancoesusalltabsrais2019 = pd.read_csv('bancoesusalltabs_04012020to08052021rais2019.csv')


# In[3]:


bancoesusalltabsrais2019.info()


# In[4]:


bancoesusalltabsrais2019.memory_usage()


# In[6]:


pd.set_option('display.max_rows',None)


# In[7]:


bancoesusalltabsrais2019.memory_usage()


# In[8]:


pd.set_option('display.max_rows',10)


# In[9]:


bancoesusalltabsrais2019


# In[10]:


bancoesusalltabsrais2019.head(3)


# In[11]:


bancoesusalltabsrais2019.shape


# In[13]:


allcepsmerge_bancoesusalltabsrais2019 = pd.read_csv('allcepsmerge_bancoesusalltabsrais2019.csv')


# In[15]:


allcepsmerge_bancoesusalltabsrais2019.head()


# In[17]:


allcepsmerge_bancoesusalltabsrais2019.memory_usage()


# In[20]:


allcepsmerge_bancoesusalltabsrais2019.info()


# CSV files are larger in memory than XLSX files, but they are 100x faster to read than XLSX, [medium article](https://towardsdatascience.com/read-excel-files-with-python-1000x-faster-407d07ad0ed8)

# In[21]:


del bancoesusalltabsrais2019 


# In[1]:


import pandas as pd


# In[22]:


bancoesusalltabsrais2019 = pd.read_csv('bancoesusalltabs_04012020to08052021rais2019.csv')


# In[23]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('.','')
bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('-','')
bancoesusalltabsrais2019['cep']


# In[24]:


bancoesusalltabsrais2019.to_csv('bancoesusalltabs_04012020to08052021rais2019.csv', sep=',', index=False)


# ## importing the separate nrows 

# In[1]:


import pandas as pd


# In[2]:


bancoesusalltabsrais2019nrows28k = pd.read_csv('bancoesusalltabs_04012020to08052021rais2019.csv', nrows=28000)


# In[3]:


#del bancoesusalltabsrais2019nrows32k


# In[4]:


#del bancoesusalltabsrais2019


# In[ ]:





# In[5]:


bancoesusalltabsrais2019nrows28k.shape


# In[6]:


bancoesusalltabsrais2019nrows28k['cep'] = bancoesusalltabsrais2019nrows28k['cep'].astype(str)


# In[7]:


bancoesusalltabsrais2019nrows28k['cep'].dtype


# In[8]:


allcepsmerge_bancoesusalltabsrais2019 = pd.read_csv('allcepsmerge_bancoesusalltabsrais2019.csv')


# In[9]:


allcepsmerge_bancoesusalltabsrais2019


# In[10]:


allcepsmerge_bancoesusalltabsrais2019.drop(['index', 'id'], axis = 1, inplace = True)


# In[11]:


allcepsmerge_bancoesusalltabsrais2019


# In[12]:


allcepsmerge_bancoesusalltabsrais2019['cep'] = allcepsmerge_bancoesusalltabsrais2019['cep'].astype(str)


# In[13]:


allcepsmerge_bancoesusalltabsrais2019['cep'].dtype


# In[14]:


#bancoesusalltabsrais2019nrows28k.merge(allcepsmerge_bancoesusalltabsrais2019, how='inner', on='cep', indicator='_merge2')


# In[15]:


bancoesusalltabsrais2019nrowslatlongmerge28k = bancoesusalltabsrais2019nrows28k.merge(allcepsmerge_bancoesusalltabsrais2019, how='inner', on='cep', indicator='_merge2')


# In[16]:


bancoesusalltabsrais2019nrowslatlongmerge28k.shape


# In[17]:


bancoesusalltabsrais2019nrowslatlongmerge28k.head(3)


# In[19]:


bancoesusalltabsrais2019nrowslatlongmerge28k.to_csv('bancoesusalltabsrais2019nrowslatlongmerge28k.csv',sep=',',index=False)


# In[20]:


bancoesusalltabsrais2019nrowslatlongmerge28k.shape


# In[21]:


#https://stackoverflow.com/questions/43394450/pandas-mergehow-inner-result-is-bigger-than-both-dataframes


# In[24]:


#I have to drop duplicates on the columns (one of the columns at least)
#the merge way back made sense because only one data had duplicates in the cep column


# In[25]:


bancoesusalltabsrais2019nrowslatlongmerge28k


# In[26]:


bancoesusalltabsrais2019nrowslatlongmerge28k['cep']


# # I can't believe I could've merge the way in the beginning directly

# In[29]:


#it would've avoided a lot of stress, at least I read about big data, datatype, ray, pyspark, kaggle notebook, 
#dask, import by nrows, importing by chunksize, skipping rows by skiprows, skiprows=range(1,500000), etc, etc

#all because as I was trying to merge the columns on both datasets had duplicates, and the way I merge way back it didn't


# In[30]:


import pandas as pd 


# In[31]:


dfrow0to25425 = pd.read_excel('dfrow0to25425latlong.xlsx')


# In[32]:


dfrow0to25425


# In[33]:


dfrow0to25425.to_csv('dfrow0to25425latlong.csv', sep=',', index=False)


# # Finally the merge

# In[210]:


import pandas as pd


# In[211]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[212]:


dfrow0to25425.shape


# In[213]:


dfrow0to25425.head(3)


# In[214]:


dfrow0to25425['cep'].nunique()


# In[215]:


len(dfrow0to25425['cep'])


# In[216]:


len(dfrow0to25425['cep']) - dfrow0to25425['cep'].nunique()


# In[217]:


pd.set_option('display.max_rows', None)


# In[218]:


dfrow0to25425['cep']


# In[219]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[220]:


dfrow0to25425['cep']


# In[221]:


pd.set_option('display.max_rows', 100)


# In[222]:


#there's 10 duplicates after regex, and only these 10 duplicates is making the merge be 266k which is greated than 252K, the original dataset
#it's not, it's something else, before regex there was 11 duplicates


# In[223]:


#(dfrow0to25425['cep']).apply(lambda x: x.duplicated()).sum()


# In[224]:


dfrow0to25425.memory_usage()


# In[225]:


dfrow0to25425.info()


# In[226]:


dfrow0to25425.dtypes


# In[227]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[228]:


dfrow0to25425.dtypes


# In[229]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[230]:


dfrow0to25425['cep']


# In[231]:


len(dfrow0to25425['cep']) - dfrow0to25425['cep'].nunique()


# In[232]:


dfrow0to25425.shape


# In[235]:


dfrow0to25425.drop_duplicates('cep')


# In[236]:


dfrow0to25425 = dfrow0to25425.drop_duplicates('cep')


# In[237]:


dfrow0to25425


# In[265]:


dfrow0to25425['latitude'].isnull().sum()


# In[266]:


(7255/25415)*100


# In[267]:


#28.5% of latitudes were not found, that is 71.5% was found


# In[269]:


28.5+71.5


# In[238]:


bancoesusalltabsrais2019 = pd.read_csv('bancoesusalltabs_04012020to08052021rais2019.csv')


# In[239]:


bancoesusalltabsrais2019.shape


# In[240]:


bancoesusalltabsrais2019.head(3)


# In[241]:


bancoesusalltabsrais2019.info()


# In[242]:


bancoesusalltabsrais2019.memory_usage()


# In[243]:


bancoesusalltabsrais2019.dtypes


# In[244]:


bancoesusalltabsrais2019['cep'].dtypes


# In[245]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].astype(str)


# In[246]:


bancoesusalltabsrais2019['cep'].dtypes


# In[247]:


bancoesusalltabsrais2019['cep']


# In[190]:


#bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('\.0','',regex=True) 
#with this the merge drops to 5k, without it the merge is 224k
#because dfrow0to25425 had the .0 too
#after regex the merge went to 266k 
#because after the regex the dfrow0to25425 had duplicates


# In[248]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('\.0','',regex=True) 


# In[249]:


bancoesusalltabsrais2019['cep']


# In[250]:


bancoesusalltabsrais2019['cep'].dtype


# In[251]:


#pd.set_option('display.max_rows', None)


# In[252]:


#dfrow0to25425


# In[253]:


#pd.set_option('display.max_rows', 10)


# In[254]:


dfrow0to25425


# In[255]:


bancoesusalltabsrais2019latlong = bancoesusalltabsrais2019.merge(dfrow0to25425, how = 'inner', on = 'cep', indicator = '_merge2')


# In[256]:


bancoesusalltabsrais2019latlong.shape


# In[257]:


bancoesusalltabsrais2019latlong.head(3)


# In[258]:


bancoesusalltabsrais2019latlong.to_csv('bancoesusalltabsrais2019latlong.csv', sep=',', index=False)


# In[259]:


bancoesusalltabsrais2019latlong


# In[260]:


bancoesusalltabsrais2019latlong['latitude'].isnull().sum()


# In[261]:


((250216-70744)/(250216))*100


# In[263]:


(1-(70744/250216))*100


# In[270]:


((250216-70744)/(252397))*100 # not divided by 252k because 2k were empty cells in the original file


# In[272]:


((250216-70744)/(250432))*100


# In[ ]:


#check df empty cells on latitude and or duplicates 


# In[39]:


#but why the merge now had 224184, and not 236k like before when it was merged with cepbancoesusalltabsrais2019? 


# In[186]:


#cepbancoesusalltabsrais2019 = pd.read_excel('cepabancoesusalltabsrais2019.xlsx')


# In[ ]:





# In[273]:


bancoesusalltabsrais2019latlong


# In[275]:


bancoesusalltabsrais2019latlong['latitude'].isnull().sum()


# In[276]:


(70744/250216)*100 #missing latitude


# In[280]:


1 - (70744/250216) #71% has latitude


# In[281]:


dfrow0to25425['latitude'].isnull().sum()


# In[282]:


dfrow0to25425


# In[284]:


(7255/25415)*100 #28% missing latitude


# In[286]:


1 - (7255/25415) #71% latitude data


# In[287]:


#I can do better than that


# In[288]:


#find more latitude, then do the merge again all over, but now, if the same problems appear, I'll know how to solve it


# In[289]:


#actually this 71% can be the best there is, because the 21% missing latitude, might be because of wrong ceps


# In[290]:


#let's find out 


# In[294]:


dfrow0to25425.to_csv('dfrow0to25425latlong.csv', sep=',', index=False)


# # Finding more latitude that was not found

# In[2]:


import pandas as pd


# In[3]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[4]:


dfrow0to25425.head(3)


# In[5]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[6]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[7]:


dfrow0to25425.shape


# In[7]:


dfrow0to25425['cep']


# In[8]:


dfrow0to25425.sort_values('latitude')


# In[9]:


pd.set_option('display.max_rows',None)


# In[9]:


dfrow0to25425.sort_values('latitude')


# In[11]:


#resetindex, get the cep with NaN latitude and try to find them


# In[10]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[13]:


#dfrow0to25425.sort_values('latitude').reset_index()
#index 0 to 18159 not NaN for latitude and longitude 
#index 18160 to NaN for latitude and longitude


# In[11]:


dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[12]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[13]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[14]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[18]:


#then do concat dfrow0to18159notnan with dfrow18160to25414allnan


# In[15]:


dfrow18160to25414allnan


# In[20]:


#test with the first model if any can be found 


# In[21]:


#from 18160 to 20000 to test, if not the other model


# In[22]:


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


# In[23]:


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


# In[24]:


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
                "".join(["http://photon.komoot.io/api?q=", address, "&limit=1"])
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


# In[25]:


#from .base import CEPConverter
#from .strategies import CorreiosPhotonConverter


def cep_to_coords(cep: str, factory: CEPConverter = CorreiosPhotonConverter) -> dict:
    coordinates = factory()(cep)
    return coordinates


# In[26]:


pd.set_option('display.max_row', 10)


# In[27]:


dfrow18160to25414allnan


# In[28]:


dfrow18160to25414allnan.loc[18160:20000]


# In[29]:


id18160nanto20000 = dfrow18160to25414allnan.loc[18160:20000]


# In[30]:


id18160nanto20000 = id18160nanto20000[['cep']]


# In[31]:


id18160nanto20000


# In[32]:


id18160nanto20000.update("cep_to_coords('" + id18160nanto20000[['cep']].astype(str) + "'),")
print(id18160nanto20000)


# In[33]:


id18160nanto20000


# In[34]:


id18160nanto20000 = id18160nanto20000.loc[:,'cep']


# In[35]:


id18160nanto20000


# In[36]:


print(" ".join(id18160nanto20000))#.tolist()


# In[ ]:


#it took 4x the time, and still did not find any 
#I tested again with 10 


# In[ ]:


coordinatesid18160nanto20000 = cep_to_coords('55000000'), cep_to_coords('50000000'), cep_to_coords('53715410'), cep_to_coords('nan'), cep_to_coords('0'), cep_to_coords('54500000'), cep_to_coords('56306620'), cep_to_coords('48900400'), cep_to_coords('56314485'), cep_to_coords('56300000'), cep_to_coords('56330790'), cep_to_coords('12228700'), cep_to_coords('56308050'), cep_to_coords('56332720'), cep_to_coords('52091010'), cep_to_coords('50670500'), cep_to_coords('50720380'), cep_to_coords('53150410'), cep_to_coords('54700500'), cep_to_coords('54774300'), cep_to_coords('53000000'), cep_to_coords('53420230'), cep_to_coords('53429230'), cep_to_coords('55600000'), cep_to_coords('29722000'), cep_to_coords('50710470'), cep_to_coords('54080042'), cep_to_coords('51298412'), cep_to_coords('52020020'), cep_to_coords('55150000'), cep_to_coords('52020117'), cep_to_coords('52220705'), cep_to_coords('55640000'), cep_to_coords('53650575'), cep_to_coords('53350144'), cep_to_coords('54000580'), cep_to_coords('56230500'), cep_to_coords('53615772'), cep_to_coords('53600000'), cep_to_coords('52041915'), cep_to_coords('53110000'), cep_to_coords('21030500'), cep_to_coords('53121360'), cep_to_coords('51780000'), cep_to_coords('52051240'), cep_to_coords('53000600'), cep_to_coords('50090075'), cep_to_coords('50810777'), cep_to_coords('53180670'), cep_to_coords('53435610'), cep_to_coords('52020010'), cep_to_coords('50721170'), cep_to_coords('53082080'), cep_to_coords('50730670'), cep_to_coords('50780020'), cep_to_coords('52490300'), cep_to_coords('54759270'), cep_to_coords('51010210'), cep_to_coords('55296510'), cep_to_coords('55290000'), cep_to_coords('52211100'), cep_to_coords('91021100'), cep_to_coords('53010200'), cep_to_coords('50761070'), cep_to_coords('440648'), cep_to_coords('55810000'), cep_to_coords('52131300'), cep_to_coords('55555555'), cep_to_coords('52030170'), cep_to_coords('50725720'), cep_to_coords('50740170'), cep_to_coords('52221370'), cep_to_coords('54150561'), cep_to_coords('51250020'), cep_to_coords('53433090'), cep_to_coords('52071280'), cep_to_coords('53402793'), cep_to_coords('54910545'), cep_to_coords('5000000000'), cep_to_coords('99999999'), cep_to_coords('52190100'), cep_to_coords('50730210'), cep_to_coords('53170621'), cep_to_coords('54762484'), cep_to_coords('52041010'), cep_to_coords('54210390'), cep_to_coords('75101080'), cep_to_coords('54735110'), cep_to_coords('50360250'), cep_to_coords('52110000'), cep_to_coords('51010010'), cep_to_coords('54777510'), cep_to_coords('53125750'), cep_to_coords('51470190'), cep_to_coords('56900000'), cep_to_coords('50570020'), cep_to_coords('54071250'), cep_to_coords('52131000'), cep_to_coords('56330370'), cep_to_coords('50940920'), cep_to_coords('50791236'), cep_to_coords('54430314'), cep_to_coords('57976848'), cep_to_coords('50640040'), cep_to_coords('53690840'), cep_to_coords('52081030'), cep_to_coords('62060030'), cep_to_coords('53139226'), cep_to_coords('50720400'), cep_to_coords('50751370'), cep_to_coords('53402710'), cep_to_coords('51260590'), cep_to_coords('54580980'), cep_to_coords('50780185'), cep_to_coords('52291291'), cep_to_coords('50791480'), cep_to_coords('50129309'), cep_to_coords('52071250'), cep_to_coords('51240210'), cep_to_coords('54530012'), cep_to_coords('52070240'), cep_to_coords('50710730'), cep_to_coords('52041040'), cep_to_coords('51280415'), cep_to_coords('46277595'), cep_to_coords('54750000'), cep_to_coords('54745440'), cep_to_coords('54762380'), cep_to_coords('54762470'), cep_to_coords('54230222'), cep_to_coords('53150005'), cep_to_coords('53439400'), cep_to_coords('55610000'), cep_to_coords('52110145'), cep_to_coords('55886000'), cep_to_coords('52191100'), cep_to_coords('55810190'), cep_to_coords('52120200'), cep_to_coords('54240130'), cep_to_coords('51020512'), cep_to_coords('55038220'), cep_to_coords('54520295'), cep_to_coords('50730600'), cep_to_coords('53401260'), cep_to_coords('54000750'), cep_to_coords('54299899'), cep_to_coords('52660290'), cep_to_coords('52021240'), cep_to_coords('54535200'), cep_to_coords('54220470'), cep_to_coords('54280642'), cep_to_coords('54000010'), cep_to_coords('53170635'), cep_to_coords('53130230'), cep_to_coords('54000000'), cep_to_coords('54000800'), cep_to_coords('53203019'), cep_to_coords('52221170'), cep_to_coords('52041000'), cep_to_coords('52230000'), cep_to_coords('53405170'), cep_to_coords('56306385'), cep_to_coords('54052380'), cep_to_coords('54505904'), cep_to_coords('50731110'), cep_to_coords('53441510'), cep_to_coords('54720210'), cep_to_coords('54170430'), cep_to_coords('54280080'), cep_to_coords('53270430'), cep_to_coords('51003010'), cep_to_coords('50070450'), cep_to_coords('53298280'), cep_to_coords('52004030'), cep_to_coords('52051200'), cep_to_coords('51870080'), cep_to_coords('54170010'), cep_to_coords('54460000'), cep_to_coords('50316078'), cep_to_coords('53403610'), cep_to_coords('54762732'), cep_to_coords('53400000'), cep_to_coords('54530060'), cep_to_coords('56310710'), cep_to_coords('54150191'), cep_to_coords('56508195'), cep_to_coords('53040055'), cep_to_coords('56503380'), cep_to_coords('56508460'), cep_to_coords('56506480'), cep_to_coords('54100581'), cep_to_coords('56500000'), cep_to_coords('56503620'), cep_to_coords('56512180'), cep_to_coords('56503270'), cep_to_coords('56519360'), cep_to_coords('55814970'), cep_to_coords('54140033'), cep_to_coords('53370828'), cep_to_coords('53403245'), cep_to_coords('50640340'), cep_to_coords('54433025'), cep_to_coords('52230360'), cep_to_coords('50711110'), cep_to_coords('51000000'), cep_to_coords('54266004'), cep_to_coords('52291210'), cep_to_coords('50761260'), cep_to_coords('54735130'), cep_to_coords('53422630'), cep_to_coords('54450250'), cep_to_coords('53370140'), cep_to_coords('55292380'), cep_to_coords('54520260'), cep_to_coords('54510320'), cep_to_coords('52221380'), cep_to_coords('50830450'), cep_to_coords('54410640'), cep_to_coords('53000200'), cep_to_coords('55190000'), cep_to_coords('53070420'), cep_to_coords('55819640'), cep_to_coords('52071000'), cep_to_coords('51113000'), cep_to_coords('53409711'), cep_to_coords('52240620'), cep_to_coords('54513605'), cep_to_coords('54000500'), cep_to_coords('55825100'), cep_to_coords('52010065'), cep_to_coords('51335496'), cep_to_coords('50820050'), cep_to_coords('52020030'), cep_to_coords('54409500'), cep_to_coords('55018210'), cep_to_coords('54460090'), cep_to_coords('52130510'), cep_to_coords('53415310'), cep_to_coords('56318070'), cep_to_coords('50712170'), cep_to_coords('1111'), cep_to_coords('52221300'), cep_to_coords('56309150'), cep_to_coords('55024810'), cep_to_coords('53130080'), cep_to_coords('50630170'), cep_to_coords('56321625'), cep_to_coords('50100350'), cep_to_coords('54519160'), cep_to_coords('51028170'), cep_to_coords('53444480'), cep_to_coords('50789000'), cep_to_coords('55046640'), cep_to_coords('50900121'), cep_to_coords('54360103'), cep_to_coords('52210001'), cep_to_coords('56308150'), cep_to_coords('53110027'), cep_to_coords('52211600'), cep_to_coords('55604200'), cep_to_coords('53442120'), cep_to_coords('43535340'), cep_to_coords('54315310'), cep_to_coords('53421805'), cep_to_coords('53405310'), cep_to_coords('51000330'), cep_to_coords('55815206'), cep_to_coords('53402165'), cep_to_coords('53400990'), cep_to_coords('54445011'), cep_to_coords('54720020'), cep_to_coords('50731050'), cep_to_coords('51260520'), cep_to_coords('52021395'), cep_to_coords('50761062'), cep_to_coords('52080281'), cep_to_coords('53240290'), cep_to_coords('52160796'), cep_to_coords('52211110'), cep_to_coords('52051281'), cep_to_coords('53402660'), cep_to_coords('53050077'), cep_to_coords('55602970'), cep_to_coords('50710430'), cep_to_coords('51325280'), cep_to_coords('51027400'), cep_to_coords('52110580'), cep_to_coords('52110460'), cep_to_coords('50920370'), cep_to_coords('50930010'), cep_to_coords('55292780'), cep_to_coords('54160575'), cep_to_coords('50760220'), cep_to_coords('53150311'), cep_to_coords('54400450'), cep_to_coords('52280025'), cep_to_coords('50879470'), cep_to_coords('53620692'), cep_to_coords('55818620'), cep_to_coords('56510120'), cep_to_coords('50850410'), cep_to_coords('54210545'), cep_to_coords('52490008'), cep_to_coords('53580135'), cep_to_coords('42130140'), cep_to_coords('53401585'), cep_to_coords('51345000'), cep_to_coords('70459000'), cep_to_coords('50790425'), cep_to_coords('51250110'), cep_to_coords('50791230'), cep_to_coords('55400090'), cep_to_coords('50040560'), cep_to_coords('24121965'), cep_to_coords('54589555'), cep_to_coords('54160454'), cep_to_coords('55630370'), cep_to_coords('54250520'), cep_to_coords('51630060'), cep_to_coords('54517270'), cep_to_coords('54735200'), cep_to_coords('53520200'), cep_to_coords('53460390'), cep_to_coords('56512790'), cep_to_coords('53424080'), cep_to_coords('52015300'), cep_to_coords('50710380'), cep_to_coords('50470130'), cep_to_coords('52280367'), cep_to_coords('53266040'), cep_to_coords('54783170'), cep_to_coords('54404010'), cep_to_coords('53330420'), cep_to_coords('50731636'), cep_to_coords('50750165'), cep_to_coords('55299390'), cep_to_coords('55032555'), cep_to_coords('54520615'), cep_to_coords('52060140'), cep_to_coords('54530105'), cep_to_coords('53420100'), cep_to_coords('53040010'), cep_to_coords('56512050'), cep_to_coords('53370166'), cep_to_coords('52050110'), cep_to_coords('51230368'), cep_to_coords('53439390'), cep_to_coords('50751530'), cep_to_coords('52110380'), cep_to_coords('50050010'), cep_to_coords('52120040'), cep_to_coords('10503235'), cep_to_coords('54735133'), cep_to_coords('53580310'), cep_to_coords('55012312'), cep_to_coords('53444490'), cep_to_coords('52071210'), cep_to_coords('53270017'), cep_to_coords('25030090'), cep_to_coords('54406200'), cep_to_coords('52211150'), cep_to_coords('54460010'), cep_to_coords('53461564'), cep_to_coords('52110220'), cep_to_coords('52121140'), cep_to_coords('55608640'), cep_to_coords('50770390'), cep_to_coords('53040480'), cep_to_coords('53410000'), cep_to_coords('52770120'), cep_to_coords('53431300'), cep_to_coords('91882915'), cep_to_coords('51010378'), cep_to_coords('50000060'), cep_to_coords('50000740'), cep_to_coords('53439420'), cep_to_coords('54720250'), cep_to_coords('50021020'), cep_to_coords('53580351'), cep_to_coords('54444029'), cep_to_coords('54220716'), cep_to_coords('52060030'), cep_to_coords('53410130'), cep_to_coords('5010820'), cep_to_coords('50760550'), cep_to_coords('52081550'), cep_to_coords('54390071'), cep_to_coords('51490071'), cep_to_coords('54470757'), cep_to_coords('50920640'), cep_to_coords('54280744'), cep_to_coords('53130010'), cep_to_coords('52210415'), cep_to_coords('54150540'), cep_to_coords('54525260'), cep_to_coords('54500001'), cep_to_coords('53610071'), cep_to_coords('50670126'), cep_to_coords('53580400'), cep_to_coords('52070501'), cep_to_coords('53013003'), cep_to_coords('55027210'), cep_to_coords('54510450'), cep_to_coords('51283080'), cep_to_coords('52000013'), cep_to_coords('42803853'), cep_to_coords('54400080'), cep_to_coords('54420030'), cep_to_coords('51130090'), cep_to_coords('30100020'), cep_to_coords('52291021'), cep_to_coords('50020080'), cep_to_coords('54325670'), cep_to_coords('54530470'), cep_to_coords('50452526'), cep_to_coords('50020240'), cep_to_coords('53240670'), cep_to_coords('52050040'), cep_to_coords('54431600'), cep_to_coords('51030700'), cep_to_coords('53435140'), cep_to_coords('52061460'), cep_to_coords('54120272'), cep_to_coords('52060451'), cep_to_coords('50091051'), cep_to_coords('54080260'), cep_to_coords('55608251'), cep_to_coords('54116059'), cep_to_coords('51100060'), cep_to_coords('53402390'), cep_to_coords('54160449'), cep_to_coords('52120250'), cep_to_coords('55809560'), cep_to_coords('53620721'), cep_to_coords('50740705'), cep_to_coords('52114300'), cep_to_coords('50751555'), cep_to_coords('55027110'), cep_to_coords('53160740'), cep_to_coords('53403285'), cep_to_coords('54705378'), cep_to_coords('54580380'), cep_to_coords('54580000'), cep_to_coords('51150590'), cep_to_coords('50980625'), cep_to_coords('53160780'), cep_to_coords('55151680'), cep_to_coords('52100000'), cep_to_coords('52041110'), cep_to_coords('50230940'), cep_to_coords('52080110'), cep_to_coords('55813425'), cep_to_coords('54783660'), cep_to_coords('52000000'), cep_to_coords('56614316'), cep_to_coords('56506970'), cep_to_coords('52041300'), cep_to_coords('52020090'), cep_to_coords('53320541'), cep_to_coords('50740660'), cep_to_coords('54150420'), cep_to_coords('55173568'), cep_to_coords('55014090'), cep_to_coords('53401450'), cep_to_coords('52191585'), cep_to_coords('50711090'), cep_to_coords('50760600'), cep_to_coords('53520172'), cep_to_coords('5632811000'), cep_to_coords('55537000'), cep_to_coords('53120012'), cep_to_coords('52110627'), cep_to_coords('53433240'), cep_to_coords('50020545'), cep_to_coords('53625400'), cep_to_coords('54100000'), cep_to_coords('54792200'), cep_to_coords('50070605'), cep_to_coords('53425580'), cep_to_coords('55641735'), cep_to_coords('50000180'), cep_to_coords('54170160'), cep_to_coords('51030690'), cep_to_coords('50070280'), cep_to_coords('53150300'), cep_to_coords('53230110'), cep_to_coords('53130020'), cep_to_coords('54230077'), cep_to_coords('51240220'), cep_to_coords('50011000'), cep_to_coords('54700000'), cep_to_coords('52070235'), cep_to_coords('56500999'), cep_to_coords('56503420'), cep_to_coords('53560470'), cep_to_coords('54525350'), cep_to_coords('53330190'), cep_to_coords('50610971'), cep_to_coords('56502165'), cep_to_coords('52091230'), cep_to_coords('52160811'), cep_to_coords('53530786'), cep_to_coords('52061010'), cep_to_coords('52090622'), cep_to_coords('50710000'), cep_to_coords('50720390'), cep_to_coords('54110000'), cep_to_coords('52091026'), cep_to_coords('52131591'), cep_to_coords('55042050'), cep_to_coords('52111414'), cep_to_coords('53030026'), cep_to_coords('2000000000'), cep_to_coords('50080000'), cep_to_coords('53031100'), cep_to_coords('55295335'), cep_to_coords('54320330'), cep_to_coords('50860010'), cep_to_coords('53070620'), cep_to_coords('79649954'), cep_to_coords('56512540'), cep_to_coords('52131010'), cep_to_coords('56515700'), cep_to_coords('53437450'), cep_to_coords('54753976'), cep_to_coords('52130470'), cep_to_coords('50865041'), cep_to_coords('54325064'), cep_to_coords('50070580'), cep_to_coords('50070030'), cep_to_coords('25021220'), cep_to_coords('53437710'), cep_to_coords('53437260'), cep_to_coords('54120000'), cep_to_coords('50070590'), cep_to_coords('50980705'), cep_to_coords('54460020'), cep_to_coords('50980494'), cep_to_coords('53434729'), cep_to_coords('50790120'), cep_to_coords('56915899'), cep_to_coords('569000000'), cep_to_coords('52280440'), cep_to_coords('53637550'), cep_to_coords('54040240'), cep_to_coords('52120313'), cep_to_coords('54771410'), cep_to_coords('55640253'), cep_to_coords('55294936'), cep_to_coords('54530072'), cep_to_coords('53370298'), cep_to_coords('53428805'), cep_to_coords('53610345'), cep_to_coords('54325000'), cep_to_coords('52060111'), cep_to_coords('59111090'), cep_to_coords('54705183'), cep_to_coords('53370150'), cep_to_coords('55608676'), cep_to_coords('53565580'), cep_to_coords('52291570'), cep_to_coords('52061050'), cep_to_coords('52191400'), cep_to_coords('54517500'), cep_to_coords('53401775'), cep_to_coords('52171260'), cep_to_coords('51300161'), cep_to_coords('54589340'), cep_to_coords('55641420'), cep_to_coords('55643632'), cep_to_coords('54460310'), cep_to_coords('50500903'), cep_to_coords('53130000'), cep_to_coords('54530121'), cep_to_coords('54130121'), cep_to_coords('55602550'), cep_to_coords('52081020'), cep_to_coords('52490070'), cep_to_coords('54429050'), cep_to_coords('50790310'), cep_to_coords('55296000'), cep_to_coords('54296548'), cep_to_coords('52080000'), cep_to_coords('54762660'), cep_to_coords('54280010'), cep_to_coords('16020365'), cep_to_coords('50760004'), cep_to_coords('51190250'), cep_to_coords('55292446'), cep_to_coords('50721230'), cep_to_coords('55640040'), cep_to_coords('56509140'), cep_to_coords('53405380'), cep_to_coords('52080330'), cep_to_coords('53130530'), cep_to_coords('52050041'), cep_to_coords('54515150'), cep_to_coords('54024420'), cep_to_coords('55293320'), cep_to_coords('54715840'), cep_to_coords('51112957'), cep_to_coords('54576821'), cep_to_coords('55155010'), cep_to_coords('55290660'), cep_to_coords('54580305'), cep_to_coords('52041340'), cep_to_coords('54433480'), cep_to_coords('55818525'), cep_to_coords('52111230'), cep_to_coords('53471031'), cep_to_coords('55612271'), cep_to_coords('54135301'), cep_to_coords('55028220'), cep_to_coords('53409228'), cep_to_coords('53500000'), cep_to_coords('52050160'), cep_to_coords('53150009'), cep_to_coords('53050110'), cep_to_coords('54340000'), cep_to_coords('52121580'), cep_to_coords('52280733'), cep_to_coords('50764640'), cep_to_coords('52111621'), cep_to_coords('55604250'), cep_to_coords('12030730'), cep_to_coords('55103001'), cep_to_coords('52030520'), cep_to_coords('54762367'), cep_to_coords('50870490'), cep_to_coords('52050010'), cep_to_coords('54230555'), cep_to_coords('50771400'), cep_to_coords('56512680'), cep_to_coords('54505505'), cep_to_coords('55012484'), cep_to_coords('51110150'), cep_to_coords('54720200'), cep_to_coords('54440050'), cep_to_coords('43103901'), cep_to_coords('54753016'), cep_to_coords('54783000'), cep_to_coords('51370170'), cep_to_coords('53442090'), cep_to_coords('51170430'), cep_to_coords('56903910'), cep_to_coords('55604300'), cep_to_coords('56503440'), cep_to_coords('54774120'), cep_to_coords('50129301'), cep_to_coords('50129303'), cep_to_coords('17021958'), cep_to_coords('5501464'), cep_to_coords('52131380'), cep_to_coords('50720520'), cep_to_coords('52620015'), cep_to_coords('55152430'), cep_to_coords('55157010'), cep_to_coords('55152060'), cep_to_coords('52110131'), cep_to_coords('53540500'), cep_to_coords('54160350'), cep_to_coords('24910000'), cep_to_coords('50761730'), cep_to_coords('50343787'), cep_to_coords('52080270'), cep_to_coords('53530990'), cep_to_coords('54400440'), cep_to_coords('55157410'), cep_to_coords('54580830'), cep_to_coords('52041770'), cep_to_coords('50370020'), cep_to_coords('52210210'), cep_to_coords('53427450'), cep_to_coords('51240060'), cep_to_coords('51240106'), cep_to_coords('7760000'), cep_to_coords('53440070'), cep_to_coords('56912440'), cep_to_coords('56909350'), cep_to_coords('53423833'), cep_to_coords('53580360'), cep_to_coords('53421690'), cep_to_coords('54100405'), cep_to_coords('56506450'), cep_to_coords('55150520'), cep_to_coords('50751180'), cep_to_coords('52280120'), cep_to_coords('53220581'), cep_to_coords('56519160'), cep_to_coords('48904150'), cep_to_coords('52060120'), cep_to_coords('53046150'), cep_to_coords('55032000'), cep_to_coords('50390710'), cep_to_coords('52191020'), cep_to_coords('54450090'), cep_to_coords('53560200'), cep_to_coords('55038530'), cep_to_coords('65765574'), cep_to_coords('50730110'), cep_to_coords('54300260'), cep_to_coords('52211000'), cep_to_coords('48900000'), cep_to_coords('50050200'), cep_to_coords('56909484'), cep_to_coords('56308185'), cep_to_coords('55402956'), cep_to_coords('54510310'), cep_to_coords('53580730'), cep_to_coords('50670179'), cep_to_coords('55008520'), cep_to_coords('50760820'), cep_to_coords('54720011'), cep_to_coords('56912100'), cep_to_coords('55640292'), cep_to_coords('54517505'), cep_to_coords('52041540'), cep_to_coords('53510480'), cep_to_coords('55022510'), cep_to_coords('53120248'), cep_to_coords('52130715'), cep_to_coords('54515120'), cep_to_coords('52111141'), cep_to_coords('54280530'), cep_to_coords('54210010'), cep_to_coords('52130310'), cep_to_coords('53450000'), cep_to_coords('54315550'), cep_to_coords('56159230'), cep_to_coords('51011685'), cep_to_coords('52240030'), cep_to_coords('54515480'), cep_to_coords('53407265'), cep_to_coords('50600000'), cep_to_coords('55604070'), cep_to_coords('29071971'), cep_to_coords('53265464'), cep_to_coords('52071090'), cep_to_coords('55608380'), cep_to_coords('55612650'), cep_to_coords('21180020'), cep_to_coords('53550150'), cep_to_coords('53580000'), cep_to_coords('53413500'), cep_to_coords('55150150'), cep_to_coords('53407245'), cep_to_coords('53417070'), cep_to_coords('52081033'), cep_to_coords('56909720'), cep_to_coords('5690000'), cep_to_coords('52120540'), cep_to_coords('53610000'), cep_to_coords('52077290'), cep_to_coords('54325395'), cep_to_coords('55014005'), cep_to_coords('54150080'), cep_to_coords('52050030'), cep_to_coords('55554000'), cep_to_coords('56511160'), cep_to_coords('54100313'), cep_to_coords('53421760'), cep_to_coords('26079000'), cep_to_coords('51420080'), cep_to_coords('55154590'), cep_to_coords('53630070'), cep_to_coords('55031636'), cep_to_coords('54440680'), cep_to_coords('55816270'), cep_to_coords('50690430'), cep_to_coords('52130023'), cep_to_coords('52090000'), cep_to_coords('56508227'), cep_to_coords('55819970'), cep_to_coords('51203090'), cep_to_coords('52110430'), cep_to_coords('53554009'), cep_to_coords('56511060'), cep_to_coords('55292260'), cep_to_coords('56506000'), cep_to_coords('55292590'), cep_to_coords('55296520'), cep_to_coords('52090195'), cep_to_coords('54440072'), cep_to_coords('55298470'), cep_to_coords('52280252'), cep_to_coords('52120110'), cep_to_coords('55021395'), cep_to_coords('55540999'), cep_to_coords('55021330'), cep_to_coords('55296120'), cep_to_coords('54360168'), cep_to_coords('56308440'), cep_to_coords('51160449'), cep_to_coords('56900906'), cep_to_coords('56903230'), cep_to_coords('56900030'), cep_to_coords('53435010'), cep_to_coords('54777280'), cep_to_coords('52111155'), cep_to_coords('56504150'), cep_to_coords('55190380'), cep_to_coords('55031460'), cep_to_coords('55154070'), cep_to_coords('55179473'), cep_to_coords('55604130'), cep_to_coords('55604060'), cep_to_coords('52081032'), cep_to_coords('55112000'), cep_to_coords('55813900'), cep_to_coords('50761562'), cep_to_coords('55038565'), cep_to_coords('53630000'), cep_to_coords('50980000'), cep_to_coords('56913311'), cep_to_coords('57000000'), cep_to_coords('54230000'), cep_to_coords('53421640'), cep_to_coords('54703510'), cep_to_coords('52041320'), cep_to_coords('53405400'), cep_to_coords('53580760'), cep_to_coords('24735140'), cep_to_coords('56903660'), cep_to_coords('56907170'), cep_to_coords('55641810'), cep_to_coords('50500000'), cep_to_coords('52081010'), cep_to_coords('55644375'), cep_to_coords('53130090'), cep_to_coords('54330214'), cep_to_coords('54768847'), cep_to_coords('55604330'), cep_to_coords('54170051'), cep_to_coords('54360000'), cep_to_coords('56667000'), cep_to_coords('70000000'), cep_to_coords('50080681'), cep_to_coords('55195112'), cep_to_coords('50750000'), cep_to_coords('53405160'), cep_to_coords('56512250'), cep_to_coords('54100260'), cep_to_coords('53402680'), cep_to_coords('55019365'), cep_to_coords('54420161'), cep_to_coords('55194220'), cep_to_coords('52030181'), cep_to_coords('56308155'), cep_to_coords('54505970'), cep_to_coords('54505001'), cep_to_coords('53620049'), cep_to_coords('54210530'), cep_to_coords('54830570'), cep_to_coords('55044180'), cep_to_coords('55293970'), cep_to_coords('55296350'), cep_to_coords('5687000'), cep_to_coords('56784000'), cep_to_coords('53441206'), cep_to_coords('55100078'), cep_to_coords('52050170'), cep_to_coords('54210323'), cep_to_coords('52011890'), cep_to_coords('55643662'), cep_to_coords('55010740'), cep_to_coords('52030720'), cep_to_coords('50771330'), cep_to_coords('54230720'), cep_to_coords('50970445'), cep_to_coords('55034360'), cep_to_coords('51240120'), cep_to_coords('55294054'), cep_to_coords('52011126'), cep_to_coords('53170495'), cep_to_coords('53110730'), cep_to_coords('53407000'), cep_to_coords('55420380'), cep_to_coords('53510370'), cep_to_coords('53510330'), cep_to_coords('53560140'), cep_to_coords('53525580'), cep_to_coords('51011020'), cep_to_coords('56512140'), cep_to_coords('56512200'), cep_to_coords('55604360'), cep_to_coords('53437110'), cep_to_coords('54435325'), cep_to_coords('52131150'), cep_to_coords('50120310'), cep_to_coords('56654000'), cep_to_coords('52041570'), cep_to_coords('29061962'), cep_to_coords('54340280'), cep_to_coords('54280113'), cep_to_coords('56332125'), cep_to_coords('50900000'), cep_to_coords('56903090'), cep_to_coords('56912555'), cep_to_coords('56909050'), cep_to_coords('53150435'), cep_to_coords('54750050'), cep_to_coords('55604220'), cep_to_coords('55604040'), cep_to_coords('51170130'), cep_to_coords('52190010'), cep_to_coords('55024750'), cep_to_coords('50244000'), cep_to_coords('53580120'), cep_to_coords('54437230'), cep_to_coords('53550147'), cep_to_coords('53043318'), cep_to_coords('54580205'), cep_to_coords('53120190'), cep_to_coords('50740460'), cep_to_coords('50192301'), cep_to_coords('56433480'), cep_to_coords('50790400'), cep_to_coords('53130320'), cep_to_coords('54460140'), cep_to_coords('56506410'), cep_to_coords('54415100'), cep_to_coords('54080475'), cep_to_coords('55293050'), cep_to_coords('54406020'), cep_to_coords('52221000'), cep_to_coords('56503340'), cep_to_coords('54160060'), cep_to_coords('53405300'), cep_to_coords('52030050'), cep_to_coords('55190100'), cep_to_coords('52280190'), cep_to_coords('50741480'), cep_to_coords('55610460'), cep_to_coords('55602270'), cep_to_coords('56502000'), cep_to_coords('56516160'), cep_to_coords('55014325'), cep_to_coords('53580020'), cep_to_coords('53540202'), cep_to_coords('52221200'), cep_to_coords('51240550'), cep_to_coords('55644648'), cep_to_coords('54310160'), cep_to_coords('55042180'), cep_to_coords('52051390'), cep_to_coords('52390090'), cep_to_coords('55297812'), cep_to_coords('55030300'), cep_to_coords('54140450'), cep_to_coords('54320600'), cep_to_coords('53417020'), cep_to_coords('54980600'), cep_to_coords('52160445'), cep_to_coords('53429701'), cep_to_coords('53435590'), cep_to_coords('56622510'), cep_to_coords('54400082'), cep_to_coords('55299490'), cep_to_coords('53110300'), cep_to_coords('50607400'), cep_to_coords('54759051'), cep_to_coords('5549000'), cep_to_coords('55008190'), cep_to_coords('54517410'), cep_to_coords('53630065'), cep_to_coords('55604110'), cep_to_coords('53520173'), cep_to_coords('53585000'), cep_to_coords('24768796'), cep_to_coords('52068080'), cep_to_coords('56740040'), cep_to_coords('59250340'), cep_to_coords('55815180'), cep_to_coords('55495970'), cep_to_coords('52050210'), cep_to_coords('55644380'), cep_to_coords('53437844'), cep_to_coords('55024670'), cep_to_coords('56515710'), cep_to_coords('53320071'), cep_to_coords('56509310'), cep_to_coords('56512310'), cep_to_coords('55293200'), cep_to_coords('51290650'), cep_to_coords('54762748'), cep_to_coords('55196157'), cep_to_coords('55014132'), cep_to_coords('50780341'), cep_to_coords('54520290'), cep_to_coords('55042075'), cep_to_coords('55559000'), cep_to_coords('54505590'), cep_to_coords('54520675'), cep_to_coords('55042270'), cep_to_coords('55030010'), cep_to_coords('51260089'), cep_to_coords('54517370'), cep_to_coords('50020360'), cep_to_coords('54517490'), cep_to_coords('53210420'), cep_to_coords('50050060'), cep_to_coords('53470340'), cep_to_coords('52884003'), cep_to_coords('50751620'), cep_to_coords('50080785'), cep_to_coords('54792110'), cep_to_coords('55643678'), cep_to_coords('53620717'), cep_to_coords('52120031'), cep_to_coords('53520700'), cep_to_coords('55038180'), cep_to_coords('56504120'), cep_to_coords('53130150'), cep_to_coords('55291170'), cep_to_coords('54520100'), cep_to_coords('53180012'), cep_to_coords('53431005'), cep_to_coords('59000000'), cep_to_coords('53429070'), cep_to_coords('50160260'), cep_to_coords('56507970'), cep_to_coords('55617970'), cep_to_coords('54600000'), cep_to_coords('42700000'), cep_to_coords('53635785'), cep_to_coords('53520015'), cep_to_coords('53560070'), cep_to_coords('52081061'), cep_to_coords('59270685'), cep_to_coords('54505195'), cep_to_coords('50450590'), cep_to_coords('55191991'), cep_to_coords('53430250'), cep_to_coords('53580050'), cep_to_coords('54150030'), cep_to_coords('56503650'), cep_to_coords('56511340'), cep_to_coords('54420620'), cep_to_coords('56512261'), cep_to_coords('54325435'), cep_to_coords('51010215'), cep_to_coords('51010045'), cep_to_coords('55610105'), cep_to_coords('56503000'), cep_to_coords('55610014'), cep_to_coords('55606590'), cep_to_coords('52054260'), cep_to_coords('50720370'), cep_to_coords('56316784'), cep_to_coords('53419903'), cep_to_coords('75830000'), cep_to_coords('52071188'), cep_to_coords('51260550'), cep_to_coords('55877000'), cep_to_coords('56912280'), cep_to_coords('56906410'), cep_to_coords('55606820'), cep_to_coords('55604275'), cep_to_coords('55608111'), cep_to_coords('55018585'), cep_to_coords('53441216'), cep_to_coords('55028210'), cep_to_coords('55028120'), cep_to_coords('54230482'), cep_to_coords('5514000'), cep_to_coords('26200353'), cep_to_coords('53000060'), cep_to_coords('56503320'), cep_to_coords('55460970'), cep_to_coords('55819200'), cep_to_coords('53110741'), cep_to_coords('55643021'), cep_to_coords('54410000'), cep_to_coords('54520190'), cep_to_coords('54525241'), cep_to_coords('54510250'), cep_to_coords('54520015'), cep_to_coords('54510150'), cep_to_coords('54535170'), cep_to_coords('54520110'), cep_to_coords('54525025'), cep_to_coords('54762000'), cep_to_coords('56312675'), cep_to_coords('54110680'), cep_to_coords('55030171'), cep_to_coords('52071290'), cep_to_coords('55606815'), cep_to_coords('50761400'), cep_to_coords('50790001'), cep_to_coords('55040005'), cep_to_coords('52456850'), cep_to_coords('55612560'), cep_to_coords('55816000'), cep_to_coords('52291120'), cep_to_coords('54510230'), cep_to_coords('54440113'), cep_to_coords('52060160'), cep_to_coords('37410000'), cep_to_coords('54410430'), cep_to_coords('54505535'), cep_to_coords('55192642'), cep_to_coords('55192663'), cep_to_coords('53413154'), cep_to_coords('56316640'), cep_to_coords('53226371'), cep_to_coords('50020060'), cep_to_coords('55643010'), cep_to_coords('52071705'), cep_to_coords('56014111'), cep_to_coords('54280634'), cep_to_coords('52110510'), cep_to_coords('51021228'), cep_to_coords('55006360'), cep_to_coords('52032250'), cep_to_coords('55819650'), cep_to_coords('55892999'), cep_to_coords('54765340'), cep_to_coords('56318260'), cep_to_coords('55602160'), cep_to_coords('54275990'), cep_to_coords('55604010'), cep_to_coords('55602068'), cep_to_coords('52721160'), cep_to_coords('56503400'), cep_to_coords('23290150'), cep_to_coords('55643700'), cep_to_coords('50731090'), cep_to_coords('55037242'), cep_to_coords('51030171'), cep_to_coords('53413000'), cep_to_coords('52220110'), cep_to_coords('54732826'), cep_to_coords('52091407'), cep_to_coords('55026530'), cep_to_coords('55000001'), cep_to_coords('54510210'), cep_to_coords('54520000'), cep_to_coords('53409090'), cep_to_coords('54525135'), cep_to_coords('53405140'), cep_to_coords('55608430'), cep_to_coords('55194324'), cep_to_coords('50890270'), cep_to_coords('55270250'), cep_to_coords('52640070'), cep_to_coords('55295050'), cep_to_coords('56512090'), cep_to_coords('55506640'), cep_to_coords('50070020'), cep_to_coords('53635085'), cep_to_coords('55159899'), cep_to_coords('55612095'), cep_to_coords('56308210'), cep_to_coords('54410355'), cep_to_coords('51010820'), cep_to_coords('55602040'), cep_to_coords('53425430'), cep_to_coords('55608055'), cep_to_coords('55604490'), cep_to_coords('55027010'), cep_to_coords('55027350'), cep_to_coords('56309010'), cep_to_coords('55018360'), cep_to_coords('52051005'), cep_to_coords('53370257'), cep_to_coords('53370830'), cep_to_coords('55643098'), cep_to_coords('50120050'), cep_to_coords('53335431'), cep_to_coords('54510001'), cep_to_coords('53230443'), cep_to_coords('53236440'), cep_to_coords('55038540'), cep_to_coords('50741050'), cep_to_coords('54280704'), cep_to_coords('55608435'), cep_to_coords('56518899'), cep_to_coords('27235375'), cep_to_coords('54230101'), cep_to_coords('56903600'), cep_to_coords('52114432'), cep_to_coords('56310746'), cep_to_coords('54420020'), cep_to_coords('50140160'), cep_to_coords('50020090'), cep_to_coords('56906530'), cep_to_coords('56900100'), cep_to_coords('77060116'), cep_to_coords('5690653'), cep_to_coords('54705394'), cep_to_coords('54759602'), cep_to_coords('55125970'), cep_to_coords('15900000'), cep_to_coords('56328010'), cep_to_coords('54793230'), cep_to_coords('50710064'), cep_to_coords('50980450'), cep_to_coords('54762360'), cep_to_coords('55643327'), cep_to_coords('55643030'), cep_to_coords('55300000'), cep_to_coords('50081000'), cep_to_coords('55250420'), cep_to_coords('53030270'), cep_to_coords('53310020'), cep_to_coords('54720122'), cep_to_coords('54404800'), cep_to_coords('56610360'), cep_to_coords('51067060'), cep_to_coords('50751080'), cep_to_coords('56318380'), cep_to_coords('55613900'), cep_to_coords('55813280'), cep_to_coords('55817140'), cep_to_coords('55641350'), cep_to_coords('51430315'), cep_to_coords('55100027'), cep_to_coords('55026901'), cep_to_coords('55490970'), cep_to_coords('54720814'), cep_to_coords('52110210'), cep_to_coords('54020030'), cep_to_coords('83328260'), cep_to_coords('55027470'), cep_to_coords('55027990'), cep_to_coords('50200065'), cep_to_coords('54230221'), cep_to_coords('50208001'), cep_to_coords('52070032'), cep_to_coords('54440131'), cep_to_coords('54020310'), cep_to_coords('52019091'), cep_to_coords('55604155'), cep_to_coords('52470220'), cep_to_coords('56504525'), cep_to_coords('56503450'), cep_to_coords('56503451'), cep_to_coords('55293440'), cep_to_coords('55008160'), cep_to_coords('54340565'), cep_to_coords('56909512'), cep_to_coords('56700970'), cep_to_coords('52125320'), cep_to_coords('54789840'), cep_to_coords('55816410'), cep_to_coords('51160111'), cep_to_coords('51130370'), cep_to_coords('53640618'), cep_to_coords('53020617'), cep_to_coords('56505210'), cep_to_coords('56503260'), cep_to_coords('53630631'), cep_to_coords('55021265'), cep_to_coords('51860200'), cep_to_coords('55819030'), cep_to_coords('56308060'), cep_to_coords('53020120'), cep_to_coords('55298290'), cep_to_coords('50880010'), cep_to_coords('55643588'), cep_to_coords('71917360'), cep_to_coords('55819110'), cep_to_coords('50690610'), cep_to_coords('55031330'), cep_to_coords('54213692'), cep_to_coords('54100014'), cep_to_coords('52060561'), cep_to_coords('55024610'), cep_to_coords('56308140'), cep_to_coords('20091968'), cep_to_coords('55016755'), cep_to_coords('56505100'), cep_to_coords('58805230'), cep_to_coords('56503360'), cep_to_coords('55024500'), cep_to_coords('55042560'), cep_to_coords('53417420'), cep_to_coords('55014021'), cep_to_coords('56306660'), cep_to_coords('56000300'), cep_to_coords('55030460'), cep_to_coords('52120510'), cep_to_coords('51031480'), cep_to_coords('34360160'), cep_to_coords('56904090'), cep_to_coords('53200100'), cep_to_coords('55024590'), cep_to_coords('55550970'), cep_to_coords('55641970'), cep_to_coords('55642605'), cep_to_coords('55816450'), cep_to_coords('56903290'), cep_to_coords('50751170'), cep_to_coords('55330999'), cep_to_coords('55290340'), cep_to_coords('54520060'), cep_to_coords('50743360'), cep_to_coords('53020340'), cep_to_coords('55602710'), cep_to_coords('55604278'), cep_to_coords('52061100'), cep_to_coords('56519040'), cep_to_coords('32333323'), cep_to_coords('56517060'), cep_to_coords('55000190'), cep_to_coords('24474295'), cep_to_coords('54720035'), cep_to_coords('56306510'), cep_to_coords('55042210'), cep_to_coords('53230420'), cep_to_coords('53407330'), cep_to_coords('74567900'), cep_to_coords('50160233'), cep_to_coords('56330400'), cep_to_coords('55645030'), cep_to_coords('55643138'), cep_to_coords('56645030'), cep_to_coords('53150280'), cep_to_coords('56906480'), cep_to_coords('52044500'), cep_to_coords('54120010'), cep_to_coords('50912301'), cep_to_coords('56512130'), cep_to_coords('55040260'), cep_to_coords('56511310'), cep_to_coords('56507295'), cep_to_coords('56507255'), cep_to_coords('56519070'), cep_to_coords('56510100'), cep_to_coords('56509900'), cep_to_coords('56328030'), cep_to_coords('56505131'), cep_to_coords('56517450'), cep_to_coords('56334899'), cep_to_coords('4111968'), cep_to_coords('53900900'), cep_to_coords('54355040'), cep_to_coords('56912070'), cep_to_coords('54792560'), cep_to_coords('56519020'), cep_to_coords('53370092'), cep_to_coords('55022768'), cep_to_coords('55840999'), cep_to_coords('53580390'), cep_to_coords('53240410'), cep_to_coords('52417130'), cep_to_coords('50070330'), cep_to_coords('51355024'), cep_to_coords('53230360'), cep_to_coords('54762491'), cep_to_coords('53401250'), cep_to_coords('52030190'), cep_to_coords('55036280'), cep_to_coords('55010090'), cep_to_coords('56506675'), cep_to_coords('56506540'), cep_to_coords('55295400'), cep_to_coords('5500000000'), cep_to_coords('55018213'), cep_to_coords('53620133'), cep_to_coords('55030020'), cep_to_coords('55037110'), cep_to_coords('52131533'), cep_to_coords('53580540'), cep_to_coords('55155440'), cep_to_coords('55038145'), cep_to_coords('55151665'), cep_to_coords('52041480'), cep_to_coords('52030295'), cep_to_coords('56306498'), cep_to_coords('52130550'), cep_to_coords('55016565'), cep_to_coords('53402532'), cep_to_coords('52040770'), cep_to_coords('51560035'), cep_to_coords('55150550'), cep_to_coords('43990000'), cep_to_coords('51240410'), cep_to_coords('54510300'), cep_to_coords('53427360'), cep_to_coords('55151140'), cep_to_coords('56503280'), cep_to_coords('56510020'), cep_to_coords('56517500'), cep_to_coords('53640731'), cep_to_coords('51160910'), cep_to_coords('60000000'), cep_to_coords('54520130'), cep_to_coords('48601330'), cep_to_coords('50050975'), cep_to_coords('56316090'), cep_to_coords('53640425'), cep_to_coords('56509822'), cep_to_coords('56912400'), cep_to_coords('55016035'), cep_to_coords('53401180'), cep_to_coords('51203320'), cep_to_coords('50780580'), cep_to_coords('56306630'), cep_to_coords('50610010'), cep_to_coords('56506140'), cep_to_coords('56550358'), cep_to_coords('56512550'), cep_to_coords('55539800'), cep_to_coords('50720490'), cep_to_coords('54320720'), cep_to_coords('56512510'), cep_to_coords('50781740'), cep_to_coords('55642550'), cep_to_coords('55640001'), cep_to_coords('55006332'), cep_to_coords('55642680'), cep_to_coords('51121580'), cep_to_coords('54777553'), cep_to_coords('56306370'), cep_to_coords('55036202'), cep_to_coords('50040720'), cep_to_coords('56909651'), cep_to_coords('56330380'), cep_to_coords('52191360'), cep_to_coords('55190971'), cep_to_coords('50771016'), cep_to_coords('56512275'), cep_to_coords('53580045'), cep_to_coords('56332465'), cep_to_coords('55151740'), cep_to_coords('56328790'), cep_to_coords('56511010'), cep_to_coords('56517020'), cep_to_coords('54460449'), cep_to_coords('53180001'), cep_to_coords('56330122'), cep_to_coords('56303310'), cep_to_coords('50820403'), cep_to_coords('54705185'), cep_to_coords('56320810'), cep_to_coords('8111971'), cep_to_coords('55036025'), cep_to_coords('50110537'), cep_to_coords('53431830'), cep_to_coords('55641778'), cep_to_coords('55641075'), cep_to_coords('3244090'), cep_to_coords('54394103'), cep_to_coords('51230402'), cep_to_coords('53441201'), cep_to_coords('55155510'), cep_to_coords('55150005'), cep_to_coords('55152380'), cep_to_coords('50721755'), cep_to_coords('50721320'), cep_to_coords('54789835'), cep_to_coords('56512290'), cep_to_coords('3961030'), cep_to_coords('56395970'), cep_to_coords('54765360'), cep_to_coords('50791000'), cep_to_coords('56330360'), cep_to_coords('55606460'), cep_to_coords('50041055'), cep_to_coords('54780320'), cep_to_coords('54800992'), cep_to_coords('66666666'), cep_to_coords('55042090'), cep_to_coords('54510160'), cep_to_coords('54535330'), cep_to_coords('54580390'), cep_to_coords('55606803'), cep_to_coords('53421650'), cep_to_coords('52060200'), cep_to_coords('55607400'), cep_to_coords('55604380'), cep_to_coords('56000080'), cep_to_coords('52201220'), cep_to_coords('52221031'), cep_to_coords('52081300'), cep_to_coords('55196065'), cep_to_coords('21171260'), cep_to_coords('54768792'), cep_to_coords('56312808'), cep_to_coords('55644010'), cep_to_coords('52401550'), cep_to_coords('53620250'), cep_to_coords('54759102'), cep_to_coords('55610060'), cep_to_coords('3982000'), cep_to_coords('52110165'), cep_to_coords('53270431'), cep_to_coords('50050075'), cep_to_coords('54080490'), cep_to_coords('50790721'), cep_to_coords('50720560'), cep_to_coords('50400303'), cep_to_coords('54437120'), cep_to_coords('50770440'), cep_to_coords('52291000'), cep_to_coords('54520765'), cep_to_coords('26017000'), cep_to_coords('50760510'), cep_to_coords('52060310'), cep_to_coords('55154507'), cep_to_coords('55155050'), cep_to_coords('50806220'), cep_to_coords('52214060'), cep_to_coords('55602450'), cep_to_coords('56435435'), cep_to_coords('53409110'), cep_to_coords('52070635'), cep_to_coords('55040140'), cep_to_coords('56507340'), cep_to_coords('52280210'), cep_to_coords('50711050'), cep_to_coords('55297035'), cep_to_coords('54330590'), cep_to_coords('54240900'), cep_to_coords('50600100'), cep_to_coords('55151635'), cep_to_coords('52291600'), cep_to_coords('55612235'), cep_to_coords('52120245'), cep_to_coords('54230085'), cep_to_coords('54762400'), cep_to_coords('54517485'), cep_to_coords('54552035'), cep_to_coords('50050100'), cep_to_coords('54530130'), cep_to_coords('54517245'), cep_to_coords('54505170'), cep_to_coords('54580636'), cep_to_coords('54670380'), cep_to_coords('55195249'), cep_to_coords('54150680'), cep_to_coords('54210080'), cep_to_coords('55191692'), cep_to_coords('54440081'), cep_to_coords('54170641'), cep_to_coords('55620010'), cep_to_coords('55604020'), cep_to_coords('56903260'), cep_to_coords('54360040'), cep_to_coords('56903248'), cep_to_coords('50721570'), cep_to_coords('53580700'), cep_to_coords('55157346'), cep_to_coords('55597979'), cep_to_coords('55157250'), cep_to_coords('55155070'), cep_to_coords('53280080'), cep_to_coords('55293220'), cep_to_coords('54240440'), cep_to_coords('56515200'), cep_to_coords('52280220'), cep_to_coords('56304020'), cep_to_coords('50730290'), cep_to_coords('54762224'), cep_to_coords('54720293'), cep_to_coords('53620330'), cep_to_coords('56000800'), cep_to_coords('54571100'), cep_to_coords('54762642'), cep_to_coords('55044070'), cep_to_coords('54470140'), cep_to_coords('55608420'), cep_to_coords('55444110'), cep_to_coords('52111020'), cep_to_coords('54520530'), cep_to_coords('54430240'), cep_to_coords('54410274'), cep_to_coords('50400600'), cep_to_coords('55606640'), cep_to_coords('53450390'), cep_to_coords('54270222'), cep_to_coords('55641340'), cep_to_coords('55024158'), cep_to_coords('55645152'), cep_to_coords('55642145'), cep_to_coords('51023210'), cep_to_coords('5340000'), cep_to_coords('50942019'), cep_to_coords('55014161'), cep_to_coords('53480120'), cep_to_coords('53825000'), cep_to_coords('55295230'), cep_to_coords('55290630'), cep_to_coords('55036050'), cep_to_coords('56332010'), cep_to_coords('50700300'), cep_to_coords('51010680'), cep_to_coords('54510122'), cep_to_coords('51052020'), cep_to_coords('55641400'), cep_to_coords('55645000'), cep_to_coords('54505585'), cep_to_coords('55819190'), cep_to_coords('51330008'), cep_to_coords('52291076'), cep_to_coords('53420150'), cep_to_coords('52061115'), cep_to_coords('51203910'), cep_to_coords('51761058'), cep_to_coords('53560640'), cep_to_coords('54170090'), cep_to_coords('56332450'), cep_to_coords('54270420'), cep_to_coords('50053000'), cep_to_coords('56516100'), cep_to_coords('55155411'), cep_to_coords('52111623'), cep_to_coords('50192309'), cep_to_coords('55290385'), cep_to_coords('55299385'), cep_to_coords('55290493'), cep_to_coords('55294000'), cep_to_coords('55220294'), cep_to_coords('55296035'), cep_to_coords('56515420'), cep_to_coords('53400701'), cep_to_coords('56551140'), cep_to_coords('50123013'), cep_to_coords('55604440'), cep_to_coords('50721360'), cep_to_coords('52061480'), cep_to_coords('54440020'), cep_to_coords('58912190'), cep_to_coords('52071255'), cep_to_coords('48306347'), cep_to_coords('56303347'), cep_to_coords('55641150'), cep_to_coords('55642160'), cep_to_coords('56318360'), cep_to_coords('54589200'), cep_to_coords('71324870'), cep_to_coords('56909370'), cep_to_coords('55019035'), cep_to_coords('50240000'), cep_to_coords('52130205'), cep_to_coords('52913291'), cep_to_coords('55643000'), cep_to_coords('50515005'), cep_to_coords('52231295'), cep_to_coords('51030210'), cep_to_coords('55024272'), cep_to_coords('50865130'), cep_to_coords('55152450'), cep_to_coords('550000000'), cep_to_coords('54735755'), cep_to_coords('55290360'), cep_to_coords('55259000'), cep_to_coords('55294520'), cep_to_coords('56517030'), cep_to_coords('56328120'), cep_to_coords('55014450'), cep_to_coords('55295150'), cep_to_coords('53340470'), cep_to_coords('54220131'), cep_to_coords('50409610'), cep_to_coords('55643640'), cep_to_coords('50070340'), cep_to_coords('50731272'), cep_to_coords('56515410'), cep_to_coords('50960430'), cep_to_coords('50761190'), cep_to_coords('54230640'), cep_to_coords('53630494'), cep_to_coords('54735796'), cep_to_coords('55150021'), cep_to_coords('50030590'), cep_to_coords('55666666'), cep_to_coords('55034561'), cep_to_coords('55036220'), cep_to_coords('56503090'), cep_to_coords('53404000'), cep_to_coords('53416590'), cep_to_coords('53409750'), cep_to_coords('52111624'), cep_to_coords('51300441'), cep_to_coords('53620020'), cep_to_coords('54330756'), cep_to_coords('55293270'), cep_to_coords('55296060'), cep_to_coords('55306054'), cep_to_coords('56512220'), cep_to_coords('56503675'), cep_to_coords('55042340'), cep_to_coords('56318010'), cep_to_coords('54762600'), cep_to_coords('53625020'), cep_to_coords('53330010'), cep_to_coords('53422460'), cep_to_coords('50060360'), cep_to_coords('54400230'), cep_to_coords('56312887'), cep_to_coords('53525712'), cep_to_coords('53011040'), cep_to_coords('54753700'), cep_to_coords('53140820'), cep_to_coords('53422070'), cep_to_coords('55026610'), cep_to_coords('50370170'), cep_to_coords('56328970'), cep_to_coords('54340015'), cep_to_coords('55297799'), cep_to_coords('50881040'), cep_to_coords('53405180'), cep_to_coords('54150193'), cep_to_coords('56310666'), cep_to_coords('43253534'), cep_to_coords('56070040'), cep_to_coords('54767455'), cep_to_coords('55021260'), cep_to_coords('55020425'), cep_to_coords('52020320'), cep_to_coords('50600700'), cep_to_coords('51230193'), cep_to_coords('54420201'), cep_to_coords('53415536'), cep_to_coords('51120183'), cep_to_coords('50741460'), cep_to_coords('55293600'), cep_to_coords('55299400'), cep_to_coords('55296080'), cep_to_coords('50822140'), cep_to_coords('53420416'), cep_to_coords('55641740'), cep_to_coords('64018018'), cep_to_coords('51022400'), cep_to_coords('23121212'), cep_to_coords('55002971'), cep_to_coords('54100170'), cep_to_coords('49035000'), cep_to_coords('54505541'), cep_to_coords('54450210'), cep_to_coords('51002130'), cep_to_coords('50680285'), cep_to_coords('42342342'), cep_to_coords('52510530'), cep_to_coords('54765125'), cep_to_coords('54510170'), cep_to_coords('53420110'), cep_to_coords('54781300'), cep_to_coords('50741510'), cep_to_coords('55610100'), cep_to_coords('50090785'), cep_to_coords('54519100'), cep_to_coords('56903320'), cep_to_coords('51260580'), cep_to_coords('51480580'), cep_to_coords('52010060'), cep_to_coords('55606800'), cep_to_coords('53610181'), cep_to_coords('52280370'), cep_to_coords('51203102'), cep_to_coords('56308090'), cep_to_coords('54160210'), cep_to_coords('50641200'), cep_to_coords('56332615'), cep_to_coords('51323329'), cep_to_coords('55038650'), cep_to_coords('55298175'), cep_to_coords('52081290'), cep_to_coords('55170800'), cep_to_coords('53010390'), cep_to_coords('55028133'), cep_to_coords('53477100'), cep_to_coords('56312000'), cep_to_coords('56312261'), cep_to_coords('53610620'), cep_to_coords('54712350'), cep_to_coords('55602170'), cep_to_coords('55155020'), cep_to_coords('56904110'), cep_to_coords('42334234'), cep_to_coords('50791487'), cep_to_coords('55036340'), cep_to_coords('74768015'), cep_to_coords('50340200'), cep_to_coords('56800330'), cep_to_coords('56512340'), cep_to_coords('56503224'), cep_to_coords('55640091'), cep_to_coords('51100000'), cep_to_coords('55642520'), cep_to_coords('54789355'), cep_to_coords('55606140'), cep_to_coords('56331020'), cep_to_coords('51335040'), cep_to_coords('55914642'), cep_to_coords('50790250'), cep_to_coords('26583660'), cep_to_coords('53200037'), cep_to_coords('53150045'), cep_to_coords('5450000'), cep_to_coords('53409050'), cep_to_coords('50050090'), cep_to_coords('54535290'), cep_to_coords('53009000'), cep_to_coords('96213002'), cep_to_coords('54762750'), cep_to_coords('52721775'), cep_to_coords('58753080'), cep_to_coords('52191555'), cep_to_coords('52132103'), cep_to_coords('54150560'), cep_to_coords('50760020'), cep_to_coords('54765236'), cep_to_coords('55866000'), cep_to_coords('54580465'), cep_to_coords('53180315'), cep_to_coords('54510340'), cep_to_coords('55606593'), cep_to_coords('55606230'), cep_to_coords('56330270'), cep_to_coords('52052130'), cep_to_coords('51011038'), cep_to_coords('51345170'), cep_to_coords('56503146'), cep_to_coords('53806700'), cep_to_coords('53341090'), cep_to_coords('53436460'), cep_to_coords('55642558'), cep_to_coords('53370158'), cep_to_coords('53550045'), cep_to_coords('54400600'), cep_to_coords('50640020'), cep_to_coords('54756356'), cep_to_coords('54768460'), cep_to_coords('54320626'), cep_to_coords('56465666'), cep_to_coords('50690222'), cep_to_coords('56313010'), cep_to_coords('50630209'), cep_to_coords('55293290'), cep_to_coords('56302440'), cep_to_coords('55190404'), cep_to_coords('55036567'), cep_to_coords('56312225'), cep_to_coords('53402786'), cep_to_coords('53250000'), cep_to_coords('50912309'), cep_to_coords('51260670'), cep_to_coords('56302460')


# In[37]:


coordinatesid18160nanto20000 = cep_to_coords('55000000'), cep_to_coords('50000000'), cep_to_coords('53715410'), cep_to_coords('nan'), cep_to_coords('0'), cep_to_coords('54500000'), cep_to_coords('56306620'), cep_to_coords('48900400'),cep_to_coords('56314485'), cep_to_coords('56300000')


# In[38]:


print(coordinatesid18160nanto20000)


# In[39]:


#it took much longer time, and it did not find any latitude and longitude as before with all other ceps


# In[40]:


#need another way to find them 


# In[41]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=55000000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[42]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=50000000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[43]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=50000000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[44]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=53715410"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[45]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=54500000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[49]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=55036340"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[48]:


#Although cepaberto was part of the model to find latitude and longitude from the cep, 
#many ceps that were not found in the model, was found here individually
#like the example above


# In[54]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=53409050"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[1]:


import requests
url = f"https://www.cepaberto.com/api/v3/cep?cep={55036340}"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[58]:


import requests
cep = {55036340,53409050}
url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[ ]:





# In[ ]:





# In[ ]:


import requests
url = f"https://www.cepaberto.com/api/v3/cep?cep={55036340}"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[33]:


import time


# In[47]:


import requests
start = 0
stop = 5
for j in range(start, stop):
    cep = dfrow18160to25414allnan['cep'].iloc[j]
    url = "https://www.cepaberto.com/api/v3/cep?cep="
    url = uri + str(cep)
    # O seu token está visível apenas pra você
    headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
    response = requests.get(url, headers=headers)
    #time.sleep(1.5)
    print(response.json())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[65]:


lat_long = []
lat_long = pd.DataFrame(lat_long)
'''
start= 3702   #defina o CEP de início
stop= 6000 #defina o CEP final
'''
start= 0   #defina o CEP de início
stop= 100
for j in range(start,stop):
            cep = dfrow18160to25414allnan["cep"].iloc[j] #selecionando coluna que possui o CEP
            uri = "https://www.cepaberto.com/api/v3/cep?cep="
            url = uri+str(cep)
            '''
            headers = {'Authorization': 'Token token= seu token'}
            '''
            headers = {'Authorization':'Token token=d8e540d0700d405acc0496142c5be3d2'}
            response = requests.get(url, headers=headers)
            
            json_string = str(response.json())
            '''
            json_string = json_string.replace("\'Praça D\'", "\"Praça D*")
            json_string = json_string.replace("Bloco D\'", "Bloco D\"")
            json_string = json_string.replace("\'Quadra D\'", "\"Quadra D\"")
            json_string = json_string.replace("\'Rua Projetada D\'", "\"Rua Projetada D\"")
            json_string = json_string.replace("\'Rua D\'", "\"Rua D\"")
            json_string = json_string.replace("Nº 624 \"A\"", "Nº 624 *A*")
            json_string = json_string.replace("\'Rua Nova Esperança-D\'", "\"Rua Nova Esperança-D\"")
            json_string = json_string.replace("Avenida D\'", "Avenida D\"")
            json_string = json_string.replace("Rua Quatro, 2\"B\"", "Rua Quatro, 2*B*")
            json_string = json_string.replace("d\'aguas", "d*aguas")
            json_string = json_string.replace("Local D\'", "Local D\"")
            json_string = json_string.replace("D\'", "D*")
            json_string = json_string.replace("Qd\'", "Qd*")
            '''
            json_string = json_string.replace("\'", "\"")
            a_json = json.loads(json_string)
            dataframe = pd.DataFrame.from_dict(a_json, orient="index")
            dataframe = dataframe.transpose()
            lat_long= pd.concat([lat_long, dataframe])
            #time.sleep(1.5)

lat_long.to_csv(f"cep_url_aberto_{start}_{stop}.csv")


# In[42]:


dfrow18160to25414allnan


# In[ ]:





# In[71]:


from time import time

start = time()
#your code goes here
dfrow18160to25414allnan.nunique() #this line is just an example
print(f'Time taken to run: {time() - start} seconds')


# In[73]:


#https://www.google.com/search?q=time+it+takes+for+a+code+to+run&oq=time+it+takes+for+a+code+to+run&aqs=chrome..69i57j33i160.5259j0j15&sourceid=chrome&ie=UTF-8


# In[72]:


dfrow18160to25414allnan.nunique() 


# In[ ]:





# In[ ]:





# In[61]:


import json


# In[68]:


import requests
cep = [{55036340, 53409050}]
uri = "https://www.cepaberto.com/api/v3/cep?cep="
url = uri + str(cep)
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
#time.sleep(1.5)
#print(response.json('{}'))
print(json.loads(response))
data = [json.loads(line) for line in open('data.json', 'r')]


# In[ ]:





# In[ ]:





# In[78]:


import requests
cep = 55036340
uri = f"https://www.cepaberto.com/api/v3/cep?cep="
url = uri+str(cep)
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[ ]:





# In[87]:


import requests
url = 'https://www.cepaberto.com/api/v3/cep?cep=55036340'
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[89]:


longlat = pd.read_excel("cepstestgooglemaps.xlsx")


# In[91]:


longlat


# In[96]:


longlat['cep'].astype(str).str.replace('\.0','', regex=True)


# In[101]:


longlat['cep'] = longlat['cep'].astype(str).str.replace('\.0','', regex=True)


# In[102]:


longlat


# In[103]:


import geopy
import pandas as pd

longlat = pd.read_excel("cepstestgooglemaps.xlsx")
geolocator = geopy.Nominatim(user_agent="check_1")

def get_zip_code(x):
    location = geolocator.reverse("{}, {}".format(x['LATITUDE_X'],x['LONGITUDE_X']))
    return location.raw['address']['postcode']
longlat['cep'] = longlat.head().apply(lambda x: get_zip_code(x), axis = 1)
print(longlat.head())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## so close to automating it to many ceps, but didn't work  

# In[104]:


import requests
cep = 55036340
uri = f"https://www.cepaberto.com/api/v3/cep?cep="
url = uri+str(cep)
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)
print(response.json())


# In[ ]:





# In[ ]:





# # using manoel's code for the remaining ceps

# In[507]:


import pandas as pd


# In[508]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[509]:


dfrow0to25425.head(3)


# In[510]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[511]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[512]:


dfrow0to25425.shape


# In[513]:


dfrow0to25425['cep']


# In[514]:


dfrow0to25425.sort_values('latitude')


# In[515]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[516]:


dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[517]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[518]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[519]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[520]:


dfrow18160to25414allnan


# In[521]:


dfrow18160to25414allnan[18160:19001]


# In[522]:


dfrow18160to25414allnan[:841]


# # dfrow18160to25414allnan_18160to19000

# In[523]:


dfrow18160to25414allnan_18160to19000 = dfrow18160to25414allnan[:841]


# In[299]:


#dfrow18160to25414allnan.drop('level_0', axis=1,inplace=True)


# In[300]:


#dfrow18160to25414allnan.sort_values('latitude').reset_index()[18160:19001]


# In[524]:


dfrow18160to25414allnan_18160to19000


# In[525]:


dfrow18160to25414allnan_18160to19000 = dfrow18160to25414allnan_18160to19000[['cep']]


# In[303]:


#some errors occured I'll use just 10 rows to test it again 


# In[304]:


#dfrow18160to25414allnan[:10]


# In[305]:


#dfrow18160to25414allnan_18160to1869 = dfrow18160to25414allnan[:10]


# In[526]:


dfrow18160to25414allnan_18160to19000


# In[229]:


#dfrow18160to25414allnan_18160to1869 = dfrow18160to25414allnan_18160to1869[['cep']]


# In[230]:


#dfrow18160to25414allnan_18160to1869 


# In[259]:


#dfrow18160to25414allnan_18160to1869 


# In[527]:


#dfrow18160to25414allnan_18160to19000[0:10]


# In[357]:


#dfrow18160to25414allnan_18160to19000.reset_index(inplace=True)


# In[358]:


#dfrow18160to25414allnan_18160to19000


# In[359]:


#dfrow18160to25414allnan_18160to19000.drop('index',axis=1,inplace=True)


# In[528]:


dfrow18160to25414allnan_18160to19000


# In[361]:


#ceps = dfrow18160to25414allnan_18160to19000


# In[362]:


#ceps


# In[529]:


dfrow18160to25414allnan_18160to19000


# In[531]:


ceps = dfrow18160to25414allnan_18160to19000


# In[532]:


ceps


# In[364]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[478]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 18160 #define the start CEP
stop= 19000 #define the final CEP
block = 40 #number of tabs opened

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[479]:


df_lat_long.shape


# In[480]:


df_lat_long


# In[481]:


base_ceps = df_lat_long


# In[482]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 840 #define the final CEP

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[483]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[462]:


#df_lat_long.reset_index()


# In[463]:


#df_lat_long.reset_index(inplace=True)


# In[486]:


#df_lat_long.to_csv('dfrow18160to25414allnan_18160to19000.csv', sep=',',index = False)


# In[495]:


df_lat_long


# In[499]:


df_lat_long.reset_index(level=0, inplace = True)


# In[533]:


df_lat_long


# In[502]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[534]:


df_lat_long


# In[535]:


df_lat_long.to_csv('dfrow18160to25414allnan_18160to19000.csv', sep=',', index = False)


# In[546]:


dfrow18160to25414allnan_18160to19000 = pd.read_csv('dfrow18160to25414allnan_18160to19000.csv')


# In[547]:


dfrow18160to25414allnan_18160to19000


# In[548]:


ceps


# In[540]:


ceps.reset_index(level=0, inplace = True)


# In[542]:


ceps.rename({'index':'cepsindex'}, axis=1,inplace=True)


# In[543]:


ceps


# In[549]:


dfrow18160to25414allnan_18160to19000['cepsindex'] = ceps['cepsindex']


# In[550]:


dfrow18160to25414allnan_18160to19000


# In[552]:


dfrow18160to25414allnan_18160to19000['lat'].isnull().sum()


# In[555]:


dfrow18160to25414allnan_18160to19000['lat'].value_counts()


# In[556]:


dfrow18160to25414allnan_18160to19000.to_csv('dfrow18160to25414allnan_18160to19000.csv',sep=',', index=False)


# In[557]:


dfrow18160to25414allnan_18160to19000 = pd.read_csv('dfrow18160to25414allnan_18160to19000.csv')


# In[558]:


dfrow18160to25414allnan_18160to19000 


# # dfrow18160to25414allnan_19000to20000

# In[559]:


#the last one stopped at 18999


# In[1]:


import pandas as pd


# In[2]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[3]:


dfrow0to25425.head(3)


# In[4]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[5]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[6]:


dfrow0to25425.shape


# In[7]:


dfrow0to25425['cep']


# In[8]:


dfrow0to25425.sort_values('latitude')


# In[9]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[10]:


pd.set_option('display.max_rows',None)


# In[12]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[13]:


pd.set_option('display.max_rows',10)


# In[15]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[16]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[17]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[18]:


dfrow18160to25414allnan


# In[19]:


dfrow18160to25414allnan[840:1841]


# In[20]:


dfrow18160to25414allnan_19000to20000 = dfrow18160to25414allnan[840:1841]


# In[21]:


dfrow18160to25414allnan_19000to20000 = dfrow18160to25414allnan_19000to20000[['cep']]


# In[22]:


dfrow18160to25414allnan_19000to20000


# In[23]:


ceps = dfrow18160to25414allnan_19000to20000


# In[24]:


ceps


# In[25]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[592]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 19000 #define the start CEP
stop= 20000 #define the final CEP #has to be the last index of the rows
block = 25 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[593]:


df_lat_long.shape


# In[594]:


df_lat_long


# In[595]:


base_ceps = df_lat_long


# In[596]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1000 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[597]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[598]:


df_lat_long.reset_index(level=0, inplace = True)


# In[599]:


df_lat_long


# In[600]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[601]:


df_lat_long


# In[602]:


df_lat_long.to_csv('dfrow18160to25414allnan_19000to19999.csv', sep=',', index = False)


# In[603]:


dfrow18160to25414allnan_19000to19999 = pd.read_csv('dfrow18160to25414allnan_19000to19999.csv')


# In[604]:


dfrow18160to25414allnan_19000to19999


# In[605]:


ceps


# In[606]:


ceps.reset_index(level=0, inplace = True)


# In[607]:


ceps.rename({'index':'cepsindex'}, axis=1,inplace=True)


# In[608]:


ceps


# In[609]:


dfrow18160to25414allnan_19000to19999['cepsindex'] = ceps['cepsindex']


# In[610]:


dfrow18160to25414allnan_19000to19999


# In[611]:


dfrow18160to25414allnan_19000to19999['lat'].isnull().sum()


# In[612]:


dfrow18160to25414allnan_19000to19999['lat'].value_counts()


# In[617]:


dfrow18160to25414allnan_19000to19999['cepsindex'].dtypes


# In[618]:


dfrow18160to25414allnan_19000to19999['cepsindex'] + 19000


# In[619]:


dfrow18160to25414allnan_19000to19999['cepsindex']  = dfrow18160to25414allnan_19000to19999['cepsindex'] + 19000


# In[620]:


dfrow18160to25414allnan_19000to19999


# In[622]:


dfrow18160to25414allnan_19000to20000


# In[621]:


ceps


# In[623]:


dfrow18160to25414allnan_19000to19999.to_csv('dfrow18160to25414allnan_19000to19999.csv',sep=',', index=False)


# In[125]:


dfrow18160to25414allnan_19000to19999 = pd.read_csv('dfrow18160to25414allnan_19000to19999.csv')


# In[126]:


dfrow18160to25414allnan_19000to19999


# # dfrow18160to25414allnan_20000to20999

# In[26]:


#the last one stopped at 19999


# In[27]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[28]:


dfrow0to25425.shape


# In[29]:


dfrow0to25425.head(3)


# In[30]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[31]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[32]:


dfrow0to25425['cep']


# In[33]:


dfrow0to25425.sort_values('latitude')


# In[34]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[35]:


pd.set_option('display.max_rows',None)


# In[36]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[37]:


pd.set_option('display.max_rows',10)


# In[38]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[39]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[40]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[41]:


dfrow18160to25414allnan


# In[44]:


dfrow18160to25414allnan[1840:2841]


# In[45]:


dfrow18160to25414allnan_19999to20999 = dfrow18160to25414allnan[1840:2841]


# In[46]:


dfrow18160to25414allnan_19999to20999 = dfrow18160to25414allnan_19999to20999[['cep']]


# In[47]:


dfrow18160to25414allnan_19999to20999


# In[48]:


ceps = dfrow18160to25414allnan_19999to20999


# In[49]:


ceps


# In[50]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[51]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 20000 #define the start CEP
stop= 21000 #define the final CEP #has to be the last index of the rows
block = 25 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[52]:


df_lat_long.shape


# In[53]:


df_lat_long


# In[54]:


base_ceps = df_lat_long


# In[55]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1000 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[56]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[57]:


df_lat_long.reset_index(level=0, inplace = True)


# In[58]:


df_lat_long


# In[59]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[81]:


df_lat_long


# In[82]:


df_lat_long.to_csv('dfrow18160to25414allnan_20000to20999.csv', sep=',', index = False)


# In[83]:


dfrow18160to25414allnan_20000to20999 = pd.read_csv('dfrow18160to25414allnan_20000to20999.csv')


# In[84]:


dfrow18160to25414allnan_20000to20999


# In[85]:


ceps


# In[65]:


ceps.reset_index(level=0, inplace = True)


# In[66]:


ceps.rename({'index':'cepsindex'}, axis=1,inplace=True)


# In[67]:


ceps


# In[108]:


dfrow18160to25414allnan_20000to20999['cepsindex'] = ceps['cepsindex']


# In[109]:


dfrow18160to25414allnan_20000to20999


# In[110]:


dfrow18160to25414allnan_20000to20999['lat'].isnull().sum()


# In[111]:


dfrow18160to25414allnan_20000to20999['lat'].value_counts()


# In[112]:


dfrow18160to25414allnan_20000to20999['cepsindex'].dtypes


# In[113]:


dfrow18160to25414allnan_20000to20999['cepsindex'] + 20000


# In[114]:


dfrow18160to25414allnan[1839:2841]


# In[115]:


dfrow18160to25414allnan_20000to20999


# In[116]:


dfrow18160to25414allnan_20000to20999['cepsindex']  = dfrow18160to25414allnan_20000to20999['cepsindex'] + 20000


# In[118]:


dfrow18160to25414allnan_20000to20999


# In[119]:


dfrow18160to25414allnan[1840:2840]


# In[120]:


ceps


# In[121]:


dfrow18160to25414allnan_20000to20999.to_csv('dfrow18160to25414allnan_20000to20999.csv', sep=',', index = False)


# In[122]:


dfrow18160to25414allnan_20000to20999 = pd.read_csv('dfrow18160to25414allnan_20000to20999.csv')


# In[123]:


dfrow18160to25414allnan_20000to20999 


# # dfrow18160to25414allnan_21000to21999

# In[124]:


#the last one stopped at 20999


# In[127]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[128]:


dfrow0to25425


# In[129]:


dfrow0to25425.head(3)


# In[130]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[131]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[132]:


dfrow0to25425['cep']


# In[133]:


dfrow0to25425.sort_values('latitude')


# In[134]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[135]:


pd.set_option('display.max_rows',None)


# In[136]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[137]:


pd.set_option('display.max_rows',10)


# In[138]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[139]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[140]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[141]:


dfrow18160to25414allnan


# In[143]:


dfrow18160to25414allnan[2840:3841]


# In[144]:


dfrow18160to25414allnan_21000to21999 = dfrow18160to25414allnan[2840:3841]


# In[146]:


dfrow18160to25414allnan_21000to21999 = dfrow18160to25414allnan_21000to21999[['cep']]


# In[147]:


dfrow18160to25414allnan_21000to21999


# In[148]:


ceps = dfrow18160to25414allnan_21000to21999


# In[149]:


ceps


# In[150]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[152]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 21000 #define the start CEP
stop= 22000 #define the final CEP #has to be the last index of the rows
block = 25 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[153]:


df_lat_long.shape


# In[154]:


df_lat_long


# In[155]:


base_ceps = df_lat_long


# In[156]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1000 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[157]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[158]:


df_lat_long.reset_index(level=0, inplace = True)


# In[159]:


df_lat_long


# In[160]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[161]:


df_lat_long


# In[162]:


df_lat_long.to_csv('dfrow18160to25414allnan_21000to21999.csv', sep=',', index = False)


# In[163]:


dfrow18160to25414allnan_21000to21999 = pd.read_csv('dfrow18160to25414allnan_21000to21999.csv')


# In[164]:


dfrow18160to25414allnan_21000to21999


# In[165]:


ceps


# In[166]:


ceps.reset_index(level=0, inplace = True)


# In[167]:


ceps.rename({'index':'cepsindex'}, axis=1,inplace=True)


# In[168]:


ceps


# In[169]:


dfrow18160to25414allnan_21000to21999['cepsindex'] = ceps['cepsindex']


# In[170]:


dfrow18160to25414allnan_21000to21999['lat'].isnull().sum()


# In[171]:


dfrow18160to25414allnan_21000to21999['lat'].value_counts()


# In[172]:


dfrow18160to25414allnan_21000to21999['cepsindex'].dtypes


# In[173]:


dfrow18160to25414allnan_21000to21999['cepsindex'] + 20000


# In[174]:


dfrow18160to25414allnan[2839:3841]


# In[175]:


dfrow18160to25414allnan_21000to21999


# In[180]:


dfrow18160to25414allnan_21000to21999['cepsindex']  = dfrow18160to25414allnan_21000to21999['cepsindex'] + 21000


# In[182]:


dfrow18160to25414allnan_21000to21999


# In[183]:


dfrow18160to25414allnan[2839:3841]


# In[184]:


ceps


# In[185]:


dfrow18160to25414allnan_21000to21999.to_csv('dfrow18160to25414allnan_21000to21999.csv', sep=',', index = False)


# In[186]:


dfrow18160to25414allnan_21000to21999 = pd.read_csv('dfrow18160to25414allnan_21000to21999.csv')


# In[187]:


dfrow18160to25414allnan_21000to21999


# # dfrow18160to25414allnan_22000to22999

# In[151]:


#the last one stopped at 21999


# In[188]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[189]:


dfrow0to25425


# In[190]:


dfrow0to25425.head(3)


# In[191]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[192]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[193]:


dfrow0to25425['cep']


# In[194]:


dfrow0to25425.sort_values('latitude')


# In[195]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[196]:


pd.set_option('display.max_rows',None)


# In[197]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[198]:


pd.set_option('display.max_rows',10)


# In[199]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[200]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[201]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[202]:


dfrow18160to25414allnan


# In[204]:


dfrow18160to25414allnan[3840:4841]


# In[205]:


dfrow18160to25414allnan_22000to22999 = dfrow18160to25414allnan[3840:4841]


# In[206]:


dfrow18160to25414allnan_22000to22999 = dfrow18160to25414allnan_22000to22999[['cep']]


# In[207]:


dfrow18160to25414allnan_22000to22999


# In[208]:


ceps = dfrow18160to25414allnan_22000to22999


# In[213]:


ceps


# In[214]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[215]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 22000 #define the start CEP
stop= 23000 #define the final CEP #has to be the last index of the rows
block = 25 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[216]:


df_lat_long.shape


# In[217]:


df_lat_long


# In[218]:


base_ceps = df_lat_long


# In[219]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1000 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[220]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[221]:


df_lat_long.reset_index(level=0, inplace = True)


# In[222]:


df_lat_long


# In[223]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[224]:


df_lat_long


# In[225]:


df_lat_long.to_csv('dfrow18160to25414allnan_22000to22999.csv', sep=',', index = False)


# In[226]:


dfrow18160to25414allnan_22000to22999 = pd.read_csv('dfrow18160to25414allnan_22000to22999.csv')


# In[227]:


dfrow18160to25414allnan_22000to22999


# In[228]:


ceps 


# In[229]:


ceps.reset_index(level=0, inplace = True)


# In[230]:


ceps.rename({'index':'cepsindex'}, axis=1,inplace=True)


# In[231]:


ceps


# In[232]:


dfrow18160to25414allnan_22000to22999['cepsindex'] = ceps['cepsindex']


# In[233]:


dfrow18160to25414allnan_22000to22999['lat'].isnull().sum()


# In[234]:


dfrow18160to25414allnan_22000to22999['lat'].value_counts()


# In[235]:


dfrow18160to25414allnan_22000to22999['cepsindex'].dtypes


# In[236]:


dfrow18160to25414allnan_22000to22999['cepsindex'] + 22000


# In[237]:


dfrow18160to25414allnan[3840:4841]


# In[238]:


dfrow18160to25414allnan_22000to22999


# In[239]:


dfrow18160to25414allnan_22000to22999['cepsindex']  = dfrow18160to25414allnan_22000to22999['cepsindex'] + 22000


# In[240]:


dfrow18160to25414allnan_22000to22999


# In[241]:


dfrow18160to25414allnan[3840:4841]


# In[242]:


ceps


# In[243]:


dfrow18160to25414allnan_22000to22999


# In[244]:


dfrow18160to25414allnan_22000to22999.to_csv('dfrow18160to25414allnan_22000to22999.csv', sep=',', index = False)


# In[245]:


dfrow18160to25414allnan_22000to22999 = pd.read_csv('dfrow18160to25414allnan_22000to22999.csv')


# In[246]:


dfrow18160to25414allnan_22000to22999


# # dfrow18160to25414allnan_23000to23999

# In[211]:


#the last one stopped at 22999


# In[247]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[248]:


dfrow0to25425


# In[249]:


dfrow0to25425.head(3)


# In[250]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[251]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[252]:


dfrow0to25425['cep']


# In[253]:


dfrow0to25425.sort_values('latitude')


# In[254]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[255]:


pd.set_option('display.max_rows',None)


# In[256]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[257]:


pd.set_option('display.max_rows',10)


# In[258]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[259]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[260]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[261]:


dfrow18160to25414allnan


# In[262]:


dfrow18160to25414allnan[4840:5841]


# In[263]:


dfrow18160to25414allnan_23000to23999 = dfrow18160to25414allnan[4840:5841]


# In[264]:


dfrow18160to25414allnan_23000to23999 = dfrow18160to25414allnan_23000to23999[['cep']]


# In[265]:


dfrow18160to25414allnan_23000to23999


# In[266]:


ceps = dfrow18160to25414allnan_23000to23999


# In[267]:


ceps


# In[268]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[269]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 23000 #define the start CEP
stop= 24000 #define the final CEP #has to be the last index of the rows
block = 25 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[270]:


df_lat_long.shape


# In[271]:


df_lat_long


# In[272]:


base_ceps = df_lat_long


# In[273]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1000 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[274]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[275]:


df_lat_long.reset_index(level=0, inplace = True)


# In[276]:


df_lat_long


# In[277]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[278]:


df_lat_long


# In[279]:


df_lat_long.to_csv('dfrow18160to25414allnan_23000to23999.csv', sep=',', index = False)


# In[280]:


dfrow18160to25414allnan_23000to23999 = pd.read_csv('dfrow18160to25414allnan_23000to23999.csv')


# In[281]:


dfrow18160to25414allnan_23000to23999


# In[282]:


ceps 


# In[283]:


ceps.reset_index(level=0, inplace = True)


# In[284]:


ceps.rename({'index':'cepsindex'}, axis=1,inplace=True)


# In[285]:


ceps


# In[286]:


dfrow18160to25414allnan_23000to23999['cepsindex'] = ceps['cepsindex']


# In[287]:


dfrow18160to25414allnan_23000to23999['lat'].isnull().sum()


# In[288]:


dfrow18160to25414allnan_23000to23999['lat'].value_counts()


# In[289]:


dfrow18160to25414allnan_23000to23999['cepsindex'].dtypes


# In[290]:


dfrow18160to25414allnan_23000to23999['cepsindex'] + 23000


# In[291]:


dfrow18160to25414allnan[4840:5841]


# In[292]:


dfrow18160to25414allnan_23000to23999


# In[293]:


dfrow18160to25414allnan_23000to23999['cepsindex']  = dfrow18160to25414allnan_23000to23999['cepsindex'] + 23000


# In[294]:


dfrow18160to25414allnan_23000to23999


# In[295]:


dfrow18160to25414allnan[4840:5841]


# In[296]:


ceps


# In[297]:


dfrow18160to25414allnan_23000to23999


# In[298]:


dfrow18160to25414allnan_23000to23999.to_csv('dfrow18160to25414allnan_23000to23999.csv', sep=',', index = False)


# In[299]:


dfrow18160to25414allnan_23000to23999 = pd.read_csv('dfrow18160to25414allnan_23000to23999.csv')


# In[300]:


dfrow18160to25414allnan_23000to23999


# # dfrow18160to25414allnan_24000to24999

# In[1]:


#the last one stopped at 23999


# In[3]:


import pandas as pd


# In[4]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[5]:


dfrow0to25425


# In[6]:


dfrow0to25425.head(3)


# In[7]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[8]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[9]:


dfrow0to25425['cep']


# In[10]:


dfrow0to25425.sort_values('latitude')


# In[11]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[12]:


pd.set_option('display.max_rows',None)


# In[13]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[14]:


pd.set_option('display.max_rows',10)


# In[15]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[16]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[17]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[18]:


dfrow18160to25414allnan


# In[21]:


dfrow18160to25414allnan[5840:6841]


# In[22]:


dfrow18160to25414allnan_24000to24999 = dfrow18160to25414allnan[5840:6841]


# In[23]:


dfrow18160to25414allnan_24000to24999 = dfrow18160to25414allnan_24000to24999[['cep']]


# In[24]:


dfrow18160to25414allnan_24000to24999


# In[25]:


ceps = dfrow18160to25414allnan_24000to24999


# In[26]:


ceps


# In[27]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[ ]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 24000 #define the start CEP
stop= 25000 #define the final CEP #has to be the last index of the rows
block = 25 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[29]:


df_lat_long.shape


# In[30]:


df_lat_long


# In[31]:


base_ceps = df_lat_long


# In[32]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1000 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[33]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[34]:


df_lat_long.reset_index(level=0, inplace = True)


# In[35]:


df_lat_long


# In[36]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[37]:


df_lat_long


# In[38]:


df_lat_long.to_csv('dfrow18160to25414allnan_24000to24999.csv', sep=',', index = False)


# In[39]:


dfrow18160to25414allnan_24000to24999 = pd.read_csv('dfrow18160to25414allnan_24000to24999.csv')


# In[40]:


dfrow18160to25414allnan_24000to24999


# In[41]:


ceps


# In[43]:


ceps.reset_index(level=0,inplace=True)


# In[46]:


ceps.rename({'index':'cepsindex'}, axis=1, inplace=True)


# In[47]:


ceps


# In[48]:


dfrow18160to25414allnan_24000to24999['cepsindex'] = ceps['cepsindex']


# In[49]:


dfrow18160to25414allnan_24000to24999['lat'].isnull().sum()


# In[50]:


dfrow18160to25414allnan_24000to24999['lat'].value_counts()


# In[51]:


dfrow18160to25414allnan_24000to24999['cepsindex'].dtypes


# In[52]:


dfrow18160to25414allnan_24000to24999['cepsindex'] + 24000


# In[53]:


dfrow18160to25414allnan[5840:6841]


# In[54]:


dfrow18160to25414allnan_24000to24999


# In[55]:


dfrow18160to25414allnan_24000to24999['cepsindex']  = dfrow18160to25414allnan_24000to24999['cepsindex'] + 24000


# In[56]:


dfrow18160to25414allnan_24000to24999


# In[57]:


dfrow18160to25414allnan_24000to24999


# In[58]:


dfrow18160to25414allnan[5840:6841]


# In[59]:


ceps


# In[60]:


dfrow18160to25414allnan_24000to24999


# In[61]:


dfrow18160to25414allnan_24000to24999.to_csv('dfrow18160to25414allnan_24000to24999.csv', sep=',', index = False)


# In[62]:


dfrow18160to25414allnan_24000to24999 = pd.read_csv('dfrow18160to25414allnan_24000to24999.csv')


# In[63]:


dfrow18160to25414allnan_24000to24999


# # dfrow18160to25414allnan_25000to25414

# In[65]:


#the last one stopped at 24999


# In[66]:


import pandas as pd


# In[67]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[68]:


dfrow0to25425


# In[69]:


dfrow0to25425.head(3)


# In[70]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[71]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[72]:


dfrow0to25425['cep']


# In[73]:


dfrow0to25425.sort_values('latitude')


# In[74]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[75]:


pd.set_option('display.max_rows',None)


# In[76]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[77]:


pd.set_option('display.max_rows',10)


# In[78]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[79]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[80]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[81]:


dfrow18160to25414allnan


# In[92]:


dfrow18160to25414allnan[6840:7255]


# In[93]:


dfrow18160to25414allnan_25000to25414 = dfrow18160to25414allnan[6840:7255]


# In[94]:


dfrow18160to25414allnan_25000to25414 = dfrow18160to25414allnan_25000to25414[['cep']]


# In[95]:


dfrow18160to25414allnan_25000to25414


# In[96]:


ceps = dfrow18160to25414allnan_25000to25414


# In[97]:


ceps


# In[98]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[99]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 25000 #define the start CEP
stop= 25414 #define the final CEP #has to be the last index of the rows
block = 23 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['cep'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['cep'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[100]:


df_lat_long.shape


# In[101]:


df_lat_long


# In[102]:


base_ceps = df_lat_long


# In[104]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 414 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[105]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[106]:


df_lat_long.reset_index(level=0, inplace = True)


# In[107]:


df_lat_long


# In[108]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[119]:


df_lat_long


# In[120]:


df_lat_long.to_csv('dfrow18160to25414allnan_25000to25414.csv', sep=',', index = False)


# In[121]:


dfrow18160to25414allnan_25000to25414 = pd.read_csv('dfrow18160to25414allnan_25000to25414.csv')


# In[122]:


dfrow18160to25414allnan_25000to25414


# In[123]:


ceps


# In[114]:


ceps.reset_index(level=0,inplace=True)


# In[115]:


ceps.rename({'index':'cepsindex'}, axis=1, inplace=True)


# In[124]:


ceps


# In[125]:


dfrow18160to25414allnan_25000to25414['cepsindex'] = ceps['cepsindex']


# In[126]:


dfrow18160to25414allnan_25000to25414['lat'].isnull().sum()


# In[127]:


dfrow18160to25414allnan_25000to25414['lat'].value_counts()


# In[128]:


dfrow18160to25414allnan_25000to25414['cepsindex'].dtypes


# In[129]:


dfrow18160to25414allnan_25000to25414['cepsindex'] + 25000


# In[130]:


dfrow18160to25414allnan[6840:7255]


# In[131]:


dfrow18160to25414allnan_25000to25414


# In[132]:


dfrow18160to25414allnan_25000to25414['cepsindex']  = dfrow18160to25414allnan_25000to25414['cepsindex'] + 24000


# In[133]:


dfrow18160to25414allnan_25000to25414


# In[134]:


dfrow18160to25414allnan[6840:7255]


# In[135]:


ceps


# In[ ]:


#the last row is missing copy row 25414 (the last row) from dfrow18160to25414allnan and add it to 
#row 414 of dfrow18160to25414allnan_25000to25414


# In[140]:


dfrow18160to25414allnan[7254:]


# In[177]:


df2 = dfrow18160to25414allnan[7254:]


# In[178]:


df2


# In[179]:


df2.drop({'level_0','index'}, axis=1, inplace=True)


# In[180]:


df2


# In[181]:


df2.reset_index(level=0, inplace=True)


# In[182]:


df2


# In[183]:


df2.rename({'index':'cepsindex'}, axis = 1 , inplace = True)


# In[184]:


df2


# In[185]:


df2[df2.columns[[1,2,3,4,0]]]


# In[186]:


df2 = df2[df2.columns[[1,2,3,4,0]]]


# In[187]:


dfrow18160to25414allnan_25000to25414


# In[188]:


df2['id'] = df2['id'].astype(str)


# In[189]:


df2


# In[190]:


df2['id'].str.replace('252350','414')


# In[191]:


df2['id'] = df2['id'].str.replace('252350','414')


# In[192]:


df2


# In[193]:


df2['id'] = df2['id'].astype(int)


# In[194]:


df2.dtypes


# In[195]:


df2


# In[197]:


df2.rename({'latitude':'lat', 'longitude':'long'},axis=1,inplace=True)


# In[198]:


df2


# In[196]:


dfrow18160to25414allnan_25000to25414


# In[199]:


dfrow18160to25414allnan_25000to25414.append(df2)


# In[201]:


dfrow18160to25414allnan_25000to25414 = dfrow18160to25414allnan_25000to25414.append(df2)


# In[203]:


dfrow18160to25414allnan_25000to25414.reset_index()


# In[205]:


dfrow18160to25414allnan_25000to25414 = dfrow18160to25414allnan_25000to25414.reset_index()


# In[206]:


dfrow18160to25414allnan_25000to25414


# In[208]:


dfrow18160to25414allnan_25000to25414.drop('index', axis=1, inplace = True)


# In[209]:


dfrow18160to25414allnan_25000to25414


# In[210]:


dfrow18160to25414allnan_25000to25414.to_csv('dfrow18160to25414allnan_25000to25414.csv', sep=',', index = False)


# In[211]:


dfrow18160to25414allnan_25000to25414 = pd.read_csv('dfrow18160to25414allnan_25000to25414.csv')


# In[212]:


dfrow18160to25414allnan_25000to25414


# # concat all dfs dfrow18160to25414allnan

# In[1]:


import pandas as pd


# In[2]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[3]:


dfrow0to25425


# In[4]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str)


# In[5]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].str.replace('\.0','',regex=True) 


# In[6]:


dfrow0to25425.sort_values('latitude')


# In[7]:


dfrow0to25425.sort_values('latitude').reset_index()


# In[8]:


dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[9]:


dfrow0to18159notnan = dfrow0to25425.sort_values('latitude').reset_index()[:18160]


# In[10]:


dfrow18160to25414allnan = dfrow0to25425.sort_values('latitude').reset_index()[18160:]


# In[11]:


dfrow0to18159notnan 


# In[14]:


dfrow18160to25414allnan_18160to19000 = pd.read_csv('dfrow18160to25414allnan_18160to19000.csv')


# In[15]:


dfrow18160to25414allnan_18160to19000


# In[16]:


dfrow18160to25414allnan_19000to19999 = pd.read_csv('dfrow18160to25414allnan_19000to19999.csv')


# In[17]:


dfrow18160to25414allnan_19000to19999


# In[18]:


dfrow18160to25414allnan_20000to20999 = pd.read_csv('dfrow18160to25414allnan_20000to20999.csv')


# In[19]:


dfrow18160to25414allnan_20000to20999


# In[20]:


dfrow18160to25414allnan_21000to21999 = pd.read_csv('dfrow18160to25414allnan_21000to21999.csv')


# In[21]:


dfrow18160to25414allnan_21000to21999


# In[22]:


dfrow18160to25414allnan_22000to22999 = pd.read_csv('dfrow18160to25414allnan_22000to22999.csv')


# In[23]:


dfrow18160to25414allnan_22000to22999


# In[24]:


dfrow18160to25414allnan_23000to23999 = pd.read_csv('dfrow18160to25414allnan_23000to23999.csv')


# In[25]:


dfrow18160to25414allnan_23000to23999


# In[26]:


dfrow18160to25414allnan_24000to24999 = pd.read_csv('dfrow18160to25414allnan_24000to24999.csv')


# In[27]:


dfrow18160to25414allnan_24000to24999 


# In[28]:


dfrow18160to25414allnan_25000to25414 = pd.read_csv('dfrow18160to25414allnan_25000to25414.csv')


# In[29]:


dfrow18160to25414allnan_25000to25414 


# In[31]:


pd.concat([dfrow18160to25414allnan_18160to19000,dfrow18160to25414allnan_19000to19999,dfrow18160to25414allnan_20000to20999,dfrow18160to25414allnan_21000to21999,dfrow18160to25414allnan_22000to22999,dfrow18160to25414allnan_23000to23999,dfrow18160to25414allnan_24000to24999,dfrow18160to25414allnan_25000to25414])


# In[32]:


dfrow18160to25414allnan_latlong = pd.concat([dfrow18160to25414allnan_18160to19000,dfrow18160to25414allnan_19000to19999,dfrow18160to25414allnan_20000to20999,dfrow18160to25414allnan_21000to21999,dfrow18160to25414allnan_22000to22999,dfrow18160to25414allnan_23000to23999,dfrow18160to25414allnan_24000to24999,dfrow18160to25414allnan_25000to25414])


# In[33]:


dfrow18160to25414allnan_latlong


# In[34]:


pd.set_option('display.max_rows',None)


# In[35]:


dfrow18160to25414allnan_latlong


# In[36]:


pd.set_option('display.max_rows',10)


# In[37]:


dfrow18160to25414allnan_latlong


# In[42]:


dfrow18160to25414allnan_latlong.drop('id',axis=1,inplace=True)


# In[43]:


dfrow18160to25414allnan_latlong


# In[45]:


dfrow18160to25414allnan_latlong = dfrow18160to25414allnan_latlong.reset_index()


# In[47]:


dfrow18160to25414allnan_latlong.drop('index',axis=1,inplace=True)


# In[48]:


dfrow18160to25414allnan_latlong


# In[49]:


dfrow18160to25414allnan_latlong.to_csv('dfrow18160to25414allnan_latlong.csv',index=False)


# In[38]:


dfrow0to18159notnan


# In[50]:


dfrow0to18159notnan.drop(['level_0','index','id'],axis=1,inplace=True)


# In[51]:


dfrow0to18159notnan


# In[53]:


dfrow0to18159notnan.reset_index(inplace=True)


# In[54]:


dfrow0to18159notnan


# In[55]:


dfrow0to18159notnan.rename({'index':'cepsindex'},axis=1,inplace=True)


# In[56]:


dfrow0to18159notnan


# In[57]:


dfrow0to18159notnan[dfrow0to18159notnan.columns[[1,2,3,0]]]


# In[58]:


dfrow0to18159notnan = dfrow0to18159notnan[dfrow0to18159notnan.columns[[1,2,3,0]]]


# In[59]:


dfrow0to18159notnan


# In[60]:


dfrow18160to25414allnan_latlong


# In[64]:


dfrow18160to25414allnan_latlong['cep'].astype(str).replace('\.0','',regex=True)


# In[65]:


dfrow18160to25414allnan_latlong['cep'] = dfrow18160to25414allnan_latlong['cep'].astype(str).replace('\.0','',regex=True)


# In[67]:


dfrow18160to25414allnan_latlong.rename({'lat':'latitude','long':'longitude'},axis=1,inplace=True)


# In[68]:


dfrow18160to25414allnan_latlong


# In[69]:


dfrow0to18159notnan


# In[70]:


pd.concat([dfrow0to18159notnan,dfrow18160to25414allnan_latlong])


# In[71]:


dfrow0to25414_morelatlong = pd.concat([dfrow0to18159notnan,dfrow18160to25414allnan_latlong])


# In[72]:


dfrow0to25414_morelatlong


# In[74]:


dfrow0to25414_morelatlong = dfrow0to25414_morelatlong.reset_index(drop=True)


# In[75]:


dfrow0to25414_morelatlong


# In[76]:


dfrow0to25414_morelatlong.to_csv('dfrow0to25414_morelatlong.csv',index=False)


# # merge back with the whole data that has all columns

# In[115]:


import pandas as pd


# In[116]:


dfrow0to25414_morelatlong = pd.read_csv('dfrow0to25414_morelatlong.csv')


# In[117]:


dfrow0to25414_morelatlong.shape


# In[118]:


dfrow0to25414_morelatlong.head(3)


# In[119]:


dfrow0to25414_morelatlong['cep']=dfrow0to25414_morelatlong['cep'].astype(str).replace('\.0','',regex=True)


# In[120]:


dfrow0to25414_morelatlong


# In[121]:


dfrow0to25414_morelatlong['latitude'].isna().sum()


# In[122]:


pd.set_option('display.max_rows',10)


# In[123]:


dfrow0to25414_morelatlong['latitude'].value_counts()


# In[159]:


1 - 4605/25414 # it raised from 76% before manoels model to 81% ceps found, good because many of the 29% remaining ceps are wrong


# In[124]:


dfrow0to25414_morelatlong


# In[125]:


dfrow0to25414_morelatlong.drop('cepsindex',axis=1,inplace=True)


# In[95]:


bancoesusalltabsrais2019 = pd.read_csv('bancoesusalltabs_04012020to08052021rais2019.csv')


# In[96]:


bancoesusalltabsrais2019.dtypes


# In[97]:


bancoesusalltabsrais2019['cep'].dtypes


# In[98]:


bancoesusalltabsrais2019.shape


# In[99]:


bancoesusalltabsrais2019.head(3)


# In[101]:


bancoesusalltabsrais2019.drop('_merge', axis=1,inplace=True)


# In[102]:


bancoesusalltabsrais2019.shape


# In[126]:


len(dfrow0to25414_morelatlong['cep']) - dfrow0to25414_morelatlong['cep'].nunique() #number of duplicates


# In[127]:


dfrow0to25414_morelatlong


# In[128]:


dfrow0to25414_morelatlong.dtypes


# In[113]:


pd.set_option('display.max_rows',None)


# In[114]:


dfrow0to25414_morelatlong


# In[129]:


dfrow0to25414_morelatlong['cep'] = dfrow0to25414_morelatlong['cep'].astype(str)


# In[130]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].astype(str)


# In[147]:


bancoesusalltabsrais2019['cep'] = bancoesusalltabsrais2019['cep'].str.replace('\.0','',regex=True)


# In[149]:


bancoesusalltabsrais2019['cep']


# In[131]:


#bancoesusalltabsrais2019morelatlong = bancoesusalltabsrais2019.merge(dfrow0to25414_morelatlong, how = 'inner', on='cep', indicator=True)


# In[132]:


bancoesusalltabsrais2019morelatlong.shape


# In[148]:


#only 43k it should've been 250k lets compare with dfrow0to25425

#the problem was with bancoesusalltabsrais2019['cep']
#bancoesusalltabsrais2019['cep'].str.replace('.\0','',regex=True)


# In[134]:


dfrow0to25425 = pd.read_csv('dfrow0to25425latlong.csv')


# In[135]:


dfrow0to25425 


# In[137]:


dfrow0to25425['cep'] = dfrow0to25425['cep'].astype(str).replace('\.0','',regex=True) 


# In[138]:


dfrow0to25425 = dfrow0to25425.drop_duplicates('cep')


# In[139]:


dfrow0to25425.sort_values('cep')


# In[141]:


dfrow0to25425.dtypes


# In[140]:


dfrow0to25414_morelatlong.sort_values('cep')


# In[145]:


dfrow0to25414_morelatlong.dtypes


# In[150]:


bancoesusalltabsrais2019morelatlong = bancoesusalltabsrais2019.merge(dfrow0to25414_morelatlong, how = 'inner', on='cep', indicator=True)


# In[151]:


bancoesusalltabsrais2019morelatlong.shape


# In[152]:


bancoesusalltabsrais2019morelatlong.to_csv('bancoesusalltabsrais2019morelatlong.csv',index = False)


# In[153]:


bancoesusalltabsrais2019morelatlong.head(3)


# In[155]:


bancoesusalltabsrais2019morelatlong['latitude'].isnull().sum()


# In[156]:


bancoesusalltabsrais2019morelatlong['latitude'].value_counts()


# In[160]:


1 - 14253/250216


# In[161]:


#over 94% of latitude and longitude observation, and the ramanining 6%, many ceps were wrong


# In[164]:


pd.set_option('display.max_columns',None)


# In[166]:


pd.set_option('display.max_columns',10)


# In[167]:


pd.set_option('display.max_rows',None)


# In[168]:


bancoesusalltabsrais2019morelatlong['cep'].sort_values


# In[169]:


bancoesusalltabsrais2019morelatlong['latitude'].sort_values


# In[170]:


1 - 14253/250216


# In[171]:


bancoesusalltabsrais2019morelatlong['latitude'].isnull().sum()


# In[173]:


pd.set_option('display.max_rows',10)


# In[175]:


bancoesusalltabsrais2019morelatlong['latitude'].value_counts()


# In[176]:


#it makes sense there's 14253, 1 NaN, and the rest of the latitudes are there


# In[177]:


#compared to before, now it's 94% of all ceps and before?


# In[178]:


bancoesusalltabsrais2019latlong = pd.read_csv('bancoesusalltabsrais2019latlong.csv')


# In[180]:


bancoesusalltabsrais2019latlong.shape


# In[181]:


bancoesusalltabsrais2019latlong['latitude'].isnull().sum()


# In[182]:


bancoesusalltabsrais2019latlong['latitude'].value_counts()


# In[183]:


1 - 70744/250216


# In[184]:


#from 71% of latitude it went to 94% of latitude


# # CEP Estab

# In[201]:


import pandas as pd


# In[203]:


bancoesusalltabsrais2019morelatlong = pd.read_csv('bancoesusalltabsrais2019morelatlong.csv')


# In[206]:


bancoesusalltabsrais2019morelatlong.head(3)


# In[209]:


bancoesusalltabsrais2019morelatlong.shape


# In[210]:


bancoesusalltabsrais2019morelatlong.columns


# In[211]:


bancoesusalltabsrais2019morelatlong['CEP Estab']


# In[212]:


bancoesusalltabsrais2019morelatlong.drop_duplicates('CEP Estab')


# In[199]:


#find these lats and long too


# In[215]:


bancoesusalltabsrais2019morelatlong[['CEP Estab']]


# In[216]:


bancoesusalltabsrais2019morelatlong_cepestab = bancoesusalltabsrais2019morelatlong[['CEP Estab']]


# In[217]:


bancoesusalltabsrais2019morelatlong_cepestab


# In[218]:


bancoesusalltabsrais2019morelatlong_cepestab.drop_duplicates('CEP Estab')


# In[219]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups = bancoesusalltabsrais2019morelatlong_cepestab.drop_duplicates('CEP Estab')


# In[220]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups


# In[222]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups = bancoesusalltabsrais2019morelatlong_cepestab_nodups.reset_index()


# In[223]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups.rename({'index':'id'},axis=1,inplace=True)


# In[224]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups


# In[225]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups.to_csv('bancoesusalltabsrais2019morelatlong_cepestab_nodups.csv', index=False)


# # Finding lat and long CEP Estab

# In[1]:


import pandas as pd 


# In[2]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups = pd.read_csv('bancoesusalltabsrais2019morelatlong_cepestab_nodups.csv')


# In[3]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups.shape


# In[4]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups.head(3)


# In[5]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups


# In[6]:


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


# In[7]:


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


# In[8]:


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
                "".join(["http://photon.komoot.io/api?q=", address, "&limit=1"])
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


# In[9]:


#from .base import CEPConverter
#from .strategies import CorreiosPhotonConverter


def cep_to_coords(cep: str, factory: CEPConverter = CorreiosPhotonConverter) -> dict:
    coordinates = factory()(cep)
    return coordinates


# In[11]:


bancoesusalltabsrais2019morelatlong_cepestab_nodups.update("cep_to_coords('" + bancoesusalltabsrais2019morelatlong_cepestab_nodups[['CEP Estab']].astype(str) + "'),")
print(bancoesusalltabsrais2019morelatlong_cepestab_nodups)


# In[18]:


cepestab0to6842 = bancoesusalltabsrais2019morelatlong_cepestab_nodups.loc[:,'CEP Estab']


# In[19]:


cepestab0to6842


# In[20]:


print(" ".join(cepestab0to6842))#.tolist()


# In[21]:




# In[22]:


print(coordinatescepestab0to6842)


# In[23]:


cepestab0to6842


# In[24]:


import re
pattern = re.compile(r"(\d+)")
result = []
for item in cepestab0to6842.tolist():
    result.append(''.join(pattern.findall(item)))


# In[25]:


print(result)


# In[26]:


dfcepestabid0to6842 = pd.DataFrame(coordinatescepestab0to6842, result)


# In[27]:


dfcepestabid0to6842 


# In[28]:


dfcepestabid0to6842.reset_index(level=0, inplace=True)


# In[29]:


dfcepestabid0to6842


# In[32]:


dfcepestabid0to6842 = dfcepestabid0to6842.rename(columns={'index':'CEP Estab','latitude':'latitudestab','longitude':'longitudestab'})


# In[33]:


dfcepestabid0to6842


# In[34]:


dfcepestabid0to6842.to_csv('cepestabid0to6842.csv',sep=',',index=False)


# # finding the remaining ceps with the other model

# In[35]:


import pandas as pd


# In[36]:


cepestabid0to6842 = pd.read_csv('cepestabid0to6842.csv')


# In[37]:


cepestabid0to6842 


# In[38]:


cepestabid0to6842.isnull().sum()


# In[40]:


1 - (1258/6842) #81% of latitude and longitude were found with the first model, let's see how many of the remaining 
                #are found with the second one


# In[41]:


cepestabid0to6842.sort_values('latitudestab')


# In[42]:


6836-1258


# In[43]:


cepestabid0to6842[:5578]


# In[50]:


cepestabid0to6842.sort_values('latitudestab').reset_index()[:5586]


# In[54]:


#del cepestabid0to6842notnan


# In[55]:


cepestabid0to6842notnan0to5584 = cepestabid0to6842.sort_values('latitudestab').reset_index()[:5585]


# In[57]:


cepestabid0to6842notnan0to5584


# In[58]:


cepestabid0to6842.sort_values('latitudestab').reset_index()[5585:]


# In[59]:


cepestabid0to6842allnan5585to6842 = cepestabid0to6842.sort_values('latitudestab').reset_index()[5585:]


# In[60]:


cepestabid0to6842allnan5585to6842 = cepestabid0to6842allnan5585to6842[['CEP Estab']]


# In[61]:


cepestabid0to6842allnan5585to6842


# In[62]:


ceps = cepestabid0to6842allnan5585to6842


# In[63]:


ceps


# In[65]:


6842-5585


# In[77]:


1257/3


# In[78]:


6841-5585


# In[80]:


1256/8 #this one


# In[64]:


import pyautogui
import time
import pyperclip
import pandas as pd


# In[82]:


pyautogui.PAUSE = 0.2
pyautogui.alert('It will start, press OK and do not touch anything nor move anything until it is done')
lat_long = []
start= 5585 #define the start CEP
stop= 6841 #define the final CEP #has to be the last index of the rows
block = 8 #number of tabs opened, it has to be a multiple of stop - start / block = integer

#it opens a new window
pyautogui.hotkey('ctrl', 'n')

for j in range(start,stop,block):
    
    #loop to open the tabs and search the urls
    for i in range(j,j+block):
        cep = ceps['CEP Estab'].loc[i] #selecting the column with CEP
        uri = 'https://www.google.com/maps/search/' #adding search to modify
        url = uri+str(cep)
        pyautogui.hotkey('ctrl', 't')
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'v')
        
        pyautogui.press('enter')

    pyautogui.hotkey('ctrl', '2')
    time.sleep(15)
    

    #loop to close the tabs and colect the urls
    for i in range(j,j+block):
        time.sleep(2)
        pyautogui.click(475, 75) #adjusting mouse position to copy the urls
        #depending on the pc the mouse position will change, there's the need to adjust the mouse position so it clicks inside the url by itself
        pyautogui.hotkey('ctrl', 'c')
        lat_long.append(pyperclip.paste())
        pyautogui.hotkey('ctrl', 'w')   

#Organizing the colected ceps into a dataframe        
df_lat_long = pd.DataFrame.from_dict(lat_long)
ceps = ceps.reset_index()
del ceps['index']
df_lat_long.insert(0,'cep', ceps['CEP Estab'], allow_duplicates=True)
df_lat_long

#Saving the coordinates into a csv file
#df_lat_long.to_csv(f"cep_url_{start}_{stop}.csv")


# In[83]:


df_lat_long.shape


# In[84]:


df_lat_long


# In[85]:


base_ceps = df_lat_long


# In[86]:


start= 0  #define the start CEP #very important this start and stop is the position, not the index, not start= 18160, but start = 0, and not stop = 18169, but stop = 10 
stop= 1256 #define the final CEP, it has to be the total number of rows

lat_long = []
for i in range(start,stop):
    text = base_ceps.iloc[i,1]
    final_index = text.find('/data=') #data(portuguese)=date(english)
    if final_index == -1:
        lat_long_i = {'lat':('-'), 'long':'-'}
        lat_long.append(lat_long_i)
    else:    
        initial_index = text.find('/@')
        text = text[initial_index+2:final_index-4]
        text = text.split(',')
        long = text[1]
        lat = text[0]
        lat_long_i = {'lat':lat, 'long':long}
        lat_long.append(lat_long_i)
        
df_lat_long = pd.DataFrame.from_dict(lat_long)


# In[87]:


df_lat_long.insert(0,'cep', base_ceps['cep'],True)
df_lat_long


# In[88]:


df_lat_long.reset_index(level=0, inplace = True)


# In[89]:


df_lat_long.rename({'index':'id'}, axis=1, inplace=True)


# In[90]:


df_lat_long


# In[91]:


df_lat_long.to_csv('dfcepestabid0to6842allnan5585to6841.csv', sep=',', index = False)


# In[93]:


dfcepestabid0to6842allnan5585to6841 = pd.read_csv('dfcepestabid0to6842allnan5585to6841.csv')


# In[94]:


dfcepestabid0to6842allnan5585to6841


# In[95]:


ceps


# In[96]:


ceps.reset_index(level=0,inplace=True)


# In[97]:


ceps.rename({'index':'cepsindex'}, axis=1, inplace=True)


# In[98]:


ceps


# In[99]:


dfcepestabid0to6842allnan5585to6841['cepsindex'] = ceps['cepsindex']


# In[100]:


dfcepestabid0to6842allnan5585to6841


# In[101]:


dfcepestabid0to6842allnan5585to6841['lat'].isnull().sum()


# In[102]:


dfcepestabid0to6842allnan5585to6841['lat'].value_counts()


# In[104]:


dfcepestabid0to6842allnan5585to6841['cepsindex'].dtypes


# In[105]:


dfcepestabid0to6842allnan5585to6841.dtypes


# In[106]:


dfcepestabid0to6842allnan5585to6841


# In[109]:


cepestabid0to6842allnan5585to6842


# In[110]:


dfcepestabid0to6842allnan5585to6841['cepsindex']+5585


# In[111]:


dfcepestabid0to6842allnan5585to6841['cepsindex'] = dfcepestabid0to6842allnan5585to6841['cepsindex']+5585


# In[112]:


dfcepestabid0to6842allnan5585to6841


# In[113]:


#there's the need to find cepsindex 6841 and 6842
#6841 -> 53250760
#6842 -> 53550540


# In[116]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=01001000"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[114]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=53250760"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[115]:


import requests

url = "https://www.cepaberto.com/api/v3/cep?cep=53550540"
# O seu token está visível apenas pra você
headers = {'Authorization': 'Token token=d8e540d0700d405acc0496142c5be3d2'}
response = requests.get(url, headers=headers)

print(response.json())


# In[117]:


dfcepestabid0to6842allnan5585to6841


# In[167]:


dfcepestabid0to6842allnan5585to6841.dtypes#this might have been after changing dtype


# In[119]:


df2 = pd.DataFrame({'id':[1256,1257],
                   'cep':[53250760,53550540],
                   'lat':['-','-'],
                   'long':['-','-'],
                    'cepsindex':[6841,6842]})


# In[120]:


df2


# In[166]:


df2.dtypes


# In[123]:


dfcepestabid0to6842allnan5585to6841 = dfcepestabid0to6842allnan5585to6841.append(df2)


# In[124]:


dfcepestabid0to6842allnan5585to6841


# In[126]:


dfcepestabid0to6842allnan5585to6841.reset_index(drop=True, inplace = True)


# In[127]:


dfcepestabid0to6842allnan5585to6841


# In[129]:


dfcepestabid0to6842allnan5585to6841.rename({'cep':'CEP Estab','lat':'latitudestab','long':'longitudestab','cepsindex':'index'},axis=1,inplace=True)


# In[130]:


dfcepestabid0to6842allnan5585to6841


# In[131]:


dfcepestabid0to6842allnan5585to6841.drop('id',axis=1,inplace=True)


# In[132]:


dfcepestabid0to6842allnan5585to6841


# In[133]:


dfcepestabid0to6842allnan5585to6841[dfcepestabid0to6842allnan5585to6841.columns[[3,0,1,2]]]


# In[134]:


dfcepestabid0to6842allnan5585to6841 = dfcepestabid0to6842allnan5585to6841[dfcepestabid0to6842allnan5585to6841.columns[[3,0,1,2]]]


# In[137]:


dfcepestabid0to6842allnan5585to6841


# In[136]:


cepestabid0to6842notnan0to5584


# In[140]:


cepestabid0to6842notnan0to5584.dtypes


# In[141]:


dfcepestabid0to6842allnan5585to6841.dtypes


# In[144]:


#cepestabid0to6842notnan0to5584['latituestab'] = cepestabid0to6842notnan0to5584['latituestab'].astype(str)
#cepestabid0to6842notnan0to5584['longitudestab'] = cepestabid0to6842notnan0to5584['longitudestab'].astype(str)


# In[148]:


cepestabid0to6842notnan0to5584.append(dfcepestabid0to6842allnan5585to6841).reset_index(drop=True)


# In[149]:


dfcepestabid0to6842latlong = cepestabid0to6842notnan0to5584.append(dfcepestabid0to6842allnan5585to6841).reset_index(drop=True)


# In[150]:


dfcepestabid0to6842latlong


# In[151]:


dfcepestabid0to6842latlong.drop('index',axis=1,inplace=True)


# In[152]:


dfcepestabid0to6842latlong


# In[153]:


dfcepestabid0to6842latlong.dtypes


# In[154]:


dfcepestabid0to6842latlong = dfcepestabid0to6842latlong.reset_index()


# In[156]:


dfcepestabid0to6842latlong.rename({'index':'cepsindex'},axis=1,inplace=True)


# In[157]:


dfcepestabid0to6842latlong


# In[158]:


dfcepestabid0to6842latlong.to_csv('dfcepestabid0to6842latlong.csv',sep=',',index=False)


# # merge back with the data with all columns

# In[3]:


import pandas as pd


# In[4]:


dfcepestabid0to6842latlong = pd.read_csv('dfcepestabid0to6842latlong.csv')


# In[5]:


dfcepestabid0to6842latlong.shape


# In[6]:


dfcepestabid0to6842latlong.head(3)


# In[7]:


dfcepestabid0to6842latlong.dtypes


# In[2]:


#merge back to with the original files
#check the weird numbers on latitude and longitude
#the first model found some wrong latitudes and longitudes
#plot on map or use another way later to see which one is wrong
#check dtype when 2 rows were appended up some cells


# In[164]:


#see which one is correct data 
#not this one bancoesusalltabsrais2019 = pd.read_csv('bancoesusalltabs_04012020to08052021rais2019.csv')
#it's the one with latand long already from the individual ceps


# In[15]:


bancoesusalltabsrais2019morelatlong = pd.read_csv('bancoesusalltabsrais2019morelatlong.csv')


# In[16]:


bancoesusalltabsrais2019morelatlong.shape


# In[17]:


bancoesusalltabsrais2019morelatlong.head(3)


# In[18]:


bancoesusalltabsrais2019morelatlong['CEP Estab']


# In[19]:


bancoesusalltabsrais2019morelatlong['latitude'].isnull().sum()


# In[20]:


bancoesusalltabsrais2019morelatlongcepestab = bancoesusalltabsrais2019morelatlong.merge(dfcepestabid0to6842latlong, how='inner',on='CEP Estab',indicator='_merge2')


# In[21]:


bancoesusalltabsrais2019morelatlongcepestab.shape


# In[22]:


bancoesusalltabsrais2019morelatlongcepestab.head(3)


# In[24]:


bancoesusalltabsrais2019morelatlongcepestab.to_csv('bancoesusalltabsrais2019morelatlongcepestab.csv', sep=',',index=False)


# In[ ]:



