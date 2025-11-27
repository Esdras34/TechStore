from rest_framework import serializers
from app.models import Desenvolvedor

class DesenvolvedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desenvolvedor
        fields=('id','nome','email', 'funcao', 'descricao')
        