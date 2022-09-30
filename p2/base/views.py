from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg
from .models import Curso, Estudiante, EstudiantePreguntas, Prueba, Preguntas, Tema
from .forms import CursoForm, EstudianteForm, PruebaForm, PreguntasForm, UPreguntasForm, EstudiantePreguntasForm, TemaForm


def loginPage(request):
    calcular()
    page = 'login'
    if request.user.is_authenticated:
        return redirect('bienvenida')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'El usuario ingresado no existe')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('bienvenida')
        else:
            messages.error(request, 'El usuario o contraseña no existe')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    calcular()
    logout(request)
    return redirect('bienvenida')

def registerPage(request):
    calcular()
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('bienvenida')
        else:
            messages.error(request, 'Un error ha ocurrido durante el registro')
    return render(request, 'base/login_register.html', {'form': form})

def bienvenida(request):
    calcular()
    return render(request, 'base/bienvenida.html')

@login_required(login_url='login')
def listacursos(request):
    calcular()
    cursos = Curso.objects.all()
    cursos_count = cursos.count()
    context = {'cursos': cursos, 'cursos_count': cursos_count}
    return render(request, 'base/listacursos.html', context)

@login_required(login_url='login')
def crearCurso(request):
    calcular()
    form = CursoForm()
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listacursos')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def actualizarCurso(request, pk):
    calcular()
    curso = Curso.objects.get(id=pk)
    form = CursoForm(instance=curso)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('listacursos')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def eliminarCurso(request, pk):
    calcular()
    curso = Curso.objects.get(id=pk)
    if request.method == 'POST':
        curso.delete()
        return redirect('listacursos')
    return render(request, 'base/delete.html', {'obj':curso})

@login_required(login_url='login')
def curso(request, pk):
    calcular()
    curso = Curso.objects.get(id=pk)
    context = {'curso': curso}
    return render(request, 'base/curso.html', context)

@login_required(login_url='login')
def crearEstudiante(request, pk):
    calcular()
    curso = Curso.objects.get(id=pk)
    context = {'curso': curso}
    form = EstudianteForm()
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base/curso.html', context)
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def actualizarEstudiante(request, pk):
    calcular()
    estudiante = Estudiante.objects.get(id=pk)
    form = EstudianteForm(instance=estudiante)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('listacursos')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def eliminarEstudiante(request, pk):
    calcular()
    estudiante = Estudiante.objects.get(id=pk)
    if request.method == 'POST':
        estudiante.delete()
        return redirect('listacursos')
    return render(request, 'base/delete.html', {'obj':estudiante})

@login_required(login_url='login')
def listapruebas(request):
    calcular()
    pruebas = Prueba.objects.filter(user=request.user)
    pruebas_count = pruebas.count()
    context = {'pruebas': pruebas, 'pruebas_count':pruebas_count}
    return render(request, 'base/listapruebas.html', context)

@login_required(login_url='login')
def crearPrueba(request):
    calcular()
    form = PruebaForm()
    if request.method == 'POST':
        form = PruebaForm(request.POST)
        if form.is_valid():
            prueba = form.save(commit=False)
            prueba.user = request.user
            prueba.save()
            return redirect('listapruebas')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def actualizarPrueba(request, pk):
    calcular()
    prueba = Prueba.objects.get(id=pk)
    form = PruebaForm(instance=prueba)
    if request.method == 'POST':
        form = PruebaForm(request.POST, instance=prueba)
        if form.is_valid():
            form.save()
            return redirect('listapruebas')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def eliminarPrueba(request, pk):
    calcular()
    prueba = Prueba.objects.get(id=pk)
    if request.method == 'POST':
        prueba.delete()
        return redirect('listapruebas')
    return render(request, 'base/delete.html', {'obj':prueba})  

@login_required(login_url='login')
def prueba(request, pk):
    calcular()
    prueba = Prueba.objects.get(id=pk)

    '''esto es de mostrarstats'''
    '''es = Preguntas.objects.filter(prueba_id=pk).aggregate(average=Avg('acierto'))
    prueba.aciertoprueba = es['average']
    prueba.save()'''
    '''esto es de mostrarstats'''

    context = {'prueba': prueba}
    return render(request, 'base/prueba.html', context)

