from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from database import get_db  # 既存のdatabase.pyからDB接続を取得
from sqlalchemy.orm import Session

app = FastAPI()

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンを許可（必要に応じて制限可能）
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)


# 商品情報のモデル
class ProductResponse(BaseModel):
    CODE: str
    NAME: str
    PRICE: Optional[str]

@app.get("/api/product", response_model=ProductResponse)
def get_product(code: str, db: Session = Depends(get_db)):
    """商品コードを受け取り、商品情報を返すAPI"""
    product = db.execute("SELECT NAME, PRICE FROM product_master WHERE CODE = %s", (code,)).fetchone()

    if product:
        return {"CODE": code, "NAME": product[0], "PRICE": str(product[1])}
    else:
        return {"CODE": code, "NAME": "商品がマスタ未登録です", "PRICE": "N/A"}

# 購入データのモデル
class PurchaseItem(BaseModel):
    NAME: str
    QUANTITY: int
    PRICE: int
    TOTAL: int

class PurchaseRequest(BaseModel):
    items: List[PurchaseItem]

@app.post("/api/purchase")
def save_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    """購入データをDBに保存するAPI"""
    try:
        for item in request.items:
            db.execute(
                "INSERT INTO purchase_history (NAME, QUANTITY, PRICE, TOTAL) VALUES (%s, %s, %s, %s)",
                (item.NAME, item.QUANTITY, item.PRICE, item.TOTAL)
            )
        db.commit()
        return {"message": "購入データを保存しました。"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="購入データの保存に失敗しました。")