from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from .forms import ProductReviewForm, UserUpdateForm, ProfileUpdateForm, UserProductForm
from .models import Product, ProductInstance, Colour


def index(request):
    num_products = Product.objects.all().count()
    num_instances_available = ProductInstance.objects.filter(status__exact='c').count()
    num_colours = Colour.objects.count()

    context = {
        'num_products': num_products,
        'num_instances_available': num_instances_available,
        'num_colours': num_colours,
    }

    return render(request, 'index.html', context=context)

def colours(request):
    paginator = Paginator(Colour.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_colours = paginator.get_page(page_number)
    context = {
        'colours': paged_colours
    }
    return render(request, 'colours.html', context=context)

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile is updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already in use!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with e-mail {email} already exist!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, 'Registration was successful! Please login')
                    return redirect('register')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')

def search(request):
    query = request.GET.get('query')
    search_results = Product.objects.filter(Q(name__icontains=query) | Q(summary__icontains=query))
    return render(request, 'search.html', {'products': search_results, 'query': query})

class ProductListView(generic.ListView):
    model = Product
    paginate_by = 3
    template_name = 'product_list.html'

class ProductDetailView(FormMixin, generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    form_class = ProductReviewForm

    class Meta:
        ordering = ['date_created']

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.product = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(ProductDetailView, self).form_valid(form)

def get_requestor_orders(request):
    paginator = Paginator(ProductInstance.objects.filter(requestor=request.user), 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)
    context = {
        'products': paged_products
    }
    return render(request, 'requestor_wardrobes.html', context=context)

class ProductByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = ProductInstance
    fields = ['product', 'requirements']
    success_url = "/woodwork/mywardrobes"
    template_name = 'user_product_form.html'

    def form_valid(self, form):
        form.instance.requestor = self.request.user
        return super().form_valid(form)

def updateProductRequest(request, pk):
    productinstance=ProductInstance.objects.get(id=pk)
    form = UserProductForm(instance=productinstance)

    if request.method == 'POST':
        form = UserProductForm(request.POST, instance=productinstance)
        if form.is_valid():
            form.instance.requestor = request.user
            form.save()
            return redirect('/woodwork/mywardrobes')
    context = {
        'form': form
    }
    return render(request, 'user_product_form.html', context)

def deleteProductRequest(request, pk):
    productinstance = ProductInstance.objects.get(id=pk)

    if request.method == 'POST':
        productinstance.delete()
        return redirect('/woodwork/mywardrobes')

    context = {
        'item': productinstance
    }
    return render(request, 'my_request_delete.html', context)


