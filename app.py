import streamlit as st
import re
import sqlite3
from datetime import datetime
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

# ADAPTY - accessible learning support prototype
st.set_page_config(page_title="ADAPTY", page_icon="🌸", layout="wide")

# -------------------- CONTENT --------------------
TEXT = {
    "English": {
        "home": "Home", "library": "Subject Library", "profile": "My Learning Preferences",
        "learn": "Learning Room", "progress": "My Progress", "about": "About ADAPTY",
        "hero": "Learn Your Way. Grow Every Day.",
        "intro": "An inclusive learning space where students can choose the support that works for them.",
        "start": "Explore learning", "supports": "Choose the support that helps you",
        "profile_title": "Set up your learning space", "name": "What should we call you?",
        "language": "Preferred explanation language", "level": "Explanation style",
        "preferences": "What learning supports would you like? (Choose any)",
        "save": "Save my preferences", "saved": "Your preferences have been saved.",
        "select_subject": "Choose a subject", "select_topic": "Choose a topic",
        "open_lesson": "Open lesson", "lesson": "Lesson", "upload": "Or upload your own PDF",
        "paste": "Or paste lesson text", "explain": "Prepare my learning notes",
        "notes": "Your learning notes", "quiz": "Check what you understood",
        "check": "Check my answers", "ask": "Ask a question about this lesson",
        "question": "Type your question", "answer": "Show learning support",
        "progress_empty": "Your completed learning activities will appear here.",
        "about_problem": "Many learning resources present information in only one format, even though students have different access needs and learning preferences.",
        "about_solution": "ADAPTY lets students choose accessible presentation options and offers structured lessons, practice questions and progress-based suggestions.",
        "notice": "ADAPTY is a learning-support prototype. It does not diagnose disabilities or replace a teacher or specialist.",
    },
    "हिन्दी": {
        "home": "मुखपृष्ठ", "library": "विषय सूची", "profile": "मेरी सीखने की पसंद",
        "learn": "सीखने का कमरा", "progress": "मेरी प्रगति", "about": "ADAPTY के बारे में",
        "hero": "अपने तरीके से सीखें, हर दिन आगे बढ़ें।",
        "intro": "एक समावेशी सीखने का स्थान, जहाँ विद्यार्थी अपनी ज़रूरत के अनुसार सहायता चुन सकते हैं।",
        "start": "सीखना शुरू करें", "supports": "अपने लिए उपयोगी सहायता चुनें",
        "profile_title": "अपनी सीखने की सुविधा तय करें", "name": "आपका नाम क्या है?",
        "language": "समझाने की पसंदीदा भाषा", "level": "समझाने का तरीका",
        "preferences": "आपको किस प्रकार की सहायता चाहिए? (एक से अधिक चुन सकते हैं)",
        "save": "मेरी पसंद सुरक्षित करें", "saved": "आपकी पसंद सुरक्षित कर ली गई है।",
        "select_subject": "विषय चुनें", "select_topic": "पाठ चुनें",
        "open_lesson": "पाठ खोलें", "lesson": "पाठ", "upload": "या अपनी PDF फ़ाइल अपलोड करें",
        "paste": "या पाठ यहाँ लिखें", "explain": "मेरे लिए सीखने के नोट्स बनाएँ",
        "notes": "आपके सीखने के नोट्स", "quiz": "आपने कितना समझा?",
        "check": "मेरे उत्तर जाँचें", "ask": "इस पाठ के बारे में प्रश्न पूछें",
        "question": "अपना प्रश्न लिखें", "answer": "सीखने में सहायता पाएँ",
        "progress_empty": "आपकी पूरी की गई सीखने की गतिविधियाँ यहाँ दिखाई देंगी।",
        "about_problem": "कई शिक्षण सामग्री केवल एक ही तरीके से जानकारी देती हैं, जबकि हर विद्यार्थी की पहुँच संबंधी ज़रूरतें और सीखने की पसंद अलग हो सकती हैं।",
        "about_solution": "ADAPTY विद्यार्थियों को अपनी सुविधा के अनुसार सामग्री देखने, पाठ समझने, अभ्यास करने और प्रगति के आधार पर सुझाव पाने का विकल्प देता है।",
        "notice": "ADAPTY सीखने में सहायता देने वाला एक प्रारंभिक प्रोटोटाइप है। यह किसी दिव्यांगता का निदान नहीं करता और न ही शिक्षक या विशेषज्ञ का विकल्प है।",
    },
    "Hinglish": {
        "home": "Home", "library": "Subject Library", "profile": "Meri Learning Preferences",
        "learn": "Learning Room", "progress": "My Progress", "about": "About ADAPTY",
        "hero": "Learn Your Way. Grow Every Day.",
        "intro": "Ek inclusive learning space jahan students apni zaroorat ke hisaab se support choose kar sakte hain.",
        "start": "Learning explore karo", "supports": "Apne liye useful support choose karo",
        "profile_title": "Apna learning space set karo", "name": "Aapka naam kya hai?",
        "language": "Explanation ki preferred language", "level": "Explanation ka style",
        "preferences": "Aapko kaunsi learning support chahiye? (Ek se zyada choose kar sakte ho)",
        "save": "Meri preferences save karo", "saved": "Aapki preferences save ho gayi hain.",
        "select_subject": "Subject choose karo", "select_topic": "Topic choose karo",
        "open_lesson": "Lesson kholo", "lesson": "Lesson", "upload": "Ya apni PDF upload karo",
        "paste": "Ya lesson ka text yahan paste karo", "explain": "Mere learning notes banao",
        "notes": "Aapke learning notes", "quiz": "Aapne kitna samjha?",
        "check": "Mere answers check karo", "ask": "Is lesson ke baare mein question poochho",
        "question": "Apna question likho", "answer": "Learning support pao",
        "progress_empty": "Aapki completed learning activities yahan dikhenge.",
        "about_problem": "Kai learning resources information ko sirf ek format mein dete hain, jabki students ki access needs aur learning preferences alag hoti hain.",
        "about_solution": "ADAPTY students ko accessible options choose karne, structured lessons padhne, practice karne aur progress ke hisaab se suggestions paane deta hai.",
        "notice": "ADAPTY ek learning-support prototype hai. Yeh disability diagnose nahi karta aur teacher ya specialist ka replacement nahi hai.",
    }
}

