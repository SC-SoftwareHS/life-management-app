"""Finance endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from ..db import get_session
from ..schemas import FinancialAccountCreate, FinancialAccountUpdate, FinancialAccountResponse
from ..models import FinancialAccount, User, FinancialAccountType
from ..auth import get_current_user

router = APIRouter()


@router.post("/", response_model=FinancialAccountResponse, status_code=status.HTTP_201_CREATED)
def create_financial_account(
    account_data: FinancialAccountCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new financial account.

    - **name**: Account name (e.g., "Chase Checking", "Vanguard 401k")
    - **account_type**: bank, investment, credit_card, loan, asset, or liability
    - **balance**: Current balance (positive for assets, negative for liabilities)
    - **institution**: Bank/institution name
    - **account_number_last4**: Optional last 4 digits of account number
    - **notes**: Optional notes
    """
    # Create financial account
    account = FinancialAccount(
        user_id=current_user.id,
        name=account_data.name,
        account_type=account_data.account_type,
        balance=account_data.balance,
        institution=account_data.institution,
        account_number_last4=account_data.account_number_last4,
        notes=account_data.notes
    )
    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@router.get("/", response_model=List[FinancialAccountResponse])
def list_financial_accounts(
    account_type: Optional[FinancialAccountType] = Query(None, description="Filter by account type"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List all financial accounts for the current user.

    Optional filters:
    - **account_type**: Filter by bank, investment, credit_card, loan, asset, or liability
    """
    # Build query
    statement = select(FinancialAccount).where(FinancialAccount.user_id == current_user.id)

    if account_type:
        statement = statement.where(FinancialAccount.account_type == account_type)

    accounts = session.exec(statement).all()
    return accounts


@router.get("/summary")
def get_financial_summary(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get financial summary with total assets, liabilities, and net worth.

    Calculates:
    - Total assets (positive balances)
    - Total liabilities (negative balances or debt accounts)
    - Net worth (assets - liabilities)
    """
    statement = select(FinancialAccount).where(FinancialAccount.user_id == current_user.id)
    accounts = session.exec(statement).all()

    total_assets = 0.0
    total_liabilities = 0.0

    for account in accounts:
        if account.account_type in [FinancialAccountType.LOAN, FinancialAccountType.LIABILITY]:
            # Loans and liabilities count as debt
            total_liabilities += abs(account.balance)
        elif account.account_type == FinancialAccountType.CREDIT_CARD:
            # Credit card balance (if positive, it's debt owed)
            if account.balance > 0:
                total_liabilities += account.balance
            else:
                # Negative credit card balance means overpayment (asset)
                total_assets += abs(account.balance)
        else:
            # Bank accounts, investments, and other assets
            if account.balance > 0:
                total_assets += account.balance
            else:
                total_liabilities += abs(account.balance)

    net_worth = total_assets - total_liabilities

    return {
        "total_assets": round(total_assets, 2),
        "total_liabilities": round(total_liabilities, 2),
        "net_worth": round(net_worth, 2),
        "account_count": len(accounts)
    }


@router.get("/{account_id}", response_model=FinancialAccountResponse)
def get_financial_account(
    account_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific financial account by ID.
    """
    account = session.get(FinancialAccount, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial account not found"
        )

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this financial account"
        )

    return account


@router.put("/{account_id}", response_model=FinancialAccountResponse)
def update_financial_account(
    account_id: int,
    account_data: FinancialAccountUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing financial account.

    All fields are optional. Only provided fields will be updated.
    """
    account = session.get(FinancialAccount, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial account not found"
        )

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this financial account"
        )

    # Update fields
    update_data = account_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(account, key, value)

    account.updated_at = datetime.utcnow()
    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_financial_account(
    account_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a financial account.
    """
    account = session.get(FinancialAccount, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial account not found"
        )

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this financial account"
        )

    session.delete(account)
    session.commit()

    return None
