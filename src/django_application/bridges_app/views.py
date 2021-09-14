from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import CreateTaskForm, CreateProjectForm, CreateWorkerForm, CreateScheduleForm
from datetime import timedelta, date, datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from tablib import Dataset
from .resources import ProjetoResource
import logging
import json
import pymysql.cursors


# Create your views here.

# instance of a logger
logger = logging.getLogger(__name__)


@login_required
def gantt(request):
    agenda = Agenda.objects.all()
    funcionarios = Funcionarios.objects.all()
    indicadores = Funcionarios.objects.raw(
        'SELECT m.id_fun, ((m.monday + m.tuesday + m.wednesday + m.thursday + m.friday + m.saturday + m.sunday) * hour(m.horas_limite) * 4) as limite, '
        'round(SUM(j.dur_tar_hours),0) as duracao_tarefa, '
        'round(((SUM(j.dur_tar_hours) / ((m.monday + m.tuesday + m.wednesday + m.thursday + m.friday + m.saturday + m.sunday) * hour(m.horas_limite) * 4)) * 100),0) as ocupacao '
        'FROM bridges_app_funcionarios m '
        'LEFT JOIN bridges_app_agenda d '
        'ON m.id_fun = d.fk_fun_id '
        'LEFT JOIN bridges_app_tarefas j '
        'ON d.fk_tar_id = j.id_tar '
        'GROUP BY m.id_fun;')

    context = {'agenda': agenda, 'funcionarios': funcionarios, 'indicadores': indicadores}
    return render(request, 'bridges_app/gantt.html', context)


@login_required
def tarefas(request):
    tarefas = Tarefas.objects.all().order_by('-id_tar')
    total_tarefas = tarefas.count()
    projetos = Projetos.objects.all()
    create_form = CreateTaskForm(request.POST or None)

    if create_form.is_valid():
        create_form.save()
        task_name = create_form.cleaned_data.get('nom_tar')
        messages.success(request, 'Tarefa "' + task_name + '" cadastrada com Sucesso!')
        return redirect('/tarefas')

    context = {'tarefas': tarefas, 'total_tarefas': total_tarefas, 'projetos': projetos, 'create_form': create_form}
    return render(request, 'bridges_app/tarefas.html', context)


@login_required
def update_task(request, pk):
    task = Tarefas.objects.get(id_tar=pk)
    create_form = CreateTaskForm(instance=task)

    if request.method == "POST":
        create_form = CreateTaskForm(request.POST, instance=task)
        if create_form.is_valid():
            create_form.save()
            return redirect('/tarefas')

    context = {'create_form': create_form}
    return render(request, 'bridges_app/update_tarefa.html', context)


@login_required
def delete_task(request, pk):
    task = Tarefas.objects.get(id_tar=pk)

    if request.method == "POST":
        task.delete()
        return redirect('/tarefas')

    context = {'task': task}
    return render(request, 'bridges_app/delete_tarefa.html', context)


@login_required
def projetos(request):
    projetos = Projetos.objects.raw('SELECT m.id_pro, m.nom_pro, '
                                    'sum(n.dur_tar_hours) + (sum(dur_tar_min) DIV 60) as total_hours, '
                                    'MOD(sum(dur_tar_min), 60) as total_minutes '
                                    'FROM bridges_app_projetos m '
                                    'LEFT JOIN bridges_app_tarefas n on  m.id_pro =  n.fk_pro_id GROUP by m.id_pro')
    total_projetos = Projetos.objects.all().count()
    create_form = CreateProjectForm(request.POST or None)

    if create_form.is_valid():
        project_name = create_form.cleaned_data.get('nom_pro')
        messages.success(request, 'Projeto "' + project_name + '" cadastrado com Sucesso!')
        create_form.save()
        return redirect('/projetos')


    context = {'projetos': projetos, 'create_form': create_form, 'total_projetos': total_projetos}
    return render(request, 'bridges_app/projetos.html', context)


