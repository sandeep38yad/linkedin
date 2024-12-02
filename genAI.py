import google.generativeai as genai

genai.configure(api_key="AIzaSyALzwgvXDCG1Zo1zNPrQxZ2uobtF3Cxkro")

model = genai.GenerativeModel('gemini-pro')
# model = genai.GenerativeModel("text - davinci - 003")

def func(jd):
    response = model.generate_content(f"Analyze the given job description and give me just "
                                      f"one thing as output 1. Minimum experience required for this job in float type."
                                      f"If no information is given regarding experience in the job description"
                                      f"then provide 0 as output. If experience range is given then provide minimum as output. Job Description:{jd}")

    print(response.text)


jd = '''
Xceedance
Share
Show more options
Test Engineer 
Gurugram, Haryana, India · 1 week ago · Over 100 applicants
HybridMatches your job preferences, workplace type is Hybrid.  Full-time  Associate
Skills: Test Cases, Integration Testing, +2 more
See how you compare to over 100 other applicants. Reactivate Premium



Am I a good fit for this job?

How can I best position myself for this job?

Tell me more about Xceedance


Easy Apply

Save
Save Test Engineer  at Xceedance
Test Engineer
Xceedance · Gurugram, Haryana, India (Hybrid)

Easy Apply

Save
Save Test Engineer  at Xceedance
Show more options
About the job
Experience: 3 - 5 Years 

Job Location: Gurgaon / Noida / Pune / Bangalore

Job Description:

Strong understanding of P&C industry and solutions and hands on experience on Duck Creek from testing standpoint.

Must have technical knowledge of overall Duck Creek suite including Policy, Billing, Claims Insights.

Experience in integration testing of Duck Creek product with upstream and downstream systems.

Collaborate with technical staff to develop effective strategies and test plans

Good knowledge of complete STLC, must be good in requirement gathering and TC writing.

Develop, execute, and maintain comprehensive test plans, test scripts, and test cases.

Participates in the analysis of new requirements and uses cases to develop test approach and deliverables (test approach, scenarios, test conditions, test cases, test data, and expected results).

Must have E2E defect management experience.

Conduct post-release/ post-implementation testing.

Must have good analytical & communication skills.


Qualifications
2 skills match your profile. Stand out by adding other skills you have.
Requirements added by the job poster
1+ years of work experience with Property and Casualty Insurance
Skills added by the job poster
2 skills on your profile
Integration Testing and Test Cases
2 skills missing on your profile
Property and Casualty Insurance and Software Testing Life Cycle (STLC)
Add skills you have to your profile to stand out to the employer. Add skills

Show qualification details
Achieve your goals faster with Premium
Get exclusive access to applicant insights, see jobs where you’d be a top applicant and more




Tushar and millions of other members use Premium

Reactivate Premium
Cancel anytime, for any reason.

About the company
Xceedance company logo
Xceedance
145,370 followers

Follow
Insurance  1,001-5,000 employees  3,410 on LinkedIn
Xceedance provides strategic operations support, technology, and data services to drive efficiencies for insurance organizations worldwide. The company helps insurers launch products, implement intelligent technology, deploy advanced analytics, and achieve business process optimization. The company’s proficiency extends to underwriting, actuarial services, catastrophe modeling, and exposure management, policy services, claims, BI and reporting, finance and accounting, and application development.

Xceedance has offices in the U.S., the U.K., Poland, Australia, and India.
…
show more

Show more'''

func(jd)
