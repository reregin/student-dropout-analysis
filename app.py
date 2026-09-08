from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model" / "student_status_model.joblib"

APPLICATION_LABELS = {
    1: "1st phase - general", 2: "Ordinance 612/93", 5: "1st phase - Azores",
    7: "Other higher course holders", 10: "Ordinance 854-B/99",
    15: "International bachelor", 16: "1st phase - Madeira",
    17: "2nd phase - general", 18: "3rd phase - general",
    26: "Different plan", 27: "Other institution", 39: "Over 23 years old",
    42: "Transfer", 43: "Change of course", 44: "Technological specialization",
    51: "Change institution/course", 53: "Short cycle diploma",
    57: "International change institution/course",
}
COURSE_LABELS = {
    33: "Biofuel Production Technologies", 171: "Animation and Multimedia Design",
    8014: "Social Service (evening)", 9003: "Agronomy",
    9070: "Communication Design", 9085: "Veterinary Nursing",
    9119: "Informatics Engineering", 9130: "Equinculture", 9147: "Management",
    9238: "Social Service", 9254: "Tourism", 9500: "Nursing",
    9556: "Oral Hygiene", 9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication", 9853: "Basic Education",
    9991: "Management (evening)",
}
QUALIFICATION_LABELS = {
    1: "Secondary education", 2: "Bachelor degree", 3: "Degree", 4: "Master",
    5: "Doctorate", 6: "Higher education attendance", 9: "12th year not completed",
    10: "11th year not completed", 12: "Other 11th year", 14: "10th year",
    15: "10th year not completed", 19: "Basic education 3rd cycle",
    38: "Basic education 2nd cycle", 39: "Technological specialization",
    40: "Degree first cycle", 42: "Professional higher technical",
    43: "Master second cycle",
}
BINARY_LABELS = {0: "No", 1: "Yes"}
ATTENDANCE_LABELS = {0: "Evening", 1: "Daytime"}
STATUS_COLORS = {"Dropout": "#C94B5B", "Graduate": "#23877A"}


