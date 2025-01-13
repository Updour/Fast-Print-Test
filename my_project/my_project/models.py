from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Users(models.Model): #coming soon kyak e
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Panjang lebih untuk menyimpan hash yang lebih aman

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  # Pastikan password di-hash saat disimpan
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=100)

    class Meta:
        db_table = 'kategori'

    def __str__(self):
        return self.nama_kategori

class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=255)
 
    class Meta:
        db_table = 'status'
        
    def __str__(self):
        return self.nama_status

class Produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    nama_produk = models.CharField(max_length=100, unique=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name="produk")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="produk")

    class Meta:
        db_table = 'produk'
        
    def __str__(self):
        return self.nama_produk
    
    