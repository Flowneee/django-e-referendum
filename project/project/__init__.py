from project.settings import DEBUG

if DEBUG:
    from mmc.mixins import inject_management

    inject_management()
