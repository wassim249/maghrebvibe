import streamlit as st
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.chains import LLMChain
import os
load_dotenv()

# edit streamlit page config
st.set_page_config(
    page_title="👋 MAGHREBVIBE.AI",
    page_icon="🇲🇦",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("👋 MAGHREBVIBE.AI")
st.markdown("This is a demo of a chatbot that does sentiment analysis,pos tagging and NER on Darija sentences")



def pos_tagging_chain(llm,sentence):
    pos_tagging_template = """Use the following sentence do POS tagging: {sentence};examples:"""
    pos_tagging_examples = [
        {"sentence": "Had produit diali makaynch fih chi khedma", "pos": "DET NOUN ADJ VERB PRON DET NOUN NOUN"},
        {"sentence": "Konti katmout f had lmal", "pos": "VERB PRON VERB ADP DET NOUN"},
        {"sentence": "L9it had kitab f lktab", "pos": "VERB DET NOUN ADP DET NOUN"},
        {"sentence": "Smahti 3la hadra dyalna", "pos": "VERB ADP NOUN ADP NOUN"},
        {"sentence": "Ghadi nchoufak 3la khatrak", "pos": "VERB PRON VERB PRON"},
        {"sentence": "Had shi wahed khassni nched", "pos": "DET NOUN DET NOUN VERB PRON VERB"},
    ]
    pos_tagging_prompt = PromptTemplate(input_variables=["sentence", "pos"], template="Sentence: {sentence}\nPOS tagging: {pos}")
    prompt = FewShotPromptTemplate(
        prefix=pos_tagging_template,
        examples=pos_tagging_examples,
        example_prompt=pos_tagging_prompt,
        suffix="sentence: {sentence}\nPOS tagging: ",
        input_variables=["sentence"],
    )
    pos_tagging_chain = LLMChain(llm=llm, prompt=prompt)
    return pos_tagging_chain.invoke(sentence)["text"]

def ner_chain(llm,sentence):
    ner_template = """Use the following sentence do NER: {sentence};examples:"""
    ner_examples = [
        {"sentence": "Had produit mal9itoch f jumia", "ner": "O O O O O location"},
        {"sentence": "Konti katmout 3la amal", "ner": "O O O O O person"},
        {"sentence": "Rabat zwina", "ner": "location O"},
        {"sentence": "Samsung 7sn mn iphone", "ner": "organization O O organization"},
        {"sentence": "Ghadi nchoufak 3la khatrak", "ner": "O O O O"},
        {"sentence": "Had shi wahed khassni nched", "ner": "O O O O O O"},
    ]
    ner_prompt = PromptTemplate(input_variables=["sentence", "ner"], template="Sentence: {sentence}\nNER: {ner}")
    prompt = FewShotPromptTemplate(
        prefix=ner_template,
        examples=ner_examples,
        example_prompt=ner_prompt,
        suffix="sentence: {sentence}\nNER: ",
        input_variables=["sentence"],
    )
    ner_chain = LLMChain(llm=llm, prompt=prompt)
    print(sentence)
    return ner_chain.invoke(sentence)["text"]

def sentiment_analysis(sentence):
    output_probality = 0.5
    return {"probality":output_probality,"sentiment":"positive" if output_probality > 0.5 else "negative"}

def get_answer(llm,sentence):
    pos_tagging = pos_tagging_chain(llm,sentence)
    ner = ner_chain(llm,sentence)
    return f"""The sentence \"{sentence}\" is classified as positive.\n
    POS tagging: {pos_tagging}\n
    NER: {ner}"""

def app():
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                         temperature=0.7)

    # display the model selection widget
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # display the messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # check if the user has entered a prompt
    if prompt := st.chat_input("Enter a sentence in Darija"):
        # append the prompt to the messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        # send the prompt to the API
        with st.chat_message("user"):
            st.markdown(prompt)
        # send the response to the API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            print("prompt",prompt)
            answer = get_answer(llm,prompt)
            message_placeholder.markdown(answer)
        # append the full response to the messages
        st.session_state.messages.append({"role": "assistant", "content": answer})



if __name__ == "__main__":
    app()