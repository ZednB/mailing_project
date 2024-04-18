from mail.management.commands.start_mail import Command


def schedule_mailing():
    Command().handle()
