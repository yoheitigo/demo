import requests
from re import search
import asyncio
from time import time

base_url = "https://www.ebi.ac.uk/chembl/api/data/"

def get_id_activities(start_id,titles):
  start_title = titles[0]
  url = f'{base_url}activity?{start_title}_chembl_id={start_id}&limit=10000'
  activities = requests.get(url, headers={'Accept': 'application/json'}).json().get('activities', [])
  id_list = []
  for activity in activities:
    activity_id = activity['activity_id']
    target_id = activity['target_chembl_id']
    assay_id = activity['assay_chembl_id']
    compound_id=activity['molecule_chembl_id']
    id_list.append([activity_id, target_id, assay_id, compound_id])
  return (id_list,activities)

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

def get_data(activities,jobs):
  act_data = {} #{acid{chid{name:xx},chid{name:xx}},acid{chid{name:xx},chid{name:xx}}}
  
  for act in activities:
    activity_id = act['activity_id']
    target_id = act['target_chembl_id']
    assay_id = act['assay_chembl_id']
    molecule_id = act['molecule_chembl_id']
    title_dic = {'target_id':target_id,'assay_id':assay_id,'molecule_id':molecule_id}
    act_data[activity_id] = {target_id:{},assay_id:{},molecule_id:{}}
    
    data = clean(act)
    for title, jobli in jobs.items():
      title_id = title_dic[f'{title}_id']
      for job in jobli:
        indices = [i for i, item in enumerate(data) if search(job, str(item))]
        if '_' in job:
          job = job.replace('_', '.*')
          indices += [i for i, item in enumerate(data) if search(job, str(item))]
        for i in indices:
          if len(data[i]) <= 30:
            act_data[activity_id][title_id][data[i]] = data[i+1]
        if indices == []:
          act_data[activity_id][title_id][job] = []
          
  return act_data


