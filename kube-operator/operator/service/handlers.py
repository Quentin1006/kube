import kopf
import kubernetes
import yaml
import pprint

pp = pprint.PrettyPrinter(indent=4)


@kopf.on.create('qsahal.org', 'v1', 'configmapincrementors')
def create_fn(body, spec, **kwargs):
    pp.pprint(body)
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']
    sign = spec['sign']

    # Make sure type is provided
    if not sign:
        raise kopf.TemporaryError(f"Type must be set. Got {sign}.")

    cm = kubernetes.client.V1ConfigMap(
        kind="ConfigMap",
        api_version="v1",
        metadata=kubernetes.client.V1ObjectMeta(name=name),
        data={"count": sign},
    )

    # Object used to communicate with the API Server
    api = kubernetes.client.CoreV1Api()

    api.create_namespaced_config_map(namespace=namespace, body=cm)

    # Make the Pod and Service the children of the Database object
    kopf.adopt(cm, owner=body)

    # Update status
    msg = f"ConfigMap  `{name}` created"
    return {'message': msg}


@kopf.on.update('qsahal.org', 'v1', 'configmapincrementors')
def update_fn(spec, old, new, diff, **_):
    print("---diff---")
    print(diff)
    pp.pprint(spec)
    pp.pprint(old)
    pp.pprint(new)
    pp.pprint(diff)

    return "ok"


@kopf.on.delete('qsahal.org', 'v1', 'configmapincrementors')
def delete(body, **kwargs):
    msg = f"Delete {body['metadata']['name']}"
    return {'message': msg}


# Run when controller is restarted
@kopf.on.resume('qsahal.org', 'v1', 'configmapincrementors')
def resume_fn(body, **kwargs):
    return {'message': "Controller resumed all configmaps"}
