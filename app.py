# app.py
# python3 app.py
#
# Dipendenze:
# pip3 install flask pandas
#
# Variabili ambiente da impostare prima di avviare:
# export ADMINPASS="scegli_una_password"
# export MAILUSER="tua_email@gmail.com"
# export MAILPASS="password_app_gmail"
#
# Note:
# - usa una password per app Gmail, non la password normale
# - il database viene creato automaticamente come medgala.db

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "medgala_secret_key_change_this"

dbnome = "medgala.db"


def connessione():
    con = sqlite3.connect(dbnome)
    con.row_factory = sqlite3.Row
    return con


def creabase():
    con = connessione()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS iscritti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        mail TEXT NOT NULL UNIQUE,
        telefono TEXT NOT NULL,
        universita TEXT NOT NULL,
        datains TEXT NOT NULL
    )
    """)

    con.commit()
    con.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/aggiornamenti")
def aggiornamenti():
    return render_template("aggiornamenti.html")


@app.route("/iscriviti", methods=["POST"])
def iscriviti():
    nome = request.form.get("nome", "").strip()
    cognome = request.form.get("cognome", "").strip()
    mail = request.form.get("mail", "").strip().lower()
    telefono = request.form.get("telefono", "").strip()
    universita = request.form.get("universita", "").strip()
    datains = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if nome == "" or cognome == "" or mail == "" or telefono == "" or universita == "":
        flash("Compila tutti i campi.")
        return redirect(url_for("aggiornamenti"))

    try:
        con = connessione()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO iscritti (nome, cognome, mail, telefono, universita, datains)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nome, cognome, mail, telefono, universita, datains)
        )
        con.commit()
        con.close()
        flash("Iscrizione completata.")
    except sqlite3.IntegrityError:
        flash("Questa email è già iscritta.")
    except Exception:
        flash("Errore durante il salvataggio.")

    return redirect(url_for("aggiornamenti"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == os.getenv("ADMINPASS", "admin123"):
            session["admin"] = "si"
            return redirect(url_for("admin"))
        flash("Password non corretta.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    if session.get("admin") != "si":
        return redirect(url_for("login"))

    con = connessione()
    dati = pd.read_sql_query("SELECT * FROM iscritti ORDER BY id DESC", con)
    con.close()

    righe = dati.to_dict(orient="records")
    totale = len(righe)

    return render_template("admin.html", righe=righe, totale=totale)


@app.route("/esporta")
def esporta():
    if session.get("admin") != "si":
        return redirect(url_for("login"))

    con = connessione()
    dati = pd.read_sql_query("SELECT * FROM iscritti ORDER BY id DESC", con)
    con.close()

    nomefile = "iscritti_medgala.csv"
    dati.to_csv(nomefile, index=False)

    return redirect(url_for("admin"))


@app.route("/newsletter", methods=["GET", "POST"])
def newsletter():
    if session.get("admin") != "si":
        return redirect(url_for("login"))

    messaggioinfo = ""

    if request.method == "POST":
        oggetto = request.form.get("oggetto", "").strip()
        testo = request.form.get("testo", "").strip()

        if oggetto == "" or testo == "":
            messaggioinfo = "Compila oggetto e testo."
            return render_template("newsletter.html", messaggioinfo=messaggioinfo)

        mailuser = os.getenv("MAILUSER", "")
        mailpass = os.getenv("MAILPASS", "")

        if mailuser == "" or mailpass == "":
            messaggioinfo = "Imposta MAILUSER e MAILPASS nelle variabili ambiente."
            return render_template("newsletter.html", messaggioinfo=messaggioinfo)

        con = connessione()
        cur = con.cursor()
        cur.execute("SELECT mail, nome FROM iscritti")
        lista = cur.fetchall()
        con.close()

        inviati = 0
        errori = 0

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(mailuser, mailpass)

            for riga in lista:
                destinatario = riga["mail"]
                nome = riga["nome"]

                corpo = f"""Hello {nome},

{testo}

MED GALA Milano
Instagram: @medgalaofficial
Email: medgala.milano@gmail.com
"""

                email = MIMEMultipart()
                email["From"] = formataddr(("MED GALA Milano", mailuser))
                email["To"] = destinatario
                email["Subject"] = oggetto
                email.attach(MIMEText(corpo, "plain"))

                try:
                    server.sendmail(mailuser, destinatario, email.as_string())
                    inviati = inviati + 1
                except Exception:
                    errori = errori + 1

            server.quit()
            messaggioinfo = f"Invio completato. Inviate: {inviati} | Errori: {errori}"

        except Exception as e:
            messaggioinfo = f"Errore invio: {e}"

    return render_template("newsletter.html", messaggioinfo=messaggioinfo)


if __name__ == "__main__":
    creabase()
    app.run(host="0.0.0.0", port=10000, debug=True)