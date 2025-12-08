# analysis-job-trend/src/config_job_detail.py

# CONFIG 1: STANDARD LAYOUT (Trang /viec-lam/ bình thường)
STANDARD = {
    "SINGLE_FIELDS": {
        "job_title": "//h1[contains(@class, 'job-detail__info--title')]",
        # Header Info (Neo vào ID header-job-info)
        "salary": "//div[@id='header-job-info']//div[contains(@class,'job-detail__info--sections')]/div[contains(@class,'job-detail__info--section')][1]//div[contains(@class,'job-detail__info--section-content-value')]",
        "province": "//div[@id='header-job-info']//div[contains(@class,'job-detail__info--sections')]/div[contains(@class,'job-detail__info--section')][2]//div[contains(@class,'job-detail__info--section-content-value')]",
        "experience_years": "//div[@id='header-job-info']//div[contains(@class,'job-detail__info--sections')]/div[contains(@class,'job-detail__info--section')][3]//div[contains(@class,'job-detail__info--section-content-value')]",
        "deadline": "//div[contains(@class,'job-detail__info--deadline-date')]",
        
        # Main Content
        "job_description": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Mô tả công việc')]/following-sibling::div",
        "job_requirements": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Yêu cầu ứng viên')]/following-sibling::div",
        "job_benefits": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Quyền lợi')]/following-sibling::div",
        "job_location_detail": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Địa điểm làm việc')]/following-sibling::div",
        "working_time": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Thời gian làm việc')]/following-sibling::div",

        # Company Info
        "company_name": "//div[contains(@class,'company-name-label')]//a",
        "company_scale": "//div[contains(@class,'company-scale')]//div[@class='company-value']",
        "company_industry": "//div[contains(@class,'company-field')]//div[@class='company-value']",
        "company_address": "//div[contains(@class,'company-address')]//div[@class='company-value']",
        
        # General Info
        "job_level": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Cấp bậc')]/following-sibling::div",
        "academic_level": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Học vấn')]/following-sibling::div",
        "job_type": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Hình thức làm việc')]/following-sibling::div",
        "quantity": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Số lượng tuyển')]/following-sibling::div",
    },
    "LIST_FIELDS": {
        "tags_role": "//div[contains(@class,'box-category')]//div[contains(text(),'Danh mục Nghề liên quan')]/following-sibling::div//a",
        "tags_skill": "//div[contains(@class,'box-category')]//div[contains(text(),'Kỹ năng cần có')]/following-sibling::div//a | //div[contains(@class,'box-category')]//div[contains(text(),'Kỹ năng cần có')]/following-sibling::div//span",
        "tags_location": "//div[contains(@class,'box-category')]//div[contains(text(),'Khu vực')]/following-sibling::div//a | //div[contains(@class,'box-category')]//div[contains(text(),'Khu vực')]/following-sibling::div//span[contains(@class, 'box-category-tag')]",
    },
    "ATTRIBUTE_FIELDS": {
        "company_url": ("//div[contains(@class,'company-name-label')]//a", "href"),
    }
}


# CONFIG 2: BRAND LAYOUT (Trang /brand/ đặc biệt)
BRAND = {
    "SINGLE_FIELDS": {
        # Header
        "job_title": "//h2[contains(@class, 'premium-job-basic-information__content--title')]",
        
        # Ô thông tin Header (Dựa vào text label để tìm value)
        "salary": "//div[contains(@class, 'basic-information-item__data--label') and (contains(text(), 'Thu nhập') or contains(text(), 'Mức lương') or contains(text(), 'Lương'))]/following-sibling::div",
        "province": "//div[contains(@class, 'basic-information-item__data--label') and contains(text(), 'Địa điểm')]/following-sibling::div",
        "experience_years": "//div[contains(@class, 'basic-information-item__data--label') and contains(text(), 'Kinh nghiệm')]/following-sibling::div",
        
        # Main Content Boxes
        "job_description": "//div[contains(@class, 'premium-job-description__box')]//h2[contains(text(), 'Mô tả')]/following-sibling::div",
        "job_requirements": "//div[contains(@class, 'premium-job-description__box') and contains(@class, 'requirement')]//div[contains(@class, 'premium-job-description__box--content')]",
        "job_benefits": "//div[contains(@class, 'premium-job-description__box') and contains(@class, 'benefit')]//div[contains(@class, 'premium-job-description__box--content')]",
        
        # Địa điểm & Thời gian
        "job_location_detail": "//div[contains(@class, 'premium-job-description__box')]//h2[contains(text(), 'Địa điểm làm việc')]/following-sibling::div",
        "working_time": "//div[contains(@class, 'premium-job-description__box')]//h2[contains(text(), 'Thời gian làm việc')]/following-sibling::div",

        # Company Info (Brand Page)
        "company_name": "//h1[contains(@class, 'company-content__title--name')]",
        "company_scale": "//div[@class='non-existent-element']", # Brand page thường giấu cái này hoặc ở trang khác, set dummy để trả về Null
        "company_industry": "//div[@class='non-existent-element']", # Tương tự
        "company_address": "//div[contains(@class, 'premium-job-description__box')]//h2[contains(text(), 'Địa điểm làm việc')]/following-sibling::div", # Lấy luôn địa điểm làm việc như bạn yêu cầu
        
        # General Info (Box bên phải)
        "job_level": "//div[contains(@class, 'general-information-data__label') and contains(text(), 'Cấp bậc')]/following-sibling::div",
        "academic_level": "//div[contains(@class, 'general-information-data__label') and contains(text(), 'Học vấn')]/following-sibling::div",
        "job_type": "//div[contains(@class, 'general-information-data__label') and contains(text(), 'Hình thức')]/following-sibling::div",
        "quantity": "//div[contains(@class, 'general-information-data__label') and contains(text(), 'Số lượng')]/following-sibling::div",
        "deadline": "//div[contains(@class, 'general-information-data__label') and contains(text(), 'Hạn nộp')]/following-sibling::div",
    },
    "LIST_FIELDS": {
        "tags_role": "//div[contains(@class, 'premium-job-related-tags')]//h2[contains(text(), 'Nghề liên quan')]/following-sibling::div//a",
        "tags_skill": "//div[contains(@class, 'premium-job-related-tags')]//h2[contains(text(), 'Kỹ năng')]/following-sibling::div//span",
        "tags_location": "//div[contains(@class, 'premium-job-related-tags')]//h2[contains(text(), 'Khu vực')]/following-sibling::div//a | //div[contains(@class, 'premium-job-related-tags')]//h2[contains(text(), 'Khu vực')]/following-sibling::div//span",
    },
    "ATTRIBUTE_FIELDS": {
        # Link công ty ở tab list
        "company_url": ("//div[contains(@class, 'premium-job-header__company--tab-list')]//a[contains(text(), 'Trang chủ')]", "href"),
    }
}

