from crontab import CronTab

cron = CronTab(user='ubuntu')

job = cron.new(command='/usr/bin/flock -n /tmp/scraper.lockfile python3 ~/ThermoRecipe/scraper/cron/test.py')
job.minute.every(1)

cron.write()