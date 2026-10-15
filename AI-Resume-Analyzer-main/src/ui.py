import streamlit as st

from src.charts import (
    ats_gauge,
    skills_chart,
    resume_stats_chart,
)

from src.utils import (
    keyword_analysis,
    badge_html,
    resume_statistics,
)


def display_dashboard(summary, ats_analysis, interview_questions, resume_text, job_description):

    stats = resume_statistics(resume_text)

    keywords = keyword_analysis(
        resume_text,
        job_description,
    )

    st.success("✅ Resume analyzed successfully!")

    st.markdown("## 📊 Resume Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "ATS Score",
            f"{ats_analysis['ats_score']}%",
        )

    with c2:
        st.metric(
            "Words",
            stats["word_count"],
        )

    with c3:
        st.metric(
            "Characters",
            stats["character_count"],
        )

    with c4:
        st.metric(
            "Reading Time",
            f"{stats['reading_time']} min",
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.plotly_chart(
            ats_gauge(
                ats_analysis["ats_score"]
            ),
            width="stretch",
        )

    with right:
        st.plotly_chart(
            skills_chart(
                ats_analysis
            ),
            width="stretch",
        )

    st.markdown("---")

    st.plotly_chart(
        resume_stats_chart(stats),
        width="stretch",
    )

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(
        [
            "📄 Summary",
            "🎯 ATS Analysis",
            "🎤 Interview Questions",
        ]
    )

    with tab1:

        st.markdown(summary)

    with tab2:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matching Skills")

            for skill in ats_analysis["matching_skills"]:
                st.success(skill)

        with col2:

            st.subheader("❌ Missing Skills")

            for skill in ats_analysis["missing_skills"]:
                st.error(skill)

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:

            st.subheader("💪 Strengths")

            for item in ats_analysis["strengths"]:
                st.info(item)

        with col4:

            st.subheader("⚠️ Weaknesses")

            for item in ats_analysis["weaknesses"]:
                st.warning(item)

        st.markdown("---")

        st.subheader("💡 Suggestions")

        for suggestion in ats_analysis["suggestions"]:
            st.write("•", suggestion)

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:

            st.subheader("🟢 Matching Keywords")

            if keywords["matching"]:

                html = ""

                for word in keywords["matching"]:
                    html += badge_html(
                        word,
                        "#16a34a",
                    )

                st.markdown(
                    html,
                    unsafe_allow_html=True,
                )

            else:
                st.info("No matching keywords found.")

        with c2:

            st.subheader("🔴 Missing Keywords")

            if keywords["missing"]:

                html = ""

                for word in keywords["missing"]:
                    html += badge_html(
                        word,
                        "#dc2626",
                    )

                st.markdown(
                    html,
                    unsafe_allow_html=True,
                )

            else:
                st.success("Excellent! No missing keywords.")

    with tab3:

        st.markdown(interview_questions)