@login_required(login_url='login')
def crearPreguntas(request, pk):
    calcular()
    prueba = Prueba.objects.get(id=pk)
    context = {'prueba': prueba}
    form = PreguntasForm(user=request.user)
    if request.method == 'POST':
        form = PreguntasForm(request.POST, user=request.user)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.user = request.user
            pregunta.save()
            return render(request, 'base/prueba.html', context)
    context = {'form': form}
    return render(request, 'base/curso_form.html', context) 

@login_required(login_url='login')
def actualizarPreguntas(request, pk):
    calcular()
    pregunta = Preguntas.objects.get(id=pk)
    form = UPreguntasForm(instance=pregunta)
    if request.method == 'POST':
        form = UPreguntasForm(request.POST, instance=pregunta)
        if form.is_valid():
            form.save()
            return redirect('listapruebas')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def eliminarPreguntas(request, pk):
    calcular()
    pregunta = Preguntas.objects.get(id=pk)
    if request.method == 'POST':
        pregunta.delete()
        return redirect('listapruebas')
    return render(request, 'base/delete.html', {'obj':pregunta})

@login_required(login_url='login')
def relacionarPreguntas(request, pk):
    calcular()
    a = Preguntas.objects.get(id=pk)
    if request.method == 'POST':
        form = EstudiantePreguntasForm(request.POST, user=request.user)
        if form.is_valid():
            relacion = form.save(commit=False)
            relacion.user = request.user
            relacion.save()
            return redirect('listapruebas')
    else:
        form = EstudiantePreguntasForm(user=request.user)
    return render(request, 'base/curso_form.html', {'form': form, 'a':a})

@login_required(login_url='login')
def pregunta(response, pk):
    calcular()
    a = Preguntas.objects.get(id=pk)

    '''esto es de mostrarstats'''
    '''es = EstudiantePreguntas.objects.filter(preguntas_id=pk).aggregate(average=Avg('correcto'))
    a.acierto = es['average']
    a.save()'''
    '''esto es de mostrarstats'''

    if response.method == 'POST':
        print(response.POST)
        if response.POST.get('save'):
            for estudiantepreguntas in a.estudiantepreguntas_set.all():
                if response.POST.get('c' + str(estudiantepreguntas.id)) == 'clicked':
                    estudiantepreguntas.correcto = True
                else:
                    estudiantepreguntas.correcto = False
                estudiantepreguntas.save()
    return render(response, 'base/pregunta.html', {"a":a})

@login_required(login_url='login')
def eliminarRelacionPreguntas(request, pk):
    calcular()
    b = EstudiantePreguntas.objects.get(id=pk)
    if request.method == 'POST':
        b.delete()
        return redirect('listapruebas')
    return render(request, 'base/delete.html', {'obj':b})

@login_required(login_url='login')
def listatemas(request):
    calcular()
    temas = Tema.objects.all()
    context = {'temas': temas}
    return render(request, 'base/listatemas.html', context)

@login_required(login_url='login')
def crearTema(request):
    calcular()
    form = TemaForm()
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listatemas')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def actualizarTema(request, pk):
    calcular()
    tema = Tema.objects.get(id=pk)
    form = TemaForm(instance=tema)
    if request.method == 'POST':
        form = TemaForm(request.POST, instance=tema)
        if form.is_valid():
            form.save()
            return redirect('listatemas')
    context = {'form': form}
    return render(request, 'base/curso_form.html', context)

@login_required(login_url='login')
def eliminarTema(request, pk):
    calcular()
    tema = Tema.objects.get(id=pk)
    if request.method == 'POST':
        tema.delete()
        return redirect('listatemas')
    return render(request, 'base/delete.html', {'obj':tema})

def calcular():
    es = EstudiantePreguntas.objects.values('preguntas_id').annotate(average=Avg('correcto'))
    for x in es:
        a = Preguntas.objects.get(id=x['preguntas_id'])
        a.acierto = x['average']
        a.save()
    es = Preguntas.objects.values('prueba_id').annotate(average=Avg('acierto'))
    for x in es:
        a = Prueba.objects.get(id=x['prueba_id'])
        a.aciertoprueba = x['average']
        a.save()
    es = Preguntas.objects.values('tema_id').annotate(average=Avg('acierto'))
    for x in es:
        a = Tema.objects.get(id=x['tema_id'])
        a.aciertotema = x['average']
        a.save()
    es = EstudiantePreguntas.objects.values('estudiante_id').annotate(average=Avg('correcto'))
    for x in es:
        a = Estudiante.objects.get(id=x['estudiante_id'])
        a.aciertoestudiante = x['average']
        a.save()