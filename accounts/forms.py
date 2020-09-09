from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        #! cause you are importing everything from the Order class in models.Order
        #! to import things individually we could use
        #! fields= ['customer','product','date_created']
