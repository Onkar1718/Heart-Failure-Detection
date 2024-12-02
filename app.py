from flask import Flask , render_template , request
import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
try:
    model = load("randomforest2.pkl")
    print("Model loaded successfully!")
except EOFError:
    print("The pickle file seems corrupted or incomplete.")
    
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/test")
def test():
    return render_template('test.html')

standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])
def predict():
    Sex_F = 0
    Sex_M = 0
    ChestPainType_ASY =0
    ChestPainType_ATA = 0
    ChestPainType_NAP = 0
    ChestPainType_TA = 0
    RestingECG_LVH = 0
    RestingECG_Normal = 0
    RestingECG_ST = 0
    ExerciseAngina_N = 0 
    ExerciseAngina_Y = 0
    ST_Slope_Down = 0
    ST_Slope_Flat = 0
    ST_Slope_Up = 0

    age = int(request.form['age'])
    restbp = int(request.form['restbp'])
    cholesterol = int(request.form['cholesterol'])
    fastingbs = int(request.form['fastingbs'])
    maxhr = int(request.form['maxhr'])
    oldpeak = int(request.form['oldpeak'])
    if request.method == 'POST':
        gender=request.form['gender']
        if(gender=='male'):
            Sex_M = 1
        else:
            Sex_F = 1
        
        chest=request.form['chest']
        if(chest=='ASY'):
            ChestPainType_ASY=1
        elif(chest=='ATA'):
            ChestPainType_ATA=1
        elif(chest=='NAP'):
            ChestPainType_NAP=1
        elif(chest=='TA'):
            ChestPainType_TA=1

        RestingECG=request.form['RestingECG']
        if(RestingECG=='LVH'):
            RestingECG_LVH=1
        elif(RestingECG=='Normal'):
            RestingECG_Normal=1
        elif(RestingECG=='ST'):
            RestingECG_ST=1

        ExerciseAngina=request.form['ExerciseAngina']
        if(ExerciseAngina=='yes'):
            ExerciseAngina_Y=1
        elif(ExerciseAngina=='no'):
            ExerciseAngina_N=1
            
        ST_Slope=request.form['ST_Slope']
        if(ST_Slope=='Down'):
            ST_Slope_Down=1
        elif(ST_Slope=='Flat'):
            ST_Slope_Flat=1
        elif(ST_Slope=='Up'):
            ST_Slope_Up=1
        
            
        input_data = ([[age,restbp,cholesterol,fastingbs,maxhr,oldpeak,Sex_F,Sex_M,ChestPainType_ASY,ChestPainType_ATA,ChestPainType_NAP,ChestPainType_TA,RestingECG_LVH,RestingECG_Normal,
                        RestingECG_ST,ExerciseAngina_N,ExerciseAngina_Y,ST_Slope_Down,ST_Slope_Flat,ST_Slope_Up]])

        input_data_numpy_array = np.asarray(input_data)

        reshape_input_data = input_data_numpy_array.reshape(1,-1)

        prediction = model.predict(reshape_input_data)
        
        if(prediction[0]==0):
            return render_template('result.html',prediction_texts ="No Heart Failure Detected")
        else:
            return render_template('result.html',prediction_texts = "Yes Heart Failure Detected")
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)