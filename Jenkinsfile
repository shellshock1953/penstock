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
    stage('Tests') {
      agent any
      steps {
        sh 'dapp dimg run -- bin/py.test src/penstock'
        sh 'dapp dimg run -- bin/py.test src/penstock'
      }
    }
  }
}