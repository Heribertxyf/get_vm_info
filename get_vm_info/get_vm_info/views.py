# -*- coding: utf-8 -*-
""" flask views here"""
from __future__ import absolute_import, unicode_literals
import os
import sys
import traceback
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for
from flask import jsonify, send_from_directory
from werkzeug import secure_filename

from get_vm_info import UPLOAD_DIR, logger_config
from utils.del_vm import read_csv, write_to_csv, get_vminfo_byname
import networkx as nx

ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xlt', 'xls', 'xlsm'])
upload = Blueprint('upload', __name__)
logger = logger_config('uploader', 'vminfo.log')


@upload.route('/')
def index():
    return redirect(url_for('upload.upload_page'))


@upload.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload/index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload.route('/uploading', methods=['GET', 'POST'])
def upload_file():
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        vm_info = {}
        if request.method == "POST":
            logger.info("uploading request files is %s" % request.files)
            file = request.files['fname']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                now = datetime.now().strftime("%Y%m%d-%H%M")
                write_filename = "%s-%s.csv" % (filename[0:-4], now)
                logger.info("saved filename is %s" % write_filename)
                save_dir = os.path.join(UPLOAD_DIR, write_filename)
                file.save(save_dir)
                logger.info("%s stored success~" % write_filename)
                csv_data = read_csv(save_dir)
                logger.info("Read upload file: %s end" % save_dir)
                for vm, values in csv_data.iteritems():
                    try:
                        vm_name = vm
                        logger.info("Get vm info by vmname start...")
                        vm_info[vm_name] = get_vminfo_byname(vm_name)
                        # 把host和status信息重新组合到新的vm_info字典里
                        vm_values = vm_info.get(vm_name)
                        vm_values['host'] = values['host']
                        vm_values['status'] = values['status']
                    except Exception:
                        logger.error(traceback.format_exc())
                # 把组合后的vm_info信息，写入新的csv文件
                write_to_csv(vm_info, save_dir)
                logger.info("Write vm info by vmname end...")
                return send_from_directory(UPLOAD_DIR, write_filename, as_attachment=True)
            return u"不支持的文件类型"
        return u"文件上传失败"
    except Exception:
        logger.error(traceback.format_exc())


from get_vm_info.models import Site, Gpncounter, db


@upload.route("/gpn", methods=['GET'])
def gpn():
    values = {}
    # 获取源节点名称
    src_name = Site.query.all()
    # 获取目的节点名称
    dest_name = src_name
    # 固定行，循环各列，依次取值
    for src in src_name:
        dest_value = []
        for dest in dest_name:
            try:
                value = Gpncounter.query.filter_by(
                    primary=True, source_id=src.id,
                    destination_id=dest.id).first().delay_value
            except Exception:
                # 没有此链路的时候默认赋值为空
                value = None
            dest_value.append(value)
        values[src] = dest_value
        db.session.remove()
    return render_template('gpncounter/gpn_base.html',
                           src_name=src_name, dest_name=dest_name, values=values)


@upload.route("/gpncounter", methods=['POST'])
def gpncounter():
    """
        根据源和目的，计算最短路径
    """
    try:
        G = nx.Graph()
        if request.method == "POST":
            query_src = request.form.get('src')
            query_src_id = Site.query.filter_by(site_name=query_src).first().id
            query_dest = request.form.get('dest')
            query_dest_id = Site.query.filter_by(
                site_name=query_dest).first().id
            # paths = Gpncounter.query.all()
            paths = Gpncounter.query.filter_by(primary=True).all()
            for path in paths:
                src = path.source_id
                dest = path.destination_id
                delay = path.delay_value
                G.add_edge(src, dest, weight=delay)
            # 所有可选路线, type is generator
            # all_paths = nx.shortest_simple_paths(
            # G, query_src, query_dest, 'weight')
            # all_path_list = [path for path in all_paths]
            # 最短路线, type is generator
            shortest_path = nx.shortest_path(
                G, query_src_id, query_dest_id, 'weight')
            logger.info("shortest_path is %s" % shortest_path)
            shortest_path = [Site.query.filter_by(
                id=site_id).first() for site_id in shortest_path]
            # shortest_path_list = [s_path for s_path in shortest_path]
            # 最短路径权值
            shortest_length = nx.shortest_path_length(
                G, query_src_id, query_dest_id, 'weight')
        value = {"path": str(shortest_path), "length": str(shortest_length)}
        G.clear()
        return jsonify(value)
    except Exception:
        logger.warn(traceback.format_exc())
