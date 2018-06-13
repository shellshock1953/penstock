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
        sh 'dapp dimg spush penstock --tag ${BUILD_NUMBER}' 
      }
    }
    stage('Tests') {
      agent {
        node {
          label 'slave'
        }
      }
     
      steps {
        sh "rm -rf output/penstock"
        sh "mkdir -p output"
        script {
           docker.image("penstock:${BUILD_NUMBER}").withRun('bash') { container ->
             try {
               sh "docker exec ${container.id} mkdir /tmp/output"
               sh "docker exec ${container.id} bin/py.test --pyargs penstock -v -o 'python_files=*.py' --doctest-modules --junitxml=/tmp/output/junit.xml --cov-report xml:/tmp/output/coverage.xml --cov-report term --cov=penstock"
             }
             finally {
               sh (
                 encoding: 'UTF-8',
                 script: "docker cp ${container.id}:/tmp/output/ output/penstock"
               )
               stash(
                 name: "penstock",
                 includes: "output/penstock/*",
                 allowEmpty: true
               )
             }
           }
        }
      }
    }
  }
}
