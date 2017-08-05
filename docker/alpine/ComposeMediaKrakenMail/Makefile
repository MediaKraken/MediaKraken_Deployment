NAME = tvial/docker-mailserver:testing

all: build-no-cache generate-accounts run fixtures tests clean
all-fast: build generate-accounts run fixtures tests clean
no-build: generate-accounts run fixtures tests clean

build-no-cache:
	cd test/docker-openldap/ && docker build -f Dockerfile -t ldap --no-cache .
	docker build --no-cache -t $(NAME) .

build:
	cd test/docker-openldap/ && docker build -f Dockerfile -t ldap .
	docker build -t $(NAME) .

generate-accounts:
	docker run --rm -e MAIL_USER=user1@localhost.localdomain -e MAIL_PASS=mypassword -t $(NAME) /bin/sh -c 'echo "$$MAIL_USER|$$(doveadm pw -s SHA512-CRYPT -u $$MAIL_USER -p $$MAIL_PASS)"' > test/config/postfix-accounts.cf
	docker run --rm -e MAIL_USER=user2@otherdomain.tld -e MAIL_PASS=mypassword -t $(NAME) /bin/sh -c 'echo "$$MAIL_USER|$$(doveadm pw -s SHA512-CRYPT -u $$MAIL_USER -p $$MAIL_PASS)"' >> test/config/postfix-accounts.cf

run:
	# Run containers
	docker run -d --name mail \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-v "`pwd`/test/onedir":/var/mail-state \
		-e ENABLE_CLAMAV=1 \
		-e ENABLE_SPAMASSASSIN=1 \
		-e SA_TAG=-5.0 \
		-e SA_TAG2=2.0 \
		-e SA_KILL=3.0 \
		-e SA_SPAM_SUBJECT="SPAM: " \
		-e VIRUSMAILS_DELETE_DELAY=7 \
		-e SASL_PASSWD="external-domain.com username:password" \
		-e ENABLE_MANAGESIEVE=1 \
		-e PERMIT_DOCKER=host \
		-e DMS_DEBUG=0 \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name mail_pop3 \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-v "`pwd`/test/config/letsencrypt":/etc/letsencrypt/live \
		-e ENABLE_POP3=1 \
		-e DMS_DEBUG=1 \
		-e SSL_TYPE=letsencrypt \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name mail_smtponly \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e SMTP_ONLY=1 \
		-e PERMIT_DOCKER=network \
		-e OVERRIDE_HOSTNAME=mail.my-domain.com \
		-t $(NAME)
	sleep 15
	docker run -d --name mail_smtponly_without_config \
		-e SMTP_ONLY=1 \
		-e ENABLE_LDAP=1 \
		-e PERMIT_DOCKER=network \
		-e OVERRIDE_HOSTNAME=mail.mydomain.com \
		-t $(NAME)
	sleep 15
	docker run -d --name mail_override_hostname \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e PERMIT_DOCKER=network \
		-e OVERRIDE_HOSTNAME=mail.my-domain.com \
		-h mail.my-domain.com \
		-t $(NAME)
	sleep 15
	docker run -d --name mail_fail2ban \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_FAIL2BAN=1 \
		--cap-add=NET_ADMIN \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name mail_fetchmail \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_FETCHMAIL=1 \
		--cap-add=NET_ADMIN \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name mail_disabled_clamav_spamassassin \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_CLAMAV=0 \
		-e ENABLE_SPAMASSASSIN=0 \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name mail_manual_ssl \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e SSL_TYPE=manual \
		-e SSL_CERT_PATH=/tmp/docker-mailserver/letsencrypt/mail.my-domain.com/fullchain.pem \
		-e SSL_KEY_PATH=/tmp/docker-mailserver/letsencrypt/mail.my-domain.com/privkey.pem \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name ldap_for_mail \
		-e LDAP_DOMAIN="localhost.localdomain" \
		-h ldap.my-domain.com -t ldap
	sleep 15
	docker run -d --name mail_with_ldap \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_LDAP=1 \
		-e LDAP_SERVER_HOST=ldap \
		-e LDAP_SEARCH_BASE=ou=people,dc=localhost,dc=localdomain \
		-e LDAP_BIND_DN=cn=admin,dc=localhost,dc=localdomain \
		-e LDAP_BIND_PW=admin \
		-e LDAP_QUERY_FILTER_USER="(&(mail=%s)(mailEnabled=TRUE))" \
		-e LDAP_QUERY_FILTER_GROUP="(&(mailGroupMember=%s)(mailEnabled=TRUE))" \
		-e LDAP_QUERY_FILTER_ALIAS="(&(mailAlias=%s)(mailEnabled=TRUE))" \
		-e DOVECOT_PASS_FILTER="(&(objectClass=PostfixBookMailAccount)(uniqueIdentifier=%n))" \
		-e DOVECOT_USER_FILTER="(&(objectClass=PostfixBookMailAccount)(uniqueIdentifier=%n))" \
		-e ENABLE_SASLAUTHD=1 \
		-e SASLAUTHD_MECHANISMS=ldap \
		-e SASLAUTHD_LDAP_SERVER=ldap \
		-e SASLAUTHD_LDAP_BIND_DN=cn=admin,dc=localhost,dc=localdomain \
		-e SASLAUTHD_LDAP_PASSWORD=admin \
		-e SASLAUTHD_LDAP_SEARCH_BASE=ou=people,dc=localhost,dc=localdomain \
		-e POSTMASTER_ADDRESS=postmaster@localhost.localdomain \
		--link ldap_for_mail:ldap \
		-h mail.my-domain.com -t $(NAME)
	sleep 15
	docker run -d --name mail_with_imap \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_SASLAUTHD=1 \
		-e SASLAUTHD_MECHANISMS=rimap \
		-e SASLAUTHD_MECH_OPTIONS=127.0.0.1 \
		-e POSTMASTER_ADDRESS=postmaster@localhost.localdomain \
		-h mail.my-domain.com -t $(NAME)
	# Wait for containers to fully start
	sleep 15
	docker run -d --name mail_lmtp_ip \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test/config/dovecot-lmtp":/etc/dovecot \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_POSTFIX_VIRTUAL_TRANSPORT=1 \
		-e POSTFIX_DAGENT=lmtp:127.0.0.1:24 \
		-h mail.my-domain.com -t $(NAME)
	sleep 30
	docker run -d --name mail_with_postgrey \
		-v "`pwd`/test/config":/tmp/docker-mailserver \
		-v "`pwd`/test":/tmp/docker-mailserver-test \
		-e ENABLE_POSTGREY=1 \
		-e POSTGREY_DELAY=15 \
		-e POSTGREY_MAX_AGE=35 \
		-e POSTGREY_TEXT="Delayed by postgrey" \
		-h mail.my-domain.com -t $(NAME)
	sleep 20


