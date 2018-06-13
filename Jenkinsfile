pipeline {
  agent any
  stages {
    stage('Build') {
      agent any
      steps {
        sh '''/usr/local/bin/dapp dimg build
'''
      }
    }
  }
}