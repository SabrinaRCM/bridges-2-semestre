from import_export import resources
from .models import Projetos
from .models import Tarefas

class ProjetoResource(resources.ModelResource):
    class Meta:
        model = Projetos
        fields = ['nom_pro']