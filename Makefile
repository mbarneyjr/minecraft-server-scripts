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

# aws infrastructure
infrastructure:
	aws cloudformation deploy \
		--stack-name minecraft-overviewer \
		--template-file template.yml
