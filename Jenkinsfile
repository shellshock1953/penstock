ci_cd_params = [
    logs: "\n",
    user: "penstock",
    image: "${JOB_NAME.toLowerCase()}:${BUILD_NUMBER}",
    buildout: [branch: 'next', repo: 'https://github.com/openprocurement/penstock'],
    packages: []
]

def postPerPackage() {
    sh(encoding: 'UTF-8', script: "rm -rf output/penstock")
    unstash(name: "penstock")
}

def postPipeline() {
    junit(
        testResults: 'output/**/junit.xml',
        allowEmptyResults: true
    )
    cobertura(
        autoUpdateHealth: false,
        autoUpdateStability: false,
        coberturaReportFile: 'output/**/coverage.xml',
        conditionalCoverageTargets: '70, 0, 0',
        failNoReports: false,
        failUnhealthy: false,
        failUnstable: false,
        lineCoverageTargets: '80, 0, 0',
        maxNumberOfBuilds: 0,
        methodCoverageTargets: '80, 0, 0',
        onlyStable: false,
        sourceEncoding: 'ASCII',
        zoomCoverageChart: false,
    )
    if (currentBuild.currentResult == 'SUCCESS') {
        COLOR = 'good'
    } else {
        COLOR = 'danger'
    }

    MESSAGE = "${currentBuild.currentResult}: Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.BUILD_URL}) $ci_cd_params.logs"
    slackSend(message: MESSAGE, color: COLOR, channel: recipient)
    if (currentBuild.currentResult == 'SUCCESS') {

        docker.image("${ci_cd_params.image}").push("latest")
    }
}

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
                sh 'dapp dimg build'
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
                    docker.image("penstock:${BUILD_NUMBER}").withRun('-i', 'bash') {container ->
                        try {
                                sh "docker exec ${container.id} mkdir /tmp/output"
                                sh "docker exec ${container.id} bin/py.test --pyargs penstock -v -o 'python_files=*.py' --doctest-modules --junitxml=/tmp/output/junit.xml --cov-report xml:/tmp/output/coverage.xml --cov-report term --cov=penstock"
                        }
                        finally {
                            sh(
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
        post {
            always {
                script {
                    node('master') {
                        postPerPackage()
                    }
                }
            }
        }
    }
}