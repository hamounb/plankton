from .models import ProductModel


def menu(request):
    cart = request.session.get('cart', {})
    products = ProductModel.objects.filter(id__in=[int(id) for id in cart.keys()])
    c = {}
    total = 0
    for k,v in cart.items():
        product = products.get(id=int(k))
        total += product.price
        c[k] = {'product': product, 'count': v}
    return {"cart":c, "total":total}