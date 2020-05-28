from crontab import CronTab

user = 'ubuntu'
cron = CronTab(user=user)

job = cron.new(command='cd /home/ubuntu/ThermoRecipe && python3 -m scraper.recipe_batch_processor >> /home/ubuntu/scraper.log')
job.every_reboot()

cron.write()