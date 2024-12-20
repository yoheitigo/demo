import requests
from re import search
import asyncio
from time import time 
base_url = "https://www.ebi.ac.uk/chembl/api/data/"

def clean(data):
  data = str(data)
  data = data.replace(',',':')
  data = data.split(':')
  cdata = []
  for i in data:
    i = i.replace('"','')
    i = i.replace('[','')
    i = i.replace(']','')
    i = i.replace('{','')
    i = i.replace('}','')
    i = i.replace("'",'')
    i = i.replace(",",'')
    i = i.replace(" ",'')
    cdata.append(i)
  return cdata


def get_data(id_list, jobs):
  target_url = f'{base_url}target/set/{id_list[0][1]}'
  assay_url = f'{base_url}assay/set/'
  molecule_url = f'{base_url}molecule/set/'
  id_dic = {}
  org_data = {}
  
  for i,ids in enumerate(id_list):
    id_dic[ids[0]] = {ids[1]:{},ids[2]:{},ids[3]:{}}
    _id = ids[2]
    if _id not in assay_url:
      if i == 0:assay_url = f'{assay_url}{_id}'
      else:assay_url = f'{assay_url};{_id}'
    _id = ids[3]
    if _id not in assay_url:
      if i == 0:molecule_url = f'{molecule_url}{_id}'
      else:molecule_url = f'{molecule_url};{_id}'
  
  target_data = requests.get(target_url, headers={'Accept': 'application/json'}).json()['targets']
  assay_data = requests.get(assay_url, headers={'Accept': 'application/json'}).json()['assays']
  molecule_data = requests.get(molecule_url, headers={'Accept': 'application/json'}).json()['molecules']
  data_dic = {'target':target_data,'assay':assay_data,'molecule':molecule_data}
  
  for title,datas in data_dic.items():
    if title in jobs.keys():
      for job in jobs[title]:
        for data in datas:
          id = data[f'{title}_chembl_id']
          if id not in org_data.keys():org_data[id] = {}
          data = clean(data)
          indices = [i for i, item in enumerate(data) if search(job, str(item))]
          if '_' in job:
            job = job.replace('_', '.*')
            indices += [i for i, item in enumerate(data) if search(job, str(item))]
          for i in indices:
            org_data[id][data[i]] = data[i+1]
          if indices == []:org_data[id][job] = []
    for actid,value in id_dic.items():
      for chemid in value:
        if chemid in org_data:
          id_dic[actid][chemid] = org_data[chemid]
        else:id_dic[actid][chemid] = {'none':'none'}
  # print(*id_dic.items(),sep='\n')
  return id_dic
    
    
id_list = [[112345, 'CHEMBL613994', 'CHEMBL701389', 'CHEMBL53463'], [128763, 'CHEMBL613994', 'CHEMBL701389', 'CHEMBL348458'], [138837, 'CHEMBL613994', 'CHEMBL701389', 'CHEMBL152966']]
jobs = {'target':['(^^)/','name','type'],'assay':['document_id','type','organism'],'molecule':['smiles','molecule_id','name','structure_type']}

if __name__ == '__main__':
  s= time()
  a = get_data(id_list,jobs)
  g=time()
  print(g-s)