# Built-in starter lessons: deliberately transparent, curated sample content.
LESSONS = {
    "Mathematics": {
        "Fractions": "A fraction represents a part of a whole. It has a numerator and a denominator. The numerator tells how many equal parts are being considered. The denominator tells how many equal parts make the whole. For example, 3/4 means three out of four equal parts. Fractions with the same denominator can be added by adding their numerators. The denominator stays the same.",
        "Basic Algebra": "Algebra uses letters or symbols to represent numbers. A variable is a letter whose value can change. An expression combines numbers, variables and operations. An equation says that two expressions are equal. To solve a simple equation, use the same operation on both sides. For example, if x + 3 = 7, subtract 3 from both sides. Therefore x = 4.",
    },
    "Science": {
        "The Human Body": "The human body has different organ systems that work together. The digestive system breaks food into nutrients that the body can absorb. The respiratory system helps the body take in oxygen and remove carbon dioxide. The circulatory system moves blood around the body. The brain and nerves help control and coordinate body activities. Healthy habits such as balanced food, movement and sleep support the body.",
        "Plants and Photosynthesis": "Plants need light, water and carbon dioxide to make food. This process is called photosynthesis. It mainly happens in leaves, inside structures called chloroplasts. Chlorophyll is the green pigment that absorbs light energy. During photosynthesis, plants make glucose and release oxygen. Photosynthesis supports plant growth and provides oxygen for many living things.",
    },
    "English": {
        "Parts of Speech": "Words have different jobs in a sentence. A noun names a person, place, thing or idea. A pronoun takes the place of a noun. A verb expresses an action or state. An adjective describes a noun. An adverb can describe a verb, adjective or another adverb. A preposition shows a relationship, often involving place or time. Learning these groups helps us build clear sentences.",
        "Reading Comprehension": "Reading comprehension means understanding the meaning of a text. First, read the title to predict the topic. Read the passage carefully and identify its main idea. Supporting details explain or give examples of the main idea. Look for unfamiliar words using the surrounding sentence for clues. After reading, explain the passage in your own words. Asking who, what, when, where, why and how can help check understanding.",
    },
    "Computer Fundamentals": {
        "Input and Output Devices": "A computer system receives data, processes it and produces information. Input devices send data to a computer. A keyboard is used to enter text, and a mouse helps point and select items. Output devices present results. A monitor displays information and speakers produce sound. Some devices, such as a touchscreen, can provide both input and output.",
        "What is the Internet?": "The Internet is a worldwide network that connects computers and other devices. It allows people to share information and communicate. A web browser is software used to open websites. A search engine helps find information on the web. People should protect personal information, use strong passwords and check whether online information is trustworthy.",
    },
    "Basic Programming": {
        "Variables": "A variable is a named place used by a program to store a value. In Python, you can create a variable by writing a name, an equals sign and a value. For example, age = 18 stores the number 18 in the variable age. A variable can hold text, numbers or other kinds of data. The value can be used later in calculations or displayed on the screen.",
        "If and Else": "An if statement lets a program make a decision. The program checks whether a condition is true. If the condition is true, it runs the indented block under if. An else block runs when the condition is false. For example, if marks are at least 40, a program can display Pass; otherwise it can display Try again. Indentation is important in Python because it shows which statements belong to each block.",
    },
    "General Knowledge": {
        "Environment and Conservation": "The environment includes living things, air, water and land. Pollution can harm people, animals and plants. Conservation means protecting natural resources and using them carefully. We can reduce waste by reusing items and recycling suitable materials. Saving water and electricity also helps. Planting and protecting trees supports habitats and improves local environments.",
        "The Solar System": "The Solar System includes the Sun and the objects that move around it. Eight planets orbit the Sun. Earth is the planet where we live. The Moon is Earth's natural satellite. Planets do not make their own visible light like the Sun; they reflect sunlight. Gravity helps keep planets and other objects in their orbits.",
    },
}

