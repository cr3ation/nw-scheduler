FROM alpine:3.15
ENV SLEEP 1
ENV URI http://app:8000/scheduled/
RUN apk add --no-cache curl

# Supress curl output
# CMD ["sh", "-c", "while sleep ${SLEEP}s; do curl -s ${URI}; done"]

# Verbose output
CMD ["sh", "-c", "while sleep ${SLEEP}s; do RESPONSE=$(curl -sb -H 'Accept: application/json' ${URI}); echo -n $(date +'%T') ; echo -n ' - '; echo $RESPONSE; done"]