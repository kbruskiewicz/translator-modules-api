openapi-generator generate --input-spec=translator-modules-api.yaml \
                    --output=server \
                    --generator-name=python-flask \
                    --package-name=cwl_server \
	                --model-package=models \
	                --artifact-version=0.0.1 \
	                --additional-properties=\
"projectName=ncats_cwl_server,packageName=cwl_server,packageVersion=0.0.1,packageUrl=https://github.com/ncats/translator-modules/master/cwl_server,serverPort=8090"