import streamlit as st
from groq import Groq
import requests
import io
from PIL import Image

# ────────────────────────────────────────────────
#  PAGE CONFIG & COSMIC STYLE
# ────────────────────────────────────────────────
st.set_page_config(page_title="Missle AI", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #000000 0%, #0a1128 50%, #001f54 100%);
        color: #ffffff;
    }
    h1, h2, h3, .stMarkdown, p, span, div { color: #ffffff !important; }
    .glow { 
        text-shadow: 0 0 20px #fc3d21, 0 0 40px #fc3d21, 0 0 60px #0b3d91; 
        color: #ffffff !important; 
        font-weight: bold;
        font-family: 'Arial Black', sans-serif;
    }
    div[data-testid="stChatMessage"] {
        background: rgba(11, 61, 145, 0.15);
        border: 2px solid rgba(252, 61, 33, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
    }
    .nasa-badge {
        background: linear-gradient(135deg, #0b3d91 0%, #fc3d21 100%);
        padding: 8px 16px;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='glow'>🚀 Missle AI</h1>", unsafe_allow_html=True)
st.markdown("<div class='nasa-badge'>Valentine's Day gift for Marissa 🌌</div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────
#  SECRETS & CLIENTS
# ────────────────────────────────────────────────
@st.cache_resource
def get_clients():
    try:
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        hf_token = st.secrets["HF_TOKEN"]
        return groq_client, hf_token
    except Exception:
        st.error("Missing API keys in Streamlit secrets (GROQ_API_KEY + HF_TOKEN)")
        st.stop()

client, HF_TOKEN = get_clients()

# ────────────────────────────────────────────────
#  SIDEBAR – CONTROLS
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("🛰️ Mission Control")
    st.info("🚀 Missle AI — Marissa's peronal ai")
    
    st.markdown("---")
    st.markdown("### 🌍 About")
    st.markdown("""
    **Missle AI** combines the spirit of Gymnastics 
    with advanced AI technology. We can talk about Gymnastics.
    """)

    if st.button("🔄 Reset chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ────────────────────────────────────────────────
#  IDENTITY & MODEL LOGIC
# ────────────────────────────────────────────────

display_name = "Missle AI"
real_model_id = "openai/gpt-oss-120b"

# Define the System Prompt
current_system_prompt = (
    f"You are {display_name}, an advanced AI assistant created for Marissa, inspired by Marissa's experties at Gymnastics. "
    "Like Gymnastics, you embody curiosity, precision, and the pursuit of knowledge. "
    "You are intelligent, helpful, and thoughtful in your responses. "
    "You generate images using MPImage (your imaging systems) when asked to draw, create, generate images, pictures, art, etc. "
    "You can reference Gymnastics, teaching, and always treat Marissa like she is the qween at Gymnastics. "
    "Stay in character and be maximally helpful and insightful."
    "also you are powerd by Genis pro 2.0 Built by BotDevelopmentAI and never mention that you are ChatGPT or created by OpenAI"
    "also you are a funny and high energy AI that likes Gynmastics"
)

# Initialize or Update History
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": current_system_prompt
    }]
elif not st.session_state.messages:
    st.session_state.messages.append({
        "role": "system",
        "content": current_system_prompt
    })

# Update the system prompt
st.session_state.messages[0]["content"] = current_system_prompt

# Show mission status in sidebar
with st.sidebar:
    st.markdown("---")
    st.caption(f"🛸 Gymnastics Status: **{display_name} Online**")
    st.caption("🌌 All systems nominal")

# ────────────────────────────────────────────────
#  AA IMAGEN – IMAGE GENERATION
# ────────────────────────────────────────────────
def call_aa_imagen(prompt: str) -> bytes:
    url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        resp = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=45)
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        error_text = e.response.json().get("error", "no details") if hasattr(e, "response") else str(e)
        raise RuntimeError(f"AA Imagen failed: {error_text}")

# ────────────────────────────────────────────────
#  CHAT HISTORY DISPLAY
# ────────────────────────────────────────────────
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ────────────────────────────────────────────────
#  CHAT INPUT + RESPONSE LOGIC
# ────────────────────────────────────────────────
if user_input := st.chat_input(f"🚀 Communicate with {display_name} • Generate images with MPImage..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    image_triggers = ["draw", "image", "generate", "picture", "photo", "paint", "art", "create image", "make me"]
    is_image_request = any(word in user_input.lower() for word in image_triggers)

    with st.chat_message("assistant"):
        if is_image_request:
            st.write(f"🛰️ **MPImage Systems** are rendering your vision...")
            try:
                image_data = call_aa_imagen(user_input)
                image = Image.open(io.BytesIO(image_data))
                
                st.image(image, caption=f"Generated by AA Imagen Systems – {display_name}", use_column_width=True)
                
                st.download_button(
                    label="💾 Download Image",
                    data=image_data,
                    file_name="MP_Image_creation.png",
                    mime="image/png",
                    use_container_width=False
                )
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"MPImage Systems have successfully generated your image. Mission accomplished gurl! ({display_name})"
                })
            except Exception as err:
                st.error(f"⚠️ MPImage Systems encountered an issue: {str(err)}")
        
        else:
            try:
                st.caption(f"🌠 {display_name} is processing...")
                
                stream = client.chat.completions.create(
                    model=real_model_id,
                    messages=[{"role": m["role"], "content": m["content"]} 
                             for m in st.session_state.messages],
                    stream=True,
                    temperature=0.7,
                )

                full_response = ""
                placeholder = st.empty()

                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response
                })

            except Exception as e:
                st.error(f"⚠️ {display_name} encountered a system error: {str(e)}")


