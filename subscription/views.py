from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from foodservice.models import Allergen, MenuType
from subscription.models import Subscription, SubscriptionType


@transaction.atomic
def register_subscription(request):
    sub_options = request.POST
    print(sub_options)
    sub_type = SubscriptionType.objects.get(term=sub_options['term'])
    allergens = [Allergen.objects.get(pk=alergen_id) for alergen_id in
                 sub_options.getlist('allergies')]
    menu_type = MenuType.objects.get(name=sub_options['menu_type'])
    new_sub = Subscription.objects.create(
        client=request.user,
        type=sub_type,
        dishes=sub_options['dishes'],
        breakfast=sub_options['breakfast'],
        dinner=sub_options['dinner'],
        supper=sub_options['supper'],
        desert=sub_options['desert'],
        menu_type=menu_type,
        price_total=sub_type.price,
    )
    new_sub.save()
    for allergen in allergens:
        new_sub.allergens.add(allergen)


def get_subscription(request):
    terms = set(
        sub_type.term for sub_type
        in SubscriptionType.objects.order_by('-term')
    )
    allergens = set(
        (allergen.name, allergen.id) for allergen in Allergen.objects.all()
    )
    menu_types = set(
        (menu_type.name, menu_type.id) for menu_type in MenuType.objects.all()
    )
    context = {
        'subscription_options': {
            'terms': terms,
            'allergens': allergens,
            'menu_types': menu_types
        }
    }

    if request.method == 'POST':
        register_subscription(request)
        context['subscription_options']['active'] = True
        return HttpResponseRedirect(reverse('profile'))

    return render(request, template_name="order.html", context=context)