# CONFIG 3: BRAND LAYOUT V2 (Giao diện Brand Box-Header)
BRAND_V2 = {
    "SINGLE_FIELDS": {
        # Header Info
        "job_title": "//div[@class='box-header']//h2[contains(@class, 'title')]",
        
        # DEADLINE: Lấy con số trong thẻ strong
        # Logic: Tìm span deadline -> lấy thẻ strong bên trong (chứa số ngày)
        "deadline": "//span[contains(@class, 'deadline')]//strong", 
        
        # Box Thông tin chính
        "salary": "//div[@class='box-item']//strong[(contains(text(), 'Mức lương') or contains(text(), 'Thu nhập') or contains(text(), 'Lương'))]/following-sibling::span",
        "quantity": "//div[@class='box-item']//strong[contains(text(), 'Số lượng tuyển')]/following-sibling::span",
        "job_type": "//div[@class='box-item']//strong[contains(text(), 'Hình thức làm việc')]/following-sibling::span",
        "job_level": "//div[@class='box-item']//strong[contains(text(), 'Cấp bậc')]/following-sibling::span",
        "academic_level": "//div[@class='box-item']//strong[contains(text(), 'Học vấn')]/following-sibling::span",
        "experience_years": "//div[@class='box-item']//strong[contains(text(), 'Kinh nghiệm')]/following-sibling::span",
        
        # Địa điểm & Thời gian
        "job_location_detail": "//div[@class='box-address']//div[not(@class)]",
        "working_time": "//div[@class='box-info']//h2[contains(text(), 'Thời gian làm việc')]/following-sibling::div",

        # Nội dung chính
        "job_description": "//div[@class='box-info']//h2[contains(text(), 'Mô tả công việc')]/following-sibling::div",
        "job_requirements": "//div[contains(@class, 'box-info') and contains(@class, 'requirement')]//div[contains(@class, 'content-tab')]",
        "job_benefits": "//div[contains(@class, 'box-info') and contains(@class, 'benefit')]//div[contains(@class, 'content-tab')]",

        # Company Info (Lấy từ Footer)
        "company_name": "//div[@class='footer-info']//div[contains(@class, 'footer-info-company-name')]",
        "company_address": "//div[@class='footer-info']//div[contains(text(), 'Địa chỉ:')]/following-sibling::div[1]",
        # Scale và Industry thường không có ở footer này, để null
        "company_scale": "//div[@id='dummy-scale']",
        "company_industry": "//div[@id='dummy-industry']",
    },
    "LIST_FIELDS": {
        # Lấy tất cả thẻ A (Tên TP) trong box Khu vực. Kết quả sẽ là: "Hà Nội, Hồ Chí Minh"
        "province": "//div[contains(@class, 'box-skill')]//h4[contains(text(), 'Khu vực')]/following-sibling::div[@class='item']//a",

        # Tags Location chi tiết (Lấy cả Phường/Quận)
        "tags_location": "//div[contains(@class, 'box-skill')]//h4[contains(text(), 'Khu vực')]/following-sibling::div[@class='item']//*[self::a or self::span]",
        
        "tags_skill": "//div[@class='job-tags__group']//div[contains(text(), 'Chuyên môn')]/parent::div//a",
        "tags_role": "//div[@class='box-career']//div[@class='item']//a",
    },
    "ATTRIBUTE_FIELDS": {
        # Lấy href của thẻ A nằm cạnh dòng chữ "Website:" trong footer
        "company_url": ("//div[@class='footer-info']//div[contains(text(), 'Website:')]/following-sibling::div[1]//a", "href"),
    }
}