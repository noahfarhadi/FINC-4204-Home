"""
course_map_app.py

Course map for FINC 4204, Portfolio Theory and Its Applications, as one Streamlit page.
Needs only Streamlit. Run with:  streamlit run course_map_app.py

All texts, links, weeks, grading shares and the layout widths sit in the data blocks in
section 1. The code in sections 2 to 4 only turns those blocks into the page.
"""
from html import escape

import streamlit as st

# ---------------------------------------------------------------------------
# 1. Settings and content (edit here)
# ---------------------------------------------------------------------------
CONFIG = {
    "page_title": "FINC 4204 Course Map",
    "eyebrow": "FINC 4204 at The American University in Cairo, Fall 2026",
    "title": "Portfolio Theory and Its Applications",
    "intro": ("Fourteen weeks that run from Markowitz to your own out-of-sample test. You work with four "
              "live tools, and with a partner you monitor a simulated portfolio of USD 1,000,000 in ten "
              "weekly reports."),
    "people": "Instructor: Professor Noah Farhadi, PhD, DBA. Teaching assistant: Dan Ashraf.",
    "map_heading": "The course map",
    "map_lead": ("Fourteen weeks in four stages. Round stops are teaching weeks and square stops carry an "
                 "exam. A tool tag opens the live tool that fits the topic."),
    "does_heading": "What I do",
    "does_statement": ("I teach the theory with the mathematics in view, give you working tools to apply it, "
                       "and assess what you can show with data."),
    "facts_heading": "The portfolio you will monitor",
    "facts_lead": ("The monitoring assignment turns the theory into records you can defend. Each team of two "
                   "follows one strategy through ten weekly reports, assessed out of 20 points."),
    "facts_closing": ("Each report gives the opening and closing value, the weekly and cumulative return, the "
                      "largest movers and what explains them, with dated sources. Good analysis is judged by "
                      "the quality of your records and explanations, not by whether the portfolio went up."),
    "grading_heading": "How you are graded",
    "grading_lead": ("Five parts carry equal weight. The exams are individual and written, and the group "
                     "project is done in teams of two."),
    "tools_heading": "The four tools",
    "tools_lead": "Each tool takes a file that you upload, and its page states the format it expects.",
    "button_prefix": "Open ",
    "contact_heading": "Questions",
    # {email} is replaced by a mail link built from contact_email
    "contact_text": ("Office hours are by appointment, in online meetings booked through Calendly. My office "
                     "is BEC 2016. For anything else, write to {email}. The syllabus has the full policies "
                     "and the reading list."),
    "contact_email": "noah.farhadi@aucegypt.edu",
    "disclaimer": ("The tools calculate results from the data you upload. "
                   "The results are not investment advice."),
    "max_width_px": 1160,        # width of the content column
    "breakpoint_wide_px": 1100,  # below this width, four-column rows become two columns
    "breakpoint_narrow_px": 700, # below this width, every row becomes one column
}

# The four tools. "key" is the name that WEEKS refers to in its "tool" entries.
TOOLS = [
    {
        "key": "grid",
        "name": "Investment Grid",
        "url": "https://optimizer-r2-grid.streamlit.app/",
        "what": ("Shows the risk and return of the assets in your file and assigns each asset to a class "
                 "by the median of all assets."),
        "upload": "You upload a price file: date in the first column, then one column of closing prices per asset.",
    },
    {
        "key": "optimizer",
        "name": "Portfolio Optimizer Demo",
        "url": "https://optimizer-r2-nexuvia.streamlit.app/",
        "what": "A teaching demo of classic textbook optimizers on historical data.",
        "upload": ("You upload prices or returns: date in the first column, then one column per asset. "
                   "A Yahoo Finance source is available as a demo."),
    },
    {
        "key": "oos",
        "name": "Out-of-sample Performance Test",
        "url": "https://oosopti.streamlit.app/",
        "what": ("Measures what each portfolio recommendation earned after its date, and reports return, "
                 "volatility, Sharpe ratio and maximum drawdown."),
        "upload": ("You upload weight files with the columns date, strategy, asset and weight, plus one "
                   "price file with prices after the recommendation dates."),
    },
    {
        "key": "ta",
        "name": "Technical Analysis",
        "url": "https://teachical-analysis.streamlit.app/",
        "what": ("Shows RSI, Connors RSI, MACD and Williams %R for the asset you pick, with overbought "
                 "and oversold readings."),
        "upload": "You upload a price file with one row per date, or one row per date and asset.",
    },
]

