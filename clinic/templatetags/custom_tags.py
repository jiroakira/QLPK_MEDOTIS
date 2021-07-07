from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()

register = template.Library()

@register.simple_tag
def danh_sach_bac_si_lam_sang():
    return User.objects.filter(chuc_nang = '3')

@register.simple_tag(takes_context=True)
def check_user_perm(context, *args, **kwargs):
    try:
        request = context['request']
        perm_codename = kwargs['perm_codename']
        
        user_obj = request.user
    
        permissions = Permission.objects.filter(group__user=user_obj)

        flag = False

        if user_obj.is_superuser:
            flag = True
        for p in permissions:
            if perm_codename.lower() == p.codename.lower():
                flag = True
        return flag
    except Exception as e:
        return ""