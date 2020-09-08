Creating app environment:

Create AKS cluster from the template:

Register the cluster with kubectl

Deploy basic infrastructure

This will now look into the repository and deploy the app automatically


`
GROUP_NAME=niceproject
LOCATION=northeurope

az group create -l $LOCATION -n $GROUP_NAME

az deployment group create -f deployment/azure/template.json -p @deployment/azure/parameters.json -g $GROUP_NAME

az aks get-credentials -g GROUP_NAME -n niceprojectcluster
`

`
GIT_URL=git@github.com:sergiuszrokoszdxc/nice_project.git

kubectl create namespace flux

helm upgrade -i flux fluxcd/flux --set git.url=$GIT_URL --set git.path=deployment --namespace flux

helm upgrade -i helm-operator fluxcd/helm-operator --set git.ssh.secretName=flux-git-deploy --set helm.versions=v3 --namespace flux
`

`
fluxctl identity --k8s-fwd-ns flux
`