@login_required
def update_project(request, pk):
    project = Projetos.objects.get(id_pro=pk)
    create_form = CreateProjectForm(instance=project)

    if request.method == "POST":
        create_form = CreateProjectForm(request.POST, instance=project)
        if create_form.is_valid():
            create_form.save()
            return redirect('/projetos')

    context = {'create_form': create_form}
    return render(request, 'bridges_app/update_projeto.html', context)


@login_required
def delete_project(request, pk):
    project = Projetos.objects.get(id_pro=pk)

    if request.method == "POST":
        project.delete()
        return redirect('/projetos')

    context = {'project': project}
    return render(request, 'bridges_app/delete_projeto.html', context)


@login_required
def funcionarios(request):
    funcionarios = Funcionarios.objects.all().order_by('-id_fun')
    #funcionarios = Funcionarios.objects.all().annotate(week_count='monday')).order_by('-id_fun')
    total_funcionarios = funcionarios.count()

    create_form = CreateWorkerForm(request.POST or None)
    if create_form.is_valid():
        worker_name = create_form.cleaned_data.get('nom_fun')
        messages.success(request, 'Funcionário(a) "' + worker_name + '" cadastrado(a) com Sucesso!')
        create_form.save()
        return redirect('/funcionarios')

    context = {'funcionarios': funcionarios, 'total_funcionarios': total_funcionarios, 'create_form': create_form}
    return render(request, 'bridges_app/funcionarios.html', context)

@login_required
def update_worker(request, pk):
    worker = Funcionarios.objects.get(id_fun=pk)
    create_form = CreateWorkerForm(instance=worker)

    if request.method == "POST":
        create_form = CreateWorkerForm(request.POST, instance=worker)
        if create_form.is_valid():
            create_form.save()
            return redirect('/funcionarios')

    context = {'create_form': create_form}
    return render(request, 'bridges_app/update_funcionario.html', context)

@login_required
def delete_worker(request, pk):
    worker = Funcionarios.objects.get(id_fun=pk)

    if request.method == "POST":
        worker.delete()
        return redirect('/funcionarios')

    context = {'worker': worker}
    return render(request, 'bridges_app/delete_funcionario.html', context)


