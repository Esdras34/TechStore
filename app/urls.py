from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('sobre', views.sobre, name='sobre'),
    path('desenvolvedores', views.dev, name='dev'),
    path('excluir-dev/<int:id_dev>', views.excluirDev, name='excluirDev'),
    path('salvar-dev', views.salvarDev, name='salvarDev'),
    path('editar-dev/<int:id_dev>', views.editarDev, name='editarDev'),


    path('contatos', views.contato, name='contato'),
    path('salvar-contato', views.salvarContato, name='salvarContato'),
    path('excluir-contato/<int:id_contato>', views.excluirContato, name='excluirContato'),

    path('api', views.getApi, name='getApi'),


    path ('api-desenvolvedores', views.getApiDev, name= 'getApiDev'),
    path ('api-desenvolvedores/<int:id_dev>', views.getIdApiDev, name= 'getIdApiDev'),

    path ('salvar-produto', views.salvarProduto, name= 'salvarProduto'),
    path ('produtos', views.produtos, name= 'produtos'),
    path('comprar/<int:id_produto>', views.comprar, name='comprar'),

    path('perfil/', views.perfil, name='perfil'),

    path('grafico', views.grafico, name='grafico'),
    
    # Login, Logout e Registro
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    # Área Administrativa do Site
    path('admin-site/login/', views.admin_site_login, name='admin_site_login'),
    path('admin-site/logout/', views.admin_site_logout, name='admin_site_logout'),
    path('admin-site/dashboard/', views.admin_site_dashboard, name='admin_site_dashboard'),
]
