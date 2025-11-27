from django.shortcuts import render, redirect, get_object_or_404
from app.models import Desenvolvedor, Contato, Produto, Pagina, Pedido, CarouselImage
from app.forms import FormDesenvolvedor, FormContato, FormProduto, formCompra, FormRegistro
import requests
#restFrameWork
from rest_framework.decorators import api_view
from app.serializers import DesenvolvedorSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import matplotlib.pyplot as plt


# Create your views here.
def grafico(request):
    vendas_totais = Compra.objects.values('produto__nome').annotate(
        quantidade_vendida=Sum('quantidade')
    ).order_by('produto__nome')
 
    produtos = [venda['produto__nome'] for venda in vendas_totais]
    quantidade_vendida = [venda['quantidade_vendida'] for venda in vendas_totais]
 
    plt.figure(figsize=(10, 6))
    plt.bar(produtos, quantidade_vendida, color='b')
    plt.title('Quantidade de Vendas por Produto', fontsize=14)
    plt.xlabel('Produto', fontsize=12)
    plt.ylabel('Quantidade', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
 
    nome_arquivo_imagem = 'quantidade_vendas_por_produto.png'
    caminho_grafico = os.path.join(settings.MEDIA_ROOT, nome_arquivo_imagem)
 
    plt.savefig(caminho_grafico)
    plt.close()
 
    url_grafico = os.path.join(settings.MEDIA_URL, nome_arquivo_imagem)
    return render(request, 'grafico.html', {'grafico': url_grafico})
    
def getApi(request):
    dados = requests.get('https://fakestoreapi.com/products').json()
    return render (request, 'api.html',{'dadosapi':dados})




@api_view(['GET', 'POST'])
def getApiDev(request):
    if request.method == 'GET':
        desenvolvedores = Desenvolvedor.objects.all()
        serializer = DesenvolvedorSerializer(desenvolvedores, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DesenvolvedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
     
    
    
@api_view(['GET', 'DELETE', 'PUT'])
def getIdApiDev(request, id_dev):
    try:
        desenvolvedor = Desenvolvedor.objects.get(id = id_dev)
    except Desenvolvedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DesenvolvedorSerializer(desenvolvedor)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        desenvolvedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
         serializer = DesenvolvedorSerializer(desenvolvedor,data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def index(request):
    # Busca os dados da página do banco de dados
    pagina = Pagina.objects.first()  # Pega o primeiro registro (ou criar um se não existir)
    # Busca produtos em destaque (últimos 6 produtos ou produtos com estoque)
    produtos_destaque = Produto.objects.filter(estoque__gt=0).order_by('-criado_em')[:6]
    if not produtos_destaque.exists():
        produtos_destaque = Produto.objects.all()[:6]
    # Busca imagens do carrossel (apenas as ativas, ordenadas)
    carousel_images = CarouselImage.objects.filter(ativo=True).order_by('ordem', '-criado_em')
    context = {
        'pagina': pagina,
        'produtos_destaque': produtos_destaque,
        'carousel_images': carousel_images
    }
    return render(request, 'index.html', context)
    
def sobre(request):
    # Busca os dados da página do banco de dados
    pagina = Pagina.objects.first()
    context = {'pagina': pagina}
    return render(request, 'sobre.html', context)

def dev(request):
    devs = Desenvolvedor.objects.all().values()
    return render(request, 'desenvolvedores.html',{'desenvolvedores':devs})

def excluirDev(request, id_dev):
    dev = Desenvolvedor.objects.get(id=id_dev)
    dev.delete()
    return redirect('dev')

def salvarDev(request):
   formulario = FormDesenvolvedor(request.POST or None)
   if request.POST:
       if formulario.is_valid():
           formulario.save()
           return redirect('dev')
   return render(request, 'salvardev.html', {"form":formulario})

def editarDev(request, id_dev):
    dev = Desenvolvedor.objects.get(id=id_dev)
    formulario = FormDesenvolvedor(request.POST or None, instance=dev)
    if request.POST:
       if formulario.is_valid():
           formulario.save()
           return redirect('dev')
    return render(request, 'editardev.html', {"form":formulario})

# contatos
def contato(request):
    contatos = Contato.objects.all().values()
    pagina = Pagina.objects.first()
    return render(request, 'contato.html', {'contatos': contatos, 'pagina': pagina})

def salvarContato(request):
    if request.method == 'POST':
        formulario = FormContato(request.POST)
        if formulario.is_valid():
            try:
                contato = formulario.save()
                messages.success(request, f'Mensagem enviada com sucesso! Obrigado, {contato.nome}.')
                return redirect('contato')
            except Exception as e:
                messages.error(request, f'Erro ao salvar mensagem: {str(e)}')
        else:
            # Mostra os erros específicos do formulário
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        formulario = FormContato()
    
    return render(request, 'salvarContato.html', {"form": formulario})

def excluirContato(request, id_contato):
    contato = Contato.objects.get(id=id_contato)
    contato.delete()
    return redirect('contato')

#create your views here

def produtos(request):
    produtos = Produto.objects.all()
    pagina = Pagina.objects.first()
    return render(request, 'produtos.html', {'prods': produtos, 'pagina': pagina})


def salvarProduto(request):
    if request.POST:
        formulario = FormProduto(request.POST , request.FILES)
    
        if formulario.is_valid():
            formulario.save()
            return redirect('index')
    else:
        formulario = FormProduto()
    return render(request, 'salvar-produto.html', {'form': formulario})


@login_required(login_url='login')
def comprar(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        
        if produto.estoque < quantidade:
            messages.error(request, 'Quantidade solicitada excede o estoque disponível')
            return redirect('produtos')
        
        # Calcula o total
        total = quantidade * produto.preco
        
        # Cria o pedido
        pedido = Pedido.objects.create(
            usuario=request.user,
            produto=produto,
            quantidade=quantidade,
            total=total
        )
        
        # O método save() do modelo Pedido já atualiza o estoque automaticamente
        messages.success(request, f'Pedido realizado com sucesso! Total: R$ {total:.2f}')
        return redirect('produtos')
    
    else:
        formulario = formCompra()
        return render(request, 'comprar.html', {'form': formulario, 'produto': produto})

# Views de Login e Logout
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                # Redireciona para a página que o usuário tentou acessar ou para index
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('index')

# Views de Área Administrativa do Site
def admin_site_login(request):
    """Login específico para área administrativa do site"""
    if request.session.get('admin_site_logged_in'):
        return redirect('admin_site_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Verifica credenciais específicas
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@techstore.com')
        admin_password = getattr(settings, 'ADMIN_PASSWORD', 'admin123')
        
        if email == admin_email and password == admin_password:
            request.session['admin_site_logged_in'] = True
            request.session['admin_email'] = email
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('admin_site_dashboard')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    
    return render(request, 'admin_site_login.html')

def admin_site_logout(request):
    """Logout da área administrativa"""
    request.session.flush()
    messages.success(request, 'Você foi desconectado da área administrativa.')
    return redirect('index')

def admin_site_dashboard(request):
    """Dashboard administrativo - visualiza pedidos e mensagens"""
    # Verifica se está logado na área administrativa
    if not request.session.get('admin_site_logged_in'):
        messages.error(request, 'Você precisa fazer login para acessar esta área.')
        return redirect('admin_site_login')
    
    # Busca todos os pedidos ordenados por data (mais recentes primeiro)
    pedidos = Pedido.objects.all().order_by('-data')
    
    # Busca todas as mensagens de contato ordenadas por data (mais recentes primeiro)
    contatos = Contato.objects.all().order_by('-criado_em')
    
    context = {
        'pedidos': pedidos,
        'contatos': contatos,
        'total_pedidos': pedidos.count(),
        'total_contatos': contatos.count(),
    }
    
    return render(request, 'admin_site_dashboard.html', context)



@login_required
def perfil(request):
    """Exibe o histórico de pedidos do usuário logado"""
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-data')
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'perfil.html', context)

# View de Registro
def registro_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {username}!')
            # Faz login automático após registro
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FormRegistro()
    
    return render(request, 'registro.html', {'form': form})