@login_required
def agenda(request):
    schedules = Agenda.objects.all().order_by('-fk_tar')
    total_schedules = schedules.count()
    funcionarios = Funcionarios.objects.all()
    create_form = CreateScheduleForm(request.POST or None)

    if create_form.is_valid():
        create_form = create_form.save(commit=False)

        # trazendo variaveis para um momento anterior ao INSERT no banco a fim de projetar da data final

        #  dados do  funcionario (horas  em decimal)
        horas_dia = Funcionarios.objects.values_list('horas_limite').filter(id_fun=create_form.fk_fun_id).first()[0].hour
        minutos_dia = Funcionarios.objects.values_list('horas_limite').filter(id_fun=create_form.fk_fun_id).first()[0].minute/60
        horas_dia_float = horas_dia + minutos_dia
        dias_da_semana = Funcionarios.objects.values_list('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                                                          'saturday', 'sunday').filter(id_fun=create_form.fk_fun_id).first()
        # dados  da tarefa
        duracao_tarefa = float(Tarefas.objects.values_list('dur_tar_hours').filter(id_tar=create_form.fk_tar_id).first()[0])

        # calculando quantos dias de trabalho o funcionário em questão vai demorar para concluir
        days_to_finish = round(duracao_tarefa / horas_dia_float, 0)

        # startando data_fim com o valor informado para inicio da atividade (a finalidade é somar a partir desse)
        data_fim = create_form.dt_inicio

        # calculo da data final. regra: se não trabalha no dia, soma-se um dia porém não contabiliza como "trabalhado"
        contador = 0
        while contador < days_to_finish:
            week_day = data_fim.weekday()
            if dias_da_semana[week_day] is True:
                data_fim = data_fim + timedelta(days=1)
                contador = contador + 1
            else:
                data_fim = data_fim + timedelta(days=1)

        # corrigindo projeção de data (termina no ultimo dia, não no proximo)
        if data_fim != create_form.dt_inicio:
            data_fim = data_fim - timedelta(days=1)

        create_form.dt_fim = data_fim
        create_form.save()
        messages.success(request, 'Agendamento realizado com Sucesso!')
        return redirect('/agenda')

    context = {'schedules': schedules, 'total_schedules': total_schedules, 'funcionarios': funcionarios, 'create_form': create_form}
    return render(request, 'bridges_app/agenda.html', context)


@login_required
def update_schedule(request, pk):
    schedule = Agenda.objects.get(id=pk)
    create_form = CreateScheduleForm(instance=schedule)

    if request.method == "POST":
        create_form = CreateScheduleForm(request.POST, instance=schedule)
        if create_form.is_valid():
            create_form = create_form.save(commit=False)
            create_form.dt_fim = create_form.dt_inicio + timedelta(days=1)
            create_form.save()
            return redirect('/agenda')

    context = {'create_form': create_form}
    return render(request, 'bridges_app/update_agendamento.html', context)


@login_required
def delete_schedule(request, pk):
    schedule = Agenda.objects.get(id=pk)

    if request.method == "POST":
        schedule.delete()
        return redirect('/agenda')

    context = {'schedule': schedule}
    return render(request, 'bridges_app/delete_agendamento.html', context)


def logout_request(request):
    logout(request)
    return redirect("/")


@login_required
@csrf_exempt
def update_gantt(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        dt_fim = received_json_data['_end'][0:10]
        dt_fim = datetime.strptime(dt_fim, '%Y-%m-%d') + timedelta(days=-1)
        # logger.error(dt_fim)
        # print(type(dt_fim))
        dt_inicio = received_json_data['_start'][0:10]
        # logger.error(dt_inicio)
        id_tarefa = received_json_data['id']
        # logger.error(id_tarefa)
        prog_tarefa = received_json_data['progress']
        nova_agenda = Agenda.objects.all().filter(fk_tar_id=id_tarefa)
        nova_agenda.update(dt_fim=dt_fim, dt_inicio=dt_inicio, prog_tar=prog_tarefa)
        # print(received_json_data)
        return HttpResponse('it was post request')

    return HttpResponse('done')

@login_required
def import_excel(request):
    
        if request.method == 'POST':
            projeto_resource = ProjetoResource()
            dataset = Dataset()
            new_project = request.FILES['myfile']

            imported_data = dataset.load(new_project.read(),format='xlsx')
            #print(imported_data)
            #nome = dataset[0][0]
            #print(nome)
            connection = pymysql.connect(host='localhost',
                             user='bridges_dev',
                             password='123456',
                             db='bridges',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

            for data in imported_data:
                Nprojeto = data[0]
                DescTarefa = data[1]
                HoraTarefa = data[2]
                MinTarefa = data[3]
                try:
                    with connection.cursor() as cursor:

                        sql = "INSERT INTO `bridges_app_projetos` (nom_pro) VALUES (%s)"
                        cursor.execute(sql, (Nprojeto))
                        connection.commit()

                        sql = "select id_pro from bridges_app_projetos where nom_pro = %s order by id_pro limit 1"
                        cursor.execute(sql, (Nprojeto))
                        result = cursor.fetchone()
                        print(result["id_pro"])

                        
                        
                        sql = "INSERT INTO `bridges_app_tarefas` (nom_tar, fk_pro_id, dur_tar_min, dur_tar_hours) VALUES (%s, %s, %s, %s)"
                        print(sql)
                        idpro = result["id_pro"]
                        cursor.execute(sql, (DescTarefa, idpro , MinTarefa, HoraTarefa))
                        connection.commit()
                        messages.success(request, 'Excel importado com Sucesso!')
                except:
                    print(":(")

            
            connection.close()
            



        return render(request, 'bridges_app/import_excel.html')
        

    

