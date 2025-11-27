from django.contrib import admin
from app.models import Categoria, Produto, Compra, Pagina, Contato, Pedido, CarouselImage


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao", "preco", "foto", "estoque", "categoria", "criado_em", "atualizado_em")
    list_filter = ("categoria", "criado_em", "atualizado_em")
    search_fields = ("nome", "descricao")
    list_editable = ("preco", "estoque")
    readonly_fields = ("criado_em", "atualizado_em")
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'categoria', 'foto')
        }),
        ('Detalhes do Produto', {
            'fields': ('descricao', 'preco', 'estoque')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    # Apenas superusuários podem acessar Produto (CRUD completo)
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

class CompraAdmin(admin.ModelAdmin):
    list_display = ("produto", "quantidade", "data", "total")

class PaginaAdmin(admin.ModelAdmin):
    list_display = ("nome_do_site", "email", "whatsapp", "criado_em", "atualizado_em")
    readonly_fields = ("criado_em", "atualizado_em")
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_do_site', 'logo_do_site')
        }),
        ('Conteúdo da Página', {
            'fields': ('texto_chamada', 'texto_sobre', 'imagem_sobre')
        }),
        ('Informações de Contato', {
            'fields': ('endereco', 'email', 'whatsapp')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    # Apenas superusuários podem acessar Pagina (CRUD completo)
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

class ContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "criado_em")
    readonly_fields = ("criado_em", "nome", "email", "mensagem")
    list_filter = ("criado_em",)
    search_fields = ("nome", "email", "mensagem")
    
    # Apenas superusuários podem ver as mensagens de Contato (apenas leitura)
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser
    
    # Admin só pode ler, não pode criar, editar ou deletar
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class PedidoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "produto", "quantidade", "total", "data")
    readonly_fields = ("data", "total")
    list_filter = ("data", "produto")

class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ordem", "ativo", "criado_em")
    list_filter = ("ativo", "criado_em")
    list_editable = ("ordem", "ativo")
    search_fields = ("titulo", "descricao")
    readonly_fields = ("criado_em",)
    fieldsets = (
        ('Imagem', {
            'fields': ('imagem',)
        }),
        ('Informações', {
            'fields': ('titulo', 'descricao')
        }),
        ('Configurações', {
            'fields': ('ordem', 'ativo')
        }),
        ('Data', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    
    # Apenas superusuários podem acessar CarouselImage (CRUD completo)
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(Pagina, PaginaAdmin)
admin.site.register(Contato, ContatoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(CarouselImage, CarouselImageAdmin)
