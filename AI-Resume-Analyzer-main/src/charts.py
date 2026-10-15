import plotly.express as px
import plotly.graph_objects as go


def ats_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%"},
            title={"text": "ATS Match Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 40], "color": "#ef4444"},
                    {"range": [40, 70], "color": "#facc15"},
                    {"range": [70, 100], "color": "#22c55e"},
                ],
            },
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def skills_chart(ats_analysis):

    labels = [
        "Matching Skills",
        "Missing Skills",
    ]

    values = [
        len(ats_analysis["matching_skills"]),
        len(ats_analysis["missing_skills"]),
    ]

    fig = px.pie(
        names=labels,
        values=values,
        hole=0.6,
    )

    fig.update_layout(
        title="Skills Distribution",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def resume_stats_chart(stats):

    labels = [
        "Words",
        "Characters",
    ]

    values = [
        stats["word_count"],
        stats["character_count"],
    ]

    fig = px.bar(
        x=labels,
        y=values,
        text=values,
    )

    fig.update_layout(
        title="Resume Statistics",
        height=350,
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig