from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from .forms import MovieForm, ReviewForm

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'reviews/movie_list.html', {'movies': movies})

def movie_list(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        message = None if movies.exists() else "Filmi nuk u gjend."
    else:
        movies = Movie.objects.all()
        message = None

    return render(request, 'reviews/movie_list.html', {
        'movies': movies,
        'message': message,
    })
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = ReviewForm()
    return render(request, 'reviews/movie_detail.html', {'movie': movie, 'form': form})

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'reviews/movie_form.html', {'form': form})

def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'reviews/movie_form.html', {'form': form})

def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'reviews/movie_confirm_delete.html', {'movie': movie})
