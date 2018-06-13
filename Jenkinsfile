pipeline {
  agent {
    node {
      label 'master'
    }

  }
  stages {
    stage('Build') {
      agent {
        node {
          label 'master'
        }

      }
      steps {
        sh '''dapp dimg build
'''
        sh 'dapp dimg tag --tag ${BUILD_NUMBER}'
        docker.image("penstock/penstock:${BUILD_NUMBER}").push()
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
      }
    }
  }
}
