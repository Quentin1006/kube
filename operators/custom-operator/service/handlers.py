import kopf
import kubernetes
import time
import random
import os



@kopf.on.create('qsahal.org', 'v1', 'configmapincrementors')
def create_fn(body, spec, **kwargs):
    print("\n-------------------START CREATING-------------------\n")
    print("VERSION :", os.environ["VERSION"]) 
    print("sha ;", 1221)
    print("body =>", body)

    name = body['metadata']['name']
    namespace = body['metadata']['namespace']
    sign = spec['sign']

    rand_int = random.randint(1, 10)


    if rand_int < int(sign):
        message = f"sign {sign} is above generated rand {rand_int}"
        print(message)
        raise kopf.PermanentError(message)

    cm = kubernetes.client.V1ConfigMap(
        kind="ConfigMap",
        api_version="v1",
        metadata=kubernetes.client.V1ObjectMeta(name=name),
        data={"count": sign, "date": f"${int(time.time())}"},
    )

    # Object used to communicate with the API Server
    api = kubernetes.client.CoreV1Api()

    api.create_namespaced_config_map(namespace=namespace, body=cm)

    # Update status
    msg = f"ConfigMap  `{name}` created"
    print("\n-------------------END CREATING-------------------\n")
    return {'message': msg}


@kopf.on.update('qsahal.org', 'v1', 'configmapincrementors')
def update_fn(spec, old, new, diff, **_):
    print("\n-------------------START UPDATING-------------------\n")
    print("---diff---")
    print("diff =>", diff)
    print("spec =>", spec)
    print("old =>", old)
    print("new =>", new)
    print("\n-------------------END UPDATING-------------------\n")

    raise kopf.TemporaryError("Error updating.", delay=60)


@kopf.on.delete('qsahal.org', 'v1', 'configmapincrementors')
def delete(body, **kwargs):

    api = kubernetes.client.CoreV1Api()
    api.create_namespaced_config_map(namespace=namespace, body=cm)
    msg = f"Delete {body['metadata']['name']}"
    return {'message': msg}


# Run when controller is restarted
@kopf.on.resume('qsahal.org', 'v1', 'configmapincrementors')
def resume_fn(body, **kwargs):
    print("\n\n-------------------START RESUMING-------------------\n\n")
    print("body =>", body)
    print("\n-------------------END RESUMING-------------------\n")
    return {'message': "Controller resumed all configmaps"}
