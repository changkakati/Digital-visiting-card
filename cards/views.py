# cards/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import VisitingCard
from .forms import VisitingCardForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
import os
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
import io

@login_required
def create_card(request):
    if request.method == 'POST':
        form = VisitingCardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('cards:list_cards')
    else:
        form = VisitingCardForm()
    return render(request, 'cards/card_form.html', {'form': form})

@login_required
def list_cards(request):
    cards = VisitingCard.objects.filter(user=request.user)
    return render(request, 'cards/card_list.html', {'cards': cards})

@login_required
def edit_card(request, pk):
    card = get_object_or_404(VisitingCard, pk=pk, user=request.user)
    if request.method == 'POST':
        form = VisitingCardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            
            # Remove photo if checkbox checked
            if request.POST.get('remove_photo') and card.photo:
                card.photo.delete(save=False)
                card.photo = None

            # Remove cover photo if checkbox checked
            if request.POST.get('remove_cover_photo') and card.cover_photo:
                card.cover_photo.delete(save=False)
                card.cover_photo = None

            card.save()
            return redirect('cards:list_cards')
    else:
        form = VisitingCardForm(instance=card)
    return render(request, 'cards/card_form.html', {'form': form, 'card': card})

    
@login_required
def delete_card(request, pk):
    card = get_object_or_404(VisitingCard, pk=pk, user=request.user)
    if request.method == 'POST':
        card.delete()
        return redirect('cards:list_cards')
    return render(request, 'cards/card_confirm_delete.html', {'card': card})

def card_detail(request, slug):
    card = get_object_or_404(VisitingCard, slug=slug)
    return render(request, 'cards/card_detail.html', {'card': card})

def card_by_username(request, username):
    # show the latest card of a username or first card -- adapt per your choice
    card = VisitingCard.objects.filter(user__username=username).order_by('-id').first()
    if not card:
        raise Http404("No card found for this user")
    return render(request, 'cards/card_detail.html', {'card': card})

def download_qr(request, slug):
    card = get_object_or_404(VisitingCard, slug=slug)
    if not card.qr_code:
        raise Http404("QR code not available")
    qr_path = card.qr_code.path
    if os.path.exists(qr_path):
        return FileResponse(open(qr_path, 'rb'), as_attachment=True, filename=os.path.basename(qr_path))
    raise Http404


def card_pdf(request, slug):
    card = get_object_or_404(VisitingCard, slug=slug)
    html = render_to_string('cards/card_pdf.html', {'card': card})
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=result)
    if pisa_status.err:
        return HttpResponse('We had errors <pre>' + html + '</pre>')
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{card.slug}.pdf"'
    return response