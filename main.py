import streamlit as st
from utils import image_to_base64
from Leaf_Disease.main import LeafDiseaseDetector

# Page config
st.set_page_config(page_title="Leaf Disease Detection", layout="centered")

# UI Styling
st.markdown("""
<style>
.main { max-width: 800px; margin: 0 auto; }

.result-box {
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    font-size: 1.1em;
}

.healthy {
    background-color: #d4edda;
    color: #155724;
    border-left: 5px solid #28a745;
}

.warning {
    background-color: #fff3cd;
    color: #856404;
    border-left: 5px solid #ffc107;
}

.danger {
    background-color: #f8d7da;
    color: #721c24;
    border-left: 5px solid #dc3545;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🍃 Leaf Disease Detection (AI Powered)")
st.write("Upload a leaf image to detect disease using Groq AI")

# Initialize detector
try:
    detector = LeafDiseaseDetector()
except Exception as e:
    st.error(str(e))
    st.stop()

# Upload image
uploaded_file = st.file_uploader(
    "Choose a leaf image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:

    col1, col2 = st.columns(2)

    with col1:
        st.image(uploaded_file, caption="Uploaded Image", width='stretch')

    with col2:
        if st.button("🔍 Analyze Image"):

            with st.spinner("Analyzing leaf using AI..."):

                try:
                    # Convert image
                    image_base64 = image_to_base64(uploaded_file)

                    # API call
                    result = detector.analyze_leaf(image_base64)

                    # Result style
                    if result.disease_detected:
                        css_class = "danger" if result.severity == "severe" else "warning"
                        title = f"🦠 {result.disease_name}"
                    else:
                        css_class = "healthy"
                        title = "✅ Healthy Leaf"

                    # Main result box
                    st.markdown(f"""
                    <div class="result-box {css_class}">
                        <h3>{title}</h3>
                        <p><b>Type:</b> {result.disease_type} | <b>Severity:</b> {result.severity}</p>
                        <p><b>Confidence:</b> {result.confidence}%</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Disease details
                    if result.disease_detected:

                        st.subheader("🧪 Disease Details")

                        details = result.disease_details
                        if details:
                            st.markdown("**📌 Introduction**")
                            st.write(details.get("introduction", ""))

                            st.markdown("**🌿 How it spreads**")
                            st.write(details.get("how_it_spreads", ""))

                            st.markdown("**⚠️ Impact on plant**")
                            st.write(details.get("impact_on_plant", ""))

                        # Symptoms
                        st.subheader("🤒 Symptoms")
                        for s in result.symptoms:
                            st.write(f"• {s}")

                        # Causes
                        st.subheader("🧬 Causes")
                        for c in result.causes:
                            st.write(f"• {c}")

                        # Treatment Plan
                        st.subheader("🩺 Treatment Plan")

                        tp = result.treatment_plan

                        if tp.get("immediate_actions"):
                            st.markdown("**🚨 Immediate Actions**")
                            for i in tp["immediate_actions"]:
                                st.write(f"• {i}")

                        if tp.get("chemical_treatment"):
                            st.markdown("**🧪 Chemical Sprays**")
                            for i in tp["chemical_treatment"]:
                                st.write(f"• {i}")

                        if tp.get("fertilizer_suggestions"):
                            st.markdown("**🌱 Fertilizers (Pakistan)**")
                            for i in tp["fertilizer_suggestions"]:
                                st.write(f"• {i}")

                        if tp.get("organic_solutions"):
                            st.markdown("**🌿 Organic Solutions**")
                            for i in tp["organic_solutions"]:
                                st.write(f"• {i}")

                        # Sindh recommendations
                        if hasattr(result, "local_recommendations_sindh"):
                            st.subheader("📍 Sindh Farming Advice")
                            for i in result.local_recommendations_sindh:
                                st.write(f"• {i}")

                    # Roman Urdu
                    st.subheader("🗣️ Roman Urdu Explanation")
                    st.write(result.roman_urdu_explanation)

                    # Timestamp
                    st.caption(f"✅ Analyzed at: {result.timestamp}")

                except Exception as e:
                    st.error(f"❌ {str(e)}")