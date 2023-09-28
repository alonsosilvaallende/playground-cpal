import streamlit as st

#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())

from langchain.chat_models import ChatOpenAI
from langchain_experimental.pal_chain import PALChain
from langchain_experimental.cpal.base import CPALChain
from tempfile import NamedTemporaryFile

title = "Causal Program-Aided LLMs"
st.set_page_config(page_title=title, page_icon=None, layout="centered")

st.title(title)

example1 = """Jan has three times the number of pets as Marcia.
Marcia has two more pets than Cindy.
If Cindy has four pets, how many total pets do all of them have?"""

example2 = """Jan has the number of pets as Marcia plus the number of pets as Cindy. Marcia has no pets. If Cindy has four pets, how many total pets do all of them have?"""

example3 = """Jan has the number of pets as Marcia plus the number of pets as Cindy. Marcia has two more pets than Cindy. If Cindy has four pets, how many total pets do all of them have?"""

example4 = """Jan has three times the number of pets as Marcia. Marcia has two more pets than Cindy. If Cindy has ten pets, how many pets does Barak have?"""

example5 = """Tim buys the same number of pets as Cindy and Boris. Cindy buys the same number of pets as Bill plus Bob. Boris buys the same number of pets as Ben plus Beth. Bill buys the same number of pets as Obama. Bob buys the same number of pets as Obama. Ben buys the same number of pets as Obama. Beth buys the same number of pets as Obama. If Obama buys one pet, how many pets total does everyone buy?"""

column1, column2 = st.columns([1,2])

with column1:
    example = st.radio("Examples:", ["Unanswerable question", "Complex narrative", "Causal mediator", "Causal collider", "Causal confounder"])

Example1 = False
Example2 = False
Example3 = False
Example4 = False
Example5 = False

with column2:
    if example == "Unanswerable question":
        Example4 = st.button(example4)
    elif example == "Complex narrative":
        Example5 = st.button(example5)
    elif example == "Causal mediator":
        Example1 = st.button(example1)
    elif example == "Causal collider":
        Example2 = st.button(example2)
    elif example == "Causal confounder":
        Example3 = st.button(example3)

if example== "Causal mediator":
    st.markdown(":blue[Correct answer: 28]")

if example == "Causal collider":
    st.markdown(":blue[Correct answer: 8]")

if example == "Causal confounder":
    st.markdown(":blue[Correct answer: 20]")

if example=="Unanswerable question":
    st.markdown(":blue[Correct answer: Unanswerable]")

if example=="Complex narrative":
    st.markdown(":blue[Correct answer: 13]")

# Initialization
if 'text' not in st.session_state:
    st.session_state['text'] = ''

if Example1:
    st.session_state['text'] = example1
if Example2:
    st.session_state['text'] = example2
if Example3:
    st.session_state['text'] = example3
if Example4:
    st.session_state['text'] = example4
if Example5:
    st.session_state['text'] = example5

with st.form(key='my_form'):
    prompt = st.text_area("Question:", st.session_state['text'])
    submit_button = st.form_submit_button(label='Submit')

#prompt = st.text_area("Question:", value=text, on_change=on_message_change)

column1, column2 = st.columns([1,1])
with column1:
    model1 = st.selectbox("Language Model 1:", ["gpt-3.5-turbo", "gpt-4"], key="model1")
with column2:
    model2 = st.selectbox("Language Model 2:", ["gpt-3.5-turbo", "gpt-4"], key="model2")

llm = ChatOpenAI(model_name=model1, temperature=0)
llm2 = ChatOpenAI(model_name=model2, temperature=0)
pal_chain = PALChain.from_math_prompt(llm=llm, verbose=True)
cpal_chain = CPALChain.from_univariate_prompt(llm=llm2, verbose=True)


pred_llm = ""
pred_cpal = ""
if submit_button:
    prompt = prompt.replace("\"", "")
    prompt = prompt.replace("\n", " ")

    col1, col2 = st.columns(2)
      
    with col1:
        st.header(f"{model1}")
        pred_llm = llm.predict(prompt)
        st.markdown(pred_llm)
    with col2:
        st.header(f"Causal Program-Aided {model2}")
        try:
            pred_cpal = cpal_chain.run(prompt)
            st.write(pred_cpal)
            with NamedTemporaryFile(suffix=".svg") as temp:
                cpal_chain.draw(path=f"{temp.name}")
                st.image(f"{temp.name}")
        except Exception as e_msg_cpal:
            pred_cpal = e_msg_cpal
            st.write(pred_cpal)
else:
    col1, col2 = st.columns(2)
    with col1:
        st.header(f"{model1}")
    with col2:
        st.header(f"Causal Program-Aided {model2}")
