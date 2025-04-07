# Bussiness Context
CodePro is an EdTech startup that had a phenomenal seed A funding round. 
It used the money to increase its brand awareness. As the marketing spend increased, it got several leads from different sources. Although it had spent significant money on acquiring customers, it had to be profitable in the long run to sustain the business. 
The major cost that the company is incurring is the customer acquisition cost (CAC). 
Businesses want to reduce their customer acquisition costs in the long run.
# Root Cause Analysis of CAC
The reasons for the high customer acquisition cost are as follows:
Improper targeting, High competition and Inefficient conversion.
1) Improper targeting can be resolved by the marketing team. They can do so using better targeting strategies and using ad recommendations.
2) To resolve the issue of high competition, brand differentiation is required, which can be taken up by the product team.
3) To address inefficient conversion, the sales team must undergo upskilling and prioritise the leads generated.
4) The sales team must work with the data science team to figure out how to prioritise leads. The data science team must come up with lead scoring for all the leads generated.
# Objectives of Lead Scoring
1) Remove Junk by categorising leads on the basis of propensity to purchase
2) Gain insights to streamline lead conversion and address improper targeting
# Understanding the Data
To classify any lead, we will require two types of information about it:
1) Origin of the lead: To better predict the likelihood of a lead purchasing a course, we need some information on the origin of the lead. The columns from ‘city_mapped’ to ‘reffered_leads’ contain the information about the origin of the lead.
2) Interaction of the lead with the website/platform: We also require information about how the lead interacted with the platform. The columns from ‘1_on_1_industry_mentorship’ to ‘whatsapp_chat_click’ store the information about a lead’s interaction with the platform.
# Origin of a Lead
1) created_data: This is the timestamp identifying when a lead was created.
2) city_mapped: This is the city where a lead was generated.
3) first_platform_c: This is the place that leads users to the source - mobile web, desktop web, Android app, etc.
4) first_utm_medium_c: Mediums are broad buckets of categories that describe the type of traffic being driven to your website. For example, ‘organic’ is a medium because it encompasses traffic coming from search engines such as Google. ‘Referral’, ‘social’ and ‘paid’ are other examples of mediums.
5) first_utm_source_c: The source is where your website’s traffic comes from (individual websites, Google, Facebook, etc.). For example, think of a journey - the source would be where you came from, and the medium would be the mode of transport.
6) total_leads_dropped: This refers to the count of leads accessed by the user. For example, a user might browse through multiple Python courses while looking for the best course based on their requirements.
7) Referred_lead: This indicates whether a lead was referred or not.
8) interaction type columns: These capture the type of interaction a user had with the CodePro website. For example, the user might look at payment options, syllabus, placement records, etc.
9) App_complete_flag: this is the column we are trying to predict. We are trying to understand whether a user will fill the application or not based on the information in the previous columns.
# Category	Tools & Frameworks
1) Programming Language	Python 3.8+
2) Machine Learning	LightGBM, PyCaret, scikit-learn
3) Data Handling	pandas, NumPy, sqlite3
4) Experiment Tracking	MLflow
5) Pipeline Orchestration	Apache Airflow
6) Model Evaluation	scikit-learn metrics, matplotlib (ROC, AUC, accuracy, F1 score, etc.)
7) Testing & Validation	Python unit tests with SQLite-based test case comparisons
8) Version Control	Git, GitHub
9) Environment Management	requirements.txt, virtualenv / conda
