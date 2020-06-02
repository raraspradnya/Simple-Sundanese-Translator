import os
import urllib.request
from app import app
from flask import Flask, flash, request, render_template
import translator
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate(results=[]):
	if request.method == "GET":
		return render_template("upload.html", results=results)    
	elif request.method == "POST":
		results=[]
		indo_vocab = []
		sunda_vocab = []
		translator.readVocab(indo_vocab, sunda_vocab)
		kalimat = (request.form["kalimat"])
		m = int(request.form["stringmatch"])
		n = int(request.form["mode"])
		result = translator.translate(m, n, kalimat, indo_vocab, sunda_vocab)
		results.append(result)
		return render_template("upload.html", results=results, kalimat=kalimat)

if __name__ == "__main__":
    app.run(debug=True)