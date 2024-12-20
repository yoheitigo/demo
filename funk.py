import act
import org
import time
import asyncio
from fastapi import FastAPI

@app.get('/')
def chembl_search(request_text):

    start_id = request_text.split('.')[0]
    req = (request_text.split('.')[-1]).split('>')
    response_dic_target = {}
    response_dic_act = {}
    titles = []
    jobs = {}
    
    for i, job in enumerate(req):
        title = job.split('[')[0]
        item = job[len(title):].strip('[]').split(',')
        titles += [title]
        jobs[title] = item
    id_list, activities = act.get_id_activities(start_id,titles)
    
    # asyncio.gather(act_data=act.get_data(activities,jobs),org_data=org.get_data(id_list,jobs))
    act_data = act.get_data(activities,jobs)
    org_data = org.get_data(id_list,jobs)

    all_data = {}
    for acti,value in act_data.items():
        all_data[acti] = {}
        for chem,info in value.items():
            all_data[acti][chem] = {}
            for job,data in info.items():
                if data == [] and job in org_data[acti][chem]:
                    all_data[acti][chem][job] = org_data[acti][chem][job]
                else:
                    all_data[acti][chem][job] = act_data[acti][chem][job]
                    
    return all_data

if __name__ == '__main__':
    s = time.time()
    request_text1 = 'CHEMBL613994.target[name,type,organism]>assay[document,id,type,conditions,reliability]>molecule[smiles,name,structure_type]'
    # data = asyncio.run(chembl_search(request_text1))
    chembl_search(request_text1)
    # print(data)
    g=time.time()
    print(g-s)