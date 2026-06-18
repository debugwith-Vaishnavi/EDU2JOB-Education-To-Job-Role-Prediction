from graphviz import Digraph

dot = Digraph(comment='Edu2Job Flowchart', format='png')
dot.node('Start', 'Start')
dot.node('Login', 'User Login/Register')
dot.node('Input', 'Enter Data for Prediction')
dot.node('API', 'Call Predict API')
dot.node('Model', 'ML Model')
dot.node('Store', 'Save History')
dot.node('Result', 'Show Result')
dot.node('End', 'End')

dot.edges(['StartLogin', 'LoginInput', 'InputAPI', 'APIModel', 'ModelResult', 'ResultStore', 'StoreEnd'])
dot.render('f:/edu2job/flowchart', cleanup=True)
