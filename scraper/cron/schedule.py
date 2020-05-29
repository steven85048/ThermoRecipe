from crontab import CronTab

cron = CronTab(user=user)

job = cron.new(command='cd /home/ubuntu/ThermoRecipe && python3 -m scraper.scraper >> /home/ubuntu/scraper.log')
job.every_reboot()

cron.write()