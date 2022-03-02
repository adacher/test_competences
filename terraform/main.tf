provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

resource "kubernetes_namespace" new_namespace {
  metadata {
    name = var.namespace_name
    labels = {
      nom = var.namespace_label_nom
      toto = var.namespace_label_toto
    }
  }
}


variable "namespace_name" {
  type        = string
}


variable "namespace_label_nom" {
  type        = string
}


variable "namespace_label_toto" {
  type        = string
}