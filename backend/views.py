from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from .serializers import LoanSerializer
import math

@api_view(['POST'])
def register_customer(request):
    monthly_salary = request.data.get('monthly_income', 0)
    approved_limit = round(36 * monthly_salary / 100000) * 100000
    
    customer_data = {
        'first_name': request.data.get('first_name'),
        'last_name': request.data.get('last_name'),
        'phone_number': request.data.get('phone_number'),
        'monthly_salary': monthly_salary,
        'approved_limit': approved_limit,
    }
    
    customer = Customer.objects.create(**customer_data)
    
    response_data = {
        'customer_id': customer.customer_id,
        'name': f"{customer.first_name} {customer.last_name}",
        'age': request.data.get('age'),
        'monthly_income': customer.monthly_salary,
        'approved_limit': customer.approved_limit,
        'phone_number': customer.phone_number
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def check_eligibility(request):
    customer_id = request.data.get('customer_id')
    loan_amount = request.data.get('loan_amount', 0)
    interest_rate = request.data.get('interest_rate', 0)
    tenure = request.data.get('tenure', 1)
    
    monthly_installment = (loan_amount * (1 + interest_rate / 100)) / tenure

    response_data = {
        "customer_id": customer_id,
        "approval": True,
        "interest_rate": interest_rate,
        "corrected_interest_rate": interest_rate,
        "tenure": tenure,
        "monthly_installment": round(monthly_installment, 2)
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_loan(request):
    customer_id = request.data.get('customer_id')
    eligibility_response = check_eligibility(request._request).data

    if eligibility_response['approval']:
        response_data = {
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": True,
            "message": "Loan approved!",
            "monthly_installment": eligibility_response['monthly_installment']
        }
    else:
        response_data = {
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": "Loan not approved based on placeholder logic.",
            "monthly_installment": None
        }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
        serializer = LoanSerializer(loan)
        return Response(serializer.data)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_customer_loans(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
        loans = Loan.objects.filter(customer=customer)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)