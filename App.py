import os
import streamlit as st

from step_reader import save_uploaded_step, read_step_file, count_topology
from validator import validate_design
from ml_model import load_model, predict_design
from report_generator import generate_report

st.set_page_config(page_title="STEP Design Validator", layout="wide")
st.title("AI-Powered CAD STEP Design Validator")

st.markdown(
    """
Upload a **STEP/STP file**, inspect its basic geometry, enter design parameters,
and run **rule-based + AI-assisted validation**.
"""
)

model = load_model()

uploaded_file = st.file_uploader("Upload STEP / STP file", type=["step", "stp"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Design Parameters")
    thickness = st.number_input("Thickness (mm)", min_value=0.1, value=1.5, step=0.1)
    hole_diameter = st.number_input("Hole Diameter (mm)", min_value=0.1, value=10.0, step=0.1)
    hole_distance = st.number_input("Hole Distance (mm)", min_value=0.1, value=12.0, step=0.1)
    edge_distance = st.number_input("Edge Distance (mm)", min_value=0.1, value=8.0, step=0.1)
    fillet_present_text = st.selectbox("Fillet Present?", ["No", "Yes"])
    fillet_present = 1 if fillet_present_text == "Yes" else 0

if uploaded_file is not None:
    try:
        # Save and read STEP file
        step_path = save_uploaded_step(uploaded_file)
        step_data = read_step_file(step_path)
        step_info = count_topology(step_data)

        with col2:
            st.subheader("STEP Geometry Summary")
            st.write(f"Filename: {uploaded_file.name}")
            st.write(f"File Size: {step_data['file_size_kb']} KB")
            st.write(f"Faces: {step_info['faces']}")
            st.write(f"Edges: {step_info['edges']}")
            st.write(f"Solids: {step_info['solids']}")
            st.success("STEP file uploaded successfully!")

        # Run validation
        result = validate_design(
            thickness,
            hole_diameter,
            hole_distance,
            edge_distance,
            fillet_present
        )

        # AI prediction
        ai_prediction = predict_design(
            model,
            thickness,
            hole_diameter,
            hole_distance,
            edge_distance,
            fillet_present
        )

        # Display results
        st.subheader("Validation Results")
        st.write(f"Rule-Based Status: {result['status']}")
        st.write(f"Compliance Score: {result['score']}/100")
        st.write(f"AI Prediction: {ai_prediction}")

        # Issues
        st.subheader("Issues Found")
        if result["issues"]:
            for issue in result["issues"]:
                st.write(f"- {issue}")
        else:
            st.success("No major issues found.")

        # Suggestions
        st.subheader("Suggestions")
        if result["suggestions"]:
            for suggestion in result["suggestions"]:
                st.write(f"- {suggestion}")
        else:
            st.success("Design looks good.")

        # Report
        if st.button("Generate PDF Report"):
            report_path = generate_report(
                uploaded_file.name,
                step_info,
                result,
                ai_prediction
            )

            with open(report_path, "rb") as f:
                st.download_button(
                    "Download Report",
                    f,
                    file_name="design_report.pdf"
                )

    except Exception as e:
        st.error(f"Error processing STEP file: {e}")

else:
    st.info("Please upload a STEP file to begin.")
