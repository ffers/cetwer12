from dataclasses import dataclass

@dataclass
class ProductRelateDTO:
    id: int 
    product_source_id: int
    quantity: int
    product_id: int
