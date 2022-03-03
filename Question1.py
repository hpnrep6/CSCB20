from flask import Flask, render_template
app = Flask(__name__)

@app.route('/<name>')
def user(name):
    return render_template('Question1.html', name=format(name))

def format(input: str) -> str:
    input.strip()
    hasUpper = False
    hasLower = False

    formatted = ""

    for i in range(len(input)):
        if input[i].islower():
            hasLower = True
        elif input[i].isupper():
            hasUpper = True
        
        if input[i].isalpha():
            formatted += input[i]
    
    if hasLower and hasUpper:
        # Kind of forgot if python actually handles invalid indicies but like
        # lets just assume it doesn't because why not
        if len(formatted) >= 1:
            formatted = formatted[0].upper() + formatted[1:]
        if len(formatted) >= 2:
            formatted = formatted[0] + formatted[1:].lower()
    elif hasLower or hasUpper:
        formatted = formatted.swapcase()
    
    return 'Welcome, ' + formatted + ', to my CSCB20 website!'