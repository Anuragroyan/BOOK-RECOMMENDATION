import flask
import difflib
import os
from numpy.core.numeric import False_
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = flask.Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

df2 = pd.read_csv('./models/test.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['AboutBook'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])
all_titles = [df2['title'][i] for i in range(len(df2['title']))]


def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    tit1 = df2['title'].iloc[book_indices]
    return_df = pd.DataFrame(columns=['title'])
    return_df['title'] = tit1
    return return_df

@app.route('/',methods=['GET','POST'])



def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    

    if flask.request.method == 'POST':
        b_name = flask.request.form['Book_name']
        result_final = get_recommendations(b_name)
        names = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])    
        
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'books.png')
        return flask.render_template('result.html',book_names=names,search_name=b_name,user_image = full_filename) 
  
            


if __name__=="__main__":
    app.run(debug=False)    