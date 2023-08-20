from .models import Category  # Import your Category model

def categories(request):
    return {'categories': Category.objects.all()}  # Pass the categories to the context
