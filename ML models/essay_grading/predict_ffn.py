from tensorflow.keras.models import model_from_json
import numpy as np
json_file = open('ffn_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("ffn_model.h5")
print("Loaded model from disk")
input = [16,    177,    13,    1,    3533.693756,    21.875 ,   118,    74.02 ,   8.54,350]
input = np.array([input])
pred = list(model.predict(input)[0])
print(pred.index(max(pred)))
