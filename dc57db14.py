
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Scholarship Search Agent",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 Scholarship Search Agent for Female English Majors")
st.markdown("**Find personalized scholarship opportunities matching your profile**")

# Sidebar for applicant profile
st.sidebar.header("📝 Your Profile")

with st.sidebar:
    name = st.text_input("Full Name", value="Jane Doe")
    gender = st.selectbox("Gender", ["female", "male", "non-binary", "prefer not to say"])
    major = st.selectbox(
        "Major/Intended Major",
        ["English Literature", "Creative Writing", "English", "Humanities", 
         "Comparative Literature", "Journalism", "Publishing"]
    )
    gpa = st.number_input("GPA (0.0 - 4.0)", min_value=0.0, max_value=4.0, value=3.5, step=0.1)
    location = st.text_input("State/Region", value="United States")
    age = st.number_input("Age", min_value=15, max_value=100, value=20)

    st.markdown("---")
    st.subheader("Additional Info")
    interests = st.multiselect(
        "Areas of Interest",
        ["Creative Writing", "Poetry", "Fiction", "Journalism", 
         "Publishing", "Literary Criticism", "Children's Literature"]
    )

    min_score = st.slider("Minimum Match Score", 0, 100, 40, 5)

    search_button = st.sidebar.button("🔍 Search Scholarships", type="primary")

# Scholarship Database
class ScholarshipDatabase:
    @staticmethod
    def get_scholarships():
        return [
            {
                "name": "Alexandra Rowan Voices of Tomorrow Scholarship",
                "amount": 3000,
                "deadline": "2026-04-01",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["english", "creative writing", "literature"],
                    "gpa_min": 0.0,
                    "essay_required": True
                },
                "description": "For women aspiring writers pursuing degrees in English/writing",
                "url": "https://bold.org/scholarships/alexandra-rowan-voices-of-tomorrow/",
                "tags": ["women", "writing", "creative"]
            },
            {
                "name": "GRCF Ladies Literary Club Scholarship",
                "amount": 5000,
                "deadline": "2026-03-01",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["english", "literature", "humanities"],
                    "gpa_min": 3.0,
                    "essay_required": True,
                    "location": ["Michigan"]
                },
                "description": "For female literature majors in Michigan",
                "url": "https://bold.org/scholarships/",
                "tags": ["women", "literature", "regional"]
            },
            {
                "name": "Des Moines Women's Club Literature Scholarship",
                "amount": 2000,
                "deadline": "2026-01-27",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["literature", "english"],
                    "gpa_min": 0.0,
                    "essay_required": True
                },
                "description": "Supporting women in literature studies",
                "url": "https://bold.org/scholarships/",
                "tags": ["women", "literature"]
            },
            {
                "name": "Valorena Publishing & Cocoa Kids Collection Scholarship",
                "amount": 500,
                "deadline": "2026-03-27",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["english", "writing", "publishing"],
                    "gpa_min": 0.0,
                    "essay_required": True,
                    "diversity": ["BIPOC", "multicultural"]
                },
                "description": "For BIPOC/multicultural women in writing and publishing",
                "url": "https://bold.org/scholarships/",
                "tags": ["women", "diversity", "publishing"]
            },
            {
                "name": "AAUW Career Development Grants",
                "amount": 8000,
                "deadline": "2026-02-15",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["english", "humanities", "liberal arts"],
                    "gpa_min": 3.0,
                    "essay_required": True
                },
                "description": "American Association of University Women grants for women",
                "url": "https://www.aauw.org/resources/programs/fellowships-grants/",
                "tags": ["women", "prestigious", "national"]
            },
            {
                "name": "Scholastic Art & Writing Awards",
                "amount": 10000,
                "deadline": "2026-02-01",
                "eligibility": {
                    "gender": ["any"],
                    "major": ["creative writing", "english", "writing"],
                    "gpa_min": 0.0,
                    "essay_required": False,
                    "portfolio_required": True
                },
                "description": "For talented young writers with portfolio submissions",
                "url": "https://www.artandwriting.org/",
                "tags": ["writing", "portfolio", "prestigious"]
            },
            {
                "name": "Sigma Tau Delta International English Honor Society Scholarships",
                "amount": 1500,
                "deadline": "2026-03-15",
                "eligibility": {
                    "gender": ["any"],
                    "major": ["english"],
                    "gpa_min": 3.5,
                    "essay_required": True,
                    "membership_required": True
                },
                "description": "For English Honor Society members",
                "url": "https://www.english.org/scholarships/",
                "tags": ["english", "academic excellence"]
            },
            {
                "name": "Jeannette Rankin Women's Scholarship Fund",
                "amount": 2500,
                "deadline": "2026-03-01",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["any"],
                    "gpa_min": 2.5,
                    "age_min": 35,
                    "essay_required": True
                },
                "description": "For women age 35+ pursuing any degree",
                "url": "https://rankinfoundation.org/",
                "tags": ["women", "non-traditional"]
            },
            {
                "name": "P.E.O. Scholar Awards",
                "amount": 20000,
                "deadline": "2026-11-30",
                "eligibility": {
                    "gender": ["female"],
                    "major": ["any"],
                    "gpa_min": 3.5,
                    "essay_required": True,
                    "level": ["graduate"]
                },
                "description": "Prestigious award for women doctoral/graduate students",
                "url": "https://www.peointernational.org/",
                "tags": ["women", "graduate", "prestigious"]
            },
            {
                "name": "National Society of Arts and Letters Scholarships",
                "amount": 3500,
                "deadline": "2026-02-28",
                "eligibility": {
                    "gender": ["any"],
                    "major": ["creative writing", "literature", "english"],
                    "gpa_min": 3.0,
                    "essay_required": True
                },
                "description": "For students excelling in creative arts and literature",
                "url": "https://www.nsalarts.org/",
                "tags": ["creative", "arts", "national"]
            }
        ]

