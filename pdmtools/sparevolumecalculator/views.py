from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from . import helpers


# Create your views here.
def index(request):
    if request.method == "POST":
        width = request.POST.get('width')
    
        return render(request, 'sparevolumecalculator/results.html')
    return render(request, 'sparevolumecalculator/index.html')

def results(request):
    if request.method == "POST":
        width = int(request.POST.get("width"))
        height = int(request.POST.get("height"))
        numCables = int(request.POST.get("numCables"))
        placed_cables = []
        cables = []

        for i in range(numCables):
            cable = int(request.POST.get("cable"+str(i)))
            cables.append(cable)

        cables = [d/2 for d in cables]
        cables = sorted(cables, reverse=True)


        for cable in cables:
            helpers.add_cable(height, width, cable, placed_cables)


        helpers.plot_circles_on_grid(placed_cables, height, width)
        spare_volume = helpers.calculate_spare_volume2(height, width, placed_cables)
        
        return render(request, "sparevolumecalculator/results.html", {'image_file':'/static/images/result.png', 'spare_volume':spare_volume})

def documentation(request):
    return render(request, "sparevolumecalculator/documentation.html", {
        "image_file":"/static/images/documentation.jpg"
        })