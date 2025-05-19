from services.ml_service import predict_item

def test_predict_item_returns_dict():
    output = predict_item({'product':'x','color':'y'})
    assert isinstance(output, dict)