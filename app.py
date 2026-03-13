from flask import Flask, render_template, request
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data=request.get_json()
    idea =data['idea']
    print("Received idea:", idea)
    return "Idea received successfully" 
if __name__ == '__main__':
    app.run(debug=True)