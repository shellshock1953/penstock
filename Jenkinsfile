pipeline {
  agent none
  stages {
    stage('Build') {
      agent any
      steps {
        sh '''dapp dimg build
'''
      }
    }
  }
  environment {
    PATH = '$PATH:/usr/local/bin'
  }
}