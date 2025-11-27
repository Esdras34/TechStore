from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from app.models import Desenvolvedor, Categoria, Produto, Compra, Contato

class FormDesenvolvedor(forms.ModelForm):
    class Meta:
        model = Desenvolvedor
        fields = "__all__"

class FormContato(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Seu nome', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com', 'class': 'form-control'}),
            'mensagem': forms.Textarea(attrs={'placeholder': 'Digite sua mensagem aqui...', 'rows': 5, 'class': 'form-control'}),
        }
    
class FormCategoria(forms.ModelForm):
    class Meta:
        model = Categoria 
        fields = ['nome']

class FormProduto(forms.ModelForm):
    class Meta:
        model = Produto 
        fields = ['nome', 'descricao', 'preco', 'foto', 'estoque', 'categoria']

        widgets = {
            'nome': forms.TextInput(attrs = {'placeholder': 'nome do produto'}),
            'foto': forms.FileInput(attrs = {'accept': 'image/*'})
        }

class formCompra(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['quantidade']

class FormRegistro(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Usuário',
            'password1': 'Senha',
            'password2': 'Confirmar Senha',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Escolha um nome de usuário'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Seu nome'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Seu sobrenome'})
        self.fields['email'].widget.attrs.update({'placeholder': 'seu@email.com'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Digite sua senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Digite a senha novamente'})
        
        # Remove os validadores de senha padrão (incluindo o de 8 caracteres)
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Apenas valida se a senha não está vazia
        if not password1:
            raise forms.ValidationError('A senha é obrigatória.')
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas não coincidem.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

