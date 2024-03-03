from flask import Blueprint
from service import oshi_setting_service

# Generate Router Instance
router = Blueprint('router_liff', __name__)



# 推し設定項目
## 推し設定項目 取得
@router.route("/liffapi/v1/oshi/settings/get", methods=['POST'])
def func001():
    return oshi_setting_service.get_oshi_setting_liff()

## 推し設定項目 設定
@router.route("/liffapi/v1/oshi/settings/update", methods=['POST'])
def func002():
    return oshi_setting_service.update_oshi_setting_liff()

