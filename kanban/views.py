
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import *
from .forms import IssueCreateForm, IssueEditForm


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
    board = board_from_path(path)
    issues = Issue.objects.filter(board=board, is_active=True)
    
    ctx = {
        'board': board,
        'issues': issues,
    }
    return render(request, 'kanban/board.html', ctx)


def done(request, path):
    """
    Mostra todas as issues Done.
    """
    ctx = {
        'issues': get_issues(path, 2)
    }
    return render(request, 'kanban/done.html', ctx)


def doing(request, path):
    """
    Mostra todas as issues Doing.
    """
    ctx = {
        'issues': get_issues(path, 1)
    }

    return render(request, 'kanban/doing.html')

def backlog(request, path):
    """
    Mostra as issues do backlog (i.e., no estado To-do)
    """
    ctx = {
        'issues': get_issues(path, 0)
    }
    return render(request, 'kanban/backlog.html', ctx)


def issue_detail(request, path, issue_id):
    """
    Mostra informações detalhadas da issue.
    """
    ctx = {
        'issue': board_from_path(path).issues.filter(id=issue_id),
    }
    return render(request, 'kanban/issue-detail.html', ctx)

def create_issue(request, path):
    """
    Cria uma issue.
    """
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
    if request.method == 'POST':
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.board = board
            issue.is_active = True
            issue.save()
    else:
        form = IssueEditForm()
        ctx = {
            'board': board,
            'form': form,
        }
        return render(request, 'kanban/board.html', ctx)

    ctx = {
        'board': board,
    }
    return render(request, 'kanban/board.html', ctx)


def board_from_path(path):
    return Board.objects.get_or_create(title=path)[0]

def get_issues(path, kind_number):
    board = board_from_path(path)
    return board.issues.filter(kind=kind_number)