# The stages. A week belongs to the stage whose "weeks" range (first, last) contains its number.
STAGES = [
    {"name": "Foundations and risk-return space", "weeks": (1, 4)},
    {"name": "Optimization", "weeks": (5, 7)},
    {"name": "Risk, rebalancing and performance", "weeks": (8, 10)},
    {"name": "Signals, alternatives and applications", "weeks": (11, 14)},
]

# The weeks. "tool" (optional) is a key from TOOLS and adds a button under the week.
# "exam" (optional, True) turns the round stop into a square one.
# The placement of the tools in the weeks is a suggestion and can be changed here.
WEEKS = [
    {"n": 1, "title": "Course introduction and portfolio foundations",
     "text": ("Risk-return thinking, investment strategy logic and the role of portfolio construction in "
              "real-world finance.")},
    {"n": 2, "title": "Markowitz portfolio theory",
     "text": ("Mean-variance theory, diversification, covariance, the efficient frontier, the minimum "
              "variance portfolio and optimal portfolio selection.")},
    {"n": 3, "title": "Risk-return space and Migration Theory I", "tool": "grid",
     "text": ("Risk-return positioning, portfolio zones, movement across the risk-return space and the "
              "conceptual foundation of Migration Theory.")},
    {"n": 4, "title": "Risk-return space and Migration Theory II",
     "text": ("Review of the Migration Theory literature and paper, with migration paths read as "
              "investment strategy signals.")},
    {"n": 5, "title": "Portfolio optimization I", "tool": "optimizer",
     "text": ("Utility-based optimization, investor preferences, risk aversion, constrained optimization "
              "and practical portfolio construction.")},
    {"n": 6, "title": "Portfolio optimization II", "tool": "optimizer",
     "text": ("Maximum Sharpe portfolio, minimum variance portfolio, Sortino optimization, Omega "
              "optimization and a comparison of the objectives.")},
    {"n": 7, "title": "Exam 1 and project launch", "exam": True,
     "text": ("Exam 1 covers Markowitz theory, risk-return space, the foundations of Migration Theory and "
              "optimization basics. The Migration Hypothesis project begins.")},
    {"n": 8, "title": "Portfolio rebalancing and risk control",
     "text": ("Rebalancing frequency, threshold-based rebalancing, portfolio drift, transaction costs, "
              "volatility changes, downside risk and portfolio risk limits.")},
    {"n": 9, "title": "Risk measures in portfolio strategy",
     "text": ("Value at Risk, Expected Shortfall, maximum drawdown, stress testing and risk monitoring "
              "after portfolio construction.")},
    {"n": 10, "title": "Performance evaluation", "tool": "oos",
     "text": ("Sharpe, Sortino, Omega and Treynor ratios, Jensen's alpha, benchmark comparison and "
              "risk-adjusted performance evaluation.")},
    {"n": 11, "title": "Technical analysis and quantitative trading rules", "tool": "ta",
     "text": ("RSI, MACD, Williams %R, moving averages, momentum signals, trend-following, mean reversion "
              "and systematic trading rules.")},
    {"n": 12, "title": "Alternative portfolio theories",
     "text": ("Post-Modern Portfolio Theory, risk parity, all-weather portfolios, factor-based investing, "
              "behavioral portfolio theory and other allocation frameworks.")},
    {"n": 13, "title": "Sustainable investing and real-world applications",
     "text": ("ESG integration, sustainability constraints, real-world investment mandates and portfolio "
              "construction under non-financial objectives.")},
    {"n": 14, "title": "Project presentations and Exam 2", "exam": True,
     "text": ("Students present the Migration Hypothesis applied to portfolio strategy. Exam 2 covers "
              "rebalancing, risk control, performance evaluation, technical analysis and alternative "
              "portfolio theories.")},
]

