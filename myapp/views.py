from curses.ascii import HT
from urllib import response
from django.shortcuts import render, HttpResponse, redirect
import random
from django.views.decorators.csrf import csrf_exempt

topics = [
{'id': 1, 'title': 'routing', 'body':'Routing is ...'},
{'id': 2, 'title': 'view', 'body':'View is ...'},
{'id': 3, 'title': 'Model', 'body':'Model is ...'},
]

nextId = 4

def HTMLTemplate(articleTag):
    global topics   # topics를 전역변수로 선언
    ol = ''
    # 상세보기 화면에 나올 메시지를 ol에 담아 출력
    # a href: 눌렀을 때 다음 화면으로 넘어가도록 함, get 방식으로 서버에 접속함 (get: 데이터를 가져옴)
    # 게시글을 delete할 때는 (버튼을 누르자마자 서버의 데이터를 변경/수정) POST 방식을 사용해야 함
    
    for topic in topics:
        ol += f'<li><a href = "/read/{topic["id"]}">{topic["title"]}</a></li>'  # f: 태그 안에 중괄호를 넣었을 때, 안에 바로 변수 사용 가능

    return f'''
    <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>
            {articleTag}
            <ul>
                <li><a href="/create/">create</a></li>
                <li>
                    <form>
                </li>
            </ul>  
        </body>
    </html>
    '''
    
# Create your views here.
# Read 기능: 1.read hompage, 2. 상세보기
def index(request):
    article = '''<h2>Welcome</h2>
            Hello, Django'''
    return HttpResponse(HTMLTemplate(article))

    #return HttpResponse('Welcome!')     # HTTP를 이용해서 응답하기 위해 HttpResponse 객체 사용
    #return HttpResponse('<h1>Random</h1>'+str(random.random())) # 해당 페이지를 열 때마다 랜덤으로 숫자 출력

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):  # read(request, id)로 들어온 id 파라미터는 문자형이므로, int형으로 바꿔줘야 함
            article = f'<h2>{topic["title"]}<h2><body>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    print("request.method", request.method) # 터미널 창에 request method를 출력
    # request method가 GET 방식, POST 방식일 때 각각 다르게 처리

    # [title]
    # input type="text" 글자를 입력받을 수 있음
    # placeholder="title" 해당 칸에 무엇을 적어야하는지 흐린 색으로 알려줌. (글자 작성 시 사라짐)
    # <p> : 단락 나타내는 태그

    # [body]
    # textarea: 여러 줄 글자를 입력받을 수 있음

    # 제출버튼을 클릭했을 때, title, body에 담긴 정보를 서버의 원하는 path로 전송하기 위해서는 전체를 form 태그로 묶어야 함
    # submit을 눌렀을 때 보내고 싶은 path는 action의 속성으로 넣으면 됨
    
    # method = "" 를 선언하지 않으면, 기본적으로 GET 방식임
    global nextId
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+ str(nextId)   # 해당 게시글의 url
        nextId += 1
        return redirect(url)    # 게시글 상세보기 페이지를 return

