from backend import db_helper

def test_fetch_expense_for_date():
    res= db_helper.fetch_expense_for_date('2024-07-01')
    assert len(res)==1
    assert res[0]["category"]=="Meals"
    assert res[0]["amount"]==50
    assert res[0]["gender"]=="Male"
    assert res[0]["description"]=="Dinner with client at Restaurant XYZ"
    assert res[0]["payment_method"]=="Credit Card"
    assert res[0]["vendor"]=="Restaurant XYZ"
    assert res[0]["account"]== "Business Account"
    assert res[0]["notes"]=="Paid with company card"

# def test_delete_month_expense():
#     res=db_helper.delete_expense_for_date("2024-10-01")
#     assert len(res)==1
     
    
    