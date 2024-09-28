'''
1. Score < 650 THEN Reject
    Rule: If the credit score is less than 650, the applicant is rejected.
2. More than 2 PAN IDs THEN Reject
    Rule: If there are more than two PAN IDs, the applicant is rejected.
3. TotalInquiries > 3 THEN Reject
    Rule: If the number of total inquiries exceeds 3, the applicant is rejected.
4. if any Account of AccountType Excluding Credit Cards
    a. SuitFiledStatus = Yes THEN Reject
    Rule: If any Account has a 'Suit Filed' status as 'Yes', the applicant is rejected.
    b. WriteOffAmount > 0 THEN Reject
    Rule: If any Account has a WriteOffAmount greater than 0, the applicant is rejected.
    c. PastDueAmount > 1,500 and DateReported < 12 months THEN Reject
    Rule: If any Account has a PastDueAmount greater than 1,500, and DateReported is within the last 12 months and the PaymentStatus in any of the past 12 months is one of the listed delinquency statuses, the applicant is rejected.
    d. AccountStatus in {WDF, SUB, DBT, etc.} THEN Reject
    Rule: If any account has a status in the listed statuses, the applicant is rejected.
    e. PastDueAmount > 1,500 and DateReported > 12 months THEN Reject
    Rule: If any Account has a PastDueAmount greater than 1,500, DateReported is more than 12 months ago, and PaymentStatus in any of the past 6 months indicates delinquency, the applicant is rejected.
5. if any Account of AccountType = Credit Card  and PastDueAmount > 5,000 THEN Reject
    Rule: If any credit card account has a PastDueAmount greater than 5,000, the applicant is rejected.
'''

{
  "version": "1.0",
  "rules_str": "\n1. Score < 650 THEN Reject\n    Rule: If the credit score is less than 650, the applicant is rejected.\n2. More than 2 PAN IDs THEN Reject\n    Rule: If there are more than two PAN IDs, the applicant is rejected.\n3. TotalInquiries > 3 THEN Reject\n    Rule: If the number of total inquiries exceeds 3, the applicant is rejected.\n4. if any Account of AccountType Excluding Credit Cards\n    a. SuitFiledStatus = Yes THEN Reject\n    Rule: If any Account has a 'Suit Filed' status as 'Yes', the applicant is rejected.\n    b. WriteOffAmount > 0 THEN Reject\n    Rule: If any Account has a WriteOffAmount greater than 0, the applicant is rejected.\n    c. PastDueAmount > 1,500 and DateReported < 12 months THEN Reject\n    Rule: If any Account has a PastDueAmount greater than 1,500, and DateReported is within the last 12 months and the PaymentStatus in any of the past 12 months is one of the listed delinquency statuses, the applicant is rejected.\n    d. AccountStatus in {WDF, SUB, DBT, etc.} THEN Reject\n    Rule: If any account has a status in the listed statuses, the applicant is rejected.\n    e. PastDueAmount > 1,500 and DateReported > 12 months THEN Reject\n    Rule: If any Account has a PastDueAmount greater than 1,500, DateReported is more than 12 months ago, and PaymentStatus in any of the past 6 months indicates delinquency, the applicant is rejected.\n5. if any Account of AccountType = Credit Card  and PastDueAmount > 5,000 THEN Reject\n    Rule: If any credit card account has a PastDueAmount greater than 5,000, the applicant is rejected.\n"
}
