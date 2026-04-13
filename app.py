import gradio as gr
import os
import asyncio

try:
    from api import consult_logic, generate_doc_logic

    print("✅ Logic successfully connected from api.py")
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")


    async def consult_logic(msg):
        return {"content": f"Logic Error: {e}"}


    async def generate_doc_logic(msg):
        return {"content": f"Logic Error: {e}"}


async def main_interface(user_text):
    if not user_text: return None, ""

    doc_keywords = ["draft", "generate", "create", "contract", "agreement", "clause", "policy", "legal form"]
    is_doc = any(kw in user_text.lower() for kw in doc_keywords) and len(user_text) > 12

    try:
        if is_doc:
            # TODO: Document generation logic (Coming Soon)
            return None, "🛠️ **Document Generation feature is coming soon!**\n\nCurrently, I can only provide legal consultations regarding GDPR. Please try asking a question like: *'What are the requirements for a Privacy Policy?'*"
        else:
            result = await consult_logic(user_text)
            return None, result.get("content", "")
    except Exception as e:
        return None, f"⚠️ System Error: {str(e)}"


async def respond(message, history):
    if history is None: history = []

    _, response_text = await main_interface(message)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response_text})

    return "", history

css_code = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
body {
    background-color: #000000 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}
.gradio-container {
    background-color: #000000 !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    height: 100vh !important;
    max-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    flex-direction: column !important;
}
footer, .header-wrapper { display: none !important; }

#app-layout {
    height: 100vh !important; /* Используем vh, чтобы точно занять весь экран */
    width: 100% !important;
    max-width: 800px !important;
    margin: 0 auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    padding: 20px 20px 30px 20px !important;
    
    box-sizing: border-box !important;
    overflow: hidden !important;
}
.title-text {
    text-align: center;
    color: #FFFFFF !important;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
    flex-shrink: 0;
}
.subtitle-text {
    width: 100% !important;
    text-align: center !important;
    color: #666 !important;
    font-size: 14px;
    margin-bottom: 25px !important;
    display: block !important;
}
#suggestions-row {
    justify-content: center !important;
    gap: 10px !important;
    margin-bottom: 20px !important;
    background: transparent !important;
    border: none !important;
    flex-shrink: 0 !important;
}
.suggestion-btn {
    background-color: #111 !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #AAA !important;
    font-size: 11px !important;
    padding: 8px 16px !important; 
    width: auto !important; 
    white-space: nowrap !important; 
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.soon-btn {
    opacity: 0.4 !important; 
    border-style: dashed !important;
    pointer-events: none !important; 
    
    filter: grayscale(100%);
    cursor: default !important;
}
.suggestion-btn:hover {
    background-color: #222 !important;
    border-color: #555 !important;
    color: #FFFFFF !important;
}
#gpt-chat {
    flex-grow: 1 !important; 
    overflow-y: auto !important;
    background: transparent !important;
    border: none !important;
    margin-bottom: 10px !important;
    scrollbar-width: none; 
}
#gpt-chat::-webkit-scrollbar { display: none; }
.gradio-chatbot { background: transparent !important; }
.bubble-wrap { background: transparent !important; border: none !important; }
.message { padding: 10px 0 !important; background: transparent !important; border: none !important; }
.message.user {
    background-color: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 18px !important;
    color: #FFFFFF !important;
    padding: 10px 15px !important;
    max-width: 85% !important;
    margin-left: auto !important;
}
.message.bot {
    background-color: transparent !important;
    color: #E0E0E0 !important;
    padding-left: 0 !important;
}
.soon-btn {
    opacity: 0.5 !important;
    cursor: not-allowed !important;
    border-style: dashed !important;
}
.soon-btn:hover {
    border-color: #333 !important;
    color: #AAA !important;
}
#input-container {
    flex-shrink: 0 !important;
    width: 100% !important;
}
#input-capsule {
    background-color: #000000 !important;
    border: 1px solid #333 !important;
    border-radius: 30px !important;
    padding: 4px 6px 4px 15px !important;
    display: flex !important;
    align-items: center !important;
    min-height: 50px !important;
}
#chat-input {
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
    flex-grow: 1 !important;
}
#chat-input textarea {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #FFFFFF !important;
    font-size: 15px !important;
    padding: 0 !important;
    height: 100% !important;
    min-height: 24px !important;
    resize: none !important;
}
#chat-input textarea:focus { box-shadow: none !important; border: none !important; }
#chat-input textarea::placeholder { color: rgba(255, 255, 255, 0.5) !important; opacity: 1 !important; }
#send-btn {
    background-color: #1f1f1f !important;
    color: #fff !important;

    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    max-width: 32px !important;
    min-height: 32px !important;
    max-height: 32px !important;

    border-radius: 50% !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 0 0 8px !important;

    display: flex !important;
    justify-content: center !important;
    align-items: center !important;

    flex-shrink: 0 !important;
    box-shadow: none !important;
}
#send-btn:hover { background-color: #FFFFFF !important; color: #000000 !important; }
</style>
"""
with gr.Blocks(title="LexGuard EU") as demo:
    gr.HTML(css_code)

    with gr.Column(elem_id="app-layout"):
        gr.HTML('<div class="subtitle-text">Next-Gen GDPR & EU Law Intelligence</div>')
        msg = gr.Textbox(
            render=False,
            elem_id="chat-input",
            placeholder="Ask about GDPR compliance or legal...",
            show_label=False,
            container=False
        )

        with gr.Row(elem_id="suggestions-row"):
            btn_doc = gr.Button("📄 Generate Document (Soon)", elem_classes=["suggestion-btn", "soon-btn"],
                                interactive=False)
            btn_law = gr.Button("⚖️ Legal Analysis", elem_classes="suggestion-btn")
            btn_cons = gr.Button("🎓 GDPR Consultation", elem_classes="suggestion-btn")
            btn_claim = gr.Button("📩 Complaints / Claims", elem_classes="suggestion-btn")
        examples_container = gr.Column()
        chatbot = gr.Chatbot(
            elem_id="gpt-chat",
            show_label=False,
            height=450,
        )


        with gr.Row(elem_id="input-capsule"):
            msg = gr.Textbox(
                elem_id="chat-input",
                placeholder="Ask about GDPR compliance or legal procedures...",
                show_label=False,
                scale=10,
                container=False
            )
            submit = gr.Button("↑", elem_id="send-btn", scale=0)
        with gr.Row():
            with gr.Column(scale=1):
                gr.Examples(
                    examples=[
                        ["What are the transparency obligations for high-risk AI?"],
                        ["Explain Article 17 GDPR."],
                        ["Cyber vulnerability reporting deadlines?"]
                    ],
                    inputs=msg,
                    label=None,
                    elem_id="compact-examples"
                )


        gr.HTML("""
            <div style="
                font-size: 11px; 
                color: #888; 
                text-align: center; 
                margin-top: 5px; 
                opacity: 0.8;
            ">
                <b>Disclaimer:</b> AI can make mistakes. Verify important information.<br>
                Powered by <b>DeepSeek-V3.2</b>
            </div>
        """)
    btn_doc.click(lambda: "Help me draft a Privacy Policy for a startup: ", None, msg)
    btn_law.click(lambda: "Analyze GDPR requirements for data processing: ", None, msg)
    btn_cons.click(lambda: "What are the DPO's main responsibilities according to GDPR? ", None, msg)
    btn_claim.click(lambda: "How to file a data breach notification to the authority? ", None, msg)

    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
    submit.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

if __name__ == "__main__":
    abs_downloads_path = os.path.abspath("downloads")
    os.makedirs(abs_downloads_path, exist_ok=True)
    demo.launch(server_name="0.0.0.0", server_port=7860, allowed_paths=[abs_downloads_path])