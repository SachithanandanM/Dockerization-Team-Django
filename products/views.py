from django.shortcuts import render, get_object_or_404 ,redirect
from django.core.paginator import Paginator
from django.db.models import Q as DjangoQ   # ✅ Rename to avoid conflict with ES Q
from django.http import JsonResponse
import logging

from .models import Category, Product
from .documents import ProductDocument

# Elasticsearch imports
from elasticsearch_dsl import Q as ESQ, Search
from elasticsearch_dsl.query import MultiMatch
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)


# 🔹 Product detail
@login_required
def product_detail(request, product_id):
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return render(request, '404.html')
    return render(request, 'product_detail.html', {'product': product})


# 🔹 Categories
@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


# 🔹 Products in one category (paginated)
@login_required
def products(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, '404.html')

    products_list = Product.objects.filter(category=category)

    paginator = Paginator(products_list, 8)  # 8 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': page_obj,
        'category': category
    })


# 🔹 All products (paginated)
@login_required
def all_products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 8)  # 8 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': page_obj,
        'category': None
    })


# 🔹 Full-text search with Elasticsearch
import re
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.query import MultiMatch



# logger = logging.getLogger(__name__)


@login_required
def search_products(request):
    query = request.GET.get('q', '').strip()

    products_list = Product.objects.none()

    if query:
        s = Search(index='products')

        response = None

        # 🔹 Check for price patterns (under, above, between)
        under_match = re.search(r"(.*)\bunder\s+(\d+)", query.lower())
        above_match = re.search(r"(.*)\babove\s+(\d+)", query.lower())
        between_match = re.search(r"(.*)\bbetween\s+(\d+)\s+and\s+(\d+)", query.lower())

        if under_match:
            keywords = under_match.group(1).strip()
            price_limit = int(under_match.group(2))

            multi_match = MultiMatch(
                query=keywords,
                fields=['name^5', 'description^3', 'category.name'],
                fuzziness='AUTO'
            )

            q = Q("bool",
                  must=[multi_match],
                  filter=[Q("range", price={"lt": price_limit})])

            response = s.query(q).execute()

        elif above_match:
            keywords = above_match.group(1).strip()
            price_limit = int(above_match.group(2))

            multi_match = MultiMatch(
                query=keywords,
                fields=['name^5', 'description^3', 'category.name'],
                fuzziness='AUTO'
            )

            q = Q("bool",
                  must=[multi_match],
                  filter=[Q("range", price={"gt": price_limit})])

            response = s.query(q).execute()

        elif between_match:
            keywords = between_match.group(1).strip()
            lower = int(between_match.group(2))
            upper = int(between_match.group(3))

            multi_match = MultiMatch(
                query=keywords,
                fields=['name^5', 'description^3', 'category.name'],
                fuzziness='AUTO'
            )

            q = Q("bool",
                  must=[multi_match],
                  filter=[Q("range", price={"gte": lower, "lte": upper})])

            response = s.query(q).execute()

        else:
            # 🔹 Pure text search (no price condition)
            multi_match = MultiMatch(
                query=query,
                fields=['name^5', 'description^3', 'category.name'],
                fuzziness='AUTO'
            )
            response = s.query(multi_match).execute()

        # Collect product IDs
        product_ids = []
        for hit in response:
            try:
                product_ids.append(int(hit.meta.id))
            except ValueError:
                logger.warning(f"Invalid product ID from Elasticsearch: {hit.meta.id}")

        # Fetch products from DB
        products_list = Product.objects.filter(id__in=product_ids)

        # Preserve ES relevance order
        preserved_order = {pid: idx for idx, pid in enumerate(product_ids)}
        products_list = sorted(
            products_list,
            key=lambda x: preserved_order.get(x.id, len(preserved_order))
        )

    # Paginate results
    paginator = Paginator(products_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': page_obj,
        'query': query
    })