pipeline {
  agent none
  stages {
    stage('Build') {
      agent any
      steps {
        sh '''printenv
dapp dimg build
'''
      }
    }
  }
  environment {
    PATH = '${env.PATH}:/usr/local/bin'
  }
}