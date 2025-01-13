from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from .forms import ProdukForm
from .models import Kategori, Status, Produk
from .serializers import KategoriSerializer, StatusSerializer, ProdukSerializer, RegisterSerializer, LoginSerializer

# Register View Mepet waktune -_-
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': 'User registered successfully',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View Mepet waktune -_-
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': serializer.validated_data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()  # Ambil semua kategori
    serializer_class = KategoriSerializer  # Gunakan serializer Kategori

    # Override method list() untuk menambahkan status dan data ke respons
    def list(self, request, *args, **kwargs):
        # Memanggil method list() dari ModelViewSet untuk mendapatkan query set
        response = super().list(request, *args, **kwargs)

        # Menambahkan struktur respons dengan status dan data
        return Response({
            'status': 'success',
            'data': response.data  # Menyertakan data yang sudah di-serialize
        })



class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.select_related('kategori', 'status')  # Mengoptimalkan query dengan join
    serializer_class = ProdukSerializer



# List semua produk
def produk_list(request):
    # Ambil parameter pencarian dan status dari request GET
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    # Filter produk berdasarkan pencarian dan status
    produk = Produk.objects.all()

    # Filter berdasarkan nama produk jika ada
    if search:
        produk = produk.filter(nama_produk__icontains=search)

    # Filter berdasarkan status jika ada
    if status_filter:
        produk = produk.filter(status__id_status=status_filter)

    kategori = Kategori.objects.all()
    status = Status.objects.all()

    return render(request, 'produk_list.html', {
        'produk': produk,
        'kategori': kategori,
        'status': status
    })

# Tambah produk baru
def produk_create(request):
    kategori = Kategori.objects.all()
    status = Status.objects.all()

    if request.method == "POST":
        form = ProdukForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produk berhasil ditambahkan!")
            return redirect('produk_list')
        else:
            messages.error(request, "Gagal menambahkan produk. Silakan coba lagi.")
            return render(request, 'produk_form.html', {'form': form, 'kategori': kategori, 'status': status})
    else:
        form = ProdukForm()

    return render(request, 'produk_form.html', {'form': form, 'kategori': kategori, 'status': status})


# Edit produk
def produk_update(request, id):
    produk = get_object_or_404(Produk, id_produk=id)
    if request.method == 'POST':
        produk.nama_produk = request.POST['nama_produk']
        produk.harga = request.POST['harga']
        produk.kategori = Kategori.objects.get(id_kategori=request.POST['kategori'])
        produk.status = Status.objects.get(id_status=request.POST['status'])
        produk.save()
        messages.success(request, "Produk berhasil diperbarui!")
        return redirect('produk_list')
    kategori = Kategori.objects.all()
    status = Status.objects.all()
    return render(request, 'produk_form.html', {'produk': produk, 'kategori': kategori, 'status': status})

# Hapus produk
def produk_delete(request, id):
    produk = get_object_or_404(Produk, id_produk=id)
    if request.method == 'POST':
        produk.delete()
        messages.success(request, "Produk berhasil dihapus!")
        return redirect('produk_list')
    return render(request, 'produk_confirm_delete.html', {'produk': produk})


#untk validassi form 
class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']

    def clean_nama_produk(self):
        nama_produk = self.cleaned_data['nama_produk']
        if len(nama_produk) < 3:
            raise forms.ValidationError("Nama produk harus lebih dari 3 karakter.")
        return nama_produk

    def clean_harga(self):
        harga = self.cleaned_data['harga']
        if harga <= 0:
            raise forms.ValidationError("Harga harus lebih besar dari 0.")
        return harga
