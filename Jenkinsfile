ci_cd_params = [
    logs: "\n",
    user: "penstock",
    tag: "${BRANCH_NAME.toLowerCase()}-${BUILD_NUMBER}",
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

    MESSAGE = "${currentBuild.currentResult}: Job ${env.JOB_NAME} [${env.BUILD_NUMBER}] (${env.RUN_DISPLAY_URL}) $ci_cd_params.logs"
    slackSend(message: MESSAGE, color: COLOR)
    if (currentBuild.currentResult == 'SUCCESS') {
        sh 'dapp dimg tag --tag ${BRANCH_NAME.toLowerCase()}-latest component penstock'
        script {
            docker.image("penstock/component:${BRANCH_NAME.toLowerCase()}-latest").push()
        }
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
                sh 'dapp dimg build component'
                sh 'dapp dimg tag --tag ${ci_cd_params.tag} component penstock'
                script {
                    docker.image("penstock/component:${ci_cd_params.tag}").push()
                }
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
                    docker.image("penstock/component:${ci_cd_params.tag}").withRun('-i', 'bash') {container ->
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
        stage('RPM') {
            agent {
                node {
                    label 'master'
                }
            }            
            when {
                anyOf {
                    branch 'next'
                }
            }
            steps {
                sh 'dapp dimg build rpm'
                sh 'dapp dimg tag --tag ${ci_cd_params.tag} rpm penstock'
                script {
                    docker.image("penstock/rpm:${ci_cd_params.tag}").withRun('-i', 'bash') {container ->
                        sh(script: "mkdir target")
                        sh(script: "docker cp ${container.id}:/root/rpmbuild/RPMS/x86_64/. target")
                    }
                }
                archiveArtifacts artifacts: 'target/*.rpm', fingerprint: true
            }

        }


    }
    post {
        always {
            script {
                node('master') {
                    postPerPackage()
                    postPipeline()
                }
            }
        }
    }
}