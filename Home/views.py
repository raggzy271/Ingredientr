from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from Home.inverse_cooking_model.src import predictr

# Create your views here.

def index(request):
    # Handling form submissions
    if request.method == 'POST' and request.FILES.get('image'):
        uploadedImage = request.FILES.get('image')
        imageFileName = FileSystemStorage().save(uploadedImage.name, uploadedImage)
        
        result = predictr.getIngredients(use_urls=False, imageFileName=imageFileName)
        result['imageSrc'] = '/static/' + imageFileName

        return render(request, 'result.html', result)

    return render(request, 'index.html')
