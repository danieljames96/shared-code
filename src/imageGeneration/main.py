import time
import src.imageGeneration.dependencies as dep
import os

API_KEY = "f1c3fdd4-f1c0-4af7-aa3d-4e6837d5227f"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_KEY}"
}

IMAGES = [
    "https://i.natgeofe.com/k/271050d8-1821-49b8-bf0b-3a4a72b6384a/obama-portrait__3x2.jpg",
    "https://d3hjzzsa8cr26l.cloudfront.net/516e6836-d278-11ea-a709-979a0378f022.jpg",
    "https://hips.hearstapps.com/hmg-prod/images/gettyimages-1239961811.jpg"
]

# Let's create a custom model, so we can fine tune it.
model_id = dep.create_model("Sample", HEADERS)

# We now upload the images to fine tune this model.
dep.upload_image_samples(model_id, IMAGES, HEADERS)

# Now it's time to fine tune the model. Notice how I'm continuously
# getting the status of the training job and waiting until it's
# finished before moving on.
version_id, status = dep.queue_training_job(model_id, HEADERS)
while status != "finished":
    time.sleep(10)
    version_id, status = dep.get_model_version(model_id, version_id, HEADERS)

# Now that we have a fine-tuned version of a model, we can
# generate images using it. Notice how I'm using '@me' to
# indicate I want pictures similar to the ones we upload to
# fine tune this model.
inference_id, status = dep.generate_image(HEADERS,
    model_id,
    prompt="A photo of @me with a tall black hat and sunglasses"
)
while status != "finished":
    time.sleep(10)
    inference_id, status, image = dep.get_inference_job(model_id, inference_id, HEADERS)

print(image)

work_dir = os.getcwd()
file_path = work_dir.replace('src', 'data') + '\\output\\image.jpg'

dep.get_image_local(image, file_path)