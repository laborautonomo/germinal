# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from models import Product, Segment
from banners.models import Banner

def index(request):
    product_list = Product.activated.all()[:9]
    segment_list = Segment.objects.all().order_by('order')[:3]
    
    template = loader.get_template('products/index.html')
    context = RequestContext(request, {
        'product_list'  : product_list,
        'segment_list'  : segment_list,
    })
    return HttpResponse(template.render(context))


def details(request, slug):
    try:
        product = Product.activated.get(slug=slug)
    except ObjectDoesNotExist:
        product = None
    
    try:
        http_referer = request.environ['HTTP_REFERER']
    except KeyError:
        http_referer = '/'
    
    template = loader.get_template('products/details.html')
    context = RequestContext(request, {
        'product'   : product,
        'http_referer' : http_referer,
    })
    return HttpResponse(template.render(context))

def query_by_segment(request, slug):
    product_list = Product.activated.filter(segment__slug=slug)
    segment = Segment.objects.get(slug=slug)
    
    template = loader.get_template('products/products.html')
    context = RequestContext(request, {
        'product_list'  : product_list,
        'filter'  : segment.title,
    })
    return HttpResponse(template.render(context))

def products_list(request):
    product_list = Product.activated.all()
    
    template = loader.get_template('products/products.html')
    context = RequestContext(request, {
        'product_list'  : product_list,
    })
    return HttpResponse(template.render(context))