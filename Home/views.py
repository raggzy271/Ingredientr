from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from Home.inverse_cooking_model.src import predictr

def index(request):
    # If it a redirect from the form
    result = request.session.get('result')
    if result:
        del(request.session['result'])
        return render(request, 'result.html', result)

    # If it is a form submission
    if request.method == 'POST' and request.FILES.get('image'):
        uploadedImage = request.FILES.get('image')
        imageFileName = FileSystemStorage().save(uploadedImage.name, uploadedImage)
        
        result = predictr.getRecipe(imageFileName)
        result['imageFileName'] = imageFileName
        request.session['result'] = result
        return redirect('/')

    # If it a request to load the home page
    return render(request, 'index.html')