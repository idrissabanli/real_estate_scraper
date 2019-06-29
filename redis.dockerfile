FROM redis:4.0.11

ENV REDIS_PASSWORD uyf0BZ350zcTOkCB

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]
