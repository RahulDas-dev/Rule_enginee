from pyjsonata import jsonata


# columns
col1: --
c

# Rules

1. Score < 650 THEN Reject: 
Rule: If the credit score is less than 650, the applicant is rejected.
Supporting Data: In the XML report, the credit score is 725, which is greater than 650. Therefore, this rule does not trigger a rejection.
2. More than 2 PAN IDs THEN Reject
Rule: If there are more than two PAN IDs, the applicant is rejected.
Supporting Data: The XML report contains two PAN IDs (AZJPA1698N and AVNPJ6436G). Since there are exactly 2 PAN IDs, this rule does not trigger a rejection.
C. TotalInquiries > 3 THEN Reject
Rule: If the number of total inquiries exceeds 3, the applicant is rejected.
Supporting Data: In the XML report, the total number of inquiries is 0. Therefore, this rule does not trigger a rejection.
D. Loan Accounts (Excluding Credit Cards)
D.a SuitFiledStatus = Yes THEN Reject
Rule: If any loan account (except credit cards) has a "Suit Filed" status as "Yes", the applicant is rejected.
Supporting Data: None of the loan accounts have the SuitFiledStatus set to "Yes". Therefore, this rule does not trigger a rejection.
D.b WriteOffAmount > 0 THEN Reject
Rule: If any loan account (excluding credit cards) has a WriteOffAmount greater than 0, the applicant is rejected.
Supporting Data: No loan accounts have a WriteOffAmount greater than 0. Therefore, this rule does not trigger a rejection.
D.c PastDueAmount > 1,500 and DateReported < 12 months THEN Reject
Rule: If any loan account has a PastDueAmount greater than 1,500, and DateReported is within the last 12 months and the PaymentStatus in any of the past 12 months is one of the listed delinquency statuses, the applicant is rejected.
Supporting Data: There is one account with a PastDueAmount of 4,465 (Consumer Loan). The DateReported is 2024-08-28, which is within the last 12 months. However, none of the PaymentStatus values in the past 12 months indicate delinquency. Therefore, this rule does not trigger a rejection.
D.d AccountStatus in {WDF, SUB, DBT, etc.} THEN Reject
Rule: If any loan account has a status in the listed statuses, the applicant is rejected.
Supporting Data: None of the loan accounts have a status in the listed statuses. Therefore, this rule does not trigger a rejection.
D.e PastDueAmount > 1,500 and DateReported > 12 months THEN Reject
Rule: If any loan account has a PastDueAmount greater than 1,500, DateReported is more than 12 months ago, and PaymentStatus in any of the past 6 months indicates delinquency, the applicant is rejected.
Supporting Data: No accounts with a PastDueAmount greater than 1,500 have a DateReported more than 12 months ago. Therefore, this rule does not trigger a rejection.
E. Credit Card PastDueAmount > 5,000 THEN Reject
Rule: If any credit card account has a PastDueAmount greater than 5,000, the applicant is rejected.
Supporting Data: The credit card account in the report has a PastDueAmount of 0. Therefore, this rule does not trigger a rejection.
Final Result:
Decision: Not Rejected
Reasoning: None of the rules trigger a rejection based on the provided XML report data.
Would you like further details on how to adjust these rules or integrate them into your system?