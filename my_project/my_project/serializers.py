from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Kategori, Status, Produk, Users

# Serializer untuk Register
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Hash password sebelum menyimpan
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


# Serializer untuk Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # Validasi username dan password
        user = Users.objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError("Username tidak ditemukan")
        
        # Memeriksa password yang dimasukkan dengan yang tersimpan di database
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Password tidak valid")
        
        return data


    
class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ProdukSerializer(serializers.ModelSerializer):
    kategori = KategoriSerializer()
    status = StatusSerializer()

    class Meta:
        model = Produk
        fields = '__all__'
