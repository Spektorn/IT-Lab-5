from django.shortcuts import render, redirect
from django.http import Http404
from .models import Article

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    
    except Article.DoesNotExist:
        raise Http404
    
def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # Обработать данные формы, если метод POST:
            # В словаре form будет храниться информация, введенная пользователем
            form = {
                'title': request.POST["title"],
                'text': request.POST["text"],
            }
            
            if form["title"] and form["text"]:
                # Если поля заполнены:
                if not Article.objects.filter(title=form["title"]):
                    # Если поле заголовка статьи является уникальным:
                    # создать пост и перейти на его страницу
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id=Article.objects.get(text=form["text"], title=form["title"], author=request.user ).id)
                else:
                    # Если поле заголовка статьи не является уникальным:
                    form['errors'] = u"Название статьи не является уникальным"
                    return render(request, 'create_post.html', {'form': form})
            else:
                # Если введенные данные неполны:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # иначе просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404