QUIZZES = {
    "Fractions": [("In 3/4, what does the 4 show?", ["Parts being considered", "Total equal parts in the whole", "The whole number"], 1, "The denominator shows the total number of equal parts."), ("What is 1/4 + 2/4?", ["3/4", "3/8", "2/4"], 0, "The denominators are the same, so add 1 + 2 and keep 4."), ("What is the top number called?", ["Denominator", "Numerator", "Variable"], 1, "The numerator is the top number.")],
    "Basic Algebra": [("What does a variable represent?", ["A changing or unknown value", "Only a fixed word", "A punctuation mark"], 0, "A variable is a symbol that can represent a number."), ("If x + 3 = 7, what is x?", ["10", "4", "3"], 1, "Subtract 3 from both sides: x = 4."), ("What does an equation show?", ["Two expressions are equal", "A list of words", "A shape"], 0, "An equation states that two expressions have equal values.")],
    "The Human Body": [("Which system helps us breathe?", ["Respiratory", "Digestive", "Circulatory"], 0, "The respiratory system takes in oxygen and removes carbon dioxide."), ("Which system moves blood?", ["Digestive", "Circulatory", "Skeletal"], 1, "The circulatory system moves blood around the body."), ("What does the digestive system do?", ["Breaks down food", "Pumps blood", "Controls light"], 0, "It breaks food into nutrients the body can absorb.")],
    "Plants and Photosynthesis": [("What energy source is needed for photosynthesis?", ["Light", "Plastic", "Sound"], 0, "Plants use light energy during photosynthesis."), ("Which pigment absorbs light?", ["Chlorophyll", "Haemoglobin", "Keratin"], 0, "Chlorophyll is the green pigment in plants."), ("Which gas is released?", ["Carbon dioxide", "Oxygen", "Nitrogen"], 1, "Oxygen is released during photosynthesis.")],
    "Parts of Speech": [("Which word names a person, place or thing?", ["Noun", "Verb", "Adverb"], 0, "A noun names a person, place, thing or idea."), ("Which part of speech expresses an action?", ["Adjective", "Verb", "Preposition"], 1, "A verb expresses an action or state."), ("Which word describes a noun?", ["Adjective", "Pronoun", "Conjunction"], 0, "An adjective describes a noun.")],
    "Reading Comprehension": [("What is the main idea?", ["The central point", "A random word", "The page number"], 0, "The main idea is the central point of a passage."), ("What do supporting details do?", ["Explain the main idea", "Replace the title", "Hide the topic"], 0, "Supporting details explain or give examples of the main idea."), ("Which is a useful comprehension question?", ["Why?", "What colour is the screen?", "How heavy is the book?"], 0, "Who, what, when, where, why and how questions help check understanding.")],
    "Input and Output Devices": [("Which is an input device?", ["Keyboard", "Monitor", "Speaker"], 0, "A keyboard sends data to the computer."), ("Which device displays information?", ["Monitor", "Mouse", "Microphone"], 0, "A monitor is an output device."), ("A touchscreen can be…", ["Input and output", "Only storage", "Only a printer"], 0, "A touchscreen accepts touch and displays information.")],
    "What is the Internet?": [("What is the Internet?", ["A worldwide network", "A single app", "A keyboard"], 0, "It connects computers and devices around the world."), ("What opens websites?", ["Web browser", "Calculator", "Paint brush"], 0, "A web browser is used to open websites."), ("What helps protect online accounts?", ["Strong passwords", "Sharing passwords", "Using the same public password"], 0, "Strong passwords help protect accounts.")],
    "Variables": [("What is a variable?", ["A named place for a value", "A type of monitor", "A website"], 0, "A variable stores a value under a name."), ("Which creates a Python variable?", ["age = 18", "18 = age", "age == = 18"], 0, "The equals sign assigns the value 18 to age."), ("Can a variable hold text?", ["Yes", "No", "Only images"], 0, "Variables can hold text as well as numbers.")],
    "If and Else": [("What does if check?", ["A condition", "A file size", "A website"], 0, "An if statement checks whether a condition is true."), ("When does else run?", ["When the if condition is false", "Before the program starts", "Only on weekends"], 0, "The else block runs when the if condition is false."), ("What shows blocks in Python?", ["Indentation", "Font colour", "File name"], 0, "Indentation shows which statements belong to a block.")],
    "Environment and Conservation": [("What does conservation mean?", ["Protecting resources", "Wasting water", "Increasing pollution"], 0, "Conservation means protecting natural resources."), ("Which action reduces waste?", ["Reuse items", "Throw everything away", "Waste electricity"], 0, "Reusing items can reduce waste."), ("Trees help support…", ["Habitats", "Plastic waste", "Noise"], 0, "Trees provide habitats and support local environments.")],
    "The Solar System": [("How many planets orbit the Sun?", ["Eight", "Two", "Twenty"], 0, "There are eight planets in our Solar System."), ("What is Earth's natural satellite?", ["The Moon", "Mars", "The Sun"], 0, "The Moon is Earth's natural satellite."), ("What keeps objects in orbit?", ["Gravity", "Sound", "Colour"], 0, "Gravity helps keep planets and other objects in orbit.")],
}

