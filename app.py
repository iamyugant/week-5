import streamlit as st
from apputil import *

st.title("🚢 Titanic Survival Analysis")

# Exercise 1
st.header("Exercise 1: Survival Demographics")
st.write("**Question:** How did survival rates vary across different age groups, and did the 'women and children first' protocol apply equally across all passenger classes?")

st.subheader("Survival Data by Demographics")
st.dataframe(survival_demographics())

st.subheader("Visualization")
st.plotly_chart(visualize_demographic(), use_container_width=True)

st.markdown("---")

# Exercise 2
st.header("Exercise 2: Family Groups and Fare Analysis")
st.write("**Question:** Did larger families pay proportionally higher fares, or were there economies of scale in ticket pricing across different passenger classes?")

st.subheader("Family Size and Fare Data")
st.dataframe(family_groups())

st.subheader("Last Name Analysis")
st.write("Top 10 most common last names:")
st.dataframe(last_names().head(10))

st.write("""
**Findings:** The last name counts align with the family size data from the table above. 
Families like Andersson (9 passengers) and Sage (11 passengers) represent the largest groups. 
These large families predominantly traveled in 3rd class, which explains the lower average 
fares per person in that class for larger family sizes. The data confirms that many passengers 
shared family groups, with some last names appearing 7-11 times in the dataset.
""")

st.subheader("Visualization")
st.plotly_chart(visualize_families(), use_container_width=True)

st.markdown("---")

# Bonus
st.header("Bonus: Age Division Analysis")
st.write("**Question:** Within each passenger class, did being older or younger than the median age for that class affect survival chances?")

st.subheader("Age Division Data")
st.dataframe(determine_age_division()[['Pclass', 'Age', 'older_passenger', 'Survived']].head(20))

st.subheader("Visualization")
st.plotly_chart(visualize_age_division(), use_container_width=True)

st.write("""
**Analysis:** The visualization shows that age relative to class median played a role in survival. 
Younger passengers (below class median) in 1st and 2nd class had better survival rates, 
supporting the "women and children first" protocol. However, in 3rd class, the pattern 
is less pronounced, suggesting that class itself was a stronger predictor of survival than 
age division within that class.
""")