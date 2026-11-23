Here is a complete, professional **README.md** for your PromptStudio – AI Content Platform project. It includes project overview, all 8 AI tools, technologies, installation instructions, screenshots section, and deployment information.

Create or open `README.md` in your VS Code project and replace its contents with this:

\# 🚀 PromptStudio – AI Content Platform\
\
An AI-powered web application built using \*\*Python, Flask, SQLite, and Groq AI\*\* that helps users generate, improve, and analyze content quickly and efficiently.\
\
PromptStudio provides multiple AI-powered tools through a simple and user-friendly dashboard.\
\
\## 🌐 Live Demo\
\
\*\*Live Website:\*\* https\://prompt-studio-ai-content-platform.vercel.app\
\
\*\*GitHub Repository:\*\* https\://github.com/Manikyam-guttula/PromptStudio-AI-Content-Platform\
\
\---\
\
\## 📌 Project Overview\
\
PromptStudio is an AI-based content generation platform designed to simplify everyday writing and content-related tasks.\
\
Users can register, log in, access different AI tools, generate responses, and view their previous activities through history and analytics.\
\
The application integrates Groq AI to generate fast AI-powered responses.\
\
\## ✨ Features\
\
\### 1. AI Content Generator\
\- Generates articles, essays, and creative content.\
\- Creates structured content with headings and paragraphs.\
\
\### 2. Text Summarizer\
\- Summarizes long paragraphs and documents.\
\- Extracts important information in simple language.\
\
\### 3. Sentiment Analysis\
\- Identifies positive, negative, and neutral sentiments.\
\- Provides explanations for the detected sentiment.\
\
\### 4. Email Generator\
\- Generates professional emails.\
\- Helps users create formal and informal email content.\
\
\### 5. Paraphrasing Tool\
\- Rewrites sentences and paragraphs.\
\- Preserves the original meaning.\
\
\### 6. Grammar Correction\
\- Corrects grammatical mistakes.\
\- Improves sentence structure and readability.\
\
\### 7. Social Media Caption Generator\
\- Creates engaging social media captions.\
\- Generates creative captions with emojis and hashtags.\
\
\### 8. Blog Title Generator\
\- Generates attractive blog titles.\
\- Helps create SEO-friendly title ideas.\
\
\### Additional Features\
\- User registration and login.\
\- Secure password hashing.\
\- Personalized dashboard.\
\- Prompt history management.\
\- Analytics and tool usage statistics.\
\- AI-generated response display.\
\- Copy generated content.\
\- Responsive web interface.\
\
\---\
\
\## 🛠️ Technologies Used\
\
\| Technology | Purpose |\
\|---|---|\
\| Python | Backend programming |\
\| Flask | Web application framework |\
\| HTML5 | Web page structure |\
\| CSS3 | Styling and design |\
\| JavaScript | Frontend interactions |\
\| SQLite | Database management |\
\| Groq API | AI response generation |\
\| Werkzeug | Password hashing |\
\| python-dotenv | Environment variable management |\
\| Vercel | Application deployment |\
\| Git & GitHub | Version control |\
\
\---\
\
\## 🏗️ Project Architecture\
\
\`\`\`text\
&#x20;                USER\
&#x20;                  |\
&#x20;                  v\
&#x20;            FLASK WEB APP\
&#x20;                  |\
&#x20;         \---------------------\
&#x20;         \|                   |\
&#x20;         v                   v\
&#x20;     FRONTEND             BACKEND\
&#x20;  HTML / CSS / JS          Flask\
&#x20;                             |\
&#x20;                \------------------------\
&#x20;                \|                      |\
&#x20;                v                      v\
&#x20;            GROQ AI API            SQLITE DATABASE\
&#x20;                \|                      |\
&#x20;                v                      v\
&#x20;          AI RESPONSE             USER DETAILS\
&#x20;                \|                 PROMPT HISTORY\
&#x20;                v\
&#x20;          DISPLAY RESULT\
&#x20;                |\
&#x20;                v\
&#x20;         DASHBOARD / HISTORY\
&#x20;              / ANALYTICS\
\`\`\`\
\
\---\
\
\## 📂 Project Structure\
\
\`\`\`text\
PromptStudio/\
│\
├── app.py\
│\
├── services/\
│   └── ai_service.py\
│\
├── templates/\
│   ├── base.html\
│   ├── login.html\
│   ├── register.html\
│   ├── dashboard.html\
│   ├── tool.html\
│   ├── history.html\
│   ├── analytics.html\
│   └── 404.html\
│\
├── static/\
│   ├── css/\
│   ├── js/\
│   └── images/\
│\
├── instance/\
│   └── promptstudio.db\
│\
├── .env\
├── .gitignore\
├── requirements.txt\
└── README.md\
\`\`\`\
\
\*Note: The structure above describes the main application files. Your actual project may contain additional files and folders.\*\
\
\---\
\
\## ⚙️ Installation and Setup\
\
\### Step 1: Clone the Repository\
\
\`\`\`bash\
git clone https\://github.com/Manikyam-guttula/PromptStudio-AI-Content-Platform.git\
\`\`\`\
\
\### Step 2: Open the Project Folder\
\
\`\`\`bash\
cd PromptStudio-AI-Content-Platform\
\`\`\`\
\
\### Step 3: Create a Virtual Environment\
\
\`\`\`bash\
python -m venv venv\
\`\`\`\
\
\### Step 4: Activate the Virtual Environment\
\
\*\*Windows:\*\*\
\
\`\`\`bash\
venv\Scripts\activate\
\`\`\`\
\
\### Step 5: Install Dependencies\
\
\`\`\`bash\
pip install -r requirements.txt\
\`\`\`\
\
\### Step 6: Configure Environment Variables\
\
Create a \`.env\` file in the project root directory.\
\
Add the following:\
\
\`\`\`env\
GROQ_API_KEY=your_groq_api_key\
SECRET_KEY=your_secret_key\
\`\`\`\
\
Replace the placeholder values with your actual credentials.\
\
Get your Groq API key from:\
\
https\://console.groq.com/keys\
\
\*\*Important:\*\* Never upload your actual \`.env\` file or API keys to GitHub.\
\
\### Step 7: Run the Application\
\
\`\`\`bash\
python app.py\
\`\`\`\
\
Open your browser:\
\
\`\`\`text\
http\://127.0.0.1:5000\
\`\`\`\
\
\---\
\
\## 🔄 Application Workflow\
\
1\. The user opens the PromptStudio website.\
2\. The user registers an account or logs in.\
3\. The dashboard displays available AI tools.\
4\. The user selects an AI tool.\
5\. The user enters text or a prompt.\
6\. Flask sends the request to the AI service.\
7\. Groq AI processes the prompt and generates a response.\
8\. The generated result is displayed to the user.\
9\. The application stores the prompt and response in SQLite.\
10\. Users can view their previous activities through History and Analytics.\
\
\---\
\
\## 🗄️ Database Details\
\
PromptStudio uses SQLite to store application data.\
\
\### Users Table\
\
Stores:\
\- User ID\
\- Username\
\- Email\
\- Password hash\
\- Account creation date\
\
\### Prompt History Table\
\
Stores:\
\- History ID\
\- User ID\
\- AI tool name\
\- User input\
\- AI response\
\- Input and output text\
\- Result\
\- Creation date\
\
\---\
\
\## 🚀 Deployment\
\
The application is deployed using \*\*Vercel\*\*.\
\
Live URL:\
\
https\://prompt-studio-ai-content-platform.vercel.app\
\
The application uses environment variables for configuration.\
\
\*\*Database note:\*\* The current Vercel configuration uses SQLite under \`/tmp\`, which is temporary storage. For permanent user accounts and prompt history, configure a persistent hosted database such as PostgreSQL through Neon or Supabase.\
\
\---\
\
\## 🔐 Security\
\
\- Passwords are hashed using Werkzeug security utilities.\
\- User sessions are managed through Flask.\
\- API keys are stored in environment variables.\
\- Database queries use parameterized SQL for user-provided values.\
\- Sensitive configuration files should not be committed to GitHub.\
\
\---\
\
\## 🎯 Future Enhancements\
\
\- Integration with a permanent cloud database.\
\- Export AI-generated content as PDF and DOCX.\
\- Support for additional AI models.\
\- Improved analytics and visual reports.\
\- Dark and light themes.\
\- More advanced prompt templates.\
\- Download and share generated content.\
\- Enhanced mobile responsiveness.\
\
\---\
\
\## 👨‍💻 Author\
\
\*\*PromptStudio – AI Content Platform\*\*\
\
Developed as an AI-based web application project using Python, Flask, and Groq AI.\
\
\---\
\
\## ⭐ Support\
\
If you find this project useful, consider giving the repository a ⭐ on GitHub.\
\
\*\*Thank you for visiting PromptStudio!\*\*\

