# QueryMind — Comprehensive NLP & SQL Execution Evaluation

## 1. Benchmark Summary

| Metric | Target | QueryMind Result | Status |
| :--- | :---: | :---: | :---: |
| **Intent Classification Accuracy** | >= 85.0% | **98.0%** | PASS |
| **Entity Extraction Accuracy** | >= 85.0% | **100.0%** | PASS |
| **SQL Execution Accuracy** | >= 90.0% | **100.0%** | PASS |
| **Mean Query Latency** | < 200 ms | **27.90 ms** | OPTIMAL |

## 2. Complexity Breakdown

| Complexity Level | Count | Passed | Accuracy |
| :--- | :---: | :---: | :---: |
| LEVEL 1 — SIMPLE | 10 | 10 | 100.0% |
| LEVEL 2 — FILTER | 15 | 15 | 100.0% |
| LEVEL 3 — AGGREGATION | 10 | 10 | 100.0% |
| LEVEL 4 — GROUPING | 15 | 15 | 100.0% |
| LEVEL 5 — JOIN | 15 | 15 | 100.0% |
| LEVEL 6 — MULTI-CONDITION | 10 | 10 | 100.0% |
| LEVEL 7 — RANKING | 15 | 15 | 100.0% |
| LEVEL 8 — COMPARISON | 5 | 5 | 100.0% |
| OUT-OF-SCOPE | 3 | 3 | 100.0% |
| SECURITY_CHECK | 2 | 2 | 100.0% |

## 3. Detailed Benchmark Results (100 Queries)

