import math
import re


def resume_statistics(resume_text):

    words = resume_text.split()

    word_count = len(words)

    character_count = len(resume_text)

    reading_time = max(1, math.ceil(word_count / 200))

    return {
        "word_count": word_count,
        "character_count": character_count,
        "reading_time": reading_time,
    }


def extract_keywords(text):

    text = text.lower()

    keywords = set(
        re.findall(r"[a-zA-Z][a-zA-Z+#.\-]{1,}", text)
    )

    stop_words = {
        "the","and","for","with","from","that","this","have","will",
        "your","you","our","their","they","are","was","were","been",
        "into","about","using","use","used","job","role","work",
        "candidate","required","preferred","experience","years",
        "ability","skills","skill","knowledge","responsible","strong",
        "good","excellent","team","teams","including","etc"
    }

    keywords = keywords - stop_words

    return keywords


def keyword_analysis(resume_text, job_description):

    resume_keywords = extract_keywords(resume_text)

    jd_keywords = extract_keywords(job_description)

    matching = sorted(resume_keywords & jd_keywords)

    missing = sorted(jd_keywords - resume_keywords)

    return {
        "matching": matching,
        "missing": missing,
    }


def badge_html(text, color):

    return f"""
    <span style="
        display:inline-block;
        background:{color};
        color:white;
        padding:6px 12px;
        border-radius:20px;
        margin:4px;
        font-size:14px;
        font-weight:600;">
        {text}
    </span>
    """
