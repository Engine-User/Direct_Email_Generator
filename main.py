import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Set page config at the very beginning
st.set_page_config(layout="wide", page_title="Direct Email Generator", page_icon="📧")

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Graduate&display=swap');

    body {
        font-family: 'Graduate', cursive !important;
    }

    .stButton > button {
        background-color: #000000;  /* Changed to jet black */
        color: white;
        font-family: 'Graduate', cursive !important;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
        box-shadow: 0 9px #333;  /* Darkened shadow */
        transform: perspective(1px) translateZ(0);
        animation: glow 1s ease-in-out infinite alternate;
    }

    .stButton > button:hover {
        animation: bounce 0.5s infinite;
    }

    .title-box {
        background-color: #000000;  /* Changed to jet black */
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        font-family: 'Graduate', cursive !important;
    }

    .title-box:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
        animation: bounce 0.5s infinite;
    }

    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }

    @keyframes glow {
        from {
            box-shadow: 0 0 2px #000000, 0 0 4px #000000, 0 0 6px #000000, 0 0 8px #000000;
        }
        to {
            box-shadow: 0 0 4px #000000, 0 0 8px #000000, 0 0 12px #000000, 0 0 16px #000000;
        }
    }

    /* Force Graduate font on all text elements */
    p, h1, h2, h3, h4, h5, h6, span, div {
        font-family: 'Graduate', cursive !important;
    }
</style>
""", unsafe_allow_html=True)

def create_streamlit_app(llm, portfolio, clean_text):
    # Sidebar
    with st.sidebar:
        why_button = st.button("Why?")
        best_practices_button = st.button("Best Practices")
        contact_info_button = st.button("Contact Info")

        if why_button:
            st.markdown("""
            <div style="font-family: 'Graduate', sans-serif; background-color: #000000; color: white; padding: 20px; border-radius: 10px; border: 2px solid #333333;">
                <h3 style="color: #CCCCCC;">Listen, let me tell you something.</h3>
                <p style="color: red;">**Direct Mail Generator**</p>
                <ul>
                    <li>You're a job aspirant, and you're tired of wasting your precious time crafting the perfect cold email, only to have it fall flat.</li>
                    <li>Well, let me introduce you to Direct Mail Generator, the cold email generator that's going to change the game.</li>
                    <li>You don't need to waste time to know time is money, and you don't have time to be messing around with imperfect emails.</li>
                    <li>With our advanced technology, we're not just generating emails, we're generating connections.</li>
                    <li>We're not just sending messages, we're sending opportunities.</li>
                </ul>
                <p><strong>Important:</strong> Always review and personalize the generated emails before sending them to ensure they accurately represent your voice and experience.</p>
            </div>
            """, unsafe_allow_html=True)

        if best_practices_button:
            st.markdown("""
            <div style="font-family: 'Graduate', sans-serif; background-color: #000000; color: white; padding: 20px; border-radius: 10px; border: 2px solid #333333;">
                <h3 style="color: #CCCCCC;">Best Practices For Sending Emails</h3>
                <p style="color: red;">**Maximize Your Chances**</p>
                <ul>
                    <li>**Input the right website**: Use our cold email generator to search for matching job openings on any website you want. Make sure you're targeting the right job, and you're one step closer to getting noticed.</li>
                    <li>**Edit and customize your email**: Our algorithm will generate a relevant email message for you to edit and use. Don't be lazy - take the time to replace those boring default credentials with your own name, and swap out those generic portfolio links with your actual portfolio.</li>
                    <li>**Make it personal, make it yours**: Don't send out the same generic email to every single company. You need to stand out, and that's where our email generator comes in. Put in the effort to make it personal, and show the company you're interested in them, not just the job.</li>
                    <li>**Don't send out generic emails**: You're not a robot, and you shouldn't be sending out robot-like emails. Make sure you've replaced those credentials and portfolio links with your own, and that the email is personalized to the company you're applying to.</li>
                    <li>**Get results with the right message**: Our cold email generator is designed to help you get results. With the right message, at the right time, and to the right person, you'll be one step closer to landing that job. So, take the time to make it happen, and don't settle for mediocrity.</li>
                    <li>Timing matters: Send your emails during business hours, preferably early in the week.</li>
                </ul>
                <p><strong>Remember:</strong> Cold emailing is about building relationships, not just asking for opportunities. Be genuine, respectful, and patient in your approach.</p>
            </div>
            """, unsafe_allow_html=True)

        if contact_info_button:
            st.markdown("""
            <div style="font-family: 'Graduate', sans-serif; background-color: #000000; color: white; padding: 20px; border-radius: 10px; border: 2px solid #333333;">
                <h3 style="color: #CCCCCC;">Contact Information</h3>
                <p>**Get in Touch with Digital Garage INC**</p>
                <ul>
                    <li>Company: Digital Garage INC</li>
                    <li>Email: ggengineerco@gmail.com</li>
                    <li style="color: red;">From: Engineer</li>    
                </ul>
                <p><strong>Note:</strong> We're always here to help! Feel free to reach out if you have any questions, feedback, or need assistance with our Direct Email Generator.</p>
            </div>
            """, unsafe_allow_html=True)

    # Main content
    st.markdown('<div class="title-box"><h1>📧 Direct Mail Generator</h1></div>', unsafe_allow_html=True)
    url_input = st.text_input("Enter the Job Site URL of Your Dream Company (eg:https://careers.cred.club/openings):", value="")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            with st.spinner('Generating your personalized email...'):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load()[0].page_content)
                portfolio.load_portfolio()
                links = portfolio.query_links(data.split())  # Use all words as potential skills
                email = llm.extract_and_generate_email(data, links)
                
                st.subheader("Your Personalized Direct Email:")
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {str(e)}")
            st.error("Please check your input and try again. If the problem persists, contact support.")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)


