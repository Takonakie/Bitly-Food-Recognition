# Bitly | Food Recognition & Calorie Estimation

A web application that can identify various food items from an image using a **YOLOv8** object detection model and provide an estimate of the total calories.

-----

## 📋 Project Description

This project leverages a **YOLOv8** machine learning model trained to recognize dozens of food types. All of this is integrated into a user-friendly interface.

  * **Backend**: Built with **Flask**, it is responsible for receiving uploaded images, running inference on the detection model, and then calculating calorie estimates for each identified food item.
  * **Frontend**: Designed in **Figma** and built with vanilla **JavaScript**, it allows users to easily upload images and view the nutritional analysis visually.

-----

## ✨ Key Features

  * 🔎 **Image-Based Food Detection**: Utilizes the YOLOv8 model for high accuracy.
  * 🍔 **Multi-Object Recognition**: Capable of detecting multiple food items in a single image.
  * ⚖️ **Automatic Calorie Estimation**: Calculates the total calories of the recognized food.
  * 🚀 **Interactive User Interface**: Simple and intuitive image upload process.
  * 📊 **Detailed Results**: Provides a list of detected foods and their calorie counts.
  * 💻 **Fast Backend**: Powered by the lightweight and efficient Flask server.
  * 🎨 **Modern Design**: UI/UX designed in Figma for a clean and modern user experience.

-----

## 🛠️ Tech Stack

  * **Machine Learning**: YOLOv8
  * **Backend**: Flask (Python)
  * **Frontend**: JavaScript (Vanilla)
  * **Design & Prototyping**: Figma

-----

## ⚙️ Installation and Local Usage

Follow these steps to run this project on your local machine.

### 1\. Prerequisites

Ensure you have **Python 3.10** or a newer version installed.

### 2\. Clone the Repository

```bash
git clone https://github.com/Takonakie/Bitly-Food-Recognition.git
cd Bitly-Food-Recognition
```

### 3\. Set Up the Backend (Flask)

Create and activate a virtual environment:

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install all the required dependencies:

```bash
pip install -r requirements.txt
```

### 4\. Run the Application

Once all dependencies are installed, run the Flask server:

```bash
python app.py
```

### 5\. Access the Application

Open your browser and navigate to the following address:

**[http://127.0.0.1:5000](https://www.google.com/search?q=http://127.0.0.1:5000)**

You can now upload a food image and see the results\!

-----

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

-----

## 🙏 Acknowledgments

  * A big thank you to the **Ultralytics** team for the incredible YOLOv8 model.
  * Inspired by various open-source food recognition projects.