# -------------------- SESSION STATE --------------------
def go_to(page):
    st.session_state.nav_page = page

for key, value in {
    "nav_page": "Home", "language": "English", "student_name": "",
    "supports": [], "level": "Simple", "current_subject": "Mathematics",
    "current_topic": "Fractions", "lesson_text": "", "notes": "",
    "history": [], "font_size": 18, "high_contrast": False,
    "line_spacing": 1.6, "focus_mode": False, "focus_support": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- STYLE --------------------
base_text = "#1F2937" if st.session_state.high_contrast else "#442B38"
base_bg = "#FFFFFF" if st.session_state.high_contrast else "#FFF7F4"
st.markdown(f"""
<style>
.stApp {{ background:{base_bg}; color:{base_text}; }}
h1,h2,h3,h4,p,label,li {{ color:{base_text} !important; }}
[data-testid="stWidgetLabel"] p {{ color:{base_text} !important; font-size:1rem; }}
.stMarkdown, .stText, .stCaption {{ font-size:{st.session_state.font_size}px; line-height:{st.session_state.line_spacing}; }}
div.stButton > button {{ background:#9D4568; color:white; border:1px solid #78344F; border-radius:10px; min-height:44px; font-weight:650; }}
div.stButton > button p {{ color:white !important; }}
input,textarea {{ background:white !important; color:#251923 !important; }}
.hero {{ background:linear-gradient(120deg,#8F355D,#C66D91); padding:34px; border-radius:18px; color:white; }}
.hero h1,.hero p {{ color:white !important; }}
.support-card {{ background:#F5E6ED; border-left:5px solid #9D4568; padding:16px; border-radius:10px; margin-bottom:10px; }}

*:focus-visible {{ outline:3px solid #7C2D52 !important; outline-offset:3px; }}
</style>
""", unsafe_allow_html=True)

# -------------------- HELPERS --------------------
def split_sentences(text):
    parts = re.split(r'(?<=[.!?।])\s+', text.strip())
    return [p.strip() for p in parts if len(p.split()) >= 4]


def make_detailed_notes(text, level):
    sentences = split_sentences(text)
    if not sentences:
        return "Please provide readable lesson text. If this is a scanned PDF, its text may need OCR."
    if len(sentences) <= 5:
        selected = sentences
    else:
        try:
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            matrix = vectorizer.fit_transform(sentences)
            scores = matrix.sum(axis=1).A1
            count = min(len(sentences), 10 if level == "Detailed" else 7 if level == "Simple" else 5)
            chosen = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:count]
            selected = [sentences[i] for i in sorted(chosen)]
        except ValueError:
            selected = sentences[:min(8, len(sentences))]
    if st.session_state.get("language") == "हिन्दी":
        heading = "पाठ के मुख्य बिंदु" if level == "Detailed" else "आइए मुख्य बातें समझें"
    elif st.session_state.get("language") == "Hinglish":
        heading = "Lesson ke main points" if level == "Detailed" else "Chalo main ideas samajhte hain"
    else:
        heading = "Key points from your lesson" if level == "Detailed" else "Let's understand the main ideas"
    return "## " + heading + "\n\n" + "\n\n".join("- " + s for s in selected) + "\n\n**Remember:** These notes select and organise information from your source. They do not add facts that were not in the lesson."



def make_lesson_quiz(text, language, count=5):
    """Create simple source-grounded fill-in-the-blank questions from the active lesson."""
    sentences = split_sentences(text)
    candidates = []
    stop_words = {
        "about", "after", "again", "also", "among", "because", "before", "being",
        "between", "could", "during", "every", "first", "from", "have", "into",
        "many", "more", "most", "other", "should", "some", "such", "than",
        "that", "their", "there", "these", "they", "this", "those", "through",
        "under", "using", "very", "when", "where", "which", "while", "with",
        "would", "your", "what", "then", "them", "will", "each", "only", "does"
    }
    for sentence in sentences:
        words = re.findall(r"[A-Za-z][A-Za-z-]{4,}", sentence)
        words = [w for w in words if w.lower() not in stop_words]
        if len(words) >= 3:
            # Choose a meaningful longer word from the sentence as the answer.
            answer = max(words, key=len)
            candidates.append((sentence, answer))
    questions = []
    seen = set()
    for sentence, answer in candidates:
        if answer.lower() in seen:
            continue
        seen.add(answer.lower())
        distractors = []
        for _, other in candidates:
            if other.lower() != answer.lower() and other.lower() not in [x.lower() for x in distractors]:
                distractors.append(other)
            if len(distractors) == 3:
                break
        if len(distractors) < 3:
            continue
        blank_sentence = re.sub(re.escape(answer), "________", sentence, count=1, flags=re.IGNORECASE)
        if language == "हिन्दी":
            prompt = f"पाठ के अनुसार खाली स्थान भरें: {blank_sentence}"
            explanation = f"इस पाठ में सही शब्द '{answer}' है। मूल वाक्य: {sentence}"
        elif language == "Hinglish":
            prompt = f"Lesson ke according blank fill karo: {blank_sentence}"
            explanation = f"Is lesson mein correct word '{answer}' hai. Original sentence: {sentence}"
        else:
            prompt = f"Complete the sentence from your lesson: {blank_sentence}"
            explanation = f"The lesson gives '{answer}' here. Source sentence: {sentence}"
        options = [answer] + distractors[:3]
        questions.append({"question": prompt, "options": options, "answer": answer, "explanation": explanation})
        if len(questions) >= count:
            break
    return questions


