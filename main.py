from fileinput import filename
from flask import Flask, request, render_template
from google.cloud import vision
from google.cloud import storage
import os
import sys


app = Flask(__name__, template_folder="templates")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "anjalee-cloud-workshop-p2.json"

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("main.html")


@app.route("/display", methods=["GET", "POST"])
def uploadimg():


    file = request.files['file']

    # filename = request.files['filename']

    """Uploads a file to the bucket."""
    
    # print(filename)

    # The ID of your GCS bucket
    bucket_name = "anjalee-cloud-workshop-p2.appspot.com"


    destination_blob_name = '%s/%s' % ('image', file.filename)

    # The ID of your GCS object
    source_file_name = ('gs://anjalee-cloud-workshop-p2.appspot.com/image/' + file.filename)
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name, chunk_size=262144 * 5)

    blob.upload_from_file(file, file.content_type)


    object = []
    isEmpty = False
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = source_file_name

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.pages_with_matching_images:

        for page in annotations.pages_with_matching_images:
            if page.full_matching_images:
                object.append(format(page.url))
                print(object)
    else:
        isEmpty = True

    return render_template('main.html', object=object, isEmpty=isEmpty)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

    