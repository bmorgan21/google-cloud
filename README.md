# google-cloud

1. Set the default Compute Engine zone to us-east1-d.

    gcloud config set compute/zone us-east1-d

2. Create a Compute Engine network for the Container Engine cluster to connect to and use.

    gcloud compute networks create jenkins --mode auto

3. Provision a Kubernetes cluster using Container Engine. This step can take up to several minutes to complete.

    gcloud container clusters create jenkins-cd \
      --network jenkins \
      --scopes "https://www.googleapis.com/auth/projecthosting,storage-rw"

4. [optional] Confirm that your cluster is running.

    gcloud container clusters list

5. Get the credentials for your cluster. Container Engine uses these credentials to access your newly provisioned cluster.

    gcloud container clusters get-credentials jenkins-cd

6. [optional] Confirm that you can connect to your cluster.

    kubectl cluster-info

7. Create the Jenkins Image

    gcloud compute images create jenkins-home-image --source-uri https://storage.googleapis.com/solutions-public-assets/jenkins-cd/jenkins-home-v3.tar.gz

8. Create the Jenkins Volume

    gcloud compute disks create jenkins-home --image jenkins-home-image --zone us-east1-d

9. Set Jenkins Password (report the password for later use)

    PASSWORD=`openssl rand -base64 15`; echo "Your password is $PASSWORD"; sed -i.bak s#CHANGE_ME#$PASSWORD# jenkins/k8s/options

10. Next, create a Kubernetes namespace for Jenkins.

    kubectl create ns jenkins

11. Create a Kubernetes secret. Kubernetes uses this object to provide Jenkins with the default username and password when Jenkins boots.

    kubectl create secret generic jenkins --from-file=jenkins/k8s/options --namespace=jenkins

12. Create the Jenkins deployment

    kubectl apply -f jenkins/k8s/jenkins.yml

13. Create the Jenkins services.

    kubectl apply -f jenkins/k8s/services/

14. [optional] Confirm that the pod is running.

    kubectl get pods --namespace jenkins

15. Create a temporary SSL certificate and key pair

    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=jenkins/O=jenkins"

16. Upload the certificate to Kubernetes as a secret object.

    kubectl create secret generic tls --from-file=/tmp/tls.crt --from-file=/tmp/tls.key --namespace jenkins

17. Create the load balancer

    kubectl apply -f jenkins/k8s/ingress.yml

18. Check the status of the loab balancer (this may take awhile, continue to run the command until an Address appears) (backends status will take a while to become healthy)

    kubectl describe ingress jenkins --namespace jenkins

19. Hit IP_ADDRESS from above and login with username `jenkins` and the password found in jenkins/k8/options


20. Change into sample-app

    cd sample-app

21. Create the Kubernetes namespace to logically isolate the production deployment.

    kubectl create ns production

22. Create the production deployments and services.

    kubectl --namespace=production apply -f k8s/production
    kubectl --namespace=production apply -f k8s/services

23. Add service account credentials

    https://cloud.google.com/solutions/continuous-delivery-jenkins-container-engine#creating_a_pipeline

24. Create a Jenkins Job

    https://cloud.google.com/solutions/continuous-delivery-jenkins-container-engine#creating_a_jenkins_job

25. Update github in Settings > Integrations & services

    Add the "Jenkins (GitHub plugin)" and point to the jenkins instance "http://JENKINS_IP_DNS/github-webhook/"

