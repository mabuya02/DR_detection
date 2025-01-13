
---

# Early detection of diabetic retinopathy

This project implements a machine learning-based system for the early detection of diabetic retinopathy (DR) from retinal images using EfficientNet-B0. The system is built using Flask and integrates model predictions, Grad-CAM visualizations, and a user-friendly web interface.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project offers a comprehensive solution for detecting diabetic retinopathy from retinal images. The system uses a deep learning model, EfficientNet-B0, to predict the stage of DR and visualize the reasoning behind the predictions using Grad-CAM. The results are served through a web application built with Flask, where users can upload retinal images and view predictions.

## Features

- **Model Prediction**: Predicts the class of diabetic retinopathy (from class 0 to 4) based on retinal image analysis.
- **Confidence Score**: Displays the confidence level for each prediction.
- **Grad-CAM Visualization**: Offers visual explanations of the model's decision-making process.
- **Web Interface**: Simple interface to upload retinal images, get predictions, and view associated results.
- **Database Integration**: Stores prediction data including patient details, predicted labels, confidence scores, and Grad-CAM images.

## Installation

### Prerequisites

Make sure you have Python 3.x installed. It is also recommended to use a virtual environment for dependency management.

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/diabetic-retinopathy-detection.git
   ```

2. Navigate to the project directory:
   ```bash
   cd diabetic-retinopathy-detection
   ```

3. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Set up the environment variables:
   - Copy the `.env.sample` file to `.env`:
     ```bash
     cp .env.sample .env
     ```
   - Configure the `.env` file with the necessary values (e.g., database URI, Flask secret key).

7. Set up the database:
   - If you are using SQLite, no further configuration is needed.
   - For other databases, make sure to update the database URI in `apps/config.py`.

8. Run database migrations:
   ```bash
   flask db upgrade
   ```

## Usage

1. Start the Flask application:
   ```bash
   flask run
   ```

2. Open the web application in your browser at `http://127.0.0.1:5000`.

3. Upload a retinal image to get predictions, including the predicted class, confidence score, and Grad-CAM visualization.

## File Structure

The project follows the structure below:

```
diabetic-retinopathy-detection/
├── __pycache__/                     # Python bytecode cache
├── .venv/                            # Virtual environment
├── apps/                             # Main application folder
│   ├── __init__.py                   # Application initialization
│   ├── config.py                     # Configuration file
│   ├── authentication/               # Authentication module
│   ├── home/                         # Home module (landing page)
│   ├── image/                        # Image processing module
│   ├── ml_model/                     # Machine learning models (e.g., EfficientNet)
│   ├── patient/                      # Patient details and management
│   ├── prediction/                   # Prediction logic and results
│   ├── static/                       # Static files (images, CSS, JS)
│   ├── templates/                    # HTML templates
│   ├── test/                         # Test-related files
├── retinal_images/                   # Folder for uploading retinal images
├── .env                              # Environment configuration
├── env.sample                        # Sample environment file
├── requirements.txt                  # List of dependencies
├── README.md                         # Project documentation
└── run.py                            # Main entry point to start the Flask app
```

## Contributing

Contributions to the project are welcome! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:
- Replace `yourusername` with your actual GitHub username.
- Ensure that the `.env.sample` file contains the required configurations such as `DATABASE_URL`, `SECRET_KEY`, etc.
