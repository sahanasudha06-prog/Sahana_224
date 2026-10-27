
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404

from .models import Member
from .forms import MemberForm


def dashboard(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(is_active=True).count()

    context = {
        'total_members': total_members,
        'active_members': active_members,
    }

    return render(request, 'gym/dashboard.html', context)


def member_list(request):
    members = Member.objects.all().order_by('-joining_date')

    context = {
        'members': members,
        'today': date.today(),
    }

    return render(request, 'gym/member_list.html', context)


def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()

    return render(
        request,
        'gym/member_form.html',
        {
            'form': form,
            'editing': False,
        }
    )


def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)

    return render(
        request,
        'gym/member_form.html',
        {
            'form': form,
            'editing': True,
            'member': member,
        }
    )


def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        member.delete()
        return redirect('member_list')

    return render(
        request,
        'gym/member_confirm_delete.html',
        {'member': member}
    )