def calculate_match_score(scholarship, profile):
    score = 0
    reasons = []

    # Gender match (30 points)
    if 'gender' in scholarship['eligibility']:
        if profile['gender'] in scholarship['eligibility']['gender'] or 'any' in scholarship['eligibility']['gender']:
            score += 30
            reasons.append("✓ Gender match")

    # Major match (40 points)
    if 'major' in scholarship['eligibility']:
        profile_major = profile['major'].lower()
        for eligible_major in scholarship['eligibility']['major']:
            if eligible_major in profile_major or profile_major in eligible_major:
                score += 40
                reasons.append(f"✓ Major match ({eligible_major})")
                break

    # GPA requirement (15 points)
    if 'gpa_min' in scholarship['eligibility']:
        required_gpa = scholarship['eligibility']['gpa_min']
        if profile['gpa'] >= required_gpa:
            score += 15
            reasons.append(f"✓ GPA qualifies ({profile['gpa']} >= {required_gpa})")
        else:
            reasons.append(f"⚠️ GPA below minimum ({profile['gpa']} < {required_gpa})")

    # Location match (bonus 10 points)
    if 'location' in scholarship['eligibility']:
        if any(loc in profile['location'] for loc in scholarship['eligibility']['location']):
            score += 10
            reasons.append("✓ Location match")
    else:
        score += 5

    # Age requirement
    if 'age_min' in scholarship['eligibility']:
        if profile['age'] >= scholarship['eligibility']['age_min']:
            reasons.append(f"✓ Age requirement met")
        else:
            score = max(0, score - 20)
            reasons.append(f"⚠️ Age requirement not met ({profile['age']} < {scholarship['eligibility']['age_min']})")

    # Calculate days until deadline
    deadline = datetime.strptime(scholarship['deadline'], "%Y-%m-%d")
    days_left = (deadline - datetime.now()).days

    if days_left < 0:
        score = 0
        reasons.append("❌ DEADLINE PASSED")
    elif days_left <= 14:
        reasons.append(f"🔥 URGENT: {days_left} days left")
    elif days_left <= 30:
        reasons.append(f"⏰ SOON: {days_left} days left")

    return score, reasons, days_left

