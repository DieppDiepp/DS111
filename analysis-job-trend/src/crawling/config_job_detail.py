# analysis-job-trend\src\crawling\config_job_detail.py

# --- CẤU HÌNH XPATH CHI TIẾT (PARSED DATA) ---

# 1. Các trường lấy 1 giá trị duy nhất (Single Text)
SINGLE_FIELDS = {
    # --- HEADER SECTION ---
    "job_title": "//h1[contains(@class, 'job-detail__info--title')]//a",
    # 1. SALARY (Mức lương/Thu nhập)
    # Logic: Tìm vào khu vực chứa các section, lấy thẻ div con ĐẦU TIÊN [1], sau đó lấy value bên trong
    "salary": "(//div[contains(@class,'job-detail__info--sections')]//div[contains(@class,'job-detail__info--section')])[1]//div[contains(@class,'job-detail__info--section-content-value')]",
    "province": "(//div[contains(@class,'job-detail__info--sections')]//div[contains(@class,'job-detail__info--section')])[2]//div[contains(@class,'job-detail__info--section-content-value')]",
    "experience_years": "(//div[contains(@class,'job-detail__info--sections')]//div[contains(@class,'job-detail__info--section')])[3]//div[contains(@class,'job-detail__info--section-content-value')]",
    "deadline": "//div[contains(@class,'job-detail__info--deadline-date')]",

    # --- MAIN CONTENT SECTION (Mô tả, Yêu cầu...) ---
    # Logic: Tìm thẻ h3 chứa tiêu đề -> lấy thẻ div liền kề sau đó
    "job_description": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Mô tả công việc')]/following-sibling::div",
    "job_requirements": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Yêu cầu ứng viên')]/following-sibling::div",
    "job_benefits": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Quyền lợi')]/following-sibling::div",
    "job_location_detail": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Địa điểm làm việc')]/following-sibling::div",
    "working_time": "//div[contains(@class,'job-description__item')]//h3[contains(text(),'Thời gian làm việc')]/following-sibling::div",

    # --- COMPANY INFO ---
    "company_name": "//div[contains(@class,'company-name-label')]//a",
    "company_scale": "//div[contains(@class,'company-scale')]//div[@class='company-value']",
    "company_industry": "//div[contains(@class,'company-field')]//div[@class='company-value']",
    "company_address": "//div[contains(@class,'company-address')]//div[@class='company-value']",
    
    # --- GENERAL INFO ---
    "job_level": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Cấp bậc')]/following-sibling::div",
    "academic_level": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Học vấn')]/following-sibling::div",
    "job_type": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Hình thức làm việc')]/following-sibling::div",
    "quantity": "//div[contains(@class,'box-general-group-info-title') and contains(text(),'Số lượng tuyển')]/following-sibling::div",
}

# 2. Các trường lấy danh sách giá trị (List/Tags) -> Sẽ gộp lại bằng dấu phẩy
LIST_FIELDS = {
    "tags_role": "//div[contains(@class,'box-category')]//div[contains(text(),'Danh mục Nghề liên quan')]/following-sibling::div//a",
    "tags_skill": "//div[contains(@class,'box-category')]//div[contains(text(),'Kỹ năng cần có')]/following-sibling::div//a | //div[contains(@class,'box-category')]//div[contains(text(),'Kỹ năng cần có')]/following-sibling::div//span",
    "tags_location": "//div[contains(@class,'box-category')]//div[contains(text(),'Khu vực')]/following-sibling::div//a",
}

# 3. Các trường đặc biệt (Lấy thuộc tính href, src...)
ATTRIBUTE_FIELDS = {
    "company_url": ("//div[contains(@class,'company-name-label')]//a", "href"),
}