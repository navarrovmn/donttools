from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from .forms import IssueCreateForm


def index(request):
    """
    Página inicial.
    """
    return render(request, 'kanban/index.html', {})


def board(request, path):
    """
    Mostra um quadro Kanban completo com as colunas de To-do, Doing e Done.

    Oculta as issues escondidas.
    """
    ctx = {
        'board': board_from_path(path),
    }
    return render(request, 'kanban/board.html', ctx)


def done(request, path):
    """
    Mostra todas as issues Done.
    """
    ctx = {
        'board': board_from_path(path),
    }
    return render(request, 'kanban/done.html', ctx)


def backlog(request, path):
    """
    Mostra as issues do backlog (i.e., no estado To-do)
    """
    ctx = {
        'board': board_from_path(path),
    }
    return render(request, 'kanban/backlog.html', ctx)


def issue_detail(request, path, issue_id):
    """
    Mostra informações detalhadas da issue.
    """
    ctx = {
        'board': board_from_path(path),
    }
    return render(request, 'kanban/issue-detail.html', ctx)


def create_issue(request, path):
    """
    Cria uma issue.
    """
    print("8"*800)
    print(request)
    print(dir(request))

    board = board_from_path(path)

    if request.method == 'POST':
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.board = board
            issue.is_active = True
            issue.save()
    else:
        form = IssueCreateForm()
        ctx = {
            'board': board,
            'form': form,
        }
        return render(request, 'kanban/board.html', ctx)

    ctx = {
        'board': board,
    }

    return render(request, 'kanban/board.html', ctx)


def issue_edit(request, path, issue_id):
    """
    Edita issue.
    """
    ctx = {
        'board': board_from_path(path),
    }
    return render(request, 'kanban/issue-edit.html', ctx)


def board_from_path(path):
    return Board.objects.get_or_create(title=path)[0]