fixtures:
	cp config/postfix-accounts.cf config/postfix-accounts.cf.bak
	# Setup sieve & create filtering folder (INBOX/spam)
	docker cp "`pwd`/test/config/sieve/dovecot.sieve" mail:/var/mail/localhost.localdomain/user1/.dovecot.sieve
	docker exec mail /bin/sh -c "maildirmake.dovecot /var/mail/localhost.localdomain/user1/.INBOX.spam"
	docker exec mail /bin/sh -c "chown 5000:5000 -R /var/mail/localhost.localdomain/user1/.INBOX.spam"
	# Sending test mails
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/amavis-spam.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/amavis-virus.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-alias-external.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-alias-local.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-alias-recipient-delimiter.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-user1.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-user2.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-user-and-cc-local-alias.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-regexp-alias-external.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-regexp-alias-local.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-catchall-local.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/sieve-spam-folder.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/sieve-pipe.txt"
	docker exec mail /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/non-existing-user.txt"
	docker exec mail_disabled_clamav_spamassassin /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-user1.txt"
	# postfix virtual transport lmtp
	docker exec mail_lmtp_ip /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-user1.txt"

	docker exec mail_override_hostname /bin/sh -c "nc 0.0.0.0 25 < /tmp/docker-mailserver-test/email-templates/existing-user1.txt"
	# Wait for mails to be analyzed
	sleep 20

tests:
	# Start tests
	./test/bats/bin/bats test/tests.bats

clean:
	# Remove running test containers
	-docker rm -f \
		mail \
		mail_pop3 \
		mail_smtponly \
		mail_smtponly_without_config \
		mail_fail2ban \
		mail_fetchmail \
		fail-auth-mailer \
		mail_disabled_clamav_spamassassin \
		mail_manual_ssl \
		ldap_for_mail \
		mail_with_ldap \
		mail_with_imap \
		mail_lmtp_ip \
		mail_with_postgrey \
		mail_override_hostname

	@if [ -f config/postfix-accounts.cf.bak ]; then\
		rm -f config/postfix-accounts.cf ;\
		mv config/postfix-accounts.cf.bak config/postfix-accounts.cf ;\
	fi
	-sudo rm -rf test/onedir \
		test/config/empty \
		test/config/without-accounts \
		test/config/without-virtual
