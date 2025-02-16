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
    allow_origins=["http://localhost:3000", "https://tech0-gen8-step4-pos-app-9.azurewebsites.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# 商品情報のモデル
class ProductResponse(BaseModel):
    code: str
    name: str
    price: Optional[str]

@app.get("/api/product", response_model=ProductResponse)
def get_product(code: str, db: Session = Depends(get_db)):
    """商品コードを受け取り、商品情報を返すAPI"""
    stmt = text("SELECT name, price FROM m_product_muto WHERE code = :code")
    product = db.execute(stmt, {"code": code}).fetchone()

    if product:
        return ProductResponse(code=code, name=product[0], price=str(product[1]))
    else:
        return ProductResponse(code=code, name="商品がマスタ未登録です", price=None)

# 購入データのモデル
class PurchaseItem(BaseModel):
    name: str
    quantity: int
    price: int
    total: int

class PurchaseRequest(BaseModel):
    items: List[PurchaseItem]

@app.post("/api/purchase")
def save_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    """購入データをDBに保存するAPI"""
    try:
        for item in request.items:
            db.execute(
                text("INSERT INTO purchase_history (name, quantity, price, total) VALUES (:name, :quantity, :price, :total)"),  # 修正！
                {"name": item.name, "quantity": item.quantity, "price": item.price, "total": item.total}
            )
        db.commit()
        return {"message": "購入データを保存しました。"}
    except Exception as e:
        db.rollback()
        print(f"購入データの保存に失敗: {e}")
        raise HTTPException(status_code=500, detail=f"購入データの保存に失敗しました。エラー: {str(e)}")
