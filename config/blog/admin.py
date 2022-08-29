from django.contrib import admin
from .models import Article,Category,IPAddress
from account.models import User


# admin  header change
admin.site.site_header = "وبلاگ جنگویی علی"
# end of admin  header change


#  my actions for articles

def make_published(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status="p")
    if rows_updated ==1 :
        message_bit = 'منتشر شد.'
    else:
        message_bit = 'منتشر شدند'
    modeladmin.message_user(request,f"{rows_updated}مقاله {message_bit}")
    
make_published.short_description ="انتشار مقالات انتخاب شده"
    
def make_draft(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status="d")
    if rows_updated ==1 :
        message_bit = 'پیش نویس شد.'
    else:
        message_bit = 'پیش نویس شدند'
    modeladmin.message_user(request,f"{rows_updated}مقاله {message_bit}") 
    
make_draft.short_description ="پیش نویس شدن مقالات انتخاب شده"    

#  end of my actions articles

#  my actions for category

def make_true(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status=True)
    if rows_updated == 1 :
        message_bit = 'نمایش داده شد.'
    else:
        message_bit = 'نمایش داده شدند'
    modeladmin.message_user(request,f"{rows_updated}دسته بندی {message_bit}")
    
make_true.short_description = "نمایش  دادن دسته بندی ها"
    
def make_false(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status=False)
    if rows_updated == 1 :
        message_bit = 'نمایش داده نمیشه.'
    else:
        message_bit = "نمایش داده نمیشوند"
    modeladmin.message_user(request,f"{rows_updated}دسته بندی {message_bit}") 
    
make_false.short_description = "نمایش ندادن دسته بندی ها"  

#  end of my actions category

# Page category
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('position','title','slug','status')
    list_filter = (['status'])
    search_fields =  ('title','slug')
    prepopulated_fields = {'slug':('title',)}
    actions = [make_true,make_false]
   
admin.site.register(Category,CategoryAdmin) 
# end of Page category

# page articles
class ArticleAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
    list_display = ('title','thumbnail_tag','author','slug','jpublish','is_special','status','category_to_str')
    list_filter = ('publish', 'status','author')
    search_fields =  ('title','descriptoin')
    prepopulated_fields = {'slug':('title',)} 
    ordering =['-status','-publish']
    actions = [make_published,make_draft]

    
    
admin.site.register(Article,ArticleAdmin)

#end of page articles
admin.site.register(IPAddress)