from flask import Flask, render_template, url_for, request, make_response, redirect, session
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

usuario_cadastrado = 'fafa'
senha_cadastrado = '123'
app.secret_key = "chave_super_secreta_e_unica"

@app.route("/")
def index():
    return redirect(url_for('login')) #adiciona ao final da url

@app.route("/login", methods= ["POST", "GET"])
def login():
    mensagem = ""

    if request.method=='POST':

        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == usuario_cadastrado and senha == senha_cadastrado:
            resposta = make_response(redirect(url_for("bemvindo")))
            resposta.set_cookie('username', usuario, max_age = 60*10)

            return resposta
        
        else:

            mensagem = "Usuário ou senha inválidos. Tente Novamente!"

    return render_template("login.html", error=mensagem)

@app.route("/bemvindo", methods=["GET", "POST"])
def bemvindo():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))

    cor = request.cookies.get('tema')

    if request.method == "POST":
        tema_escolhido = request.form.get("tema")
        if tema_escolhido in ['claro', 'escuro']:
            # Definir a cor de fundo com base na escolha
            if tema_escolhido == 'claro':
                cor = "#f0f2f5"
            else:
                cor = "#222222"

            # Criar resposta com cookie válido por 30 minutos
            resposta = make_response(render_template("bemvindo.html", user=username, cordefundo=cor, tema=tema_escolhido))
            expira = datetime.utcnow() + timedelta(minutes=30)
            resposta.set_cookie('tema', cor, expires=expira)
            return resposta

    # Se o cookie já existir, usa ele. Se não, padrão claro
    if not cor:
        cor = "#f0f2f5"
        tema_escolhido = 'claro'
    else:
        tema_escolhido = 'escuro' if cor == "#222222" else 'claro'

    return render_template("bemvindo.html", user=username, cordefundo=cor, tema=tema_escolhido)

@app.route('/esportes')
def esportes():
    cor = request.cookies.get('tema')
    return render_template('esportes.html', cordefundo=cor)

@app.route('/entretenimento')
def entretenimento():
    cor = request.cookies.get('tema')
    return render_template('entretenimento.html', cordefundo=cor)

@app.route('/lazer')
def lazer():
    cor = request.cookies.get('tema')
    return render_template('lazer.html', cordefundo=cor)

@app.route("/logout")
def logout():
    resposta = make_response(redirect(url_for("login")))
    resposta.set_cookie('username', '', expires=0)
    return resposta


if __name__ == '__main__':
    app.run(debug=True)

