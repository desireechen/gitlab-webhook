from fastapi import FastAPI, Request
from datacataloglib.utils import addDatasetStatistic, addDatasetVersion, addDataset
from datacataloglib.data_catalog_interfaces import DatasetStatistic, DatasetStatisticColumn, DatasetVersion, Dataset

app = FastAPI()


@app.post("/message")
async def send_message(hook: Request):
    body = await hook.json()
    print(await hook.body())

    if (body["total_commits_count"] == 0) or (body["user_username"] == 'dataeng'):
        pass
    else:
        commits_count = body["total_commits_count"]

        for i in range(commits_count):
            org = "None"
            project = body["project"]["namespace"]
            repository = body["repository"]["name"]
            dataset = body["commits"][i]["added"]
            dataset = [x for x in dataset if x.endswith('.dvc')]
            dataset = [x[:-4] for x in dataset]
            dataset = [x.rsplit('/', 1)[-1] for x in dataset]
            columns = []
            description = body["commits"][i]["message"]

            result = []
            for x in dataset:
                if x.endswith('.csv') or x.endswith('.xls') or x.endswith('.xlsx'):
                    tags = ["tabular"]
                else:
                    tags = []
                result.append(Dataset(org, project, repository, x, description, tags, columns))
            
            addDataset("<insert-url-here>", result)

                        
        for i in range(commits_count):
            org = "None"
            project = body["project"]["namespace"]
            repository = body["repository"]["name"]
            dataset = body["commits"][i]["modified"]
            dataset = [x for x in dataset if x.endswith('.dvc')]
            dataset = [x[:-4] for x in dataset]
            dataset = [x.rsplit('/', 1)[-1] for x in dataset]
            descriptionSource = "dvc"
            tags = ["versions"]
            description = body["commits"][i]["message"]

            result = []
            for x in dataset:
                result.append(DatasetVersion(org, project, repository, x, description, descriptionSource, tags))

            addDatasetVersion("<insert-url-here>", result)
    
    return {"client_host": hook.client.host}