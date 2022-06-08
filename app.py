from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__) 
app.debug = False
app.config ['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)


responses = []

@app.route('/')
def start_survey():
   """Start survey"""

   return render_template('start-survey.html', survey=survey)



@app.route('/begin', methods=["POST"])
def begin():
   """Clear responses list"""
   responses.clear()
   session['responses'] = []

   return redirect('/questions/0')



@app.route('/questions/<int:qid>')
def show_question(qid):
   """Show current question; POST answer to /answer"""

   responses = session.get('responses')

   if responses == None:
      return redirect('/')

   if len(responses) != qid:
      flash(f"Invalid question id: {qid}.")
      return redirect('/questions/{len(repsonses}')

   question = survey.questions[qid]

   return render_template('questions.html', question_num=qid, question=question)



@app.route('/answer', methods=["POST"])
def handle_answer():
   """Redirect to next question"""
    

   choice = request.form['answer'] # request.form for POST requests (vice GET - request.args)
   responses = session['responses']
   responses.append(choice)
   session['responses'] = responses

   if (len(responses) == len(survey.questions)):
      return redirect('/complete')

   else:
      return redirect(f"/questions/{len(responses)}")



@app.route('/complete')
def complete_survey():
   """End of survey 'Thank you'"""

   # print('*****SESSION*****')
   # print(session['responses'])
   # print('*****SESSION*****')

   return render_template('complete.html')