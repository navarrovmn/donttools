
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import IssueCreateForm, IssueEditForm
import json
from django.http import JsonResponse


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

    ctx = {
        'board': board,
        'path': path,
        'todo': get_issues(board, 0),
        'doing': get_issues(board, 1),
        'done': get_issues(board, 2)
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
    form = IssueCreateForm()

    if request.method == 'POST':
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.board = board
            issue.is_active = True
            issue.kind = 0
            issue.save()
            return redirect('/' + path)

    ctx = {
        'board': board,
        'form': form,
    }
    return render(request, 'kanban/board.html', ctx)


def issue_edit(request, path, issue_id):
    """
    Edita issue.
    """

@csrf_exempt
def update_kind(request):
    """
    Update issue kind.
    """
    kinds = {
        "todo": 0,
        "doing": 1,
        "done": 2
    }
    data = json.loads(request.body.decode("utf-8"))
    issue = Issue.objects.get(id=data["issue_id"])
    issue.kind = kinds[data["new_kind"]]
    issue.save()
    return JsonResponse({"result": "ok"})

def board_from_path(path):
    return Board.objects.get_or_create(title=path)[0]

def get_issues(path, kind_number):
    board = board_from_path(path)
    return board.issues.filter(kind=kind_number)
