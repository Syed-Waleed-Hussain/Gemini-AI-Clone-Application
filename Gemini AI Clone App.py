from flask import Flask,render_template,request
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
client = genai.Client(api_key="User your Own API here I cam't share my API")

@app.route('/')
def hello():
    return render_template('IMG.html')


@app.route("/IMG", methods=['POST'])
def IMG():
    prompt = request.form['userprompt']

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]  # Must include TEXT and IMAGE
        )
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            image = Image.open(BytesIO(image_data))

            # Resize image
            max_size = (256,256)  # or (256, 256)
            image.thumbnail(max_size, Image.LANCZOS)

            # Save to /static
            os.makedirs("static", exist_ok=True)
            filename = "generated_image.png"
            filepath = os.path.join("static", filename)
            image.save(filepath)

            image_url = f"/static/{filename}"
            break
    else:
        image_url = None

    return render_template('IMG.html', prompt=prompt, image_url=image_url)

@app.route('/gemini',methods = ['POST'])
def gemini():
    query= request.form['userprompt']
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=query,
)
    return render_template('home.html', prompt=query,data=response.text)

app.run(debug = True)