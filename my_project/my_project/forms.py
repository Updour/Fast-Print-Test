from django import forms
from .models import Produk, Kategori, Status

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']

    def clean_nama_produk(self):
        nama_produk = self.cleaned_data.get('nama_produk')
        if Produk.objects.filter(nama_produk=nama_produk).exists():
            raise forms.ValidationError("Produk dengan nama ini sudah ada. Silakan pilih nama produk lain.")
        return nama_produk

    
    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga <= 0:
            raise forms.ValidationError("Harga harus lebih dari 0.")
        return harga

    def clean_kategori(self):
        kategori = self.cleaned_data.get('kategori')
        if kategori is None:
            raise forms.ValidationError("Kategori harus dipilih.")
        return kategori
