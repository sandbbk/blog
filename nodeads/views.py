from django.shortcuts import render, redirect
from .models import Group, Element
from .forms import ElementForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone



def mptt_list(request):
    groups = Group.objects.all()
    return render(request, "nodeads/mptt.html", {'groups': groups})


def group_detail(request, pk):
    groups = Group.objects.all()
    group = groups.get(pk=pk)
    group_childs = group.get_children()
    elements_gr = Element.objects.filter(group__pk=pk)
    elements = elements_gr.filter(is_modered='true')
    this_page = Paginator(elements, 2)
    num_page = request.GET.get('page')
    try:
        page_content = this_page.page(num_page)
    except PageNotAnInteger:
        page_content = this_page.page(1)
    except EmptyPage:
        page_content = this_page.page(this_page.page(this_page.num_pages))
    return render(request, 'nodeads/group_detail.html', {'group_childs': group_childs,
                                                         'group_child_count': group_childs.count(),
                                                         'elements_md_count': elements.count(),
                                                         'elements_gr_count': elements_gr.count(),
                                                         'groups': groups,
                                                         'elements': page_content,
                                                         'group': group,
                                                         'pk': pk})

def element_detail(request, pk):
    element = Element.objects.get(pk=pk)
    groups = Group.objects.all()
    return render(request, 'nodeads/element_detail.html', {'element': element, 'groups': groups})


def create_el(request, pk):
    if request.method == "POST":
        form = ElementForm(request.POST, request.FILES)
        if form.is_valid():
            element = form.save(commit=False)
            element.group = Group.objects.get(pk=pk)
            element.created_date = timezone.now()
            element.save()
            return redirect('group_detail', pk=pk)
    else:
        if request.user.is_authenticated:
            form = ElementForm()
            return render(request, 'nodeads/create_el.html', {'form': form})
        else:
            return render(request, 'nodeads/perm_deny.html')
