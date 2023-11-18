from common.constants import TITLE, INDEX_PAGE_TITLE

JAZZMIN_SETTINGS = {
    "site_title": TITLE,
    "site_header": TITLE,
    "site_brand": TITLE,
    "site_logo": "img/logo.png",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": f"Welcome to the {TITLE}",
    "copyright": TITLE,
    # "search_model": ["auth.User", "auth.Group"],
    "user_avatar": None,
    # "topmenu_links": [
    #     {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    #     {"model": "auth.User"},
    # ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    # "order_with_respect_to": ["users", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "users.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "common.SiteConfiguration": "fas fa-cog",
        "locations.Country": "fas fa-globe",
        "locations.State": "fas fa-map-marker-alt",
        "locations.City": "fas fa-city",
        "users.UserAddresses": "fas fa-address-card",
        "products.ProductCategories": "fas fa-cubes",
        "products.ProductInventory": "fas fa-archive",
        "products.ProductDiscount": "fas fa-percent",
        "products.Product": "fas fa-box"
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "body_small_text": True,
    "brand_colour": "navbar-navy",
    "accent": "accent-primary",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_legacy_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-primary"
    }
}