st.set_page_config(
    page_title="Student Early-Warning Prototype",
    page_icon="🎓",
    layout="wide",
)
st.markdown(
    """
    <style>
    .block-container {max-width: 1180px; padding-top: 2.2rem; padding-bottom: 3rem;}
    [data-testid="stMetric"] {background: #F7F9FC; border: 1px solid #E5E9F0; border-radius: 12px; padding: 14px;}
    .support-note {background: #EEF6F5; border-left: 4px solid #23877A; padding: 14px 16px; border-radius: 6px;}
    .warning-note {background: #FFF5F2; border-left: 4px solid #C94B5B; padding: 14px 16px; border-radius: 6px;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_artifact(path: Path):
    return joblib.load(path)


def select_code(label, feature, artifact, labels):
    options = artifact["input_options"][feature]
    default = artifact["input_defaults"][feature]
    index = options.index(default) if default in options else 0
    return st.selectbox(
        label,
        options=options,
        index=index,
        format_func=lambda value: labels.get(value, f"Code {value}"),
    )


if not MODEL_PATH.exists():
    st.error(f"Model artifact was not found at `{MODEL_PATH}`.")
    st.stop()

artifact = load_artifact(MODEL_PATH)

st.title("Student Early-Warning Prototype")
st.caption("Jaya Jaya Institut · Binary Dropout-vs-Graduate model · Submission by reregin")
st.markdown(
    """
    <div class="support-note">
    This prototype scores currently enrolled students after semester one using a
    model trained only on historical Dropout and Graduate outcomes. It does not
    determine sanctions, admission, tuition access, or academic eligibility.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Model information")
    st.write(f"**Checkpoint:** {artifact['checkpoint']}")
    st.write(f"**Model:** {artifact['model_name']}")
    st.write(f"**Features:** {len(artifact['feature_columns'])}")
    st.write(f"**Dropout alert threshold:** {artifact['dropout_threshold']:.3f}")
    st.divider()
    st.caption(
        "Training uses only students with resolved Dropout or Graduate outcomes. "
        "Students still Enrolled were excluded from training and reserved for future scoring. "
        "Students whose recorded status was Enrolled were excluded from training "
        "and reserved for future scoring. The model also excludes gender, "
        "nationality, marital status, age, international "
        "status, special needs, family background, macroeconomic indicators, and "
        "all second-semester performance fields."
    )

with st.form("student_form"):
    st.subheader("Student information")
    enrollment_tab, finance_tab, semester_tab = st.tabs(
        ["Enrollment", "Financial and schedule", "Semester one"]
    )

    with enrollment_tab:
        left, right = st.columns(2)
        with left:
            application_mode = select_code(
                "Application mode", "Application_mode", artifact, APPLICATION_LABELS
            )
            course = select_code("Course", "Course", artifact, COURSE_LABELS)
            previous_qualification = select_code(
                "Previous qualification", "Previous_qualification", artifact,
                QUALIFICATION_LABELS,
            )
            application_order = st.number_input(
                "Application order (0 = first choice)", min_value=0, max_value=9,
                value=int(artifact["input_defaults"]["Application_order"]), step=1,
            )
        with right:
            previous_grade = st.number_input(
                "Previous qualification grade", min_value=95.0, max_value=190.0,
                value=float(artifact["input_defaults"]["Previous_qualification_grade"]),
                step=0.1,
            )
            admission_grade = st.number_input(
                "Admission grade", min_value=95.0, max_value=190.0,
                value=float(artifact["input_defaults"]["Admission_grade"]), step=0.1,
            )
            displaced = select_code("Displaced student", "Displaced", artifact, BINARY_LABELS)

    with finance_tab:
        left, right = st.columns(2)
        with left:
            tuition = select_code(
                "Tuition fees up to date", "Tuition_fees_up_to_date", artifact,
                BINARY_LABELS,
            )
            debtor = select_code("Debtor", "Debtor", artifact, BINARY_LABELS)
        with right:
            scholarship = select_code(
                "Scholarship holder", "Scholarship_holder", artifact, BINARY_LABELS
            )
            attendance = select_code(
                "Attendance schedule", "Daytime_evening_attendance", artifact,
                ATTENDANCE_LABELS,
            )

    with semester_tab:
        left, middle, right = st.columns(3)
        with left:
            credited = st.number_input("Credited units", 0, 20, 0, 1)
            enrolled = st.number_input("Enrolled units", 0, 26, 6, 1)
        with middle:
            evaluations = st.number_input("Evaluations", 0, 45, 8, 1)
            approved = st.number_input("Approved units", 0, 26, 5, 1)
        with right:
            semester_grade = st.number_input(
                "Average grade", 0.0, 20.0,
                float(artifact["input_defaults"]["Curricular_units_1st_sem_grade"]),
                0.1,
            )
            without_evaluations = st.number_input(
                "Units without evaluations", 0, 12, 0, 1
            )

    submitted = st.form_submit_button("Assess student status", type="primary")

if submitted:
    validation_errors = []
    if approved > enrolled:
        validation_errors.append("Approved units cannot exceed enrolled units.")
    if enrolled == 0 and approved > 0:
        validation_errors.append("Approved units must be zero when no units are enrolled.")
    if without_evaluations > enrolled:
        validation_errors.append("Units without evaluations cannot exceed enrolled units.")

    if validation_errors:
        for message in validation_errors:
            st.error(message)
    else:
        input_row = pd.DataFrame([{
            "Application_mode": application_mode,
            "Application_order": application_order,
            "Course": course,
            "Daytime_evening_attendance": attendance,
            "Previous_qualification": previous_qualification,
            "Previous_qualification_grade": previous_grade,
            "Admission_grade": admission_grade,
            "Displaced": displaced,
            "Debtor": debtor,
            "Tuition_fees_up_to_date": tuition,
            "Scholarship_holder": scholarship,
            "Curricular_units_1st_sem_credited": credited,
            "Curricular_units_1st_sem_enrolled": enrolled,
            "Curricular_units_1st_sem_evaluations": evaluations,
            "Curricular_units_1st_sem_approved": approved,
            "Curricular_units_1st_sem_grade": semester_grade,
            "Curricular_units_1st_sem_without_evaluations": without_evaluations,
        }])[artifact["feature_columns"]]

        probabilities = artifact["model"].predict_proba(input_row)[0]
        classes = list(artifact["model"].classes_)
        probability_map = dict(zip(classes, probabilities))
        dropout_probability = float(probability_map[1])
        alert = dropout_probability >= artifact["dropout_threshold"]
        predicted_status = "Dropout" if alert else "Graduate"

        st.divider()
        st.subheader("Assessment result")
        result_col, risk_col, review_col = st.columns(3)
        result_col.metric("Predicted status", predicted_status)
        risk_col.metric("Estimated dropout probability", f"{dropout_probability:.1%}")
        review_col.metric("Support review", "Prioritize" if alert else "Routine monitoring")

        probability_table = pd.DataFrame({
            "Status": ["Graduate", "Dropout"],
            "Estimated probability": [probability_map[0], probability_map[1]],
        })
        chart_col, table_col = st.columns([1.4, 1])
        with chart_col:
            st.bar_chart(probability_table.set_index("Status"), color="#457B9D")
        with table_col:
            st.dataframe(
                probability_table.style.format({"Estimated probability": "{:.1%}"}),
                hide_index=True,
                width="stretch",
            )

        if alert:
            st.markdown(
                """
                <div class="warning-note"><strong>Support review recommended.</strong>
                The Dropout probability exceeds the training-tuned screening threshold.
                A staff member should verify context before contacting the student.</div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("The score is below the outreach threshold. Continue routine monitoring.")

        support_actions = []
        approval_rate = approved / enrolled if enrolled else None
        if tuition == 0 or debtor == 1:
            support_actions.append("Offer a confidential financial-support or payment-plan consultation.")
        if approved == 0 or (approval_rate is not None and approval_rate < 0.5):
            support_actions.append("Arrange an academic recovery meeting with an advisor or tutor.")
        if attendance == 0:
            support_actions.append("Check whether evening or flexible support hours are needed.")
        if without_evaluations > 0:
            support_actions.append("Review missed evaluations and agree on a completion plan.")
        if not support_actions:
            support_actions.append("Continue ordinary advisor check-ins and monitor the next academic checkpoint.")

        st.subheader("Suggested human review")
        for action in support_actions:
            st.write(f"- {action}")
        st.caption(
            "Probabilities are estimates from historical data, not certainties. "
            "Staff remain responsible for interpreting the result and selecting support."
        )
