from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from PIL import Image
from tinymce.models import HTMLField
import uuid

# Create your models here.

class Type(models.Model):
    name = models.CharField('Type', max_length=200, help_text='Enter type of wardrobe (e.g. Bedroom wardrobe)')

    def __str__(self):
        return self.name


class Product(models.Model):
    cover = models.ImageField('Example', upload_to='covers', null=True)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField('Name', max_length=200)
    colour = models.ForeignKey('Colour', on_delete=models.SET_NULL, null=True, related_name='products')
    summary = HTMLField()
    type = models.ManyToManyField(Type, help_text='Please select type for this wardrobe')

    def __str__(self):
        return f'{self.name} ({self.code})'

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    def display_type(self):
            return ', '.join(type.name for type in self.type.all()[:3])

    display_type.short_description = 'Type'

class ProductInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique IO for wardrobe copy')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Will be available to order', null=True, blank=True)
    requestor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    requirements = HTMLField('Your notes for us', max_length=2000, null=True, blank=True, default='', help_text='Enter the date till when you would like to have the wardrobe ready and any other requirements (e.g. size, different colour, your city)')

    LOAN_STATUS = (
        ('o', 'Orderred'),
        ('c', 'Can be orderred'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='o',
        help_text='Status',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.product.name})'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Colour(models.Model):
    colour = models.CharField('Colour', max_length=100)
    visual = models.ImageField('Example', upload_to='covers', null=True)

    def get_absolute_url(self):
        return reverse('colour-detail', args=[str(self.id)])

    def __str__(self):
        return self.colour

    def display_products(self):
        return ', '.join(product.name for product in self.products.all()[:3])

    display_products.short_description = 'products'

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Feedback', max_length=2000)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


