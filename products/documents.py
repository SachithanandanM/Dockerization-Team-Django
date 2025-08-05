from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product, Category

@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'description': fields.TextField(),
        'id': fields.IntegerField()
    })

    price = fields.FloatField()

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            # 'price',
            'quantity',
        ]

    def get_queryset(self):
        return super().get_queryset().select_related('category')
