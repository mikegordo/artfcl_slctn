.PHONY: build_generator run_generator build_bioreactor build_ui deploy_generator deploy_redis deploy_bioreactor deploy_ui kill deploy

build_generator:
	cp -r shared ./generator/
	docker build -t himor/as-generator ./generator
	rm -fr ./generator/shared
	docker push himor/as-generator

run_generator:
	docker run -p 8080:8080 himor/as-generator

build_bioreactor:
	cp -r shared ./bioreactor/
	docker build -t himor/as-bioreactor ./bioreactor
	rm -fr ./bioreactor/shared
	docker push himor/as-bioreactor

build_ui:
	cp -r shared ./ui/
	docker build -t himor/as-ui ./ui
	rm -fr ./ui/shared
	docker push himor/as-ui

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

deploy_bioreactor:
	kubectl create -f deploy/bioreactor-deployment.yaml

deploy_ui:
	kubectl create -f deploy/ui-deployment.yaml
	kubectl create -f deploy/ui-service-exposed.yaml

build: build_generator build_bioreactor build_ui
	# done

kill:
	kubectl delete deployment generator-deployment
	kubectl delete deployment redis-deployment
	kubectl delete deployment bioreactor-deployment
	kubectl delete deployment ui-deployment
	kubectl delete service generator
	kubectl delete service redis
	kubectl delete service ui-service-exposed
	# kubectl delete service generator-service-exposed

deploy: deploy_generator deploy_redis deploy_bioreactor deploy_ui
	@echo "\nURL:"
	@minikube service ui-service-exposed --url