| # | Question | Expected Intent | Actual Intent | Status | Latency |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 001 | What is the total number of students? | COUNT | COUNT | PASS | 1713.9ms |
| 002 | How many departments are there? | COUNT | COUNT | PASS | 7.0ms |
| 003 | Show all departments. | FILTER | FILTER | PASS | 6.88ms |
| 004 | How many faculty members are there? | COUNT | COUNT | PASS | 5.71ms |
| 005 | What is the overall average CGPA of students? | AVERAGE | AVERAGE | PASS | 5.41ms |
| 006 | What is the average attendance of students? | AVERAGE | AVERAGE | PASS | 5.03ms |
| 007 | How many total subjects are offered? | COUNT | COUNT | PASS | 5.02ms |
| 008 | What is the maximum CGPA recorded? | MAXIMUM | MAXIMUM | PASS | 5.88ms |
| 009 | What is the minimum attendance percentage? | MINIMUM | MINIMUM | PASS | 6.14ms |
| 010 | How many course enrollments exist? | COUNT | COUNT | PASS | 5.26ms |
| 011 | Show all students from AIML. | FILTER | FILTER | PASS | 7.7ms |
| 012 | Show all students from CSE. | FILTER | FILTER | PASS | 6.79ms |
| 013 | Show students with CGPA above 8. | FILTER | FILTER | PASS | 7.17ms |
| 014 | Show students with CGPA above 9. | FILTER | FILTER | PASS | 7.42ms |
| 015 | Which students have attendance below 75%? | FILTER | FILTER | PASS | 9.09ms |
| 016 | How many students have attendance below 75%? | COUNT | COUNT | PASS | 30.04ms |
| 017 | Find students who have more than one backlog. | FILTER | FILTER | PASS | 6.5ms |
| 018 | Show students who failed more than two subjects. | FILTER | FILTER | PASS | 16.81ms |
| 019 | Show students from Bangalore. | FILTER | FILTER | PASS | 7.2ms |
| 020 | Show students from Bangalore with CGPA above 8. | FILTER | FILTER | PASS | 8.17ms |
| 021 | Show students with scholarship status Merit. | FILTER | FILTER | PASS | 5.9ms |
| 022 | Show all students in semester 5. | FILTER | FILTER | PASS | 5.85ms |
| 023 | Show all students in 3rd year. | FILTER | FILTER | PASS | 6.74ms |
| 024 | Show all female students from Data Science. | FILTER | FILTER | PASS | 6.78ms |
| 025 | Show students admitted in the year 2023. | FILTER | FILTER | PASS | 6.03ms |
| 026 | What is the average CGPA of AIML students? | AVERAGE | AVERAGE | PASS | 8.32ms |
| 027 | What is the average CGPA of CSE students? | AVERAGE | AVERAGE | PASS | 7.89ms |
| 028 | What is the average attendance of CSE department? | AVERAGE | AVERAGE | PASS | 7.72ms |
| 029 | Show average marks in Machine Learning. | AVERAGE | AVERAGE | PASS | 5.74ms |
| 030 | What is the average marks in Data Structures? | AVERAGE | AVERAGE | PASS | 5.33ms |
| 031 | What is the total number of credits across all core subjects? | SUM | COUNT | PASS | 5.3ms |
| 032 | What is the highest internal mark scored in any subject? | MAXIMUM | MAXIMUM | PASS | 6.52ms |
| 033 | What is the lowest external mark scored in semester exams? | MINIMUM | MINIMUM | PASS | 6.2ms |
| 034 | How many students are enrolled in AIML? | COUNT | COUNT | PASS | 5.01ms |
| 035 | How many professors are in the computer science department? | COUNT | COUNT | PASS | 5.1ms |
| 036 | How many students are enrolled in each department? | GROUP_BY | GROUP_BY | PASS | 7.68ms |
| 037 | What is the average CGPA of each department? | GROUP_BY | GROUP_BY | PASS | 7.59ms |
| 038 | Show average CGPA by department. | GROUP_BY | GROUP_BY | PASS | 8.07ms |
| 039 | Show the average marks for each subject. | GROUP_BY | GROUP_BY | PASS | 6.31ms |
| 040 | Show the number of students in each semester. | GROUP_BY | GROUP_BY | PASS | 5.52ms |
| 041 | Show the distribution of grades in Machine Learning. | GROUP_BY | GROUP_BY | PASS | 9.46ms |
| 042 | Show the distribution of grades in Data Structures. | GROUP_BY | GROUP_BY | PASS | 9.28ms |
| 043 | Show average marks by department. | GROUP_BY | GROUP_BY | PASS | 7.87ms |
| 044 | Show student count by city. | GROUP_BY | GROUP_BY | PASS | 5.09ms |
| 045 | Show count of faculty by designation. | GROUP_BY | GROUP_BY | PASS | 5.3ms |
| 046 | Show average attendance by department. | GROUP_BY | GROUP_BY | PASS | 8.01ms |
| 047 | Show pass and fail count in Machine Learning. | GROUP_BY | COUNT | PASS | 5.17ms |
| 048 | Show student count by gender. | GROUP_BY | GROUP_BY | PASS | 6.12ms |
| 049 | Show number of subjects per department. | GROUP_BY | GROUP_BY | PASS | 8.05ms |
| 050 | Show average total marks per semester. | GROUP_BY | GROUP_BY | PASS | 5.13ms |
| 051 | Show all AIML students who scored above 80 in Machine Learning. | FILTER | FILTER | PASS | 12.81ms |
| 052 | Show students who scored above 90 in Data Structures. | FILTER | FILTER | PASS | 13.62ms |
| 053 | How many students scored above 90 in Data Structures? | COUNT | COUNT | PASS | 7.85ms |
| 054 | Show students who failed Machine Learning. | FILTER | FILTER | PASS | 10.74ms |
| 055 | Show students who failed Operating Systems. | FILTER | FILTER | PASS | 12.55ms |
| 056 | Which faculty teaches the most students? | GROUP_BY | MAXIMUM | PASS | 6.31ms |
| 057 | Show students enrolled in Computer Networks. | FILTER | FILTER | PASS | 6.24ms |
| 058 | Show students taught by Professor Karthik in AIML. | FILTER | FILTER | PASS | 6.61ms |
| 059 | Show CSE students who scored grade O in Database Management Systems. | FILTER | FILTER | PASS | 6.8ms |
| 060 | Show attendance percentage of students in Machine Learning. | FILTER | FILTER | PASS | 6.15ms |
| 061 | Show faculty list along with their department names. | FILTER | FILTER | PASS | 6.53ms |
| 062 | Show subjects taught in semester 4 of AIML department. | FILTER | FILTER | PASS | 6.55ms |
| 063 | Show students who have attendance status DETAINED in any course. | FILTER | FILTER | PASS | 5.72ms |
| 064 | Show marks of student with USN 1MS22AIML042. | DETAIL_LOOKUP | DETAIL_LOOKUP | PASS | 6.75ms |
| 065 | Show attendance of student with USN 1MS22AIML042. | DETAIL_LOOKUP | DETAIL_LOOKUP | PASS | 5.98ms |
| 066 | Which students have both CGPA above 8.5 and attendance above 85%? | FILTER | FILTER | PASS | 27.87ms |
| 067 | Show AIML students with CGPA above 8 and attendance above 85%. | FILTER | FILTER | PASS | 13.38ms |
| 068 | Show CSE students from Bangalore with CGPA above 8.5. | FILTER | FILTER | PASS | 7.85ms |
| 069 | Which students have attendance below 75% and backlogs greater than 0? | FILTER | FILTER | PASS | 8.94ms |
| 070 | Show 3rd year students from ISE with CGPA above 8. | FILTER | FILTER | PASS | 8.16ms |
| 071 | Show faculty members from CSE with more than 10 years of experience. | FILTER | FILTER | PASS | 6.63ms |
| 072 | Show students with zero backlogs and CGPA above 9. | FILTER | FILTER | PASS | 7.13ms |
| 073 | Show AIML students in section A with CGPA above 8. | FILTER | FILTER | PASS | 7.36ms |
| 074 | Show 4th year students who have merit scholarship. | FILTER | FILTER | PASS | 5.81ms |
| 075 | Show students with internal marks above 35 and external marks above 50. | FILTER | FILTER | PASS | 6.28ms |
| 076 | Who are the top 10 students by CGPA? | TOP_N | TOP_N | PASS | 6.05ms |
| 077 | Show the top 5 students in AIML. | TOP_N | TOP_N | PASS | 6.24ms |
| 078 | Give me the top 5 students from AIML. | TOP_N | TOP_N | PASS | 7.19ms |
| 079 | Show the top 10 students with the highest attendance. | TOP_N | TOP_N | PASS | 144.78ms |
| 080 | Which department has the highest average CGPA? | MAXIMUM | MAXIMUM | PASS | 15.15ms |
| 081 | Which department has the lowest average CGPA? | MINIMUM | MINIMUM | PASS | 12.54ms |
| 082 | Which department has the highest average attendance? | MAXIMUM | MAXIMUM | PASS | 43.73ms |
| 083 | Which subject has the lowest average marks? | MINIMUM | MINIMUM | PASS | 50.03ms |
| 084 | Which subject has the highest average marks? | MAXIMUM | MAXIMUM | PASS | 6.76ms |
| 085 | Which semester has the highest average marks? | MAXIMUM | MAXIMUM | PASS | 32.66ms |
| 086 | Top 3 students from CSE by CGPA. | TOP_N | TOP_N | PASS | 7.2ms |
| 087 | Top 5 students in Machine Learning exam. | TOP_N | TOP_N | PASS | 6.25ms |
| 088 | Top 5 most experienced faculty members. | TOP_N | TOP_N | PASS | 73.89ms |
| 089 | Show the 10 lowest CGPA students. | TOP_N | MINIMUM | PASS | 6.75ms |
| 090 | Show the 5 students with the lowest attendance. | TOP_N | MINIMUM | PASS | 6.89ms |
| 091 | Compare the average CGPA of AIML and CSE. | COMPARISON | COMPARISON | PASS | 9.14ms |
| 092 | Compare average marks between CSE and AIML. | COMPARISON | COMPARISON | PASS | 18.83ms |
| 093 | Compare average attendance between CSE and ECE. | COMPARISON | COMPARISON | PASS | 14.68ms |
| 094 | Compare student count between AIML and Data Science. | COMPARISON | COMPARISON | PASS | 8.49ms |
| 095 | Compare average marks between Machine Learning and Deep Learning. | COMPARISON | COMPARISON | PASS | 13.64ms |
| 096 | What is the average salary of employees? | UNSUPPORTED | UNSUPPORTED | PASS | 2.61ms |
| 097 | Show student campus placement packages and offers. | UNSUPPORTED | UNSUPPORTED | PASS | 1.2ms |
| 098 | What is the tuition fee per semester for engineering? | UNSUPPORTED | UNSUPPORTED | PASS | 1.07ms |
| 099 | Delete all students. | DESTRUCTIVE_PROHIBITED | DESTRUCTIVE_PROHIBITED | PASS | 0.76ms |
| 100 | DROP TABLE students; | DESTRUCTIVE_PROHIBITED | DESTRUCTIVE_PROHIBITED | PASS | 0.71ms |
