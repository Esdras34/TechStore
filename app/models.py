from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Desenvolvedor(models.Model):
    nome = models.CharField(max_length=100)
    funcao = models.CharField(max_length=50)
    descricao = models.CharField(max_length=300)
    email = models.CharField(unique=True)

class Pagina(models.Model):
    """Armazena dados institucionais e informações exibidas na página inicial."""
    nome_do_site = models.CharField(max_length=200, verbose_name="Nome do Site")
    logo_do_site = models.ImageField(upload_to='pagina/', null=True, blank=True, verbose_name="Logo do Site")
    texto_chamada = models.TextField(verbose_name="Texto de Chamada")
    texto_sobre = models.TextField(verbose_name="Texto Sobre")
    imagem_sobre = models.ImageField(upload_to='pagina/', null=True, blank=True, verbose_name="Imagem Sobre")
    endereco = models.CharField(max_length=300, verbose_name="Endereço")
    email = models.EmailField(verbose_name="E-mail")
    whatsapp = models.CharField(max_length=20, verbose_name="WhatsApp")
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"

    def __str__(self):
        return self.nome_do_site

class Contato(models.Model):
    """Armazena as mensagens enviadas pelo formulário de contato."""
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    mensagem = models.TextField(verbose_name="Mensagem")
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"

    def __str__(self):
        return f"{self.nome} - {self.email}"

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique= True)


    def __str__(self):
     return self.nome

class Produto(models.Model):
    """Armazena os produtos disponíveis para compra."""
    nome = models.CharField(max_length=100, verbose_name="Nome")
    estoque = models.PositiveIntegerField(default=0, verbose_name="Estoque")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    descricao = models.TextField(max_length=500, verbose_name="Descrição")
    foto = models.ImageField(upload_to='produtos/', null=True, blank=True, verbose_name="Foto")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    """Registra os pedidos realizados pelos usuários, atualizando o estoque do produto."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", default=0)
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username} - {self.produto.nome}"

    def save(self, *args, **kwargs):
        # Calcula o total antes de salvar
        self.total = self.quantidade * self.produto.preco
        # Atualiza o estoque do produto
        if self.produto.estoque >= self.quantidade:
            self.produto.estoque -= self.quantidade
            self.produto.save()
        super().save(*args, **kwargs)

# Mantendo Compra para compatibilidade com código existente
class Compra(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.quantidade * self.produto.preco

class CarouselImage(models.Model):
    """Armazena as imagens do carrossel da página inicial."""
    imagem = models.ImageField(upload_to='carousel/', verbose_name="Imagem")
    titulo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem de Exibição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(default=timezone.now, verbose_name="Criado em")

    class Meta:
        verbose_name = "Imagem do Carrossel"
        verbose_name_plural = "Imagens do Carrossel"
        ordering = ['ordem', '-criado_em']

    def __str__(self):
        return self.titulo if self.titulo else f"Imagem #{self.id}"

