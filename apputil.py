import pandas as pd
import plotly.express as px

# Exercise 1 Functions
def survival_demographics():
    """Analyze survival by class, sex, and age group."""
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    # Create age categories
    bins = [0, 12, 19, 59, 100]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)
    
    # Group by class, sex, age_group
    grouped = df.groupby(['Pclass', 'Sex', 'age_group'], dropna=False)
    
    result = grouped.agg(
        n_passengers=('Survived', 'count'),
        n_survivors=('Survived', 'sum')
    ).reset_index()
    
    result['survival_rate'] = result['n_survivors'] / result['n_passengers']
    
    result = result.sort_values(['Pclass', 'Sex', 'age_group'])
    
    return result

def visualize_demographic():
    """Visualize survival patterns by class, sex, and age group."""
    df = survival_demographics()
    
    # Filter out rows with missing age_group for cleaner visualization
    df_clean = df.dropna(subset=['age_group'])
    
    fig = px.bar(
        df_clean,
        x='age_group',
        y='survival_rate',
        color='Sex',
        facet_col='Pclass',
        barmode='group',
        title='Survival Rates by Class, Sex, and Age Group',
        labels={
            'survival_rate': 'Survival Rate',
            'age_group': 'Age Group',
            'Pclass': 'Passenger Class'
        },
        color_discrete_map={'male': '#1f77b4', 'female': '#ff7f0e'}
    )
    
    fig.update_yaxes(range=[0, 1])
    fig.update_layout(showlegend=True)
    
    return fig

# Exercise 2 Functions
def family_groups():
    """Analyze family size, class, and fare."""
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    # Create family_size column
    df['family_size'] = df['SibSp'] + df['Parch'] + 1
    
    # Group by family_size and Pclass
    result = df.groupby(['family_size', 'Pclass']).agg(
        n_passengers=('Fare', 'count'),
        avg_fare=('Fare', 'mean'),
        min_fare=('Fare', 'min'),
        max_fare=('Fare', 'max')
    ).reset_index()
    
    result = result.sort_values(['Pclass', 'family_size'])
    
    return result

def last_names():
    """Extract and count last names."""
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    df['LastName'] = df['Name'].str.split(',').str[0]
    
    return df['LastName'].value_counts()

def visualize_families():
    """Visualize relationship between family size and fare by class."""
    df = family_groups()
    
    fig = px.scatter(
        df,
        x='family_size',
        y='avg_fare',
        color='Pclass',
        size='n_passengers',
        title='Average Fare by Family Size and Passenger Class',
        labels={
            'family_size': 'Family Size',
            'avg_fare': 'Average Fare ($)',
            'Pclass': 'Class',
            'n_passengers': 'Number of Passengers'
        },
        color_continuous_scale='Viridis'
    )
    
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    
    return fig

# Bonus Functions
def determine_age_division():
    """Add older_passenger column based on class median age."""
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    df['older_passenger'] = df.groupby('Pclass')['Age'].transform(
        lambda x: df.loc[x.index, 'Age'] > x.median()
    )
    
    return df

def visualize_age_division():
    """Visualize age division and survival patterns."""
    df = determine_age_division()
    
    # Remove rows with missing age data
    df_clean = df.dropna(subset=['Age', 'older_passenger'])
    
    # Group by class, age division, and survival
    summary = df_clean.groupby(['Pclass', 'older_passenger', 'Survived']).size().reset_index(name='count')
    
    fig = px.bar(
        summary,
        x='Pclass',
        y='count',
        color='Survived',
        facet_col='older_passenger',
        barmode='group',
        title='Survival Count by Class and Age Division (Above/Below Class Median)',
        labels={
            'Pclass': 'Passenger Class',
            'count': 'Number of Passengers',
            'Survived': 'Survived',
            'older_passenger': 'Older than Class Median'
        },
        color_discrete_map={0: '#d62728', 1: '#2ca02c'}
    )
    
    return fig