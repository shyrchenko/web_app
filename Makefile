up_db:
	docker-compose up -d db

shell_db:
	docker-compose exec db mysql -umaster -pmaster_password