from flask import Flask, render_template, jsonify, request, url_for
import json

app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html")


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    print(jsdata)
    return jsdata


@app.route('/getpythondata')
def get_python_data(pythondata):
    return json.dumps(pythondata)


if __name__ == "__main__":
    app.run(debug=True)


# from Curriculum import Curriculum
# from Coloring import Coloring
#
# data = [[1, 1, 1],
#         [2, 1, 2],
#         [0, 1, 1]]
#
# data2 = [[5,3,4],
#          [6,1,2],
#          [5,2,6],
#          [3,3,2],
#          [4,1,3],
#          [1,2,3]]
#
# data3 = [[5,6,6],
#          [3,3,3],
#          [1,1,1],
#          [1,1,1],
#          [1,1,2],
#          [3,3,3],
#          [4,4,5],
#          [1,1,1],
#          [1,1,1],
#          [4,4,4],
#          [1,1,1]]
#
# curriculum = Curriculum(3, 11, data3, ["POL", "ANG", "MUZ", "PLA", "HIS", "BIO", "MAT", "INF", "TEC", "WF", "ZZW"])
# curriculum.display_curriculum_graph_matrix()
# coloring = Coloring(curriculum.curriculum_graph)
# # colors = coloring.run_greedy()
# colors2 = coloring.run_genet ic(2000,2000)
# # curriculum.transform_coloring_to_timetable(colors)
# curriculum.transform_coloring_to_timetable(colors2)