#------------------------------------------------------------------------------------------------
activities = [{'action_type': None, 'activity_comment': None, 'activity_id': 112345, 'activity_properties': [], 'assay_chembl_id': 'CHEMBL701389', 'assay_description': 'Ability to inhibit growth of human myelogenous leukemic cell line KBM-3 variant namely KBM-3/DOX, was determined in an in vitro MTT assay.', 'assay_type': 'F', 'assay_variant_accession': None, 'assay_variant_mutation': None, 'bao_endpoint': 'BAO_0000190', 'bao_format': 'BAO_0000219', 'bao_label': 'cell-based format', 'canonical_smiles': 'COc1cccc2c1C(=O)c1c(O)c3c(c(O)c1C2=O)C[C@@](O)(C(=O)CO)C[C@@H]3O[C@H]1C[C@H](N)[C@H](O)[C@H](C)O1', 'data_validity_comment': None, 'data_validity_description': None, 'document_chembl_id': 'CHEMBL1125235', 'document_journal': 'J Med Chem', 'document_year': 1991, 'ligand_efficiency': None, 'molecule_chembl_id': 'CHEMBL53463', 'molecule_pref_name': 'DOXORUBICIN', 'parent_molecule_chembl_id': 'CHEMBL53463', 'pchembl_value': '6.31', 'potential_duplicate': 0, 'qudt_units': 'http://www.openphacts.org/units/Nanomolar', 'record_id': 299288, 'relation': '=', 'src_id': 1, 'standard_flag': 1, 'standard_relation': '=', 'standard_text_value': None, 'standard_type': 'IC50', 'standard_units': 'nM', 'standard_upper_value': None, 'standard_value': '490.0', 'target_chembl_id': 'CHEMBL613994', 'target_organism': 'Homo sapiens', 'target_pref_name': 'KBM-3/DOX cell line', 'target_tax_id': '9606', 'text_value': None, 'toid': None, 'type': 'IC50', 'units': 'uM', 'uo_units': 'UO_0000065', 'upper_value': None, 'value': '0.49'}, {'action_type': None, 'activity_comment': None, 'activity_id': 128763, 'activity_properties': [], 'assay_chembl_id': 'CHEMBL701389', 'assay_description': 'Ability to inhibit growth of human myelogenous leukemic cell line KBM-3 variant namely KBM-3/DOX, was determined in an in vitro MTT assay.', 'assay_type': 'F', 'assay_variant_accession': None, 'assay_variant_mutation': None, 'bao_endpoint': 'BAO_0000190', 'bao_format': 'BAO_0000219', 'bao_label': 'cell-based format', 'canonical_smiles': 'COc1cccc2c1C(=O)c1c(O)c3c(c(O)c1C2=O)C[C@](O)(C(=O)CO)C[C@@H]3OC1CC(NC(=O)CBr)C(O)C(C)O1', 'data_validity_comment': None, 'data_validity_description': None, 'document_chembl_id': 'CHEMBL1125235', 'document_journal': 'J Med Chem', 'document_year': 1991, 'ligand_efficiency': None, 'molecule_chembl_id': 'CHEMBL348458', 'molecule_pref_name': None, 'parent_molecule_chembl_id': 'CHEMBL348458', 'pchembl_value': '6.80', 'potential_duplicate': 0, 'qudt_units': 'http://www.openphacts.org/units/Nanomolar', 'record_id': 299291, 'relation': '=', 'src_id': 1, 'standard_flag': 1, 'standard_relation': '=', 'standard_text_value': None, 'standard_type': 'IC50', 'standard_units': 'nM', 'standard_upper_value': None, 'standard_value': '160.0', 'target_chembl_id': 'CHEMBL613994', 'target_organism': 'Homo sapiens', 'target_pref_name': 'KBM-3/DOX cell line', 'target_tax_id': '9606', 'text_value': None, 'toid': None, 'type': 'IC50', 'units': 'uM', 'uo_units': 'UO_0000065', 'upper_value': None, 'value': '0.16'}, {'action_type': None, 'activity_comment': None, 'activity_id': 138837, 'activity_properties': [], 'assay_chembl_id': 'CHEMBL701389', 'assay_description': 'Ability to inhibit growth of human myelogenous leukemic cell line KBM-3 variant namely KBM-3/DOX, was determined in an in vitro MTT assay.', 'assay_type': 'F', 'assay_variant_accession': None, 'assay_variant_mutation': None, 'bao_endpoint': 'BAO_0000190', 'bao_format': 'BAO_0000219', 'bao_label': 'cell-based format', 'canonical_smiles': 'COc1cccc2c1C(=O)c1c(O)c3c(c(O)c1C2=O)C[C@](O)(C(=O)CO)C[C@@H]3OC1CC(NC(=O)N(CCCl)N=O)C(O)C(C)O1', 'data_validity_comment': None, 'data_validity_description': None, 'document_chembl_id': 'CHEMBL1125235', 'document_journal': 'J Med Chem', 'document_year': 1991, 'ligand_efficiency': None, 'molecule_chembl_id': 'CHEMBL152966', 'molecule_pref_name': None, 'parent_molecule_chembl_id': 'CHEMBL152966', 'pchembl_value': '6.60', 'potential_duplicate': 0, 'qudt_units': 'http://www.openphacts.org/units/Nanomolar', 'record_id': 299290, 'relation': '=', 'src_id': 1, 'standard_flag': 1, 'standard_relation': '=', 'standard_text_value': None, 'standard_type': 'IC50', 'standard_units': 'nM', 'standard_upper_value': None, 'standard_value': '250.0', 'target_chembl_id': 'CHEMBL613994', 'target_organism': 'Homo sapiens', 'target_pref_name': 'KBM-3/DOX cell line', 'target_tax_id': '9606', 'text_value': None, 'toid': None, 'type': 'IC50', 'units': 'uM', 'uo_units': 'UO_0000065', 'upper_value': None, 'value': '0.25'}]
id_list = [[112345, 'CHEMBL613994', 'CHEMBL701389', 'CHEMBL53463'], [128763, 'CHEMBL613994', 'CHEMBL701389', 'CHEMBL348458'], [138837, 'CHEMBL613994', 'CHEMBL701389', 'CHEMBL152966']]
jobs = {'target': ['target_name', 'type', 'organism'], 'assay': ['document', 'id', 'type', 'conditions', 'reliability'], 'molecule': ['smiles', 'name','structure_type']}
start_id = 'CHEMBL613994'
titles = ['target', 'assay', 'molecule']

if __name__ == '__main__':
  s=time()
  a = get_id_activities(start_id,titles)
  g=time()
  print(g-s)
  
  s=time()
  a = get_data(activities,jobs)
  g=time()
  print(g-s)