def adaptive_level(score, seconds, attempts):
    # Small illustrative training set; recommendation is a practice suggestion, not a diagnosis.
    samples = [[20,100,4],[35,90,3],[45,80,3],[55,70,2],[65,60,2],[70,50,2],[80,40,1],[90,30,1],[100,20,1]]
    labels = [0,0,0,1,1,1,2,2,2]
    model = DecisionTreeClassifier(max_depth=3, random_state=7)
    model.fit(samples, labels)
    return int(model.predict([[score, seconds, attempts]])[0])


def save_result(topic, score, suggestion):
    # Persistent local history in SQLite.
    connection = sqlite3.connect("adapty_progress.db")
    connection.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, student TEXT, topic TEXT, score REAL, suggestion TEXT, created_at TEXT)")
    connection.execute("INSERT INTO results (student, topic, score, suggestion, created_at) VALUES (?, ?, ?, ?, ?)", (st.session_state.student_name or "Student", topic, score, suggestion, datetime.now().isoformat(timespec="minutes")))
    connection.commit()
    connection.close()


def read_results():
    connection = sqlite3.connect("adapty_progress.db")
    connection.execute("CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, student TEXT, topic TEXT, score REAL, suggestion TEXT, created_at TEXT)")
    rows = connection.execute("SELECT topic, score, suggestion, created_at FROM results ORDER BY id DESC LIMIT 30").fetchall()
    connection.close()
    return rows


def get_question_support(question, lesson):
    if not question.strip():
        return "Write a question so I can help you study this lesson."
    words = [w.lower() for w in re.findall(r"[A-Za-z]{4,}", question) if w.lower() not in {"what","when","where","which","does","this","that","with","from","your","about","explain","please"}]
    sentences = split_sentences(lesson)
    if not sentences:
        return "Please open a lesson or provide lesson text first."
    if words:
        ranked = sorted(sentences, key=lambda s: sum(w in s.lower() for w in words), reverse=True)
        matched = [s for s in ranked if any(w in s.lower() for w in words)][:3]
    else:
        matched = []
    if matched:
        return "Here are the most relevant points from your lesson:\n\n" + "\n\n".join("- " + s for s in matched) + "\n\nTry reading each point and explaining it in your own words."
    return "I couldn't find a direct answer in the provided lesson. Try using one or two important words from the topic, or ask your teacher to clarify this point."

def apply_home_support(title):
    """Apply the selected support and open its settings page."""
    support_map = {
        "Visual access": "High contrast",
        "Audio access": "Text-to-speech preference",
        "Reading support": "Larger text",
        "Keyboard access": "Keyboard navigation",
        "Step-by-step learning": "Step-by-step explanations",
        "Text-first support": "Written instructions",
    }
    selected = support_map.get(title)
    if selected and selected not in st.session_state.supports:
        st.session_state.supports.append(selected)
    if title == "Visual access":
        st.session_state.high_contrast = True
        st.session_state.font_size = max(st.session_state.font_size, 20)
    elif title == "Reading support":
        st.session_state.font_size = max(st.session_state.font_size, 20)
        st.session_state.line_spacing = 1.8
    elif title == "Step-by-step learning":
        st.session_state.level = "Simple"
    st.session_state.focus_support = title
    st.session_state.nav_page = "My Learning Preferences" if title in ("Visual access", "Reading support", "Keyboard access") else "Learning Room"


# -------------------- HEADER / NAV --------------------
lang = "English"  # Hindi and Hinglish are hidden until full lesson translation is supported.
t = TEXT[lang]
nav_options = [t["home"], t["library"], t["profile"], t["learn"], t["progress"], t["about"]]
page_to_label = dict(zip(["Home","Subject Library","My Learning Preferences","Learning Room","My Progress","About ADAPTY"], nav_options))
label_to_page = {v:k for k,v in page_to_label.items()}
if st.session_state.nav_page not in page_to_label:
    st.session_state.nav_page = "Home"
selected_label = st.radio("Main navigation", nav_options, index=nav_options.index(page_to_label[st.session_state.nav_page]), horizontal=True, label_visibility="collapsed")
page = label_to_page[selected_label]
st.session_state.nav_page = page

