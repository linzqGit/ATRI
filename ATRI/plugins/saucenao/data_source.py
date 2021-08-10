from random import choice

from ATRI.service import Service
from ATRI.rule import is_in_service
from ATRI.exceptions import RequestError
from ATRI.utils import request, UbuntuPaste


URL = "https://saucenao.com/search.php"


__doc__ = """
以图搜图，仅限二刺螈
"""


class SaouceNao(Service):
    
    def __init__(self, api_key: str = None, output_type=2, testmode=1, dbmaski=32768, db=5, numres=5):
        Service.__init__(self, "以图搜图", __doc__, rule=is_in_service("以图搜图"))

        params = dict()
        params["api_key"] = api_key
        params["output_type"] = output_type
        params["testmode"] = testmode
        params["dbmaski"] = dbmaski
        params["db"] = db
        params["numres"] = numres
        self.params = params
    
    async def _request(self, url: str):
        self.params["url"] = url
        
        try:
            res = await request.post(URL, params=self.params)
        except RequestError:
            raise RequestError("Request failed!")
        data = await res.json()
        return data
    
    async def search(self, url: str) -> str:
        data = await self._request(url)
        res = data["results"]
        
        result = list()
        for i in range(len(res)):
            data = res[i]
            
            _result = dict()
            _result["similarity"] = data["header"]["similarity"]
            _result["index_name"] = data["header"]["index_name"]
            _result["url"] = choice(data["data"].get("ext_urls", ["None"]))
            result.append(_result)
        
        msg0 = str()
        for i in result:
            msg0 += (
                "\n——————————\n"
                f"Similarity: {i['similarity']}\n"
                f"Name: {i['index_name']}\n"
                f"URL: {i['url'].replace('https://', '')}"
            )
        
        if len(res) <= 3:
            return msg0
        else:
            repo = f"\n详细请移步此处~\n{await UbuntuPaste(content=msg0).paste()}"
            return repo