# Main app logic
if search_button or 'matches' not in st.session_state:
    profile = {
        "name": name,
        "gender": gender,
        "major": major,
        "gpa": gpa,
        "location": location,
        "age": age,
        "interests": interests
    }

    scholarships = ScholarshipDatabase.get_scholarships()
    matches = []

    for scholarship in scholarships:
        score, reasons, days_left = calculate_match_score(scholarship, profile)

        if score >= min_score and days_left >= 0:
            matches.append({
                'scholarship': scholarship,
                'score': score,
                'reasons': reasons,
                'days_until_deadline': days_left
            })

    matches.sort(key=lambda x: (-x['score'], x['days_until_deadline']))
    st.session_state.matches = matches
    st.session_state.profile = profile

# Display results
if 'matches' in st.session_state:
    matches = st.session_state.matches

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Scholarships Found", len(matches))
    with col2:
        total_value = sum(m['scholarship']['amount'] for m in matches)
        st.metric("Total Value", f"${total_value:,}")
    with col3:
        urgent = len([m for m in matches if m['days_until_deadline'] <= 14])
        st.metric("Urgent (< 14 days)", urgent)
    with col4:
        avg_score = int(sum(m['score'] for m in matches) / len(matches)) if matches else 0
        st.metric("Avg Match Score", f"{avg_score}/100")

    st.markdown("---")

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_urgent = st.checkbox("Show only urgent deadlines (< 14 days)", value=False)
    with col2:
        sort_by = st.selectbox("Sort by", ["Match Score", "Deadline", "Amount"])

    # Apply filters
    filtered_matches = matches
    if filter_urgent:
        filtered_matches = [m for m in matches if m['days_until_deadline'] <= 14]

    if sort_by == "Deadline":
        filtered_matches.sort(key=lambda x: x['days_until_deadline'])
    elif sort_by == "Amount":
        filtered_matches.sort(key=lambda x: -x['scholarship']['amount'])

    # Display scholarships
    if filtered_matches:
        for i, match in enumerate(filtered_matches, 1):
            s = match['scholarship']
            days_left = match['days_until_deadline']

            # Urgency indicator
            if days_left <= 14:
                urgency_color = "🔴"
                urgency_text = "URGENT"
            elif days_left <= 30:
                urgency_color = "🟡"
                urgency_text = "SOON"
            else:
                urgency_color = "🟢"
                urgency_text = "UPCOMING"

            with st.expander(f"{urgency_color} **{s['name']}** - ${s['amount']:,} | Match: {match['score']}/100", expanded=(i<=3)):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Description:** {s['description']}")
                    st.markdown(f"**Deadline:** {s['deadline']} ({urgency_text} - {days_left} days left)")
                    st.markdown(f"**Award Amount:** ${s['amount']:,}")

                    st.markdown("**Match Reasons:**")
                    for reason in match['reasons']:
                        st.markdown(f"- {reason}")

                    if s['eligibility'].get('essay_required'):
                        st.info("📝 Essay required")
                    if s['eligibility'].get('portfolio_required'):
                        st.info("📁 Portfolio required")
                    if s['eligibility'].get('membership_required'):
                        st.info("👥 Membership required")

                with col2:
                    st.markdown(f"**Match Score**")
                    st.progress(match['score'] / 100)
                    st.markdown(f"### {match['score']}/100")

                    st.markdown("**Tags:**")
                    for tag in s['tags']:
                        st.markdown(f"`{tag}`")

                    st.link_button("Apply Now →", s['url'], use_container_width=True)

        # Export functionality
        st.markdown("---")
        st.subheader("📥 Export Results")

        # Prepare data for export
        export_data = []
        for i, match in enumerate(filtered_matches, 1):
            s = match['scholarship']
            export_data.append({
                'Rank': i,
                'Scholarship': s['name'],
                'Amount': f"${s['amount']:,}",
                'Deadline': s['deadline'],
                'Days Left': match['days_until_deadline'],
                'Match Score': f"{match['score']}/100",
                'URL': s['url'],
                'Description': s['description']
            })

        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)

        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name=f"scholarship_matches_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No scholarships match your current filters. Try adjusting your criteria.")
else:
    st.info("👈 Fill out your profile in the sidebar and click 'Search Scholarships' to get started!")

# Footer
st.markdown("---")
st.markdown("**💡 Tip:** Update your profile and search regularly for new opportunities!")
