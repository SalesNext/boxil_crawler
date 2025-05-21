from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from urllib.parse import urljoin
from boxil_crawler.parser.parse_service_rating import parse_service_rating
from collections.abc import Iterable
from boxil_crawler.schema.service import Service
from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from boxil_crawler.parser.parse_service_review import parse_service_review
import re

DATA_TABLE = {
    "導入形態": "service_deployment_type",
    "OS": "service_os",
    "iOSアプリ": "service_ios_app",
    "Androidアプリ": "service_android_app",
    "スマートフォンのブラウザ対応": "service_mobile_browser_support",
    "API連携": "service_api_integration",
    "SOC": "service_soc",
    "プライバシーマーク": "service_privacy_mark",
    "ISO": "service_iso",
    "そのほかセキュリティ認証": "service_other_security_cert",
    "メール": "service_support_email",
    "電話": "service_support_phone",
    "チャット": "service_support_chat",
    "オフィスコンビニ": "service_office_convenience",
    "お弁当": "service_lunch_box",
    "お菓子": "service_snacks",
    "ドリンク": "service_drinks",
    "冷蔵庫設置": "service_refrigerator_setup",
    "自販機設置": "service_vending_machine_setup",
    "冷蔵庫・自販機等メンテナンス無料": "service_free_maintenance",
    "メニュー日替り": "service_daily_menu",
    "注文販売": "service_order_sales",
    "直販販売": "service_direct_sales",
    "会社決済": "service_company_payment",
    "評価点数の設定": "service_rating_score_setting",
    "アラート機能": "service_alert_function",
    "生体認証": "service_biometric_authentication",
    "休暇管理・休暇付与方法": "service_holiday_management",
    "工数管理": "service_work_management",
    "ワークフロー機能（有給申請・残業申請）": "service_workflow_function",
    "スマホアプリ打刻": "service_smartphone_app_stamp",
    "シフト管理": "service_shift_management",
    "WEB打刻": "service_web_stamp",
    "ICカード打刻": "service_ic_card_stamp",
    "GPS打刻": "service_gps_stamp",
    "36協定対応機能": "service_36_agreement_function",
    "予実管理": "service_budget_management",
    "勤怠データのエクスポート方法": "service_attendance_data_export_method",
    "労務規定違反のアラート機能": "service_alert_function",
    "夜勤シフト対応": "service_night_shift_support",
    "複数店舗管理": "service_multiple_store_management",
    "出退勤の打刻": "service_attendance_stamp",
    "個人カレンダー	": "service_personal_calendar",
    "権限管理": "service_authority_management",
    "勤務時間の集計": "service_work_time_aggregation",
    "休憩の自動割り当て": "service_automatic_break_assignment",
    "印刷機能": "service_printing_function",
    "リマインドメール・連絡	": "service_reminder_email",
    "メッセージ機能": "service_message_function",
    "ヘルプ募集": "service_help_recruitment_function",
    "シフト自動作成": "service_shift_auto_creation",
    "シフト共有": "service_shift_sharing",
    "シフトパターンの登録": "service_shift_pattern_registration",
    "シフトのダウンロード": "service_shift_download",
    
    
}

