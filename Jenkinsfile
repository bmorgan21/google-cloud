node {
  def project = 'sample-app-163923'
  def appName = 'sample-app'
  def feSvcName = "${appName}-frontend"
  def imageTag = "gcr.io/${project}/${appName}:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"

  checkout scm

  stage 'Build image'
  sh("cd sample-app; docker build -t ${imageTag} .")

  stage 'Push image to registry'
  sh("cd sample-app; gcloud docker push ${imageTag}")

  stage "Deploy Application"
  switch (env.BRANCH_NAME) {
    // Roll out to production
    case "master":
        sh("cd sample-app; sed -i.bak 's#gcr.io/sample-app-images:1.0.0#${imageTag}#' ./k8s/production/*.yml")
        sh("cd sample-app; kubectl --namespace=production apply -f k8s/services/")
        sh("cd sample-app; kubectl --namespace=production apply -f k8s/production/")
        sh("echo http://`kubectl --namespace=production get service/${feSvcName} --output=json | jq -r '.status.loadBalancer.ingress[0].ip'` > ${feSvcName}")
        break
  }
}
