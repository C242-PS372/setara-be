import numpy as np
import tensorflow as tf
import joblib

interpreter = tf.lite.Interpreter(model_path="./exported_model/job_recommendation_model.tflite")
interpreter.allocate_tensors()

encoder_path = './exported_model/encoder/'

disability_encoder = joblib.load(f'{encoder_path}disability_encoder.joblib')
age_encoder = joblib.load(f'{encoder_path}age_encoder.joblib')
experience_encoder = joblib.load(f'{encoder_path}experience_encoder.joblib')
city_encoder = joblib.load(f'{encoder_path}city_encoder.joblib')
job_encoder = joblib.load(f'{encoder_path}job_encoder.joblib')

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def predict_job(disability, age, experience, city, 
                disability_encoder, age_encoder, 
                experience_encoder, city_encoder,
                job_encoder):
    # Prepare input data - reshape as 2D arrays
    disability_data = np.array([[disability]])
    age_data = np.array([[age]])
    experience_data = np.array([[experience]])
    city_data = np.array([[city]])
    
    # Encode the input using the same encoders used during training
    encoded_disability = disability_encoder.transform(disability_data)
    encoded_age = age_encoder.transform(age_data)
    encoded_experience = experience_encoder.transform(experience_data)
    encoded_city = city_encoder.transform(city_data)
    
    # Combine all encoded features
    predict_data = np.hstack((encoded_disability, encoded_age, encoded_experience, encoded_city))
    
    # Convert to float32 (required by TFLite)
    input_data = predict_data.astype(np.float32)
    
   # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output tensor
    predicted_job = interpreter.get_tensor(output_details[0]['index'])

    # Get the predicted job category
    job_index = np.argmax(predicted_job[0])
    recommended_job = job_encoder.categories_[0][job_index]

    return recommended_job


result = predict_job(
    disability="Netra",
    age="31-35",
    experience="6",
    city="Jakarta",
    disability_encoder=disability_encoder,
    age_encoder=age_encoder,
    experience_encoder=experience_encoder,
    city_encoder=city_encoder,
    job_encoder=job_encoder
)

print(result)
