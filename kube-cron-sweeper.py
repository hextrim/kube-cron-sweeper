import subprocess
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

def helm_delete_release(ns_name):
    helm_list_releases_in_namespace = subprocess.Popen(["helm", "ls", "--namespace", ns_name, "--short"], stdout=subprocess.PIPE)
    helm_delete_releases_in_namespace = subprocess.Popen(["xargs", "-L1", "helm", "delete", "--purge"], stdin=helm_list_releases_in_namespace.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    helm_delete_releases_in_namespace_stdout, helm_delete_releases_in_namespace_stderr = helm_delete_releases_in_namespace.communicate()
    print('Namespace: ' + ns_name + ' results with: ' + helm_delete_releases_in_namespace_stdout.decode("utf-8")) 
    print('Namespace: ' + ns_name + ' errors with: ' + helm_delete_releases_in_namespace_stderr.decode("utf-8"))

def k8s_delete_ns(ns_name):
    body = client.V1DeleteOptions()
    try:
        v1.delete_namespace(name=ns_name, body=body)
        print('Namespace: ' + ns_name + ' deleted.\n')
    except ApiException:
        print('Namespace: ' + ns_name + ' does not exist.\n')
        pass

config.load_incluster_config()

v1 = client.CoreV1Api()

namespaces = v1.list_namespace(watch=False)
filter_projects = ['app-master']
namespaces_list = []
for item in namespaces.items:
    namespaces_list.append(str(item.metadata.name))

namespaces_filtered = [n for n in namespaces_list if n.startswith('app') and n not in filter_projects]

print('## App Namespaces to skip:')
print(filter_projects)
print('## App Namespaces to delete:')
print(namespaces_filtered)

#for ns in filter_projects:
for ns in namespaces_filtered:
    print('[i] For namespace: ' + ns + ' executing...')
    helm_delete_release(ns)
    k8s_delete_ns(ns)
