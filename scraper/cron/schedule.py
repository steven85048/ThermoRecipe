from crontab import CronTab

user = 'ubuntu'
cron = CronTab(user=user)

job = cron.new(command='/usr/bin/flock -n /tmp/scraper.lockfile python3 ~/ThermoRecipe/scraper/cron/test.py >> /home/{}/scraper.log 2>&1'.format(user))
job.minute.every(1)

cron.write()