# The four blocks under "What I do": (heading, text)
DOES = [
    ("I teach",
     ("Lectures on the core concepts, theories and frameworks, followed by discussion, think-pair-share and "
      "jigsaw activities, case studies and hands-on problem solving. The course is mathematically rigorous: "
      "risk-return calculations, covariance and correlation analysis, portfolio optimization, vector algebra, "
      "rebalancing rules, risk measures and performance metrics.")),
    ("I provide",
     ("Four working tools that run on your own data, and the Eagles and Ellipse strategy allocations for the "
      "monitoring assignment. Conventions that the assignment leaves open, such as fractional shares or "
      "dividend treatment, are settled with me. I am asking Dan Ashraf, our teaching assistant, to create a "
      "series of videos that guide you through the tools. Office hours are by appointment, online through "
      "Calendly.")),
    ("I assess",
     ("Participation, two individual written exams, a group project in teams of two, and academic discipline "
      "and integrity, each worth 20 percent. Assignments, deadlines, rubrics and feedback procedures are "
      "communicated through the official course platform. The monitoring reports are judged on accurate, "
      "reconciled records and on explanations that rest on dated evidence.")),
    ("I expect",
     ("Preparation before class and about 6 to 8 hours per week outside it. Exams are completed independently. "
      "AI tools may support your learning, and any AI assistance in submitted work is disclosed with the tool, "
      "the purpose and what it generated.")),
]

# The monitoring assignment: (label, text)
FACTS = [
    ("Capital", "USD 1,000,000 per team of two students, in a simulated portfolio."),
    ("Start", "Wednesday 23 September 2026, at closing prices."),
    ("Allocation", "One strategy chosen by your team from the Eagles and Ellipse families, 17 in total. "
                   "The weights are fixed inputs."),
    ("Rules", "Long-only equities funded from cash. No borrowing, no short selling, and no discretionary "
              "trades or rebalancing after setup."),
    ("Software", "Portfolio Performance, with a parallel register that you reconcile to the software every week."),
    ("Reports", "Ten weekly reports, up to 2 points each, 20 points in total."),
]

# The grading table: (part, percent of the course grade). The syllabus table gives 20 percent for
# participation; its guidelines section mentions 30 percent. Change the number here once that is settled.
GRADING = [
    ("Participation", 20),
    ("Exam 1", 20),
    ("Exam 2", 20),
    ("Group project", 20),
    ("Academic discipline and integrity", 20),
]

