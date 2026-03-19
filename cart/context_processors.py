from .cart import Cart 
#creating context processor for making cart work in all pages

def cart(request):
    return {'cart' : Cart(request)}