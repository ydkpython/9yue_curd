from django.template import Library
register = Library()
#上面这两条是自定制http页面中的函数
# @register.simple_tag() 被它装饰的函数对参数个数没有限制,但是它装饰的函数不能再if语句中出现,即不能作为判断条件使用
# @register.filter()被它装饰的函数最多俩个参数切显示是:参数2|func:参数1,优点是可以作为判断条件
# @register.inclusion_tag()能导入模板,通过模板渲染后再返回
def inner(result_list,list_display,ygadmin_obj):
    for row in result_list:
        yield [name(ygadmin_obj,row) if callable(name) else getattr(row,name) for name in list_display]

def inner_title(list_display):
    for t in list_display:
        yield t.__name__ if callable(t) else t

def change_inner(result_list,list_display,ygadmin_obj):
    for row in list_display:
        if not callable(row):
            if row != 'id':
                yield (row,getattr(result_list,row))


@register.inclusion_tag("yg/md.html")
def func(result_list,list_display,ygadmin_obj):
    v = inner(result_list,list_display,ygadmin_obj)
    t = inner_title(list_display)

    return {'xx':v,'yy':t}

@register.inclusion_tag("yg/md_change.html")
def func1(result_list,list_display,ygadmin_obj):
    v = change_inner(result_list,list_display,ygadmin_obj)

    return {'xx':v}


@register.simple_tag
def my_format(str,mesg):
    return str.format(*mesg)