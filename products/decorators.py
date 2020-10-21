from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


def paginate(func):
    def wrap(request, id, sort):
        try:
            books = func(request, id, sort)
            paginator = Paginator(books, 10)
            page = request.GET.get("page")
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        return books

    return wrap