# -------------------- HOME --------------------
if page == "Home":
    # A simple welcome page: explain the purpose first, then let students choose a support.
    st.markdown("""
    <style>
    .home-hero {
        background: linear-gradient(115deg, #7E2F53 0%, #A84F75 58%, #D18AA4 100%);
        border-radius: 24px;
        padding: 46px 46px;
        color: #FFFFFF;
        margin: 8px 0 24px 0;
        box-shadow: 0 14px 34px rgba(111, 43, 75, 0.16);
        position: relative;
        overflow: hidden;
    }
    .home-hero:after {
        content: "✿";
        position: absolute;
        right: 28px;
        bottom: -42px;
        font-size: 170px;
        color: rgba(255,255,255,0.12);
        line-height: 1;
    }
    .home-kicker {
        display: inline-block;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.32);
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 13px;
        letter-spacing: 0.3px;
    }
    .home-hero h1 {
        color: #FFFFFF !important;
        font-size: clamp(30px, 4vw, 46px) !important;
        line-height: 1.15 !important;
        margin: 18px 0 12px 0;
    }
    .home-hero p {
        color: #FFF8FB !important;
        font-size: 17px;
        max-width: 680px;
        line-height: 1.65;
    }
    .home-side {
        background: linear-gradient(155deg, #F7EAF0, #F0DCE6);
        border: 1px solid #E8CAD6;
        border-radius: 24px;
        padding: 32px 26px;
        min-height: 285px;
        text-align: center;
        box-shadow: 0 10px 26px rgba(111, 43, 75, 0.08);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .home-side .book-icon { font-size: 76px; margin-bottom: 8px; }
    .home-side h3 { margin: 4px 0 10px 0; color: #442B38 !important; }
    .home-side p { color: #614653 !important; line-height: 1.55; }
    .home-section-title { margin: 16px 0 4px 0; }
    .home-section-note { color: #765C68; margin-bottom: 18px; font-size: 16px; }
    .home-support-button div.stButton > button {
        min-height: 158px !important;
        height: 158px !important;
        white-space: pre-wrap !important;
        text-align: left !important;
        padding: 22px 22px !important;
        background: linear-gradient(145deg, #FFFFFF 0%, #F7EAF0 100%) !important;
        color: #442B38 !important;
        border: 1px solid #E8CAD6 !important;
        border-left: 6px solid #9D4568 !important;
        border-radius: 18px !important;
        font-weight: 550 !important;
        box-shadow: 0 7px 18px rgba(111, 43, 75, 0.07) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease !important;
        line-height: 1.55 !important;
    }
    .home-support-button div.stButton > button:hover {
        background: linear-gradient(145deg, #F9EDF2 0%, #F0DCE6 100%) !important;
        border-color: #9D4568 !important;
        box-shadow: 0 12px 24px rgba(111, 43, 75, 0.13) !important;
        transform: translateY(-3px);
    }
    .home-support-button div.stButton > button p { color: #442B38 !important; font-size: 16px !important; line-height: 1.55 !important; }
    .home-prompt {
        margin: 4px 0 18px 0;
        padding: 14px 18px;
        border-radius: 14px;
        background: #F2E3E9;
        color: #654453;
        font-size: 15px;
        text-align: center;
    }
    .home-note {
        background: #F8EEF2;
        border-radius: 12px;
        padding: 13px 16px;
        color: #604653;
        border: 1px solid #EED9E2;
        margin-top: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.55, 1], gap="large")
    with left:
        st.markdown(f"""
        <div class="home-hero">
            <span class="home-kicker">🌸 ADAPTY · A SPACE THAT LEARNS WITH YOU</span>
            <h1>{t['hero']}</h1>
            <p>{t['intro']}</p>
            <p style="font-size:15px; margin-top:18px;">Read at your pace. Listen when you want. Practise one step at a time.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("📚  " + t["start"], on_click=go_to, args=("Subject Library",), type="primary")
    with right:
        st.markdown("""
        <div class="home-side">
            <div class="book-icon">📚</div>
            <h3>Small steps. Real progress.</h3>
            <p>Start with a topic that interests you. Choose the support that makes learning easier, then practise at your own pace.</p>
            <div style="font-size:30px; margin-top:14px;">🌱 ✨ 🌷</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="home-section-title">', unsafe_allow_html=True)
    st.subheader(t["supports"])
    st.markdown('<div class="home-section-note">Pick one that feels right. Your learning space will adjust to your choice.</div>', unsafe_allow_html=True)
    st.markdown('<div class="home-prompt">✨ Your learning style is yours to choose — try a support and change it whenever you like.</div>', unsafe_allow_html=True)

    cards = [
        ("👁️", "Visual access", "Make text clearer with stronger contrast and a larger reading size."),
        ("🔊", "Audio access", "Listen to lesson content instead of reading every line."),
        ("📝", "Reading support", "Give words more room with comfortable text size and spacing."),
        ("⌨️", "Keyboard access", "Move through learning controls with your keyboard."),
        ("🧩", "Step-by-step learning", "Turn longer material into smaller, easier-to-follow parts."),
        ("🧏", "Text-first support", "Keep important instructions and learning feedback in writing."),
    ]
    cols = st.columns(2, gap="large")
    for i, (icon, title, desc) in enumerate(cards):
        with cols[i % 2]:
            st.markdown('<div class="home-support-button">', unsafe_allow_html=True)
            if st.button(f"{icon}  {title}\n\n{desc}", key="home_support_" + str(i), use_container_width=True):
                apply_home_support(title)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="home-note">{t["notice"]}</div>', unsafe_allow_html=True)

# -------------------- SUBJECT LIBRARY --------------------
elif page == "Subject Library":
    st.title(t["library"])
    st.write("Choose a subject and a starter lesson. You can change the language and accessibility settings at any time.")
    subject = st.selectbox(t["select_subject"], list(LESSONS.keys()), key="subject_picker")
    topic = st.selectbox(t["select_topic"], list(LESSONS[subject].keys()), key="topic_picker")
    st.session_state.current_subject = subject
    st.session_state.current_topic = topic
    st.markdown(f"<div class='support-card'><h3>{topic}</h3><p>{LESSONS[subject][topic]}</p></div>", unsafe_allow_html=True)
    st.button(t["open_lesson"], on_click=go_to, args=("Learning Room",))

# -------------------- PROFILE / ACCESSIBILITY --------------------
elif page == "My Learning Preferences":
    st.title(t["profile_title"])
    st.caption("ADAPTY is currently available in English. More learning languages will be added after lesson and quiz translation is supported.")
    st.text_input(t["name"], key="name_input", value=st.session_state.student_name)
    st.selectbox(t["level"], ["Very Simple", "Simple", "Detailed"], key="explanation_level", index=["Very Simple","Simple","Detailed"].index(st.session_state.level))
    support_options = ["Larger text", "High contrast", "Extra line spacing", "Text-to-speech preference", "Short sections", "Step-by-step explanations", "Keyboard navigation", "Reduced distractions", "Written instructions"]
    if "support_picker" not in st.session_state:
        st.session_state.support_picker = st.session_state.supports
    st.multiselect(t["preferences"], support_options, key="support_picker")
    st.subheader("Display and reading controls")
    if st.session_state.get("focus_support"):
        st.info("Selected support: " + st.session_state.focus_support + ". You can change these settings at any time.")
        if st.session_state.focus_support == "Keyboard access":
            st.write("Keyboard tips: press Tab to move forward, Shift+Tab to move back, Enter or Space to activate a control, and arrow keys to change radio or menu selections. Streamlit controls support standard keyboard navigation.")
        elif st.session_state.focus_support == "Text-first support":
            st.write("Instructions, lesson notes and quiz feedback are shown as text. Audio is optional.")
    st.slider("Text size", 14, 26, key="font_size")
    st.slider("Line spacing", 1.2, 2.2, step=0.1, key="line_spacing")
    st.checkbox("High contrast", key="high_contrast")
    st.checkbox("Distraction-free mode", key="focus_mode")
    if st.button(t["save"]):
        st.session_state.student_name = st.session_state.get("name_input", "")
        st.session_state.supports = st.session_state.get("support_picker", [])
        st.session_state.level = st.session_state.get("explanation_level", "Simple")
        st.success(t["saved"])
    if st.session_state.focus_mode:
        st.info("Distraction-free mode is selected. The page uses a simplified layout where possible.")
    st.caption("Audio reading needs the optional gTTS package and an internet connection.")

# -------------------- LEARNING ROOM --------------------
elif page == "Learning Room":
    st.title(t["learn"])
    st.caption("Built-in lesson or your own study material")
    if lang != "English":
        st.info("Interface language changed. Lesson text, PDF content, questions based on the source, and worked examples stay in the original language for now; this version does not translate study material.")
    subject = st.selectbox(t["select_subject"], list(LESSONS.keys()), key="room_subject")
    topic = st.selectbox(t["select_topic"], list(LESSONS[subject].keys()), key="room_topic")
    built_in_text = LESSONS[subject][topic]
    uploaded = st.file_uploader(t["upload"], type=["pdf"])
    pasted = st.text_area(t["paste"], height=140, key="pasted_lesson")
    source_text = built_in_text
    source_name = topic
    if uploaded is not None:
        try:
            reader = PdfReader(uploaded)
            extracted = "\n".join((p.extract_text() or "") for p in reader.pages)
            if extracted.strip():
                source_text = extracted
                source_name = uploaded.name
                st.success("PDF text extracted. You can prepare notes below.")
            else:
                st.warning("No selectable text was found. This may be a scanned PDF; OCR is not included in this prototype.")
        except Exception as exc:
            st.error(f"Could not read this PDF: {exc}")
    elif pasted.strip():
        source_text = pasted
        source_name = "Pasted lesson"
    if st.button(t["explain"]):
        st.session_state.lesson_text = source_text
        st.session_state.notes = make_detailed_notes(source_text, st.session_state.level)
    if st.session_state.notes:
        st.subheader(t["notes"])
        st.markdown(st.session_state.notes)
    st.divider()
    st.subheader(t["ask"])
    question = st.text_input(t["question"], key="student_question")
    if st.button(t["answer"]):
        st.markdown(get_question_support(question, source_text))
        st.caption("This prototype finds relevant sentences in the lesson. It is not a generative AI tutor and may not answer questions beyond the supplied text.")
    st.divider()
    st.subheader(t["quiz"])
    english_letters = len(re.findall(r"[A-Za-z]", source_text))
    quiz_items = make_lesson_quiz(source_text, lang, count=5) if english_letters >= 20 else []
    if not quiz_items:
        st.warning("This lesson does not contain enough English text for this prototype's question builder. Try an English text-based PDF or paste English lesson text. Hindi PDF question generation is not included yet.")
    else:
        st.caption({"English": "Questions are created from the lesson text currently open above.", "हिन्दी": "प्रश्न ऊपर खुले हुए पाठ की सामग्री से बनाए गए हैं।", "Hinglish": "Questions abhi open lesson ke content se banaye gaye hain."}[lang])
        answers = []
        for i, item in enumerate(quiz_items):
            answers.append(st.radio(item["question"], item["options"], key=f"dynamic_quiz_{i}_{source_name}"))
        seconds = st.slider("Approximate time taken (seconds)" if lang == "English" else "लगभग कितना समय लगा (सेकंड)" if lang == "हिन्दी" else "Approx time kitna laga (seconds)", 10, 180, 60)
        attempts = st.slider("Attempts used" if lang == "English" else "कितनी बार प्रयास किया" if lang == "हिन्दी" else "Kitni attempts lagi", 1, 5, 1)
        if st.button(t["check"]):
            correct_count = sum(1 for i, item in enumerate(quiz_items) if answers[i] == item["answer"])
            score = round(correct_count / len(quiz_items) * 100)
            level_id = adaptive_level(score, seconds, attempts)
            suggestions = [
                "Revisit this lesson using shorter steps and try again.",
                "Good progress. Review the key points and try another practice set.",
                "You may be ready for a more challenging lesson."
            ]
            suggestion = suggestions[level_id]
            save_result(source_name, score, suggestion)
            st.success(f"{t['score']}: {correct_count}/{len(quiz_items)} ({score}%)")
            for i, item in enumerate(quiz_items):
                is_correct = answers[i] == item["answer"]
                if lang == "हिन्दी":
                    status = "✓ सही" if is_correct else "↻ दोबारा पढ़ें"
                elif lang == "Hinglish":
                    status = "✓ Sahi" if is_correct else "↻ Dobara revise karo"
                else:
                    status = "✓ Correct" if is_correct else "↻ Review"
                st.write(status + " — " + item["explanation"])
            if lang == "हिन्दी":
                st.info("अगला सुझाव: " + ("पाठ को छोटे चरणों में दोबारा पढ़ें और फिर अभ्यास करें।" if level_id == 0 else "अच्छी प्रगति। मुख्य बिंदुओं को दोहराएँ और फिर अभ्यास करें।" if level_id == 1 else "अब आप थोड़ा कठिन पाठ पढ़ने का प्रयास कर सकते हैं।"))
            elif lang == "Hinglish":
                st.info("Next suggestion: " + ("Lesson ko chhote steps mein revise karke dobara try karo." if level_id == 0 else "Achhi progress! Key points revise karke next practice try karo." if level_id == 1 else "Ab aap thoda challenging lesson try kar sakte ho."))
            else:
                st.info("Suggested next step: " + suggestion)
            st.caption("The Decision Tree uses illustrative training examples. It is an experimental practice suggestion, not a validated assessment of ability.")

    # Optional text-to-speech: do not pretend audio is available if dependency is missing.
    if st.session_state.get("supports") and "Text-to-speech preference" in st.session_state.supports:
        st.divider()
        st.subheader("🔊 Read this lesson aloud" if lang == "English" else "🔊 इस पाठ को सुनें" if lang == "हिन्दी" else "🔊 Lesson ko suno")
        try:
            from gtts import gTTS
            import io
            audio_language = "hi" if lang == "हिन्दी" else "en"
            speech = gTTS(source_text[:4500], lang=audio_language)
            audio_buffer = io.BytesIO()
            speech.write_to_fp(audio_buffer)
            st.audio(audio_buffer.getvalue(), format="audio/mp3")
        except ImportError:
            st.warning("Audio reading package is not installed. Install it with: python -m pip install gTTS")
        except Exception:
            st.warning("Audio could not be created. Check your internet connection or try again later.")

# -------------------- PROGRESS --------------------
elif page == "My Progress":
    st.title(t["progress"])
    rows = read_results()
    if not rows:
        st.info(t["progress_empty"])
    else:
        for topic, score, suggestion, created in rows:
            with st.container(border=True):
                st.subheader(topic)
                st.metric("Quiz score", f"{score:.0f}%")
                st.write(suggestion)
                st.caption(created)

# -------------------- ABOUT --------------------
elif page == "About ADAPTY":
    st.title("About ADAPTY")
    st.subheader("The challenge")
    st.write(t["about_problem"])
    st.subheader("Our approach")
    st.write(t["about_solution"])
    st.subheader("Who is it designed to support?")
    st.write("Students may choose supports useful for visual access, hearing access, dyslexia-friendly reading, attention, mobility and different learning preferences. ADAPTY does not ask students to disclose a diagnosis.")
    st.subheader("What is included in this prototype?")
    st.write("Subject-based starter lessons, selectable display preferences, PDF text extraction, extractive lesson notes, lesson-linked starter quizzes, sentence matching for questions and an experimental Decision Tree recommendation.")
    st.info(t["notice"])

# Student-facing footer: no unnecessary technology list.
st.divider()
st.markdown("<div style='text-align:center;padding:12px'><h3 style='color:#9D4568'>🌸 ADAPTY</h3><p>Learn Your Way. Grow Every Day.</p></div>", unsafe_allow_html=True)
