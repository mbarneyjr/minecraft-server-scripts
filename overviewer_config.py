from .observer import Observer, ProgressBarObserver, MultiplexingObserver


class MyObserver(Observer):
    def update_job(self, percent):
        try:
            import requests, os
            if os.getenv('JOB_ID'):
                requests.put('https://api.map.mc.mbarney.me/jobs/{}'.format(os.getenv('JOB_ID')), json={
                    'status': 'IN_PROGRESS',
                    'percent': int(percent),
                })
        except Exception as e:
            print(e)
    def start(self, max_value):
        self.threshold = 5
        self.max_value = max_value
    def update(self, current_value):
        if self.max_value:
            percent = (current_value / self.max_value) * 100
            if percent > self.threshold:
                self.threshold += 5
                self.update_job(percent)
    def finish(self):
        self.update_job(100)


observer = MultiplexingObserver(MyObserver(), ProgressBarObserver())


worlds['world'] = '~/.minecraft/server/world'
customwebassets = '/home/mbarney/.minecraft/server/minecraft-overviewer-admin/'

renders['overworld-day'] = {
    'world': 'world',
    'title': 'Overworld Daytime',
    'rendermode': 'smooth_lighting',
    'dimension': 'overworld',
}

renders['overworld-night'] = {
    'world': 'world',
    'title': 'Overworld Night',
    'rendermode': 'smooth_night',
    'dimension': 'overworld',
}

outputdir = '~/.minecraft/server/map'
