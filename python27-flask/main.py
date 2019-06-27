#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import urlfetch
import json
from flask import Flask, render_template, request


app = Flask(__name__)
app.debug = True

networkJson = urlfetch.fetch("https://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

class Station:
    def __init__(self, name):
        self.name = name
        self.is_visited = False

def make_graph(rosen_list):
    station_links_dict = {}
    for rosen in rosen_list:
        for i in range(len(rosen['Stations'])-1):
            if rosen['Stations'][i] in station_links_dict:
                station_links_dict[rosen['Stations'][i]].append(rosen['Stations'][i+1])
            else:
                station_links_dict[rosen['Stations'][i]] = [rosen['Stations'][i+1]]
            if rosen['Stations'][i+1] in station_links_dict:
                station_links_dict[rosen['Stations'][i+1]].append(rosen['Stations'][i])
            else:
                station_links_dict[rosen['Stations'][i+1]] = [rosen['Stations'][i]]
    return station_links_dict

def make_station_list(rosen_list):
    station_list = []
    for rosen in rosen_list:
        for i in range(len(rosen['Stations'])):
            if Station(rosen['Stations'][i]) not in station_list:
                station_list.append(Station(rosen['Stations'][i]))
    return station_list

def is_visited(station_name, station_list):
    for a in station_list:
        if station_name == a.name:
            a.is_visited = True
            break

def check_is_visited(station_name, station_list):
    for a in station_list:
        if station_name == a.name:
            return a.is_visited

def BFS(from_A, to_B, graph, station_list):
    path = []
    que = []
    que.append(from_A)
    is_visited(from_A, station_list)
    
    while que:
        current_station = que.pop(0)
        path.append(current_station)
        if current_station== to_B:
            return path
        unreached_count = 0
        for a in graph[current_station]:
            if check_is_visited(a, station_list) == False:
                que.append(a)
                is_visited(a, station_list)
                unreached_count += 1
        if unreached_count == 0:
            path.pop()
    return 'Not Connected'

def make_shotest_path(from_A, to_B, rosen_list, graph):
    station_list = make_station_list(rosen_list)
    path = BFS(from_A, to_B, graph, station_list)
    
    length = len(path)
    cur = path[length-1]
    shotest_path = [cur]
    
    for i in range(length-2, -1, -1):
        if path[i] in graph[cur]:
            shotest_path.insert(0, path[i])
            cur = path[i]
            
    return shotest_path

graph = make_graph(network)


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
  path = make_shotest_path(fromA, toB, network, graph)
  return render_template('norikae.html', network=network, result=result, path = path, fromA=fromA, toB=toB)

def printA():
  print 'A'

@app.route('/norikae/search')
def search():
  #fromA = request.args.get('from', '')
  #toB = request.args.get('to', '')
  a = 'A'
  return render_template('search.html', fromA=a)

