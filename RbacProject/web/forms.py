from django.forms import Form, fields, widgets
from web import models


class OrderForm(Form):
    title = fields.CharField(
        required=True,
        max_length=32,
        widget=widgets.TextInput(attrs={'class': "form-control", 'name': "title", 'placeholder': "请输入标题"})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'name': "detail", 'id': "detail", 'cols': "30", 'rows': "10"})
    )
    status = fields.IntegerField(
        widget=widgets.Select(choices=models.Order.statusChoices)
    )
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'name': "solution", 'id': "solution", 'cols': "30", 'rows': "10"})
    )
