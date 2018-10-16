from flask import Flask, redirect, url_for,render_template,make_response
from flask_dance.contrib.github import make_github_blueprint, github
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'

github_blueprint = make_github_blueprint(client_id='5b8003c3f9728acb0501', client_secret='0066b529145b582917e3190215c3537c7b72eaab')

app.register_blueprint(github_blueprint, url_prefix='/github_login')

user = {
    "name" : '',
    "login" :'',
    "avatar_url":'',
    "bio":''
}

repos = []



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/profile')
def profile():    
    print(repos)
    return render_template('profile.html',user= user,repos=repos)

@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')
    repo_info = github.get('/user/repos')

    if account_info.ok:
        account_info_json = account_info.json()
        repo_info_json = repo_info.json()
        print(len(repo_info_json))
       
        for r in repo_info_json :
            
            repos.append({"name":r.get('name'),"url":r.get('html_url')})
       

        user['name'] = account_info_json.get('name')
        user['login'] = account_info_json.get('login')
        user['avatar_url'] = account_info_json.get('avatar_url')
        user['bio'] = account_info_json.get('bio')


        return redirect(url_for('profile'))

        #redirect(url_for('github'))
        #return '<h1>Your Github name is {} '.format(account_info_json['login'] )
        #return render_template('github.html',name=account_info.get('name'))


    return redirect(url_for('github.login'))

if __name__ == '__main__':
    app.run(debug=True)