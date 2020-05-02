# minecraft server management
start:
	screen -DmS minecraft java -Xmx8G -jar server.jar nogui &
resume:
	screen -r minecraft
stop:
	screen -p 0 -S minecraft -X eval 'stuff "say SERVER SHUTTING DOWN. Saving map..."\\015'
	screen -p 0 -S minecraft -X eval 'stuff "save-all"\\015'
	sleep 5
	screen -p 0 -S minecraft -X eval 'stuff "stop"\\015'

# chunk generation and mapping
chunks:
	./chunks.sh
map: world
	overviewer.py --config=overviewer_config.py
upload: map
	export SITE_BUCKET=$$(aws ssm get-parameter --name /minecraft-overviewer/site-bucket --query Parameter.Value --output text); \
	cd map; aws s3 sync . s3://$${SITE_BUCKET} --delete
map-watch:
	screen -DmS map-watch python watch.py &
resume-map-watch:
	screen -r map-watch

# aws infrastructure
infrastructure:
	aws cloudformation deploy \
		--stack-name minecraft-overviewer \
		--template-file template.yml

# world customizations
death-counter:
	screen -p 0 -S minecraft -X eval 'stuff "scoreboard objectives add totalDeaths deathCount \\"Total Deaths\\""\\015'
	screen -p 0 -S minecraft -X eval 'stuff "scoreboard objectives setdisplay list totalDeaths"\\015'
	screen -p 0 -S minecraft -X eval 'stuff "scoreboard objectives setdisplay belowName totalDeaths"\\015'
