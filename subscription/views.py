from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from foodservice.models import Allergen
from subscription.models import Subscription, SubscriptionType


@transaction.atomic
def register_subscription(request):
    sub_options = request.POST
    sub_type = SubscriptionType.objects.get(term=sub_options['term'])
    allergens = [Allergen.objects.get(pk=alergen_id) for alergen_id in
                 sub_options.getlist('allergies')]

    new_sub = Subscription.objects.create(
        client=request.user,
        type=sub_type,
        dishes=sub_options['dishes'],
        breakfast=sub_options['breakfast'],
        dinner=sub_options['dinner'],
        supper=sub_options['supper'],
        desert=sub_options['desert'],
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
    context = {
        'subscription_options': {
            'terms': terms,
            'allergens': allergens
        }
    }

    if request.method == 'POST':
        register_subscription(request)
        context['subscription_options']['active'] = True
        return HttpResponseRedirect(reverse('profile'))

    return render(request, template_name="order.html", context=context)
