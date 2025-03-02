from server_flask.db import db
from server_flask.models import (Products,
                                 ProductAnalitic,
                                 ProductRelate,
                                 ProductSource)


class ProductRep():
    def add_product(self, description, article, product_name, price, quantity):
        try:
            product = Products(description=description,
                            article=article,
                            product_name=product_name,
                            price=price,
                            quantity=quantity)
            db.session.add(product)
            db.session.commit()
            add_analitic = ProductAnalitic(product_id=product.id)
            db.session.add(add_analitic)
            db.session.commit()
            return True
        except:
            return False
        
    def add_product_relate(self, data_list):
        try:
            item = ProductRelate(
                article=data_list[0],
                name="",
                quantity=int(data_list[1]),
                product_id=data_list[2],
                product_source_id=data_list[0]
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except:
            return False
 

    def update_product_item(self, data, id):
        try:
            product = Products.query.get_or_404(id)
            print(id, product.id, product.product_name, product.article)
            product.article = data[0]
            product.product_name = data[1]
            db.session.commit()
            return True
        except:
            return False
                  
                                  
    def update_after_arrival(self, combined_list):
        for item in combined_list:
            datetime_new, product_id, quantity, price, total = item
            product = Products.query.get_or_404(product_id)
            product.quantity = quantity + product.quantity
            product.body_product_price = price
            db.session.commit()
        return True
         
    def delete_product(self, id):
        task_to_delete = Products.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

    def changeBodyPrice(self):
        products = self.load_product_all()
        for item in products:
            if not item.body_product_price:
                item.body_product_price = 0

    def update_product_relate(self, data, id):
        try:
            product = ProductRelate.query.get_or_404(id)

            print(f"артикил {data}")
            product.article = data[0]
            product.quantity = data[1],
            product.product_id = data[2]
            product.product_source_id = data[0]
            db.session.commit()
            return True
        except:
            return False

    def load_product_all(self):
        products = Products.query.order_by(Products.timestamp).all()
        return products

    def load_product_item(self, product_id):
        product = Products.query.get_or_404(product_id)
        return product
    
    def load_by_article(self, art):
        try:
            product = Products.query.filter_by(article=art).first()
            return product
        except:
            return False

    def load_product_relate(self):
        products = ProductRelate.query.order_by(ProductRelate.timestamp).all()
        return products

    def load_product_relate_item(self, product_id):
        item = ProductRelate.query.get_or_404(product_id) 
        return item

    def load_prod_relate_product_id(self, id):
        item = ProductRelate.query.filter_by(product_id=id).first()
        return item

    def load_prod_relate_product_id_all(self, id):
        item = ProductRelate.query.filter_by(product_id=id).all()
        return item


    def delete_product_relate(self, id):
        task_to_delete = ProductRelate.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True






prod_rep = ProductRep()



