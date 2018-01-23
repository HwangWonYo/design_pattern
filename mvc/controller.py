from flask import redirect, render_template, request, Flask
from werkzeug.exceptions import BadRequest, NotFound


import models

app = Flask(__name__, template_folder='views')


@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/shorten/')
def shorten():
    full_url = request.args.get('url')
    print(request.args)
    if not full_url:
        raise BadRequest()

    # short_url 프로퍼티와 함께 객체를 반환하는 모델
    url_model = models.Url.shorten(full_url)

    # 뷰에 데이터를 전달하고 화면 표시 메소드를 호출
    short_url = request.host + '/' + url_model.short_url
    return render_template('success.html', short_url=short_url)


@app.route('/<path:path>')
def redirect_to_full(path=''):
    """압축된 URL을 받아서 일치하는 원래 주소가 있다면 그 곳으로 사용자를 연결한다."""
    # full_url 프로퍼트와 함께 객체를 반환하는 모델
    url_model = models.Url.get_by_short_url(path)
    # 검증 모델 반환
    if not url_model:
        raise NotFound()

    return redirect(url_model.full_url)

if __name__ == "__main__":
    app.run(debug=True)


