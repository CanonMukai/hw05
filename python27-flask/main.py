#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
import json
from flask import Flask, render_template, request


app = Flask(__name__)
app.debug = True

networkJson = urlfetch.fetch("https://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

@app.route('/')
# / のリクエスト（例えば http://localhost:8080/ ）をこの関数で処理する。
# ここでメニューを表示をしているだけです。
def root():
  return render_template('hello.html')
"""
  return ('''
<body>
	<h1>Hello!</h1>
  <ul>
    <li><a href=/pata>パタトクカシーー</a></li>
    <li><a href=/norikae>乗換案内</a></li>
  </ul>
</body>
''')
"""

@app.route('/pata')
# /pata のリクエスト（例えば http://localhost:8080/pata ）をこの関数で処理する。
# これをパタトクカシーーを処理するようにしています。
def pata():
  # とりあえずAとBをつなぐだけで返事を作っていますけど、パタタコカシーーになるように自分で直してください！
  a = request.args.get('a', '')
  b = request.args.get('b', '')
  pata = ' '
  if len(a) <= 0 and len(b) > 0:
    pata = b
  elif len(b) <= 0 and len(a) > 0:
    pata = a
  else:
    if len(a) >= len(b):
      length = len(b)
      c = a[length:len(a)]
      print c
    else:
      length = len(a)
      c = b[length:len(b)]
      print c
    for i in range(length):
      pata = pata + a[i] + b[i]
    pata = pata + c
  # pata.htmlのテンプレートの内容を埋め込んで、返事を返す。
  return render_template('pata.html', pata=pata)

@app.route('/norikae')
# /norikae のリクエスト（例えば http://localhost:8080/norikae ）をこの関数で処理する。
# ここで乗り換え案内をするように編集してください。
def norikae():
  result = 'A'
  printA()
  #print network
  fromA = request.args.get('from', '')
  toB = request.args.get('to', '')
  #print ('fromA = %s' % fromA)
  return render_template('norikae.html', network=network, result=result)

def printA():
  print 'A'

@app.route('/norikae/search')
def search():
  #fromA = request.args.get('from', '')
  #toB = request.args.get('to', '')
  a = 'A'
  return render_template('search.html', fromA=a)

