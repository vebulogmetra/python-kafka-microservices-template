DC = docker compose
DB = docker build
LOGS = docker logs

ORDER_DOCKERFILE = Dockerfile-order
PAYMENT_DOCKERFILE = Dockerfile-payment
NOTIFICATION_DOCKERFILE = Dockerfile-notification
ANALYTIC_DOCKERFILE = Dockerfile-analytic

ORDER_CONTAINER = order_service
PAYMENT_CONTAINER = payment_service
NOTIFICATION_CONTAINER = notification_service
ANALYTIC_CONTAINER = analytic_service


.PHONY: build_all build_order_service build_payment_service build_notification_service build_analytic_service

build_all: build_order_service build_payment_service build_notification_service build_analytic_service
	@echo "All services built successfully"

build_order_service:
	${DB} -t order_service:v1 -f ${ORDER_DOCKERFILE} .

build_payment_service:
	${DB} -t payment_service:v1 -f ${PAYMENT_DOCKERFILE} .

build_notification_service:
	${DB} -t notification_service:v1 -f ${NOTIFICATION_DOCKERFILE} .

build_analytic_service:
	${DB} -t analytic_service:v1 -f ${ANALYTIC_DOCKERFILE} .


.PHONY: order-logs payment-logs notification-logs analytic-logs

order-logs:
	${LOGS} ${ORDER_CONTAINER} -f

payment-logs:
	${LOGS} ${PAYMENT_CONTAINER} -f

notification-logs:
	${LOGS} ${NOTIFICATION_CONTAINER} -f

analytic-logs:
	${LOGS} ${ANALYTIC_CONTAINER} -f


.PHONY: serve stop

serve:
	${DC} up

stop:
	${DC} down -v