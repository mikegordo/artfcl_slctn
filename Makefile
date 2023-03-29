.PHONY: build_generator run_generator deploy_generator kill deploy_redis deploy

build_generator:
	docker build -t himor/as-generator ./generator
	docker push himor/as-generator

run_generator:
	docker run -p 8080:8080 himor/as-generator

deploy_generator:
	kubectl create -f deploy/generator-deployment.yaml
	kubectl create -f deploy/generator-service.yaml
	# kubectl create -f deploy/generator-service-exposed.yaml
	# @echo "\nGenerator URL (default endpoint /get-sentence):"
	# @minikube service generator-service-exposed --url
	# @echo "\n"

deploy_redis:
	kubectl create -f deploy/redis-deployment.yaml
	kubectl create -f deploy/redis-service.yaml

kill:
	kubectl delete deployment generator-deployment
	kubectl delete deployment redis-deployment
	kubectl delete service generator-service
	kubectl delete service redis
	# kubectl delete service generator-service-exposed

deploy: deploy_generator deploy_redis
	@echo "\nURL:"
	@minikube service ui-service-exposed --url
