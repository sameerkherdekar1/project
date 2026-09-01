import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="QA Multi-Agent - By Sameer", layout="wide")
st.title("QA Multi-Agent System - Built by Sameer")
st.markdown("---")

#STEP 1: SIDEBAR - इथेच Key टाकायची - Code मध्ये नाही!
st.sidebar.header("🔐 API Configuration")
api_key = st.sidebar.text_input("", type="password", help="Get from aistudio.google.com")
st.sidebar.info("Your Key is Safe - Not stored in code!")

if not api_key:
    st.warning("⚠️ कृपया Sidebar मध्ये API Key टाका - मगच App चालेल!")
    st.stop()  # Key नसेल तर इथेच थांबेल - पुढे जाणार नाही!

#STEP 2: Key मिळाल्यावरच Model बनवा - हाच Fix आहे!
try:
    genai.configure(api_key="")
    model = genai.GenerativeModel("gemini-3.5-flash")
    st.sidebar.success("✅ API Connected!")
except Exception as e:
    st.sidebar.error(f"Key Error: {e}")
    st.stop()




#STEP 3: आता तुमचे 3 Tabs - 100% चालणार!
tab1, tab2, tab3 = st.tabs(["📝 Manual & API Tests", "🎭 Playwright Tests", "🐞 Jira Bug Analyzer"])

with tab1:
    st.subheader("Agent 1: Manual & API Test Generator")
    req1 = st.text_area("Enter Requirement:", "Login with Email and Password", key="r1")
    if st.button("Generate Manual Cases - 7 Cases", key="btn1"):
        with st.spinner("Generating 7 Cases..."):
            prompt = f"Requirement: {req1}. Generate 7 Manual and API Test Cases with columns: TC ID, Type, Steps, Expected Result. Format as table."
            try:
                res = model.generate_content(prompt)
                st.session_state['manual'] = res.text
                st.markdown(res.text)
                st.success("Part 1 Done - 7 Cases Generated!")
            except Exception as e:
                if "429" in str(e):
                    st.error("30 सेकंद थांबा - Free Limit!")
                else:
                    st.error(str(e))

with tab2:
    st.subheader("Agent 2: Playwright Test Generator")
    req2 = st.text_area("Enter Requirement:", "Login with Email and Password - Secure Test", key="r2")
    if st.button("Generate Playwright Code - 8 Cases", key="btn2"):
        with st.spinner("Generating 8 Cases..."):
            prompt = f"Requirement: {req2}. Generate Playwright TypeScript code for 8 test cases with Page Object Model. Give full code."
            try:
                res = model.generate_content(prompt)
                st.session_state['pw'] = res.text
                st.code(res.text, language="typescript")
                st.download_button("Download test.spec.ts", res.text, file_name="test.spec.ts")
                st.success("Part 2 Done - 8 Cases Generated!")
            except Exception as e:
                if "429" in str(e):
                    st.error("30 सेकंद थांबा - Free Limit!")
                else:
                    st.error(str(e))

with tab3:
    st.subheader("Agent 3: Jira Bug Analyzer - JOINT Agent")
    st.info("हा Agent वरच्या 7+8 Cases चा Context वापरतो!")
    bug = st.text_input("Bug Title:", "Login failed with valid credentials", key="bug")
    log = st.text_area("Error Log:", "TypeError: token undefined at auth.js:22", key="log")
    if st.button("Analyze Bug - JOINT Analysis", key="btn3"):
        with st.spinner("Analyzing with Joint Context..."):
            context = st.session_state.get('manual','')[:1500] + st.session_state.get('pw','')[:1500]
            prompt = f"You are QA Lead. Context of previous tests: {context}. Bug: {bug}. Log: {log}. Give Root Cause, Severity, Steps to Reproduce, and Suggested Fix in Playwright."
            try:
                res = model.generate_content(prompt)
                st.markdown(res.text)
                st.success("✅ Jira Output - Multi-Agent Workflow Complete! - Built by Sameer")
                st.balloons()
            except Exception as e:
                st.error(str(e))
