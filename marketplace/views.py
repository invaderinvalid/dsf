from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Service, Order
from .forms import ServiceForm, OrderForm

@login_required
def service_list(request):
    services = Service.objects.all()
    
    # If there are no services, create a sample service
    if not services.exists():
        sample_user, created = User.objects.get_or_create(username='sample_provider')
        sample_service = Service.objects.create(
            provider=sample_user,
            title="Sample Service",
            description="This is a sample service description.",
            price=9.99,
            category='other'
        )
        services = Service.objects.all()
    
    return render(request, 'marketplace/service_list.html', {'services': services})

@login_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.service = service
            order.save()
            messages.success(request, f"You have successfully ordered {service.title}")
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'marketplace/service_detail.html', {'service': service, 'form': form})

@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, f"Your service '{service.title}' has been created")
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'marketplace/create_service.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(client=request.user)
    provided_services = Service.objects.filter(provider=request.user)
    received_orders = Order.objects.filter(service__in=provided_services)
    return render(request, 'marketplace/order_list.html', {'orders': orders, 'received_orders': received_orders})

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, service__provider=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order status updated to {order.get_status_display()}")
        else:
            messages.error(request, "Invalid status")
    return redirect('order_list')
