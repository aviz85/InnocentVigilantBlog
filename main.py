from flask import Flask, render_template, request, jsonify
import replicate
import os
import base64
import time
from replit import db
import json

app = Flask(__name__)
# Set the API token and the generation limit
REPLICATE_API_TOKEN = os.environ.get('REPLICATE_API_TOKEN')
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
GENERATION_LIMIT = 10
# Initialize Replit DB keys if they don't exist
if 'generation_count' not in db:
    db['generation_count'] = 0
if 'last_reset' not in db:
    db['last_reset'] = time.time()

# Load prompts from JSON file
with open('prompts.json', 'r') as file:
    prompts = json.load(file)


# Define the API endpoint
@app.route('/')
def index():
    return render_template('index.html', prompts=prompts)


@app.route('/transform', methods=['POST'])
def transform_image():
    global generation_count, last_reset

    # Reset the counter every 24 hours
    current_time = time.time()
    last_reset = db['last_reset']

    if current_time - last_reset > 86400:  # 86400 seconds in a day
        db['generation_count'] = 0
        db['last_reset'] = current_time
    # Check if the generation limit has been reached
    generation_count = db['generation_count']
    if generation_count >= GENERATION_LIMIT:
        return jsonify(
            {"error":
             "Generation limit reached. Please try again tomorrow."}), 429

    image_data = request.json['image']
    prompt_index = int(request.json['promptIndex'])
    # Decode base64 image
    image_data = base64.b64decode(image_data.split(',')[1])
    # Save the image temporarily
    temp_image_path = "temp_image.jpg"
    with open(temp_image_path, "wb") as f:
        f.write(image_data)
    # Prepare prompt with 'img' trigger word
    prompt = f"A photo of a person img as a {prompts[prompt_index]['character']} {prompts[prompt_index]['location']}, {prompts[prompt_index]['style']} style"
    try:
        # Call Replicate API
        output = replicate.run(
            "tencentarc/photomaker:ddfc2b08d209f9fa8c1eca692712918bd449f695dabb4a958da31802a9570fe4",
            input={
                "prompt": prompt,
                "input_image": open(temp_image_path, "rb"),
                "num_steps": 50,
                "style_strength_ratio": 20,
                "guidance_scale": 5,
            })
        result = {"output": output[0] if isinstance(output, list) else output}

        # Increment the generation count
        generation_count += 1
        db['generation_count'] = generation_count

        # Log usage
        remaining_generations = GENERATION_LIMIT - generation_count
        log_entry = {
            "timestamp": current_time,
            "remaining_generations": remaining_generations,
            "prompt_index": prompt_index
        }
        if "usage_logs" not in db:
            db["usage_logs"] = []
        db["usage_logs"].append(log_entry)
        # Include remaining generations in the response
        result["remaining_generations"] = remaining_generations

        # Print remaining generations to the console
        print(f"Remaining generations for the day: {remaining_generations}")

    except Exception as e:
        result = {"error": str(e)}
    finally:
        # Remove temporary image
        os.remove(temp_image_path)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
