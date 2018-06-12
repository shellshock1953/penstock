pipeline {
  agent any
  stages {
    stage('error') {
      agent any
      steps {
        git(changelog: true, url: 'https://github.com/ktarasz/temp.git', branch: 'master', poll: true)
        sh 'printenv'
      }
    }
  }
}