from django.contrib import admin
from .models import Type, Product, ProductInstance, Colour, ProductReview, Profile

class ProductInstanceInline(admin.TabularInline):
    model = ProductInstance
    readonly_fields = ('id',)
    can_delete = False
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'colour', 'display_type')

class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('product', 'status', 'requestor', 'due_back', 'id', 'requirements')
    list_editable = ('status', 'due_back')
    list_filter = ('status', 'due_back')
    search_fields = ('name', 'colour')

    fieldsets = (
        ('General', {
            'fields': ('product', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'requestor')
        }),
    )

class ColourAdmin(admin.ModelAdmin):
    list_display = ('colour', 'display_products')

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'date_created', 'reviewer', 'content')

admin.site.register(Type)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInstance, ProductInstanceAdmin)
admin.site.register(Colour, ColourAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Profile)

