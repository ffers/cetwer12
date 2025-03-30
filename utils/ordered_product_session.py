class OrderedProductSession:
    @staticmethod
    def proccess(dto):
        data = dto.model_dump()
        products = []
        for p in dto.ordered_product:
            products.append(p.model_dump())
        data["ordered_product"] = products
        # print("OrderedProductSession:", products)
        return data