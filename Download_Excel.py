import json,re,os,traceback
from httpx import AsyncClient


FILE_PATH = os.path.dirname(__file__)

cookies = ""

dowload_url = "https://drive.kdocs.cn/api/v5/groups/409310106/files/{}/download?isblocks=false&support_checksums=md5,sha1,sha224,sha256,sha384,sha512"

async def get_url(url: Str):
    async with AsyncClient() as client:
        req = await client.get(
            url=url,
            headers={
                "Cookie":cookies,
                'origin': 'https://www.kdocs.cn',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
            }
        )
    return req.text

async def get_file(url: Str,title: Str):
    print("————开始下载{}————".format(title))
    async with AsyncClient() as client:
        req = await client.get(
            url=url
        )
    with open(os.path.join(FILE_PATH,title), "wb") as code:
        code.write(req.content)
    print("下载成功！")

async def dwonload(doc_url: Str):
      html_doc = await get_url(doc_url)
      data = re.search(r"window\.__WPSENV__=(.*?);", html_doc).group(1)
      data = json.loads(data)
      fileTitle = data["file_info"]["file"]["name"]
      fileID = data["file_info"]["file"]["id"]
      url = dowload_url.format(fileID)
      download_raw_data = json.loads(await get_url(url))
      Link = download_raw_data["url"]
      await get_file(Link,fileTitle)
