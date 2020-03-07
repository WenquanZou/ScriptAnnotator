import flask
from flask import request, jsonify, send_from_directory, abort
from ast import literal_eval
from flask_cors import CORS, cross_origin
import os
from os import listdir
from os.path import isfile, join
import lxml.etree as ET

app = flask.Flask(__name__)
cors = CORS(app)

app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/plays', methods=['GET'])
@cross_origin()
def get_plays():
    scripts_path = os.path.abspath("shakespeare_scripts")
    all_scripts = [f for f in listdir(scripts_path) if isfile(join(scripts_path, f))]
    return jsonify({
        'plays': all_scripts
    })


@app.route('/play/<directory>/<playname>', methods=['GET'])
def get_play(directory, playname):
    script_dir = os.path.abspath(os.path.join(directory, "shakespeare_scripts"))
    xml_filename = os.path.join(script_dir, playname)
    
    dom = ET.parse(xml_filename)
    acts = []
    title = dom.xpath("//title")[0].text
    for child in dom.xpath("//act"):
        acts.append(parse_act(child))
    return jsonify({
        'acts': acts,
        'title': title
    })


@app.route('/act/<directory>/<playname>/<actnum>', methods=['GET'])
def get_play_act(directory, playname, actnum):
    script_dir = os.path.abspath(os.path.join(directory, "shakespeare_scripts"))

    xml_filename = os.path.join(script_dir, playname)

    dom = ET.parse(xml_filename)
    updated_act = dom.xpath(f"//act[@actnum={actnum}]")
    act = parse_act(updated_act)
    return jsonify({
        'act': act,
        'actnum': actnum
    })


@app.route('/submit/<directory>/<playname>', methods=['POST'])
def submit_annotation(directory, playname):
    annotations = literal_eval(request.data.decode('utf8'))
    script_dir = os.path.abspath(os.path.join(directory, "shakespeare_scripts"))
    xml_filename = os.path.join(script_dir, playname)
    
    dom = ET.parse(xml_filename)
    for annotation in annotations:
        specific_lines = dom.xpath(f"//line[@globalnumber >= {annotation['lineStart']} and @globalnumber <= {annotation['lineEnd']}]")
        for specific_line in specific_lines:
            specific_line.attrib['annotation'] = annotation['actionVerb']
    acts = []
    
    with open(xml_filename, 'wb') as f:
        f.write(ET.tostring(dom, pretty_print=True))
    for child in dom.xpath("//act"):
        acts.append(parse_act(child))

    return jsonify({
        'acts': acts
    })


@app.route("/download/<directory>/<playname>")
def get_image(directory, playname):
    script_dir = os.path.abspath(os.path.join(directory, "shakespeare_scripts"))
    try:
        return send_from_directory(script_dir, filename=playname, as_attachment=True)
    except FileNotFoundError:
        abort(404)


def parse_act(element):
    children = []
    for child in element.xpath("./scene"):
        children.append(parse_scene(child))
    return {'type': 'act', 'act_num': element.attrib['num'], 'scenes': children}


def parse_scene(element):
    children = []
    scene_num = element.attrib['num']
    act_num = element.attrib['actnum']
    for child in element.iterchildren():
        if child.tag == "speech":
            children.append(parse_speech(child))
        elif child.tag == "stagedir":
            children.append(parse_stagedir(child))
    return {'type': "scene", 'act_num': act_num, 'scene_num': scene_num, 'content': children}


def parse_speech(element):
    children = []
    for child in element.iterchildren():
        if child.tag == "line":
            children.append(parse_line(child))
        elif child.tag == "stagedir":
            children.append(parse_stagedir(child))
    speaker = element.xpath("./speaker")[0].text
    
    return {'type': "speech", 'speaker': speaker, 'content': children}


def parse_line(element):
    line_num = element.attrib['globalnumber']
    if 'annotation' in element.attrib:
        action = element.attrib['annotation']
    else:
        action = ""
    text = ""
    if element.text:
        text = element.text
    for child in element.iterchildren():
        if child.tag == "foreign" and child.text:
            text = text + child.text + child.tail
    return {'type': "line", 'line_num': line_num, 'text': text, 'annotation':action}


def parse_stagedir(element):
    stagedir_num = element.attrib['sdglobalnumber']
    dir = element.xpath("./dir")[0].text
    return {'type': 'stagedir', 'stage_num': stagedir_num, 'dir': dir}

