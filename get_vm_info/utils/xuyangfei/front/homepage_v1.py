# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for
from front.__init__ import app
import libs.get_msg
import libs.look_for_shortest_way
import json


@app.route('/', methods=['GET'])
def homepage():
    data_deal = libs.get_msg.transmit_to_homepage()
    return render_template('showDB.html', data=data_deal)


@app.route('/result', methods=['GET', 'POST'])
def test():
    data = request.get_json()
    source = data["S"]
    destination = data["D"]
    (shortest_way, all_ways, all_ways_lenth) = libs.look_for_shortest_way.get_way(source, destination)
    result = {}
    for i in range(len(all_ways)):
        result[i] = all_ways[i]
        result[i+len(all_ways)] = all_ways_lenth[i]
    result = json.dumps(result)
    return result


@app.route('/manage_db')
def admin():
    return redirect(url_for('/admin'))