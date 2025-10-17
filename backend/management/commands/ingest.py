import pandas as pd
from django.core.management.base import BaseCommand
from backend.models import Customer, Loan

class Command(BaseCommand):
    help = 'Ingest data from customer_data.xlsx and loan_data.xlsx'

    def handle(self, *args, **kwargs):
        customers_df = pd.read_excel('data/customer_data.xlsx')
        loans_df = pd.read_excel('data/loan_data.xlsx')

        for _, row in customers_df.iterrows():
            Customer.objects.create(
                customer_id=row.get('Customer Id'),
                first_name=row.get('First Name'),
                last_name=row.get('Last Name'),
                phone_number=row.get('Phone Number'),
                monthly_salary=row.get('Monthly Salary'),
                approved_limit=row.get('Approved Limit')
            )
        self.stdout.write(self.style.SUCCESS('Successfully ingested customer data.'))

        for _, row in loans_df.iterrows():
            customer_instance = Customer.objects.get(customer_id=row.get('Customer ID'))
            Loan.objects.create(
                customer=customer_instance,
                loan_id=row.get('Loan Id'),
                loan_amount=row.get('Loan Amount'),
                tenure=row.get('Tenure'),
                interest_rate=row.get('Interest Rate'),
                monthly_repayment=row.get('Monthly Payment', 0),
                emis_paid_on_time=row.get('EMIs paid on_Time', 0),
                start_date=row.get('Date of Approval'),
                end_date=row.get('End Date')
            )
        self.stdout.write(self.style.SUCCESS('Successfully ingested loan data.'))