from django import template
from ..models import Category,Article
from django.db.models import Count,Q
from datetime import datetime,timedelta

register = template.Library()

@register.simple_tag
def title():
    return "وبلاگ علی"

@register.inclusion_tag('blog/partials/category_navbar.html')
def cetagory_navbar():
    return  {
        'category': Category.objects.filter(status=True),
    }
    
    
@register.inclusion_tag('registration/partials/link.html')
def link(request,link_name,content,name_js):
    return {
        "request":request,
        "link_name":link_name,
        'link': 'account:{}'.format(link_name),
        "content":content,
        "name_js":name_js,

    }
    
@register.inclusion_tag('blog/partials/popular_articles.html')
def popular_articles():
    last_month = datetime.today() - timedelta(days=30)
    return  {
        'popular_articles':  Article.objects.published().annotate(
        count = Count('hits',filter=Q(articlehit__created__gt = last_month))).order_by('-count',"-publish")[:5]
    }
    