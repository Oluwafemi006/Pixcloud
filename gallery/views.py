from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import ImageGallery, Profile, Category
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ImageUploadForm
from django.contrib.auth.mixins import LoginRequiredMixin

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'gallery/register.html', {'form': form})

@login_required
def profile(request):
    # S'assurer que le profil existe
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Votre profil a été mis à jour !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'gallery/profile.html', context)

class ImageListView(LoginRequiredMixin, ListView):
    model = ImageGallery
    template_name = 'gallery/home.html'
    context_object_name = 'images'
    ordering = ['-created_at']
    paginate_by = 12
    
    def get_queryset(self):
        # Afficher seulement les images de l'utilisateur connecté
        return ImageGallery.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ImageDetailView(LoginRequiredMixin, DetailView):
    model = ImageGallery
    template_name = 'gallery/image_detail.html'
    
    def get_queryset(self):
        # S'assurer que l'utilisateur ne peut voir que ses propres images
        return ImageGallery.objects.filter(user=self.request.user)

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, 'Votre image a été téléversée avec succès !')
            return redirect('gallery-home')
    else:
        form = ImageUploadForm()
    
    return render(request, 'gallery/upload.html', {'form': form})

@login_required
def delete_image(request, pk):
    image = get_object_or_404(ImageGallery, pk=pk)
    
    # Vérifier que l'utilisateur est propriétaire de l'image
    if image.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette image.")
        return redirect('gallery-home')
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image supprimée avec succès.')
        return redirect('gallery-home')
    
    return render(request, 'gallery/confirm_delete.html', {'image': image})

def category_images(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    images = ImageGallery.objects.filter(user=request.user, category=category).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'gallery/category.html', {
        'images': images,
        'category': category,
        'categories': categories })  

@login_required
def custom_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')