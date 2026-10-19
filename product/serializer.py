from rest_framework import serializers


class ProductDocumentSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    price = serializers.FloatField()
    description = serializers.CharField()

    def to_representation(self, instance):
        return {
            "product_name": instance.product_name,
            "description": instance.description,
            "price": instance.price,
        }
