from flask import Flask, render_template , url_for, request, redirect , flash, session
from database import DBhandler
import hashlib
import sys

app = Flask(__name__)
app.config["SECRET_KEY"]="helloosp"
DB = DBhandler()


@app.route('/')
def index():
    #return render_template('index.html')
    return redirect(url_for('view_list'))

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/product-add') 
def productAdd():
    return render_template('product_add.html')


@app.route('/add-product-post', methods=["POST"])
def registerproduct():
    print(request.form)  # 확인용 출력
    print(request.files)  # 확인용 출력
    image_file = request.files["img_path"]
    image_file.save("static/img/{}".format(image_file.filename))
    data = {
        "product_description": request.form.get("product-description"),
        "product_place": request.form.get("product-place"),
        "product_number": request.form.get("product-number"),
        "product_category": request.form.get("product-category"),
        "start_date": request.form.get("start-date"),
        "end_date": request.form.get("end-date"),
        "img_path": "static/img/" + image_file.filename
    }
    DB.insert_item(data['product_category'], data, image_file.filename)
    return render_template("products_list.html", data={ "img_path": "static/img/" + image_file.filename, **data })

@app.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page = 6  # item count to display per page
    per_row = 3  # item count to display per row   
    start_idx=per_page*page
    end_idx=per_page*(page+1)
   
    data = DB.get_items()  # read the table
    
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    
    row_data = [list(data.items())[i * per_row:(i + 1) * per_row] for i in range(per_page // per_row)]
    
@app.route('/signup1')
def signup1():
    return render_template('signup1.html')

@app.route('/signup1_post', methods=["POST"])
def register_user_1():
    data = request.form
    password1 = request.form['password1']
    pw_hash = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("signup2.html")
    else:
        return render_template("signup1.html")

@app.route('/signup2')
def signup2():
    return render_template('signup2.html')

@app.route('/signup2_post', methods=["POST"])
def register_user_2():
    data = {
        "nickname": request.form.get("nickname"),
        "profile-img": request.form.get("profile-img")
    }
    if DB.insert_user2(data):
        return render_template("signup3.html")

   
@app.route("/view_detail/<name>/")
def view_item_detail(name):
        data = DB.get_item_byname(str(name))
        return render_template("detail.html", name=name, data=data)


@app.route("/product-detail")
def productDetail():
    return render_template('product_detail.html')

@app.route("/products-list")
def productsList():
    return render_template('products_list.html')





@app.route("/review-add") 
def reviewAdd():
    return render_template('review_add.html')

@app.route("/review-detail")
def reviewDetail():
    return render_template('review_detail.html')

@app.route("/reviews-list")
def reviewList():
    return render_template('reviews_list.html')


@app.route("/signup1")
def signup1():
    return render_template('signup1.html')

@app.route("/signup2", methods=["GET", "POST"])
def signup2():
    if request.method == "POST":
        return redirect(url_for('signup1'))
    return render_template('signup2.html')



@app.route("/signup1_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    
    if DB.insert_user(data, pw_hash):
        return render_template("signup2.html")
    else:
        flash("user id already exist!")
        return render_template("signup1.html")

#이거 추가
@app.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("review_add.html", name=name)

@app.route("/reg_review", methods=['POST'])
def reg_review():
    print(request.files)
    image_file = request.files.get("img_path")
    image_file.save("static/img/{}".format(image_file.filename))
    
    # 'reviewStar' 키가 없을 경우 기본값으로 '0' 사용
    rate = request.form.get('reviewStar', '0')

    data = {
        'name': request.form['name'],
        'title': request.form['title'],
        'rate': rate,
        'review': request.form['reviewContents'],
        "img_path": "static/img/" + image_file.filename
    }
    DB.reg_review(data, image_file.filename)
    return redirect(url_for('login'))

@app.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'], name)
    return jsonify({'my_heart': my_heart})

@app.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '위시 상품에 등록되었습니다!'})

@app.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '위시 상품에서 제외되었습니다.'})

@app.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['password']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('index'))
    else:
        flash("존재하지 않는 정보입니다! 다시 로그인을 시도해주세요.")
        return redirect(url_for('login'))
      
@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)