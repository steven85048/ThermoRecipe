from crontab import CronTab

user="ubuntu"
cron = CronTab(user=user)

job = cron.new(command='source ~/.profile && cd /home/ubuntu/ThermoRecipe && python3 -m scraper.scraper >> /home/ubuntu/scraper.log 2&>1')
job.every_reboot()

cron.write()