# ---------------------------------------------------------------------------
# 2. Styling
# ---------------------------------------------------------------------------
# Colours are defined once as variables; a second set is used when the visitor's system is set
# to dark mode. The page paints its own background, so it looks the same whatever theme
# Streamlit itself uses. --t1 to --t5 are the five teal tints of the stage headers and grading tiles.
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap');
:root{--paper:#F4F6F9;--panel:#FFFFFF;--ink:#14213D;--body:#2B3A55;--muted:#4A586F;--line:#D3DAE4;
--accent:#0B6E75;--rail:#BADCDF;--exam:#14213D;--btn:#14213D;--btn-text:#FFFFFF;--btn-hover:#0B6E75;
--t1:#E3F1F2;--t2:#CFE6E8;--t3:#BADCDF;--t4:#A6D1D5;--t5:#92C6CB;
--foot:#14213D;--foot-text:#FFFFFF;--foot-soft:#E3E9F2;--foot-muted:#B9C4D6;}
@media (prefers-color-scheme: dark){:root{--paper:#0D1420;--panel:#142033;--ink:#E8ECF4;--body:#C9D2E2;
--muted:#A5B0C4;--line:#2A3850;--accent:#5CC8CF;--rail:#2F4A5E;--exam:#E8ECF4;--btn:#E8ECF4;
--btn-text:#0D1420;--btn-hover:#5CC8CF;--t1:#16303A;--t2:#1A3A45;--t3:#1E4450;--t4:#234E5B;--t5:#285966;
--foot:#1A2A44;--foot-text:#FFFFFF;--foot-soft:#D5DDEB;--foot-muted:#A5B0C4;}}
.stApp{background:var(--paper) !important;}
header[data-testid="stHeader"],[data-testid="stToolbar"],#MainMenu,footer{display:none !important;}
.block-container{max-width:__MAXW__px !important;margin:0 auto !important;padding:3.2rem 1.25rem 3rem !important;}
.cm{color:var(--ink);text-align:center;line-height:1.5;}
.cm a{text-decoration:none;}
.cm a:focus-visible{outline:3px solid var(--accent);outline-offset:2px;}
.cm-serif,.cm-title,.cm-h2,.cm-h3,.cm-state,.cm-pct,.cm-tname{font-family:'Source Serif 4',Georgia,'Times New Roman',serif;}
.cm-hero{padding:1.2rem 0 .4rem;}
.cm-eyebrow{font-size:1rem;color:var(--muted);}
.cm-title{font-size:clamp(2.1rem,5.4vw,3.6rem);font-weight:600;letter-spacing:-0.015em;line-height:1.1;margin:.9rem 0 0;}
.cm-intro{max-width:40rem;margin:1.5rem auto 0;font-size:clamp(1.1rem,2.2vw,1.3rem);line-height:1.55;color:var(--body);}
.cm-people{margin-top:1.2rem;font-size:1rem;color:var(--muted);}
.cm-sec{margin-top:4.2rem;}
.cm-h2{font-size:clamp(1.75rem,4vw,2.5rem);font-weight:600;letter-spacing:-0.01em;line-height:1.15;margin:0;}
.cm-lead{max-width:41rem;margin:1rem auto 0;font-size:1.12rem;color:var(--body);}
.cm-stages,.cm-tools{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.25rem;margin-top:2.6rem;text-align:left;}
.cm-stage{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);
border-radius:6px;overflow:hidden;}
.cm-sh{padding:1.1rem 1.35rem;}
.cm-t1{background:var(--t1);}.cm-t2{background:var(--t2);}.cm-t3{background:var(--t3);}
.cm-t4{background:var(--t4);}.cm-t5{background:var(--t5);}
.cm-range{font-size:.88rem;color:var(--body);}
.cm-h3{font-size:1.3rem;font-weight:600;line-height:1.25;margin:.15rem 0 0;}
.cm-weeks{padding:1.5rem 1.35rem .25rem;}
.cm-wk{display:grid;grid-template-columns:14px minmax(0,1fr);column-gap:1rem;}
.cm-rail{display:flex;flex-direction:column;align-items:center;}
.cm-dot{width:14px;height:14px;border-radius:50%;background:var(--accent);margin-top:5px;flex:none;}
.cm-dot.sq{border-radius:2px;background:var(--exam);}
.cm-line{width:2px;flex:1;background:var(--rail);margin-top:5px;}
.cm-wk:last-child .cm-line{display:none;}
.cm-wb{padding-bottom:1.5rem;}
.cm-wlab{font-size:.88rem;color:var(--muted);}
.cm-wt{font-weight:600;font-size:1.06rem;line-height:1.3;}
.cm-wd{margin-top:.4rem;font-size:.95rem;line-height:1.5;color:var(--body);}
.cm a.cm-tag{display:inline-flex;align-items:center;gap:.5rem;margin-top:.75rem;min-height:44px;
padding:.5rem .9rem;box-sizing:border-box;border:1.5px solid var(--accent);border-radius:6px;
background:var(--panel);color:var(--accent) !important;font-size:.95rem;font-weight:600;line-height:1.3;}
.cm a.cm-tag:hover{background:var(--t1);}
.cm-tag svg{flex:none;}
.cm-does{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2.5rem 3.5rem;margin:3.2rem auto 0;
max-width:1000px;text-align:left;}
.cm-blk{border-top:1px solid var(--line);padding-top:1.2rem;}
.cm-blk .cm-h3{font-size:1.5rem;margin:0;}
.cm-blk .cm-p{margin-top:.6rem;font-size:1.06rem;line-height:1.6;color:var(--body);}
.cm-state{max-width:47rem;margin:1.5rem auto 0;font-weight:500;font-size:clamp(1.3rem,2.6vw,1.7rem);
line-height:1.4;}
.cm-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2rem 2.5rem;max-width:1000px;
margin:3rem auto 0;background:var(--panel);border:1px solid var(--line);border-radius:6px;
padding:2.2rem 2.2rem .5rem;text-align:left;}
.cm-fact{padding-bottom:1.7rem;}
.cm-flab{font-size:.95rem;font-weight:600;color:var(--muted);}
.cm-fval{margin-top:.25rem;font-size:1.06rem;line-height:1.5;}
.cm-close{max-width:47rem;margin:2rem auto 0;font-size:1.06rem;line-height:1.6;color:var(--body);}
.cm-grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;max-width:1000px;
margin:3rem auto 0;background:var(--line);border:1px solid var(--line);border-radius:6px;overflow:hidden;
text-align:left;}
.cm-tile{padding:1.7rem 1.35rem;}
.cm-pct{font-size:2.25rem;font-weight:600;line-height:1.1;}
.cm-tlab{margin-top:.5rem;font-size:1.06rem;font-weight:600;}
.cm-tool{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);
border-radius:6px;padding:1.6rem 1.5rem 1.5rem;}
.cm-tname{font-size:1.35rem;font-weight:600;line-height:1.25;}
.cm-what{margin-top:.65rem;font-size:1rem;line-height:1.55;color:var(--body);}
.cm-up{margin-top:.8rem;font-size:.95rem;line-height:1.5;color:var(--muted);}
.cm-fill{flex:1;min-height:1.3rem;}
.cm a.cm-btn{display:flex;align-items:center;justify-content:center;min-height:46px;padding:.6rem .9rem;
box-sizing:border-box;text-align:center;background:var(--btn);color:var(--btn-text) !important;
font-weight:600;border-radius:6px;border:1px solid var(--btn);transition:background-color .15s,border-color .15s;}
.cm a.cm-btn:hover{background:var(--btn-hover);border-color:var(--btn-hover);}
.cm-foot{margin-top:4.2rem;background:var(--foot);color:var(--foot-text);border-radius:6px;
padding:3.4rem 1.6rem 2.6rem;}
.cm-foot .cm-h2{color:var(--foot-text);font-size:clamp(1.6rem,3.6vw,2.1rem);}
.cm-ftext{max-width:47rem;margin:1.1rem auto 0;font-size:1.1rem;line-height:1.6;color:var(--foot-soft);}
.cm a.cm-mail{color:var(--foot-text) !important;font-weight:600;text-decoration:underline;}
.cm-fdisc{max-width:47rem;margin:2rem auto 0;font-size:.95rem;line-height:1.6;color:var(--foot-muted);}
@media (max-width:__BPW__px){
.cm-stages,.cm-tools{grid-template-columns:repeat(2,minmax(0,1fr));}
.cm-facts{grid-template-columns:repeat(2,minmax(0,1fr));}
}
@media (max-width:__BPN__px){
.cm-stages,.cm-tools,.cm-facts,.cm-does{grid-template-columns:minmax(0,1fr);}
.cm-facts{padding:1.6rem 1.3rem .3rem;}
.cm-sec{margin-top:3.4rem;}
}
@media (prefers-reduced-motion: reduce){.cm a.cm-btn{transition:none;}}
"""

# One small "opens in a new tab" arrow used inside the tool tags
ARROW_SVG = ('<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" '
             'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
             'focusable="false"><path d="M8 2h4v4M12 2L6.5 7.5M10 8.5V12H2V4h3.5"></path></svg>')


# ---------------------------------------------------------------------------
# 3. Building blocks (each function returns one HTML string without line breaks)
# ---------------------------------------------------------------------------
def link(url, inner_html, css_class):
    """Anchor that opens in a new tab. inner_html must already be escaped."""
    return (f'<a class="{css_class}" href="{escape(url, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{inner_html}</a>')


def section(heading, lead=None, body=""):
    """A centered section: heading, optional one-line lead, then the body HTML."""
    lead_html = f'<div class="cm-lead">{escape(lead)}</div>' if lead else ""
    return (f'<div class="cm cm-sec"><div class="cm-h2" role="heading" aria-level="2">{escape(heading)}</div>'
            f'{lead_html}{body}</div>')


def week_html(week, tools_by_key):
    """One stop on the line of a stage: marker, week number, title, text and optional tool tag."""
    marker = "cm-dot sq" if week.get("exam") else "cm-dot"
    tag = ""
    tool = tools_by_key.get(week.get("tool"))
    if tool:                                  # a tool tag only if the week names a known tool
        tag = link(tool["url"], f'{ARROW_SVG}<span>{escape(tool["name"])}</span>', "cm-tag")
    return (
        '<div class="cm-wk">'
        f'<div class="cm-rail"><span class="{marker}"></span><span class="cm-line"></span></div>'
        '<div class="cm-wb">'
        f'<div class="cm-wlab">Week {week["n"]}</div>'
        f'<div class="cm-wt" role="heading" aria-level="4">{escape(week["title"])}</div>'
        f'<div class="cm-wd">{escape(week["text"])}</div>{tag}'
        '</div></div>')


def stage_html(index, stage, weeks, tools_by_key):
    """One stage card: tinted header with its week range, then the weeks that fall inside the range."""
    first, last = stage["weeks"]
    inside = [w for w in weeks if first <= w["n"] <= last]
    tint = min(index + 1, 5)                  # five tints exist
    return (
        '<div class="cm-stage">'
        f'<div class="cm-sh cm-t{tint}"><div class="cm-range">Weeks {first} to {last}</div>'
        f'<div class="cm-h3" role="heading" aria-level="3">{escape(stage["name"])}</div></div>'
        f'<div class="cm-weeks">{"".join(week_html(w, tools_by_key) for w in inside)}</div>'
        '</div>')


def does_html(blocks):
    """The four 'I teach / provide / assess / expect' blocks."""
    items = "".join(
        f'<div class="cm-blk"><div class="cm-h3" role="heading" aria-level="3">{escape(head)}</div>'
        f'<div class="cm-p">{escape(text)}</div></div>'
        for head, text in blocks)
    return f'<div class="cm-does">{items}</div>'


def facts_html(facts):
    """The fact panel of the monitoring assignment."""
    items = "".join(
        f'<div class="cm-fact"><div class="cm-flab">{escape(label)}</div><div class="cm-fval">{escape(text)}</div></div>'
        for label, text in facts)
    return f'<div class="cm-facts">{items}</div>'


def grading_html(parts):
    """One tile per graded part, with a tint that gets darker from left to right."""
    tiles = "".join(
        f'<div class="cm-tile cm-t{min(i + 1, 5)}"><div class="cm-pct">{pct:g}%</div>'
        f'<div class="cm-tlab">{escape(name)}</div></div>'
        for i, (name, pct) in enumerate(parts))
    return f'<div class="cm-grade">{tiles}</div>'


def tool_card_html(tool, button_prefix):
    """One tool card: name, what it does, what to upload, button."""
    return (
        '<div class="cm-tool">'
        f'<div class="cm-tname" role="heading" aria-level="3">{escape(tool["name"])}</div>'
        f'<div class="cm-what">{escape(tool["what"])}</div>'
        f'<div class="cm-up">{escape(tool["upload"])}</div>'
        '<div class="cm-fill"></div>'
        f'{link(tool["url"], escape(button_prefix + tool["name"]), "cm-btn")}'
        '</div>')


# ---------------------------------------------------------------------------
# 4. Page
# ---------------------------------------------------------------------------
st.set_page_config(page_title=CONFIG["page_title"], layout="wide", initial_sidebar_state="collapsed")

# Step 1: styles (content width and the two breakpoints come from CONFIG)
css = (CSS.replace("__MAXW__", str(int(CONFIG["max_width_px"])))
          .replace("__BPW__", str(int(CONFIG["breakpoint_wide_px"])))
          .replace("__BPN__", str(int(CONFIG["breakpoint_narrow_px"]))))
st.markdown(f"<style>{' '.join(css.split())}</style>", unsafe_allow_html=True)

tools_by_key = {t["key"]: t for t in TOOLS}

# Step 2: title block with course name, short description and the people
st.markdown(
    '<div class="cm cm-hero">'
    f'<div class="cm-eyebrow">{escape(CONFIG["eyebrow"])}</div>'
    f'<div class="cm-title" role="heading" aria-level="1">{escape(CONFIG["title"])}</div>'
    f'<div class="cm-intro">{escape(CONFIG["intro"])}</div>'
    f'<div class="cm-people">{escape(CONFIG["people"])}</div>'
    '</div>', unsafe_allow_html=True)

# Step 3: the course map, one card per stage
stages_body = "".join(stage_html(i, s, WEEKS, tools_by_key) for i, s in enumerate(STAGES))
st.markdown(section(CONFIG["map_heading"], CONFIG["map_lead"], f'<div class="cm-stages">{stages_body}</div>'),
            unsafe_allow_html=True)

# Step 4: what the instructor does
st.markdown(section(CONFIG["does_heading"], None,
                    f'<div class="cm-state">{escape(CONFIG["does_statement"])}</div>{does_html(DOES)}'),
            unsafe_allow_html=True)

# Step 5: the monitoring assignment
st.markdown(section(CONFIG["facts_heading"], CONFIG["facts_lead"],
                    f'{facts_html(FACTS)}<div class="cm-close">{escape(CONFIG["facts_closing"])}</div>'),
            unsafe_allow_html=True)

# Step 6: grading
st.markdown(section(CONFIG["grading_heading"], CONFIG["grading_lead"], grading_html(GRADING)),
            unsafe_allow_html=True)

# Step 7: the four tools
tools_body = "".join(tool_card_html(t, CONFIG["button_prefix"]) for t in TOOLS)
st.markdown(section(CONFIG["tools_heading"], CONFIG["tools_lead"], f'<div class="cm-tools">{tools_body}</div>'),
            unsafe_allow_html=True)

# Step 8: contact block and disclaimer
mail = link("mailto:" + CONFIG["contact_email"], escape(CONFIG["contact_email"]), "cm-mail")
contact_text = escape(CONFIG["contact_text"]).replace("{email}", mail)
st.markdown(
    '<div class="cm cm-foot">'
    f'<div class="cm-h2" role="heading" aria-level="2">{escape(CONFIG["contact_heading"])}</div>'
    f'<div class="cm-ftext">{contact_text}</div>'
    f'<div class="cm-fdisc">{escape(CONFIG["disclaimer"])}</div>'
    '</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Version log
# ---------------------------------------------------------------------------
# v1.0 (2026-10-08)  New file. Added: CONFIG, TOOLS, STAGES, WEEKS, DOES, FACTS, GRADING, CSS,
#   ARROW_SVG, link, section, week_html, stage_html, does_html, facts_html, grading_html,
#   tool_card_html, and the page build in section 4 (steps 1 to 8). Content is taken from the
#   published FINC 4204 course map page.
