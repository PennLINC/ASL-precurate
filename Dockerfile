# GDCM
# Start with Alpine Linux
FROM alpine:3.8

#LABEL Tinashe M. Tapera <taperat@pennmedicine.upenn.edu>

RUN apk --update add ca-certificates && apk upgrade

RUN apk add cmake>3.12-suffix
RUN apk add alpine-sdk perl tzdata && \
    mkdir -p /opt/GDCM/BUILD && cd /opt/GDCM && \
    git clone -b 'release' --depth=1 https://github.com/malaterre/GDCM.git && \
    cd /opt/GDCM/BUILD && \
    cmake -DCMAKE_BUILD_TYPE=Release -DGDCM_BUILD_SHARED_LIBS:BOOL=ON -DGDCM_BUILD_TESTING:BOOL=OFF -DGDCM_BUILD_APPLICATIONS:BOOL=ON /opt/GDCM/GDCM && \
    make && make install && rm -rf /opt/GDCM && \
    apk del --purge alpine-sdk perl tzdata cmake && apk add libstdc++

RUN mkdir -p /inputs && \
    mkdir -p /outputs

ENTRYPOINT ["gdcmdump", "--csa"]
