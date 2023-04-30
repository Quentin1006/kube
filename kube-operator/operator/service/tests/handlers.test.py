import pprint
import kubernetes

pp = pprint.PrettyPrinter(indent=4)

body = {'apiVersion': 'qsahal.org/v1', 'kind': 'ConfigMapIncrementor', 'metadata': {'annotations': {'kopf.zalando.org/create_fn': '{"started":"2023-04-30T13:22:10.499269","delayed":"2023-04-30T13:32:11.825603","purpose":"create","retries":10,"success":false,"failure":false,"message":"\'set\' object has no attribute \'openapi_types\'"}', 'kopf.zalando.org/touch-dummy': '2023-04-30T13:32:11.856042', 'kubectl.kubernetes.io/last-applied-configuration': '{"apiVersion":"qsahal.org/v1","kind":"ConfigMapIncrementor","metadata":{"annotations":{},"name":"op-cmi-cr2","namespace":"custom"},"spec":{"sign":"ok"}}\n'}, 'creationTimestamp': '2023-04-30T13:22:10Z', 'finalizers': ['kopf.zalando.org/KopfFinalizerMarker'], 'generation': 21, 'managedFields': [{'apiVersion': 'qsahal.org/v1', 'fieldsType': 'FieldsV1', 'fieldsV1': {'f:metadata': {'f:annotations': {'.': {}, 'f:kubectl.kubernetes.io/last-applied-configuration': {}}}, 'f:spec': {'.': {}, 'f:sign': {}}}, 'manager': 'kubectl-client-side-apply', 'operation': 'Update', 'time': '2023-04-30T13:22:10Z'}, {
    'apiVersion': 'qsahal.org/v1', 'fieldsType': 'FieldsV1', 'fieldsV1': {'f:metadata': {'f:annotations': {'f:kopf.zalando.org/create_fn': {}, 'f:kopf.zalando.org/touch-dummy': {}}, 'f:finalizers': {'.': {}, 'v:"kopf.zalando.org/KopfFinalizerMarker"': {}}}, 'f:status': {'.': {}, 'f:kopf': {'.': {}, 'f:dummy': {}, 'f:progress': {'.': {}, 'f:create_fn': {'.': {}, 'f:delayed': {}, 'f:failure': {}, 'f:message': {}, 'f:purpose': {}, 'f:retries': {}, 'f:started': {}, 'f:success': {}}}}}}, 'manager': 'kopf', 'operation': 'Update', 'time': '2023-04-30T13:32:11Z'}], 'name': 'op-cmi-cr2', 'namespace': 'custom', 'resourceVersion': '65241', 'uid': '36f990fa-2fe6-4db7-88f7-bc1b6e51e7d5'}, 'spec': {'sign': 'ok'}, 'status': {'kopf': {'dummy': '2023-04-30T13:32:11.856042', 'progress': {'create_fn': {'delayed': '2023-04-30T13:32:11.825603', 'failure': False, 'message': "'set' object has no attribute 'openapi_types'", 'purpose': 'create', 'retries': 10, 'started': '2023-04-30T13:22:10.499269', 'success': False}}}}}


def runTest():
    name = body['metadata']['name']
    namespace = body['metadata']['namespace']

    api = kubernetes.client.CoreV1Api()

    cm = kubernetes.client.V1ConfigMap(
        kind="ConfigMap",
        api_version="v1",
        metadata=kubernetes.client.V1ObjectMeta(name=name),
        data={"sign": "ok"},
    )

    print("START cm")
    print(cm)
    print("END cm")

    api.create_namespaced_config_map(namespace=namespace, body=cm)


runTest()
