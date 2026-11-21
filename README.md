
# PromptStudio | AI Content Platform

PromptStudio is an AI-powered content generation platform developed as part of the Prompt Engineering for AI internship capstone project.

It provides simple tools to generate content, summarize text, analyze sentiment, and view activity analytics through a user-friendly dashboard.

## Features

- **AI Content Generation:** Generate content based on user prompts.
- **Text Summarization:** Convert long text into concise summaries.
- **Sentiment Analysis:** Identify the sentiment of text.
- **Prompt History:** Store and view previous activities.
- **Analytics Dashboard:** Visualize platform usage and activities.
- **User-Friendly Interface:** Modern and responsive dashboard.
- **Demo Mode:** Use basic demo functionality without an API key.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- Chart.js
- OpenAI API (optional)

## Project Structure

```text
PromptStudio/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── services/
│   ├── __init__.py
│   └── ai_service.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── instance/
    └── app.db
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/PromptStudio-AI-Content-Platform.git
```

### 2. Open the project folder

```bash
cd PromptStudio-AI-Content-Platform
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the OpenAI API (Optional)

Create a `.env` file in the project folder and add:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

Keep your API key private. Never upload the `.env` file to GitHub.

### 7. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## Application Modules

| Module | Description |
|---|---|
| Content Generation | Generates content from prompts |
| Text Summarization | Creates short summaries |
| Sentiment Analysis | Analyzes text sentiment |
| Prompt History | Stores previous activities |
| Analytics | Displays usage statistics |

## Database

PromptStudio uses SQLite to store prompt history and activity information.

## Future Enhancements

- More AI-powered content tools
- Advanced prompt templates
- Improved sentiment analysis
- Export generated content
- User authentication
- Enhanced analytics

## Author

Developed as an internship capstone project for Prompt Engineering for AI.

## License

This project is developed for educational purposes.
