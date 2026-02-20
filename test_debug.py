import pandas as pd
from apputil import survival_demographics, family_groups, last_names, determine_age_division

print("=" * 60)
print("TESTING EXERCISE 1: survival_demographics()")
print("=" * 60)

df = survival_demographics()

# Test 1: Check total rows (should be 24: 3 classes × 2 sexes × 4 age groups)
print(f"\n✓ Total rows: {len(df)} (expected: 24)")
assert len(df) == 24, "Should have 24 rows"

# Test 2: Check column names
expected_cols = ['Pclass', 'Sex', 'age_group', 'n_passengers', 'n_survivors', 'survival_rate']
print(f"✓ Columns: {df.columns.tolist()}")
assert list(df.columns) == expected_cols, f"Columns should be {expected_cols}"

# Test 3: Check age_group is categorical
print(f"✓ age_group dtype: {df['age_group'].dtype} (should be 'category')")
assert df['age_group'].dtype.name == 'category', "age_group should be categorical"

# Test 4: Check the specific problematic group (Pclass=2, Sex='female', age_group='Senior')
problem_group = df[(df['Pclass'] == 2) & (df['Sex'] == 'female') & (df['age_group'] == 'Senior')]
print(f"\n✓ Second class, female, Senior group:")
print(problem_group)
assert len(problem_group) == 1, "Should find exactly 1 row for this group"
assert problem_group.iloc[0]['n_passengers'] == 0, "Should have 0 passengers"
assert problem_group.iloc[0]['n_survivors'] == 0, "Should have 0 survivors"
assert problem_group.iloc[0]['survival_rate'] == 0.0, "Should have 0.0 survival rate"

# Test 5: Check a real group with data (Pclass=1, Sex='female', age_group='Adult')
real_group = df[(df['Pclass'] == 1) & (df['Sex'] == 'female') & (df['age_group'] == 'Adult')]
print(f"\n✓ First class, female, Adult group:")
print(real_group)
assert len(real_group) == 1, "Should find exactly 1 row"
assert real_group.iloc[0]['n_passengers'] > 0, "Should have passengers"

# Test 6: Check all groups with 0 passengers
empty_groups = df[df['n_passengers'] == 0]
print(f"\n✓ Groups with 0 passengers: {len(empty_groups)}")
print(empty_groups[['Pclass', 'Sex', 'age_group', 'n_passengers']])

print("\n" + "=" * 60)
print("TESTING EXERCISE 2: family_groups() and last_names()")
print("=" * 60)

# Test family_groups
fg = family_groups()
print(f"\n✓ family_groups() shape: {fg.shape}")
expected_fg_cols = ['family_size', 'Pclass', 'n_passengers', 'avg_fare', 'min_fare', 'max_fare']
print(f"✓ Columns: {fg.columns.tolist()}")
assert list(fg.columns) == expected_fg_cols, f"Columns should be {expected_fg_cols}"

# Test last_names
ln = last_names()
print(f"\n✓ last_names() type: {type(ln)}")
print(f"✓ Top 5 last names:\n{ln.head()}")
assert isinstance(ln, pd.Series), "Should return a pandas Series"
assert ln.index.name is None or ln.index.name == 'LastName', "Index should be last names"

print("\n" + "=" * 60)
print("TESTING BONUS: determine_age_division()")
print("=" * 60)

bonus_df = determine_age_division()

# Test 1: Check column exists
print(f"\n✓ Columns include: {bonus_df.columns.tolist()}")
assert 'older_passenger' in bonus_df.columns, "Should have 'older_passenger' column"

# Test 2: Check dtype
print(f"✓ older_passenger dtype: {bonus_df['older_passenger'].dtype}")
print(f"  (acceptable types: bool, boolean, object with True/False/NaN)")

# Test 3: Check values
value_counts = bonus_df['older_passenger'].value_counts(dropna=False)
print(f"\n✓ Value counts:\n{value_counts}")

# Test 4: Check sample values
print(f"\n✓ Sample values (first 10 with Age):")
sample = bonus_df[['Pclass', 'Age', 'older_passenger']].head(10)
print(sample)

# Test 5: Check that NaN ages result in NaN older_passenger
nan_ages = bonus_df[bonus_df['Age'].isna()]
print(f"\n✓ Passengers with NaN age: {len(nan_ages)}")
print(f"  older_passenger values for NaN ages (should all be NaN/None):")
print(nan_ages['older_passenger'].value_counts(dropna=False).head())

# Test 6: Verify logic - check if values make sense for one class
class_1 = bonus_df[bonus_df['Pclass'] == 1].copy()
class_1_median = class_1['Age'].median()
print(f"\n✓ Class 1 median age: {class_1_median}")

# Check a few specific cases
test_cases = class_1[class_1['Age'].notna()].head(5)
for idx, row in test_cases.iterrows():
    expected = row['Age'] > class_1_median
    actual = row['older_passenger']
    match = "✓" if expected == actual else "✗"
    print(f"  {match} Age {row['Age']}: older_passenger={actual} (expected {expected})")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED!")
print("=" * 60)
print("\nIf you see any ✗ or assertion errors above, fix those issues.")
print("If all tests pass, your code should work on Gradescope!")