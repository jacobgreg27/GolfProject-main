from django.shortcuts import render
from django.shortcuts import render
from .models import Scanner
from smsApp.models import Members
from django.shortcuts import render
from scanner.models import Scanner

# Create your views here.
def ScannerView(request):
    name = Members.objects.first().first_name
    obj=Scanner.objects.get(id=1)

    context = {
        'name': name,
        'obj': obj,}
    
    return render(request, 'scanner.html', context)


import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def generate_qr_code(request):
    # Get the current user
    user = request.user
    
    # Generate the QR code using the user's ID
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(user.id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Return the QR code image as a response
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = buffer.getvalue()
    return HttpResponse(qr_image, content_type='image/png')




