from sqlalchemy import select

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository):
    def list(self, company_id: int) -> list[Product]:
        return list(self.db.scalars(select(Product).where(Product.company_id == company_id).order_by(Product.name)).all())

    def get(self, company_id: int, product_id: int) -> Product | None:
        return self.db.scalar(select(Product).where(Product.company_id == company_id, Product.id == product_id))

    def create(self, company_id: int, data: dict) -> Product:
        product = Product(company_id=company_id, **data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product, data: dict) -> Product:
        for key, value in data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()
