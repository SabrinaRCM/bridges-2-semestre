# bridges

### Resumo do Projeto
O projeto foi proposto pela empresa Necto qual a proposta foi criar uma interface que permita o usuário cadastrar todos os aspectos de seu ambiente de desenvolvimento como pessoas(nome e carga horária), projetos(nome e total de horas) e tarefas(descrição e duração). A interface contém também um gráfico gantt para visualização de tarefas.

### Tecnologias adotadas na solução

A linguagem principal escolhida foi python, foi usado o framework Django para construção da interface web integrando HTML, CSS e JavaScript, o gráfico gantt foi gerado usando a biblioteca Frappe Gantt, como banco de dados foi escolhido mysql que foi conectado ao python usando a biblioteca pymysql. Outras práticas foram aplicadas como boas práticas de python e conceitos de Scrum.

* Python 3.7 - Linguagem principal
* PyCharm e/ou Visual Studio Code - IDE
* FrameWork Django 3 - interface WEB
* MySQL - Banco de Dados
* Frappe Gantt - interface do gráfico gantt
* Conceitos do SCRUM - Norteador do Projeto
* Zen of Python - boas práticas para o Projeto
* Principais Bibliotecas Python:  
    **PyMySQL** - interação com nosso Banco de Dados;
    **Crispy Forms** - renderizar formulários com Bootstrap;
    **Import-export** - para importar e exportar arquivos de excel .csv;

### Contribuições individuais/pessoais

Como contribuição pessoal, fui responsável pela criação do front end do projeto, incluindo a implementação do gráfico Gantt. Os códigos foram fragmentados usando um renderizador de formulários chamado crispy forms, com ele conseguimos criar somente um cabeçalho e um rodapé e carrega-los nos templates HTML. Todas as telas são preenchidas com dados direto do banco de dados.Compartilharei a seguir algumas das telas e trechos de códigos utilizados. 

#### Tela de Login
<img src="login.png"/>

A tela acima foi gerada através do código: 
```HTML
```

#### Tela de projetos
<img src="projetos.png"/>

A tela acima foi gerada através do código: 
```HTML
```

#### Tela do gráfico Gantt
<img src="gantt.png"/>

A tela acima foi gerada através do código: 
```HTML
{% extends 'bridges_app/main.html' %}
{% load static %}

{% block title %}

<title>Bridges - Gantt</title>

{% endblock %}

{% block content %}


        <div class="container mt-5 pt-5">
          <div class="card" style="overflow: scroll">
            <svg id="gantt"></svg>
          </div>
        </div>     
...

...
 <!-- Gráfico de indicadores - Funcionários -->
    <div class="card-body">
      <div class="row">
        <!-- /.col -->
        <div class="container mt-5">
          <div class="col-md-7" style="margin-left: 200px;">
                <p class="text-center">
                    <strong>Indicador: Horas disponíveis para cada funcionário</strong>
                </p>
                {% for indicadores in indicadores %}
                <!-- /.progress-group -->
                <div class="progress-group mt-3">
                    {{indicadores.id_fun}} - {{indicadores.nom_fun}}
                    <span class="float-right">{% if indicadores.ocupacao == null %}0{% else %}{{indicadores.ocupacao}}%{% endif %}  (<b>{% if indicadores.duracao_tarefa == null %}0{% else %}{{indicadores.duracao_tarefa}}{% endif %}</b>/{{indicadores.limite}} hrs)</span>
                    <div class="progress progress-sm">
                        <div class="progress-bar {% if indicadores.ocupacao > 80 %}bg-danger{% else %}bg-primary{% endif %}" style="width:{{indicadores.ocupacao}}%"></div>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="col-md-7 mt-3"><br /><br /></div>
            <!-- /.progress-group -->
          </div>
          <!-- /.col -->
      </div>
      <!-- /.row -->
  </div>     
 {% endblock %}
```
#### O gráfico Gantt
Para a construção do gráfico foi usada o framework baseado em JavaScript [Frappe.io/gantt](https://github.com/frappe/gantt). O gráfico mostra o nome da tarefa, funcionário responsável, início e fim de uma tarefa, e porcentagem da tarefa. Dentro do gráfico é possível alterar a data de início e fim de uma tarefa em quantidade de dias, realocar a tarefa para outro dia e modificar a porcentagem de conclusão. Os dados são inseridos no gráfico por requisição POST no banco de dados como mostra o código a seguir:
``` HTML
...
<script>
          var tasks = [
            {% for agenda in agenda %}
                {
                id: '{{agenda.fk_tar_id}}',
                custom_class: 'gantt-color',
                name: '{{agenda.fk_tar}} - {{agenda.fk_fun}}',
                start: '{{ agenda.dt_inicio|date:"Y" }}-{{ agenda.dt_inicio|date:"m" }}-{{ agenda.dt_inicio|date:"d" }}',
                end: '{{ agenda.dt_fim|date:"Y" }}-{{ agenda.dt_fim|date:"m" }}-{{ agenda.dt_fim|date:"d" }}',
                progress: '{{agenda.prog_tar}}'
                },
            {% endfor %}
        ]
          var gantt = new Gantt('#gantt', tasks, {
            on_click: function (task) {
              console.log(task);
            },
            on_date_change: function(task, start, end) {

                // convertendo data para enviar alerta ao usuário
                var data_convertida  = ""
                var data_convertida2  = ""
                data_convertida = data_convertida.concat(start.getDate(), "/", start.getMonth()+1, "/", start.getFullYear())
                data_convertida2 = data_convertida2.concat(end.getDate(), "/", end.getMonth()+1, "/", end.getFullYear())
                // alert(data_convertida);

                // enviando o post para URL do django
                var xhr = new XMLHttpRequest();
                xhr.open("POST", '{% url 'update_gantt' %}', true);
                xhr.setRequestHeader('Content-Type', 'text/plain');
                xhr.send(JSON.stringify(task));
                alert('Data da tarefa "' + task.name + '" alterada com Sucesso!\n' + 'Novo Data de Início: ' + data_convertida + '\nNova Data de Fim: ' + data_convertida2)
            },
            on_progress_change: function(task, progress) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", '{% url 'update_gantt' %}', true);
                xhr.setRequestHeader('Content-Type', 'text/plain');
                xhr.send(JSON.stringify(task));
                alert('Progresso da tarefa ' + task.name + ' alterado para: ' + progress + '%' + ' com sucesso!')
            },
            on_view_change: function(mode) {
              console.log(mode);
            },
            view_mode: 'Day',
            language: 'ptBr',
            });
        </script>
...
```

### Aprendizados Efetivos

* **Python e Django** 
<p>Com a realização deste projeto foi possível aprimorar meus conhecimentos em python. Foi utilizado novamente a biblioteca Django para construir a interface Web mas dessa vez integrando ao crispy forms que auxiliou na renderização dos formulários.</p>


