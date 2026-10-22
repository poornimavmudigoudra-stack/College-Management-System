from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import staff_required

from .forms import NoticeForm
from .models import Notice


def notice_list(request):
    notices = Notice.objects.for_user(request.user).select_related("posted_by")
    q = request.GET.get("q", "").strip()
    if q:
        notices = notices.filter(Q(title__icontains=q) | Q(content__icontains=q))
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "page_obj": Paginator(notices, 10).get_page(request.GET.get("page")),
        "q": q,
        "querystring": params.urlencode(),
    }
    return render(request, "notices/notice_list.html", context)


def notice_detail(request, pk):
    notice = get_object_or_404(Notice.objects.for_user(request.user).select_related("posted_by"), pk=pk)
    user = request.user
    can_delete = user.is_authenticated and (user.is_admin_user or notice.posted_by_id == user.id)
    return render(request, "notices/notice_detail.html", {"notice": notice, "can_delete": can_delete})


@staff_required
def notice_add(request):
    form = NoticeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        notice = form.save(commit=False)
        notice.posted_by = request.user
        notice.save()
        messages.success(request, "Notice published.")
        return redirect("notices:detail", pk=notice.pk)
    return render(request, "notices/notice_add.html", {"form": form})


@staff_required
@require_POST
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if not (request.user.is_admin_user or notice.posted_by_id == request.user.id):
        messages.error(request, "You can only delete notices you posted.")
        return redirect("notices:detail", pk=pk)
    notice.delete()
    messages.success(request, "Notice deleted.")
    return redirect("notices:list")
