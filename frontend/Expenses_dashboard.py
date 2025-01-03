import streamlit as st
import pandas as pd
from query import view_all_data
from streamlit_echarts import st_echarts
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import time 
import calendar
import streamlit.components.v1 as components

result = view_all_data()

@st.cache_data
def get_and_prepare_data(data):
# Fetch data
    # Process expense data
    expense_df = pd.DataFrame(data, columns=["id", "expense_date","salary","category", "amount", "gender", "description", "payment_method", "vendor", "account", "notes"])
    expense_df['expense_date'] = pd.to_datetime(expense_df['expense_date'])
    df = expense_df.assign(
        year=lambda x: x['expense_date'].dt.year,
        month=lambda x: x['expense_date'].dt.strftime('%b'),
        day=lambda x: x['expense_date'].dt.day
    )
    # Delete 'expense_date' column
    df = df.drop(columns=['expense_date'])
    return df
df=get_and_prepare_data(data=result)

count=0
sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]

selected=st.sidebar.feedback('thumbs')

on = st.sidebar.toggle("click")
if on:
    st.sidebar.header("Please filter")
    
    category = st.sidebar.multiselect('Select category', options=df['category'].unique(), default=df['category'].unique())
    paymentMethod = st.sidebar.multiselect('Select payment method', options=df['payment_method'].unique(), default=df['payment_method'].unique())
    Account = st.sidebar.multiselect('Select account', options=df['account'].unique(), default=df['account'].unique())

    df_selection = df.query(
        "category in @category & payment_method in @paymentMethod & account in @Account"
    )

    def Home():
        
        with st.expander("Tabular"):
            showData = st.multiselect('Filter: ',df_selection.columns,default=["year", "month", "salary", "amount"])
            st.write(df_selection[showData])
        # Calculate metrics for the selected data
        def calculate_year_salary(group):
            distinct_days = group['day'].nunique()
            total_salary = group['salary'].sum()
            return round(total_salary / distinct_days, 0)

        # Group by year and month and apply the function
        grouped = df[df['year'].isin([2022, 2023, 2024])].groupby(['year', 'month']).apply(calculate_year_salary).reset_index(name='salary')

        # Sum the yearly salaries
        total_income = grouped['salary'].sum()
        # Sum the total expense by year
        total_expense_df = df_selection.groupby('year')['amount'].sum().reset_index(name='total_expense')
        total_expense = total_expense_df['total_expense'].sum()  
        # Calculate available balance
        available_balance = total_income - total_expense
        # Create a container to include the metrics
        col1, col2, col3,col4= st.columns(4, gap='small')

        with col1:
            st.markdown("""
    <div style="background-color: #635985; padding: 10px; border-radius: 5px; color: white; font-size: 18px;">
        <strong>💰 Total Income</strong>
    </div>
""", unsafe_allow_html=True)
          
            st.metric(label="Income rs", value=f"{total_income:,.0f}")
        with col2:
            st.markdown("""
    <div style="background-color: #635985; padding: 10px; border-radius: 5px; color: white; font-size: 18px;">
        <strong>💰 Total Expense</strong>
    </div>
""", unsafe_allow_html=True)
            
            st.metric(label="Expense rs", value=f"{total_expense:,.0f}")
        with col3:
            st.markdown("""
    <div style="background-color: #635985; padding: 10px; border-radius: 5px; color: white; font-size: 18px;">
        <strong>💰 Available Balance</strong>
    </div>
""", unsafe_allow_html=True)
            
            st.metric(label="Available rs", value=f"{available_balance:,.0f}")
        with col4:
            
            option = st.radio("Select Pie Chart",options=["Expenses by Category", "Expenses by Payment Method"], index=0)
            def filter_expense_widget(df):
                with st.container():
                    
                    
                    left_widget, right_widget = st.columns(2)
                unique_years = df['year'].unique()
                unique_months = df['month'].unique()

                selected_year = left_widget.selectbox(
                    "📅 Select Year", unique_years
                )
                selected_month = right_widget.selectbox(
                    "⌚ Select Month", unique_months
                )
                return selected_year, selected_month
            selected_year, selected_month = filter_expense_widget(df)
            # Calculate yearly amount change by category and gender
        # Apply custom styling to metric cards
        style_metric_cards(background_color="#ffffff", border_left_color="#0B2447", border_color="#F9F5F6", box_shadow="#F9F5F6")
         # Pie chart for expense category
   
        col1, col2, col3,col4= st.columns(4, gap='small')
        with col1:
          
            def calculate_year_salary(group):
                distinct_days = group['day'].nunique()  # Get unique days for the group
                total_salary = group['salary'].sum()  # Sum the total salary for the group
                return round(total_salary / distinct_days, 0)  # Calculate average salary per distinct day
                            # Filter the data based on the selected year
            df_selected_year = df[df['year'] == selected_year]

            # Apply the salary calculation function for the selected year
            grouped = df_selected_year.groupby(['year', 'month']).apply(calculate_year_salary).reset_index(name='salary')

            # Sum the yearly salaries (aggregate over all months in each year)
            total_income = grouped.groupby('year')['salary'].sum().reset_index(name='total_income')

            # Sum the total expense by year
            total_expense_df = df_selected_year.groupby('year')['amount'].sum().reset_index(name='total_expense')

            # Merge the total income and total expense dataframes on 'year' to calculate the available balance
            df_salary_expenses = pd.merge(total_income, total_expense_df, on='year')

            # Calculate the available balance for the selected year
            df_salary_expenses['available_balance'] = df_salary_expenses['total_income'] - df_salary_expenses['total_expense']
           

            # # Plot the data as a bar chart
            st.write(f'Expenses,Income & Available Balance Comparison for the {selected_year}')
            fig_expenses_salary = px.bar(df_salary_expenses, x='year', y=['total_expense', 'total_income', 'available_balance'],
                                        labels={'total_expense': 'Total Expense', 'total_income': 'Total Income', 'available_balance': 'Available Balance'},
                                        barmode='group',  # Group the bars next to each other
                                        color_discrete_sequence=['#19376D',
'#576CBC',
'#A5D7E8'])  # Colors for Expense, Salary, and Available Balance

            # Customize the layout of the chart
            fig_expenses_salary.update_layout(
                xaxis_title='Year',
                yaxis_title='Amount',
                barmode='group',  # Group the bars
                bargap=0.2,  # Gap between bars
                width=800,  # Width of the chart
                height=400 # Height of the chart
            )

            # Display the chart in the right column
            st.plotly_chart(fig_expenses_salary, use_container_width=True)

        with col3:
            with st.container():
                if option == "Expenses by Category":
                    st.text("Expenses by Category")
                    
                    # Define custom colors for each category
                    category_colors = {
                        'Food': '#EBD3F8',  # Light purple
                        'Transport': '#EBD3F8',  # Light purple
                        'Insurance': '#7A1CAC',  # Dark purple
                        'Utilities': '#EBD3F8',  # Light purple
                        'Loan Repayment': '#AD49E1',  # Bright purple
                        'Housing': '#2E073F'  # Dark red
                    }
                    
                    # Create the pie chart with custom colors
                    fig_category = px.pie(df_selection, values='amount', names='category', hole=0.3,
                                        color='category', color_discrete_map=category_colors)
                    st.plotly_chart(fig_category, use_container_width=True, height=200)  # Set a fixed height

                elif option == "Expenses by Payment Method":
                    st.text("Expenses by Payment Method")
                    
                    # Define custom colors for each payment method
                    payment_method_colors = {
                        'Credit Card': '#7A1CAC',  # Dark purple
                        'Debit Card': '#EBD3F8',  # Light purple
                        'Bank Transfer': '#2E073F'  # Dark red
                    }
                    
                    # Create the pie chart with custom colors
                    fig_payment = px.pie(df_selection, values='amount', names='payment_method', hole=0.3,
                                        color='payment_method', color_discrete_map=payment_method_colors)
                    st.plotly_chart(fig_payment, use_container_width=True, height=200)  # Set a fixed height
        with col2:
            
            
   
            with st.container():
                st.write(f'Expenses in {selected_year} by month')
                # Filter the data for the selected year and group by month to sum up expenses
                df_time = df_selection[df_selection['year'] == selected_year].groupby(['month'])['amount'].sum().reset_index()
                df_time = df_time.sort_values(by='month')
                    # Find the highest and lowest expense months
                highest_expense_month = df_time.loc[df_time['amount'].idxmax()]
          

                # Assign custom colors based on the expense amount
                df_time['color'] = df_time['month'].apply(
                    lambda x: 'highest' if x == highest_expense_month['month'] else 'lowest')
                

               # Create the area chart using Plotly
            fig_area = px.area(df_time, x='month', y='amount', color='color',
                            labels={'amount': 'Total Expense ($)', 'month': 'Month'},
                            color_discrete_map={'highest': '#5C469C', 'lowest': '#D8B9C3'})

            # Increase the area chart width and remove gaps between areas
            fig_area.update_layout(
                width=800,  # Increase the width of the chart
                height=400  # Adjust height if needed
            )

            # Display the area chart
            st.plotly_chart(fig_area, use_container_width=True)


        with col4:
            with st.container():
                
        

                # Calculate year-wise data
                category_gender_revenues = (
                    df.groupby(["category", "gender", "year"])["amount"]
                    .sum()
                    .unstack()
                    .assign(change=lambda x: x.pct_change(axis=1)[selected_year] * 100)
                )
            
                def calculate_year_salary(group):
                    distinct_days = group['day'].nunique()
                    total_salary = group['salary'].sum()
                    return round(total_salary / distinct_days, 0)

                # Find the highest expense for the selected year
                grouped = df[df['year'] == selected_year].groupby(['year', 'month']).apply(calculate_year_salary).reset_index(name='salary')
                

                # Sum the yearly salaries for the selected year
                income_for_year = grouped['salary'].sum()

                # Sum the total expense by year for the selected year
                total_expense_df_year = df[df['year'] == selected_year].groupby('year')['amount'].sum().reset_index(name='total_expense')
                total_expense_for_year_sum = total_expense_df_year['total_expense'].sum()

                # Calculate available balance for the selected year
                available_balance = income_for_year - total_expense_for_year_sum

                # Get the highest expense details
                max_amount = category_gender_revenues[selected_year].max()
                max_combination = category_gender_revenues[selected_year].idxmax()

                # Extract the details of the highest expense
                max_category, max_gender = max_combination
                max_change = category_gender_revenues.loc[max_combination, 'change']

                # Determine delta symbol and color based on change
                if max_change > 0:
                    delta_symbol = f"▲ {max_change:.0f}%"
                    delta_color = "green"
                elif max_change < 0:
                    delta_symbol = f"▼ {abs(max_change):.0f}%"
                    delta_color = "red"
                else:
                    delta_symbol = f"{max_change:.0f}%"
                    delta_color = "gray"


            

                # Style the first card (yearly data)
                card_style_1 = f"""
                <div style="background-color: #ffffff; 
            backdrop-filter: blur(10px); 
            border-radius: 15px; 
            padding: 15px; 
            margin: 10px; 
            box-shadow: 0 4px 8px rgb(24, 18, 43);
            font-family: 'Arial', sans-serif; 
            width: 275px; 
            font-size: 14px; 
            border: 3px solid rgba(255, 255, 255, 0.5);">
                    <div style="color: #333; padding: 10px; text-align: center; font-size: 16px; font-weight: bold; width: 100%;">
                
   
                        Highest Expense for {selected_year}
                    </div>
                    <div style="border-bottom: 2px solid #7A1CAC; margin-bottom: 10px;"></div>
                    <div style="text-align: center;">
                        <p style="font-size: 14px; font-weight: bold;">Category: {max_category}</p>
                        <p style="font-size: 14px; font-weight: bold;">Gender: {max_gender}</p>
                        <p style="font-size: 16px; font-weight: bold; color: #2a9d8f;">High Exp Amount: $ {max_amount:,.0f}</p>
                        <p style="font-size: 14px; font-weight: bold; color: {delta_color};">Change vs. PY: {delta_symbol}</p>
                        <p style="font-size: 14px; font-weight: bold; color: #4f4f4f;">Total Income for {selected_year}: $ {income_for_year:,.0f}</p>
                        <p style="font-size: 14px; font-weight: bold; color: #e76f51;">Total Expense for {selected_year}: $ {total_expense_for_year_sum:,.0f}</p>
                        <p style="font-size: 14px; font-weight: bold; color: #18122B;">Available Balance for {selected_year}: $ {available_balance:,.0f}</p>
                        
                     
                    </div>
                </div>
                """
                
                # Calculate month-wise data
                category_gender_revenues_month = (
                    
                    df.groupby(["category", "gender", "month"])["amount"]
                    .sum()
                    .unstack()
                    .assign(change=lambda x: x.pct_change(axis=1)[selected_month] * 100)
                )
               
                def calculate_year_salary(group):
                
                    month_salary = group['salary'].iloc[0]
                    return month_salary

                # Find the highest expense for the selected month
                grouped1 = df[(df['month'] == selected_month) & (df['year'] == selected_year)].groupby(['month', 'year']).apply(calculate_year_salary).reset_index(name='salary')
                
                # Sum the month salary for the selected month
                income_for_month = grouped1['salary'].sum()
                
                # Sum the total expense by year for the selected month
                total_expense_df = df[(df['month'] == selected_month) & (df['year'] == selected_year)].groupby('month')['amount'].sum().reset_index(name='total_expense')
                
                total_expense_for_month = total_expense_df['total_expense'].sum()
               
                # Calculate available balance for the selected month
                available_balance_month  = income_for_month - total_expense_for_month
               
                # Get the highest expense details
                max_amount_month  = category_gender_revenues_month[selected_month].max()
              
                max_combination_month = category_gender_revenues_month[selected_month].idxmax()
               
                
                # Extract the details of the highest expense
                max_category_month, max_gender_month= max_combination_month
            
                max_change_month = category_gender_revenues_month.loc[max_combination_month, 'change']
                
                
                # Determine delta symbol and color based on change
                if max_change_month > 0:
                    delta_symbol = f"▲ {max_change_month:.0f}%"
                    delta_color = "green"
                elif max_change_month < 0:
                    delta_symbol = f"▼ {abs(max_change_month):.0f}%"
                    delta_color = "red"
                else:
                    delta_symbol = f"{max_change_month:.0f}%"
                    delta_color = "gray"


                
                card_style_2 = f"""
                <div style="background-color:#ffffff; 
            backdrop-filter: blur(10px); 
            border-radius: 10px; 
            padding: 15px; 
            margin: 10px; 
            box-shadow: 0 4px 8px rgb(24, 18, 43);
            font-family: 'Arial', sans-serif; 
            width: 275px; 
            font-size: 14px; 
            border: 3px solid rgba(255, 255, 255, 0.5);">
                    <div style="color:#333; padding: 10px; border-radius: 15px; text-align: center; font-size: 16px; font-weight: bold; width: 100%;">
                
                        Highest Expense for {selected_month}
                    </div>
                    <div style="border-bottom: 2px solid #7A1CAC; margin-bottom: 10px;"></div>
                    <div style="text-align: center;">
                        <p style="font-size: 14px; font-weight: bold;">Category: {max_category_month}</p>
                        <p style="font-size: 14px; font-weight: bold;">Gender: {max_gender_month}</p>
                        <p style="font-size: 16px; font-weight: bold; color: #2a9d8f;">High Exp Amount: $ {max_amount_month:,.0f}</p>
                        <p style="font-size: 14px; font-weight: bold; color: {delta_color};">Change vs. PM: {delta_symbol}</p>
                        <p style="font-size: 14px; font-weight: bold; color: #4f4f4f;">Total Income for {selected_month}: $ {income_for_month:,.0f}</p>
                        <p style="font-size: 14px; font-weight: bold; color: #e76f51;">Total Expense for {selected_month}: $ {total_expense_for_month:,.0f}</p>
                        <p style="font-size: 14px; font-weight: bold; color: #18122B;">Available Balance for {selected_month}: $ {available_balance_month:,.0f}</p>
                    </div>
                </div>
                """

                        
            carousel_html = f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
            
            
                <title>Bootstrap Carousel</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous" >
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous" ></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js" integrity="sha384-0pUGZvbkm6XF6gxjEnlmuGrJXVbNuzT9qBBavbLwCsOGabYfZo0T0to5eqruptLy" crossorigin="anonymous"></script>
                
                </head>
                <body style="background-color: transparent; border-radius: 2px; margin: 1px;">
                    <div id="carouselExampleIndicators"  class="carousel slide" data-bs-ride="carousel"  >
                        <div class="carousel-inner">
                            <div class="carousel-item active"  >
                                {card_style_1}
                            </div>
                            <div class="carousel-item">
                                {card_style_2}
                            </div>
                        </div>
                        <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-bs-slide="prev" >
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </a>
                        <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </a>
                    </div>
                </body>
            </html>
            """
            components.html(carousel_html, height=390,width=290)
    Home()
            

        

                            

                            
                                
                            
        



