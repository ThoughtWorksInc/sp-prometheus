def build_image(cli, dockerfile, workspace, image_name):
    for response in cli.build(
            dockerfile=dockerfile,
            path=workspace,
            tag=image_name,
            rm=True,
            nocache=True,
            decode=True
    ):
        if response.has_key('error'):
            raise Exception("Error building docker image: {}".format(response['error']))
            # print response.encode("utf-8")


def push_to_registry(cli, image_name, insecure_registry=True):
    log = cli.push(image_name, insecure_registry=insecure_registry)
    print log
