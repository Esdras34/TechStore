from app.models import Pagina

def pagina_context(request):
    """Context processor para disponibilizar dados da Pagina em todos os templates"""
    pagina = Pagina.objects.first()
    return {'pagina': pagina}

