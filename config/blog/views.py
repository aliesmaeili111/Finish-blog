from django.shortcuts import get_object_or_404
from . models import Article,Category
# from django.core.paginator import Paginator
from django.views.generic import ListView,DeleteView
from account.models import User
from account.mixins import AuthorAccessMixin
from django.db.models import Q

# start home view

# def home(request,page=1):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list,5)   
#     articles = paginator.get_page(page)
#     context = {
#         'articles':articles, 
#     }
#     return render(request,'blog/home.html',context)

class ArticleList(ListView):
    # model = Article
    # template_name = 'blog/home.html'
    # context_object_name =  'articles'
    queryset = Article.objects.published()
    paginate_by =  5
    
# end of home view

# start detail view

# def detail(request,slug):
#     context={
#         'article':get_object_or_404(Article.objects.published(),slug=slug)
#     }
#     return render(request,'blog/detail.html',context)

class ArticleDetail(DeleteView):
    template_name = "blog/article_detail.html"
    def get_object(self):
        slug = self.kwargs.get('slug')
        article =  get_object_or_404(Article.objects.published(),slug=slug)
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article
# end of detail view

# start category view

# def category(request,slug,page=1):
#     category = get_object_or_404(Category,slug=slug,status=True) 
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list,5)   
#     articles = paginator.get_page(page)
    
#     context={
#         'category':category,
#         'articles':articles
#     }
#     return render(request,'blog/category.html',context)

class CategoryList(ListView):
    template_name = "blog/category_list.html"
    paginate_by =  5
    def get_queryset(self):
        global category
        slug  = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(),slug=slug) 
       
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
# end of category view


# start view author
class AuthorList(ListView):
    template_name = "blog/author_list.html"
    paginate_by =  5
    def get_queryset(self):
        global author
        username  = self.kwargs.get('username')
        author = get_object_or_404(User,username = username )  
       
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
# end of start view 

class ArticlePreview(AuthorAccessMixin,DeleteView):
    template_name = "blog/article_detail.html"
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article,pk=pk)
    
    

class SearchList(ListView):
    paginate_by = 5
    template_name = 'blog/search_list.html'
    
    def get_queryset(self):
        global search
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains = search) | Q(title__icontains = search))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = search
        return context
    
