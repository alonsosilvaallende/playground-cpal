import streamlit as st

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

from langchain.chat_models import ChatOpenAI
from langchain_experimental.pal_chain import PALChain
from langchain_experimental.cpal.base import CPALChain

llm = ChatOpenAI(model_name="gpt-4", temperature=0)
pal_chain = PALChain.from_math_prompt(llm=llm, verbose=True)
cpal_chain = CPALChain.from_univariate_prompt(llm=llm, verbose=True)

example1 = """Jan has three times the number of pets as Marcia.
Marcia has two more pets than Cindy.
If Cindy has four pets, how many total pets do all of them have?"""

example2 = """Jan has the number of pets as Marcia plus the number of pets as Cindy. Marcia has no pets. If Cindy has four pets, how many total pets do the three have?"""

example3 = """Jan has the number of pets as Marcia plus the number of pets as Cindy. Marcia has two more pets than Cindy. If Cindy has four pets, how many total pets do the three have?"""

example4 = """Jan has three times the number of pets as Marcia. Marcia has two more pets than Cindy. If Cindy has ten pets, how many pets does Barak have?"""

example5 = """Tim buys the same number of pets as Cindy and Boris. Cindy buys the same number of pets as Bill plus Bob. Boris buys the same number of pets as Ben plus Beth. Bill buys the same number of pets as Obama. Bob buys the same number of pets as Obama. Ben buys the same number of pets as Obama. Beth buys the same number of pets as Obama. If Obama buys one pet, how many pets total does everyone buy?"""

column1, column2 = st.columns([1,2])

with column1:
    example = st.radio("Examples", ["Causal mediator", "Causal collider", "Causal confounder", "Unanswerable question", "Complex narrative"])

Example1 = False
Example2 = False
Example3 = False
Example4 = False
Example5 = False

with column2:
    if example == "Causal mediator":
        Example1 = st.button(example1)
    elif example == "Causal collider":
        Example2 = st.button(example2)
    elif example == "Causal confounder":
        Example3 = st.button(example3)
    elif example == "Unanswerable question":
        Example4 = st.button(example4)
    else:
        Example5 = st.button(example5)

text = ""
if Example1:
    text = example1
if Example2:
    text = example2
if Example3:
    text = example3
if Example4:
    text = example4
if Example5:
    text = example5

#def on_message_change():
#    prompt = st.session_state["input"]
#    prompt = prompt.replace("\"", "")
#    prompt = prompt.replace("\n", " ")

prompt = st.text_area("Question:", value=text)
prompt = prompt.replace("\"", "")
prompt = prompt.replace("\n", " ")

pred_llm = ""
# pred_pal = ""
pred_cpal = ""
if prompt != "":
    if Example1:
        prompt = example1
    col1, col3 = st.columns(2)
    #col1, col2, col3 = st.columns(3)
      
    pred_llm = llm.predict(prompt)
    with col1:
        st.header("gpt-4")
        st.markdown(pred_llm)
#    try:
#        pred_pal = pal_chain.run(prompt)
#    except Exception as e_msg_pal:
#        pred_pal = e_msg_pal
#    with col2:
#        st.header("PAL")
#        st.write(pred_pal)
    try:
        pred_cpal = cpal_chain.run(prompt)
    except Exception as e_msg_cpal:
        pred_cpal = e_msg_cpal

    with col3:
        st.header("CPAL")
        st.write(pred_cpal)
else:
    col1, col3 = st.columns(2)
    #col1, col2, col3 = st.columns(3)
    with col1:
        st.header("GPT-4")
    #with col2:
    #    st.header("PAL")
    with col3:
        st.header("CPAL")


