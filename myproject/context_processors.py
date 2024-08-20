from myapp.models import Post


def searchFunction(request):
    search_context = {}
    posts = Post.objects.all()
    if "search" in request.GET:
        query = request.GET.get("q")
        print(query)
        #<Filter:
        search_tag = request.GET.get("search-tag")
        if search_tag == "descriptions":
            objects = posts.filter(content__icontains=query)
        elif search_tag == "titles":
            objects = posts.filter(title__icontains=query)
        else:
            objects = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
        #</Filter
        # print(objects)
        search_context = {
            "objects": objects,
            "query": query
        }
    return search_context
