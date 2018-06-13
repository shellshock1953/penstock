pipeline {
  agent {
    node {
      label 'master'
    }

  }
  stages {
    stage('Build') {
      agent any
      steps {
        sh 'printenv'
        sh '''dapp dimg build
'''
      }
    }
    stage('Tests') {
      agent {
        node {
          label 'master'
        }

      }
      steps {
        sh 'dapp dimg run -- bin/py.test src/penstock'
        sh 'dapp dimg run -- bin/py.test src/penstock'
      }
    }
  }
}