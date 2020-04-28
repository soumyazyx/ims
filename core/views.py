from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import Item, OrderItem, Order
from .forms import AddItemForm    


##

class HomeView(ListView):
    model = Item 
    ordering = ['item_name']
    paginate_by = 99999999
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.order_by('item_name').get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item 
    template_name = "product.html"


@login_required
def AddNewItemView(request):
    form = AddItemForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("core:home")
    
    context = {
        'form': form
    }
    return render(request, "item/add_new_item.html", context)


class AddToInventoryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(f"[Order] ordered status:{order.ordered}")
            for order_item in order.items.all():
                print("--")
                print(f"[Order item] ordered status:{order_item.ordered}")
                print(f"Item Name:{order_item.item}")
                print(f"Quantity to be added:{order_item.quantity}")
                for item_obj in Item.objects.filter(item_name=order_item.item):
                    print(f"Existing quanity:{item_obj.quantity}")
                    item_obj.quantity += order_item.quantity
                    item_obj.save()
                order_item.ordered = True
                order_item.save()
            order.ordered = True
            order.save()
            messages.info(self.request, "The inventory was updated successfully")
            return redirect("/")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class DeleteFromInventoryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(f"[Order] ordered status:{order.ordered}")
            for order_item in order.items.all():
                print("--")
                print(f"[Order item] ordered status:{order_item.ordered}")
                print(f"Item Name:{order_item.item}")
                print(f"Quantity to be added:{order_item.quantity}")
                for item_obj in Item.objects.filter(item_name=order_item.item):
                    print(f"Existing quanity:{item_obj.quantity}")
                    item_obj.quantity -= order_item.quantity
                    item_obj.save()
                order_item.ordered = True
                order_item.save()
            order.ordered = True
            order.save()
            messages.info(self.request, "The inventory was updated successfully")
            return redirect("/")
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

# def checkout(request):
#     order = Order.objects.get(user=self.request.user, ordered=False)
#     print(order)
#     return render(request, 'checkout-page.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You dont have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def landing_page(request):
    return render(request, "landing_page.html")
