CREATE_NOTIFICATION_URL = 'https://onesignal.com/api/v1/notifications'
NOTIFICATION_CAMPAIGN_NAME = 'Backend'


# Trigger point name should start with module name. Ex: REVIEW_
# Module name should be same as the key defined in base.constants.MODULE_NAME_MAPPING
CUSTOM_NOTIFICATION = 'CUSTOM_NOTIFICATION'
# REVIEW_DEFAULT_SEND_REVIEWEE = 'REVIEW_DEFAULT_SEND_REVIEWEE'
# REVIEW_DEFAULT_SEND_HR = 'REVIEW_DEFAULT_SEND_HR'
# REVIEW_DEFAULT_SEND_MENTOR = 'REVIEW_DEFAULT_SEND_MENTOR'
# REVIEW_YEAR_END = 'REVIEW_YEAR_END'
# REVIEW_MANAGER_MENTOR = 'REVIEW_MANAGER_MENTOR'
NOTIFICATION_TRIGGER_POINTS = [
    # (REVIEW_DEFAULT_SEND_REVIEWEE, 'When an employee send a review from app - for reviewee'),
    # (REVIEW_DEFAULT_SEND_HR, 'When an employee send a review from app - for hr'),
    # (REVIEW_DEFAULT_SEND_MENTOR, 'When an employee send a review from app - for mentor'),
    # (REVIEW_MANAGER_MENTOR, 'When HR/People team send reminder for every 3 months review from admin'),
    # (REVIEW_YEAR_END, 'When HR/People team send reminder for year end review'),
]
NOTIFICATION_TRIGGER_POINTS_WITH_DYNAMIC_VARIABLES = {
    # REVIEW_DEFAULT_SEND_REVIEWEE: ['{review_to}', '{review_from}'],
    # REVIEW_DEFAULT_SEND_HR: ['{review_to}', '{review_from}'],
    # REVIEW_DEFAULT_SEND_MENTOR: ['{review_to}', '{review_from}', '{mentor_name}'],
    # REVIEW_YEAR_END: ['{mentor_name}', '{mentee_name}', '{last_date}', '{year}'],
    # REVIEW_MANAGER_MENTOR: ['{mentor_name}', '{mentee_name}'],
    CUSTOM_NOTIFICATION: ['{employee_name}'],
}
