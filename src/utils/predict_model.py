import numpy as np
import tensorflow as tf
import joblib
import os
from google.cloud import storage

class PredictModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictModel, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.bucket_name = os.environ.get('GOOGLE_S3_BUCKET_NAME')
        self.model_path = os.environ.get('MODEL_PATH')
        self.model_name = os.environ.get('MODEL_NAME')
        self.encoder_path = os.environ.get('ENCODER_PATH')
        
        self.client = storage.Client()

        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')

        self.model_local_path = self.download_file(self.model_path, self.model_name)

        self.interpreter = tf.lite.Interpreter(model_path=self.model_local_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.disability_encoder = self.load_encoder('disability_encoder.joblib')
        self.age_encoder = self.load_encoder('age_encoder.joblib')
        self.experience_encoder = self.load_encoder('experience_encoder.joblib')
        self.city_encoder = self.load_encoder('city_encoder.joblib')
        self.job_encoder = self.load_encoder('job_encoder.joblib')

    def download_file(self, folder_path, file_name):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(os.path.join(folder_path, file_name))

        local_path = os.path.join('./tmp', file_name) 
        blob.download_to_filename(local_path)
        return local_path
    
    def load_encoder(self, encoder_file_name):
        local_path = self.download_file(self.encoder_path, encoder_file_name)
        return joblib.load(local_path)

    def predict(self, disability, age, experience, city):
        # Prepare input data - reshape as 2D arrays
        disability_data = np.array([[disability]])
        age_data = np.array([[age]])
        experience_data = np.array([[experience]])
        city_data = np.array([[city]])
        
        # Encode the input using the same encoders used during training
        encoded_disability = self.disability_encoder.transform(disability_data)
        encoded_age = self.age_encoder.transform(age_data)
        encoded_experience = self.experience_encoder.transform(experience_data)
        encoded_city = self.city_encoder.transform(city_data)
        
        # Combine all encoded features
        predict_data = np.hstack((encoded_disability, encoded_age, encoded_experience, encoded_city))
        
        # Convert to float32 (required by TFLite)
        input_data = predict_data.astype(np.float32)
        
        # Set the input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        # Run inference
        self.interpreter.invoke()

        # Get the output tensor
        predicted_job = self.interpreter.get_tensor(self.output_details[0]['index'])

        # Get the predicted job category
        job_index = np.argmax(predicted_job[0])
        recommended_job = self.job_encoder.categories_[0][job_index]

        return recommended_job