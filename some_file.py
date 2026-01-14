from pydantic import BaseModel
import json
import pprint
from typing import Optional

class Bupao(BaseModel):
    bizid: int
    listingid: int
    userid: int
    flowid: str
    zuid: int
    categorycode: str = None  # categorycode 可以是字符串或 None
    isReentry: bool

def bupaoTest(userid, listingid, bizid, flowid, zuid, isReentry, categorycode=None):
    if categorycode:
        # 使用传递的 categorycode
        b = Bupao(userid=userid, listingid=listingid, bizid=bizid, flowid=flowid, 
                  zuid=zuid, categorycode=categorycode, isReentry=isReentry)
    else:
        # 不使用 categorycode
        b = Bupao(userid=userid, listingid=listingid, bizid=bizid, flowid=flowid, 
                  zuid=zuid, isReentry=isReentry)
    
    payload = json.dumps(b.dict(exclude_none=True))  # 排除 None 的字段
    pprint.pprint(payload)

# 测试
test_data_with_categorycode = {
    "userid": 12345,
    "listingid": 67890,
    "bizid": 1,
    "flowid": "phi-quechao-test-flow",
    "zuid": 999,
    "isReentry": False,
    "categorycode": "test-categorycode"
}

test_data_without_categorycode = {
    "userid": 12345,
    "listingid": 67890,
    "bizid": 1,
    "flowid": "phi-quechao-test-flow",
    "zuid": 999,
    "isReentry": False
}

# 使用 categorycode
bupaoTest(**test_data_with_categorycode)
print("--------------------------------------------------------------------------------")
# 不使用 categorycode
bupaoTest(**test_data_without_categorycode)
