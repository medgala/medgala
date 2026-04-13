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

import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
app.secret_key = "medgala_secret_key_change_this"

dbnome = "medgala.db"


def connessione():
    url = os.getenv("DATABASE_URL", "")
    con = psycopg.connect(url, row_factory=dict_row)
    return con


def creabase():
    con = connessione()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS iscritti (
        id SERIAL PRIMARY KEY,
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

    # 1) salva nel database
    try:
        con = connessione()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO iscritti (nome, cognome, mail, telefono, universita, datains)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nome, cognome, mail, telefono, universita, datains)
        )
        con.commit()
        con.close()

    except psycopg.errors.UniqueViolation:
        flash("Questa email è già iscritta.")
        return redirect(url_for("aggiornamenti"))

    except Exception as e:
        import traceback
        print("Errore salvataggio database:", repr(e))
        traceback.print_exc()
        flash(f"Errore durante il salvataggio: {e}")
        return redirect(url_for("aggiornamenti"))

    # 2) invia mail di benvenuto
    try:
        mailuser = os.getenv("MAILUSER", "")
        mailpass = os.getenv("MAILPASS", "")

        if mailuser != "" and mailpass != "":
            server = smtplib.SMTP("smtp-relay.brevo.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mailuser, mailpass)

            oggetto = "Welcome to MED GALA Milano"

            corpo = f"""Hello {nome},

You are now officially part of MED GALA Milano.

An exclusive night where medicine meets elegance, bringing together students from the leading universities in Milan.

You will receive early access to tickets, event details, and all upcoming announcements.

We look forward to welcoming you.

MED GALA Milano
@medgalaofficial
"""

            email = MIMEMultipart()
            email["From"] = formataddr(("MED GALA Milano", mailuser))
            email["To"] = mail
            email["Subject"] = oggetto
            email.attach(MIMEText(corpo, "plain"))

            server.sendmail(mailuser, mail, email.as_string())
            server.quit()

    except Exception as e:
        print("Errore invio email:", e)

    flash("Iscrizione completata.")
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
    cur = con.cursor()
    cur.execute("SELECT * FROM iscritti ORDER BY id DESC")
    righe = cur.fetchall()
    con.close()

    totale = len(righe)

    return render_template("admin.html", righe=righe, totale=totale)


@app.route("/esporta")
def esporta():
    if session.get("admin") != "si":
        return redirect(url_for("login"))

    con = connessione()
    cur = con.cursor()
    cur.execute("SELECT * FROM iscritti ORDER BY id DESC")
    righe = cur.fetchall()
    con.close()

    dati = pd.DataFrame(righe)

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
            server = smtplib.SMTP("smtp-relay.brevo.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.ehlo()
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