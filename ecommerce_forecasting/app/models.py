from mongoengine import Document, DateField, StringField, IntField, FloatField, TimeField

class EcommerceData(Document):
    order_date = DateField()
    time = TimeField()
    aging = FloatField()
    customer_id = IntField()
    gender = StringField(max_length=10)
    device_type = StringField(max_length=20)
    customer_login_type = StringField(max_length=20)
    product_category = StringField(max_length=50)
    product = StringField(max_length=50)
    sales = FloatField()

    meta = {'collection': 'ecommerce_data'}
