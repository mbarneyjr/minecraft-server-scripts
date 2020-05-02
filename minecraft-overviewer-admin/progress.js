setInterval(async () => {
    const mapProgress = document.getElementById('map-progress');
    const respones = await fetch('https://api.map.mc.mbarney.me/jobs');
    const { jobs } = await respones.json();
    if (jobs && jobs.length > 0) {
        const job = jobs[0];
        mapProgress.hidden = false;
        if (job.status == 'REQUESTED') {
            delete mapProgress.max;
            delete mapProgress.value;
        } else if (job.status == 'IN_PROGRESS') {
            const jobProgress = String(job.percent || 0);
            mapProgress.max = 100;
            mapProgress.value = jobProgress;
        }
    } else {
        mapProgress.hidden = true;
    }
}, 5000)

async function requestMap() {
    await fetch('https://api.map.mc.mbarney.me/jobs', {method: 'POST'});
}