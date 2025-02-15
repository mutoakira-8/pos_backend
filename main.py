from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from database import get_db  # 既存のdatabase.pyからDB接続を取得
from sqlalchemy.orm import Session
from sqlalchemy.sql import text  # ← ここを追加！

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tech0-gen8-step4-pos-app-9.azurewebsites.net/"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# 商品情報のモデル
class ProductResponse(BaseModel):
    CODE: str
    NAME: str
    PRICE: Optional[str]

@app.get("/api/product", response_model=ProductResponse)
def get_product(code: str, db: Session = Depends(get_db)):
    """商品コードを受け取り、商品情報を返すAPI"""
    stmt = text("SELECT NAME, PRICE FROM m_product_muto WHERE CODE = :code")
    product = db.execute(stmt, {"code": code}).fetchone()

    if product:
        return ProductResponse(CODE=code, NAME=product[0], PRICE=str(product[1]))
    else:
        return ProductResponse(CODE=code, NAME="商品がマスタ未登録です", PRICE=None)

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
                text("INSERT INTO purchase_history (NAME, QUANTITY, PRICE, TOTAL) VALUES (:name, :quantity, :price, :total)"),  # 修正！
                {"name": item.NAME, "quantity": item.QUANTITY, "price": item.PRICE, "total": item.TOTAL}
            )
        db.commit()
        return {"message": "購入データを保存しました。"}
    except Exception as e:
        db.rollback()
        print(f"購入データの保存に失敗: {e}")
        raise HTTPException(status_code=500, detail=f"購入データの保存に失敗しました。エラー: {str(e)}")
