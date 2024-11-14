from datetime import datetime, timezone








class SourDiffAnServ():
    def __init__(self) -> None:
        pass

    def add_source_difference_req(self, req):
        event_date = datetime.strptime(req.form['event_date'], "%d-%m-%Y")
        source_id = req.form['source_id']
        quantity_crm = req.form['quantity_crm']
        quantity_stock = req.form['quantity_stock']
        difference = req.form['difference']
        return (event_date, source_id, quantity_crm,  
                quantity_stock, difference)
    
    def update_quantity(self, products):
        for product in products:
            product.quantity
 
    def add_quantity_crm(self, item, event_date):
        quantity = item.quantity
        id = item.id
        data = (event_date, id, quantity)
        return data
    
    def update_source_diff_line(self, req):
        quantity_crm = req.form['quantity_crm']
        quantity_stock = req.form['quantity_stock']
        return ( quantity_crm,  
                quantity_stock)