# views.py
from django.shortcuts import render
from .static.scripts.plot_script  import plotFunction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
   

def index_view(request):
    return render(request, 'index.html')


@csrf_exempt  # This decorator is used to exempt CSRF protection for simplicity in this example

def company_details(request):
    return render(request, 'company_details.html')

@csrf_exempt   
def plot_graph(request):
    if request.method == 'GET':
        # Retrieve the selected graph type and company name from the request's query parameters
        selected_graph_type = request.GET.get('graphType', '')
        company_symbol = request.GET.get('symbol', '')
        
        # Process the selected graph type and company name
        plot_html = plotFunction(company_symbol, selected_graph_type)
        # Return a JSON response if needed
        return JsonResponse({'plot_html': plot_html})
        
        
    # Handle other HTTP methods if necessary
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})