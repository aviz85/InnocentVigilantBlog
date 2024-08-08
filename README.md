# PhotoMaker App

PhotoMaker App is a web-based application that allows users to capture images using their webcam and transform them into various artistic styles using machine learning models. It's based on the Flask framework and utilizes the Replicate API for image transformation.

## Features

- Capture images directly from your webcam.
- Choose from a variety of transformation prompts.
- Generate stylized images based on selected prompts.
- Get feedback on the remaining number of transformations you can perform per day.
- View error messages in a user-friendly modal dialog.

## Usage

### Prerequisites

To run this project locally, you need to have the following installed:

- Python (>= 3.10)
- Flask
- Replicate API
- Replit's Database

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/photomaker-app.git
    cd photomaker-app
    ```

2. Install the required dependencies:
    ```bash
    poetry install
    ```

3. Set up your Replicate API token:
    ```bash
    export REPLICATE_API_TOKEN=<your_replicate_api_token>
    ```

### Running the App

To start the Flask server, run:

```bash
poetry run python main.py
```

Open your web browser and go to `http://localhost:5000` to see the app.

### Configuration

You can customize the transformation prompts by editing the `prompts.json` file. Each prompt should have the structure:

```json
{
    "character": "Character Description",
    "location": "Location Description",
    "style": "Art Style"
}
```

You can also adjust the generation limit by modifying the `GENERATION_LIMIT` value in the `main.py` file:

```python
GENERATION_LIMIT = 10
```

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits

This project was developed using:

- Flask for the web framework.
- Replicate API for AI model integration.
- Replit's Database for storing usage data.

## How to Contribute

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Add a "Made with Replit" badge

You can add a "Made with Replit" badge to your webview by adding the following code before the closing `</body>` tag in your `index.html` file:

```html
<script src="https://replit.com/public/js/replit-badge-v2.js" theme="dark" position="bottom-right"></script>
```

## Contact

For any issues, please open an issue on GitHub or contact the repository owner.

---

Thank you for checking out the PhotoMaker App! Enjoy generating beautiful images with unique styles!