from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可（必要に応じて制限可能）
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# 仮の「商品マスタデータA」
PRODUCT_MASTER = {
    "12345678901": {"NAME": "りんご", "PRICE": 100},
    "23456789012": {"NAME": "バナナ", "PRICE": 150},
    "34567890123": {"NAME": "オレンジ", "PRICE": 120},
}

class ProductResponse(BaseModel):
    CODE: str
    NAME: str
    PRICE: Optional[str]

@app.get("/api/product", response_model=ProductResponse)
def get_product(code: str):
    """商品コードを受け取り、商品情報を返すAPI"""
    product = PRODUCT_MASTER.get(code)
    
    if product:
        return {"CODE": code, "NAME": product["NAME"], "PRICE": str(product["PRICE"])}
    else:
        return {"CODE": code, "NAME": "商品がマスタ未登録です", "PRICE": "N/A"}

# 仮のデータベース（辞書をリストで管理）
PURCHASE_DB = []

# 購入データのモデル
class PurchaseItem(BaseModel):
    NAME: str
    QUANTITY: int
    PRICE: int
    TOTAL: int

class PurchaseRequest(BaseModel):
    items: List[PurchaseItem]

@app.post("/api/purchase")
def save_purchase(request: PurchaseRequest):
    """購入データをDBに保存するAPI"""
    try:
        # データをDB (仮) に追加
        PURCHASE_DB.extend(request.items)
        return {"message": "購入データを保存しました。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="購入データの保存に失敗しました。")
