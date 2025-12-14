import gradio as gr
import time
from client import SentinelClient

# Initialize Client (connects to local backend)
client = SentinelClient(base_url="http://127.0.0.1:8000")

def check_system_health():
    try:
        status = client.status()
        return f"✅ ONLINE\nVersion: {status.get('version')}\nEnvironment: {status.get('environment')}"
    except Exception as e:
        return f"❌ OFFLINE\nError: {str(e)}"

def chat_with_sentinel(message, history):
    if not message:
        return ""
    
    # Context from history could be added here
    response = client.chat(message)
    return response

def save_memory(text, tag):
    try:
        result = client.upsert_note(text, tag)
        return f"✅ Memory Saved! ID: {result.get('id')}"
    except Exception as e:
        return f"❌ Failed: {str(e)}"

# --- UI Layout ---
with gr.Blocks(title="Sentinel Forge Command", theme=gr.themes.Glass()) as demo:
    gr.Markdown("# 🛡️ Sentinel Forge Command Node")
    
    with gr.Tabs():
        # Tab 1: Neural Link (Chat)
        with gr.TabItem("🧠 Neural Link"):
            chatbot = gr.Chatbot(height=400, label="Sentinel Prime")
            msg = gr.Textbox(label="Transmission", placeholder="Enter command or query...")
            clear = gr.Button("Clear Protocol")

            def user(user_message, history):
                return "", history + [[user_message, None]]

            def bot(history):
                user_message = history[-1][0]
                bot_message = chat_with_sentinel(user_message, "")
                history[-1][1] = bot_message
                return history

            msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )
            clear.click(lambda: None, None, chatbot, queue=False)

        # Tab 2: Memory Lattice (Database)
        with gr.TabItem("💠 Memory Lattice"):
            with gr.Row():
                mem_input = gr.Textbox(label="Data Fragment", lines=4)
                mem_tag = gr.Textbox(label="Tag / Partition", value="manual-entry")
            mem_btn = gr.Button("Upsert to Lattice")
            mem_output = gr.Markdown()
            
            mem_btn.click(save_memory, inputs=[mem_input, mem_tag], outputs=mem_output)

        # Tab 3: System Diagnostics
        with gr.TabItem("📊 Diagnostics"):
            health_btn = gr.Button("Run System Scan")
            health_display = gr.Textbox(label="System Status", interactive=False)
            health_btn.click(check_system_health, inputs=[], outputs=health_display)

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