def parse_service_detail(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
    
) -> Iterable[Event]:
    data = Service(
    service_id = response.url.split("/")[-2],
    service_name = response.xpath('//*[contains(@class, "ServiceInfoSection_serviceName")]/text()').get(),
    service_company_name = response.xpath('//*[contains(@class, "Organization_name")]/text()').get(),
    source_service_url = response.url,
    service_last_updated_at = response.xpath('//time/@datetime').get(),
    service_review_ranking= response.xpath('//*[contains(@class, "ServiceSummaryReviews_reviewCountRanking")]/text()').get(),
    service_rating_ranking = response.xpath('//*[contains(@class, "ServiceSummaryReviews_reviewAverageRanking")]/text()').get(),
    service_average_rating = response.xpath('//*[contains(@class, "ServiceSummaryReviews_reviewAverageValue")]/text()').get(),
    service_summary_description = ". ".join(response.xpath('//*[contains(@class, "ServiceSummaryPoints_pointTitleList")]/text()').getall()),
    service_price = response.xpath('//*[contains(@class, "ServiceSummaryPlans_fixedCostValue")]/text()').get(),
    service_initial_price = response.xpath('//*[contains(@class, "ServiceSummaryPlans_initialCostValue")]/text()').get(),
    service_overview_description = response.xpath('//*[contains(@class, "ServiceOverview_description")]/text()').get(),
    service_business_content = " ".join(response.xpath('//*[contains(@class, "ServiceEffect_description")]//text()').getall()),
    
    service_category_id = response.url.split('=')[-1]
    )
    pricing_and_plan = response.xpath('//*[contains(@class, "ServicePlans_badges")]//div/text()').getall(),
    
    for option in pricing_and_plan:
        if '無料プラン：' in option:
            option = option.replace("無料プラン：","")
            if option == 'ー':
                data.service_is_free_plan = False
            if option == 'あり':
                data.service_is_free_plan = True
                
        if '無料トライアル：' in option:
            option = option.replace("無料トライアル：","")
            if option == 'ー':
                data.service_is_free_trial = False
            if option == 'あり':
                data.service_is_free_trial = True
    data.service_monthly_price = "".join(response.xpath('//dd[contains(@class, "PlanCard_rowValue")]//text()').getall())
    data.service_customers = response.xpath('//*[contains(@class, "ServiceCustomers_list")]//li/span/text()').getall()
    data.service_img_url = response.xpath('//*[contains(@class, "ServiceMediaContents")]//div/img/@src').getall()
    data.service_company_logo_img = response.xpath('//*[contains(@class, "Organization_logo")]/img/@src').get()
    data.service_company_name = response.xpath("//*[contains(@class, 'Organization_name')]/text()").get()
    data.service_company_industry = response.xpath("//*[contains(@class, 'Organization_caption')][1]/text()").get()
    data.service_company_address = "".join(response.xpath("//*[contains(@class, 'Organization_caption')][2]/text()").getall())
    
    if data.service_company_industry:
        service_company_industry = data.service_company_industry.split("/")

        if len(service_company_industry) == 3:
            data.service_company_large_industry = data.service_company_industry.split("/")[0]
            data.service_company_medium_industry = data.service_company_industry.split("/")[1]
            data.service_company_small_industry = data.service_company_industry.split("/")[2]
        if len(service_company_industry) == 2:
            data.service_company_large_industry = data.service_company_industry.split("/")[0]
            data.service_company_medium_industry = data.service_company_industry.split("/")[1]
            data.service_company_small_industry = None
        if len(service_company_industry) == 1:
            data.service_company_large_industry = data.service_company_industry.split("/")[0]
            data.service_company_medium_industry = None
            data.service_company_small_industry = None
         
    data_table = response.xpath('//*[contains(@class, "SpecificationParent_table")]/tbody')
    
    for line in data_table:
        for label in DATA_TABLE:
            if label == "導入形態" or label == "導入形態" or label == "ISO" or label == "そのほかセキュリティ認証" or label == "評価点数の設定" or label == "勤怠データのエクスポート方法" or label == "SOC":
                value = line.xpath(f'.//tr[th[contains(text(), "{label}")]]/td//text()').get()
                setattr(data, DATA_TABLE[label], value)
            else:   
                value_false =  response.xpath(f'.//tr[th[contains(text(), "{label}")]]//div[contains(@class, "EmptyValue")]') or response.xpath(f'.//tr[th[contains(text(), "{label}")]]//div[contains(@class, "Bool_icon")]/svg[contains(@class, "Bool_disabled")]')
                value_true =  response.xpath(f'.//tr[th[contains(text(), "{label}")]]//div[contains(@class, "Bool_icon")]/svg[contains(@class, "Bool_enabled")]/circle')
                if  value_false:
                    value = False
                    setattr(data, DATA_TABLE[label], value)
                if  value_true:
                    value = True
                    setattr(data, DATA_TABLE[label], value)
                if not value_false and not value_true:
                    value = None
    
    yield CrawlEvent(
        request = Request(f"https://boxil.jp/service/{data.service_id}/reviews"),
        metadata= {
            "data": data,
        },
        callback = parse_service_rating,
    )
    
    yield CrawlEvent(
        request = Request(f"https://boxil.jp/service/{data.service_id}/reviews"),
        metadata= None,
        callback = parse_service_review,
    )