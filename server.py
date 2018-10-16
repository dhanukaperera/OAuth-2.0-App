from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'

github_blueprint = make_github_blueprint(client_id='5b8003c3f9728acb0501', client_secret='0066b529145b582917e3190215c3537c7b72eaab')

app.register_blueprint(github_blueprint, url_prefix='/github_login')



@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        return '<h1>Your Github name is {} '.format(account_info_json['login'] )

    return redirect(url_for('github.login'))

if __name__ == '__main__':
    app.run(debug=True)